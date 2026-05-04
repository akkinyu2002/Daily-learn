import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';

interface OAuthCallbackProps {
  setIsAuthenticated: (value: boolean) => void;
}

function OAuthCallback({ setIsAuthenticated }: OAuthCallbackProps) {
  const [searchParams] = useSearchParams();
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const oauthError = searchParams.get('error');
    const token = searchParams.get('token');
    const username = searchParams.get('username');

    if (oauthError) {
      setError(oauthError);
      return;
    }

    if (!token || !username) {
      setError('GitHub did not return login details.');
      return;
    }

    localStorage.setItem('github_token', token);
    localStorage.setItem('github_username', username);
    setIsAuthenticated(true);
    navigate('/dashboard', { replace: true });
  }, [navigate, searchParams, setIsAuthenticated]);

  if (error) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      }}>
        <div className="card" style={{ maxWidth: '420px', width: '100%', margin: '20px' }}>
          <h1 style={{ color: '#991b1b', marginBottom: '12px' }}>GitHub Sign-In Failed</h1>
          <p style={{ color: '#4b5563', marginBottom: '20px' }}>{error}</p>
          <button
            type="button"
            className="btn btn-primary"
            style={{ width: '100%' }}
            onClick={() => navigate('/', { replace: true })}
          >
            Back to Sign In
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      color: 'white',
      fontFamily: 'system-ui, -apple-system, sans-serif',
      fontSize: '20px',
      fontWeight: 700,
    }}>
      Finishing GitHub sign-in...
    </div>
  );
}

export default OAuthCallback;
