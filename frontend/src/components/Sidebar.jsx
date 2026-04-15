import { Link, useLocation, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard, Users, FileText, FileCheck, FileSignature,
  Settings, Package, Bot, LogOut, Sun, Users2, File
} from 'lucide-react';
import { useUserRole } from '../hooks/useUserRole';
import { useBranding } from '../hooks/useBranding';
import { useState, useEffect, useRef } from 'react';

const menuItems = [
  { path: '/dashboard', icon: LayoutDashboard, label: 'Dashboard', allowVendedor: true },
  { path: '/clientes', icon: Users, label: 'Clientes', allowVendedor: true },
  { path: '/orcamentos', icon: FileText, label: 'Orçamentos', allowVendedor: true },
  { path: '/propostas', icon: FileCheck, label: 'Propostas', allowVendedor: true },
  { path: '/contratos', icon: FileSignature, label: 'Contratos', allowVendedor: true },
  { path: '/vendedores', icon: Users2, label: 'Vendedores', allowVendedor: false },
  { path: '/equipamentos', icon: Package, label: 'Equipamentos', allowVendedor: false },
  { path: '/templates', icon: File, label: 'Templates', allowVendedor: false },
  { path: '/premissas', icon: Settings, label: 'Premissas', allowVendedor: false },
  { path: '/suporte', icon: Bot, label: 'Suporte IA', allowVendedor: true },
];

const Sidebar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { isVendedor, loading } = useUserRole();
  const branding = useBranding();
  const [isOpen, setIsOpen] = useState(false);
  const sidebarRef = useRef(null);

  // Fechar ao clicar fora
  useEffect(() => {
    const handleClick = (e) => {
      if (isOpen && sidebarRef.current && !sidebarRef.current.contains(e.target)) {
        // Não fecha se clicou no trigger
        if (!e.target.closest('[data-sidebar-trigger]')) {
          setIsOpen(false);
        }
      }
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, [isOpen]);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('sunops_branding');
    navigate('/login');
  };

  const filteredItems = isVendedor
    ? menuItems.filter(item => item.allowVendedor)
    : menuItems;

  if (loading) return null;

  return (
    <>
      {/* Trigger — barra lateral sutil */}
      <div
        data-sidebar-trigger
        className={`fixed left-0 top-1/2 -translate-y-1/2 w-1 h-16 bg-surface-200 rounded-r cursor-pointer
                    hover:bg-solar-500 hover:w-1.5 transition-all duration-200 z-40`}
        onClick={() => setIsOpen(!isOpen)}
        onMouseEnter={() => setIsOpen(true)}
      />

      {/* Overlay */}
      {isOpen && (
        <div className="fixed inset-0 bg-surface-900/20 backdrop-blur-[1px] z-40" />
      )}

      {/* Sidebar */}
      <aside
        ref={sidebarRef}
        className={`w-64 bg-white border-r border-surface-200 h-screen flex flex-col
                    fixed left-0 top-0 z-50 transition-transform duration-300 ease-out
                    ${isOpen ? 'translate-x-0' : '-translate-x-full'}
                    shadow-soft-lg`}
      >
        {/* Logo */}
        <div className="px-5 py-5 border-b border-surface-100">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-solar-500 rounded-lg flex items-center justify-center">
              <Sun size={16} className="text-white" />
            </div>
            <div>
              <h1 className="text-base font-semibold text-surface-900 tracking-tight">
                {branding.nome_fantasia || 'SunOps'}
              </h1>
              <p className="text-[11px] text-surface-400 font-medium uppercase tracking-wider">Sistema de Gestão</p>
            </div>
          </div>
        </div>

        {/* Navegação */}
        <nav className="flex-1 px-3 py-4 overflow-y-auto space-y-0.5">
          {filteredItems.map(({ path, icon: Icon, label }) => {
            const isActive = location.pathname === path;
            return (
              <Link
                key={path}
                to={path}
                onClick={() => setIsOpen(false)}
                className={`flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium
                           transition-colors duration-100
                           ${isActive
                             ? 'bg-surface-100 text-surface-900'
                             : 'text-surface-600 hover:bg-surface-50 hover:text-surface-900'
                           }`}
              >
                <Icon size={18} className={isActive ? 'text-solar-500' : 'text-surface-400'} />
                <span>{label}</span>
              </Link>
            );
          })}
        </nav>

        {/* Footer — Logout */}
        <div className="px-3 py-4 border-t border-surface-100">
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium
                       text-surface-500 hover:text-danger hover:bg-danger-bg
                       transition-colors duration-150"
          >
            <LogOut size={18} />
            <span>Sair</span>
          </button>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
