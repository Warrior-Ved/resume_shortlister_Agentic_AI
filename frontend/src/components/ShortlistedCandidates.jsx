import React, { useState } from 'react';

const ShortlistedCandidates = ({ candidates }) => {
  const [expandedCards, setExpandedCards] = useState({});

  const toggleCard = (index) => {
    setExpandedCards(prev => ({
      ...prev,
      [index]: !prev[index]
    }));
  };

  if (!candidates || candidates.length === 0) {
    return (
      <div className="card-modern">
        <h3>✨ Shortlisted Candidates</h3>
        <p style={{ color: '#64748b', textAlign: 'center', padding: '2rem 0' }}>
          No candidates shortlisted yet. Complete the shortlisting process to see results.
        </p>
      </div>
    );
  }

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.9) return '#10b981';
    if (confidence >= 0.8) return '#3b82f6';
    if (confidence >= 0.7) return '#f59e0b';
    return '#64748b';
  };

  return (
    <div className="card-modern">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h3 style={{ margin: 0 }}>✨ Shortlisted Candidates</h3>
        <span style={{
          background: '#10b981',
          color: 'white',
          padding: '0.5rem 1rem',
          borderRadius: '20px',
          fontWeight: '600',
          fontSize: '0.9rem'
        }}>
          {candidates.length} Selected
        </span>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {candidates.map((candidate, index) => (
          <div
            key={index}
            style={{
              background: '#f8fafc',
              borderRadius: '12px',
              overflow: 'hidden',
              border: '1px solid #e2e8f0',
              transition: 'all 0.3s'
            }}
          >
            <div
              onClick={() => toggleCard(index)}
              style={{
                padding: '1.25rem',
                cursor: 'pointer',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                background: expandedCards[index] ? 'white' : '#f8fafc',
                transition: 'all 0.3s'
              }}
            >
              <div style={{ flex: 1 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '0.5rem' }}>
                  <div style={{
                    width: '40px',
                    height: '40px',
                    borderRadius: '50%',
                    background: `linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)`,
                    color: 'white',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontWeight: '700',
                    fontSize: '1.1rem'
                  }}>
                    {candidate.name.charAt(0)}
                  </div>
                  <div>
                    <h4 style={{ margin: 0, fontSize: '1.1rem', color: '#1e293b' }}>
                      {candidate.name}
                    </h4>
                    {candidate.email && (
                      <p style={{ margin: '0.25rem 0 0 0', color: '#64748b', fontSize: '0.85rem' }}>
                        📧 {candidate.email}
                      </p>
                    )}
                  </div>
                </div>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <div style={{
                  padding: '0.5rem 1rem',
                  borderRadius: '20px',
                  background: getConfidenceColor(candidate.confidence),
                  color: 'white',
                  fontWeight: '700',
                  fontSize: '0.95rem'
                }}>
                  {(candidate.confidence * 100).toFixed(0)}%
                </div>
                <span style={{
                  fontSize: '1.5rem',
                  color: '#6366f1',
                  transition: 'transform 0.3s',
                  transform: expandedCards[index] ? 'rotate(180deg)' : 'rotate(0deg)'
                }}>
                  ▼
                </span>
              </div>
            </div>

            {expandedCards[index] && (
              <div style={{
                padding: '1.5rem',
                background: 'white',
                borderTop: '1px solid #e2e8f0',
                animation: 'slideDown 0.3s ease-out'
              }}>
                {candidate.experience !== null && candidate.experience !== undefined && (
                  <div style={{ marginBottom: '1rem' }}>
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem',
                      marginBottom: '0.5rem'
                    }}>
                      <span style={{ fontSize: '1.2rem' }}>💼</span>
                      <strong style={{ color: '#1e293b' }}>Experience:</strong>
                    </div>
                    <span style={{ color: '#64748b', marginLeft: '1.75rem' }}>
                      {candidate.experience} years
                    </span>
                  </div>
                )}

                {candidate.skills && candidate.skills.length > 0 && (
                  <div style={{ marginBottom: '1rem' }}>
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem',
                      marginBottom: '0.75rem'
                    }}>
                      <span style={{ fontSize: '1.2rem' }}>🛠️</span>
                      <strong style={{ color: '#1e293b' }}>Skills:</strong>
                    </div>
                    <div style={{
                      display: 'flex',
                      flexWrap: 'wrap',
                      gap: '0.5rem',
                      marginLeft: '1.75rem'
                    }}>
                      {candidate.skills.map((skill, idx) => (
                        <span key={idx} style={{
                          background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                          color: 'white',
                          padding: '0.4rem 0.75rem',
                          borderRadius: '6px',
                          fontSize: '0.85rem',
                          fontWeight: '500'
                        }}>
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {candidate.cover_letter && (
                  <div style={{ marginBottom: '1rem' }}>
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem',
                      marginBottom: '0.75rem'
                    }}>
                      <span style={{ fontSize: '1.2rem' }}>💬</span>
                      <strong style={{ color: '#1e293b' }}>AI-Generated Cover Letter:</strong>
                    </div>
                    <div style={{
                      background: '#f8fafc',
                      padding: '1rem',
                      borderRadius: '8px',
                      marginLeft: '1.75rem',
                      fontSize: '0.9rem',
                      lineHeight: '1.6',
                      color: '#475569',
                      fontStyle: 'italic',
                      borderLeft: '3px solid #6366f1'
                    }}>
                      {candidate.cover_letter}
                    </div>
                  </div>
                )}

                {candidate.cv_path && (
                  <div style={{
                    marginTop: '1rem',
                    paddingTop: '1rem',
                    borderTop: '1px solid #e2e8f0'
                  }}>
                    <span style={{ fontSize: '0.85rem', color: '#64748b' }}>
                      📄 Resume: {candidate.cv_path}
                    </span>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ShortlistedCandidates;
