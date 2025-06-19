import api from './api';

const idsService = {
  detectIntrusion: async (features, userContact) => {
    try {
      const response = await api.post('/detect', { features, ...userContact });
      return response.data;
    } catch (error) {
      console.error("Intrusion detection failed:", error.response ? error.response.data : error.message);
      throw error;
    }
  },
  getAlerts: async () => {
    try {
      const response = await api.get('/alerts');
      return response.data.alerts || [];
    } catch (error) {
      console.error("Failed to fetch alerts:", error.response ? error.response.data : error.message);
      return [];
    }
  }
};

export default idsService;
