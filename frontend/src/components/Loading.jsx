import { Loader2 } from 'lucide-react';

const Loading = ({ message = 'Carregando...' }) => {
  return (
    <div className="min-h-screen bg-surface-50 flex items-center justify-center">
      <div className="text-center">
        <Loader2 size={48} className="text-solar-500 animate-spin mx-auto mb-4" />
        <p className="text-surface-600 text-sm">{message}</p>
      </div>
    </div>
  );
};

export default Loading;
