import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Plus, Trash2, Save, AlertTriangle, FileText } from 'lucide-react';
import api from '../services/api';
import { useToast, ToastContainer } from '../components/Toast';

const OrcamentoDetalhe = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { toasts, showToast, removeToast } = useToast();
  
  const [orcamento, setOrcamento] = useState(null);
  const [itens, setItens] = useState([]);
  const [deslocamento, setDeslocamento] = useState(null);
  const [premissas, setPremissas] = useState(null);
  const [editando, setEditando] = useState(false);
  const [itemEditando, setItemEditando] = useState(null);
  
  const [valoresOriginais, setValoresOriginais] = useState({});
  const [valoresEditados, setValoresEditados] = useState({
    comissao: 0,
    lucro: 0,
    imposto: 0
  });

  useEffect(() => {
    carregarDados();
  }, [id]);

  const carregarDados = async () => {
    try {
      const [orcRes, detRes, premRes] = await Promise.all([
        api.get(`/orcamentos/${id}/`),
        api.get(`/orcamentos/${id}/detalhamento/`),
        api.get('/premissas/ativa/')
      ]);
      
      setOrcamento(orcRes.data);
      setItens(detRes.data.itens);
      setDeslocamento(detRes.data.deslocamento);
      setPremissas(premRes.data);
      
      // Usar margens do orçamento se existirem, senão usar das premissas
      const originais = {
        comissao: orcRes.data.comissao_percentual || premRes.data.comissao_percentual,
        lucro: orcRes.data.margem_lucro_percentual || premRes.data.margem_lucro_percentual,
        imposto: orcRes.data.imposto_percentual || premRes.data.imposto_percentual
      };
      setValoresOriginais(originais);
      setValoresEditados(originais);
    } catch (error) {
      console.error('Erro:', error);
      showToast('Erro ao carregar orçamento', 'error');
      navigate('/orcamentos');
    }
  };

  const adicionarItem = () => {
    setItens([...itens, {
      categoria: 'Custos',
      item: '',
      quantidade: 1,
      valor_unitario: 0,
      valor_total: 0
    }]);
    showToast('Item adicionado', 'success');
  };

  const removerItem = (index) => {
    setItens(itens.filter((_, i) => i !== index));
    showToast('Item removido', 'success');
  };

  const atualizarItem = (index, campo, valor) => {
    const novosItens = [...itens];
    novosItens[index][campo] = valor;
    
    if (campo === 'quantidade' || campo === 'valor_unitario') {
      novosItens[index].valor_total = novosItens[index].quantidade * novosItens[index].valor_unitario;
    }
    
    setItens(novosItens);
  };

  const calcularTotal = () => {
    return itens.reduce((sum, item) => sum + parseFloat(item.valor_total || 0), 0);
  };

  const calcularSubtotal = () => {
    return itens.reduce((sum, item) => sum + parseFloat(item.valor_total || 0), 0);
  };

  const arredondarValor = (valor) => {
    return Math.ceil(valor / 100) * 100;
  };

  const calcularValorBase = () => {
    const custo = calcularSubtotal();
    const comissao = parseFloat(valoresEditados.comissao) || 0;
    const imposto = parseFloat(valoresEditados.imposto) || 0;
    const lucro = parseFloat(valoresEditados.lucro) || 0;
    const percentualTotal = (comissao + imposto + lucro) / 100;
    
    if (percentualTotal >= 1 || percentualTotal <= 0) return custo;
    
    const valorBase = custo / (1 - percentualTotal);
    return arredondarValor(valorBase);
  };

  const calcularValorFinal = () => {
    const valorBase = calcularValorBase();
    const margemDesconto = premissas?.margem_desconto_avista_percentual || 2;
    const valorComMargem = valorBase * (1 + margemDesconto / 100);
    return arredondarValor(valorComMargem);
  };

  const calcularComissao = () => {
    const comissao = parseFloat(valoresEditados.comissao) || 0;
    return calcularValorFinal() * (comissao / 100);
  };

  const calcularImposto = () => {
    const imposto = parseFloat(valoresEditados.imposto) || 0;
    return calcularValorFinal() * (imposto / 100);
  };

  const calcularLucro = () => {
    const lucro = parseFloat(valoresEditados.lucro) || 0;
    return calcularValorFinal() * (lucro / 100);
  };

  const calcularTotalArredondado = () => {
    return calcularValorFinal();
  };

  const calcularValorFinalComMargem = () => {
    return calcularValorFinal();
  };

  const calcularMargemDesconto = () => {
    return 0;
  };

  const salvar = async () => {
    try {
      const valorFinalCalculado = calcularValorFinal();
      const custoTotal = calcularSubtotal();
      
      await api.patch(`/orcamentos/${id}/`, {
        itens_adicionais: itens.filter(i => i.categoria === 'Custos' && i.item && !['Materiais Elétricos', 'Estrutura'].some(base => i.item.includes(base))),
        valor_total: custoTotal,
        valor_final: valorFinalCalculado,
        comissao_percentual: valoresEditados.comissao,
        imposto_percentual: valoresEditados.imposto,
        margem_lucro_percentual: valoresEditados.lucro
      });
      
      showToast('Orçamento atualizado com sucesso!', 'success');
      setEditando(false);
      carregarDados();
    } catch (error) {
      console.error('Erro:', error);
      showToast('Erro ao salvar orçamento', 'error');
    }
  };

  const foiAlterado = (campo) => {
    return valoresEditados[campo] !== valoresOriginais[campo];
  };

  if (!orcamento) return <div className="p-6">Carregando...</div>;

  return (
    <div className="space-y-6">
      <ToastContainer toasts={toasts} removeToast={removeToast} />
      
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button onClick={() => navigate('/orcamentos')} className="btn-outline p-2">
            <ArrowLeft size={20} />
          </button>
          <div>
            <h2 className="text-2xl font-bold">Orçamento #{orcamento.numero}</h2>
            <p className="text-gray-600">{orcamento.cliente_nome} - {orcamento.nome_kit}</p>
          </div>
        </div>
        
        <div className="flex gap-2">
          <button 
            onClick={async () => {
              try {
                const response = await api.get(`/orcamentos/${id}/gerar-pdf-dimensionamento/`, {
                  responseType: 'blob'
                });
                
                const contentType = response.headers['content-type'];
                const isPdf = contentType.includes('application/pdf');
                const extension = isPdf ? 'pdf' : 'docx';
                
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', `Orcamento_${orcamento.numero}.${extension}`);
                document.body.appendChild(link);
                link.click();
                link.remove();
                window.URL.revokeObjectURL(url);
                showToast('Orçamento gerado com sucesso!', 'success');
              } catch (error) {
                console.error('Erro:', error);
                showToast(error.response?.data?.error || 'Erro ao gerar orçamento', 'error');
              }
            }}
            className="btn-primary flex items-center gap-2"
          >
            <FileText size={20} />
            Gerar PDF
          </button>
          {editando ? (
            <>
              <button 
                onClick={() => {
                  setEditando(false);
                  carregarDados();
                  showToast('Edição cancelada', 'warning');
                }} 
                className="btn-outline"
              >
                Cancelar
              </button>
              <button onClick={salvar} className="btn-accent flex items-center gap-2">
                <Save size={20} />
                Salvar
              </button>
            </>
          ) : (
            <button 
              onClick={() => {
                setEditando(true);
                showToast('Modo de edição ativado', 'success');
              }} 
              className="btn-accent"
            >
              Editar
            </button>
          )}
        </div>
      </div>

      {/* Resumo */}
      <div className="grid grid-cols-4 gap-4">
        <div className="card">
          <p className="text-sm text-gray-600">Painéis</p>
          <p className="text-2xl font-bold">{orcamento.quantidade_paineis}x {orcamento.potencia_painel}W</p>
          <p className="text-xs text-gray-500">{orcamento.marca_painel}</p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-600">Inversor</p>
          <p className="text-2xl font-bold">{orcamento.quantidade_inversores}x {orcamento.potencia_inversor}W</p>
          <p className="text-xs text-gray-500">{orcamento.marca_inversor}</p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-600">Potência Total</p>
          <p className="text-2xl font-bold text-accent">
            {((orcamento.quantidade_paineis * orcamento.potencia_painel) / 1000).toFixed(2)} kWp
          </p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-600">Estrutura</p>
          <p className="text-2xl font-bold">{orcamento.tipo_estrutura}</p>
        </div>
      </div>

      {/* Tabela de Itens */}
      <div className="card">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-bold">Itens do Orçamento</h3>
          {editando && (
            <button onClick={adicionarItem} className="btn-accent text-sm flex items-center gap-2">
              <Plus size={16} />
              Adicionar Item
            </button>
          )}
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-100">
              <tr>
                <th className="text-left p-3 text-sm font-semibold">Categoria</th>
                <th className="text-left p-3 text-sm font-semibold">Item</th>
                <th className="text-center p-3 text-sm font-semibold">Qtd</th>
                <th className="text-right p-3 text-sm font-semibold">Valor Unit.</th>
                <th className="text-right p-3 text-sm font-semibold">Total</th>
                {editando && <th className="text-center p-3 text-sm font-semibold">Ações</th>}
              </tr>
            </thead>
            <tbody>
              {itens.map((item, index) => (
                <tr key={index} className="border-b hover:bg-gray-50">
                  <td className="p-3">
                    {itemEditando === index && item.categoria === 'Custos' && !['Materiais Elétricos', 'Estrutura'].includes(item.item) ? (
                      <select
                        className="input text-sm"
                        value={item.categoria}
                        onChange={(e) => atualizarItem(index, 'categoria', e.target.value)}
                      >
                        <option value="Kit">Kit</option>
                        <option value="Serviços">Serviços</option>
                        <option value="Custos">Custos</option>
                      </select>
                    ) : (
                      <span 
                        className="text-sm cursor-pointer hover:bg-blue-50 px-2 py-1 rounded"
                        onDoubleClick={() => {
                          if (item.categoria === 'Custos' && !['Materiais Elétricos', 'Estrutura'].includes(item.item)) {
                            setItemEditando(index);
                            showToast('Duplo clique nos campos para editar', 'success');
                          }
                        }}
                        title={item.categoria === 'Custos' && !['Materiais Elétricos', 'Estrutura'].includes(item.item) ? 'Duplo clique para editar' : 'Item não editável'}
                      >
                        {item.categoria}
                      </span>
                    )}
                  </td>
                  <td className="p-3">
                    {itemEditando === index && item.categoria === 'Custos' && !['Materiais Elétricos', 'Estrutura'].includes(item.item) ? (
                      <input
                        type="text"
                        className="input text-sm"
                        value={item.item}
                        onChange={(e) => atualizarItem(index, 'item', e.target.value)}
                        autoFocus
                      />
                    ) : (
                      <span 
                        className="text-sm cursor-pointer hover:bg-blue-50 px-2 py-1 rounded"
                        onDoubleClick={() => {
                          if (item.categoria === 'Custos' && !['Materiais Elétricos', 'Estrutura'].includes(item.item)) {
                            setItemEditando(index);
                            showToast('Editando item', 'success');
                          }
                        }}
                        title={item.categoria === 'Custos' && !['Materiais Elétricos', 'Estrutura'].includes(item.item) ? 'Duplo clique para editar' : 'Item não editável'}
                      >
                        {item.item}
                      </span>
                    )}
                  </td>
                  <td className="p-3 text-center">
                    {itemEditando === index ? (
                      <input
                        type="number"
                        className="input text-sm w-20 text-center"
                        value={item.quantidade}
                        onChange={(e) => atualizarItem(index, 'quantidade', parseFloat(e.target.value))}
                      />
                    ) : (
                      <span 
                        className="text-sm cursor-pointer hover:bg-blue-50 px-2 py-1 rounded"
                        onDoubleClick={() => {
                          setItemEditando(index);
                          showToast('Editando item', 'success');
                        }}
                        title="Duplo clique para editar"
                      >
                        {item.quantidade}
                      </span>
                    )}
                  </td>
                  <td className="p-3 text-right">
                    {itemEditando === index ? (
                      <input
                        type="number"
                        step="0.01"
                        className="input text-sm w-32 text-right"
                        value={item.valor_unitario}
                        onChange={(e) => atualizarItem(index, 'valor_unitario', parseFloat(e.target.value))}
                      />
                    ) : (
                      <span 
                        className="text-sm cursor-pointer hover:bg-blue-50 px-2 py-1 rounded"
                        onDoubleClick={() => {
                          setItemEditando(index);
                          showToast('Editando item', 'success');
                        }}
                        title="Duplo clique para editar"
                      >
                        R$ {parseFloat(item.valor_unitario).toLocaleString('pt-BR', {minimumFractionDigits: 2})}
                      </span>
                    )}
                  </td>
                  <td className="p-3 text-right">
                    <span className="text-sm font-semibold">
                      R$ {parseFloat(item.valor_total).toLocaleString('pt-BR', {minimumFractionDigits: 2})}
                    </span>
                  </td>
                  {(editando || itemEditando !== null) && (
                    <td className="p-3 text-center">
                      {itemEditando === index && (
                        <button
                          onClick={() => {
                            setItemEditando(null);
                            showToast('Alterações salvas', 'success');
                          }}
                          className="text-green-500 hover:text-green-700 font-bold"
                          title="Confirmar edição"
                        >
                          ✓ OK
                        </button>
                      )}
                      {item.categoria === 'Custos' && !['Materiais Elétricos', 'Estrutura'].includes(item.item) && (
                        <button
                          onClick={() => removerItem(index)}
                          className="ml-2 text-red-500 hover:text-red-700"
                          title="Excluir item"
                        >
                          <Trash2 size={16} />
                        </button>
                      )}
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
            <tfoot className="bg-gray-50">
              <tr className="border-b">
                <td colSpan={(editando || itemEditando !== null) ? 4 : 4} className="p-3 text-right font-semibold">CUSTO TOTAL:</td>
                <td className="p-3 text-right">
                  <span className="text-lg font-semibold">
                    R$ {calcularSubtotal().toLocaleString('pt-BR', {minimumFractionDigits: 2})}
                  </span>
                </td>
                {(editando || itemEditando !== null) && <td></td>}
              </tr>
              <tr className="border-b bg-blue-50">
                <td colSpan={(editando || itemEditando !== null) ? 4 : 4} className="p-3 text-right font-semibold">VALOR BASE:</td>
                <td className="p-3 text-right">
                  <span className="text-lg font-semibold text-blue-600">
                    R$ {calcularValorBase().toLocaleString('pt-BR', {minimumFractionDigits: 2})}
                  </span>
                </td>
                {(editando || itemEditando !== null) && <td></td>}
              </tr>
              <tr className="border-b bg-yellow-50">
                <td colSpan={(editando || itemEditando !== null) ? 4 : 4} className="p-3 text-right text-sm">+ Margem Desconto ({premissas?.margem_desconto_avista_percentual || 2}%):</td>
                <td className="p-3 text-right">
                  <span className="text-sm text-yellow-600 font-semibold">
                    R$ {(calcularValorFinal() - calcularValorBase()).toLocaleString('pt-BR', {minimumFractionDigits: 2})}
                  </span>
                </td>
                {(editando || itemEditando !== null) && <td></td>}
              </tr>
              <tr className="border-b bg-green-50">
                <td colSpan={(editando || itemEditando !== null) ? 4 : 4} className="p-3 text-right font-bold text-lg">VALOR FINAL:</td>
                <td className="p-3 text-right">
                  <span className="text-2xl font-bold text-green-600">
                    R$ {calcularValorFinal().toLocaleString('pt-BR', {minimumFractionDigits: 2})}
                  </span>
                </td>
                {(editando || itemEditando !== null) && <td></td>}
              </tr>
              <tr className="border-t-2 border-gray-300">
                <td colSpan={(editando || itemEditando !== null) ? 5 : 5} className="p-3 text-center text-xs font-semibold text-gray-500 bg-gray-100">
                  BREAKDOWN FINANCEIRO
                </td>
                {(editando || itemEditando !== null) && <td className="bg-gray-100"></td>}
              </tr>
              <tr className="border-b bg-gray-50">
                <td colSpan={(editando || itemEditando !== null) ? 4 : 4} className="p-3 text-right text-sm">
                  <span className="font-bold text-blue-700">{valoresEditados.comissao}%</span> Comissão:
                  <span className="text-xs text-gray-500 ml-2">({((calcularComissao() / calcularValorFinal()) * 100).toFixed(2)}% do valor final)</span>
                </td>
                <td className="p-3 text-right">
                  <span className="text-sm text-blue-600 font-semibold">
                    R$ {calcularComissao().toLocaleString('pt-BR', {minimumFractionDigits: 2})}
                  </span>
                </td>
                {(editando || itemEditando !== null) && <td></td>}
              </tr>
              <tr className="border-b bg-gray-50">
                <td colSpan={(editando || itemEditando !== null) ? 4 : 4} className="p-3 text-right text-sm">
                  <span className="font-bold text-orange-700">{valoresEditados.imposto}%</span> Imposto:
                  <span className="text-xs text-gray-500 ml-2">({((calcularImposto() / calcularValorFinal()) * 100).toFixed(2)}% do valor final)</span>
                </td>
                <td className="p-3 text-right">
                  <span className="text-sm text-orange-600 font-semibold">
                    R$ {calcularImposto().toLocaleString('pt-BR', {minimumFractionDigits: 2})}
                  </span>
                </td>
                {(editando || itemEditando !== null) && <td></td>}
              </tr>
              <tr className="border-b bg-gray-50">
                <td colSpan={(editando || itemEditando !== null) ? 4 : 4} className="p-3 text-right text-sm">
                  <span className="font-bold text-green-700">{valoresEditados.lucro}%</span> Lucro:
                  <span className="text-xs text-gray-500 ml-2">({((calcularLucro() / calcularValorFinal()) * 100).toFixed(2)}% do valor final)</span>
                </td>
                <td className="p-3 text-right">
                  <span className="text-sm text-green-600 font-semibold">
                    R$ {calcularLucro().toLocaleString('pt-BR', {minimumFractionDigits: 2})}
                  </span>
                </td>
                {(editando || itemEditando !== null) && <td></td>}
              </tr>
              <tr className="border-b bg-purple-50">
                <td colSpan={(editando || itemEditando !== null) ? 4 : 4} className="p-3 text-right text-sm font-semibold">
                  Custo Total:
                  <span className="text-xs text-gray-500 ml-2 font-normal">({((calcularSubtotal() / calcularValorFinal()) * 100).toFixed(2)}% do valor final)</span>
                </td>
                <td className="p-3 text-right">
                  <span className="text-sm text-purple-600 font-semibold">
                    R$ {calcularSubtotal().toLocaleString('pt-BR', {minimumFractionDigits: 2})}
                  </span>
                </td>
                {(editando || itemEditando !== null) && <td></td>}
              </tr>
              {deslocamento && deslocamento.cobrar && (
                <tr className="border-b bg-green-100">
                  <td colSpan={(editando || itemEditando !== null) ? 4 : 4} className="p-3 text-right text-sm">+ Lucro Deslocamento ({deslocamento.distancia_total_km?.toFixed(0)} km):</td>
                  <td className="p-3 text-right">
                    <span className="text-sm text-green-700 font-bold">
                      R$ {deslocamento.margem_lucro?.toFixed(2)}
                    </span>
                  </td>
                  {(editando || itemEditando !== null) && <td></td>}
                </tr>
              )}
              {deslocamento && deslocamento.cobrar && (
                <tr className="border-b bg-green-200">
                  <td colSpan={(editando || itemEditando !== null) ? 4 : 4} className="p-3 text-right text-sm font-bold">LUCRO TOTAL:</td>
                  <td className="p-3 text-right">
                    <span className="text-sm text-green-800 font-bold">
                      R$ {(calcularLucro() + (deslocamento.margem_lucro || 0)).toLocaleString('pt-BR', {minimumFractionDigits: 2})}
                    </span>
                  </td>
                  {(editando || itemEditando !== null) && <td></td>}
                </tr>
              )}
            </tfoot>
          </table>
        </div>
      </div>

      {/* Valores Financeiros */}
      <div className="card">
        <h3 className="text-xl font-bold mb-4">Valores Financeiros</h3>
        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-semibold mb-2">Comissão (%)</label>
            <input
              type="number"
              step="0.01"
              className={`input ${foiAlterado('comissao') ? 'border-2 border-yellow-400 bg-yellow-50' : ''}`}
              value={valoresEditados.comissao}
              onChange={(e) => setValoresEditados({...valoresEditados, comissao: parseFloat(e.target.value)})}
              disabled={!editando}
            />
            {foiAlterado('comissao') && (
              <p className="text-xs text-yellow-600 mt-1 flex items-center gap-1">
                <AlertTriangle size={12} />
                Valor alterado
              </p>
            )}
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2">Margem Lucro (%)</label>
            <input
              type="number"
              step="0.01"
              className={`input ${foiAlterado('lucro') ? 'border-2 border-yellow-400 bg-yellow-50' : ''}`}
              value={valoresEditados.lucro}
              onChange={(e) => setValoresEditados({...valoresEditados, lucro: parseFloat(e.target.value)})}
              disabled={!editando}
            />
            {foiAlterado('lucro') && (
              <p className="text-xs text-yellow-600 mt-1 flex items-center gap-1">
                <AlertTriangle size={12} />
                Valor alterado
              </p>
            )}
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2">Imposto (%)</label>
            <input
              type="number"
              step="0.01"
              className={`input ${foiAlterado('imposto') ? 'border-2 border-yellow-400 bg-yellow-50' : ''}`}
              value={valoresEditados.imposto}
              onChange={(e) => setValoresEditados({...valoresEditados, imposto: parseFloat(e.target.value)})}
              disabled={!editando}
            />
            {foiAlterado('imposto') && (
              <p className="text-xs text-yellow-600 mt-1 flex items-center gap-1">
                <AlertTriangle size={12} />
                Valor alterado
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default OrcamentoDetalhe;
