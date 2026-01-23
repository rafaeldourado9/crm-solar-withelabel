import { useState, useEffect } from 'react';
import { Settings, Save } from 'lucide-react';
import { premissasAPI } from '../services/api';

const Premissas = () => {
  const [premissa, setPremissa] = useState({
    imposto_percentual: 0,
    comissao_percentual: 0,
    lucro_percentual: 0,
    montagem_por_painel: 0,
    valor_projeto: 0,
    taxa_inflacao_anual: 9.5,
    perda_eficiencia_sistema: 0.8,
    tempo_vida_minima: 25,
    validade_proposta_dias: 10
  });

  useEffect(() => {
    carregarPremissas();
  }, []);

  const carregarPremissas = async () => {
    try {
      const response = await premissasAPI.listar();
      if (response.data.length > 0) {
        setPremissa(response.data[0]);
      }
    } catch (error) {
      console.error('Erro:', error);
    }
  };

  const salvar = async () => {
    try {
      if (premissa.id) {
        await premissasAPI.atualizar(premissa.id, premissa);
      } else {
        await premissasAPI.criar(premissa);
      }
      alert('Premissas salvas com sucesso!');
    } catch (error) {
      console.error('Erro:', error);
    }
  };

  return (
    <div className="space-y-6">
      <div className="card bg-gradient-to-r from-primary to-gray-800 text-white">
        <div className="flex items-center gap-4">
          <Settings size={48} />
          <div>
            <h2 className="text-2xl font-bold">Configurações de Premissas</h2>
            <p className="text-sm opacity-80">Configure margens e parâmetros do sistema</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4 pb-3 border-b border-gray-200">
            💰 Margens Financeiras
          </h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Imposto (%)</label>
              <input
                type="number"
                step="0.01"
                className="input"
                value={premissa.imposto_percentual}
                onChange={(e) => setPremissa({...premissa, imposto_percentual: e.target.value})}
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-2">Comissão (%)</label>
              <input
                type="number"
                step="0.01"
                className="input"
                value={premissa.comissao_percentual}
                onChange={(e) => setPremissa({...premissa, comissao_percentual: e.target.value})}
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-2">Lucro (%)</label>
              <input
                type="number"
                step="0.01"
                className="input"
                value={premissa.lucro_percentual}
                onChange={(e) => setPremissa({...premissa, lucro_percentual: e.target.value})}
              />
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold mb-4 pb-3 border-b border-gray-200">
            🔧 Valores de Serviço
          </h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Montagem por Painel (R$)</label>
              <input
                type="number"
                step="0.01"
                className="input"
                value={premissa.montagem_por_painel}
                onChange={(e) => setPremissa({...premissa, montagem_por_painel: e.target.value})}
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-2">Valor do Projeto (R$)</label>
              <input
                type="number"
                step="0.01"
                className="input"
                value={premissa.valor_projeto}
                onChange={(e) => setPremissa({...premissa, valor_projeto: e.target.value})}
              />
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold mb-4 pb-3 border-b border-gray-200">
            📊 Parâmetros de Cálculo
          </h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Taxa Inflação Anual (%)</label>
              <input
                type="number"
                step="0.01"
                className="input"
                value={premissa.taxa_inflacao_anual}
                onChange={(e) => setPremissa({...premissa, taxa_inflacao_anual: e.target.value})}
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-2">Perda Eficiência Sistema (%)</label>
              <input
                type="number"
                step="0.01"
                className="input"
                value={premissa.perda_eficiencia_sistema}
                onChange={(e) => setPremissa({...premissa, perda_eficiencia_sistema: e.target.value})}
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-2">Tempo Vida Mínima (anos)</label>
              <input
                type="number"
                className="input"
                value={premissa.tempo_vida_minima}
                onChange={(e) => setPremissa({...premissa, tempo_vida_minima: e.target.value})}
              />
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold mb-4 pb-3 border-b border-gray-200">
            ⏱️ Prazos
          </h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Validade Proposta (dias)</label>
              <input
                type="number"
                className="input"
                value={premissa.validade_proposta_dias}
                onChange={(e) => setPremissa({...premissa, validade_proposta_dias: e.target.value})}
              />
            </div>
            
            <div className="p-4 bg-blue-50 rounded-lg">
              <p className="text-sm text-blue-800">
                <strong>💡 Dica:</strong> Estas configurações afetam todos os novos orçamentos criados
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-end">
        <button onClick={salvar} className="btn-accent flex items-center gap-2 px-8">
          <Save size={20} />
          Salvar Configurações
        </button>
      </div>
    </div>
  );
};

export default Premissas;
