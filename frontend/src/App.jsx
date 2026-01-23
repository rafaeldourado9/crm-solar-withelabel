import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import PrivateRoute from './components/PrivateRoute';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Clientes from './pages/Clientes';
import Orcamentos from './pages/Orcamentos';
import Propostas from './pages/Propostas';
import Contratos from './pages/Contratos';
import Vendedores from './pages/Vendedores';
import Equipamentos from './pages/Equipamentos';
import Premissas from './pages/Premissas';
import IAFeatures from './pages/IAFeatures';

const App = () => {
  const routes = [
    { path: '/dashboard', component: Dashboard, title: 'Dashboard' },
    { path: '/clientes', component: Clientes, title: 'Clientes' },
    { path: '/orcamentos', component: Orcamentos, title: 'Orçamentos' },
    { path: '/propostas', component: Propostas, title: 'Propostas' },
    { path: '/contratos', component: Contratos, title: 'Contratos' },
    { path: '/vendedores', component: Vendedores, title: 'Vendedores' },
    { path: '/equipamentos', component: Equipamentos, title: 'Equipamentos' },
    { path: '/premissas', component: Premissas, title: 'Premissas' },
    { path: '/ia', component: IAFeatures, title: 'IA Features' },
  ];

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Navigate to="/login" replace />} />
        
        {routes.map(({ path, component: Component, title }) => (
          <Route
            key={path}
            path={path}
            element={
              <PrivateRoute>
                <div className="flex min-h-screen">
                  <Sidebar />
                  <div className="flex-1">
                    <Header title={title} />
                    <main className="p-8">
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
