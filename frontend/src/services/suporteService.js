import api from './api';

export const suporteService = {
  // Agente IA
  getMeuAgente: () => api.get('/suporte/agentes/meu_agente/'),
  renomearAgente: (nome_agente) => api.post('/suporte/agentes/renomear/', { nome_agente }),

  // Chat
  enviarMensagem: (mensagem) => api.post('/suporte/conversas/chat/', { mensagem }),
  getHistorico: (limite = 50) => api.get(`/suporte/conversas/historico/?limite=${limite}`),
  limparHistorico: () => api.delete('/suporte/conversas/limpar_historico/'),
};
