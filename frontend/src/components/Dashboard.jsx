import React from 'react';

const Dashboard = ({ jobStatus }) => {
  if (!jobStatus) {
    return null;
  }

  const getStatusColor = (status) => {
    const colors = {
      'pending': '#f59e0b',
      'uploaded': '#3b82f6',
      'processing': '#8b5cf6',
      'phase1': '#6366f1',
      'phase2': '#8b5cf6',
      'completed': '#10b981',
      'error': '#ef4444',
    };
    return colors[status] || '#64748b';
  };

  const stats = [
    {
      label: 'Total Resumes',
      value: jobStatus.total_resumes,
      icon: '📄',
      color: '#3b82f6'
    },
    {
      label: 'Phase 1 Passed',
      value: jobStatus.phase1_completed,
      icon: '🔍',
      color: '#6366f1'
    },
    {
      label: 'Phase 2 Reviewed',
      value: jobStatus.phase2_completed,
      icon: '🤖',
      color: '#8b5cf6'
    },
    {
      label: 'Final Shortlist',
      value: jobStatus.shortlisted_count,
      icon: '✨',
      color: '#10b981'
    }
  ];

  return (
    <div className="card-modern">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h3 style={{ margin: 0 }}>📊 Job Dashboard</h3>
        <span
          style={{
            padding: '0.5rem 1rem',
            borderRadius: '20px',
            fontSize: '0.85rem',
            fontWeight: '600',
            background: getStatusColor(jobStatus.status),
            color: 'white'
          }}
        >
          {jobStatus.status.toUpperCase()}
        </span>
      </div>

      <div style={{ marginBottom: '1.5rem' }}>
        <h4 style={{ fontSize: '1.25rem', color: '#1e293b', marginBottom: '0.25rem' }}>
          {jobStatus.job_title}
        </h4>
        <p style={{ color: '#64748b', fontSize: '0.9rem', margin: 0 }}>
          Created {new Date(jobStatus.created_at).toLocaleString()}
        </p>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
        gap: '1rem'
      }}>
        {stats.map((stat, index) => (
          <div
            key={index}
            style={{
              background: '#f8fafc',
              padding: '1rem',
              borderRadius: '8px',
              border: '1px solid #e2e8f0',
              transition: 'all 0.3s'
            }}
          >
            <div style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>
              {stat.icon}
            </div>
            <div style={{ fontSize: '1.75rem', fontWeight: '700', color: stat.color }}>
              {stat.value}
            </div>
            <div style={{ fontSize: '0.85rem', color: '#64748b', marginTop: '0.25rem' }}>
              {stat.label}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
