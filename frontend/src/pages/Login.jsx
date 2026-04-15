import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sun, LogIn } from 'lucide-react';
import { authAPI } from '../services/api';

const TENANT_ID = localStorage.getItem('tenant_id') || 'a9664639-f0ff-4c9f-ba72-27286841aa69';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Salvar tenant_id no localStorage antes de fazer login
      localStorage.setItem('tenant_id', TENANT_ID);
      
      const response = await authAPI.login(email, password, TENANT_ID);
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);
      navigate('/dashboard');
    } catch (err) {
      let mensagemErro;
      const data = err.response?.data;
      if (data?.detail) {
        if (typeof data.detail === 'string') {
          mensagemErro = data.detail;
        } else if (Array.isArray(data.detail)) {
          mensagemErro = data.detail.map(d => d.msg ?? d.message).join(', ');
        } else {
          mensagemErro = 'Erro de validação';
        }
      } else {
        mensagemErro = err.message || 'Erro ao conectar com o servidor';
      }
      setError(mensagemErro);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Painel esquerdo — branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-surface-900 relative overflow-hidden">
        {/* Padrão decorativo */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-20 w-72 h-72 bg-solar-500 rounded-full blur-3xl" />
          <div className="absolute bottom-20 right-20 w-96 h-96 bg-solar-400 rounded-full blur-3xl" />
        </div>

        <div className="relative z-10 flex flex-col justify-between p-12 w-full">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-solar-500 rounded-lg flex items-center justify-center">
              <Sun size={22} className="text-white" />
            </div>
            <span className="text-white text-xl font-semibold tracking-tight">SunOps</span>
          </div>

          <div>
            <h2 className="text-white text-4xl font-bold leading-tight tracking-tight">
              Gestão solar<br />simples e eficiente
            </h2>
            <p className="text-surface-400 mt-4 text-lg max-w-md">
              Orçamentos, propostas e contratos em um só lugar.
            </p>
          </div>

          <div className="flex items-center gap-6 text-surface-500 text-sm">
            <span>CRM Solar</span>
            <span className="w-1 h-1 bg-surface-600 rounded-full" />
            <span>v1.0</span>
          </div>
        </div>
      </div>

      {/* Painel direito — formulário */}
      <div className="flex-1 flex items-center justify-center p-6 sm:p-8">
        <div className="w-full max-w-sm">
          {/* Logo mobile */}
          <div className="lg:hidden flex items-center gap-3 mb-10">
            <div className="w-9 h-9 bg-solar-500 rounded-lg flex items-center justify-center">
              <Sun size={18} className="text-white" />
            </div>
            <span className="text-surface-900 text-lg font-semibold tracking-tight">SunOps</span>
          </div>

          <div className="mb-8">
            <h1 className="text-2xl font-semibold text-surface-900 tracking-tight">Bem-vindo de volta</h1>
            <p className="text-surface-500 mt-1.5 text-sm">Insira suas credenciais para acessar o sistema</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label htmlFor="email" className="label">Email</label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input"
                placeholder="seu@email.com"
                autoComplete="email"
                required
              />
            </div>

            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label htmlFor="password" className="label mb-0">Senha</label>
              </div>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input"
                placeholder="••••••••"
                autoComplete="current-password"
                required
              />
            </div>

            {error && (
              <div className="flex items-start gap-3 p-3 rounded-lg bg-danger-bg border border-danger-border text-danger text-sm animate-fadeIn">
                <LogIn size={16} className="mt-0.5 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary py-3 text-sm"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Entrando...
                </span>
              ) : 'Entrar'}
            </button>
          </form>

          <p className="mt-8 text-center text-xs text-surface-400">
            © 2025 SunOps. Todos os direitos reservados.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
