import { useState, useEffect, useRef } from 'react';
import { Upload, FileText, Trash2, Download, Eye } from 'lucide-react';
import { templatesAPI } from '../services/api';
import { useToast, ToastContainer } from '../components/Toast';
import { ConfirmDialog } from '../components/ConfirmDialog';
import { renderAsync } from 'docx-preview';

const CHAVES = [
  {
    grupo: 'Cliente',
    itens: [
      '{{CLIENTE_NOME}}', '{{CLIENTE_CPF_CNPJ}}', '{{CLIENTE_TELEFONE}}',
      '{{CLIENTE_EMAIL}}', '{{CLIENTE_ENDERECO}}', '{{CLIENTE_CIDADE}}', '{{CLIENTE_ESTADO}}',
    ],
  },
  {
    grupo: 'Dimensionamento',
    itens: [
      '{{POTENCIA_KWP}}', '{{QUANTIDADE_PAINEIS}}', '{{MODELO_PAINEL}}',
      '{{POTENCIA_PAINEL_W}}', '{{MODELO_INVERSOR}}', '{{POTENCIA_INVERSOR_W}}',
      '{{GERACAO_MENSAL_KWH}}', '{{AREA_NECESSARIA_M2}}',
    ],
  },
  {
    grupo: 'Financeiro (Orçamento)',
    itens: [
      '{{NUMERO_ORCAMENTO}}', '{{VALOR_KIT}}', '{{VALOR_ESTRUTURA}}',
      '{{VALOR_MATERIAL_ELETRICO}}', '{{VALOR_MONTAGEM}}', '{{VALOR_PROJETO}}',
      '{{CUSTO_DESLOCAMENTO}}', '{{SUBTOTAL}}', '{{VALOR_FINAL}}',
      '{{FORMA_PAGAMENTO}}', '{{NUMERO_PARCELAS}}', '{{VALOR_PARCELA}}', '{{TAXA_JUROS}}',
    ],
  },
  {
    grupo: 'Datas (Orçamento)',
    itens: ['{{DATA_ORCAMENTO}}', '{{DATA_VALIDADE}}', '{{DATA_EXTENSO}}'],
  },
  {
    grupo: 'Empresa (Contrato)',
    itens: [
      '{{empresa_razao_social}}', '{{empresa_cnpj}}', '{{empresa_endereco}}',
      '{{empresa_cidade}}', '{{empresa_cep}}', '{{empresa_representante_nome}}',
      '{{empresa_representante_cpf}}', '{{empresa_representante_rg}}',
    ],
  },
  {
    grupo: 'Banco (Contrato)',
    itens: ['{{banco_nome}}', '{{banco_agencia}}', '{{banco_conta}}', '{{banco_titular}}'],
  },
  {
    grupo: 'Valores (Contrato)',
    itens: [
      '{{potencia_total}}', '{{quantidade_paineis}}', '{{valor_total}}',
      '{{valor_total_extenso}}', '{{numero_parcelas}}', '{{valor_parcela}}',
      '{{valor_parcela_extenso}}',
    ],
  },
  {
    grupo: 'Termos (Contrato)',
    itens: ['{{prazo_execucao_dias}}', '{{garantia_instalacao_meses}}', '{{foro_comarca}}'],
  },
];

const Templates = () => {
  const { toasts, showToast, removeToast } = useToast();
  const [templates, setTemplates] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [showChavesModal, setShowChavesModal] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const [confirmDialog, setConfirmDialog] = useState({ isOpen: false, id: null });
  const [uploading, setUploading] = useState(false);
  const previewRef = useRef(null);

  const [formData, setFormData] = useState({ nome: '', tipo: 'orcamento', arquivo: null });

  useEffect(() => {
    carregarTemplates();
  }, []);

  const carregarTemplates = async () => {
    try {
      const response = await templatesAPI.listar();
      setTemplates(Array.isArray(response.data) ? response.data : []);
    } catch {
      showToast('Erro ao carregar templates', 'error');
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    if (!file.name.endsWith('.docx')) {
      showToast('Apenas arquivos .docx são permitidos', 'error');
      return;
    }
    setFormData({ ...formData, arquivo: file });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.arquivo) {
      showToast('Selecione um arquivo .docx', 'error');
      return;
    }
    setUploading(true);
    try {
      const data = new FormData();
      data.append('nome', formData.nome);
      data.append('tipo', formData.tipo);
      data.append('arquivo', formData.arquivo);
      await templatesAPI.upload(data);
      showToast('Template enviado!', 'success');
      setShowModal(false);
      setFormData({ nome: '', tipo: 'orcamento', arquivo: null });
      carregarTemplates();
    } catch (error) {
      const msg = error.response?.data?.detail || 'Erro ao enviar template';
      showToast(msg, 'error');
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await templatesAPI.deletar(id);
      showToast('Template excluído', 'success');
      carregarTemplates();
    } catch {
      showToast('Erro ao excluir template', 'error');
    }
  };

  const handleDownload = async (template) => {
    try {
      const response = await templatesAPI.download(template.id);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.download = `${template.nome}.docx`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      showToast('Download iniciado!', 'success');
    } catch {
      showToast('Erro ao baixar template', 'error');
    }
  };

  const handlePreview = async (template) => {
    try {
      const response = await templatesAPI.download(template.id);
      setShowPreview(true);
      setTimeout(async () => {
        if (previewRef.current) {
          previewRef.current.innerHTML = '';
          await renderAsync(response.data, previewRef.current);
        }
      }, 100);
    } catch {
      showToast('Erro ao visualizar template', 'error');
    }
  };

  const copiarChave = (chave) => {
    navigator.clipboard.writeText(chave);
    showToast(`Copiado: ${chave}`, 'success');
  };

  return (
    <div className="space-y-6">
      <ToastContainer toasts={toasts} removeToast={removeToast} />
      <ConfirmDialog
        isOpen={confirmDialog.isOpen}
        onClose={() => setConfirmDialog({ isOpen: false, id: null })}
        onConfirm={() => handleDelete(confirmDialog.id)}
        title="Excluir Template"
        message="Deseja excluir este template?"
        confirmText="Excluir"
      />

      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">Templates de Documentos</h2>
          <p className="text-gray-600">Gerencie templates .docx para orçamentos e contratos</p>
        </div>
        <div className="flex gap-2">
          <button onClick={() => setShowChavesModal(true)} className="btn-outline flex items-center gap-2">
            <Eye size={18} />
            Ver Chaves
          </button>
          <button onClick={() => setShowModal(true)} className="btn-accent flex items-center gap-2">
            <Upload size={18} />
            Novo Template
          </button>
        </div>
      </div>

      {/* Grid de templates */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {templates.map((t) => (
          <div key={t.id} className={`card border-l-4 ${t.ativo ? 'border-accent' : 'border-gray-300 opacity-60'}`}>
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center gap-3">
                <FileText size={28} className={t.ativo ? 'text-accent' : 'text-gray-400'} />
                <div>
                  <p className="font-bold">{t.nome}</p>
                  <p className="text-xs text-gray-500 capitalize">{t.tipo} {t.ativo ? '· Ativo' : '· Inativo'}</p>
                </div>
              </div>
              <button
                onClick={() => setConfirmDialog({ isOpen: true, id: t.id })}
                className="text-red-400 hover:text-red-600"
              >
                <Trash2 size={16} />
              </button>
            </div>

            <div className="text-xs text-gray-400 mb-3">
              <p>{t.variaveis_encontradas.length} variáveis encontradas</p>
              <p>Criado em: {new Date(t.created_at).toLocaleDateString('pt-BR')}</p>
            </div>

            <div className="flex gap-2">
              <button
                onClick={() => handleDownload(t)}
                className="flex-1 btn-outline text-sm py-2 flex items-center justify-center gap-1"
              >
                <Download size={14} />
                Baixar
              </button>
              <button
                onClick={() => handlePreview(t)}
                className="flex-1 btn-accent text-sm py-2 flex items-center justify-center gap-1"
              >
                <Eye size={14} />
                Preview
              </button>
            </div>
          </div>
        ))}

        {templates.length === 0 && (
          <div className="col-span-full text-center py-16 text-gray-400">
            <FileText size={48} className="mx-auto mb-3 opacity-40" />
            <p>Nenhum template cadastrado</p>
            <p className="text-sm mt-1">Clique em "Novo Template" para começar</p>
          </div>
        )}
      </div>

      {/* Modal Upload */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-8 max-w-md w-full mx-4">
            <h3 className="text-xl font-bold mb-6">Novo Template</h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Nome *</label>
                <input
                  type="text"
                  className="input"
                  placeholder="Ex: Orçamento Padrão 2024"
                  value={formData.nome}
                  onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Tipo *</label>
                <select
                  className="input"
                  value={formData.tipo}
                  onChange={(e) => setFormData({ ...formData, tipo: e.target.value })}
                >
                  <option value="orcamento">Orçamento</option>
                  <option value="proposta">Proposta</option>
                  <option value="contrato">Contrato</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Arquivo (.docx) *</label>
                <input type="file" accept=".docx" className="input" onChange={handleFileChange} required />
                {formData.arquivo && (
                  <p className="text-xs text-green-600 mt-1">✓ {formData.arquivo.name}</p>
                )}
              </div>
              <div className="bg-blue-50 p-3 rounded-lg text-sm text-blue-700">
                Use <code>{'{{CLIENTE_NOME}}'}</code> no Word. As variáveis são substituídas automaticamente ao gerar o documento.
              </div>
              <div className="flex gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => { setShowModal(false); setFormData({ nome: '', tipo: 'orcamento', arquivo: null }); }}
                  className="flex-1 btn-outline"
                  disabled={uploading}
                >
                  Cancelar
                </button>
                <button type="submit" className="flex-1 btn-accent" disabled={uploading}>
                  {uploading ? 'Enviando...' : 'Enviar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal Preview */}
      {showPreview && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl p-4 w-full h-full max-w-5xl max-h-[90vh] flex flex-col">
            <div className="flex justify-between items-center mb-3">
              <h3 className="text-lg font-bold">Preview do Template</h3>
              <button onClick={() => setShowPreview(false)} className="text-2xl text-gray-400 hover:text-gray-700">×</button>
            </div>
            <div ref={previewRef} className="flex-1 border rounded overflow-auto bg-white p-4" />
          </div>
        </div>
      )}

      {/* Modal Chaves */}
      {showChavesModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl p-6 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <h3 className="text-xl font-bold mb-4">Variáveis Disponíveis</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {CHAVES.map((grupo) => (
                <div key={grupo.grupo} className="border rounded-lg p-4">
                  <h4 className="font-semibold text-accent mb-2">{grupo.grupo}</h4>
                  <div className="space-y-1">
                    {grupo.itens.map((chave) => (
                      <div
                        key={chave}
                        onClick={() => copiarChave(chave)}
                        className="flex items-center justify-between p-2 bg-gray-50 rounded hover:bg-gray-100 cursor-pointer"
                      >
                        <code className="text-xs">{chave}</code>
                        <span className="text-xs text-gray-400">copiar</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-4 bg-yellow-50 p-3 rounded-lg text-sm text-yellow-800">
              <strong>Como usar:</strong> Insira as variáveis no seu arquivo .docx. Ao gerar o documento, serão substituídas pelos dados reais.
            </div>
            <button onClick={() => setShowChavesModal(false)} className="w-full btn-accent mt-4">
              Fechar
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Templates;
