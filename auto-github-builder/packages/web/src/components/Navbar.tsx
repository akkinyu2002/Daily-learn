import React from 'react';
import { Link, useLocation } from 'react-router-dom';

function Navbar() {
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path ? '#667eea' : '#666';
  };

  return (
    <nav style={{ background: 'rgba(255, 255, 255, 0.95)', boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)', position: 'sticky', top: 0, zIndex: 100 }}>
      <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', height: '60px', padding: '0 20px' }}>
        <Link to="/dashboard" style={{ textDecoration: 'none', color: '#667eea', fontSize: '20px', fontWeight: 'bold' }}>
          🚀 AGB
        </Link>
        <div style={{ display: 'flex', gap: '32px', alignItems: 'center' }}>
          <Link 
            to="/dashboard" 
            style={{ 
              textDecoration: 'none', 
              color: isActive('/dashboard'),
              fontWeight: location.pathname === '/dashboard' ? '600' : '400',
              transition: 'color 0.3s'
            }}
          >
            Dashboard
          </Link>
          <Link 
            to="/portfolio" 
            style={{ 
              textDecoration: 'none', 
              color: isActive('/portfolio'),
              fontWeight: location.pathname === '/portfolio' ? '600' : '400',
              transition: 'color 0.3s'
            }}
          >
            Portfolio
          </Link>
          <Link 
            to="/settings" 
            style={{ 
              textDecoration: 'none', 
              color: isActive('/settings'),
              fontWeight: location.pathname === '/settings' ? '600' : '400',
              transition: 'color 0.3s'
            }}
          >
            Settings
          </Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
