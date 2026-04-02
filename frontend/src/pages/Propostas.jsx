import { useState, useEffect } from 'react';
import { CheckCircle, Clock, XCircle, FileText } from 'lucide-react';
import { propostasAPI, contratosAPI } from '../services/api';
import { useToast, ToastContainer } from '../components/Toast';
import { ConfirmDialog } from '../components/ConfirmDialog';

const Propostas = () => {
  const [propostas, setPropostas] = useState([]);
  const [loading, setLoading] = useState(false);
  const { toasts, showToast, removeToast } = useToast();
  const [confirmAceitar, setConfirmAceitar] = useState({ isOpen: false, id: null });
  const [confirmRecusar, setConfirmRecusar] = useState({ isOpen: false, id: null });

  useEffect(() => {
    carregarPropostas();
  }, []);

  const carregarPropostas = async () => {
    setLoading(true);
    try {
      const response = await propostasAPI.listar();
      const data = response.data;
      setPropostas(Array.isArray(data) ? data : (data.items || []));
    } catch {
      showToast('Erro ao carregar propostas', 'error');
      setPropostas([]);
    } finally {
      setLoading(false);
    }
  };

  const aceitarProposta = async (id) => {
    try {
      await propostasAPI.aceitar(id);
      showToast('Proposta aceita!', 'success');
      carregarPropostas();
    } catch {
      showToast('Erro ao aceitar proposta', 'error');
    }
  };

  const recusarProposta = async (id) => {
    try {
      await propostasAPI.recusar(id);
      showToast('Proposta recusada', 'success');
      carregarPropostas();
    } catch {
      showToast('Erro ao recusar proposta', 'error');
    }
  };

  const gerarContrato = async (propostaId) => {
    try {
      showToast('Gerando contrato...', 'info');
      await contratosAPI.criar({
        proposta_id: propostaId,
        prazo_execucao_dias: 30,
        garantia_instalacao_meses: 12,
        foro_comarca: '',
      });
      showToast('Contrato gerado! Acesse a aba Contratos.', 'success');
      carregarPropostas();
    } catch (error) {
      const msg = error.response?.data?.detail || 'Erro ao gerar contrato';
      showToast(msg, 'error');
    }
  };

  const getStatusIcon = (status) => {
    if (status === 'aceita') return <CheckCircle className="text-green-500" size={18} />;
    if (status === 'recusada') return <XCircle className="text-red-500" size={18} />;
    return <Clock className="text-yellow-500" size={18} />;
  };

  const formatarData = (iso) => {
    if (!iso) return '-';
    return new Date(iso).toLocaleDateString('pt-BR');
  };

  const formatarValor = (v) =>
    Number(v).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

  return (
    <div className="space-y-6">
      <ToastContainer toasts={toasts} removeToast={removeToast} />

      <ConfirmDialog
        isOpen={confirmAceitar.isOpen}
        onClose={() => setConfirmAceitar({ isOpen: false, id: null })}
        onConfirm={() => aceitarProposta(confirmAceitar.id)}
        title="Aceitar Proposta"
        message="Confirma aceite desta proposta?"
        confirmText="Aceitar"
      />
      <ConfirmDialog
        isOpen={confirmRecusar.isOpen}
        onClose={() => setConfirmRecusar({ isOpen: false, id: null })}
        onConfirm={() => recusarProposta(confirmRecusar.id)}
        title="Recusar Proposta"
        message="Deseja recusar esta proposta? Esta ação não pode ser desfeita."
        confirmText="Recusar"
      />

      {/* Cards de resumo */}
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

      <div className="card overflow-x-auto">
        {loading ? (
          <p className="text-center py-8 text-gray-400">Carregando...</p>
        ) : (
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 font-semibold">Número</th>
                <th className="text-left py-3 px-4 font-semibold">Cliente</th>
                <th className="text-left py-3 px-4 font-semibold">Valor Final</th>
                <th className="text-left py-3 px-4 font-semibold">Validade</th>
                <th className="text-left py-3 px-4 font-semibold">Status</th>
                <th className="text-right py-3 px-4 font-semibold">Ações</th>
              </tr>
            </thead>
            <tbody>
              {propostas.map((prop) => (
                <tr key={prop.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4 font-medium">{prop.numero}</td>
                  <td className="py-3 px-4">
                    <p>{prop.cliente_nome}</p>
                    <p className="text-xs text-gray-500">{prop.cliente_cidade}/{prop.cliente_estado}</p>
                  </td>
                  <td className="py-3 px-4 font-semibold text-green-600">
                    {formatarValor(prop.valor_final)}
                  </td>
                  <td className="py-3 px-4 text-sm">{formatarData(prop.data_validade)}</td>
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-2">
                      {getStatusIcon(prop.status)}
                      <span className="capitalize text-sm">{prop.status}</span>
                    </div>
                  </td>
                  <td className="py-3 px-4 text-right">
                    <div className="flex gap-2 justify-end">
                      {prop.status === 'pendente' && (
                        <>
                          <button
                            onClick={() => setConfirmAceitar({ isOpen: true, id: prop.id })}
                            className="btn-accent text-sm py-1 px-3"
                          >
                            Aceitar
                          </button>
                          <button
                            onClick={() => setConfirmRecusar({ isOpen: true, id: prop.id })}
                            className="btn-outline text-sm py-1 px-3 text-red-600 border-red-300"
                          >
                            Recusar
                          </button>
                        </>
                      )}
                      {prop.status === 'aceita' && (
                        <button
                          onClick={() => gerarContrato(prop.id)}
                          className="btn-primary text-sm py-1 px-3 flex items-center gap-1"
                        >
                          <FileText size={14} />
                          Gerar Contrato
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
              {propostas.length === 0 && (
                <tr>
                  <td colSpan={6} className="text-center py-12 text-gray-400">
                    Nenhuma proposta encontrada
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default Propostas;
