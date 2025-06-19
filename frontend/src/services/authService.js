import api from './api';

const authService = {
  signup: async (userData) => {
    try {
      const response = await api.post('/auth/signup', userData);
      return response.data;
    } catch (error) {
      console.error("Signup failed:", error.response ? error.response.data : error.message);
      throw error;
    }
  },
  
  verifyOtp: async (data) => {
    try {
      const response = await api.post('/auth/verify-otp', data);
      return response.data;
    } catch (error) {
      console.error("OTP verification failed:", error.response ? error.response.data : error.message);
      throw error;
    }
  },

  login: async (credentials) => {
    try {
      const response = await api.post('/auth/login', credentials);
      return response.data;
    } catch (error) {
      console.error("Login failed:", error.response ? error.response.data : error.message);
      throw error;
    }
  }
};

export default authService;
