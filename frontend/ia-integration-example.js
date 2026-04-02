// Exemplo de integração das features de IA no frontend

// 1. Chatbot Widget
class ChatbotWidget {
  constructor(apiUrl, clienteId = null) {
    this.apiUrl = apiUrl;
    this.clienteId = clienteId;
  }

  async enviarMensagem(mensagem) {
    const response = await fetch(`${this.apiUrl}/api/ia/chatbot/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mensagem, cliente_id: this.clienteId })
    });
    const data = await response.json();
    return data.resposta;
  }
}

// 2. Upload e OCR de Conta de Luz
async function processarContaLuz(file) {
  const base64 = await fileToBase64(file);
  
  const response = await fetch('/api/ia/extrair-conta-luz/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ imagem_base64: base64 })
  });
  
  const dados = await response.json();
  // Auto-preencher formulário
  document.getElementById('consumo').value = dados.consumo_kwh;
  document.getElementById('valor').value = dados.valor_total;
  
  return dados;
}

// 3. Análise de Viabilidade em Tempo Real
async function analisarViabilidade(formData) {
  const response = await fetch('/api/ia/analisar-viabilidade/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData)
  });
  
  const resultado = await response.json();
  
  // Exibir score visual
  const scoreElement = document.getElementById('viability-score');
  scoreElement.innerHTML = `
    <div class="score ${resultado.viavel ? 'viable' : 'not-viable'}">
      <span class="score-value">${resultado.score}/100</span>
      <span class="score-label">${resultado.viavel ? 'Viável' : 'Não Viável'}</span>
    </div>
    <ul class="recommendations">
      ${resultado.recomendacoes.map(r => `<li>${r}</li>`).join('')}
    </ul>
  `;
  
  return resultado;
}

// 4. Otimização Automática de Proposta
async function otimizarProposta(orcamentoId) {
  const response = await fetch(`/api/ia/otimizar-proposta/${orcamentoId}/`, {
    method: 'POST'
  });
  
  const otimizacao = await response.json();
  
  // Mostrar sugestões
  if (otimizacao.economia_possivel > 0) {
    showNotification(
      `💡 Economia possível: R$ ${otimizacao.economia_possivel}`,
      otimizacao.sugestoes
    );
  }
  
  return otimizacao;
}

// 5. Previsão de Economia Interativa
async function mostrarPrevisaoEconomia(consumo, tarifa) {
  const response = await fetch('/api/ia/prever-economia/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ consumo, tarifa, anos: 25 })
  });
  
  const previsao = await response.json();
  
  // Renderizar gráfico
  renderChart('economia-chart', {
    labels: previsao.previsao_anual.map(p => `Ano ${p.ano}`),
    data: previsao.previsao_anual.map(p => p.economia)
  });
  
  return previsao;
}

// 6. Follow-up Automático
async function agendarFollowup(clienteId, dias) {
  const response = await fetch(`/api/ia/email-followup/${clienteId}/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ dias_sem_resposta: dias })
  });
  
  const { email } = await response.json();
  
  // Pré-visualizar email antes de enviar
  document.getElementById('email-preview').innerHTML = email;
  
  return email;
}

// Helpers
function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });
}

function showNotification(title, items) {
  // Implementar notificação toast
  console.log(title, items);
}

function renderChart(elementId, data) {
  // Implementar com Chart.js ou similar
  console.log('Rendering chart:', elementId, data);
}

// Uso
const chatbot = new ChatbotWidget('http://localhost:8000', 123);
chatbot.enviarMensagem('Quanto custa um sistema de 10kWp?')
  .then(resposta => console.log(resposta));
