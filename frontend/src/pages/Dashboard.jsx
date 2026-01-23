import { useEffect, useState } from 'react';
import { Users, FileText, TrendingUp, Clock } from 'lucide-react';
import { clientesService } from '../services/clientesService';

const Dashboard = () => {
  const [stats, setStats] = useState({
    total_clientes: 0,
    novos_leads: 0,
    propostas_ativas: 0,
    ultimos_clientes: []
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await clientesService.getDashboardStats();
        setStats(response.data);
      } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchStats();
  }, []);

  const cards = [
    { title: 'Total de Clientes', value: stats.total_clientes, icon: Users, color: 'bg-blue-500' },
    { title: 'Novos Leads (30d)', value: stats.novos_leads, icon: TrendingUp, color: 'bg-green-500' },
    { title: 'Propostas Ativas', value: stats.propostas_ativas, icon: FileText, color: 'bg-yellow-500' },
  ];

  if (loading) {
    return <div className="text-center py-12">Carregando...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {cards.map((card) => (
          <div key={card.title} className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">{card.title}</p>
                <p className="text-3xl font-bold mt-2">{card.value}</p>
              </div>
              <div className={`${card.color} p-3 rounded-lg`}>
                <card.icon size={24} className="text-white" />
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Clock size={20} className="text-accent" />
          Últimos Clientes
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 font-semibold">Nome</th>
                <th className="text-left py-3 px-4 font-semibold">Telefone</th>
                <th className="text-left py-3 px-4 font-semibold">Status</th>
                <th className="text-left py-3 px-4 font-semibold">Data</th>
              </tr>
            </thead>
            <tbody>
              {stats.ultimos_clientes.map((cliente) => (
                <tr key={cliente.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4 font-medium">{cliente.nome}</td>
                  <td className="py-3 px-4">{cliente.telefone || '-'}</td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      cliente.status === 'orcamento' ? 'bg-blue-100 text-blue-800' :
                      cliente.status === 'proposta' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {cliente.status}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-gray-500">
                    {new Date(cliente.created_at).toLocaleDateString('pt-BR')}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          
          {stats.ultimos_clientes.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              Nenhum cliente cadastrado
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
