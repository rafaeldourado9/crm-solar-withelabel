import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import PrivateRoute from './components/PrivateRoute';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Clientes from './pages/Clientes';
import Orcamentos from './pages/Orcamentos';
import OrcamentoDetalhe from './pages/OrcamentoDetalhe';
import Contratos from './pages/Contratos';
import Vendedores from './pages/Vendedores';
import Equipamentos from './pages/Equipamentos';
import Premissas from './pages/PremissasConfig';
import Templates from './pages/Templates';
import Suporte from './pages/Suporte';

const App = () => {
  const routes = [
    { path: '/dashboard', component: Dashboard, title: 'Dashboard', allowVendedor: true },
    { path: '/clientes', component: Clientes, title: 'Clientes', allowVendedor: true },
    { path: '/orcamentos', component: Orcamentos, title: 'Orçamentos', allowVendedor: true },
    { path: '/contratos', component: Contratos, title: 'Contratos', allowVendedor: true },
    { path: '/vendedores', component: Vendedores, title: 'Vendedores', allowVendedor: false },
    { path: '/equipamentos', component: Equipamentos, title: 'Equipamentos', allowVendedor: false },
    { path: '/templates', component: Templates, title: 'Templates', allowVendedor: false },
    { path: '/premissas', component: Premissas, title: 'Premissas', allowVendedor: false },
    { path: '/suporte', component: Suporte, title: 'Suporte IA', allowVendedor: true },
  ];

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Navigate to="/login" replace />} />
        
        <Route
          path="/orcamentos/:id"
          element={
            <PrivateRoute>
              <div className="flex min-h-screen">
                <Sidebar />
                <div className="flex-1 w-full">
                  <Header title="Detalhes do Orçamento" />
                  <main className="p-4 md:p-8">
                    <OrcamentoDetalhe />
                  </main>
                </div>
              </div>
            </PrivateRoute>
          }
        />
        
        {routes.map(({ path, component: Component, title }) => (
          <Route
            key={path}
            path={path}
            element={
              <PrivateRoute>
                <div className="flex min-h-screen">
                  <Sidebar />
                  <div className="flex-1 w-full">
                    <Header title={title} />
                    <main className="p-4 md:p-8">
                      <Component />
                    </main>
                  </div>
                </div>
              </PrivateRoute>
            }
          />
        ))}
      </Routes>
    </BrowserRouter>
  );
};

export default App;