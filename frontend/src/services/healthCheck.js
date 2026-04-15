import axios from 'axios';

export const checkAPIHealth = async () => {
  try {
    const response = await axios.get('/api/v1/health', { timeout: 5000 });
    return { ok: true, data: response.data };
  } catch (error) {
    console.error('API Health Check falhou:', error.message);
    return { 
      ok: false, 
      error: error.response?.data?.detail || error.message || 'API não está respondendo'
    };
  }
};

export const getAPIBaseURL = () => {
  return import.meta.env.VITE_API_URL || '/api/v1';
};
