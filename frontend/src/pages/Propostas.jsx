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

  useEffect(() => { carregarPropostas(); }, []);

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
    try { await propostasAPI.aceitar(id); showToast('Proposta aceita!', 'success'); carregarPropostas(); }
    catch { showToast('Erro ao aceitar proposta', 'error'); }
  };

  const recusarProposta = async (id) => {
    try { await propostasAPI.recusar(id); showToast('Proposta recusada', 'success'); carregarPropostas(); }
    catch { showToast('Erro ao recusar proposta', 'error'); }
  };

  const gerarContrato = async (propostaId) => {
    try {
      showToast('Gerando contrato...', 'info');
      await contratosAPI.criar({ proposta_id: propostaId, prazo_execucao_dias: 30, garantia_instalacao_meses: 12, foro_comarca: '' });
      showToast('Contrato gerado! Acesse a aba Contratos.', 'success');
      carregarPropostas();
    } catch (error) {
      const msg = error.response?.data?.detail || 'Erro ao gerar contrato';
      showToast(msg, 'error');
    }
  };

  const getStatusIcon = (status) => {
    if (status === 'aceita') return <CheckCircle className="text-green-600" size={16} />;
    if (status === 'recusada') return <XCircle className="text-danger" size={16} />;
    return <Clock className="text-warning" size={16} />;
  };

  const formatarData = (iso) => { if (!iso) return '-'; return new Date(iso).toLocaleDateString('pt-BR'); };
  const formatarValor = (v) => Number(v).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

  return (
    <div className="space-y-6">
      <ToastContainer toasts={toasts} removeToast={removeToast} />
      <ConfirmDialog isOpen={confirmAceitar.isOpen} onClose={() => setConfirmAceitar({ isOpen: false, id: null })}
        onConfirm={() => aceitarProposta(confirmAceitar.id)} title="Aceitar Proposta" message="Confirma aceite desta proposta?" confirmText="Aceitar" />
      <ConfirmDialog isOpen={confirmRecusar.isOpen} onClose={() => setConfirmRecusar({ isOpen: false, id: null })}
        onConfirm={() => recusarProposta(confirmRecusar.id)} title="Recusar Proposta" message="Deseja recusar esta proposta?" confirmText="Recusar" variant="danger" />

      {/* Resumo */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card bg-warning-bg border-warning-border">
          <p className="text-sm text-yellow-700">Pendentes</p>
          <p className="text-3xl font-bold text-yellow-800">{propostas.filter(p => p.status === 'pendente').length}</p>
        </div>
        <div className="card bg-success-bg border-success-border">
          <p className="text-sm text-green-700">Aceitas</p>
          <p className="text-3xl font-bold text-green-800">{propostas.filter(p => p.status === 'aceita').length}</p>
        </div>
        <div className="card bg-danger-bg border-danger-border">
          <p className="text-sm text-red-700">Recusadas</p>
          <p className="text-3xl font-bold text-red-800">{propostas.filter(p => p.status === 'recusada').length}</p>
        </div>
      </div>

      {/* Tabela */}
      <div className="card p-0 overflow-hidden">
        {loading ? (
          <p className="text-center py-8 text-surface-400 text-sm">Carregando...</p>
        ) : (
          <div className="table-wrapper">
            <table className="table">
              <thead>
                <tr>
                  <th>Número</th>
                  <th>Cliente</th>
                  <th>Valor Final</th>
                  <th>Validade</th>
                  <th>Status</th>
                  <th className="text-right">Ações</th>
                </tr>
              </thead>
              <tbody>
                {propostas.map((prop) => (
                  <tr key={prop.id}>
                    <td className="font-medium text-surface-800">{prop.numero}</td>
                    <td>
                      <p className="text-surface-800">{prop.cliente_nome}</p>
                      <p className="text-xs text-surface-400">{prop.cliente_cidade}/{prop.cliente_estado}</p>
                    </td>
                    <td className="font-semibold text-surface-900">{formatarValor(prop.valor_final)}</td>
                    <td className="text-surface-400">{formatarData(prop.data_validade)}</td>
                    <td>
                      <div className="flex items-center gap-2">
                        {getStatusIcon(prop.status)}
                        <span className="capitalize text-sm text-surface-700">{prop.status}</span>
                      </div>
                    </td>
                    <td className="text-right">
                      <div className="flex gap-1.5 justify-end">
                        {prop.status === 'pendente' && (
                          <>
                            <button onClick={() => setConfirmAceitar({ isOpen: true, id: prop.id })} className="btn-accent text-xs py-1 px-2.5">Aceitar</button>
                            <button onClick={() => setConfirmRecusar({ isOpen: true, id: prop.id })} className="btn-outline text-xs py-1 px-2.5 border-danger-border text-danger hover:bg-danger-bg">Recusar</button>
                          </>
                        )}
                        {prop.status === 'aceita' && (
                          <button onClick={() => gerarContrato(prop.id)} className="btn-primary text-xs py-1 px-2.5 flex items-center gap-1">
                            <FileText size={12} /> Gerar Contrato
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
                {propostas.length === 0 && (
                  <tr><td colSpan={6} className="text-center py-12 text-surface-400 text-sm">Nenhuma proposta encontrada</td></tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default Propostas;
