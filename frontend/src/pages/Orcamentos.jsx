import { useState, useEffect } from 'react';
import { Plus, FileText, Download, ArrowRight, Calculator, RefreshCw } from 'lucide-react';
import { orcamentosAPI, premissasAPI, equipamentosAPI } from '../services/api';
import api from '../services/api';

const Orcamentos = () => {
  const [orcamentos, setOrcamentos] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [premissas, setPremissas] = useState(null);
  const [paineis, setPaineis] = useState([]);
  const [calculando, setCalculando] = useState(false);
  
  const [formData, setFormData] = useState({
    nome_cliente: '',
    cidade: '',
    telefone: '',
    consumo_medio_kwh: '',
    painel_id: '',
    parcelas: '',
    quantidade_paineis: '',
    potencia_total_kwp: '',
    modelo_inversor: '',
    geracao_estimada_kwh: '',
    valor_final: '',
    valor_parcela: ''
  });
  
  const [resultado, setResultado] = useState(null);

  useEffect(() => {
    carregarOrcamentos();
    carregarPremissas();
    carregarPaineis();
  }, []);

  const carregarOrcamentos = async () => {
    try {
      const response = await orcamentosAPI.listar();
      setOrcamentos(Array.isArray(response.data) ? response.data : response.data.results || []);
    } catch (error) {
      console.error('Erro:', error);
    }
  };

  const carregarPremissas = async () => {
    try {
      const response = await api.get('/premissas/ativa/');
      setPremissas(response.data);
    } catch (error) {
      console.error('Erro ao carregar premissas:', error);
    }
  };

  const carregarPaineis = async () => {
    try {
      const response = await api.get('/equipamentos/', { params: { tipo: 'painel' } });
      setPaineis(Array.isArray(response.data) ? response.data : response.data.results || []);
    } catch (error) {
      console.error('Erro ao carregar painéis:', error);
    }
  };

  const calcularDimensionamento = async () => {
    if (!formData.consumo_medio_kwh || !formData.painel_id) {
      alert('Preencha o consumo e selecione um painel');
      return;
    }

    setCalculando(true);
    try {
      const response = await api.post('/orcamentos/calcular/', {
        consumo_kwh: formData.consumo_medio_kwh,
        painel_id: formData.painel_id,
        parcelas: formData.parcelas || null
      });
      
      setResultado(response.data);
      setFormData({
        ...formData,
        quantidade_paineis: response.data.quantidade_paineis,
        potencia_total_kwp: response.data.potencia_total_kwp,
        modelo_inversor: response.data.inversor?.modelo || '',
        geracao_estimada_kwh: response.data.geracao_estimada_kwh,
        valor_final: response.data.valor_final,
        valor_parcela: response.data.parcelamento?.valor_parcela || ''
      });
    } catch (error) {
      console.error('Erro ao calcular:', error);
      alert('Erro ao calcular dimensionamento');
    } finally {
      setCalculando(false);
    }
  };

  const recalcularComAjuste = () => {
    if (!resultado) return;
    
    const painel = paineis.find(p => p.id === parseInt(formData.painel_id));
    if (!painel) return;

    const qtd = parseInt(formData.quantidade_paineis);
    const potenciaTotal = (qtd * painel.potencia) / 1000;
    const hsp = resultado.hsp_utilizado;
    const perda = resultado.perda_utilizada;
    const geracaoEstimada = potenciaTotal * hsp * 30 * (1 - perda);

    setFormData({
      ...formData,
      potencia_total_kwp: potenciaTotal.toFixed(2),
      geracao_estimada_kwh: geracaoEstimada.toFixed(2)
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await orcamentosAPI.criar({
        ...formData,
        painel_id: parseInt(formData.painel_id),
        parcelas: formData.parcelas ? parseInt(formData.parcelas) : null
      });
      setShowModal(false);
      carregarOrcamentos();
      setFormData({
        nome_cliente: '',
        cidade: '',
        telefone: '',
        consumo_medio_kwh: '',
        painel_id: '',
        parcelas: '',
        quantidade_paineis: '',
        potencia_total_kwp: '',
        modelo_inversor: '',
        geracao_estimada_kwh: '',
        valor_final: '',
        valor_parcela: ''
      });
      setResultado(null);
    } catch (error) {
      console.error('Erro ao criar orçamento:', error);
    }
  };

  const gerarPDF = async (id) => {
    try {
      const response = await orcamentosAPI.gerarPDF(id);
      window.open(response.data.pdf_url, '_blank');
    } catch (error) {
      console.error('Erro ao gerar PDF:', error);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold text-gray-600">Total de Orçamentos</h3>
          <p className="text-3xl font-bold">{orcamentos.length}</p>
        </div>
        
        <button onClick={() => setShowModal(true)} className="btn-accent flex items-center gap-2">
          <Plus size={20} />
          Novo Orçamento
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {Array.isArray(orcamentos) && orcamentos.map((orc) => (
          <div key={orc.id} className="card hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-gray-500">Orçamento</p>
                <p className="text-xl font-bold text-accent">#{orc.numero}</p>
              </div>
              <FileText className="text-gray-400" size={24} />
            </div>
            
            <h4 className="font-semibold text-lg mb-2">{orc.cliente_nome}</h4>
            
            <div className="space-y-2 text-sm mb-4">
              <div className="flex justify-between">
                <span className="text-gray-600">Potência:</span>
                <span className="font-medium">{orc.potencia_instalada_kwp} kWp</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Painéis:</span>
                <span className="font-medium">{orc.quantidade_placas} un</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Valor:</span>
                <span className="font-bold text-green-600">R$ {orc.valor_total}</span>
              </div>
            </div>
            
            <div className="flex gap-2">
              <button 
                onClick={() => gerarPDF(orc.id)}
                className="flex-1 btn-outline text-sm py-2 flex items-center justify-center gap-2"
              >
                <Download size={16} />
                PDF
              </button>
              <button className="flex-1 btn-accent text-sm py-2 flex items-center justify-center gap-2">
                <ArrowRight size={16} />
                Proposta
              </button>
            </div>
          </div>
        ))}
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 overflow-y-auto">
          <div className="bg-white rounded-xl p-8 max-w-4xl w-full mx-4 my-8">
            <h3 className="text-2xl font-bold mb-6">Novo Orçamento - Calculadora Inteligente</h3>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Dados do Cliente */}
              <div className="border-b pb-4">
                <h4 className="font-semibold mb-3">Dados do Cliente</h4>
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Nome do Cliente</label>
                    <input
                      type="text"
                      className="input"
                      value={formData.nome_cliente}
                      onChange={(e) => setFormData({...formData, nome_cliente: e.target.value})}
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium mb-2">Cidade</label>
                    <input
                      type="text"
                      className="input"
                      value={formData.cidade}
                      onChange={(e) => setFormData({...formData, cidade: e.target.value})}
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium mb-2">Telefone</label>
                    <input
                      type="text"
                      className="input"
                      value={formData.telefone}
                      onChange={(e) => setFormData({...formData, telefone: e.target.value})}
                    />
                  </div>
                </div>
              </div>

              {/* Dimensionamento */}
              <div className="border-b pb-4">
                <h4 className="font-semibold mb-3 flex items-center gap-2">
                  <Calculator size={20} />
                  Dimensionamento Automático
                </h4>
                <div className="grid grid-cols-3 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Consumo Médio (kWh/mês)</label>
                    <input
                      type="number"
                      className="input"
                      value={formData.consumo_medio_kwh}
                      onChange={(e) => setFormData({...formData, consumo_medio_kwh: e.target.value})}
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium mb-2">Modelo do Painel</label>
                    <select
                      className="input"
                      value={formData.painel_id}
                      onChange={(e) => setFormData({...formData, painel_id: e.target.value})}
                      required
                    >
                      <option value="">Selecione...</option>
                      {paineis.map(p => (
                        <option key={p.id} value={p.id}>{p.modelo} - {p.potencia}W</option>
                      ))}
                    </select>
                  </div>
                  
                  <div className="flex items-end">
                    <button
                      type="button"
                      onClick={calcularDimensionamento}
                      disabled={calculando}
                      className="btn-accent w-full flex items-center justify-center gap-2"
                    >
                      {calculando ? <RefreshCw size={16} className="animate-spin" /> : <Calculator size={16} />}
                      Calcular
                    </button>
                  </div>
                </div>

                {resultado && (
                  <div className="bg-blue-50 p-4 rounded-lg space-y-3">
                    <div className="grid grid-cols-4 gap-4">
                      <div>
                        <label className="block text-sm font-medium mb-2">Qtd Painéis</label>
                        <input
                          type="number"
                          className="input"
                          value={formData.quantidade_paineis}
                          onChange={(e) => {
                            setFormData({...formData, quantidade_paineis: e.target.value});
                            setTimeout(recalcularComAjuste, 100);
                          }}
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium mb-2">Potência Total (kWp)</label>
                        <input
                          type="text"
                          className="input bg-gray-100"
                          value={formData.potencia_total_kwp}
                          readOnly
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium mb-2">Inversor</label>
                        <input
                          type="text"
                          className="input bg-gray-100"
                          value={formData.modelo_inversor}
                          readOnly
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium mb-2">Geração (kWh/mês)</label>
                        <input
                          type="text"
                          className="input bg-gray-100"
                          value={formData.geracao_estimada_kwh}
                          readOnly
                        />
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Pagamento */}
              {resultado && (
                <div className="border-b pb-4">
                  <h4 className="font-semibold mb-3">Forma de Pagamento</h4>
                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-2">Parcelas</label>
                      <select
                        className="input"
                        value={formData.parcelas}
                        onChange={(e) => {
                          setFormData({...formData, parcelas: e.target.value});
                          if (e.target.value) calcularDimensionamento();
                        }}
                      >
                        <option value="">À vista</option>
                        {premissas?.taxa_juros_maquininha && Object.keys(premissas.taxa_juros_maquininha).map(p => (
                          <option key={p} value={p}>{p}x</option>
                        ))}
                      </select>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium mb-2">Valor Total</label>
                      <input
                        type="text"
                        className="input bg-gray-100 font-bold text-green-600"
                        value={`R$ ${formData.valor_final}`}
                        readOnly
                      />
                    </div>
                    
                    {formData.valor_parcela && (
                      <div>
                        <label className="block text-sm font-medium mb-2">Valor da Parcela</label>
                        <input
                          type="text"
                          className="input bg-gray-100"
                          value={`R$ ${formData.valor_parcela}`}
                          readOnly
                        />
                      </div>
                    )}
                  </div>
                </div>
              )}
              
              <div className="flex gap-3 pt-4">
                <button 
                  type="button" 
                  onClick={() => {
                    setShowModal(false);
                    setResultado(null);
                  }} 
                  className="btn-outline flex-1"
                >
                  Cancelar
                </button>
                <button 
                  type="submit" 
                  className="btn-accent flex-1"
                  disabled={!resultado}
                >
                  Criar Orçamento
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Orcamentos;
