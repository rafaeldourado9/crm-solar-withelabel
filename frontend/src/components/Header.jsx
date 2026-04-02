import { Bell, User } from 'lucide-react';

const Header = ({ title }) => {
  return (
    <header className="bg-white border-b border-gray-200 px-4 md:px-8 py-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl md:text-2xl font-bold text-primary">{title}</h2>
        
        <div className="flex items-center gap-2 md:gap-4">
          <button className="relative p-2 hover:bg-gray-100 rounded-lg transition-colors">
            <Bell size={20} />
            <span className="absolute top-1 right-1 w-2 h-2 bg-accent rounded-full"></span>
          </button>
          
          <div className="hidden md:flex items-center gap-3 pl-4 border-l border-gray-200">
            <div className="text-right">
              <p className="text-sm font-medium">Admin</p>
              <p className="text-xs text-gray-500">Administrador</p>
            </div>
            <div className="w-10 h-10 bg-accent rounded-full flex items-center justify-center">
              <User size={20} className="text-primary" />
            </div>
          </div>
          
          <div className="md:hidden w-8 h-8 bg-accent rounded-full flex items-center justify-center">
            <User size={16} className="text-primary" />
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;