import React from 'react';

interface StreakCardProps {
  label: string;
  value: number;
  unit: string;
}

function StreakCard({ label, value, unit }: StreakCardProps) {
  return (
    <div className="card" style={{ textAlign: 'center' }}>
      <p style={{ color: '#666', marginBottom: '12px' }}>{label}</p>
      <p style={{ fontSize: '48px', fontWeight: 'bold', color: '#667eea', marginBottom: '8px' }}>
        {value}
      </p>
      <p style={{ color: '#999', fontSize: '12px' }}>{unit}</p>
    </div>
  );
}

export default StreakCard;
