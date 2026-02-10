import { useState, useEffect } from 'react';
import { Search, Plus, Edit2, Trash2, Edit, Trash } from 'lucide-react';
import { clientesService } from '../services/clientesService';
import { useToast, ToastContainer } from '../components/Toast';
import { ConfirmDialog } from '../components/ConfirmDialog';
import api from '../services/api';

const Clientes = () => {
  const { toasts, showToast, removeToast } = useToast();
  const [clientes, setClientes] = useState([]);
  const [vendedores, setVendedores] = useState([]);
  const [filtro, setFiltro] = useState('todos');
  const [busca, setBusca] = useState('');
  const [paginaAtual, setPaginaAtual] = useState(1);
  const [totalPaginas, setTotalPaginas] = useState(1);
  const [totalClientes, setTotalClientes] = useState(0);
  const [showModal, setShowModal] = useState(false);
  const [confirmDialog, setConfirmDialog] = useState({ isOpen: false, clienteId: null });
  const [formData, setFormData] = useState({
    nome: '',
    cpf_cnpj: '',
    telefone: '',
    email: '',
    cep: '',
    endereco: '',
    bairro: '',
    cidade: '',
    estado: '',
    vendedor: '',
    status: 'orcamento'
  });
  const [editingId, setEditingId] = useState(null);
  const [buscandoCep, setBuscandoCep] = useState(false);

  const formatarCEP = (valor) => {
    const numeros = valor.replace(/\D/g, '').substring(0, 8);
    if (numeros.length <= 5) return numeros;
    return `${numeros.slice(0, 5)}-${numeros.slice(5)}`;
  };

  const formatarTelefone = (valor) => {
    const numeros = valor.replace(/\D/g, '');
    if (numeros.length <= 2) return numeros;
    if (numeros.length <= 6) return `(${numeros.slice(0, 2)}) ${numeros.slice(2)}`;
    if (numeros.length <= 10) return `(${numeros.slice(0, 2)}) ${numeros.slice(2, 6)}-${numeros.slice(6)}`;
    return `(${numeros.slice(0, 2)}) ${numeros.slice(2, 7)}-${numeros.slice(7, 11)}`;
  };

  const formatarCPFCNPJ = (valor) => {
    const numeros = valor.replace(/\D/g, '');
    if (numeros.length <= 11) {
      // CPF: 000.000.000-00
      if (numeros.length <= 3) return numeros;
      if (numeros.length <= 6) return `${numeros.slice(0, 3)}.${numeros.slice(3)}`;
      if (numeros.length <= 9) return `${numeros.slice(0, 3)}.${numeros.slice(3, 6)}.${numeros.slice(6)}`;
      return `${numeros.slice(0, 3)}.${numeros.slice(3, 6)}.${numeros.slice(6, 9)}-${numeros.slice(9, 11)}`;
    } else {
      // CNPJ: 00.000.000/0000-00
      if (numeros.length <= 2) return numeros;
      if (numeros.length <= 5) return `${numeros.slice(0, 2)}.${numeros.slice(2)}`;
      if (numeros.length <= 8) return `${numeros.slice(0, 2)}.${numeros.slice(2, 5)}.${numeros.slice(5)}`;
      if (numeros.length <= 12) return `${numeros.slice(0, 2)}.${numeros.slice(2, 5)}.${numeros.slice(5, 8)}/${numeros.slice(8)}`;
      return `${numeros.slice(0, 2)}.${numeros.slice(2, 5)}.${numeros.slice(5, 8)}/${numeros.slice(8, 12)}-${numeros.slice(12, 14)}`;
    }
  };

  const buscarCep = async (cep) => {
    const cepLimpo = cep.replace(/\D/g, '');
    if (cepLimpo.length !== 8) return;
    
    setBuscandoCep(true);
    try {
      const response = await fetch(`https://viacep.com.br/ws/${cepLimpo}/json/`);
      const data = await response.json();
      
      if (!data.erro) {
        setFormData({
          ...formData,
          cidade: data.localidade,
          estado: data.uf,
          endereco: data.logradouro,
          bairro: data.bairro
        });
        showToast('CEP encontrado!', 'success');
      } else {
        showToast('CEP não encontrado', 'error');
      }
    } catch (error) {
      showToast('Erro ao buscar CEP', 'error');
    } finally {
      setBuscandoCep(false);
    }
  };

  useEffect(() => {
    carregarClientes(1);
    carregarVendedores();
  }, [filtro, busca]);

  const carregarClientes = async (pagina = 1) => {
    try {
      const params = { page: pagina, page_size: 50 };
      if (filtro !== 'todos') params.status = filtro;
      if (busca) params.search = busca;
      
      const response = await clientesService.getAll(params);
      const data = response.data;
      
      setClientes(data.results || []);
      setTotalClientes(data.count || 0);
      setTotalPaginas(Math.ceil((data.count || 0) / 50));
      setPaginaAtual(pagina);
    } catch (error) {
      console.error('Erro ao carregar clientes:', error);
    }
  };

  const carregarVendedores = async () => {
    try {
      const response = await api.get('/vendedores/');
      const data = Array.isArray(response.data) ? response.data : response.data.results || [];
      setVendedores(data.filter(v => v.ativo && !v.bloqueado));
    } catch (error) {
      console.error('Erro ao carregar vendedores:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const dadosParaSalvar = {
        ...formData,
        cep: formData.cep.replace(/\D/g, '') // Remove hífen antes de salvar
      };
      
      if (editingId) {
        await clientesService.update(editingId, dadosParaSalvar);
        showToast('Cliente atualizado com sucesso', 'success');
      } else {
        await clientesService.create(dadosParaSalvar);
        showToast('Cliente criado com sucesso', 'success');
      }
      setShowModal(false);
      setEditingId(null);
      setFormData({ nome: '', cpf_cnpj: '', telefone: '', email: '', cep: '', endereco: '', bairro: '', cidade: '', estado: '', vendedor: '', status: 'orcamento' });
      carregarClientes(paginaAtual);
    } catch (error) {
      console.error('Erro ao salvar cliente:', error);
      showToast('Erro ao salvar cliente', 'error');
    }
  };

  const handleEdit = (cliente) => {
    setFormData({
      ...cliente,
      cep: formatarCEP(cliente.cep || ''),
      vendedor: cliente.vendedor || '',
      estado: cliente.estado || ''
    });
    setEditingId(cliente.id);
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    try {
      await clientesService.delete(id);
      showToast('Cliente excluído com sucesso', 'success');
      carregarClientes(paginaAtual);
    } catch (error) {
      console.error('Erro ao excluir cliente:', error);
      showToast('Erro ao excluir cliente', 'error');
    }
  };

  const clientesFiltrados = clientes;

  return (
    <div className="space-y-6">
      <ToastContainer toasts={toasts} removeToast={removeToast} />
      <ConfirmDialog
        isOpen={confirmDialog.isOpen}
        onClose={() => setConfirmDialog({ isOpen: false, clienteId: null })}
        onConfirm={() => {
          handleDelete(confirmDialog.clienteId);
          setConfirmDialog({ isOpen: false, clienteId: null });
        }}
        title="Excluir Cliente"
        message="Deseja realmente excluir este cliente? Esta ação não pode ser desfeita."
        confirmText="Excluir"
      />
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">Clientes</h2>
          <p className="text-gray-600">{totalClientes} clientes (página {paginaAtual} de {totalPaginas})</p>
        </div>
        <button onClick={() => setShowModal(true)} className="btn-accent flex items-center gap-2">
          <Plus size={20} />
          Novo Cliente
        </button>
      </div>

      <div className="card">
        <div className="relative mb-4">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="Buscar por nome, vendedor, contato, cidade ou status..."
            className="input pl-10"
            value={busca}
            onChange={(e) => setBusca(e.target.value)}
          />
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 font-semibold">Nome</th>
                <th className="text-left py-3 px-4 font-semibold">Vendedor</th>
                <th className="text-left py-3 px-4 font-semibold">Contato</th>
                <th className="text-left py-3 px-4 font-semibold">Cidade</th>
                <th className="text-left py-3 px-4 font-semibold">Status</th>
                <th className="text-right py-3 px-4 font-semibold">Ações</th>
              </tr>
            </thead>
            <tbody>
              {clientesFiltrados.map((cliente) => (
                <tr key={cliente.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4 font-medium">{cliente.nome}</td>
                  <td className="py-3 px-4">
                    {cliente.vendedor_nome ? (
                      <span className="px-2 py-1 bg-purple-100 text-purple-600 rounded text-xs">{cliente.vendedor_nome}</span>
                    ) : (
                      <span className="text-gray-400 text-xs">Sem vendedor</span>
                    )}
                  </td>
                  <td className="py-3 px-4">{cliente.telefone || cliente.email || '-'}</td>
                  <td className="py-3 px-4">{cliente.cidade}</td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      cliente.status === 'orcamento' ? 'bg-blue-100 text-blue-800' :
                      cliente.status === 'proposta' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {cliente.status}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-right">
                    <div className="flex gap-2 justify-end">
                      <button 
                        onClick={() => handleEdit(cliente)}
                        className="text-blue-600 hover:text-blue-800"
                        title="Editar"
                      >
                        <Edit size={18} />
                      </button>
                      <button 
                        onClick={() => setConfirmDialog({ isOpen: true, clienteId: cliente.id })}
                        className="text-red-600 hover:text-red-800"
                        title="Excluir"
                      >
                        <Trash size={18} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          
          {clientesFiltrados.length === 0 && (
            <div className="text-center py-12 text-gray-500">
              Nenhum cliente encontrado
            </div>
          )}
        </div>
        
        {/* Paginação */}
        {totalPaginas > 1 && (
          <div className="flex justify-center items-center gap-2 mt-4">
            <button
              onClick={() => carregarClientes(paginaAtual - 1)}
              disabled={paginaAtual === 1}
              className="btn-outline px-4 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              ← Anterior
            </button>
            
            <div className="flex gap-1">
              {[...Array(Math.min(5, totalPaginas))].map((_, i) => {
                let pageNum;
                if (totalPaginas <= 5) {
                  pageNum = i + 1;
                } else if (paginaAtual <= 3) {
                  pageNum = i + 1;
                } else if (paginaAtual >= totalPaginas - 2) {
                  pageNum = totalPaginas - 4 + i;
                } else {
                  pageNum = paginaAtual - 2 + i;
                }
                
                return (
                  <button
                    key={i}
                    onClick={() => carregarClientes(pageNum)}
                    className={`px-3 py-2 rounded ${
                      paginaAtual === pageNum
                        ? 'bg-accent text-white'
                        : 'btn-outline'
                    }`}
                  >
                    {pageNum}
                  </button>
                );
              })}
            </div>
            
            <button
              onClick={() => carregarClientes(paginaAtual + 1)}
              disabled={paginaAtual === totalPaginas}
              className="btn-outline px-4 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Próxima →
            </button>
          </div>
        )}
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-8 max-w-2xl w-full mx-4">
            <h3 className="text-2xl font-bold mb-6">{editingId ? 'Editar Cliente' : 'Novo Cliente'}</h3>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Nome</label>
                  <input
                    type="text"
                    className="input"
                    value={formData.nome}
                    onChange={(e) => setFormData({...formData, nome: e.target.value})}
                    required
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-2">CPF/CNPJ</label>
                  <input
                    type="text"
                    className="input"
                    value={formData.cpf_cnpj}
                    onChange={(e) => setFormData({...formData, cpf_cnpj: formatarCPFCNPJ(e.target.value)})}
                    placeholder="000.000.000-00"
                    maxLength="18"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-2">Telefone</label>
                  <input
                    type="text"
                    className="input"
                    value={formData.telefone}
                    onChange={(e) => setFormData({...formData, telefone: formatarTelefone(e.target.value)})}
                    placeholder="(00) 00000-0000"
                    maxLength="15"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-2">Email</label>
                  <input
                    type="email"
                    className="input"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value.toLowerCase()})}
                    placeholder="email@exemplo.com"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-2">CEP</label>
                  <input
                    type="text"
                    className="input"
                    value={formData.cep}
                    onChange={(e) => {
                      const cepFormatado = formatarCEP(e.target.value);
                      setFormData({...formData, cep: cepFormatado});
                      const cepLimpo = cepFormatado.replace(/\D/g, '');
                      if (cepLimpo.length === 8) {
                        buscarCep(cepLimpo);
                      }
                    }}
                    placeholder="00000-000"
                    maxLength="9"
                  />
                  {buscandoCep && <span className="text-xs text-blue-600">Buscando...</span>}
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-2">Endereço</label>
                  <input
                    type="text"
                    className="input"
                    value={formData.endereco}
                    onChange={(e) => setFormData({...formData, endereco: e.target.value})}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-2">Bairro</label>
                  <input
                    type="text"
                    className="input"
                    value={formData.bairro}
                    onChange={(e) => setFormData({...formData, bairro: e.target.value})}
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
                  <label className="block text-sm font-medium mb-2">Estado</label>
                  <select
                    className="input"
                    value={formData.estado}
                    onChange={(e) => setFormData({...formData, estado: e.target.value})}
                    required
                  >
                    <option value="">Selecione...</option>
                    <option value="AC">Acre</option>
                    <option value="AL">Alagoas</option>
                    <option value="AP">Amapá</option>
                    <option value="AM">Amazonas</option>
                    <option value="BA">Bahia</option>
                    <option value="CE">Ceará</option>
                    <option value="DF">Distrito Federal</option>
                    <option value="ES">Espírito Santo</option>
                    <option value="GO">Goiás</option>
                    <option value="MA">Maranhão</option>
                    <option value="MT">Mato Grosso</option>
                    <option value="MS">Mato Grosso do Sul</option>
                    <option value="MG">Minas Gerais</option>
                    <option value="PA">Pará</option>
                    <option value="PB">Paraíba</option>
                    <option value="PR">Paraná</option>
                    <option value="PE">Pernambuco</option>
                    <option value="PI">Piauí</option>
                    <option value="RJ">Rio de Janeiro</option>
                    <option value="RN">Rio Grande do Norte</option>
                    <option value="RS">Rio Grande do Sul</option>
                    <option value="RO">Rondônia</option>
                    <option value="RR">Roraima</option>
                    <option value="SC">Santa Catarina</option>
                    <option value="SP">São Paulo</option>
                    <option value="SE">Sergipe</option>
                    <option value="TO">Tocantins</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-2">Vendedor</label>
                  <select
                    className="input"
                    value={formData.vendedor}
                    onChange={(e) => setFormData({...formData, vendedor: e.target.value})}
                  >
                    <option value="">Selecione um vendedor</option>
                    {vendedores.map(v => (
                      <option key={v.id} value={v.id}>{v.nome}</option>
                    ))}
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-2">Status</label>
                  <select
                    className="input"
                    value={formData.status}
                    onChange={(e) => setFormData({...formData, status: e.target.value})}
                  >
                    <option value="orcamento">Orçamento</option>
                    <option value="proposta">Proposta</option>
                    <option value="contrato">Contrato</option>
                  </select>
                </div>
              </div>
              
              <div className="flex gap-3 pt-4">
                <button 
                  type="button" 
                  onClick={() => {
                    setShowModal(false);
                    setEditingId(null);
                    setFormData({ nome: '', cpf_cnpj: '', telefone: '', email: '', cep: '', endereco: '', bairro: '', cidade: '', estado: '', vendedor: '', status: 'orcamento' });
                  }} 
                  className="btn-outline flex-1"
                >
                  Cancelar
                </button>
                <button type="submit" className="btn-accent flex-1">
                  {editingId ? 'Atualizar' : 'Criar'} Cliente
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Clientes;
