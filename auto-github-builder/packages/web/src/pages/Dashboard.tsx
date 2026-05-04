import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import StreakCard from '../components/StreakCard';
import ProjectGenerator from '../components/ProjectGenerator';

function Dashboard() {
  const [streak, setStreak] = useState({ current: 0, longest: 0, totalCommits: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const username = localStorage.getItem('github_username') || 'User';

  useEffect(() => {
    const fetchStreak = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`/api/users/${username}/streak`);
        setStreak(response.data.streak);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch streak:', err);
        setError('Could not load streak data');
        // Use default values
        setStreak({ current: 0, longest: 0, totalCommits: 0 });
      } finally {
        setLoading(false);
      }
    };

    fetchStreak();
  }, [username]);

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
      <Navbar />
      <div className="container" style={{ paddingTop: '32px', paddingBottom: '32px' }}>
        <h1 style={{ color: 'white', marginBottom: '32px' }}>Welcome back, {username}! 👋</h1>
        
        {error && (
          <div style={{ background: '#fecaca', color: '#991b1b', padding: '16px', borderRadius: '8px', marginBottom: '24px' }}>
            {error}
          </div>
        )}
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '24px', marginBottom: '32px' }}>
          {loading ? (
            <>
              <div className="card" style={{ height: '150px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>Loading...</div>
              <div className="card" style={{ height: '150px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>Loading...</div>
              <div className="card" style={{ height: '150px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>Loading...</div>
            </>
          ) : (
            <>
              <StreakCard
                label="Current Streak 🔥"
                value={streak.current}
                unit="days"
              />
              <StreakCard
                label="Longest Streak"
                value={streak.longest}
                unit="days"
              />
              <StreakCard
                label="Total Commits"
                value={streak.totalCommits}
                unit="commits"
              />
            </>
          )}
        </div>

        <ProjectGenerator />
      </div>
    </div>
  );
}

export default Dashboard;
