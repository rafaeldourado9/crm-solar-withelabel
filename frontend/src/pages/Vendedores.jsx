import { useState, useEffect } from 'react';
import { Users, Plus, Edit, Trash, Lock, Unlock, TrendingUp, UserCheck, Key, History, CheckCircle } from 'lucide-react';
import { vendedoresAPI } from '../services/api';
import { useToast, ToastContainer } from '../components/Toast';
import { ConfirmDialog } from '../components/ConfirmDialog';

const formatarValor = (v) => Number(v).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

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
  const [formData, setFormData] = useState({ nome: '', email: '', password: '', role: 'vendedor' });

  useEffect(() => { carregarVendedores(); }, []);

  const carregarVendedores = async () => {
    try { const res = await vendedoresAPI.listar(); setVendedores(Array.isArray(res.data) ? res.data : []); }
    catch { showToast('Erro ao carregar vendedores', 'error'); setVendedores([]); }
  };

  const abrirCriar = () => { setEditando(null); setFormData({ nome: '', email: '', password: '', role: 'vendedor' }); setShowModal(true); };
  const abrirEditar = (v) => { setEditando(v); setFormData({ nome: v.nome, email: v.email, password: '', role: v.role }); setShowModal(true); };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editando) { await vendedoresAPI.atualizar(editando.id, { nome: formData.nome, role: formData.role }); showToast('Vendedor atualizado!', 'success'); }
      else { await vendedoresAPI.criar(formData); showToast(`Vendedor criado! Email: ${formData.email}`, 'success'); }
      setShowModal(false); carregarVendedores();
    } catch (error) { const msg = error.response?.data?.detail || 'Erro ao salvar vendedor'; showToast(msg, 'error'); }
  };

  const handleBloquear = async (id) => {
    try { await vendedoresAPI.bloquear(id); showToast('Status atualizado!', 'success'); carregarVendedores(); }
    catch { showToast('Erro ao atualizar status', 'error'); }
  };

  const handleResetarSenha = async (id) => {
    const novaSenha = window.prompt('Nova senha (mínimo 6 caracteres):');
    if (!novaSenha) return;
    if (novaSenha.length < 6) { showToast('Senha muito curta', 'error'); return; }
    try { await vendedoresAPI.resetarSenha(id, { nova_senha: novaSenha }); showToast('Senha redefinida!', 'success'); }
    catch { showToast('Erro ao redefinir senha', 'error'); }
  };

  const handleDelete = async (id) => {
    try { await vendedoresAPI.deletar(id); showToast('Vendedor excluído', 'success'); carregarVendedores(); }
    catch { showToast('Erro ao excluir vendedor', 'error'); }
  };

  const verResumo = async (id) => {
    try { const res = await vendedoresAPI.resumo(id); setResumo(res.data); setShowResumo(true); }
    catch { showToast('Erro ao carregar resumo', 'error'); }
  };

  const verHistorico = async (id) => {
    try { const res = await vendedoresAPI.historico(id); setHistorico(res.data); setShowHistorico(true); }
    catch { showToast('Erro ao carregar histórico', 'error'); }
  };

  const handleMarcarPago = async (vendaId) => {
    try { await vendedoresAPI.marcarComissaoPaga(vendaId); showToast('Comissão marcada como paga!', 'success'); const res = await vendedoresAPI.historico(historico.vendedor_id); setHistorico(res.data); }
    catch { showToast('Erro ao marcar comissão', 'error'); }
  };

  const totalAtivos = vendedores.filter(v => v.ativo && !v.bloqueado).length;
  const totalBloqueados = vendedores.filter(v => v.bloqueado).length;

  return (
    <div className="space-y-6">
      <ToastContainer toasts={toasts} removeToast={removeToast} />
      <ConfirmDialog isOpen={confirmDelete.isOpen} onClose={() => setConfirmDelete({ isOpen: false, id: null })}
        onConfirm={() => handleDelete(confirmDelete.id)} title="Excluir Vendedor" message="Deseja excluir este vendedor?" confirmText="Excluir" variant="danger" />

      {/* Header */}
      <div className="page-header">
        <div className="flex items-center gap-3">
          <Users size={24} className="text-solar-500" />
          <h2 className="page-title">Vendedores</h2>
        </div>
        <button onClick={abrirCriar} className="btn-accent flex items-center gap-2">
          <Plus size={16} /> Novo Vendedor
        </button>
      </div>

      {/* Resumo */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card"><div className="flex items-center gap-3"><Users className="text-blue-500" size={24} /><div><p className="text-sm text-surface-500">Total</p><p className="text-2xl font-semibold">{vendedores.length}</p></div></div></div>
        <div className="card"><div className="flex items-center gap-3"><UserCheck className="text-green-600" size={24} /><div><p className="text-sm text-surface-500">Ativos</p><p className="text-2xl font-semibold">{totalAtivos}</p></div></div></div>
        <div className="card"><div className="flex items-center gap-3"><Lock className="text-danger" size={24} /><div><p className="text-sm text-surface-500">Bloqueados</p><p className="text-2xl font-semibold">{totalBloqueados}</p></div></div></div>
      </div>

      {/* Tabela */}
      <div className="card p-0 overflow-hidden">
        <div className="table-wrapper">
          <table className="table">
            <thead><tr><th>Nome</th><th>Email</th><th>Tipo</th><th>Status</th><th className="text-right">Ações</th></tr></thead>
            <tbody>
              {vendedores.map((v) => (
                <tr key={v.id}>
                  <td className="font-medium text-surface-800">{v.nome}</td>
                  <td className="text-surface-500 text-sm">{v.email}</td>
                  <td><span className={`badge ${v.role === 'indicacao' ? 'badge-purple' : 'badge-blue'}`}>{v.role === 'indicacao' ? 'Indicação' : 'Vendedor'}</span></td>
                  <td>{v.bloqueado ? <span className="badge badge-yellow">Bloqueado</span> : <span className="badge badge-green">Ativo</span>}</td>
                  <td className="text-right">
                    <div className="flex gap-1 justify-end">
                      <button onClick={() => verResumo(v.id)} className="p-1.5 text-surface-400 hover:text-solar-500 rounded hover:bg-surface-100 transition-colors" title="Resumo"><TrendingUp size={16} /></button>
                      <button onClick={() => verHistorico(v.id)} className="p-1.5 text-surface-400 hover:text-info rounded hover:bg-surface-100 transition-colors" title="Histórico"><History size={16} /></button>
                      <button onClick={() => handleResetarSenha(v.id)} className="p-1.5 text-surface-400 hover:text-warning rounded hover:bg-surface-100 transition-colors" title="Resetar Senha"><Key size={16} /></button>
                      <button onClick={() => abrirEditar(v)} className="p-1.5 text-surface-400 hover:text-surface-700 rounded hover:bg-surface-100 transition-colors" title="Editar"><Edit size={16} /></button>
                      <button onClick={() => handleBloquear(v.id)} className={`p-1.5 text-surface-400 hover:text-surface-700 rounded hover:bg-surface-100 transition-colors`} title={v.bloqueado ? 'Desbloquear' : 'Bloquear'}>{v.bloqueado ? <Unlock size={16} /> : <Lock size={16} />}</button>
                      <button onClick={() => setConfirmDelete({ isOpen: true, id: v.id })} className="p-1.5 text-surface-400 hover:text-danger rounded hover:bg-danger-bg transition-colors" title="Excluir"><Trash size={16} /></button>
                    </div>
                  </td>
                </tr>
              ))}
              {vendedores.length === 0 && <tr><td colSpan={5} className="text-center py-12 text-surface-400 text-sm">Nenhum vendedor cadastrado</td></tr>}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal Criar/Editar */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content max-w-md" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-base font-semibold text-surface-900 mb-4">{editando ? 'Editar' : 'Novo'} Vendedor</h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div><label className="label">Nome Completo *</label><input type="text" className="input" value={formData.nome} onChange={(e) => setFormData({ ...formData, nome: e.target.value })} required /></div>
              {!editando && (<div><label className="label">Email *</label><input type="email" className="input" value={formData.email} onChange={(e) => setFormData({ ...formData, email: e.target.value })} required /></div>)}
              {!editando && (<div><label className="label">Senha *</label><input type="password" className="input" value={formData.password} minLength={6} onChange={(e) => setFormData({ ...formData, password: e.target.value })} required placeholder="Mínimo 6 caracteres" /></div>)}
              <div><label className="label">Tipo</label><select className="select" value={formData.role} onChange={(e) => setFormData({ ...formData, role: e.target.value })}><option value="vendedor">Vendedor</option><option value="indicacao">Indicação</option></select></div>
              <div className="flex gap-3 pt-4"><button type="button" onClick={() => setShowModal(false)} className="btn-outline flex-1">Cancelar</button><button type="submit" className="btn-accent flex-1">Salvar</button></div>
            </form>
          </div>
        </div>
      )}

      {/* Modal Histórico */}
      {showHistorico && historico && (
        <div className="modal-overlay" onClick={() => setShowHistorico(false)}>
          <div className="modal-content max-w-2xl max-h-[85vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-base font-semibold text-surface-900 mb-4">Histórico de Comissões — {historico.nome}</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
              <div className="bg-info-bg rounded-lg p-3 border border-info-border"><p className="text-xs text-surface-500">Volume de Vendas</p><p className="text-sm font-bold text-info">{formatarValor(historico.total_vendas)}</p></div>
              <div className="bg-warning-bg rounded-lg p-3 border border-warning-border"><p className="text-xs text-surface-500">Total Comissão</p><p className="text-sm font-bold text-warning">{formatarValor(historico.total_comissao)}</p></div>
              <div className="bg-success-bg rounded-lg p-3 border border-success-border"><p className="text-xs text-surface-500">Pago</p><p className="text-sm font-bold text-success">{formatarValor(historico.total_pago)}</p></div>
              <div className="bg-danger-bg rounded-lg p-3 border border-danger-border"><p className="text-xs text-surface-500">A Pagar</p><p className="text-sm font-bold text-danger">{formatarValor(historico.total_a_pagar)}</p></div>
            </div>
            {historico.vendas.length === 0 ? (<p className="text-surface-400 text-sm text-center py-8">Nenhuma venda registrada</p>) : (
              <div className="table-wrapper"><table className="table">
                <thead><tr><th>Data</th><th>Valor Venda</th><th>Comissão</th><th>Status</th><th></th></tr></thead>
                <tbody>
                  {historico.vendas.map((v) => (
                    <tr key={v.id}>
                      <td className="text-surface-400 text-xs">{new Date(v.created_at).toLocaleDateString('pt-BR')}</td>
                      <td className="font-medium text-surface-800">{formatarValor(v.valor_venda)}</td>
                      <td className="text-warning font-medium">{formatarValor(v.valor_comissao)}</td>
                      <td>{v.pago ? <span className="badge badge-green">Pago</span> : <span className="badge badge-orange">Pendente</span>}</td>
                      <td className="text-right">{!v.pago && (<button onClick={() => handleMarcarPago(v.id)} className="p-1 text-surface-400 hover:text-success transition-colors" title="Marcar como pago"><CheckCircle size={14} /></button>)}</td>
                    </tr>
                  ))}
                </tbody>
              </table></div>
            )}
            <button onClick={() => setShowHistorico(false)} className="btn-primary w-full mt-6">Fechar</button>
          </div>
        </div>
      )}

      {/* Modal Resumo */}
      {showResumo && resumo && (
        <div className="modal-overlay" onClick={() => setShowResumo(false)}>
          <div className="modal-content max-w-md" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-base font-semibold text-surface-900 mb-4">Resumo — {resumo.nome}</h3>
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-info-bg rounded-lg p-4 border border-info-border"><p className="text-xs text-surface-500">Clientes</p><p className="text-2xl font-bold text-info">{resumo.total_clientes}</p></div>
              <div className="bg-purple-50 rounded-lg p-4 border border-purple-200"><p className="text-xs text-surface-500">Contratos</p><p className="text-2xl font-bold text-purple-600">{resumo.total_contratos}</p></div>
              <div className="bg-success-bg rounded-lg p-4 border border-success-border"><p className="text-xs text-surface-500">Volume de Vendas</p><p className="text-lg font-bold text-success">{formatarValor(resumo.valor_total_vendas)}</p></div>
              <div className="bg-warning-bg rounded-lg p-4 border border-warning-border"><p className="text-xs text-surface-500">Comissão Estimada</p><p className="text-lg font-bold text-warning">{formatarValor(resumo.comissao_estimada)}</p></div>
            </div>
            <button onClick={() => setShowResumo(false)} className="btn-primary w-full mt-6">Fechar</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Vendedores;
