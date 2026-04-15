# Troubleshooting - Erro 500 Frontend

## Problema: "Failed to load resource: the server responded with a status of 500"

### Causas Comuns

1. **Backend não está rodando**
   - Verifique se o backend está ativo na porta 8000
   - Execute: `cd backend && uvicorn src.main:app --reload`

2. **Problemas de CORS**
   - Verifique as configurações de CORS no backend
   - Arquivo: `backend/src/config.py`

3. **Banco de dados não inicializado**
   - Execute as migrations: `cd backend && alembic upgrade head`
   - Execute o seed: `cd backend && python seed.py`

4. **Variáveis de ambiente não configuradas**
   - Copie `.env.example` para `.env` no backend
   - Copie `.env.example` para `.env` no frontend

### Verificações Rápidas

#### 1. Verificar se o backend está rodando
```bash
curl http://localhost:8000/api/v1/health
```

Resposta esperada:
```json
{"status": "ok", "version": "1.0.0"}
```

#### 2. Verificar logs do backend
```bash
cd backend
# Procure por erros no console
```

#### 3. Verificar logs do frontend
- Abra o DevTools do navegador (F12)
- Vá para a aba "Console"
- Procure por erros em vermelho
- Vá para a aba "Network" e veja quais requisições estão falhando

#### 4. Limpar cache e storage
```javascript
// No console do navegador:
localStorage.clear();
sessionStorage.clear();
location.reload();
```

### Soluções Implementadas

✅ **ErrorBoundary**: Captura erros de renderização do React
✅ **Melhor tratamento de erros nos hooks**: useBranding e useUserRole
✅ **Logs detalhados**: Interceptor do axios com logs de erro
✅ **Verificações de token**: Antes de fazer chamadas à API
✅ **Loading states**: Componente de loading para melhor UX

### Como Testar

1. **Iniciar o backend**:
```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

2. **Iniciar o frontend**:
```bash
cd frontend
npm run dev
```

3. **Acessar**: http://localhost:5173

### Erros Específicos

#### Erro: "Network Error"
- Backend não está rodando
- Porta 8000 não está acessível
- Firewall bloqueando conexão

#### Erro: "401 Unauthorized"
- Token expirado ou inválido
- Limpe o localStorage e faça login novamente

#### Erro: "404 Not Found"
- Endpoint não existe no backend
- Verifique a URL da requisição

#### Erro: "500 Internal Server Error"
- Erro no backend
- Verifique os logs do backend
- Pode ser erro de banco de dados ou lógica de negócio

### Contato

Se o problema persistir:
1. Capture os logs do backend
2. Capture os logs do console do navegador
3. Capture a aba Network do DevTools
4. Entre em contato com o suporte técnico
