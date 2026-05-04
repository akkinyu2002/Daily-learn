import React from 'react';
import Navbar from '../components/Navbar';
import { useNavigate } from 'react-router-dom';

interface SettingsProps {
  setIsAuthenticated: (value: boolean) => void;
}

function Settings({ setIsAuthenticated }: SettingsProps) {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('github_token');
    localStorage.removeItem('github_username');
    setIsAuthenticated(false);
    navigate('/', { replace: true });
  };

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
      <Navbar />
      <div className="container" style={{ paddingTop: '32px', paddingBottom: '32px' }}>
        <div className="card" style={{ background: 'white' }}>
          <h1>⚙️ Settings</h1>
          
          <div style={{ marginTop: '32px' }}>
            <h3>Schedule</h3>
            <p style={{ color: '#666', marginBottom: '16px' }}>Configure when projects are generated</p>
            
            <label style={{ display: 'block', marginBottom: '16px' }}>
              <input type="radio" name="schedule" defaultChecked /> Daily at 9 AM
            </label>
            <label style={{ display: 'block', marginBottom: '16px' }}>
              <input type="radio" name="schedule" /> Daily at 12 PM
            </label>
            <label style={{ display: 'block', marginBottom: '32px' }}>
              <input type="radio" name="schedule" /> Daily at 6 PM
            </label>

            <button className="btn btn-primary">Save Schedule</button>
          </div>

          <div style={{ marginTop: '48px', paddingTop: '32px', borderTop: '1px solid #eee' }}>
            <h3>Danger Zone</h3>
            <button
              className="btn"
              onClick={handleLogout}
              style={{ background: '#ef4444', color: 'white' }}
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Settings;
