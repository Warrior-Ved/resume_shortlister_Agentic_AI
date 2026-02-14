import React, { useState, useEffect } from 'react';
import { api } from './api';
import JobPostingForm from './components/JobPostingForm';
import ResumeUploader from './components/ResumeUploader';
import Dashboard from './components/Dashboard';
import ShortlistedCandidates from './components/ShortlistedCandidates';
import ProcessingTimeline from './components/ProcessingTimeline';

function App() {
  const [currentJobId, setCurrentJobId] = useState(null);
  const [jobStatus, setJobStatus] = useState(null);
  const [shortlistedCandidates, setShortlistedCandidates] = useState([]);
  const [message, setMessage] = useState({ text: '', type: '' });
  const [isShortlistingStarted, setIsShortlistingStarted] = useState(false);
  const [processingSteps, setProcessingSteps] = useState([]);

  // Poll job status every 3 seconds when processing
  useEffect(() => {
    if (!currentJobId) return;

    const interval = setInterval(async () => {
      try {
        const status = await api.getJobStatus(currentJobId);
        setJobStatus(status);

        // Update processing timeline
        updateProcessingSteps(status);

        // If completed, fetch shortlisted candidates
        if (status.status === 'completed' && status.shortlisted_count > 0) {
          const result = await api.getShortlistedCandidates(currentJobId);
          setShortlistedCandidates(result.shortlisted);
        }
      } catch (error) {
        console.error('Error fetching job status:', error);
      }
    }, 3000);

    return () => clearInterval(interval);
  }, [currentJobId]);

  const updateProcessingSteps = (status) => {
    const steps = [];

    steps.push({
      name: 'Job Created',
      status: 'completed',
      icon: '✅',
      time: new Date(status.created_at).toLocaleTimeString()
    });

    if (status.total_resumes > 0) {
      steps.push({
        name: `${status.total_resumes} Resumes Uploaded`,
        status: 'completed',
        icon: '✅',
        detail: 'PDF parsed and extracted'
      });
    }

    if (status.status === 'phase1' || status.status === 'phase2' || status.status === 'completed') {
      steps.push({
        name: 'Phase 1: Keyword Matching',
        status: status.phase1_completed > 0 ? 'completed' : 'in-progress',
        icon: status.phase1_completed > 0 ? '✅' : '⏳',
        detail: `${status.phase1_completed} candidates passed`,
        progress: status.total_resumes > 0 ? (status.phase1_completed / status.total_resumes * 100) : 0
      });
    }

    if (status.status === 'phase2' || status.status === 'completed') {
      steps.push({
        name: 'Phase 2: AI Review',
        status: status.status === 'completed' ? 'completed' : 'in-progress',
        icon: status.status === 'completed' ? '✅' : '🤖',
        detail: status.status === 'completed'
          ? `${status.phase2_completed} candidates reviewed`
          : 'AI analyzing resumes...',
        progress: status.phase1_completed > 0 ? (status.phase2_completed / status.phase1_completed * 100) : 0
      });
    }

    if (status.status === 'completed') {
      steps.push({
        name: 'Shortlisting Complete',
        status: 'completed',
        icon: '🎉',
        detail: `${status.shortlisted_count} candidates shortlisted`
      });
    }

    setProcessingSteps(steps);
  };

  const handleJobCreated = async (jobData) => {
    try {
      const result = await api.createJob(jobData);
      setCurrentJobId(result.job_id);
      setMessage({
        text: '✅ Job created successfully! Upload your resumes to begin.',
        type: 'success'
      });

      // Fetch initial status
      const status = await api.getJobStatus(result.job_id);
      setJobStatus(status);
      updateProcessingSteps(status);
    } catch (error) {
      setMessage({ text: '❌ Error creating job: ' + error.message, type: 'error' });
    }
  };

  const handleResumeUpload = async (file) => {
    try {
      setMessage({ text: '⏳ Uploading and processing PDF...', type: 'info' });
      const result = await api.uploadResumes(currentJobId, file);
      setMessage({
        text: `✅ Successfully uploaded! Processed ${result.total_resumes} resumes from PDF.`,
        type: 'success'
      });

      // Refresh status
      const status = await api.getJobStatus(currentJobId);
      setJobStatus(status);
      updateProcessingSteps(status);
    } catch (error) {
      setMessage({ text: '❌ Error uploading resumes: ' + error.message, type: 'error' });
      throw error;
    }
  };

  const handleStartShortlisting = async () => {
    try {
      await api.startShortlisting(currentJobId);
      setIsShortlistingStarted(true);
      setMessage({
        text: '🚀 Shortlisting process started! This will take 2-5 minutes. Watch the progress below.',
        type: 'info'
      });
    } catch (error) {
      setMessage({ text: '❌ Error starting shortlisting: ' + error.message, type: 'error' });
    }
  };

  const handleReset = () => {
    if (confirm('Start a new job? Current progress will be lost.')) {
      setCurrentJobId(null);
      setJobStatus(null);
      setShortlistedCandidates([]);
      setMessage({ text: '', type: '' });
      setIsShortlistingStarted(false);
      setProcessingSteps([]);
    }
  };

  return (
    <div className="app">
      {/* Modern Header with Gradient */}
      <div className="header-modern">
        <div className="header-content">
          <div className="logo-section">
            <div className="logo-icon">🎯</div>
            <div>
              <h1>Resume Shortlister AI</h1>
              <p className="tagline">Intelligent Two-Phase AI-Powered Resume Screening</p>
            </div>
          </div>
          {currentJobId && (
            <div className="header-actions">
              <button className="button-outline" onClick={handleReset}>
                ↻ New Job
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Status Message Banner */}
      {message.text && (
        <div className={`alert-modern alert-${message.type}`}>
          <span className="alert-icon">
            {message.type === 'success' && '✅'}
            {message.type === 'error' && '❌'}
            {message.type === 'info' && 'ℹ️'}
          </span>
          <span className="alert-text">{message.text}</span>
        </div>
      )}

      <div className="container-modern">
        {!currentJobId ? (
          // Step 1: Job Creation
          <div className="welcome-section">
            <div className="welcome-card">
              <h2>👋 Welcome to Resume Shortlister AI</h2>
              <p>Get started by creating a job posting with your requirements.</p>
              <div className="feature-list">
                <div className="feature-item">
                  <span className="feature-icon">🔍</span>
                  <span>Phase 1: Keyword & Experience Matching</span>
                </div>
                <div className="feature-item">
                  <span className="feature-icon">🤖</span>
                  <span>Phase 2: AI-Powered Comprehensive Review</span>
                </div>
                <div className="feature-item">
                  <span className="feature-icon">📊</span>
                  <span>Confidence Scores & AI-Generated Cover Letters</span>
                </div>
              </div>
            </div>
            <JobPostingForm onJobCreated={handleJobCreated} />
          </div>
        ) : (
          // Main Processing View
          <div className="processing-view">
            {/* Left Column: Progress & Status */}
            <div className="left-column">
              {/* Processing Timeline */}
              {processingSteps.length > 0 && (
                <ProcessingTimeline steps={processingSteps} />
              )}

              {/* Dashboard Stats */}
              {jobStatus && <Dashboard jobStatus={jobStatus} />}

              {/* Resume Upload Section */}
              {jobStatus && jobStatus.status === 'pending' && (
                <div className="upload-section">
                  <ResumeUploader
                    jobId={currentJobId}
                    onUploadComplete={handleResumeUpload}
                  />
                </div>
              )}

              {/* Start Shortlisting Button */}
              {jobStatus &&
               (jobStatus.status === 'uploaded' || jobStatus.status === 'pending') &&
               jobStatus.total_resumes > 0 &&
               !isShortlistingStarted && (
                <div className="card-modern action-card">
                  <h3>✅ Ready to Process</h3>
                  <p className="card-description">
                    {jobStatus.total_resumes} resumes are ready for AI-powered shortlisting.
                  </p>
                  <button
                    className="button-primary-large"
                    onClick={handleStartShortlisting}
                  >
                    🚀 Start Shortlisting Process
                  </button>
                  <div className="info-box">
                    <p><strong>What happens next:</strong></p>
                    <ul>
                      <li>Phase 1: Keyword matching (fast, ~seconds)</li>
                      <li>Phase 2: AI comprehensive review (2-5 minutes)</li>
                      <li>Results with confidence scores & cover letters</li>
                    </ul>
                  </div>
                </div>
              )}

              {/* Processing Indicator */}
              {jobStatus && (jobStatus.status === 'processing' ||
                            jobStatus.status === 'phase1' ||
                            jobStatus.status === 'phase2') && (
                <div className="card-modern processing-card">
                  <div className="processing-animation">
                    <div className="spinner-modern"></div>
                    <h3>
                      {jobStatus.status === 'phase1' && '🔍 Phase 1: Keyword Matching'}
                      {jobStatus.status === 'phase2' && '🤖 Phase 2: AI Review'}
                      {jobStatus.status === 'processing' && '⚙️ Initializing...'}
                    </h3>
                    <p className="processing-detail">
                      {jobStatus.status === 'phase1' && `Analyzing ${jobStatus.total_resumes} resumes for keyword and experience match...`}
                      {jobStatus.status === 'phase2' && `AI is comprehensively reviewing ${jobStatus.phase1_completed} qualified candidates...`}
                      {jobStatus.status === 'processing' && 'Setting up the shortlisting pipeline...'}
                    </p>
                    {jobStatus.status === 'phase2' && (
                      <div className="ai-indicator">
                        <span className="ai-badge">🧠 Ollama AI Active</span>
                        <span className="model-badge">ministral-3:3b</span>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>

            {/* Right Column: Results */}
            <div className="right-column">
              {jobStatus && jobStatus.status === 'completed' && (
                <>
                  <div className="completion-banner">
                    <div className="completion-icon">🎉</div>
                    <div>
                      <h2>Shortlisting Complete!</h2>
                      <p>{jobStatus.shortlisted_count} candidates matched your requirements</p>
                    </div>
                  </div>
                  <ShortlistedCandidates candidates={shortlistedCandidates} />
                </>
              )}

              {jobStatus && jobStatus.status === 'error' && (
                <div className="card-modern error-card">
                  <h3>⚠️ Processing Error</h3>
                  <p>An error occurred during the shortlisting process.</p>
                  <button className="button" onClick={handleReset}>
                    Start Over
                  </button>
                </div>
              )}

              {/* Empty State */}
              {jobStatus && jobStatus.status !== 'completed' && jobStatus.status !== 'error' && (
                <div className="empty-state">
                  <div className="empty-icon">📋</div>
                  <h3>Results will appear here</h3>
                  <p>Once the shortlisting process is complete, you'll see the selected candidates with their confidence scores and AI-generated cover letters.</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="footer">
        <p>Powered by Ollama AI (Ministral 3B) | FastAPI Backend | React Frontend</p>
      </div>
    </div>
  );
}

export default App;

