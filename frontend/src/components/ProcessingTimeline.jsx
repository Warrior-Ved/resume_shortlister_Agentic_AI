import React from 'react';

const ProcessingTimeline = ({ steps }) => {
  return (
    <div className="card-modern timeline-card">
      <h3>📊 Processing Timeline</h3>
      <div className="timeline">
        {steps.map((step, index) => (
          <div key={index} className={`timeline-item ${step.status}`}>
            <div className="timeline-marker">
              <span className="timeline-icon">{step.icon}</span>
              {index < steps.length - 1 && <div className="timeline-line"></div>}
            </div>
            <div className="timeline-content">
              <h4>{step.name}</h4>
              {step.detail && <p className="timeline-detail">{step.detail}</p>}
              {step.time && <span className="timeline-time">{step.time}</span>}
              {step.progress !== undefined && step.status === 'in-progress' && (
                <div className="progress-bar">
                  <div
                    className="progress-fill"
                    style={{ width: `${step.progress}%` }}
                  ></div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProcessingTimeline;
