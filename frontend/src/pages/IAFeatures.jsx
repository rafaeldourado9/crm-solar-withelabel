import { useState } from 'react';
import { Zap, MessageSquare, Upload, TrendingUp, Mail, Brain } from 'lucide-react';
import { iaAPI } from '../services/api';

const IAFeatures = () => {
  const [chatMensagem, setChatMensagem] = useState('');
  const [chatResposta, setChatResposta] = useState('');
  const [loading, setLoading] = useState(false);

  const enviarMensagem = async () => {
    if (!chatMensagem.trim()) return;
    
    setLoading(true);
    try {
      const response = await iaAPI.chatbot({ mensagem: chatMensagem });
      setChatResposta(response.data.resposta);
    } catch (error) {
      console.error('Erro:', error);
    } finally {
      setLoading(false);
    }
  };

  const features = [
    {
      icon: Brain,
      title: 'Análise de Consumo',
      description: 'IA analisa padrões e recomenda dimensionamento ideal',
      color: 'bg-purple-500'
    },
    {
      icon: TrendingUp,
      title: 'Otimização de Proposta',
      description: 'Sugere economia mantendo qualidade do projeto',
      color: 'bg-blue-500'
    },
    {
      icon: MessageSquare,
      title: 'Chatbot 24/7',
      description: 'Assistente virtual para atendimento ao cliente',
      color: 'bg-green-500'
    },
    {
      icon: Upload,
      title: 'OCR Conta de Luz',
      description: 'Extração automática de dados da conta',
      color: 'bg-yellow-500'
    },
    {
      icon: Mail,
      title: 'Follow-up Automático',
      description: 'Emails personalizados gerados por IA',
      color: 'bg-red-500'
    },
    {
      icon: Zap,
      title: 'Previsão de Economia',
      description: 'Projeção de 25 anos com IA',
      color: 'bg-indigo-500'
    }
  ];

  return (
    <div className="space-y-6">
      <div className="card bg-gradient-to-r from-accent to-yellow-300 text-primary">
        <div className="flex items-center gap-4">
          <Zap size={48} />
          <div>
            <h2 className="text-2xl font-bold">Features de IA</h2>
            <p className="text-sm opacity-80">Inteligência Artificial para otimizar seu CRM</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {features.map((feature, index) => (
          <div key={index} className="card hover:shadow-lg transition-shadow">
            <div className={`${feature.color} w-12 h-12 rounded-lg flex items-center justify-center mb-4`}>
              <feature.icon size={24} className="text-white" />
            </div>
            <h3 className="font-semibold text-lg mb-2">{feature.title}</h3>
            <p className="text-gray-600 text-sm">{feature.description}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <MessageSquare className="text-accent" />
            Testar Chatbot
          </h3>
          
          <div className="space-y-4">
            <textarea
              className="input min-h-[100px]"
              placeholder="Digite sua mensagem..."
              value={chatMensagem}
              onChange={(e) => setChatMensagem(e.target.value)}
            />
            
            <button 
              onClick={enviarMensagem}
              disabled={loading}
              className="btn-accent w-full"
            >
              {loading ? 'Processando...' : 'Enviar'}
            </button>
            
            {chatResposta && (
              <div className="p-4 bg-gray-50 rounded-lg">
                <p className="text-sm font-medium text-gray-600 mb-2">Resposta da IA:</p>
                <p className="text-gray-800">{chatResposta}</p>
              </div>
            )}
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Upload className="text-accent" />
            Upload Conta de Luz
          </h3>
          
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-accent transition-colors cursor-pointer">
            <Upload size={48} className="mx-auto text-gray-400 mb-4" />
            <p className="text-gray-600 mb-2">Arraste a foto da conta de luz</p>
            <p className="text-sm text-gray-500">ou clique para selecionar</p>
            <input type="file" className="hidden" accept="image/*" />
          </div>
          
          <div className="mt-4 p-4 bg-blue-50 rounded-lg">
            <p className="text-sm text-blue-800">
              <strong>💡 Dica:</strong> A IA extrairá automaticamente consumo, valor e concessionária
            </p>
          </div>
        </div>
      </div>

      <div className="card bg-gray-50">
        <h3 className="text-lg font-semibold mb-4">⚙️ Configuração</h3>
        <div className="space-y-3 text-sm">
          <div className="flex items-center justify-between p-3 bg-white rounded-lg">
            <span>OpenAI API</span>
            <span className="badge bg-green-100 text-green-800">Configurado</span>
          </div>
          <div className="flex items-center justify-between p-3 bg-white rounded-lg">
            <span>Anthropic API</span>
            <span className="badge bg-green-100 text-green-800">Configurado</span>
          </div>
          <div className="flex items-center justify-between p-3 bg-white rounded-lg">
            <span>Custo Estimado Mensal</span>
            <span className="font-bold text-green-600">~R$ 30,00</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default IAFeatures;
