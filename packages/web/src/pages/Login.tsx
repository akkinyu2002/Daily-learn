import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

interface LoginProps {
  setIsAuthenticated: (value: boolean) => void;
}

function Login({ setIsAuthenticated }: LoginProps) {
  const [method, setMethod] = useState<'token' | 'oauth'>('token');
  const [token, setToken] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleTokenSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('/api/auth/validate-token', { token });
      localStorage.setItem('github_token', token);
      localStorage.setItem('github_username', response.data.user.login);
      setIsAuthenticated(true);
      navigate('/dashboard', { replace: true });
    } catch (err: any) {
      console.error('Auth error:', err);
      setError(err.response?.data?.error || 'Invalid token. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
      <div className="card" style={{ maxWidth: '400px', width: '100%', margin: '20px' }}>
        <h1 style={{ textAlign: 'center', color: '#667eea', marginBottom: '32px' }}>🚀 Auto GitHub Builder</h1>
        
        <div style={{ marginBottom: '24px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
          <button
            onClick={() => setMethod('token')}
            className={`btn ${method === 'token' ? 'btn-primary' : 'btn-secondary'}`}
            style={{ width: '100%' }}
          >
            Token
          </button>
          <button
            onClick={() => setMethod('oauth')}
            className={`btn ${method === 'oauth' ? 'btn-primary' : 'btn-secondary'}`}
            style={{ width: '100%' }}
          >
            OAuth
          </button>
        </div>

        {error && (
          <div style={{ background: '#fecaca', color: '#991b1b', padding: '12px', borderRadius: '6px', marginBottom: '16px', fontSize: '14px' }}>
            {error}
          </div>
        )}

        {method === 'token' ? (
          <form onSubmit={handleTokenSubmit}>
            <input
              type="password"
              placeholder="GitHub Personal Access Token"
              value={token}
              onChange={(e) => setToken(e.target.value)}
              required
              disabled={loading}
            />
            <button
              type="submit"
              className="btn btn-primary"
              style={{ width: '100%', marginBottom: '16px' }}
              disabled={loading}
            >
              {loading ? 'Authenticating...' : 'Sign In'}
            </button>
            <p style={{ fontSize: '12px', marginTop: '12px', color: '#666' }}>
              Need a token? <a href="https://github.com/settings/tokens" target="_blank" rel="noreferrer" style={{ color: '#667eea' }}>Create one here</a>
            </p>
          </form>
        ) : (
          <button
            className="btn btn-primary"
            style={{ width: '100%' }}
            onClick={() => window.location.href = '/api/auth/github'}
          >
            Sign in with GitHub
          </button>
        )}
      </div>
    </div>
  );
}

export default Login;
