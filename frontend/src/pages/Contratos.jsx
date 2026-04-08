import { useState, useEffect } from 'react';
import { FileSignature, Download } from 'lucide-react';
import { contratosAPI } from '../services/api';
import { useToast, ToastContainer } from '../components/Toast';

const STATUS_LABELS = {
  rascunho: { label: 'Rascunho', cls: 'bg-gray-100 text-gray-700' },
  assinado: { label: 'Assinado', cls: 'bg-blue-100 text-blue-700' },
  em_execucao: { label: 'Em Execução', cls: 'bg-yellow-100 text-yellow-700' },
  concluido: { label: 'Concluído', cls: 'bg-green-100 text-green-700' },
};

const Contratos = () => {
  const [contratos, setContratos] = useState([]);
  const [total, setTotal] = useState(0);
  const [statusFiltro, setStatusFiltro] = useState('');
  const [loading, setLoading] = useState(false);
  const { toasts, showToast, removeToast } = useToast();

  useEffect(() => {
    carregarContratos();
  }, [statusFiltro]);

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
    const proximo = {
      rascunho: 'assinado',
      assinado: 'em_execucao',
      em_execucao: 'concluido',
    }[contrato.status];
    if (!proximo) return;
    try {
      await contratosAPI.atualizar(contrato.id, { status: proximo });
      showToast('Status atualizado!', 'success');
      carregarContratos();
    } catch {
      showToast('Erro ao atualizar status', 'error');
    }
  };

  const formatarValor = (v) =>
    Number(v).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

  const formatarData = (iso) => {
    if (!iso) return '-';
    return new Date(iso).toLocaleDateString('pt-BR');
  };

  return (
    <div className="space-y-6">
      <ToastContainer toasts={toasts} removeToast={removeToast} />

      {/* Resumo */}
      <div className="card bg-green-50 border-green-200">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-green-700">Total de Contratos</p>
            <p className="text-4xl font-bold text-green-800">{total}</p>
          </div>
          <FileSignature size={48} className="text-green-600" />
        </div>
      </div>

      {/* Filtro de status */}
      <div className="card">
        <div className="flex gap-2 flex-wrap">
          {['', 'rascunho', 'assinado', 'em_execucao', 'concluido'].map((s) => (
            <button
              key={s}
              onClick={() => setStatusFiltro(s)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                statusFiltro === s
                  ? 'bg-primary text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {s === '' ? 'Todos' : STATUS_LABELS[s]?.label}
            </button>
          ))}
        </div>
      </div>

      {/* Tabela */}
      <div className="card overflow-x-auto">
        {loading ? (
          <p className="text-center py-8 text-gray-400">Carregando...</p>
        ) : (
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 font-semibold">Número</th>
                <th className="text-left py-3 px-4 font-semibold">Cliente</th>
                <th className="text-left py-3 px-4 font-semibold">Empresa</th>
                <th className="text-left py-3 px-4 font-semibold">Valor Total</th>
                <th className="text-left py-3 px-4 font-semibold">Status</th>
                <th className="text-left py-3 px-4 font-semibold">Criado em</th>
                <th className="text-right py-3 px-4 font-semibold">Ações</th>
              </tr>
            </thead>
            <tbody>
              {contratos.map((c) => {
                const statusInfo = STATUS_LABELS[c.status] || { label: c.status, cls: 'bg-gray-100' };
                return (
                  <tr key={c.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3 px-4 font-medium">{c.numero}</td>
                    <td className="py-3 px-4">
                      <p>{c.cliente_nome}</p>
                      <p className="text-xs text-gray-500">{c.cliente_cidade}/{c.cliente_estado}</p>
                    </td>
                    <td className="py-3 px-4 text-sm text-gray-600">{c.empresa_razao_social}</td>
                    <td className="py-3 px-4 font-bold text-green-600">{formatarValor(c.valor_total)}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusInfo.cls}`}>
                        {statusInfo.label}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-sm">{formatarData(c.created_at)}</td>
                    <td className="py-3 px-4 text-right">
                      <div className="flex gap-2 justify-end">
                        {c.status !== 'concluido' && (
                          <button
                            onClick={() => avancarStatus(c)}
                            className="btn-outline text-sm py-1 px-3"
                          >
                            Avançar
                          </button>
                        )}
                        <button
                          onClick={() => gerarPdf(c.id, c.numero)}
                          className="btn-primary text-sm py-1 px-3 flex items-center gap-1"
                        >
                          <Download size={14} />
                          PDF
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
              {contratos.length === 0 && (
                <tr>
                  <td colSpan={7} className="text-center py-12 text-gray-400">
                    <FileSignature size={40} className="mx-auto mb-2 opacity-40" />
                    Nenhum contrato encontrado
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default Contratos;
