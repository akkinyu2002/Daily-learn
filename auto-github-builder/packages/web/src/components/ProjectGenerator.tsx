import React, { useState } from 'react';
import axios from 'axios';

function ProjectGenerator() {
  const [loading, setLoading] = useState(false);
  const [lastProject, setLastProject] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const token = localStorage.getItem('github_token');
  const username = localStorage.getItem('github_username');

  const handleGenerateProject = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('/api/projects/generate-and-commit', {
        token,
        owner: username,
        repo: 'auto-projects',
        branch: 'main',
      });
      setLastProject(response.data.project);
    } catch (err: any) {
      console.error('Generation error:', err);
      setError(err.response?.data?.error || 'Failed to generate project');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card" style={{ background: 'white' }}>
      <h2>✨ Generate Project</h2>
      <p style={{ color: '#666', marginBottom: '24px' }}>
        Create a new random project and commit it to your repository.
      </p>
      
      {error && (
        <div style={{ background: '#fecaca', color: '#991b1b', padding: '12px', borderRadius: '6px', marginBottom: '16px', fontSize: '14px' }}>
          {error}
        </div>
      )}

      <button
        className="btn btn-primary"
        onClick={handleGenerateProject}
        disabled={loading}
        style={{ minWidth: '200px', marginBottom: lastProject ? '24px' : '0' }}
      >
        {loading ? 'Generating...' : 'Generate Now'}
      </button>

      {lastProject && (
        <div style={{ marginTop: '24px', padding: '16px', background: '#f0f9ff', borderRadius: '6px', border: '1px solid #bfdbfe' }}>
          <p style={{ fontSize: '12px', color: '#666', marginBottom: '8px' }}>Last Generated</p>
          <p style={{ fontSize: '18px', fontWeight: 'bold', color: '#333' }}>{lastProject.name}</p>
          <p style={{ fontSize: '12px', color: '#666' }}>Type: {lastProject.type}</p>
        </div>
      )}
    </div>
  );
}

export default ProjectGenerator;
