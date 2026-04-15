import { useState, useEffect } from 'react';
import { Search, Plus, Edit, Trash } from 'lucide-react';
import { clientesService } from '../services/clientesService';
import { useToast, ToastContainer } from '../components/Toast';
import { ConfirmDialog } from '../components/ConfirmDialog';
import api from '../services/api';

const STATUS_MAP = {
  orcamento: { label: 'Orçamento', cls: 'badge-blue' },
  proposta: { label: 'Proposta', cls: 'badge-yellow' },
  contrato: { label: 'Contrato', cls: 'badge-green' },
};

const EMPTY_FORM = {
  nome: '', cpf_cnpj: '', telefone: '', email: '', cep: '',
  endereco: '', bairro: '', cidade: '', estado: '', vendedor: '', status: 'orcamento'
};

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
  const [formData, setFormData] = useState(EMPTY_FORM);
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
      if (numeros.length <= 3) return numeros;
      if (numeros.length <= 6) return `${numeros.slice(0, 3)}.${numeros.slice(3)}`;
      if (numeros.length <= 9) return `${numeros.slice(0, 3)}.${numeros.slice(3, 6)}.${numeros.slice(6)}`;
      return `${numeros.slice(0, 3)}.${numeros.slice(3, 6)}.${numeros.slice(6, 9)}-${numeros.slice(9, 11)}`;
    } else {
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
        setFormData({ ...formData, cidade: data.localidade, estado: data.uf, endereco: data.logradouro, bairro: data.bairro });
        showToast('CEP encontrado!', 'success');
      } else {
        showToast('CEP não encontrado', 'error');
      }
    } catch {
      showToast('Erro ao buscar CEP', 'error');
    } finally {
      setBuscandoCep(false);
    }
  };

  useEffect(() => { carregarClientes(1); carregarVendedores(); }, [filtro, busca]);

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
      const dadosParaSalvar = { ...formData, cep: formData.cep.replace(/\D/g, '') };
      if (editingId) {
        await clientesService.update(editingId, dadosParaSalvar);
        showToast('Cliente atualizado com sucesso', 'success');
      } else {
        await clientesService.create(dadosParaSalvar);
        showToast('Cliente criado com sucesso', 'success');
      }
      setShowModal(false);
      setEditingId(null);
      setFormData(EMPTY_FORM);
      carregarClientes(paginaAtual);
    } catch {
      showToast('Erro ao salvar cliente', 'error');
    }
  };

  const handleEdit = (cliente) => {
    setFormData({ ...cliente, cep: formatarCEP(cliente.cep || ''), vendedor: cliente.vendedor || '', estado: cliente.estado || '' });
    setEditingId(cliente.id);
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    try {
      await clientesService.delete(id);
      showToast('Cliente excluído com sucesso', 'success');
      carregarClientes(paginaAtual);
    } catch {
      showToast('Erro ao excluir cliente', 'error');
    }
  };

  return (
    <div className="space-y-6">
      <ToastContainer toasts={toasts} removeToast={removeToast} />
      <ConfirmDialog
        isOpen={confirmDialog.isOpen}
        onClose={() => setConfirmDialog({ isOpen: false, clienteId: null })}
        onConfirm={() => { handleDelete(confirmDialog.clienteId); setConfirmDialog({ isOpen: false, clienteId: null }); }}
        title="Excluir Cliente"
        message="Deseja realmente excluir este cliente? Esta ação não pode ser desfeita."
        confirmText="Excluir"
        variant="danger"
      />

      {/* Page Header */}
      <div className="page-header">
        <div>
          <h2 className="page-title">Clientes</h2>
          <p className="page-subtitle">{totalClientes} clientes — página {paginaAtual} de {totalPaginas}</p>
        </div>
        <button onClick={() => { setEditingId(null); setFormData(EMPTY_FORM); setShowModal(true); }} className="btn-accent flex items-center gap-2">
          <Plus size={16} />
          Novo Cliente
        </button>
      </div>

      {/* Filtros + Busca */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-surface-400" size={16} />
          <input
            type="text"
            placeholder="Buscar por nome, vendedor, contato, cidade..."
            className="input pl-9"
            value={busca}
            onChange={(e) => setBusca(e.target.value)}
          />
        </div>
        <div className="flex gap-2">
          {['todos', 'orcamento', 'proposta', 'contrato'].map((f) => (
            <button
              key={f}
              onClick={() => setFiltro(f)}
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors
                ${filtro === f
                  ? 'bg-surface-900 text-white'
                  : 'bg-white text-surface-600 border border-surface-200 hover:bg-surface-50'
                }`}
            >
              {f === 'todos' ? 'Todos' : STATUS_MAP[f]?.label || f}
            </button>
          ))}
        </div>
      </div>

      {/* Tabela */}
      <div className="card p-0 overflow-hidden">
        <div className="table-wrapper">
          <table className="table">
            <thead>
              <tr>
                <th>Nome</th>
                <th>Vendedor</th>
                <th>Contato</th>
                <th>Cidade</th>
                <th>Status</th>
                <th className="text-right">Ações</th>
              </tr>
            </thead>
            <tbody>
              {clientes.map((cliente) => {
                const statusInfo = STATUS_MAP[cliente.status] || { label: cliente.status, cls: 'badge-gray' };
                return (
                  <tr key={cliente.id}>
                    <td className="font-medium text-surface-800">{cliente.nome}</td>
                    <td>
                      {cliente.vendedor_nome ? (
                        <span className="badge badge-purple">{cliente.vendedor_nome}</span>
                      ) : (
                        <span className="text-surface-400 text-xs">Sem vendedor</span>
                      )}
                    </td>
                    <td className="text-surface-500">{cliente.telefone || cliente.email || '-'}</td>
                    <td className="text-surface-500">{cliente.cidade}</td>
                    <td><span className={`badge ${statusInfo.cls}`}>{statusInfo.label}</span></td>
                    <td className="text-right">
                      <div className="flex gap-1 justify-end">
                        <button onClick={() => handleEdit(cliente)} className="p-1.5 text-surface-400 hover:text-surface-700 rounded hover:bg-surface-100 transition-colors" title="Editar">
                          <Edit size={16} />
                        </button>
                        <button onClick={() => setConfirmDialog({ isOpen: true, clienteId: cliente.id })} className="p-1.5 text-surface-400 hover:text-danger rounded hover:bg-danger-bg transition-colors" title="Excluir">
                          <Trash size={16} />
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {clientes.length === 0 && (
          <div className="text-center py-16 text-surface-400">
            <p className="text-sm">Nenhum cliente encontrado</p>
          </div>
        )}

        {/* Paginação */}
        {totalPaginas > 1 && (
          <div className="flex justify-center items-center gap-2 px-6 py-4 border-t border-surface-100">
            <button onClick={() => carregarClientes(paginaAtual - 1)} disabled={paginaAtual === 1} className="btn-outline px-3 py-1.5 text-xs disabled:opacity-40">
              ← Anterior
            </button>
            <div className="flex gap-1">
              {[...Array(Math.min(5, totalPaginas))].map((_, i) => {
                let pageNum;
                if (totalPaginas <= 5) pageNum = i + 1;
                else if (paginaAtual <= 3) pageNum = i + 1;
                else if (paginaAtual >= totalPaginas - 2) pageNum = totalPaginas - 4 + i;
                else pageNum = paginaAtual - 2 + i;
                return (
                  <button key={i} onClick={() => carregarClientes(pageNum)}
                    className={`w-8 h-8 rounded-md text-sm font-medium transition-colors
                      ${paginaAtual === pageNum ? 'bg-surface-900 text-white' : 'text-surface-600 hover:bg-surface-100'}`}>
                    {pageNum}
                  </button>
                );
              })}
            </div>
            <button onClick={() => carregarClientes(paginaAtual + 1)} disabled={paginaAtual === totalPaginas} className="btn-outline px-3 py-1.5 text-xs disabled:opacity-40">
              Próxima →
            </button>
          </div>
        )}
      </div>

      {/* Modal Form */}
      {showModal && (
        <div className="modal-overlay" onClick={() => { setShowModal(false); setEditingId(null); setFormData(EMPTY_FORM); }}>
          <div className="modal-content max-w-2xl max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-lg font-semibold text-surface-900 mb-6">{editingId ? 'Editar Cliente' : 'Novo Cliente'}</h3>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="col-span-2">
                  <label className="label">Nome</label>
                  <input type="text" className="input" value={formData.nome} onChange={(e) => setFormData({...formData, nome: e.target.value})} required />
                </div>
                <div>
                  <label className="label">CPF/CNPJ</label>
                  <input type="text" className="input" value={formData.cpf_cnpj} onChange={(e) => setFormData({...formData, cpf_cnpj: formatarCPFCNPJ(e.target.value)})} placeholder="000.000.000-00" maxLength="18" />
                </div>
                <div>
                  <label className="label">Telefone</label>
                  <input type="text" className="input" value={formData.telefone} onChange={(e) => setFormData({...formData, telefone: formatarTelefone(e.target.value)})} placeholder="(00) 00000-0000" maxLength="15" />
                </div>
                <div>
                  <label className="label">Email</label>
                  <input type="email" className="input" value={formData.email} onChange={(e) => setFormData({...formData, email: e.target.value.toLowerCase()})} placeholder="email@exemplo.com" />
                </div>
                <div>
                  <label className="label">CEP</label>
                  <input type="text" className="input" value={formData.cep} onChange={(e) => {
                    const cepFormatado = formatarCEP(e.target.value);
                    setFormData({...formData, cep: cepFormatado});
                    if (cepFormatado.replace(/\D/g, '').length === 8) buscarCep(cepFormatado.replace(/\D/g, ''));
                  }} placeholder="00000-000" maxLength="9" />
                  {buscandoCep && <span className="text-xs text-surface-400 mt-1">Buscando...</span>}
                </div>
                <div>
                  <label className="label">Endereço</label>
                  <input type="text" className="input" value={formData.endereco} onChange={(e) => setFormData({...formData, endereco: e.target.value})} />
                </div>
                <div>
                  <label className="label">Bairro</label>
                  <input type="text" className="input" value={formData.bairro} onChange={(e) => setFormData({...formData, bairro: e.target.value})} />
                </div>
                <div>
                  <label className="label">Cidade</label>
                  <input type="text" className="input" value={formData.cidade} onChange={(e) => setFormData({...formData, cidade: e.target.value})} required />
                </div>
                <div>
                  <label className="label">Estado</label>
                  <select className="select" value={formData.estado} onChange={(e) => setFormData({...formData, estado: e.target.value})} required>
                    <option value="">Selecione...</option>
                    {['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO'].map(uf => (
                      <option key={uf} value={uf}>{uf}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="label">Vendedor</label>
                  <select className="select" value={formData.vendedor} onChange={(e) => setFormData({...formData, vendedor: e.target.value})}>
                    <option value="">Selecione um vendedor</option>
                    {vendedores.map(v => (<option key={v.id} value={v.id}>{v.nome}</option>))}
                  </select>
                </div>
                <div>
                  <label className="label">Status</label>
                  <select className="select" value={formData.status} onChange={(e) => setFormData({...formData, status: e.target.value})}>
                    <option value="orcamento">Orçamento</option>
                    <option value="proposta">Proposta</option>
                    <option value="contrato">Contrato</option>
                  </select>
                </div>
              </div>

              <div className="flex gap-3 pt-4 border-t border-surface-100">
                <button type="button" onClick={() => { setShowModal(false); setEditingId(null); setFormData(EMPTY_FORM); }} className="btn-outline flex-1">
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
