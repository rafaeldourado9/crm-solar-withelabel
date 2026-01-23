# Arquitetura do Sistema

## Visão Geral

O CRM Solar segue uma arquitetura de **3 camadas** com separação clara de responsabilidades:

```
┌─────────────────────────────────────────┐
│           FRONTEND (React)              │
│  - Componentes UI                       │
│  - Gerenciamento de Estado              │
│  - Integração com API                   │
└─────────────────────────────────────────┘
                  ↓ HTTP/REST
┌─────────────────────────────────────────┐
│        BACKEND (Django REST)            │
│  ┌───────────────────────────────────┐  │
│  │  Views (Controllers)              │  │
│  └───────────────────────────────────┘  │
│  ┌───────────────────────────────────┐  │
│  │  Services (Business Logic)        │  │
│  └───────────────────────────────────┘  │
│  ┌───────────────────────────────────┐  │
│  │  Models (Data Layer)              │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
                  ↓ ORM
┌─────────────────────────────────────────┐
│         DATABASE (PostgreSQL)           │
└─────────────────────────────────────────┘
```

## Decisões Arquiteturais

### 1. Service Layer Pattern

**Decisão:** Criar camada de serviços separada das views.

**Motivação:**
- Lógica de negócio complexa (cálculos de engenharia)
- Reutilização de código
- Facilita testes unitários
- Mantém views limpas

**Exemplo:**
```python
# apps/orcamentos/services.py
class SolarCalculator:
    def calcular_dimensionamento(self, consumo, painel_id):
        # Lógica complexa aqui
        pass
```

### 2. Token Authentication

**Decisão:** Usar Token Auth ao invés de JWT.

**Motivação:**
- Simplicidade para MVP
- Suporte nativo do DRF
- Suficiente para aplicação interna
- Fácil implementação

**Trade-offs:**
- Não tem expiração automática
- Requer consulta ao banco
- Menos features que JWT

### 3. Singleton Pattern para Premissas

**Decisão:** Apenas uma premissa ativa por vez.

**Motivação:**
- Evita inconsistências nos cálculos
- Simplifica lógica de negócio
- Histórico mantido (soft delete)

**Implementação:**
```python
@classmethod
def get_ativa(cls):
    return cls.objects.filter(ativo=True).first() or cls.objects.create()
```

### 4. Cálculo Client-Side + Server-Side

**Decisão:** Cálculos iniciais no servidor, ajustes no cliente.

**Motivação:**
- Servidor: Fonte única de verdade
- Cliente: Feedback imediato ao usuário
- Melhor UX sem latência

**Fluxo:**
1. Usuário insere consumo → API calcula tudo
2. Usuário ajusta painéis → Recálculo local
3. Salvar → Validação no servidor

### 5. Modular App Structure

**Decisão:** Apps Django separados por domínio.

**Motivação:**
- Baixo acoplamento
- Alta coesão
- Facilita manutenção
- Permite deploy independente (futuro)

**Estrutura:**
```
apps/
├── clientes/      # Domínio: Gestão de clientes
├── orcamentos/    # Domínio: Orçamentos + Cálculos
├── premissas/     # Domínio: Configurações
└── dashboard/     # Domínio: Métricas
```

## Padrões de Código

### Backend

#### ViewSets
```python
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filtro por usuário
        pass
```

#### Services
```python
class SolarCalculator:
    def __init__(self):
        self.premissa = Premissa.get_ativa()
    
    def calcular_completo(self, **kwargs):
        # Orquestra múltiplos cálculos
        pass
```

### Frontend

#### Hooks Pattern
```javascript
const [data, setData] = useState([]);

useEffect(() => {
    loadData();
}, []);
```

#### Service Layer
```javascript
// services/clientesService.js
export const clientesService = {
    getAll: (params) => api.get('/clientes/', { params }),
    create: (data) => api.post('/clientes/', data)
};
```

## Segurança

### Autenticação
- Token obrigatório em todas as rotas privadas
- Logout automático em 401
- Token no localStorage (considerar httpOnly cookie)

### Autorização
- Usuários comuns: apenas seus dados
- Admin: acesso total
- Validação no backend (nunca confiar no frontend)

### CORS
- Configurado para domínios específicos
- Desenvolvimento: localhost permitido

## Performance

### Backend
- Paginação padrão: 50 itens
- Índices em campos de busca
- Select related para evitar N+1

### Frontend
- Lazy loading de componentes
- Debounce em buscas
- Cache de premissas

## Escalabilidade

### Horizontal
- Backend stateless (pronto para múltiplas instâncias)
- Token no banco (considerar Redis)

### Vertical
- PostgreSQL suporta alto volume
- Índices otimizados

## Monitoramento

### Logs
- Django logging configurado
- Erros capturados

### Métricas
- Dashboard com KPIs
- Histórico de ações

## Próximos Passos

1. **Cache:** Implementar Redis para tokens e premissas
2. **Queue:** Celery para geração de PDFs
3. **CDN:** Servir assets estáticos
4. **Monitoring:** Sentry para erros
5. **CI/CD:** GitHub Actions
