import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Home, Users, DollarSign, FileText, FileCheck, FileSignature, Settings, Package, Zap, LogOut, File } from 'lucide-react';
import { useUserRole } from '../hooks/useUserRole';
import { useState } from 'react';

const Sidebar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { isVendedor, isAdmin, loading } = useUserRole();
  const [isOpen, setIsOpen] = useState(false);
  
  const menuItems = [
    { path: '/dashboard', icon: Home, label: 'Dashboard', allowVendedor: true },
    { path: '/clientes', icon: Users, label: 'Clientes', allowVendedor: true },
    { path: '/orcamentos', icon: FileText, label: 'Orçamentos', allowVendedor: true },
    { path: '/contratos', icon: FileSignature, label: 'Contratos', allowVendedor: true },
    { path: '/vendedores', icon: DollarSign, label: 'Vendedores', allowVendedor: false },
    { path: '/equipamentos', icon: Package, label: 'Equipamentos', allowVendedor: false },
    { path: '/templates', icon: File, label: 'Templates', allowVendedor: false },
    { path: '/premissas', icon: Settings, label: 'Premissas', allowVendedor: false },
    { path: '/ia', icon: Zap, label: 'IA Features', allowVendedor: true },
  ];
  
  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };
  
  const filteredMenuItems = isVendedor 
    ? menuItems.filter(item => item.allowVendedor)
    : menuItems;
  
  if (loading) return null;
  
  return (
    <>
      {/* Faixa Vertical Pequena */}
      <div 
        className="fixed left-0 top-1/2 -translate-y-1/2 w-1 h-20 bg-primary rounded-r-lg cursor-pointer hover:w-2 hover:h-24 transition-all z-40 shadow-md"
        onClick={() => setIsOpen(true)}
        onMouseEnter={() => setIsOpen(true)}
      />

      {/* Overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`w-64 bg-primary text-white h-screen p-6 flex flex-col fixed left-0 top-0 overflow-y-auto z-50 transition-transform duration-300 shadow-2xl ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        <div className="mb-8">
          <h1 className="text-2xl font-bold">CRM <span className="text-accent">Solar</span></h1>
          <p className="text-gray-400 text-sm mt-1">Sistema de Gestão</p>
        </div>
        
        <nav className="space-y-2 flex-1">
          {filteredMenuItems.map(({ path, icon: Icon, label }) => (
            <Link
              key={path}
              to={path}
              onClick={() => setIsOpen(false)}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                location.pathname === path
                  ? 'bg-accent text-primary font-medium'
                  : 'text-gray-300 hover:bg-gray-800'
              }`}
            >
              <Icon size={20} />
              <span>{label}</span>
            </Link>
          ))}
        </nav>
        
        <button
          onClick={handleLogout}
          className="flex items-center gap-3 px-4 py-3 rounded-lg text-gray-300 hover:bg-red-600 hover:text-white transition-colors mt-4"
        >
          <LogOut size={20} />
          <span>Sair</span>
        </button>
      </aside>
    </>
  );
};

export default Sidebar;