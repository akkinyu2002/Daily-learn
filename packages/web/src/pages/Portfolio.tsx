import React from 'react';
import Navbar from '../components/Navbar';

function Portfolio() {
  const username = localStorage.getItem('github_username');

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
      <Navbar />
      <div className="container" style={{ paddingTop: '32px', paddingBottom: '32px' }}>
        <div className="card" style={{ background: 'white' }}>
          <h1>📊 Your Portfolio</h1>
          <p style={{ color: '#666', marginBottom: '32px' }}>Showcase all your auto-generated projects here.</p>
          
          <div style={{ marginTop: '32px', textAlign: 'center', padding: '48px 24px', background: '#f9fafb', borderRadius: '8px' }}>
            <p style={{ fontSize: '48px', marginBottom: '16px' }}>🚀</p>
            <p style={{ color: '#666', fontSize: '16px' }}>Portfolio visualization coming soon!</p>
            <p style={{ fontSize: '14px', color: '#999', marginTop: '16px' }}>
              Your projects are being generated and stored at:{' '}
              <code style={{ background: '#f0f0f0', padding: '4px 8px', borderRadius: '4px', display: 'inline-block', marginTop: '8px' }}>
                github.com/{username}/auto-projects
              </code>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Portfolio;
