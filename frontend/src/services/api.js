import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' }
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const clientesAPI = {
  listar: (params) => api.get('/clientes/', { params }),
  criar: (data) => api.post('/clientes/', data),
  atualizar: (id, data) => api.put(`/clientes/${id}/`, data),
  deletar: (id) => api.delete(`/clientes/${id}/`),
};

export const orcamentosAPI = {
  listar: () => api.get('/orcamentos/'),
  criar: (data) => api.post('/orcamentos/', data),
  calcular: (data) => api.post('/orcamentos/calcular/', data),
  gerarPDF: (id) => api.post(`/orcamentos/${id}/gerar_pdf/`),
  converterProposta: (id, data) => api.post(`/orcamentos/${id}/converter_proposta/`, data),
};

export const propostasAPI = {
  listar: () => api.get('/propostas/'),
  aceitar: (id) => api.post(`/propostas/${id}/aceitar/`),
  converterContrato: (id, data) => api.post(`/propostas/${id}/converter_contrato/`, data),
};

export const contratosAPI = {
  listar: () => api.get('/contratos/'),
  gerarPDF: (id) => api.post(`/contratos/${id}/gerar_pdf/`),
};

export const vendedoresAPI = {
  listar: () => api.get('/vendedores/'),
  criar: (data) => api.post('/vendedores/', data),
  historicoVendas: (id) => api.get(`/vendedores/${id}/historico_vendas/`),
};

export const premissasAPI = {
  listar: () => api.get('/premissas/'),
  criar: (data) => api.post('/premissas/', data),
  atualizar: (id, data) => api.put(`/premissas/${id}/`, data),
};

export const equipamentosAPI = {
  listar: (params) => api.get('/equipamentos/', { params }),
  criar: (data) => api.post('/equipamentos/', data),
  atualizar: (id, data) => api.put(`/equipamentos/${id}/`, data),
  paineis: () => api.get('/equipamentos/paineis/'),
  inversores: () => api.get('/equipamentos/inversores/'),
  // NOVO: Função para gerar a OS recebendo o PDF (blob)
  gerarOS: (dados) => api.post('/equipamentos/gerar_os/', dados, {
    responseType: 'blob' 
  }),
};

export const iaAPI = {
  analisarConsumo: (data) => api.post('/ia/analisar-consumo/', data),
  otimizarProposta: (id) => api.post(`/ia/otimizar-proposta/${id}/`),
  chatbot: (data) => api.post('/ia/chatbot/', data),
  analisarViabilidade: (data) => api.post('/ia/analisar-viabilidade/', data),
  emailFollowup: (id, data) => api.post(`/ia/email-followup/${id}/`, data),
  extrairContaLuz: (data) => api.post('/ia/extrair-conta-luz/', data),
  preverEconomia: (data) => api.post('/ia/prever-economia/', data),
};

export default api;