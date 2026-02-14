import React, { useState } from 'react';

const JobPostingForm = ({ onJobCreated }) => {
  const [formData, setFormData] = useState({
    job_title: '',
    description: '',
    required_tech_stack: '',
    minimum_experience: 0,
    hiring_slots: 1,
    phase1_shortlist_count: 10,
    phase2_shortlist_count: 5,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'minimum_experience' || name === 'hiring_slots' ||
              name === 'phase1_shortlist_count' || name === 'phase2_shortlist_count'
        ? parseInt(value) || 0
        : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Convert comma-separated tech stack to array
    const jobData = {
      ...formData,
      required_tech_stack: formData.required_tech_stack
        .split(',')
        .map(skill => skill.trim())
        .filter(skill => skill.length > 0)
    };

    onJobCreated(jobData);
  };

  return (
    <div className="card-modern" style={{ maxWidth: '900px', margin: '0 auto' }}>
      <div style={{ marginBottom: '2rem' }}>
        <h2 style={{
          fontSize: '1.75rem',
          color: '#1e293b',
          marginBottom: '0.5rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.75rem'
        }}>
          📝 Create Job Posting
        </h2>
        <p style={{ color: '#64748b', margin: 0 }}>
          Fill in the details below to start the AI-powered resume shortlisting process
        </p>
      </div>

      <form onSubmit={handleSubmit}>
        {/* Job Title */}
        <div style={{ marginBottom: '1.5rem' }}>
          <label
            htmlFor="job_title"
            style={{
              display: 'block',
              fontWeight: '600',
              color: '#1e293b',
              marginBottom: '0.5rem',
              fontSize: '0.95rem'
            }}
          >
            💼 Job Title <span style={{ color: '#ef4444' }}>*</span>
          </label>
          <input
            type="text"
            id="job_title"
            name="job_title"
            value={formData.job_title}
            onChange={handleChange}
            required
            placeholder="e.g., Senior Software Engineer"
            style={{
              width: '100%',
              padding: '0.75rem 1rem',
              fontSize: '1rem',
              border: '2px solid #e2e8f0',
              borderRadius: '8px',
              transition: 'all 0.3s',
              outline: 'none',
              fontFamily: 'inherit'
            }}
            onFocus={(e) => e.target.style.borderColor = '#6366f1'}
            onBlur={(e) => e.target.style.borderColor = '#e2e8f0'}
          />
        </div>

        {/* Job Description */}
        <div style={{ marginBottom: '1.5rem' }}>
          <label
            htmlFor="description"
            style={{
              display: 'block',
              fontWeight: '600',
              color: '#1e293b',
              marginBottom: '0.5rem',
              fontSize: '0.95rem'
            }}
          >
            📄 Job Description <span style={{ color: '#ef4444' }}>*</span>
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
            placeholder="Describe the role, responsibilities, and requirements..."
            rows="4"
            style={{
              width: '100%',
              padding: '0.75rem 1rem',
              fontSize: '1rem',
              border: '2px solid #e2e8f0',
              borderRadius: '8px',
              transition: 'all 0.3s',
              outline: 'none',
              fontFamily: 'inherit',
              resize: 'vertical'
            }}
            onFocus={(e) => e.target.style.borderColor = '#6366f1'}
            onBlur={(e) => e.target.style.borderColor = '#e2e8f0'}
          />
        </div>

        {/* Required Tech Stack */}
        <div style={{ marginBottom: '1.5rem' }}>
          <label
            htmlFor="required_tech_stack"
            style={{
              display: 'block',
              fontWeight: '600',
              color: '#1e293b',
              marginBottom: '0.5rem',
              fontSize: '0.95rem'
            }}
          >
            🛠️ Required Tech Stack <span style={{ color: '#ef4444' }}>*</span>
          </label>
          <input
            type="text"
            id="required_tech_stack"
            name="required_tech_stack"
            value={formData.required_tech_stack}
            onChange={handleChange}
            required
            placeholder="e.g., Python, React, FastAPI, Machine Learning"
            style={{
              width: '100%',
              padding: '0.75rem 1rem',
              fontSize: '1rem',
              border: '2px solid #e2e8f0',
              borderRadius: '8px',
              transition: 'all 0.3s',
              outline: 'none',
              fontFamily: 'inherit'
            }}
            onFocus={(e) => e.target.style.borderColor = '#6366f1'}
            onBlur={(e) => e.target.style.borderColor = '#e2e8f0'}
          />
          <p style={{
            fontSize: '0.85rem',
            color: '#64748b',
            margin: '0.5rem 0 0 0',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            💡 Separate skills with commas
          </p>
        </div>

        {/* Two Column Layout */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '1.5rem',
          marginBottom: '1.5rem'
        }}>
          {/* Minimum Experience */}
          <div>
            <label
              htmlFor="minimum_experience"
              style={{
                display: 'block',
                fontWeight: '600',
                color: '#1e293b',
                marginBottom: '0.5rem',
                fontSize: '0.95rem'
              }}
            >
              ⏰ Min. Experience (years) <span style={{ color: '#ef4444' }}>*</span>
            </label>
            <input
              type="number"
              id="minimum_experience"
              name="minimum_experience"
              value={formData.minimum_experience}
              onChange={handleChange}
              min="0"
              required
              style={{
                width: '100%',
                padding: '0.75rem 1rem',
                fontSize: '1rem',
                border: '2px solid #e2e8f0',
                borderRadius: '8px',
                transition: 'all 0.3s',
                outline: 'none',
                fontFamily: 'inherit'
              }}
              onFocus={(e) => e.target.style.borderColor = '#6366f1'}
              onBlur={(e) => e.target.style.borderColor = '#e2e8f0'}
            />
            <p style={{ fontSize: '0.8rem', color: '#64748b', margin: '0.5rem 0 0 0' }}>
              Use 0 for entry-level
            </p>
          </div>

          {/* Hiring Slots */}
          <div>
            <label
              htmlFor="hiring_slots"
              style={{
                display: 'block',
                fontWeight: '600',
                color: '#1e293b',
                marginBottom: '0.5rem',
                fontSize: '0.95rem'
              }}
            >
              👥 Number of Positions <span style={{ color: '#ef4444' }}>*</span>
            </label>
            <input
              type="number"
              id="hiring_slots"
              name="hiring_slots"
              value={formData.hiring_slots}
              onChange={handleChange}
              min="1"
              required
              style={{
                width: '100%',
                padding: '0.75rem 1rem',
                fontSize: '1rem',
                border: '2px solid #e2e8f0',
                borderRadius: '8px',
                transition: 'all 0.3s',
                outline: 'none',
                fontFamily: 'inherit'
              }}
              onFocus={(e) => e.target.style.borderColor = '#6366f1'}
              onBlur={(e) => e.target.style.borderColor = '#e2e8f0'}
            />
          </div>
        </div>

        {/* Shortlist Configuration */}
        <div style={{
          background: '#f8fafc',
          padding: '1.5rem',
          borderRadius: '12px',
          marginBottom: '2rem',
          border: '2px solid #e2e8f0'
        }}>
          <h3 style={{
            fontSize: '1.1rem',
            color: '#1e293b',
            marginBottom: '1rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            ⚙️ Shortlisting Configuration
          </h3>

          <div style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: '1.5rem'
          }}>
            {/* Phase 1 Count */}
            <div>
              <label
                htmlFor="phase1_shortlist_count"
                style={{
                  display: 'block',
                  fontWeight: '600',
                  color: '#1e293b',
                  marginBottom: '0.5rem',
                  fontSize: '0.95rem'
                }}
              >
                🔍 Phase 1 Shortlist <span style={{ color: '#ef4444' }}>*</span>
              </label>
              <input
                type="number"
                id="phase1_shortlist_count"
                name="phase1_shortlist_count"
                value={formData.phase1_shortlist_count}
                onChange={handleChange}
                min="1"
                required
                style={{
                  width: '100%',
                  padding: '0.75rem 1rem',
                  fontSize: '1rem',
                  border: '2px solid #e2e8f0',
                  borderRadius: '8px',
                  transition: 'all 0.3s',
                  outline: 'none',
                  fontFamily: 'inherit',
                  background: 'white'
                }}
                onFocus={(e) => e.target.style.borderColor = '#6366f1'}
                onBlur={(e) => e.target.style.borderColor = '#e2e8f0'}
              />
              <p style={{ fontSize: '0.8rem', color: '#64748b', margin: '0.5rem 0 0 0' }}>
                Keyword matching phase
              </p>
            </div>

            {/* Phase 2 Count */}
            <div>
              <label
                htmlFor="phase2_shortlist_count"
                style={{
                  display: 'block',
                  fontWeight: '600',
                  color: '#1e293b',
                  marginBottom: '0.5rem',
                  fontSize: '0.95rem'
                }}
              >
                🤖 Phase 2 Shortlist <span style={{ color: '#ef4444' }}>*</span>
              </label>
              <input
                type="number"
                id="phase2_shortlist_count"
                name="phase2_shortlist_count"
                value={formData.phase2_shortlist_count}
                onChange={handleChange}
                min="1"
                required
                style={{
                  width: '100%',
                  padding: '0.75rem 1rem',
                  fontSize: '1rem',
                  border: '2px solid #e2e8f0',
                  borderRadius: '8px',
                  transition: 'all 0.3s',
                  outline: 'none',
                  fontFamily: 'inherit',
                  background: 'white'
                }}
                onFocus={(e) => e.target.style.borderColor = '#6366f1'}
                onBlur={(e) => e.target.style.borderColor = '#e2e8f0'}
              />
              <p style={{ fontSize: '0.8rem', color: '#64748b', margin: '0.5rem 0 0 0' }}>
                AI review phase (final)
              </p>
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          style={{
            width: '100%',
            padding: '1rem 2rem',
            fontSize: '1.1rem',
            fontWeight: '600',
            color: 'white',
            background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
            border: 'none',
            borderRadius: '12px',
            cursor: 'pointer',
            transition: 'all 0.3s',
            boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '0.75rem'
          }}
          onMouseOver={(e) => {
            e.target.style.transform = 'translateY(-2px)';
            e.target.style.boxShadow = '0 10px 15px -3px rgb(0 0 0 / 0.1)';
          }}
          onMouseOut={(e) => {
            e.target.style.transform = 'translateY(0)';
            e.target.style.boxShadow = '0 4px 6px -1px rgb(0 0 0 / 0.1)';
          }}
        >
          <span style={{ fontSize: '1.25rem' }}>✨</span>
          Create Job Posting
        </button>
      </form>
    </div>
  );
};

export default JobPostingForm;
