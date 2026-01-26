import { useState, useEffect } from 'react';
import { Plus, FileText, Search, Calculator, Trash2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { useToast, ToastContainer } from '../components/Toast';
import { ConfirmDialog } from '../components/ConfirmDialog';

const Orcamentos = () => {
  const navigate = useNavigate();
  const { toasts, showToast, removeToast } = useToast();
  const [orcamentos, setOrcamentos] = useState([]);
  const [orcamentosFiltrados, setOrcamentosFiltrados] = useState([]);
  const [busca, setBusca] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [clientes, setClientes] = useState([]);
  const [paineis, setPaineis] = useState([]);
  const [inversores, setInversores] = useState([]);
  const [premissas, setPremissas] = useState(null);
  const [confirmDialog, setConfirmDialog] = useState({ isOpen: false, orcamentoId: null });
  
  const [formData, setFormData] = useState({
    nome_kit: '',
    cliente_id: '',
    valor_kit: '',
    marca_painel: '',
    potencia_painel: '',
    quantidade_paineis: '',
    marca_inversor: '',
    potencia_inversor: '',
    quantidade_inversores: 1,
    tipo_estrutura: 'ceramico',
    valor_estrutura: 0,
    valor_material_eletrico: 0,
    forma_pagamento: 'avista'
  });
  
  const [painelSelecionado, setPainelSelecionado] = useState(null);
  const [inversorSelecionado, setInversorSelecionado] = useState(null);
  
  const [searchPainel, setSearchPainel] = useState('');
  const [searchInversor, setSearchInversor] = useState('');
  const [showPainelDropdown, setShowPainelDropdown] = useState(false);
  const [showInversorDropdown, setShowInversorDropdown] = useState(false);

  useEffect(() => {
    carregarDados();
  }, []);

  const carregarDados = async () => {
    try {
      const timestamp = new Date().getTime();
      const [orcRes, cliRes, painelRes, invRes, premRes] = await Promise.all([
        api.get(`/orcamentos/?_t=${timestamp}`),
        api.get('/clientes/'),
        api.get('/equipamentos/paineis/?limit=1000'),
        api.get('/equipamentos/inversores/?limit=1000'),
        api.get('/premissas/ativa/')
      ]);
      
      setOrcamentos(orcRes.data.results || orcRes.data);
      setOrcamentosFiltrados(orcRes.data.results || orcRes.data);
      setClientes(cliRes.data.results || cliRes.data);
      setPaineis(painelRes.data.results || painelRes.data);
      setInversores(invRes.data.results || invRes.data);
      setPremissas(premRes.data);
    } catch (error) {
      console.error('Erro:', error);
      showToast('Erro ao carregar dados', 'error');
    }
  };

  useEffect(() => {
    if (!busca.trim()) {
      setOrcamentosFiltrados(orcamentos);
      return;
    }
    
    const termo = busca.toLowerCase();
    const filtrados = orcamentos.filter(orc => 
      orc.nome_kit.toLowerCase().includes(termo) ||
      orc.cliente_nome.toLowerCase().includes(termo) ||
      orc.numero.toLowerCase().includes(termo)
    );
    setOrcamentosFiltrados(filtrados);
  }, [busca, orcamentos]);

  const calcularMaterialEletrico = async () => {
    if (!formData.potencia_inversor || !formData.quantidade_inversores) return;
    
    // Calcular baseado na potência do INVERSOR
    const potencia_kwp = (formData.potencia_inversor * formData.quantidade_inversores) / 1000;
    
    try {
      const res = await api.post('/orcamentos/calcular-material-eletrico/', { potencia_kwp });
      setFormData({...formData, valor_material_eletrico: res.data.valor_material_eletrico});
    } catch (error) {
      console.error('Erro:', error);
      showToast('Erro ao calcular material elétrico', 'error');
    }
  };

  const validarDimensionamento = async () => {
    if (!painelSelecionado || !inversorSelecionado || !formData.quantidade_paineis) return;
    
    try {
      const res = await api.post('/orcamentos/validar-dimensionamento/', {
        potencia_painel: painelSelecionado.potencia_w,
        quantidade_paineis: formData.quantidade_paineis,
        inversor_id: inversorSelecionado.id,
        quantidade_inversores: formData.quantidade_inversores
      });
      
      if (!res.data.valido) {
        showToast(res.data.mensagem, 'error');
        return false;
      }
      return true;
    } catch (error) {
      console.error('Erro:', error);
      showToast('Erro ao validar dimensionamento', 'error');
      return false;
    }
  };

  useEffect(() => {
    if (formData.potencia_inversor && formData.quantidade_inversores) {
      calcularMaterialEletrico();
    }
  }, [formData.potencia_inversor, formData.quantidade_inversores]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validar dimensionamento
    const dimensionamentoValido = await validarDimensionamento();
    if (!dimensionamentoValido) return;
    
    try {
      await api.post('/orcamentos/', formData);
      showToast('Orçamento criado com sucesso!', 'success');
      resetForm();
      setShowModal(false);
      await carregarDados();
    } catch (error) {
      console.error('Erro:', error);
      showToast('Erro ao criar orçamento', 'error');
    }
  };

  const resetForm = () => {
    setFormData({
      nome_kit: '',
      cliente_id: '',
      valor_kit: '',
      marca_painel: '',
      potencia_painel: '',
      quantidade_paineis: '',
      marca_inversor: '',
      potencia_inversor: '',
      quantidade_inversores: 1,
      tipo_estrutura: 'ceramico',
      valor_estrutura: 0,
      valor_material_eletrico: 0,
      forma_pagamento: 'avista'
    });
    setSearchPainel('');
    setSearchInversor('');
    setPainelSelecionado(null);
    setInversorSelecionado(null);
  };

  const paineisFiltered = paineis.filter(p => 
    searchPainel.length >= 2 && (
      p.fabricante.toLowerCase().includes(searchPainel.toLowerCase()) ||
      p.potencia_w.toString().includes(searchPainel)
    )
  );

  // Agrupar por fabricante e potência (remover duplicatas)
  const paineisUnicos = [];
  const vistos = new Set();
  paineisFiltered.forEach(p => {
    const chave = `${p.fabricante}-${p.potencia_w}`;
    if (!vistos.has(chave)) {
      vistos.add(chave);
      paineisUnicos.push(p);
    }
  });

  const inversoresFiltered = inversores.filter(i => 
    searchInversor.length >= 2 && (
      i.fabricante.toLowerCase().includes(searchInversor.toLowerCase()) ||
      i.potencia_w.toString().includes(searchInversor)
    )
  );

  // Agrupar por fabricante e potência (remover duplicatas)
  const inversoresUnicos = [];
  const vistosInv = new Set();
  inversoresFiltered.forEach(i => {
    const chave = `${i.fabricante}-${i.potencia_w}`;
    if (!vistosInv.has(chave)) {
      vistosInv.add(chave);
      inversoresUnicos.push(i);
    }
  });

  const handleDeleteOrcamento = async (id) => {
    try {
      await api.delete(`/orcamentos/${id}/`);
      showToast('Orçamento excluído com sucesso', 'success');
      carregarDados();
    } catch (error) {
      showToast('Erro ao excluir orçamento', 'error');
    }
  };

  return (
    <div className="space-y-6">
      <ToastContainer toasts={toasts} removeToast={removeToast} />
      <ConfirmDialog
        isOpen={confirmDialog.isOpen}
        onClose={() => setConfirmDialog({ isOpen: false, orcamentoId: null })}
        onConfirm={() => handleDeleteOrcamento(confirmDialog.orcamentoId)}
        title="Excluir Orçamento"
        message="Deseja realmente excluir este orçamento?"
        confirmText="Excluir"
      />
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">Orçamentos</h2>
          <p className="text-gray-600">{orcamentosFiltrados.length} orçamentos</p>
        </div>
        
        <button onClick={() => setShowModal(true)} className="btn-accent flex items-center gap-2">
          <Plus size={20} />
          Novo Orçamento
        </button>
      </div>

      <div className="card">
        <div className="relative">
          <Search className="absolute left-3 top-3 text-gray-400" size={20} />
          <input
            type="text"
            className="input pl-10"
            placeholder="Buscar por nome do kit, cliente ou número..."
            value={busca}
            onChange={(e) => setBusca(e.target.value)}
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {orcamentosFiltrados.map((orc) => (
          <div key={orc.id} className="card border-l-4 border-accent">
            <div className="flex justify-between mb-3">
              <div>
                <p className="text-xs text-gray-500">#{orc.numero}</p>
                <p className="font-bold text-lg">{orc.nome_kit}</p>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => navigate(`/orcamentos/${orc.id}`)}
                  className="text-accent hover:text-accent-dark"
                  title="Editar"
                >
                  <FileText size={20} />
                </button>
                <button
                  onClick={() => setConfirmDialog({ isOpen: true, orcamentoId: orc.id })}
                  className="text-red-500 hover:text-red-700"
                  title="Excluir"
                >
                  <Trash2 size={20} />
                </button>
              </div>
            </div>
            
            <p className="text-sm text-gray-600 mb-3">{orc.cliente_nome}</p>
            
            <div className="space-y-1 text-sm mb-3">
              <div className="flex justify-between">
                <span>Painéis:</span>
                <span className="font-semibold">{orc.quantidade_paineis}x {orc.potencia_painel}W</span>
              </div>
              <div className="flex justify-between">
                <span>Inversor:</span>
                <span className="font-semibold">{orc.potencia_inversor}W</span>
              </div>
              <div className="flex justify-between pt-2 border-t">
                <span className="font-medium">Total:</span>
                <span className="font-bold text-green-600">
                  R$ {(parseFloat(orc.valor_final) || 0).toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})}
                </span>
              </div>
            </div>
            
            <button 
              onClick={() => navigate(`/orcamentos/${orc.id}`)}
              className="w-full btn-accent text-sm py-2 flex items-center justify-center gap-1"
            >
              Ver Detalhes
            </button>
          </div>
        ))}
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <div className="bg-gradient-to-r from-accent to-accent/80 text-white p-6">
              <h3 className="text-2xl font-bold">Novo Orçamento</h3>
            </div>

            <form onSubmit={handleSubmit} className="p-6 space-y-6">
              {/* Básico */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold mb-2">Nome do Kit *</label>
                  <input
                    type="text"
                    className="input"
                    placeholder="Ex: Kit 5kWp Residencial"
                    value={formData.nome_kit}
                    onChange={(e) => setFormData({...formData, nome_kit: e.target.value})}
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold mb-2">Cliente *</label>
                  <select
                    className="input"
                    value={formData.cliente_id}
                    onChange={(e) => setFormData({...formData, cliente_id: e.target.value})}
                    required
                  >
                    <option value="">Selecione...</option>
                    {clientes.map(c => (
                      <option key={c.id} value={c.id}>{c.nome}</option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Valor Kit */}
              <div>
                <label className="block text-sm font-semibold mb-2">Valor do Kit Cotado (R$) *</label>
                <input
                  type="number"
                  step="0.01"
                  className="input text-lg font-bold"
                  placeholder="7160.00"
                  value={formData.valor_kit}
                  onChange={(e) => setFormData({...formData, valor_kit: e.target.value})}
                  required
                />
              </div>

              {/* Painel */}
              <div className="border-t pt-4">
                <div className="flex justify-between items-center mb-3">
                  <h4 className="font-bold">Painel Solar</h4>
                  {painelSelecionado && formData.quantidade_paineis && (
                    <span className="text-xs bg-accent text-primary px-3 py-1 rounded-full font-bold">
                      {((painelSelecionado.potencia_w * formData.quantidade_paineis) / 1000).toFixed(2)} kWp
                    </span>
                  )}
                </div>
                <div className="grid grid-cols-3 gap-4">
                  <div className="col-span-2 relative">
                    <label className="block text-sm font-semibold mb-2">Buscar Painel *</label>
                    {!painelSelecionado ? (
                      <>
                        <div className="relative">
                          <Search className="absolute left-3 top-3 text-gray-400" size={18} />
                          <input
                            type="text"
                            className="input pl-10"
                            placeholder="Digite 2+ caracteres (Ex: Era ou 550)"
                            value={searchPainel}
                            onChange={(e) => {
                              setSearchPainel(e.target.value);
                              setShowPainelDropdown(e.target.value.length >= 2);
                            }}
                            onFocus={() => searchPainel.length >= 2 && setShowPainelDropdown(true)}
                          />
                        </div>
                        {showPainelDropdown && paineisUnicos.length > 0 && (
                          <div className="mt-2 max-h-60 overflow-y-auto border rounded-lg bg-white shadow-lg absolute z-50 left-0 right-0">
                            {paineisUnicos.map(p => (
                              <div
                                key={p.id}
                                className="p-2 hover:bg-blue-50 cursor-pointer text-sm border-b"
                                onClick={() => {
                                  setPainelSelecionado(p);
                                  setFormData({
                                    ...formData,
                                    marca_painel: p.fabricante,
                                    potencia_painel: p.potencia_w
                                  });
                                  setSearchPainel('');
                                  setShowPainelDropdown(false);
                                }}
                              >
                                <div className="font-semibold">{p.fabricante}</div>
                                <div className="text-xs text-gray-600">{p.potencia_w}W</div>
                              </div>
                            ))}
                          </div>
                        )}
                        {showPainelDropdown && searchPainel.length >= 2 && paineisUnicos.length === 0 && (
                          <div className="mt-2 p-3 border rounded-lg bg-gray-50 text-sm text-gray-500 absolute z-50 left-0 right-0">
                            Nenhum painel encontrado
                          </div>
                        )}
                      </>
                    ) : (
                      <div className="flex items-center gap-2 p-3 bg-green-50 border-2 border-green-500 rounded-lg">
                        <div className="flex-1">
                          <div className="font-bold text-green-800">{painelSelecionado.fabricante}</div>
                          <div className="text-sm text-green-700">{painelSelecionado.potencia_w}W</div>
                        </div>
                        <button
                          type="button"
                          onClick={() => {
                            setPainelSelecionado(null);
                            setFormData({...formData, marca_painel: '', potencia_painel: ''});
                          }}
                          className="text-red-500 hover:text-red-700 font-bold"
                        >
                          ×
                        </button>
                      </div>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-semibold mb-2">Quantidade *</label>
                    <input
                      type="number"
                      className="input"
                      value={formData.quantidade_paineis}
                      onChange={(e) => setFormData({...formData, quantidade_paineis: e.target.value})}
                      required
                    />
                  </div>
                </div>
              </div>

              {/* Inversor */}
              <div className="border-t pt-4">
                <div className="flex justify-between items-center mb-3">
                  <h4 className="font-bold">Inversor</h4>
                  {inversorSelecionado && painelSelecionado && formData.quantidade_paineis && (
                    <div className="flex items-center gap-2">
                      <span className="text-xs bg-purple-100 text-purple-800 px-3 py-1 rounded-full font-bold">
                        Overload: {inversorSelecionado.overload ? `${((inversorSelecionado.overload - 1) * 100).toFixed(0)}%` : 'N/A'}
                      </span>
                      <span className={`text-xs px-3 py-1 rounded-full font-bold ${
                        (() => {
                          const potPaineis = painelSelecionado.potencia_w * formData.quantidade_paineis;
                          const potInversor = formData.potencia_inversor * formData.quantidade_inversores;
                          const overloadUsado = ((potPaineis / potInversor - 1) * 100);
                          const overloadMax = (inversorSelecionado.overload - 1) * 100;
                          return overloadUsado <= overloadMax ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800';
                        })()
                      }`}>
                        Usando: {(() => {
                          const potPaineis = painelSelecionado.potencia_w * formData.quantidade_paineis;
                          const potInversor = formData.potencia_inversor * formData.quantidade_inversores;
                          const overloadUsado = ((potPaineis / potInversor - 1) * 100);
                          return overloadUsado > 0 ? `${overloadUsado.toFixed(1)}%` : '0%';
                        })()}
                      </span>
                    </div>
                  )}
                </div>
                <div className="grid grid-cols-3 gap-4">
                  <div className="col-span-2 relative">
                    <label className="block text-sm font-semibold mb-2">Buscar Inversor *</label>
                    {!inversorSelecionado ? (
                      <>
                        <div className="relative">
                          <Search className="absolute left-3 top-3 text-gray-400" size={18} />
                          <input
                            type="text"
                            className="input pl-10"
                            placeholder="Digite 2+ caracteres (Ex: Growatt ou 5000)"
                            value={searchInversor}
                            onChange={(e) => {
                              setSearchInversor(e.target.value);
                              setShowInversorDropdown(e.target.value.length >= 2);
                            }}
                            onFocus={() => searchInversor.length >= 2 && setShowInversorDropdown(true)}
                          />
                        </div>
                        {showInversorDropdown && inversoresUnicos.length > 0 && (
                          <div className="mt-2 max-h-60 overflow-y-auto border rounded-lg bg-white shadow-lg absolute z-50 left-0 right-0">
                            {inversoresUnicos.map(i => (
                              <div
                                key={i.id}
                                className="p-2 hover:bg-blue-50 cursor-pointer text-sm border-b"
                                onClick={() => {
                                  setInversorSelecionado(i);
                                  setFormData({
                                    ...formData,
                                    marca_inversor: i.fabricante,
                                    potencia_inversor: i.potencia_w
                                  });
                                  setSearchInversor('');
                                  setShowInversorDropdown(false);
                                }}
                              >
                                <div className="font-semibold">{i.fabricante}</div>
                                <div className="text-xs text-gray-600">{i.potencia_w}W</div>
                              </div>
                            ))}
                          </div>
                        )}
                        {showInversorDropdown && searchInversor.length >= 2 && inversoresUnicos.length === 0 && (
                          <div className="mt-2 p-3 border rounded-lg bg-gray-50 text-sm text-gray-500 absolute z-50 left-0 right-0">
                            Nenhum inversor encontrado
                          </div>
                        )}
                      </>
                    ) : (
                      <div className="flex items-center gap-2 p-3 bg-green-50 border-2 border-green-500 rounded-lg">
                        <div className="flex-1">
                          <div className="font-bold text-green-800">{inversorSelecionado.fabricante}</div>
                          <div className="text-sm text-green-700">{inversorSelecionado.potencia_w}W</div>
                        </div>
                        <button
                          type="button"
                          onClick={() => {
                            setInversorSelecionado(null);
                            setFormData({...formData, marca_inversor: '', potencia_inversor: ''});
                          }}
                          className="text-red-500 hover:text-red-700 font-bold"
                        >
                          ×
                        </button>
                      </div>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-semibold mb-2">Quantidade</label>
                    <input
                      type="number"
                      className="input"
                      value={formData.quantidade_inversores}
                      onChange={(e) => setFormData({...formData, quantidade_inversores: e.target.value})}
                    />
                  </div>
                </div>
              </div>

              {/* Estrutura e Custos */}
              <div className="border-t pt-4">
                <h4 className="font-bold mb-3">Estrutura e Custos</h4>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold mb-2">Tipo Estrutura *</label>
                    <select
                      className="input"
                      value={formData.tipo_estrutura}
                      onChange={(e) => setFormData({...formData, tipo_estrutura: e.target.value})}
                    >
                      <option value="ceramico">Cerâmico/Colonial</option>
                      <option value="fibromadeira">Fibromadeira</option>
                      <option value="fibrometal">Fibrometal</option>
                      <option value="zinco">Zinco</option>
                      <option value="solo">Solo</option>
                      <option value="laje">Laje</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold mb-2 flex items-center gap-1">
                      Material Elétrico (R$)
                      <Calculator size={14} className="text-accent" />
                    </label>
                    <input
                      type="number"
                      step="0.01"
                      className="input bg-blue-50"
                      value={formData.valor_material_eletrico}
                      readOnly
                    />
                  </div>
                </div>
              </div>

              {/* Pagamento */}
              <div className="border-t pt-4">
                <h4 className="font-bold mb-3">Forma de Pagamento</h4>
                <select
                  className="input"
                  value={formData.forma_pagamento}
                  onChange={(e) => setFormData({...formData, forma_pagamento: e.target.value})}
                >
                  <option value="avista">À vista</option>
                  {premissas?.taxas_maquininha && Object.keys(premissas.taxas_maquininha).map(p => (
                    <option key={p} value={p}>{p}x ({premissas.taxas_maquininha[p]}%)</option>
                  ))}
                </select>
              </div>

              <div className="flex gap-3 pt-4">
                <button 
                  type="button" 
                  onClick={() => { setShowModal(false); resetForm(); }} 
                  className="flex-1 btn-outline"
                >
                  Cancelar
                </button>
                <button type="submit" className="flex-1 btn-accent">
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
