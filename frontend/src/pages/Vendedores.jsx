import { useState, useEffect } from 'react';
import { Users, Plus, Edit, Trash, Lock, Unlock, TrendingUp, UserCheck, Key } from 'lucide-react';
import api from '../services/api';
import { useToast, ToastContainer } from '../components/Toast';
import { ConfirmDialog } from '../components/ConfirmDialog';

const Vendedores = () => {
  const [vendedores, setVendedores] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [showResumo, setShowResumo] = useState(false);
  const [vendedorSelecionado, setVendedorSelecionado] = useState(null);
  const [resumo, setResumo] = useState(null);
  const { toasts, showToast, removeToast } = useToast();
  const [confirmDialog, setConfirmDialog] = useState({ isOpen: false, action: null, vendedorId: null });
  const [formData, setFormData] = useState({
    nome: '',
    cpf: '',
    telefone: '',
    email: '',
    senha: '',
    tipo: 'vendedor'
  });

  useEffect(() => {
    carregarVendedores();
  }, []);

  const carregarVendedores = async () => {
    try {
      const response = await api.get('/vendedores/');
      const data = Array.isArray(response.data) ? response.data : response.data.results || [];
      setVendedores(data);
    } catch (error) {
      console.error('Erro ao carregar vendedores:', error);
      showToast('Erro ao carregar vendedores', 'error');
      setVendedores([]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (formData.id) {
        await api.put(`/vendedores/${formData.id}/`, formData);
        showToast('Vendedor atualizado com sucesso!', 'success');
      } else {
        await api.post('/vendedores/', formData);
        showToast(`Vendedor criado! Email: ${formData.email}`, 'success');
      }
      setShowModal(false);
      setFormData({ nome: '', cpf: '', telefone: '', email: '', senha: '', tipo: 'vendedor' });
      carregarVendedores();
    } catch (error) {
      console.error('Erro ao salvar:', error);
      showToast('Erro ao salvar vendedor', 'error');
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(`/vendedores/${id}/`);
      showToast('Vendedor excluído com sucesso!', 'success');
      carregarVendedores();
    } catch (error) {
      console.error('Erro:', error);
      showToast('Erro ao excluir vendedor', 'error');
    }
  };

  const handleBloquear = async (id) => {
    try {
      await api.post(`/vendedores/${id}/bloquear/`);
      showToast('Status atualizado com sucesso!', 'success');
      carregarVendedores();
    } catch (error) {
      console.error('Erro:', error);
      showToast('Erro ao atualizar status', 'error');
    }
  };

  const handleResetarSenha = async (id) => {
    const novaSenha = prompt('Digite a nova senha (mínimo 6 caracteres):');
    if (novaSenha && novaSenha.length >= 6) {
      try {
        await api.post(`/vendedores/${id}/resetar_senha/`, { senha: novaSenha });
        showToast('Senha resetada com sucesso!', 'success');
      } catch (error) {
        console.error('Erro:', error);
        showToast('Erro ao resetar senha', 'error');
      }
    } else if (novaSenha) {
      showToast('Senha deve ter no mínimo 6 caracteres', 'warning');
    }
  };

  const carregarResumo = async (id) => {
    try {
      const response = await api.get(`/vendedores/${id}/resumo/`);
      setResumo(response.data);
      setVendedorSelecionado(vendedores.find(v => v.id === id));
      setShowResumo(true);
    } catch (error) {
      console.error('Erro:', error);
      showToast('Erro ao carregar resumo', 'error');
    }
  };

  const executeConfirmAction = () => {
    const { action, vendedorId } = confirmDialog;
    if (action === 'delete') handleDelete(vendedorId);
  };

  return (
    <div className="space-y-6">
      <ToastContainer toasts={toasts} removeToast={removeToast} />
      <ConfirmDialog
        isOpen={confirmDialog.isOpen}
        onClose={() => setConfirmDialog({ isOpen: false, action: null, vendedorId: null })}
        onConfirm={executeConfirmAction}
        title={confirmDialog.action === 'delete' ? 'Excluir Vendedor' : 'Confirmar'}
        message={confirmDialog.action === 'delete' ? 'Deseja excluir este vendedor?' : ''}
        confirmText="Confirmar"
      />
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Users size={32} className="text-accent" />
          <h2 className="text-2xl font-bold">Vendedores</h2>
        </div>
        <button 
          onClick={() => { 
            setFormData({ nome: '', cpf: '', telefone: '', email: '', senha: '', tipo: 'vendedor' }); 
            setShowModal(true); 
          }} 
          className="btn-accent flex items-center gap-2"
        >
          <Plus size={20} />
          Novo Vendedor
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center gap-3">
            <Users className="text-blue-600" size={32} />
            <div>
              <p className="text-sm text-gray-600">Total Vendedores</p>
              <p className="text-2xl font-bold">{vendedores.length}</p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center gap-3">
            <UserCheck className="text-green-600" size={32} />
            <div>
              <p className="text-sm text-gray-600">Ativos</p>
              <p className="text-2xl font-bold">{vendedores.filter(v => v.ativo && !v.bloqueado).length}</p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center gap-3">
            <Lock className="text-red-600" size={32} />
            <div>
              <p className="text-sm text-gray-600">Bloqueados</p>
              <p className="text-2xl font-bold">{vendedores.filter(v => v.bloqueado).length}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 font-semibold">Nome</th>
                <th className="text-left py-3 px-4 font-semibold">Email</th>
                <th className="text-left py-3 px-4 font-semibold">Telefone</th>
                <th className="text-left py-3 px-4 font-semibold">Clientes</th>
                <th className="text-left py-3 px-4 font-semibold">Status</th>
                <th className="text-right py-3 px-4 font-semibold">Ações</th>
              </tr>
            </thead>
            <tbody>
              {vendedores.map((vendedor) => (
                <tr key={vendedor.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4 font-medium">{vendedor.nome}</td>
                  <td className="py-3 px-4">{vendedor.email}</td>
                  <td className="py-3 px-4">{vendedor.telefone}</td>
                  <td className="py-3 px-4">{vendedor.total_clientes || 0}</td>
                  <td className="py-3 px-4">
                    {vendedor.bloqueado ? (
                      <span className="px-2 py-1 bg-red-100 text-red-600 rounded text-xs">Bloqueado</span>
                    ) : vendedor.ativo ? (
                      <span className="px-2 py-1 bg-green-100 text-green-600 rounded text-xs">Ativo</span>
                    ) : (
                      <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">Inativo</span>
                    )}
                  </td>
                  <td className="py-3 px-4 text-right flex gap-2 justify-end">
                    <button 
                      onClick={() => carregarResumo(vendedor.id)}
                      className="text-purple-600 hover:text-purple-800"
                      title="Ver Resumo"
                    >
                      <TrendingUp size={18} />
                    </button>
                    <button 
                      onClick={() => handleResetarSenha(vendedor.id)}
                      className="text-yellow-600 hover:text-yellow-800"
                      title="Resetar Senha"
                    >
                      <Key size={18} />
                    </button>
                    <button 
                      onClick={() => { setFormData(vendedor); setShowModal(true); }} 
                      className="text-blue-600 hover:text-blue-800"
                    >
                      <Edit size={18} />
                    </button>
                    <button 
                      onClick={() => handleBloquear(vendedor.id)}
                      className={vendedor.bloqueado ? "text-green-600 hover:text-green-800" : "text-orange-600 hover:text-orange-800"}
                      title={vendedor.bloqueado ? "Desbloquear" : "Bloquear"}
                    >
                      {vendedor.bloqueado ? <Unlock size={18} /> : <Lock size={18} />}
                    </button>
                    <button 
                      onClick={() => setConfirmDialog({ isOpen: true, action: 'delete', vendedorId: vendedor.id })} 
                      className="text-red-600 hover:text-red-800"
                    >
                      <Trash size={18} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-8 max-w-md w-full mx-4">
            <h3 className="text-2xl font-bold mb-6">
              {formData.id ? 'Editar' : 'Novo'} Vendedor
            </h3>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Nome Completo</label>
                <input
                  type="text"
                  className="input w-full"
                  value={formData.nome}
                  onChange={(e) => setFormData({...formData, nome: e.target.value})}
                  required
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">CPF</label>
                  <input
                    type="text"
                    className="input w-full"
                    value={formData.cpf}
                    onChange={(e) => setFormData({...formData, cpf: e.target.value})}
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Telefone</label>
                  <input
                    type="text"
                    className="input w-full"
                    value={formData.telefone}
                    onChange={(e) => setFormData({...formData, telefone: e.target.value})}
                    required
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">Email</label>
                <input
                  type="email"
                  className="input w-full"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  required
                />
              </div>
              
              {!formData.id && (
                <div>
                  <label className="block text-sm font-medium mb-2">Senha</label>
                  <input
                    type="password"
                    className="input w-full"
                    value={formData.senha}
                    onChange={(e) => setFormData({...formData, senha: e.target.value})}
                    required
                    minLength="6"
                    placeholder="Mínimo 6 caracteres"
                  />
                </div>
              )}
              
              <div className="flex gap-3 pt-4">
                <button type="button" onClick={() => setShowModal(false)} className="btn-outline flex-1">
                  Cancelar
                </button>
                <button type="submit" className="btn-accent flex-1">
                  Salvar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {showResumo && vendedorSelecionado && resumo && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-8 max-w-2xl w-full mx-4">
            <h3 className="text-2xl font-bold mb-6">Resumo - {vendedorSelecionado.nome}</h3>
            
            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="card bg-blue-50">
                <p className="text-sm text-gray-600">Total de Clientes</p>
                <p className="text-3xl font-bold text-blue-600">{resumo.total_clientes}</p>
              </div>
              <div className="card bg-green-50">
                <p className="text-sm text-gray-600">Clientes Ativos</p>
                <p className="text-3xl font-bold text-green-600">{resumo.clientes_ativos}</p>
              </div>
              <div className="card bg-purple-50">
                <p className="text-sm text-gray-600">Total de Vendas</p>
                <p className="text-3xl font-bold text-purple-600">{resumo.total_vendas}</p>
              </div>
              <div className="card bg-yellow-50">
                <p className="text-sm text-gray-600">Valor Total</p>
                <p className="text-3xl font-bold text-yellow-600">
                  R$ {resumo.valor_total?.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                </p>
              </div>
            </div>
            
            <button 
              onClick={() => setShowResumo(false)} 
              className="btn-accent w-full"
            >
              Fechar
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Vendedores;
