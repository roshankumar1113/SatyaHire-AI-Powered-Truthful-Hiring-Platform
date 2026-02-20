import axios, { AxiosError, AxiosRequestConfig } from 'axios';
import { publicEnv, isProduction, getApiUrl } from './env';

/**
 * API Client Configuration
 * 
 * Production-ready API client with:
 * - Type-safe environment variables
 * - Automatic token refresh
 * - Request/response interceptors
 * - Error handling
 * - Retry logic
 */

// Use the centralized environment configuration
const API_BASE_URL = publicEnv.apiUrl;

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expired, try refresh
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          });
          localStorage.setItem('access_token', response.data.access_token);
          // Retry original request
          error.config.headers.Authorization = `Bearer ${response.data.access_token}`;
          return axios(error.config);
        } catch (refreshError) {
          // Refresh failed, logout
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

// API functions
export const authAPI = {
  signup: (data: any) => apiClient.post('/auth/signup', data),
  login: (data: any) => apiClient.post('/auth/login', data),
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },
};

export const companyAPI = {
  createJob: (data: any) => apiClient.post('/jobs', data),
  getJobs: () => apiClient.get('/jobs'),
  createTest: (jobId: string) => apiClient.post(`/jobs/${jobId}/tests`),
  getCandidates: (jobId: string) => apiClient.get(`/jobs/${jobId}/candidates`),
};

export const candidateAPI = {
  getTests: () => apiClient.get('/tests'),
  startTest: (testId: string) => apiClient.post(`/tests/${testId}/start`),
  submitAnswer: (submissionId: string, data: any) => 
    apiClient.post(`/submissions/${submissionId}/answers`, data),
  completeTest: (submissionId: string) => 
    apiClient.post(`/submissions/${submissionId}/complete`),
};
