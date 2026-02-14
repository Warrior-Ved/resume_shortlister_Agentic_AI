import React, { useState } from 'react';

const ResumeUploader = ({ jobId, onUploadComplete }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
    } else {
      alert('Please select a PDF file');
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type === 'application/pdf') {
        setSelectedFile(file);
      } else {
        alert('Please drop a PDF file');
      }
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select a file first');
      return;
    }

    setUploading(true);
    try {
      await onUploadComplete(selectedFile);
      setSelectedFile(null);
    } catch (error) {
      alert('Error uploading file: ' + error.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="card-modern">
      <h3 style={{
        marginBottom: '1rem',
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem'
      }}>
        📤 Upload Resumes
      </h3>
      <p style={{ color: '#64748b', marginBottom: '1.5rem', fontSize: '0.95rem' }}>
        Upload a PDF file with multiple resumes (one resume per page)
      </p>

      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => document.getElementById('file-input').click()}
        style={{
          border: `3px dashed ${dragActive ? '#6366f1' : '#e2e8f0'}`,
          borderRadius: '12px',
          padding: '3rem 2rem',
          textAlign: 'center',
          cursor: 'pointer',
          transition: 'all 0.3s',
          background: dragActive ? '#f0f0ff' : selectedFile ? '#f0fdf4' : '#f8fafc',
          marginBottom: '1.5rem'
        }}
      >
        <input
          id="file-input"
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
        <div style={{
          fontSize: '3.5rem',
          marginBottom: '1rem',
          filter: selectedFile ? 'none' : 'grayscale(50%)'
        }}>
          {selectedFile ? '✅' : '📄'}
        </div>
        <p style={{
          fontSize: '1.1rem',
          color: '#1e293b',
          marginBottom: '0.5rem',
          fontWeight: '600'
        }}>
          {selectedFile ? selectedFile.name : dragActive ? 'Drop PDF here' : 'Click to select or drag & drop PDF'}
        </p>
        <p style={{ color: '#64748b', fontSize: '0.9rem', margin: 0 }}>
          {selectedFile
            ? `Size: ${(selectedFile.size / 1024 / 1024).toFixed(2)} MB • Ready to upload`
            : 'PDF files only • Multiple resumes supported'}
        </p>
      </div>

      {selectedFile && (
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button
            onClick={handleUpload}
            disabled={uploading}
            style={{
              flex: 1,
              padding: '0.875rem 1.5rem',
              fontSize: '1rem',
              fontWeight: '600',
              color: 'white',
              background: uploading
                ? '#94a3b8'
                : 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
              border: 'none',
              borderRadius: '8px',
              cursor: uploading ? 'not-allowed' : 'pointer',
              transition: 'all 0.3s',
              boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '0.5rem'
            }}
            onMouseOver={(e) => {
              if (!uploading) {
                e.target.style.transform = 'translateY(-2px)';
                e.target.style.boxShadow = '0 10px 15px -3px rgb(0 0 0 / 0.1)';
              }
            }}
            onMouseOut={(e) => {
              e.target.style.transform = 'translateY(0)';
              e.target.style.boxShadow = '0 4px 6px -1px rgb(0 0 0 / 0.1)';
            }}
          >
            {uploading ? (
              <>
                <div style={{
                  width: '16px',
                  height: '16px',
                  border: '2px solid white',
                  borderTopColor: 'transparent',
                  borderRadius: '50%',
                  animation: 'spin 0.8s linear infinite'
                }}></div>
                Uploading...
              </>
            ) : (
              <>
                <span>🚀</span>
                Upload and Process
              </>
            )}
          </button>

          <button
            onClick={() => setSelectedFile(null)}
            disabled={uploading}
            style={{
              padding: '0.875rem 1.5rem',
              fontSize: '1rem',
              fontWeight: '600',
              color: '#64748b',
              background: 'white',
              border: '2px solid #e2e8f0',
              borderRadius: '8px',
              cursor: uploading ? 'not-allowed' : 'pointer',
              transition: 'all 0.3s'
            }}
            onMouseOver={(e) => {
              if (!uploading) {
                e.target.style.borderColor = '#ef4444';
                e.target.style.color = '#ef4444';
              }
            }}
            onMouseOut={(e) => {
              e.target.style.borderColor = '#e2e8f0';
              e.target.style.color = '#64748b';
            }}
          >
            Clear
          </button>
        </div>
      )}
    </div>
  );
};

export default ResumeUploader;
