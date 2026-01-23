import { useState, useEffect } from 'react';
import { Package, Plus } from 'lucide-react';
import { equipamentosAPI } from '../services/api';

const Equipamentos = () => {
  const [equipamentos, setEquipamentos] = useState([]);
  const [filtro, setFiltro] = useState('todos');

  useEffect(() => {
    carregarEquipamentos();
  }, [filtro]);

  const carregarEquipamentos = async () => {
    try {
      const params = filtro !== 'todos' ? { categoria: filtro } : {};
      const response = await equipamentosAPI.listar(params);
      setEquipamentos(response.data);
    } catch (error) {
      console.error('Erro:', error);
    }
  };

  const categorias = [
    { value: 'todos', label: 'Todos', color: 'bg-gray-500' },
    { value: 'kit', label: 'Kit', color: 'bg-blue-500' },
    { value: 'servicos', label: 'Serviços', color: 'bg-green-500' },
    { value: 'custos', label: 'Custos', color: 'bg-red-500' }
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div className="flex gap-2">
          {categorias.map((cat) => (
            <button
              key={cat.value}
              onClick={() => setFiltro(cat.value)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                filtro === cat.value
                  ? 'bg-accent text-primary'
                  : 'bg-white border border-gray-300 hover:bg-gray-50'
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>
        
        <button className="btn-accent flex items-center gap-2">
          <Plus size={20} />
          Novo Equipamento
        </button>
      </div>

      <div className="card">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="text-left py-3 px-4 font-semibold">Categoria</th>
              <th className="text-left py-3 px-4 font-semibold">Item</th>
              <th className="text-left py-3 px-4 font-semibold">Código</th>
              <th className="text-left py-3 px-4 font-semibold">Quantidade</th>
              <th className="text-left py-3 px-4 font-semibold">Custo Unit.</th>
              <th className="text-left py-3 px-4 font-semibold">Custo Total</th>
              <th className="text-right py-3 px-4 font-semibold">Ações</th>
            </tr>
          </thead>
          <tbody>
            {equipamentos.map((equip) => (
              <tr key={equip.id} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="py-3 px-4">
                  <span className={`badge ${
                    equip.categoria === 'kit' ? 'bg-blue-100 text-blue-800' :
                    equip.categoria === 'servicos' ? 'bg-green-100 text-green-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {equip.categoria}
                  </span>
                </td>
                <td className="py-3 px-4 font-medium">{equip.item}</td>
                <td className="py-3 px-4 text-gray-600">{equip.codigo}</td>
                <td className="py-3 px-4">{equip.quantidade}</td>
                <td className="py-3 px-4">R$ {equip.custo_unitario}</td>
                <td className="py-3 px-4 font-bold">R$ {equip.custo_total}</td>
                <td className="py-3 px-4 text-right">
                  <button className="text-accent hover:text-accent-dark font-medium">
                    Editar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Equipamentos;
