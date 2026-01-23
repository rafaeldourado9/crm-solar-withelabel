import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Home, Users, DollarSign, FileText, FileCheck, FileSignature, Settings, Package, Zap, LogOut } from 'lucide-react';

const Sidebar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  
  const menuItems = [
    { path: '/dashboard', icon: Home, label: 'Dashboard' },
    { path: '/clientes', icon: Users, label: 'Clientes' },
    { path: '/orcamentos', icon: FileText, label: 'Orçamentos' },
    { path: '/propostas', icon: FileCheck, label: 'Propostas' },
    { path: '/contratos', icon: FileSignature, label: 'Contratos' },
    { path: '/vendedores', icon: DollarSign, label: 'Vendedores' },
    { path: '/equipamentos', icon: Package, label: 'Equipamentos' },
    { path: '/premissas', icon: Settings, label: 'Premissas' },
    { path: '/ia', icon: Zap, label: 'IA Features' },
  ];
  
  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };
  
  return (
    <aside className="w-64 bg-primary text-white min-h-screen p-6 flex flex-col">
      <div className="mb-8">
        <h1 className="text-2xl font-bold">CRM <span className="text-accent">Solar</span></h1>
        <p className="text-gray-400 text-sm mt-1">Sistema de Gestão</p>
      </div>
      
      <nav className="space-y-2 flex-1">
        {menuItems.map(({ path, icon: Icon, label }) => (
          <Link
            key={path}
            to={path}
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
  );
};

export default Sidebar;
