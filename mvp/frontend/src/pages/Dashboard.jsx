import { useEffect, useState } from 'react';
import { Users, FileText, TrendingUp, DollarSign, Clock, Award, AlertCircle } from 'lucide-react';
import { dashboardAPI } from '../services/api';
import { useToast, ToastContainer } from '../components/Toast';

const StatCard = ({ title, value, icon: Icon, color, sub }) => (
  <div className="card">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-gray-500 text-sm">{title}</p>
        <p className="text-3xl font-bold mt-1">{value}</p>
        {sub && <p className="text-xs text-gray-400 mt-1">{sub}</p>}
      </div>
      <div className={`${color} p-3 rounded-lg`}>
        <Icon size={24} className="text-white" />
      </div>
    </div>
  </div>
);

const formatarValor = (v) =>
  Number(v).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

const STATUS_CLS = {
  orcamento: 'bg-blue-100 text-blue-800',
  proposta: 'bg-yellow-100 text-yellow-800',
  contrato: 'bg-green-100 text-green-800',
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
      <div className="flex items-center justify-center py-20 text-gray-400">
        <div className="text-center">
          <div className="animate-spin w-8 h-8 border-4 border-primary border-t-transparent rounded-full mx-auto mb-3" />
          Carregando dashboard...
        </div>
      </div>
    );
  }

  if (!data) return null;

  const cards = [
    { title: 'Total de Clientes', value: data.total_clientes, icon: Users, color: 'bg-blue-500' },
    { title: 'Novos Leads (30d)', value: data.leads_30d, icon: TrendingUp, color: 'bg-green-500', sub: 'últimos 30 dias' },
    { title: 'Propostas Ativas', value: data.propostas_ativas, icon: FileText, color: 'bg-yellow-500', sub: 'aguardando resposta' },
    { title: 'Contratos no Mês', value: data.contratos_mes, icon: Award, color: 'bg-purple-500' },
    { title: 'Faturamento Mensal', value: formatarValor(data.faturamento_mensal), icon: DollarSign, color: 'bg-emerald-500' },
    { title: 'Comissões Pendentes', value: formatarValor(data.comissoes_pendentes), icon: AlertCircle, color: 'bg-orange-500' },
  ];

  return (
    <div className="space-y-6">
      <ToastContainer toasts={toasts} removeToast={removeToast} />

      {/* Cards de KPI */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {cards.map((c) => <StatCard key={c.title} {...c} />)}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Vendedores */}
        <div className="card">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Award size={20} className="text-accent" />
            Top Vendedores
          </h3>
          {data.top_vendedores.length === 0 ? (
            <p className="text-gray-400 text-sm text-center py-6">Nenhum contrato fechado ainda</p>
          ) : (
            <div className="space-y-3">
              {data.top_vendedores.map((v, i) => (
                <div key={v.vendedor_id} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0">
                  <div className="flex items-center gap-3">
                    <span className={`w-7 h-7 rounded-full flex items-center justify-center text-sm font-bold text-white ${
                      i === 0 ? 'bg-yellow-500' : i === 1 ? 'bg-gray-400' : 'bg-orange-400'
                    }`}>
                      {i + 1}
                    </span>
                    <div>
                      <p className="font-medium text-sm">{v.nome}</p>
                      <p className="text-xs text-gray-500">{v.total_contratos} contrato{v.total_contratos !== 1 ? 's' : ''}</p>
                    </div>
                  </div>
                  <p className="font-semibold text-green-600 text-sm">{formatarValor(v.valor_total)}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Últimos Clientes */}
        <div className="card">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Clock size={20} className="text-accent" />
            Últimos Clientes
          </h3>
          {data.ultimos_clientes.length === 0 ? (
            <p className="text-gray-400 text-sm text-center py-6">Nenhum cliente cadastrado</p>
          ) : (
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200 text-left">
                  <th className="py-2 text-sm font-semibold">Nome</th>
                  <th className="py-2 text-sm font-semibold">Status</th>
                  <th className="py-2 text-sm font-semibold">Data</th>
                </tr>
              </thead>
              <tbody>
                {data.ultimos_clientes.map((c) => (
                  <tr key={c.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-2 text-sm font-medium">{c.nome}</td>
                    <td className="py-2">
                      <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${STATUS_CLS[c.status] || 'bg-gray-100 text-gray-600'}`}>
                        {c.status}
                      </span>
                    </td>
                    <td className="py-2 text-xs text-gray-400">
                      {new Date(c.created_at).toLocaleDateString('pt-BR')}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
