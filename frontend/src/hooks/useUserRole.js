import { useState, useEffect } from 'react';
import { authAPI } from '../services/api';

export const useUserRole = () => {
  const [isVendedor, setIsVendedor] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkRole = async () => {
      try {
        const response = await authAPI.me();
        const role = response.data.role;
        setIsVendedor(role === 'vendedor' || role === 'indicacao');
        setIsAdmin(role === 'admin' || role === 'staff');
      } catch {
        // token inválido — PrivateRoute vai redirecionar
      } finally {
        setLoading(false);
      }
    };
    checkRole();
  }, []);

  return { isVendedor, isAdmin, loading };
};
