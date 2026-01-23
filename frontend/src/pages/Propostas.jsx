import { useState, useEffect } from 'react';
import { CheckCircle, Clock, XCircle } from 'lucide-react';
import { propostasAPI } from '../services/api';

const Propostas = () => {
  const [propostas, setPropostas] = useState([]);

  useEffect(() => {
    carregarPropostas();
  }, []);

  const carregarPropostas = async () => {
    try {
      const response = await propostasAPI.listar();
      setPropostas(response.data);
    } catch (error) {
      console.error('Erro:', error);
    }
  };

  const aceitarProposta = async (id) => {
    try {
      await propostasAPI.aceitar(id);
      carregarPropostas();
    } catch (error) {
      console.error('Erro:', error);
    }
  };

  const getStatusIcon = (status) => {
    switch(status) {
      case 'aceita': return <CheckCircle className="text-green-500" size={20} />;
      case 'recusada': return <XCircle className="text-red-500" size={20} />;
      default: return <Clock className="text-yellow-500" size={20} />;
    }
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card bg-yellow-50 border-yellow-200">
          <p className="text-sm text-yellow-700">Pendentes</p>
          <p className="text-3xl font-bold text-yellow-800">
            {propostas.filter(p => p.status === 'pendente').length}
          </p>
        </div>
        <div className="card bg-green-50 border-green-200">
          <p className="text-sm text-green-700">Aceitas</p>
          <p className="text-3xl font-bold text-green-800">
            {propostas.filter(p => p.status === 'aceita').length}
          </p>
        </div>
        <div className="card bg-red-50 border-red-200">
          <p className="text-sm text-red-700">Recusadas</p>
          <p className="text-3xl font-bold text-red-800">
            {propostas.filter(p => p.status === 'recusada').length}
          </p>
        </div>
      </div>

      <div className="card">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="text-left py-3 px-4 font-semibold">Número</th>
              <th className="text-left py-3 px-4 font-semibold">Cliente</th>
              <th className="text-left py-3 px-4 font-semibold">Status</th>
              <th className="text-left py-3 px-4 font-semibold">Data Criação</th>
              <th className="text-left py-3 px-4 font-semibold">Dias desde aceite</th>
              <th className="text-right py-3 px-4 font-semibold">Ações</th>
            </tr>
          </thead>
          <tbody>
            {propostas.map((prop) => (
              <tr key={prop.id} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="py-3 px-4 font-medium">{prop.numero}</td>
                <td className="py-3 px-4">{prop.cliente_nome}</td>
                <td className="py-3 px-4">
                  <div className="flex items-center gap-2">
                    {getStatusIcon(prop.status)}
                    <span className="capitalize">{prop.status}</span>
                  </div>
                </td>
                <td className="py-3 px-4">{new Date(prop.data_criacao).toLocaleDateString('pt-BR')}</td>
                <td className="py-3 px-4">{prop.dias_desde_aceite || '-'}</td>
                <td className="py-3 px-4 text-right">
                  {prop.status === 'pendente' && (
                    <button 
                      onClick={() => aceitarProposta(prop.id)}
                      className="btn-accent text-sm py-1 px-4"
                    >
                      Aceitar
                    </button>
                  )}
                  {prop.status === 'aceita' && !prop.convertido_contrato && (
                    <button className="btn-primary text-sm py-1 px-4">
                      Gerar Contrato
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Propostas;
