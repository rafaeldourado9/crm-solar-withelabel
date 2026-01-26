import { useState, useEffect } from 'react';
import { Upload, FileText, Trash2, Download, Eye, Zap } from 'lucide-react';
import api from '../services/api';
import { useToast, ToastContainer } from '../components/Toast';
import { ConfirmDialog } from '../components/ConfirmDialog';

const Templates = () => {
  const { toasts, showToast, removeToast } = useToast();
  const [templates, setTemplates] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [showChavesModal, setShowChavesModal] = useState(false);
  const [confirmDialog, setConfirmDialog] = useState({ isOpen: false, templateId: null });
  const [uploading, setUploading] = useState(false);
  
  const [formData, setFormData] = useState({
    nome: '',
    tipo: 'orcamento',
    arquivo: null
  });

  const chaves = [
    { grupo: 'Orçamento', itens: ['{{NUMERO_ORCAMENTO}}', '{{DATA_CRIACAO}}', '{{NOME_KIT}}'] },
    { grupo: 'Cliente', itens: ['{{CLIENTE_NOME}}', '{{CLIENTE_CPF_CNPJ}}', '{{CLIENTE_TELEFONE}}', '{{CLIENTE_EMAIL}}', '{{CLIENTE_ENDERECO}}', '{{CLIENTE_CIDADE}}', '{{CLIENTE_ESTADO}}'] },
    { grupo: 'Painéis', itens: ['{{PAINEIS_QTD}}', '{{PAINEIS_MARCA}}', '{{PAINEIS_POTENCIA}}', '{{PAINEIS_POTENCIA_TOTAL}}'] },
    { grupo: 'Inversor', itens: ['{{INVERSOR_QTD}}', '{{INVERSOR_MARCA}}', '{{INVERSOR_POTENCIA}}', '{{INVERSOR_OVERLOAD}}'] },
    { grupo: 'Técnico', itens: ['{{POTENCIA_TOTAL_KWP}}', '{{GERACAO_ESTIMADA_KWH}}', '{{HSP}}', '{{PERDA_SISTEMA}}', '{{TIPO_ESTRUTURA}}'] },
    { grupo: 'Financeiro', itens: ['{{VALOR_KIT}}', '{{VALOR_FINAL}}', '{{CUSTO_TOTAL}}', '{{COMISSAO_PERCENTUAL}}', '{{IMPOSTO_PERCENTUAL}}', '{{LUCRO_PERCENTUAL}}'] },
  ];

  useEffect(() => {
    carregarTemplates();
  }, []);

  const carregarTemplates = async () => {
    try {
      const response = await api.get('/templates/');
      setTemplates(response.data.results || response.data);
    } catch (error) {
      console.error('Erro:', error);
      showToast('Erro ao carregar templates', 'error');
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const ext = file.name.split('.').pop().toLowerCase();
      if (ext !== 'docx') {
        showToast('Apenas arquivos .docx são permitidos', 'error');
        return;
      }
      setFormData({...formData, arquivo: file});
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setUploading(true);

    try {
      const data = new FormData();
      data.append('nome', formData.nome);
      data.append('tipo', formData.tipo);
      data.append('arquivo', formData.arquivo);

      await api.post('/templates/', data, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      showToast('Template enviado com sucesso!', 'success');
      setShowModal(false);
      setFormData({ nome: '', tipo: 'orcamento', arquivo: null });
      carregarTemplates();
    } catch (error) {
      console.error('Erro completo:', error);
      console.error('Resposta do servidor:', error.response?.data);
      const mensagem = error.response?.data?.error || error.response?.data?.arquivo?.[0] || 'Erro ao enviar template';
      showToast(mensagem, 'error');
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(`/templates/${id}/`);
      showToast('Template excluído com sucesso', 'success');
      carregarTemplates();
    } catch (error) {
      showToast('Erro ao excluir template', 'error');
    }
  };

  const copiarChave = (chave) => {
    navigator.clipboard.writeText(chave);
    showToast(`Chave ${chave} copiada!`, 'success');
  };

  return (
    <div className="space-y-6">
      <ToastContainer toasts={toasts} removeToast={removeToast} />
      <ConfirmDialog
        isOpen={confirmDialog.isOpen}
        onClose={() => setConfirmDialog({ isOpen: false, templateId: null })}
        onConfirm={() => handleDelete(confirmDialog.templateId)}
        title="Excluir Template"
        message="Deseja excluir este template?"
        confirmText="Excluir"
      />

      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">Templates de Documentos</h2>
          <p className="text-gray-600">Gerencie templates para orçamentos e contratos</p>
        </div>
        <div className="flex gap-2">
          <button 
            onClick={() => setShowChavesModal(true)}
            className="btn-outline flex items-center gap-2"
          >
            <Eye size={20} />
            Ver Chaves
          </button>
          <button 
            onClick={() => setShowModal(true)}
            className="btn-accent flex items-center gap-2"
          >
            <Upload size={20} />
            Novo Template
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {templates.map((template) => (
          <div key={template.id} className="card border-l-4 border-accent">
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center gap-3">
                <FileText size={32} className="text-accent" />
                <div>
                  <p className="font-bold">{template.nome}</p>
                  <p className="text-xs text-gray-500 capitalize">{template.tipo}</p>
                </div>
              </div>
              <button
                onClick={() => setConfirmDialog({ isOpen: true, templateId: template.id })}
                className="text-red-500 hover:text-red-700"
              >
                <Trash2 size={18} />
              </button>
            </div>
            
            <div className="text-xs text-gray-500 mb-3">
              <p>Enviado em: {new Date(template.created_at).toLocaleDateString('pt-BR')}</p>
              <p>Arquivo: {template.arquivo_nome}</p>
            </div>

            <div className="flex gap-2">
              <button
                onClick={async () => {
                  try {
                    const response = await api.get(`/templates/${template.id}/?download=true`, { responseType: 'blob' });
                    const url = window.URL.createObjectURL(new Blob([response.data]));
                    const link = document.createElement('a');
                    link.href = url;
                    link.setAttribute('download', template.arquivo_nome);
                    document.body.appendChild(link);
                    link.click();
                    link.remove();
                    showToast('Download iniciado!', 'success');
                  } catch (error) {
                    showToast('Erro ao baixar', 'error');
                  }
                }}
                className="flex-1 btn-outline text-sm py-2 flex items-center justify-center gap-2"
              >
                <Download size={16} />
                Baixar
              </button>
              
              <button
                onClick={() => window.open(`http://localhost:8000/media/templates/${template.arquivo_nome}`, '_blank')}
                className="flex-1 btn-accent text-sm py-2 flex items-center justify-center gap-2"
              >
                <Eye size={16} />
                Abrir
              </button>
            </div>
          </div>
        ))}

        {templates.length === 0 && (
          <div className="col-span-full text-center py-12 text-gray-500">
            <FileText size={48} className="mx-auto mb-3 opacity-50" />
            <p>Nenhum template cadastrado</p>
          </div>
        )}
      </div>

      {/* Modal Upload */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-8 max-w-md w-full mx-4">
            <h3 className="text-2xl font-bold mb-6">Novo Template</h3>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Nome do Template *</label>
                <input
                  type="text"
                  className="input"
                  placeholder="Ex: Orçamento Padrão"
                  value={formData.nome}
                  onChange={(e) => setFormData({...formData, nome: e.target.value})}
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Tipo *</label>
                <select
                  className="input"
                  value={formData.tipo}
                  onChange={(e) => setFormData({...formData, tipo: e.target.value})}
                >
                  <option value="orcamento">Orçamento</option>
                  <option value="contrato">Contrato</option>
                  <option value="proposta">Proposta</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Arquivo (.docx) *</label>
                <input
                  type="file"
                  accept=".docx"
                  className="input"
                  onChange={handleFileChange}
                  required
                />
                {formData.arquivo && (
                  <p className="text-xs text-green-600 mt-1">
                    ✓ {formData.arquivo.name}
                  </p>
                )}
              </div>

              <div className="bg-blue-50 p-3 rounded-lg text-sm">
                <p className="font-semibold text-blue-800 mb-1">💡 Dica:</p>
                <p className="text-blue-700">
                  Use as chaves como {'{{CLIENTE_NOME}}'} no seu documento Word. 
                  Elas serão substituídas automaticamente ao gerar o PDF.
                </p>
              </div>

              <div className="flex gap-3 pt-4">
                <button 
                  type="button" 
                  onClick={() => {
                    setShowModal(false);
                    setFormData({ nome: '', tipo: 'orcamento', arquivo: null });
                  }}
                  className="flex-1 btn-outline"
                  disabled={uploading}
                >
                  Cancelar
                </button>
                <button 
                  type="submit" 
                  className="flex-1 btn-accent"
                  disabled={uploading}
                >
                  {uploading ? 'Enviando...' : 'Enviar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal Chaves */}
      {showChavesModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl p-8 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <h3 className="text-2xl font-bold mb-6">Chaves Disponíveis</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {chaves.map((grupo) => (
                <div key={grupo.grupo} className="border rounded-lg p-4">
                  <h4 className="font-bold text-lg mb-3 text-accent">{grupo.grupo}</h4>
                  <div className="space-y-2">
                    {grupo.itens.map((chave) => (
                      <div
                        key={chave}
                        onClick={() => copiarChave(chave)}
                        className="flex items-center justify-between p-2 bg-gray-50 rounded hover:bg-gray-100 cursor-pointer"
                      >
                        <code className="text-sm">{chave}</code>
                        <span className="text-xs text-gray-500">Clique para copiar</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-6 bg-yellow-50 p-4 rounded-lg">
              <p className="text-sm text-yellow-800">
                <strong>Como usar:</strong> Insira estas chaves no seu documento Word/PDF. 
                Ao gerar o documento, elas serão substituídas pelos valores reais do orçamento.
              </p>
            </div>

            <button
              onClick={() => setShowChavesModal(false)}
              className="w-full btn-accent mt-6"
            >
              Fechar
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Templates;
