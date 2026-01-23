import { useState, useEffect } from 'react';
import api from '../services/api';

export const useUserRole = () => {
  const [isVendedor, setIsVendedor] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkRole = async () => {
      try {
        const response = await api.get('/auth/me/');
        setIsVendedor(response.data.is_vendedor || false);
        setIsAdmin(response.data.is_staff || response.data.is_superuser || false);
      } catch (error) {
        console.error('Erro ao verificar role:', error);
      } finally {
        setLoading(false);
      }
    };
    checkRole();
  }, []);

  return { isVendedor, isAdmin, loading };
};
