import { useState, useEffect } from 'react';
import { FileSignature, Download } from 'lucide-react';
import { contratosAPI } from '../services/api';
import { useToast, ToastContainer } from '../components/Toast';

const STATUS_MAP = {
  rascunho: { label: 'Rascunho', cls: 'badge-gray' },
  assinado: { label: 'Assinado', cls: 'badge-blue' },
  em_execucao: { label: 'Em Execução', cls: 'badge-yellow' },
  concluido: { label: 'Concluído', cls: 'badge-green' },
};

const Contratos = () => {
  const [contratos, setContratos] = useState([]);
  const [total, setTotal] = useState(0);
  const [statusFiltro, setStatusFiltro] = useState('');
  const [loading, setLoading] = useState(false);
  const { toasts, showToast, removeToast } = useToast();

  useEffect(() => { carregarContratos(); }, [statusFiltro]);

  const carregarContratos = async () => {
    setLoading(true);
    try {
      const params = {};
      if (statusFiltro) params.status_filtro = statusFiltro;
      const response = await contratosAPI.listar(params);
      const data = response.data;
      const items = Array.isArray(data) ? data : (data.items || []);
      setContratos(items);
      setTotal(data.total ?? items.length);
    } catch {
      showToast('Erro ao carregar contratos', 'error');
      setContratos([]);
    } finally {
      setLoading(false);
    }
  };

  const gerarPdf = async (id, numero) => {
    try {
      showToast('Gerando PDF...', 'info');
      const response = await contratosAPI.gerarPdf(id);
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `Contrato_${numero}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      showToast('PDF gerado!', 'success');
    } catch {
      showToast('Erro ao gerar PDF', 'error');
    }
  };

  const avancarStatus = async (contrato) => {
    const proximo = { rascunho: 'assinado', assinado: 'em_execucao', em_execucao: 'concluido' }[contrato.status];
    if (!proximo) return;
    try {
      await contratosAPI.atualizar(contrato.id, { status: proximo });
      showToast('Status atualizado!', 'success');
      carregarContratos();
    } catch {
      showToast('Erro ao atualizar status', 'error');
    }
  };

  const formatarValor = (v) => Number(v).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
  const formatarData = (iso) => { if (!iso) return '-'; return new Date(iso).toLocaleDateString('pt-BR'); };

  return (
    <div className="space-y-6">
      <ToastContainer toasts={toasts} removeToast={removeToast} />

      {/* Resumo */}
      <div className="card bg-success-bg border-success-border">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-green-700">Total de Contratos</p>
            <p className="text-4xl font-bold text-green-800">{total}</p>
          </div>
          <FileSignature size={48} className="text-green-600" />
        </div>
      </div>

      {/* Filtros */}
      <div className="flex gap-2 flex-wrap">
        {['', 'rascunho', 'assinado', 'em_execucao', 'concluido'].map((s) => (
          <button key={s} onClick={() => setStatusFiltro(s)}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              statusFiltro === s ? 'bg-surface-900 text-white' : 'bg-white text-surface-600 border border-surface-200 hover:bg-surface-50'
            }`}>
            {s === '' ? 'Todos' : STATUS_MAP[s]?.label}
          </button>
        ))}
      </div>

      {/* Tabela */}
      <div className="card p-0 overflow-hidden">
        {loading ? (
          <p className="text-center py-8 text-surface-400 text-sm">Carregando...</p>
        ) : (
          <div className="table-wrapper">
            <table className="table">
              <thead>
                <tr>
                  <th>Número</th>
                  <th>Cliente</th>
                  <th>Empresa</th>
                  <th>Valor Total</th>
                  <th>Status</th>
                  <th>Criado em</th>
                  <th className="text-right">Ações</th>
                </tr>
              </thead>
              <tbody>
                {contratos.map((c) => {
                  const statusInfo = STATUS_MAP[c.status] || { label: c.status, cls: 'badge-gray' };
                  return (
                    <tr key={c.id}>
                      <td className="font-medium text-surface-800">{c.numero}</td>
                      <td>
                        <p className="text-surface-800">{c.cliente_nome}</p>
                        <p className="text-xs text-surface-400">{c.cliente_cidade}/{c.cliente_estado}</p>
                      </td>
                      <td className="text-surface-500 text-sm">{c.empresa_razao_social}</td>
                      <td className="font-semibold text-surface-900">{formatarValor(c.valor_total)}</td>
                      <td><span className={`badge ${statusInfo.cls}`}>{statusInfo.label}</span></td>
                      <td className="text-surface-400">{formatarData(c.created_at)}</td>
                      <td className="text-right">
                        <div className="flex gap-1.5 justify-end">
                          {c.status !== 'concluido' && (
                            <button onClick={() => avancarStatus(c)} className="btn-outline text-xs py-1 px-2.5">Avançar</button>
                          )}
                          <button onClick={() => gerarPdf(c.id, c.numero)} className="btn-primary text-xs py-1 px-2.5 flex items-center gap-1">
                            <Download size={12} /> PDF
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
                {contratos.length === 0 && (
                  <tr><td colSpan={7} className="text-center py-12 text-surface-400 text-sm">Nenhum contrato encontrado</td></tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default Contratos;
