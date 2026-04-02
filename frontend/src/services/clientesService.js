import api from './api';

export const clientesService = {
  getAll: (params) => api.get('/clientes/', { params }),
  getById: (id) => api.get(`/clientes/${id}/`),
  create: (data) => api.post('/clientes/', data),
  update: (id, data) => api.put(`/clientes/${id}/`, data),
  delete: (id) => api.delete(`/clientes/${id}/`),
  getDashboardStats: () => api.get('/dashboard/resumo/')
};
