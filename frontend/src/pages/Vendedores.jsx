import { useState, useEffect } from 'react';
import { DollarSign, TrendingUp, Plus } from 'lucide-react';
import { vendedoresAPI } from '../services/api';

const Vendedores = () => {
  const [vendedores, setVendedores] = useState([]);

  useEffect(() => {
    carregarVendedores();
  }, []);

  const carregarVendedores = async () => {
    try {
      const response = await vendedoresAPI.listar();
      setVendedores(response.data);
    } catch (error) {
      console.error('Erro:', error);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold text-gray-600">Total de Vendedores</h3>
          <p className="text-3xl font-bold">{vendedores.length}</p>
        </div>
        
        <button className="btn-accent flex items-center gap-2">
          <Plus size={20} />
          Novo Vendedor
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {vendedores.map((vendedor) => (
          <div key={vendedor.id} className="card hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <h4 className="font-semibold text-lg">{vendedor.nome}</h4>
                <p className="text-sm text-gray-500">{vendedor.email}</p>
                <p className="text-sm text-gray-500">{vendedor.telefone}</p>
              </div>
              <span className={`badge ${vendedor.tipo === 'vendedor' ? 'bg-blue-100 text-blue-800' : 'bg-purple-100 text-purple-800'}`}>
                {vendedor.tipo}
              </span>
            </div>
            
            <div className="space-y-2 mb-4">
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-2">
                  <DollarSign size={16} className="text-green-600" />
                  <span className="text-sm text-gray-600">Comissão</span>
                </div>
                <span className="font-bold text-green-600">{vendedor.comissao_percentual}%</span>
              </div>
              
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-2">
                  <TrendingUp size={16} className="text-blue-600" />
                  <span className="text-sm text-gray-600">Total Vendas</span>
                </div>
                <span className="font-bold text-blue-600">{vendedor.total_vendas || 0}</span>
              </div>
            </div>
            
            <button className="btn-outline w-full text-sm py-2">
              Ver Histórico
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Vendedores;
