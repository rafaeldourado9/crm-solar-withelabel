import { useState } from 'react';
import { CheckCircle, XCircle, AlertCircle, Info, X } from 'lucide-react';

let toastId = 0;

export const useToast = () => {
  const [toasts, setToasts] = useState([]);

  const showToast = (message, type = 'success') => {
    const id = toastId++;
    setToasts(prev => [...prev, { id, message, type }]);
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id));
    }, 3500);
  };

  const removeToast = (id) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  };

  return { toasts, showToast, removeToast };
};

export const ToastContainer = ({ toasts, removeToast }) => {
  if (!toasts.length) return null;

  return (
    <div className="fixed top-4 right-4 z-[9999] space-y-2">
      {toasts.map(toast => (
        <Toast key={toast.id} {...toast} onClose={() => removeToast(toast.id)} />
      ))}
    </div>
  );
};

const TOAST_STYLES = {
  success: {
    icon: <CheckCircle size={16} className="text-green-600 shrink-0" />,
    wrapper: 'bg-white border border-surface-200 shadow-soft-lg',
  },
  error: {
    icon: <XCircle size={16} className="text-danger shrink-0" />,
    wrapper: 'bg-white border border-danger-border shadow-soft-lg',
  },
  warning: {
    icon: <AlertCircle size={16} className="text-warning shrink-0" />,
    wrapper: 'bg-white border border-warning-border shadow-soft-lg',
  },
  info: {
    icon: <Info size={16} className="text-info shrink-0" />,
    wrapper: 'bg-white border border-info-border shadow-soft-lg',
  },
};

const Toast = ({ message, type, onClose }) => {
  const style = TOAST_STYLES[type] || TOAST_STYLES.success;

  return (
    <div className={`${style.wrapper} rounded-lg p-3.5 min-w-[320px] max-w-sm flex items-start gap-3 animate-slideInRight`}>
      {style.icon}
      <p className="flex-1 text-sm text-surface-700 leading-snug">{message}</p>
      <button
        onClick={onClose}
        className="text-surface-400 hover:text-surface-600 transition-colors shrink-0 p-0.5"
      >
        <X size={14} />
      </button>
    </div>
  );
};
