import axios from 'axios';

// Load API base URL from environment or fallback to localhost
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

console.log("🌐 API Base URL:", API_BASE_URL); // Helpful for debugging

// Create an Axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Important if you're using sessions or cookies
});

// Global response interceptor for logging and centralized error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("🚨 API Error:", error.response?.data || error.message);
    return Promise.reject(error); // Re-throw error to handle locally if needed
  }
);

export default api;
