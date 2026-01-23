import { useState, useEffect } from 'react';
import { FileSignature, Download } from 'lucide-react';
import { contratosAPI } from '../services/api';

const Contratos = () => {
  const [contratos, setContratos] = useState([]);

  useEffect(() => {
    carregarContratos();
  }, []);

  const carregarContratos = async () => {
    try {
      const response = await contratosAPI.listar();
      setContratos(response.data);
    } catch (error) {
      console.error('Erro:', error);
    }
  };

  return (
    <div className="space-y-6">
      <div className="card bg-green-50 border-green-200">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-green-700">Total de Contratos</p>
            <p className="text-4xl font-bold text-green-800">{contratos.length}</p>
          </div>
          <FileSignature size={48} className="text-green-600" />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {contratos.map((contrato) => (
          <div key={contrato.id} className="card border-l-4 border-green-500">
            <div className="flex justify-between items-start mb-4">
              <div>
                <p className="text-sm text-gray-500">Contrato</p>
                <p className="text-xl font-bold">{contrato.numero}</p>
              </div>
              <span className="badge bg-green-100 text-green-800">Ativo</span>
            </div>
            
            <h4 className="font-semibold text-lg mb-3">{contrato.cliente_nome}</h4>
            
            <div className="space-y-2 text-sm mb-4">
              <div className="flex justify-between">
                <span className="text-gray-600">Valor Total:</span>
                <span className="font-bold text-green-600">R$ {contrato.valor_total}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Forma Pagamento:</span>
                <span className="font-medium capitalize">{contrato.forma_pagamento}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Data Assinatura:</span>
                <span>{new Date(contrato.data_assinatura).toLocaleDateString('pt-BR')}</span>
              </div>
            </div>
            
            <button className="btn-primary w-full text-sm py-2 flex items-center justify-center gap-2">
              <Download size={16} />
              Baixar PDF
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Contratos;
