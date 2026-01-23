import { useState, useEffect } from 'react';
import { Settings, Save } from 'lucide-react';
import api from '../services/api';

const PremissasConfig = () => {
  const [premissa, setPremissa] = useState(null);
  const [loading, setLoading] = useState(false);
  const [taxas, setTaxas] = useState({ '12': '', '18': '', '24': '' });

  useEffect(() => {
    carregarPremissa();
  }, []);

  const carregarPremissa = async () => {
    try {
      const response = await api.get('/premissas/ativa/');
      setPremissa(response.data);
      if (response.data.taxas_maquininha) {
        setTaxas(response.data.taxas_maquininha);
      }
    } catch (error) {
      console.error('Erro ao carregar premissas:', error);
      alert('Não foi possível carregar as configurações.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // 1. Preparar dados para evitar erro de validação (casas decimais)
      const dadosParaEnviar = {
        ...premissa,
        // Garante que a taxa é enviada como número ou 0
        taxas_maquininha: {
            '12': Number(taxas['12']) || 0,
            '18': Number(taxas['18']) || 0,
            '24': Number(taxas['24']) || 0
        },
        // Garante precisão correta para evitar erro 400 do Django
        perda_padrao: Number(premissa.perda_padrao).toFixed(2), 
        hsp_padrao: Number(premissa.hsp_padrao).toFixed(2),
        tarifa_energia_atual: Number(premissa.tarifa_energia_atual).toFixed(2),
        inflacao_energetica_anual: Number(premissa.inflacao_energetica_anual).toFixed(2),
        perda_eficiencia_anual: Number(premissa.perda_eficiencia_anual).toFixed(2),
        overload_inversor: Number(premissa.overload_inversor).toFixed(2),
        
        // Novos campos adicionados (Margens e Serviços)
        margem_lucro_percentual: Number(premissa.margem_lucro_percentual).toFixed(2),
        comissao_percentual: Number(premissa.comissao_percentual).toFixed(2),
        imposto_percentual: Number(premissa.imposto_percentual).toFixed(2),
        montagem_por_painel: Number(premissa.montagem_por_painel).toFixed(2),
        valor_projeto: Number(premissa.valor_projeto).toFixed(2),
        
        // Campos inteiros
        prazo_entrega_padrao: parseInt(premissa.prazo_entrega_padrao),
        garantia_instalacao_meses: parseInt(premissa.garantia_instalacao_meses),
      };

      await api.put(`/premissas/${premissa.id}/`, dadosParaEnviar);
      alert('Premissas atualizadas com sucesso!');
      
      carregarPremissa(); 

    } catch (error) {
      console.error('Erro detalhado:', error.response?.data);
      let msg = 'Erro ao atualizar.';
      if (error.response?.data) {
        const erros = Object.entries(error.response.data)
          .map(([campo, erro]) => `${campo}: ${erro}`)
          .join('\n');
        msg += `\n\nDetalhes:\n${erros}`;
      }
      alert(msg);
    } finally {
      setLoading(false);
    }
  };

  if (!premissa) return <div className="p-8 text-center">Carregando configurações...</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3 mb-6">
        <Settings size={32} className="text-accent" />
        <h2 className="text-2xl font-bold">Configurações Globais</h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        
        {/* PARÂMETROS TÉCNICOS */}
        <div className="card bg-base-100 shadow p-6 rounded-lg">
          <h3 className="font-semibold text-lg mb-4 border-b pb-2">Parâmetros Técnicos</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">HSP Padrão (h)</label>
              <input
                type="number"
                step="0.01"
                required
                className="input input-bordered w-full"
                value={premissa.hsp_padrao}
                onChange={(e) => setPremissa({...premissa, hsp_padrao: e.target.value})}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Perda Padrão (%)</label>
              <input
                type="number"
                step="0.01"
                required
                className="input input-bordered w-full"
                // Exibe em porcentagem (0.20 -> 20)
                value={premissa.perda_padrao ? (premissa.perda_padrao * 100).toFixed(2) : ''}
                // Salva em decimal (20 -> 0.20)
                onChange={(e) => setPremissa({...premissa, perda_padrao: e.target.value / 100})}
              />
              <span className="text-xs text-gray-500">Ex: 20 para 20%</span>
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Overload Inversor</label>
              <input
                type="number"
                step="0.01"
                required
                className="input input-bordered w-full"
                value={premissa.overload_inversor}
                onChange={(e) => setPremissa({...premissa, overload_inversor: e.target.value})}
              />
            </div>
          </div>
        </div>

        {/* MARGENS E SERVIÇOS (ADICIONADO) */}
        <div className="card bg-base-100 shadow p-6 rounded-lg">
          <h3 className="font-semibold text-lg mb-4 border-b pb-2">Margens e Serviços</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">Margem de Lucro (%)</label>
              <input
                type="number"
                step="0.01"
                className="input input-bordered w-full"
                value={premissa.margem_lucro_percentual}
                onChange={(e) => setPremissa({...premissa, margem_lucro_percentual: e.target.value})}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Comissão (%)</label>
              <input
                type="number"
                step="0.01"
                className="input input-bordered w-full"
                value={premissa.comissao_percentual}
                onChange={(e) => setPremissa({...premissa, comissao_percentual: e.target.value})}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Imposto (%)</label>
              <input
                type="number"
                step="0.01"
                className="input input-bordered w-full"
                value={premissa.imposto_percentual}
                onChange={(e) => setPremissa({...premissa, imposto_percentual: e.target.value})}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Montagem/Painel (R$)</label>
              <input
                type="number"
                step="0.01"
                className="input input-bordered w-full"
                value={premissa.montagem_por_painel}
                onChange={(e) => setPremissa({...premissa, montagem_por_painel: e.target.value})}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Valor Projeto (R$)</label>
              <input
                type="number"
                step="0.01"
                className="input input-bordered w-full"
                value={premissa.valor_projeto}
                onChange={(e) => setPremissa({...premissa, valor_projeto: e.target.value})}
              />
            </div>
          </div>
        </div>

        {/* PARÂMETROS FINANCEIROS */}
        <div className="card bg-base-100 shadow p-6 rounded-lg">
          <h3 className="font-semibold text-lg mb-4 border-b pb-2">Parâmetros Financeiros</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">Tarifa Energia (R$/kWh)</label>
              <input
                type="number"
                step="0.01"
                required
                className="input input-bordered w-full"
                value={premissa.tarifa_energia_atual}
                onChange={(e) => setPremissa({...premissa, tarifa_energia_atual: e.target.value})}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Inflação Energética (%/ano)</label>
              <input
                type="number"
                step="0.1"
                required
                className="input input-bordered w-full"
                value={premissa.inflacao_energetica_anual}
                onChange={(e) => setPremissa({...premissa, inflacao_energetica_anual: e.target.value})}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Perda Eficiência (%/ano)</label>
              <input
                type="number"
                step="0.1"
                required
                className="input input-bordered w-full"
                value={premissa.perda_eficiencia_anual}
                onChange={(e) => setPremissa({...premissa, perda_eficiencia_anual: e.target.value})}
              />
            </div>
          </div>
        </div>

        {/* PRAZOS E GARANTIAS (ADICIONADO) */}
        <div className="card bg-base-100 shadow p-6 rounded-lg">
          <h3 className="font-semibold text-lg mb-4 border-b pb-2">Prazos e Garantias</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">Prazo de Entrega (Dias)</label>
              <input
                type="number"
                className="input input-bordered w-full"
                value={premissa.prazo_entrega_padrao}
                onChange={(e) => setPremissa({...premissa, prazo_entrega_padrao: e.target.value})}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Garantia Instalação (Meses)</label>
              <input
                type="number"
                className="input input-bordered w-full"
                value={premissa.garantia_instalacao_meses}
                onChange={(e) => setPremissa({...premissa, garantia_instalacao_meses: e.target.value})}
              />
            </div>
          </div>
        </div>

        {/* TAXAS DE PARCELAMENTO */}
        <div className="card bg-base-100 shadow p-6 rounded-lg">
          <h3 className="font-semibold text-lg mb-4 border-b pb-2">Taxas de Parcelamento (%)</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">12x</label>
              <input
                type="number"
                step="0.1"
                className="input input-bordered w-full"
                value={taxas['12']}
                onChange={(e) => setTaxas({...taxas, '12': e.target.value})}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">18x</label>
              <input
                type="number"
                step="0.1"
                className="input input-bordered w-full"
                value={taxas['18']}
                onChange={(e) => setTaxas({...taxas, '18': e.target.value})}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">24x</label>
              <input
                type="number"
                step="0.1"
                className="input input-bordered w-full"
                value={taxas['24']}
                onChange={(e) => setTaxas({...taxas, '24': e.target.value})}
              />
            </div>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="btn btn-primary w-full flex items-center justify-center gap-2"
        >
          <Save size={20} />
          {loading ? 'Salvando...' : 'Salvar Configurações'}
        </button>
      </form>
    </div>
  );
};

export default PremissasConfig;