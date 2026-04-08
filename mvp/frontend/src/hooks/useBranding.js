import { useState, useEffect } from 'react';
import { authAPI, tenantsAPI } from '../services/api';

const STORAGE_KEY = 'sunops_branding';

const DEFAULTS = {
  nome_fantasia: 'SunOps',
  cor_primaria: '#1E40AF',
  cor_secundaria: '#F59E0B',
  logo_url: null,
};

const applyColors = (cor_primaria, cor_secundaria) => {
  document.documentElement.style.setProperty('--color-primary', cor_primaria);
  document.documentElement.style.setProperty('--color-accent', cor_secundaria);
  // accent-dark: versão 15% mais escura da cor secundária
  document.documentElement.style.setProperty('--color-accent-dark', cor_secundaria);
};

export const useBranding = () => {
  const [branding, setBranding] = useState(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      return stored ? JSON.parse(stored) : DEFAULTS;
    } catch {
      return DEFAULTS;
    }
  });

  useEffect(() => {
    applyColors(branding.cor_primaria, branding.cor_secundaria);
  }, [branding]);

  useEffect(() => {
    const carregar = async () => {
      try {
        const me = await authAPI.me();
        const tenantRes = await tenantsAPI.obter(me.data.tenant_id);
        const t = tenantRes.data;
        const dados = {
          nome_fantasia: t.nome_fantasia || DEFAULTS.nome_fantasia,
          cor_primaria: t.cor_primaria || DEFAULTS.cor_primaria,
          cor_secundaria: t.cor_secundaria || DEFAULTS.cor_secundaria,
          logo_url: t.logo_url || null,
        };
        localStorage.setItem(STORAGE_KEY, JSON.stringify(dados));
        setBranding(dados);
      } catch {
        // silencioso — usa defaults
      }
    };
    carregar();
  }, []);

  return branding;
};
