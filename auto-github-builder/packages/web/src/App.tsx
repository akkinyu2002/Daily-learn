import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Portfolio from './pages/Portfolio';
import Settings from './pages/Settings';
import OAuthCallback from './pages/OAuthCallback';
import './styles/global.css';

interface AppState {
  isAuthenticated: boolean | null;
  isLoading: boolean;
  error: string | null;
}

class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean; error: Error | null }
> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('App Error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '100vh',
          background: '#fee2e2',
          fontFamily: 'system-ui, -apple-system, sans-serif',
          padding: '20px',
        }}>
          <div style={{
            background: 'white',
            padding: '32px',
            borderRadius: '8px',
            maxWidth: '600px',
            color: '#991b1b',
          }}>
            <h1 style={{ marginBottom: '12px' }}>⚠️ Application Error</h1>
            <p style={{ marginBottom: '16px' }}>Something went wrong:</p>
            <pre style={{
              background: '#f5f5f5',
              padding: '12px',
              borderRadius: '4px',
              overflow: 'auto',
              fontSize: '12px',
            }}>
              {this.state.error?.message}
            </pre>
            <p style={{ marginTop: '16px', fontSize: '14px' }}>
              Check the browser console (F12) for more details.
            </p>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

function AppContent() {
  const [state, setState] = useState<AppState>({
    isAuthenticated: null,
    isLoading: true,
    error: null,
  });

  useEffect(() => {
    try {
      console.log('[App] Checking authentication...');
      const token = localStorage.getItem('github_token');
      const authStatus = !!token;
      console.log('[App] Auth status:', authStatus);
      
      setState({
        isAuthenticated: authStatus,
        isLoading: false,
        error: null,
      });
    } catch (err) {
      console.error('[App] Auth check failed:', err);
      setState({
        isAuthenticated: false,
        isLoading: false,
        error: `Auth check failed: ${err}`,
      });
    }
  }, []);

  if (state.isLoading) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        fontFamily: 'system-ui, -apple-system, sans-serif',
      }}>
        <div style={{ color: 'white', fontSize: '24px', fontWeight: 'bold' }}>
          Loading...
        </div>
      </div>
    );
  }

  if (state.error) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        background: '#fee2e2',
        fontFamily: 'system-ui, -apple-system, sans-serif',
        padding: '20px',
      }}>
        <div style={{
          background: 'white',
          padding: '32px',
          borderRadius: '8px',
          color: '#991b1b',
          textAlign: 'center',
        }}>
          <h2>Error Loading App</h2>
          <p>{state.error}</p>
        </div>
      </div>
    );
  }

  console.log('[App] Rendering with isAuthenticated:', state.isAuthenticated);

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            state.isAuthenticated ? (
              <Navigate to="/dashboard" replace />
            ) : (
              <Login setIsAuthenticated={(value: boolean) => {
                console.log('[App] Auth state changed to:', value);
                setState(prev => ({ ...prev, isAuthenticated: value }));
              }} />
            )
          }
        />
        <Route
          path="/auth/github/callback"
          element={
            <OAuthCallback setIsAuthenticated={(value: boolean) => {
              setState(prev => ({ ...prev, isAuthenticated: value }));
            }} />
          }
        />
        <Route
          path="/dashboard"
          element={
            state.isAuthenticated ? (
              <Dashboard />
            ) : (
              <Navigate to="/" replace />
            )
          }
        />
        <Route
          path="/portfolio"
          element={
            state.isAuthenticated ? (
              <Portfolio />
            ) : (
              <Navigate to="/" replace />
            )
          }
        />
        <Route
          path="/settings"
          element={
            state.isAuthenticated ? (
              <Settings setIsAuthenticated={(value: boolean) => {
                setState(prev => ({ ...prev, isAuthenticated: value }));
              }} />
            ) : (
              <Navigate to="/" replace />
            )
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <AppContent />
    </ErrorBoundary>
  );
}

export default App;
