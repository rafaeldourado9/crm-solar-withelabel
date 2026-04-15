import { useEffect, useState } from 'react';
import { Users, FileText, TrendingUp, DollarSign, Clock, Award, AlertCircle } from 'lucide-react';
import { dashboardAPI } from '../services/api';
import { useToast, ToastContainer } from '../components/Toast';

const StatCard = ({ title, value, icon: Icon, accent, sub }) => (
  <div className="card card-hover">
    <div className="flex items-start justify-between">
      <div className="space-y-2">
        <p className="text-sm font-medium text-surface-500">{title}</p>
        <p className="text-2xl font-semibold text-surface-900 tracking-tight">{value}</p>
        {sub && <p className="text-xs text-surface-400">{sub}</p>}
      </div>
      <div className={`p-2.5 rounded-lg ${accent}`}>
        <Icon size={18} className="text-white" />
      </div>
    </div>
  </div>
);

const formatarValor = (v) =>
  Number(v).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

const STATUS_MAP = {
  orcamento: { label: 'Orçamento', cls: 'badge-blue' },
  proposta: { label: 'Proposta', cls: 'badge-yellow' },
  contrato: { label: 'Contrato', cls: 'badge-green' },
};

const Dashboard = () => {
  const { toasts, showToast, removeToast } = useToast();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const carregar = async () => {
      try {
        const res = await dashboardAPI.resumo();
        setData(res.data);
      } catch {
        showToast('Erro ao carregar dashboard', 'error');
      } finally {
        setLoading(false);
      }
    };
    carregar();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-24 text-surface-400">
        <div className="text-center">
          <div className="animate-spin w-6 h-6 border-2 border-surface-300 border-t-solar-500 rounded-full mx-auto mb-3" />
          <p className="text-sm">Carregando dashboard...</p>
        </div>
      </div>
    );
  }

  if (!data) return null;

  const cards = [
    { title: 'Total de Clientes', value: data.total_clientes, icon: Users, accent: 'bg-blue-500', sub: '' },
    { title: 'Novos Leads (30d)', value: data.leads_30d, icon: TrendingUp, accent: 'bg-emerald-500', sub: 'últimos 30 dias' },
    { title: 'Propostas Ativas', value: data.propostas_ativas, icon: FileText, accent: 'bg-amber-500', sub: 'aguardando resposta' },
    { title: 'Contratos no Mês', value: data.contratos_mes, icon: Award, accent: 'bg-violet-500' },
    { title: 'Faturamento Mensal', value: formatarValor(data.faturamento_mensal), icon: DollarSign, accent: 'bg-green-600' },
    { title: 'Comissões Pendentes', value: formatarValor(data.comissoes_pendentes), icon: AlertCircle, accent: 'bg-orange-500' },
  ];

  return (
    <div className="space-y-6">
      <ToastContainer toasts={toasts} removeToast={removeToast} />

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {cards.map((c) => <StatCard key={c.title} {...c} />)}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Vendedores */}
        <div className="card">
          <h3 className="text-sm font-semibold text-surface-900 mb-4 flex items-center gap-2">
            <Award size={16} className="text-solar-500" />
            Top Vendedores
          </h3>
          {data.top_vendedores.length === 0 ? (
            <p className="text-surface-400 text-sm text-center py-8">Nenhum contrato fechado ainda</p>
          ) : (
            <div className="space-y-1">
              {data.top_vendedores.map((v, i) => (
                <div key={v.vendedor_id} className="flex items-center justify-between py-2.5 group">
                  <div className="flex items-center gap-3">
                    <span className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold text-white
                      ${i === 0 ? 'bg-yellow-400' : i === 1 ? 'bg-surface-400' : 'bg-orange-400'}`}>
                      {i + 1}
                    </span>
                    <div>
                      <p className="font-medium text-sm text-surface-800">{v.nome}</p>
                      <p className="text-xs text-surface-400">{v.total_contratos} contrato{v.total_contratos !== 1 ? 's' : ''}</p>
                    </div>
                  </div>
                  <p className="font-semibold text-sm text-surface-900">{formatarValor(v.valor_total)}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Últimos Clientes */}
        <div className="card">
          <h3 className="text-sm font-semibold text-surface-900 mb-4 flex items-center gap-2">
            <Clock size={16} className="text-solar-500" />
            Últimos Clientes
          </h3>
          {data.ultimos_clientes.length === 0 ? (
            <p className="text-surface-400 text-sm text-center py-8">Nenhum cliente cadastrado</p>
          ) : (
            <div className="table-wrapper">
              <table className="table">
                <thead>
                  <tr>
                    <th>Nome</th>
                    <th>Status</th>
                    <th>Data</th>
                  </tr>
                </thead>
                <tbody>
                  {data.ultimos_clientes.map((c) => {
                    const statusInfo = STATUS_MAP[c.status] || { label: c.status, cls: 'badge-gray' };
                    return (
                      <tr key={c.id}>
                        <td className="font-medium text-surface-800">{c.nome}</td>
                        <td>
                          <span className={`badge ${statusInfo.cls}`}>{statusInfo.label}</span>
                        </td>
                        <td className="text-surface-400">
                          {new Date(c.created_at).toLocaleDateString('pt-BR')}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
