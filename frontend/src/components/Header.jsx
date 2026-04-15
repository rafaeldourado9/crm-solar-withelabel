import { useEffect, useState } from 'react';
import { Bell, User } from 'lucide-react';
import { authAPI } from '../services/api';

const Header = ({ title }) => {
  const [usuario, setUsuario] = useState(null);

  useEffect(() => {
    const carregarUsuario = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) return;
        
        const res = await authAPI.me();
        setUsuario(res.data);
      } catch (error) {
        console.warn('Erro ao carregar usuário:', error.message);
      }
    };
    carregarUsuario();
  }, []);

  const nomeExibido = usuario?.nome?.split(' ')[0] || 'Usuário';
  const roleExibido = usuario?.role === 'admin' ? 'Administrador'
    : usuario?.role === 'vendedor' ? 'Vendedor'
    : usuario?.role === 'indicacao' ? 'Indicação'
    : '';

  return (
    <header className="bg-white border-b border-surface-200 px-6 py-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-surface-900 tracking-tight">{title}</h2>
        </div>

        <div className="flex items-center gap-3">
          {/* Notificações */}
          <button className="relative p-2 text-surface-400 hover:text-surface-600 hover:bg-surface-50 rounded-md transition-colors">
            <Bell size={18} />
            <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 bg-solar-500 rounded-full" />
          </button>

          {/* Divider */}
          <div className="w-px h-8 bg-surface-200" />

          {/* User */}
          <div className="flex items-center gap-3 pl-1">
            <div className="text-right hidden sm:block">
              <p className="text-sm font-medium text-surface-800">{nomeExibido}</p>
              <p className="text-xs text-surface-400">{roleExibido}</p>
            </div>
            <div className="w-9 h-9 bg-surface-100 border border-surface-200 rounded-full flex items-center justify-center">
              <User size={16} className="text-surface-500" />
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
