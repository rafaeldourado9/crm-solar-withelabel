import { useState, useEffect } from 'react';
import { FileSignature, Download, Search, Filter, X } from 'lucide-react';
import { contratosAPI } from '../services/api';
import { useToast, ToastContainer } from '../components/Toast';

const Contratos = () => {
  const [contratos, setContratos] = useState([]);
  const [totalContratos, setTotalContratos] = useState(0);
  const [showFiltros, setShowFiltros] = useState(false);
  const [filtros, setFiltros] = useState({
    search: '',
    data_inicio: '',
    data_fim: '',
    forma_pagamento: ''
  });
  const { toasts, showToast, removeToast } = useToast();

  useEffect(() => {
    carregarContratos();
  }, []);

  const carregarContratos = async () => {
    try {
      const params = {};
      if (filtros.search) params.search = filtros.search;
      if (filtros.data_inicio) params.data_inicio = filtros.data_inicio;
      if (filtros.data_fim) params.data_fim = filtros.data_fim;
      if (filtros.forma_pagamento) params.forma_pagamento = filtros.forma_pagamento;
      
      const response = await contratosAPI.listar(params);
      const data = response.data.results || response.data;
      setContratos(Array.isArray(data) ? data : []);
      setTotalContratos(response.data.count || data.length);
    } catch (error) {
      console.error('Erro:', error);
      showToast('Erro ao carregar contratos', 'error');
      setContratos([]);
    }
  };

  const limparFiltros = () => {
    setFiltros({ search: '', data_inicio: '', data_fim: '', forma_pagamento: '' });
    setTimeout(carregarContratos, 100);
  };

  const gerarPDF = async (id, numero) => {
    try {
      showToast('Gerando PDF do contrato...', 'info');
      const response = await contratosAPI.gerarPDF(id);
      
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `Contrato_${numero}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      showToast('PDF gerado com sucesso!', 'success');
      carregarContratos();
    } catch (error) {
      if (error.response?.data?.campos_faltantes) {
        showToast(`Dados incompletos: ${error.response.data.campos_faltantes.join(', ')}`, 'error');
      } else {
        showToast('Erro ao gerar PDF', 'error');
      }
    }
  };

  return (
    <div className="space-y-6">
      <ToastContainer toasts={toasts} removeToast={removeToast} />
      
      <div className="card bg-green-50 border-green-200">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-green-700">Total de Contratos</p>
            <p className="text-4xl font-bold text-green-800">{totalContratos}</p>
          </div>
          <FileSignature size={48} className="text-green-600" />
        </div>
      </div>

      <div className="card">
        <div className="flex gap-3 mb-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="text"
              placeholder="Buscar por número ou cliente..."
              className="input pl-10 w-full"
              value={filtros.search}
              onChange={(e) => setFiltros({...filtros, search: e.target.value})}
              onKeyPress={(e) => e.key === 'Enter' && carregarContratos()}
            />
          </div>
          <button
            onClick={() => setShowFiltros(!showFiltros)}
            className="btn-outline flex items-center gap-2"
          >
            <Filter size={20} />
            Filtros
          </button>
          <button onClick={carregarContratos} className="btn-primary">
            Buscar
          </button>
        </div>

        {showFiltros && (
          <div className="bg-gray-50 p-4 rounded-lg mb-4 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Data Início</label>
              <input
                type="date"
                className="input"
                value={filtros.data_inicio}
                onChange={(e) => setFiltros({...filtros, data_inicio: e.target.value})}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Data Fim</label>
              <input
                type="date"
                className="input"
                value={filtros.data_fim}
                onChange={(e) => setFiltros({...filtros, data_fim: e.target.value})}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Forma Pagamento</label>
              <select
                className="input"
                value={filtros.forma_pagamento}
                onChange={(e) => setFiltros({...filtros, forma_pagamento: e.target.value})}
              >
                <option value="">Todas</option>
                <option value="vista">À Vista</option>
                <option value="cartao">Cartão de Crédito</option>
                <option value="financiamento">Financiamento Bancário</option>
              </select>
            </div>
            <div className="md:col-span-3 flex justify-end">
              <button onClick={limparFiltros} className="btn-outline flex items-center gap-2">
                <X size={16} />
                Limpar Filtros
              </button>
            </div>
          </div>
        )}
      </div>

      <div className="card">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="text-left py-3 px-4 font-semibold">Número</th>
              <th className="text-left py-3 px-4 font-semibold">Cliente</th>
              <th className="text-left py-3 px-4 font-semibold">Valor Total</th>
              <th className="text-left py-3 px-4 font-semibold">Forma Pagamento</th>
              <th className="text-left py-3 px-4 font-semibold">Data Assinatura</th>
              <th className="text-right py-3 px-4 font-semibold">Ações</th>
            </tr>
          </thead>
          <tbody>
            {contratos.map((contrato) => (
              <tr key={contrato.id} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="py-3 px-4 font-medium">{contrato.numero}</td>
                <td className="py-3 px-4">{contrato.cliente_nome}</td>
                <td className="py-3 px-4 font-bold text-green-600">R$ {contrato.valor_total}</td>
                <td className="py-3 px-4 capitalize">{contrato.forma_pagamento}</td>
                <td className="py-3 px-4">{new Date(contrato.data_assinatura).toLocaleDateString('pt-BR')}</td>
                <td className="py-3 px-4 text-right">
                  <button 
                    onClick={() => gerarPDF(contrato.id, contrato.numero)}
                    className="btn-primary text-sm py-1 px-4 flex items-center gap-2 ml-auto"
                  >
                    <Download size={16} />
                    {contrato.pdf_contrato ? 'Baixar PDF' : 'Gerar PDF'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        
        {contratos.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            <FileSignature size={48} className="mx-auto mb-3 opacity-50" />
            <p>Nenhum contrato encontrado</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Contratos;
