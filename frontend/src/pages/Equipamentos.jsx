import { useState, useEffect, useRef, useCallback } from 'react';
import { Package, Plus, Edit, Trash, AlertCircle, Search } from 'lucide-react';
import api from '../services/api';

const Equipamentos = () => {
  const [categoria, setCategoria] = useState('inversores');
  const [equipamentos, setEquipamentos] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [busca, setBusca] = useState('');
  const [buscaDebounced, setBuscaDebounced] = useState('');
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const observerTarget = useRef(null);
  const loadingRef = useRef(false);
  const cacheRef = useRef({});
  
  const [formData, setFormData] = useState({
    modelo: '',
    fabricante: '',
    potencia_w: '',
    potencia_maxima_w: ''
  });

  const categorias = [
    { id: 'inversores', label: 'Inversores', endpoint: 'inversores' },
    { id: 'modulos', label: 'Módulos (Painéis)', endpoint: 'paineis' },
  ];

  const getEndpoint = () => {
    const cat = categorias.find(c => c.id === categoria);
    return `/equipamentos/${cat.endpoint}/`;
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      setBuscaDebounced(busca);
    }, 500);
    return () => clearTimeout(timer);
  }, [busca]);

  const carregarEquipamentos = async (pageNum = 1, append = false) => {
    if (loadingRef.current) return;
    
    const cacheKey = `${categoria}-${buscaDebounced}-${pageNum}`;
    if (cacheRef.current[cacheKey] && !append) {
      setEquipamentos(cacheRef.current[cacheKey].data);
      setHasMore(cacheRef.current[cacheKey].hasMore);
      return;
    }
    
    loadingRef.current = true;
    setLoading(true);
    try {
      const params = new URLSearchParams({
        page: pageNum,
        page_size: 100,
        ordering: 'fabricante,potencia_w,modelo'
      });
      if (buscaDebounced) params.append('search', buscaDebounced);
      
      const response = await api.get(`${getEndpoint()}?${params}`);
      const data = response.data.results || [];
      
      if (append) {
        setEquipamentos(prev => {
          const newData = [...prev, ...data];
          cacheRef.current[cacheKey] = { data: newData, hasMore: !!response.data.next };
          return newData;
        });
      } else {
        setEquipamentos(data);
        cacheRef.current[cacheKey] = { data, hasMore: !!response.data.next };
      }
      
      setHasMore(!!response.data.next);
    } catch (error) {
      console.error('Erro ao carregar:', error);
      if (!append) {
        setEquipamentos([]);
      }
      setHasMore(false);
    } finally {
      setLoading(false);
      loadingRef.current = false;
    }
  };

  useEffect(() => {
    setEquipamentos([]);
    setPage(1);
    setHasMore(true);
    carregarEquipamentos(1, false);
  }, [categoria, buscaDebounced]);

  const loadMore = useCallback(() => {
    if (hasMore && !loadingRef.current) {
      const nextPage = page + 1;
      setPage(nextPage);
      carregarEquipamentos(nextPage, true);
    }
  }, [hasMore, page]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      entries => {
        if (entries[0].isIntersecting) {
          loadMore();
        }
      },
      { threshold: 0.1 }
    );

    if (observerTarget.current) {
      observer.observe(observerTarget.current);
    }

    return () => observer.disconnect();
  }, [loadMore]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        ...formData,
        potencia_w: parseInt(formData.potencia_w),
        ...(categoria === 'inversores' && { 
            potencia_maxima_w: parseInt(formData.potencia_maxima_w || formData.potencia_w) 
        })
      };

      const url = getEndpoint();

      if (formData.id) {
        await api.put(`${url}${formData.id}/`, payload);
      } else {
        await api.post(url, payload);
      }
      
      setShowModal(false);
      setFormData({ modelo: '', fabricante: '', potencia_w: '', potencia_maxima_w: '' });
      cacheRef.current = {};
      setEquipamentos([]);
      setPage(1);
      setHasMore(true);
      carregarEquipamentos(1, false);
      alert('Equipamento salvo com sucesso!');
    } catch (error) {
      console.error('Erro ao salvar:', error.response?.data || error);
      alert(`Erro ao salvar: ${JSON.stringify(error.response?.data || 'Verifique o console')}`);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Deseja excluir este equipamento?')) return;
    try {
      await api.delete(`${getEndpoint()}${id}/`);
      cacheRef.current = {};
      setEquipamentos([]);
      setPage(1);
      setHasMore(true);
      carregarEquipamentos(1, false);
    } catch (error) {
      console.error('Erro:', error);
      alert('Erro ao excluir item.');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Package size={32} className="text-accent" />
          <h2 className="text-2xl font-bold">Equipamentos</h2>
        </div>
        <button 
          onClick={() => { 
            setFormData({ modelo: '', fabricante: '', potencia_w: '', potencia_maxima_w: '' }); 
            setShowModal(true); 
          }} 
          className="btn-accent flex items-center gap-2"
        >
          <Plus size={20} />
          Novo Equipamento
        </button>
      </div>

      <div className="flex gap-2">
        {categorias.map((cat) => (
          <button
            key={cat.id}
            onClick={() => setCategoria(cat.id)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              categoria === cat.id
                ? 'bg-accent text-primary'
                : 'bg-white border border-gray-300 hover:bg-gray-50'
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      <div className="card">
        <div className="mb-4 flex gap-3">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="text"
              placeholder="Buscar por fabricante, modelo ou potência (ex: 5000)..."
              className="input w-full pl-10"
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
            />
          </div>
        </div>
        
        <div className="text-sm text-gray-600 mb-3">
          {loading && equipamentos.length === 0 ? (
            <span className="text-blue-600">Carregando...</span>
          ) : (
            <span>Exibindo {equipamentos.length} equipamentos</span>
          )}
        </div>

        {equipamentos.length === 0 && !loading ? (
          <div className="text-center py-8 text-gray-500 flex flex-col items-center">
            <AlertCircle size={48} className="mb-2 opacity-50"/>
            <p>{busca ? 'Nenhum equipamento encontrado.' : 'Nenhum equipamento cadastrado.'}</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-semibold">Fabricante</th>
                  <th className="text-left py-3 px-4 font-semibold">Modelo</th>
                  <th className="text-left py-3 px-4 font-semibold">Potência</th>
                  <th className="text-right py-3 px-4 font-semibold">Ações</th>
                </tr>
              </thead>
              <tbody>
                {equipamentos.map((equip) => (
                <tr key={equip.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4 font-medium">{equip.fabricante}</td>
                  <td className="py-3 px-4">{equip.modelo}</td>
                  <td className="py-3 px-4">
                    {equip.potencia_w} W
                    {categoria === 'inversores' && equip.potencia_maxima_w && (
                      <span className="text-xs text-gray-500 block">Máx: {equip.potencia_maxima_w} W</span>
                    )}
                  </td>
                  <td className="py-3 px-4 text-right flex gap-2 justify-end">
                    <button 
                      onClick={() => { setFormData(equip); setShowModal(true); }} 
                      className="text-blue-600 hover:text-blue-800"
                    >
                      <Edit size={18} />
                    </button>
                    <button onClick={() => handleDelete(equip.id)} className="text-red-600 hover:text-red-800">
                      <Trash size={18} />
                    </button>
                  </td>
                </tr>
                ))}
              </tbody>
            </table>
            
            {hasMore && (
              <div ref={observerTarget} className="py-4 text-center">
                <span className="text-sm text-gray-500">
                  {loading ? 'Carregando mais...' : 'Role para carregar mais'}
                </span>
              </div>
            )}
          </div>
        )}
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-8 max-w-md w-full mx-4">
            <h3 className="text-2xl font-bold mb-6">
              {formData.id ? 'Editar' : 'Novo'} {categorias.find(c => c.id === categoria)?.label}
            </h3>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Modelo</label>
                <input
                  type="text"
                  className="input w-full"
                  value={formData.modelo}
                  onChange={(e) => setFormData({...formData, modelo: e.target.value})}
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">Fabricante</label>
                <input
                  type="text"
                  className="input w-full"
                  value={formData.fabricante}
                  onChange={(e) => setFormData({...formData, fabricante: e.target.value})}
                  required
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">
                    Potência Nominal (W)
                  </label>
                  <input
                    type="number"
                    className="input w-full"
                    value={formData.potencia_w}
                    onChange={(e) => setFormData({...formData, potencia_w: e.target.value})}
                    required
                  />
                </div>

                {categoria === 'inversores' && (
                  <div>
                    <label className="block text-sm font-medium mb-2 text-blue-600">
                      Potência Máx (W)
                    </label>
                    <input
                      type="number"
                      className="input w-full border-blue-200"
                      value={formData.potencia_maxima_w}
                      onChange={(e) => setFormData({...formData, potencia_maxima_w: e.target.value})}
                      required
                      placeholder="Obrigatório"
                    />
                  </div>
                )}
              </div>
              
              <div className="flex gap-3 pt-4">
                <button type="button" onClick={() => setShowModal(false)} className="btn-outline flex-1">
                  Cancelar
                </button>
                <button type="submit" className="btn-accent flex-1">
                  Salvar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Equipamentos;
