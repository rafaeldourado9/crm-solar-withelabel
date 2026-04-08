import { useState, useEffect } from 'react';
import { Users, Plus, Edit, Trash, Lock, Unlock, TrendingUp, UserCheck, Key, History, CheckCircle } from 'lucide-react';
import { vendedoresAPI } from '../services/api';
import { useToast, ToastContainer } from '../components/Toast';
import { ConfirmDialog } from '../components/ConfirmDialog';

const formatarValor = (v) =>
  Number(v).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

const Vendedores = () => {
  const [vendedores, setVendedores] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [showResumo, setShowResumo] = useState(false);
  const [resumo, setResumo] = useState(null);
  const [showHistorico, setShowHistorico] = useState(false);
  const [historico, setHistorico] = useState(null);
  const [editando, setEditando] = useState(null);
  const { toasts, showToast, removeToast } = useToast();
  const [confirmDelete, setConfirmDelete] = useState({ isOpen: false, id: null });

  const [formData, setFormData] = useState({
    nome: '', email: '', password: '', role: 'vendedor',
  });

  useEffect(() => { carregarVendedores(); }, []);

  const carregarVendedores = async () => {
    try {
      const res = await vendedoresAPI.listar();
      setVendedores(Array.isArray(res.data) ? res.data : []);
    } catch {
      showToast('Erro ao carregar vendedores', 'error');
      setVendedores([]);
    }
  };

  const abrirCriar = () => {
    setEditando(null);
    setFormData({ nome: '', email: '', password: '', role: 'vendedor' });
    setShowModal(true);
  };

  const abrirEditar = (v) => {
    setEditando(v);
    setFormData({ nome: v.nome, email: v.email, password: '', role: v.role });
    setShowModal(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editando) {
        await vendedoresAPI.atualizar(editando.id, { nome: formData.nome, role: formData.role });
        showToast('Vendedor atualizado!', 'success');
      } else {
        await vendedoresAPI.criar(formData);
        showToast(`Vendedor criado! Email: ${formData.email}`, 'success');
      }
      setShowModal(false);
      carregarVendedores();
    } catch (error) {
      const msg = error.response?.data?.detail || 'Erro ao salvar vendedor';
      showToast(msg, 'error');
    }
  };

  const handleBloquear = async (id) => {
    try {
      await vendedoresAPI.bloquear(id);
      showToast('Status atualizado!', 'success');
      carregarVendedores();
    } catch {
      showToast('Erro ao atualizar status', 'error');
    }
  };

  const handleResetarSenha = async (id) => {
    const novaSenha = window.prompt('Nova senha (mínimo 6 caracteres):');
    if (!novaSenha) return;
    if (novaSenha.length < 6) { showToast('Senha muito curta', 'error'); return; }
    try {
      await vendedoresAPI.resetarSenha(id, { nova_senha: novaSenha });
      showToast('Senha redefinida!', 'success');
    } catch {
      showToast('Erro ao redefinir senha', 'error');
    }
  };

  const handleDelete = async (id) => {
    try {
      await vendedoresAPI.deletar(id);
      showToast('Vendedor excluído', 'success');
      carregarVendedores();
    } catch {
      showToast('Erro ao excluir vendedor', 'error');
    }
  };

  const verResumo = async (id) => {
    try {
      const res = await vendedoresAPI.resumo(id);
      setResumo(res.data);
      setShowResumo(true);
    } catch {
      showToast('Erro ao carregar resumo', 'error');
    }
  };

  const verHistorico = async (id) => {
    try {
      const res = await vendedoresAPI.historico(id);
      setHistorico(res.data);
      setShowHistorico(true);
    } catch {
      showToast('Erro ao carregar histórico', 'error');
    }
  };

  const handleMarcarPago = async (vendaId) => {
    try {
      await vendedoresAPI.marcarComissaoPaga(vendaId);
      showToast('Comissão marcada como paga!', 'success');
      // Recarrega histórico
      const res = await vendedoresAPI.historico(historico.vendedor_id);
      setHistorico(res.data);
    } catch {
      showToast('Erro ao marcar comissão', 'error');
    }
  };

  return (
    <div className="space-y-6">
      <ToastContainer toasts={toasts} removeToast={removeToast} />
      <ConfirmDialog
        isOpen={confirmDelete.isOpen}
        onClose={() => setConfirmDelete({ isOpen: false, id: null })}
        onConfirm={() => handleDelete(confirmDelete.id)}
        title="Excluir Vendedor"
        message="Deseja excluir este vendedor? Esta ação é irreversível."
        confirmText="Excluir"
      />

      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Users size={28} className="text-accent" />
          <h2 className="text-2xl font-bold">Vendedores</h2>
        </div>
        <button onClick={abrirCriar} className="btn-accent flex items-center gap-2">
          <Plus size={18} />
          Novo Vendedor
        </button>
      </div>

      {/* Resumo */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card">
          <div className="flex items-center gap-3">
            <Users className="text-blue-500" size={28} />
            <div>
              <p className="text-sm text-gray-500">Total</p>
              <p className="text-2xl font-bold">{vendedores.length}</p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center gap-3">
            <UserCheck className="text-green-500" size={28} />
            <div>
              <p className="text-sm text-gray-500">Ativos</p>
              <p className="text-2xl font-bold">{vendedores.filter(v => v.ativo && !v.bloqueado).length}</p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center gap-3">
            <Lock className="text-red-500" size={28} />
            <div>
              <p className="text-sm text-gray-500">Bloqueados</p>
              <p className="text-2xl font-bold">{vendedores.filter(v => v.bloqueado).length}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabela */}
      <div className="card overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="text-left py-3 px-4 font-semibold">Nome</th>
              <th className="text-left py-3 px-4 font-semibold">Email</th>
              <th className="text-left py-3 px-4 font-semibold">Tipo</th>
              <th className="text-left py-3 px-4 font-semibold">Status</th>
              <th className="text-right py-3 px-4 font-semibold">Ações</th>
            </tr>
          </thead>
          <tbody>
            {vendedores.map((v) => (
              <tr key={v.id} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="py-3 px-4 font-medium">{v.nome}</td>
                <td className="py-3 px-4 text-sm text-gray-600">{v.email}</td>
                <td className="py-3 px-4">
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                    v.role === 'indicacao' ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'
                  }`}>
                    {v.role === 'indicacao' ? 'Indicação' : 'Vendedor'}
                  </span>
                </td>
                <td className="py-3 px-4">
                  {v.bloqueado
                    ? <span className="px-2 py-0.5 bg-red-100 text-red-600 rounded text-xs">Bloqueado</span>
                    : <span className="px-2 py-0.5 bg-green-100 text-green-600 rounded text-xs">Ativo</span>
                  }
                </td>
                <td className="py-3 px-4 text-right">
                  <div className="flex gap-2 justify-end">
                    <button onClick={() => verResumo(v.id)} className="text-purple-500 hover:text-purple-700" title="Resumo">
                      <TrendingUp size={17} />
                    </button>
                    <button onClick={() => verHistorico(v.id)} className="text-indigo-500 hover:text-indigo-700" title="Histórico de Comissões">
                      <History size={17} />
                    </button>
                    <button onClick={() => handleResetarSenha(v.id)} className="text-yellow-500 hover:text-yellow-700" title="Resetar Senha">
                      <Key size={17} />
                    </button>
                    <button onClick={() => abrirEditar(v)} className="text-blue-500 hover:text-blue-700" title="Editar">
                      <Edit size={17} />
                    </button>
                    <button
                      onClick={() => handleBloquear(v.id)}
                      className={v.bloqueado ? 'text-green-500 hover:text-green-700' : 'text-orange-500 hover:text-orange-700'}
                      title={v.bloqueado ? 'Desbloquear' : 'Bloquear'}
                    >
                      {v.bloqueado ? <Unlock size={17} /> : <Lock size={17} />}
                    </button>
                    <button onClick={() => setConfirmDelete({ isOpen: true, id: v.id })} className="text-red-500 hover:text-red-700" title="Excluir">
                      <Trash size={17} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
            {vendedores.length === 0 && (
              <tr><td colSpan={5} className="text-center py-10 text-gray-400">Nenhum vendedor cadastrado</td></tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Modal Criar/Editar */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-8 max-w-md w-full mx-4">
            <h3 className="text-xl font-bold mb-6">{editando ? 'Editar' : 'Novo'} Vendedor</h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Nome Completo *</label>
                <input type="text" className="input w-full" value={formData.nome}
                  onChange={(e) => setFormData({ ...formData, nome: e.target.value })} required />
              </div>
              {!editando && (
                <div>
                  <label className="block text-sm font-medium mb-1">Email *</label>
                  <input type="email" className="input w-full" value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })} required />
                </div>
              )}
              {!editando && (
                <div>
                  <label className="block text-sm font-medium mb-1">Senha *</label>
                  <input type="password" className="input w-full" value={formData.password} minLength={6}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })} required placeholder="Mínimo 6 caracteres" />
                </div>
              )}
              <div>
                <label className="block text-sm font-medium mb-1">Tipo</label>
                <select className="input" value={formData.role}
                  onChange={(e) => setFormData({ ...formData, role: e.target.value })}>
                  <option value="vendedor">Vendedor</option>
                  <option value="indicacao">Indicação</option>
                </select>
              </div>
              <div className="flex gap-3 pt-2">
                <button type="button" onClick={() => setShowModal(false)} className="flex-1 btn-outline">Cancelar</button>
                <button type="submit" className="flex-1 btn-accent">Salvar</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal Histórico de Comissões */}
      {showHistorico && historico && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-8 max-w-2xl w-full mx-4 max-h-[85vh] overflow-y-auto">
            <h3 className="text-xl font-bold mb-2">Histórico de Comissões — {historico.nome}</h3>

            {/* Totais */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
              <div className="bg-blue-50 rounded-lg p-3">
                <p className="text-xs text-gray-500">Volume de Vendas</p>
                <p className="text-sm font-bold text-blue-700">{formatarValor(historico.total_vendas)}</p>
              </div>
              <div className="bg-yellow-50 rounded-lg p-3">
                <p className="text-xs text-gray-500">Total Comissão</p>
                <p className="text-sm font-bold text-yellow-700">{formatarValor(historico.total_comissao)}</p>
              </div>
              <div className="bg-green-50 rounded-lg p-3">
                <p className="text-xs text-gray-500">Pago</p>
                <p className="text-sm font-bold text-green-700">{formatarValor(historico.total_pago)}</p>
              </div>
              <div className="bg-red-50 rounded-lg p-3">
                <p className="text-xs text-gray-500">A Pagar</p>
                <p className="text-sm font-bold text-red-700">{formatarValor(historico.total_a_pagar)}</p>
              </div>
            </div>

            {/* Lista de vendas */}
            {historico.vendas.length === 0 ? (
              <p className="text-gray-400 text-sm text-center py-8">Nenhuma venda registrada</p>
            ) : (
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-200 text-left">
                    <th className="py-2 font-semibold">Data</th>
                    <th className="py-2 font-semibold">Valor Venda</th>
                    <th className="py-2 font-semibold">Comissão</th>
                    <th className="py-2 font-semibold">Status</th>
                    <th className="py-2 font-semibold"></th>
                  </tr>
                </thead>
                <tbody>
                  {historico.vendas.map((v) => (
                    <tr key={v.id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-2 text-gray-500 text-xs">
                        {new Date(v.created_at).toLocaleDateString('pt-BR')}
                      </td>
                      <td className="py-2 font-medium">{formatarValor(v.valor_venda)}</td>
                      <td className="py-2 text-yellow-700 font-medium">{formatarValor(v.valor_comissao)}</td>
                      <td className="py-2">
                        {v.pago
                          ? <span className="px-2 py-0.5 bg-green-100 text-green-700 rounded text-xs">Pago</span>
                          : <span className="px-2 py-0.5 bg-orange-100 text-orange-700 rounded text-xs">Pendente</span>
                        }
                      </td>
                      <td className="py-2 text-right">
                        {!v.pago && (
                          <button
                            onClick={() => handleMarcarPago(v.id)}
                            className="text-green-600 hover:text-green-800"
                            title="Marcar como pago"
                          >
                            <CheckCircle size={16} />
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}

            <button onClick={() => setShowHistorico(false)} className="btn-accent w-full mt-6">Fechar</button>
          </div>
        </div>
      )}

      {/* Modal Resumo */}
      {showResumo && resumo && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-8 max-w-md w-full mx-4">
            <h3 className="text-xl font-bold mb-6">Resumo — {resumo.nome}</h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="card bg-blue-50">
                <p className="text-xs text-gray-500">Clientes</p>
                <p className="text-3xl font-bold text-blue-600">{resumo.total_clientes}</p>
              </div>
              <div className="card bg-purple-50">
                <p className="text-xs text-gray-500">Contratos</p>
                <p className="text-3xl font-bold text-purple-600">{resumo.total_contratos}</p>
              </div>
              <div className="card bg-green-50">
                <p className="text-xs text-gray-500">Volume de Vendas</p>
                <p className="text-xl font-bold text-green-600">{formatarValor(resumo.valor_total_vendas)}</p>
              </div>
              <div className="card bg-yellow-50">
                <p className="text-xs text-gray-500">Comissão Estimada</p>
                <p className="text-xl font-bold text-yellow-600">{formatarValor(resumo.comissao_estimada)}</p>
              </div>
            </div>
            <button onClick={() => setShowResumo(false)} className="btn-accent w-full mt-6">Fechar</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Vendedores;
