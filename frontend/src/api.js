import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const api = {
  // Create a new job posting
  createJob: async (jobData) => {
    const response = await axios.post(`${API_BASE_URL}/jobs/create`, jobData);
    return response.data;
  },

  // Upload resumes for a job
  uploadResumes: async (jobId, file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(
      `${API_BASE_URL}/jobs/${jobId}/upload-resumes`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  },

  // Start the shortlisting process
  startShortlisting: async (jobId) => {
    const response = await axios.post(`${API_BASE_URL}/jobs/${jobId}/start-shortlisting`);
    return response.data;
  },

  // Get job status
  getJobStatus: async (jobId) => {
    const response = await axios.get(`${API_BASE_URL}/jobs/${jobId}/status`);
    return response.data;
  },

  // Get shortlisted candidates
  getShortlistedCandidates: async (jobId) => {
    const response = await axios.get(`${API_BASE_URL}/jobs/${jobId}/shortlisted`);
    return response.data;
  },

  // List all jobs
  listJobs: async () => {
    const response = await axios.get(`${API_BASE_URL}/jobs`);
    return response.data;
  },
};
