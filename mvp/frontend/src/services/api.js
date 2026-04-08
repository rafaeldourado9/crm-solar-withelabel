import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' }
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;

    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      const refreshToken = localStorage.getItem('refresh_token');

      if (refreshToken) {
        try {
          const res = await axios.post('/api/v1/auth/refresh', { refresh_token: refreshToken });
          const newToken = res.data.access_token;
          localStorage.setItem('access_token', newToken);
          original.headers.Authorization = `Bearer ${newToken}`;
          return api(original);
        } catch {
          // refresh falhou — força logout
        }
      }

      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/login';
    }

    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  refresh: (refresh_token) => api.post('/auth/refresh', { refresh_token }),
  me: () => api.get('/auth/me'),
};

export const clientesAPI = {
  listar: (params) => api.get('/clientes', { params }),
  criar: (data) => api.post('/clientes', data),
  obter: (id) => api.get(`/clientes/${id}`),
  atualizar: (id, data) => api.put(`/clientes/${id}`, data),
  deletar: (id) => api.delete(`/clientes/${id}`),
};

export const orcamentosAPI = {
  listar: (params) => api.get('/orcamentos', { params }),
  criar: (data) => api.post('/orcamentos', data),
  obter: (id) => api.get(`/orcamentos/${id}`),
  atualizar: (id, data) => api.put(`/orcamentos/${id}`, data),
  deletar: (id) => api.delete(`/orcamentos/${id}`),
  calcularMaterialEletrico: (data) => api.post('/orcamentos/calcular-material-eletrico', data),
};

export const deslocamentoAPI = {
  calcular: (data) => api.post('/deslocamento/calcular', data),
};

export const premissasAPI = {
  obterAtiva: () => api.get('/premissas/ativa'),
  atualizar: (id, data) => api.put(`/premissas/${id}`, data),
};

export const equipamentosAPI = {
  paineis: (params) => api.get('/equipamentos/paineis', { params }),
  inversores: (params) => api.get('/equipamentos/inversores', { params }),
  criarPainel: (data) => api.post('/equipamentos/paineis', data),
  criarInversor: (data) => api.post('/equipamentos/inversores', data),
  atualizarPainel: (id, data) => api.put(`/equipamentos/paineis/${id}`, data),
  atualizarInversor: (id, data) => api.put(`/equipamentos/inversores/${id}`, data),
  validarDimensionamento: (data) => api.post('/equipamentos/validar-dimensionamento', data),
};

export const propostasAPI = {
  listar: (params) => api.get('/propostas', { params }),
  criar: (data) => api.post('/propostas', data),
  obter: (id) => api.get(`/propostas/${id}`),
  aceitar: (id) => api.post(`/propostas/${id}/aceitar`),
  recusar: (id) => api.post(`/propostas/${id}/recusar`),
};

export const contratosAPI = {
  listar: (params) => api.get('/contratos', { params }),
  criar: (data) => api.post('/contratos', data),
  obter: (id) => api.get(`/contratos/${id}`),
  atualizar: (id, data) => api.put(`/contratos/${id}`, data),
  gerarPdf: (id) => api.get(`/contratos/${id}/gerar-pdf`, { responseType: 'blob' }),
};

export const templatesAPI = {
  listar: () => api.get('/templates'),
  upload: (formData) => api.post('/templates', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  download: (id) => api.get(`/templates/${id}/download`, { responseType: 'blob' }),
  deletar: (id) => api.delete(`/templates/${id}`),
};

export const vendedoresAPI = {
  listar: () => api.get('/vendedores'),
  criar: (data) => api.post('/vendedores', data),
  atualizar: (id, data) => api.put(`/vendedores/${id}`, data),
  bloquear: (id) => api.post(`/vendedores/${id}/bloquear`),
  resetarSenha: (id, data) => api.post(`/vendedores/${id}/resetar-senha`, data),
  resumo: (id) => api.get(`/vendedores/${id}/resumo`),
  historico: (id) => api.get(`/vendedores/${id}/historico`),
  marcarComissaoPaga: (vendaId) => api.post(`/vendedores/comissoes/${vendaId}/pagar`),
  deletar: (id) => api.delete(`/vendedores/${id}`),
};

export const dashboardAPI = {
  resumo: () => api.get('/dashboard/resumo'),
};

export const tenantsAPI = {
  obter: (id) => api.get(`/tenants/${id}`),
  atualizar: (id, data) => api.put(`/tenants/${id}`, data),
};

export default api;
