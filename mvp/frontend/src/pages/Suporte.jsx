import { useState, useEffect, useRef } from 'react';
import { suporteService } from '../services/suporteService';
import { Bot, Send, Trash2, Edit2, Sparkles } from 'lucide-react';

export default function Suporte() {
  const [agente, setAgente] = useState(null);
  const [mensagem, setMensagem] = useState('');
  const [conversas, setConversas] = useState([]);
  const [loading, setLoading] = useState(false);
  const [editandoNome, setEditandoNome] = useState(false);
  const [novoNome, setNovoNome] = useState('');
  const chatEndRef = useRef(null);

  useEffect(() => {
    carregarAgente();
    carregarHistorico();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [conversas]);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const carregarAgente = async () => {
    try {
      const response = await suporteService.getMeuAgente();
      setAgente(response.data);
      setNovoNome(response.data.nome_agente);
    } catch (error) {
      console.error('Erro ao carregar agente:', error);
    }
  };

  const carregarHistorico = async () => {
    try {
      const response = await suporteService.getHistorico(20);
      setConversas(response.data.reverse());
    } catch (error) {
      console.error('Erro ao carregar histórico:', error);
    }
  };

  const enviarMensagem = async (e) => {
    e.preventDefault();
    if (!mensagem.trim() || loading) return;

    const msgUsuario = mensagem;
    setMensagem('');
    setLoading(true);

    // Adicionar mensagem do usuário imediatamente
    const novaMsgUsuario = {
      id: Date.now(),
      mensagem: msgUsuario,
      resposta: null,
      criado_em: new Date().toISOString(),
    };
    setConversas(prev => [...prev, novaMsgUsuario]);

    try {
      const response = await suporteService.enviarMensagem(msgUsuario);
      
      // Atualizar com resposta do agente
      setConversas(prev => 
        prev.map(c => c.id === novaMsgUsuario.id ? response.data : c)
      );
    } catch (error) {
      console.error('Erro ao enviar mensagem:', error);
      setConversas(prev => 
        prev.map(c => c.id === novaMsgUsuario.id ? {
          ...c,
          resposta: '❌ Erro ao processar mensagem. Tente novamente.'
        } : c)
      );
    } finally {
      setLoading(false);
    }
  };

  const renomearAgente = async () => {
    if (!novoNome.trim()) return;
    
    try {
      await suporteService.renomearAgente(novoNome);
      setAgente(prev => ({ ...prev, nome_agente: novoNome }));
      setEditandoNome(false);
    } catch (error) {
      console.error('Erro ao renomear agente:', error);
    }
  };

  const limparHistorico = async () => {
    if (!confirm('Deseja limpar todo o histórico de conversas?')) return;
    
    try {
      await suporteService.limparHistorico();
      setConversas([]);
    } catch (error) {
      console.error('Erro ao limpar histórico:', error);
    }
  };

  const sugestoes = [
    'Olá! Como você está?',
    'Mostre propostas vencendo',
    'Clientes sem retorno',
    'Gerar relatório de vendas',
    'Dúvidas sobre HSP',
    'Conte uma piada solar',
  ];

  return (
    <div className="h-[calc(100vh-4rem)] flex flex-col bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="bg-gradient-to-br from-yellow-400 to-orange-500 p-3 rounded-xl">
            <Bot className="w-6 h-6 text-white" />
          </div>
          <div>
            {editandoNome ? (
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={novoNome}
                  onChange={(e) => setNovoNome(e.target.value)}
                  className="border rounded px-2 py-1 text-lg font-semibold"
                  autoFocus
                />
                <button
                  onClick={renomearAgente}
                  className="text-green-600 hover:text-green-700"
                >
                  ✓
                </button>
                <button
                  onClick={() => {
                    setEditandoNome(false);
                    setNovoNome(agente?.nome_agente || '');
                  }}
                  className="text-red-600 hover:text-red-700"
                >
                  ✗
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <h1 className="text-xl font-bold text-gray-800">
                  {agente?.nome_agente || 'Solar Bot'}
                </h1>
                <button
                  onClick={() => setEditandoNome(true)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <Edit2 className="w-4 h-4" />
                </button>
              </div>
            )}
            <p className="text-sm text-gray-500 flex items-center gap-1">
              <Sparkles className="w-3 h-3" />
              Assistente Solar Inteligente
            </p>
          </div>
        </div>
        
        <button
          onClick={limparHistorico}
          className="flex items-center gap-2 px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition"
        >
          <Trash2 className="w-4 h-4" />
          Limpar Chat
        </button>
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {conversas.length === 0 && (
          <div className="text-center py-12">
            <div className="bg-gradient-to-br from-yellow-400 to-orange-500 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
              <Bot className="w-10 h-10 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-gray-800 mb-2">
              Olá! Sou seu assistente solar! ☀️
            </h2>
            <p className="text-gray-600 mb-6">
              Posso ajudar com orçamentos, relatórios, alertas e dúvidas técnicas!
            </p>
            
            <div className="max-w-2xl mx-auto">
              <p className="text-sm text-gray-500 mb-3">Sugestões:</p>
              <div className="grid grid-cols-2 gap-2">
                {sugestoes.map((sug, idx) => (
                  <button
                    key={idx}
                    onClick={() => setMensagem(sug)}
                    className="text-left px-4 py-2 bg-white border border-gray-200 rounded-lg hover:border-yellow-400 hover:bg-yellow-50 transition text-sm"
                  >
                    {sug}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {conversas.map((conversa, index) => (
          <div key={conversa.id || `conversa-${index}`} className="space-y-3">
            {/* Mensagem do usuário */}
            <div className="flex justify-end">
              <div className="bg-yellow-500 text-white px-4 py-2 rounded-2xl rounded-tr-sm max-w-2xl">
                <p className="whitespace-pre-wrap">{conversa.mensagem}</p>
              </div>
            </div>

            {/* Resposta do agente */}
            {conversa.resposta && (
              <div className="flex justify-start">
                <div className="bg-white border border-gray-200 px-4 py-3 rounded-2xl rounded-tl-sm max-w-2xl shadow-sm">
                  <p className="whitespace-pre-wrap text-gray-800">{conversa.resposta}</p>
                  {conversa.tipo_acao && (
                    <span className="inline-block mt-2 text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                      {conversa.tipo_acao}
                    </span>
                  )}
                </div>
              </div>
            )}

            {/* Loading */}
            {!conversa.resposta && loading && (
              <div className="flex justify-start">
                <div className="bg-white border border-gray-200 px-4 py-3 rounded-2xl rounded-tl-sm">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
        
        <div ref={chatEndRef} />
      </div>

      {/* Input Area */}
      <div className="bg-white border-t px-6 py-4">
        <form onSubmit={enviarMensagem} className="flex gap-3">
          <input
            type="text"
            value={mensagem}
            onChange={(e) => setMensagem(e.target.value)}
            placeholder="Digite sua mensagem..."
            className="flex-1 border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-yellow-400"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={!mensagem.trim() || loading}
            className="bg-gradient-to-r from-yellow-400 to-orange-500 text-white px-6 py-3 rounded-xl hover:from-yellow-500 hover:to-orange-600 disabled:opacity-50 disabled:cursor-not-allowed transition flex items-center gap-2"
          >
            <Send className="w-5 h-5" />
            Enviar
          </button>
        </form>
      </div>
    </div>
  );
}
