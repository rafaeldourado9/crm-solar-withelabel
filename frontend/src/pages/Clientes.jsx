import { useState, useEffect } from 'react';
import { Search, Plus, Edit2, Trash2 } from 'lucide-react';
import { clientesService } from '../services/clientesService';

const Clientes = () => {
  const [clientes, setClientes] = useState([]);
  const [vendedores, setVendedores] = useState([]);
  const [filtro, setFiltro] = useState('todos');
  const [busca, setBusca] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    nome: '',
    cpf_cnpj: '',
    telefone: '',
    email: '',
    cidade: '',
    estado: '',
    vendedor: '',
    status: 'orcamento'
  });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    carregarClientes();
    carregarVendedores();
  }, [filtro]);

  const carregarClientes = async () => {
    try {
      const params = filtro !== 'todos' ? { status: filtro } : {};
      const response = await clientesService.getAll(params);
      setClientes(Array.isArray(response.data) ? response.data : response.data.results || []);
    } catch (error) {
      console.error('Erro ao carregar clientes:', error);
    }
  };

  const carregarVendedores = async () => {
    try {
      const response = await clientesService.api.get('/vendedores/');
      const data = Array.isArray(response.data) ? response.data : response.data.results || [];
      setVendedores(data.filter(v => v.ativo && !v.bloqueado));
    } catch (error) {
      console.error('Erro ao carregar vendedores:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        await clientesService.update(editingId, formData);
      } else {
        await clientesService.create(formData);
      }
      setShowModal(false);
      setEditingId(null);
      setFormData({ nome: '', cpf_cnpj: '', telefone: '', email: '', cidade: '', estado: '', vendedor: '', status: 'orcamento' });
      carregarClientes();
    } catch (error) {
      console.error('Erro ao salvar cliente:', error);
    }
  };

  const handleEdit = (cliente) => {
    setFormData(cliente);
    setEditingId(cliente.id);
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (confirm('Deseja realmente excluir este cliente?')) {
      try {
        await clientesService.delete(id);
        carregarClientes();
      } catch (error) {
        console.error('Erro ao excluir cliente:', error);
      }
    }
  };

  const clientesFiltrados = Array.isArray(clientes) ? clientes.filter(c => 
    c.nome.toLowerCase().includes(busca.toLowerCase()) ||
    c.cidade.toLowerCase().includes(busca.toLowerCase())
  ) : [];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="Buscar clientes..."
            className="input pl-10"
            value={busca}
            onChange={(e) => setBusca(e.target.value)}
          />
        </div>
        
        <button onClick={() => setShowModal(true)} className="btn-accent flex items-center gap-2">
          <Plus size={20} />
          Novo Cliente
        </button>
      </div>

      <div className="flex gap-2">
        {['todos', 'orcamento', 'proposta', 'contrato'].map((status) => (
          <button
            key={status}
            onClick={() => setFiltro(status)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              filtro === status
                ? 'bg-accent text-primary'
                : 'bg-white border border-gray-300 hover:bg-gray-50'
            }`}
          >
            {status.charAt(0).toUpperCase() + status.slice(1)}
          </button>
        ))}
      </div>

      <div className="card">
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
                    <button onClick={() => handleEdit(cliente)} className="text-blue-600 hover:text-blue-800 mr-3">
                      <Edit2 size={18} />
                    </button>
                    <button onClick={() => handleDelete(cliente.id)} className="text-red-600 hover:text-red-800">
                      <Trash2 size={18} />
                    </button>
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
                    onChange={(e) => setFormData({...formData, cpf_cnpj: e.target.value})}
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
                
                <div>
                  <label className="block text-sm font-medium mb-2">Email</label>
                  <input
                    type="email"
                    className="input"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
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
                  <input
                    type="text"
                    className="input"
                    maxLength="2"
                    value={formData.estado}
                    onChange={(e) => setFormData({...formData, estado: e.target.value.toUpperCase()})}
                  />
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
                    setFormData({ nome: '', cpf_cnpj: '', telefone: '', email: '', cidade: '', estado: '', vendedor: '', status: 'orcamento' });
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
