import { useState, useEffect } from 'react';
import { authAPI } from '../services/api';

export const useUserRole = () => {
  const [isVendedor, setIsVendedor] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkRole = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          setLoading(false);
          return;
        }
        
        const response = await authAPI.me();
        const role = response.data.role;
        setIsVendedor(role === 'vendedor' || role === 'indicacao');
        setIsAdmin(role === 'admin' || role === 'staff');
      } catch (error) {
        console.warn('Erro ao verificar role:', error.message);
      } finally {
        setLoading(false);
      }
    };
    checkRole();
  }, []);

  return { isVendedor, isAdmin, loading };
};
