# API Endpoints - SunOps SaaS MVP

Base URL: `/api/v1`

## Auth
| Metodo | Endpoint | Descricao | Auth |
|--------|----------|-----------|------|
| POST | `/auth/login` | Login (retorna access + refresh JWT) | Nao |
| POST | `/auth/refresh` | Renovar access token | Refresh token |
| POST | `/auth/logout` | Invalidar refresh token | Sim |
| GET | `/auth/me` | Dados do usuario logado | Sim |

## Tenants
| Metodo | Endpoint | Descricao | Auth |
|--------|----------|-----------|------|
| POST | `/tenants` | Criar tenant (signup) | Nao |
| GET | `/tenants/me` | Dados do tenant atual | Sim |
| PUT | `/tenants/me` | Atualizar tenant | Admin |
| PUT | `/tenants/me/branding` | Atualizar logo/cores | Admin |

## Clientes
| Metodo | Endpoint | Descricao | Auth |
|--------|----------|-----------|------|
| GET | `/clientes` | Listar clientes (paginado, filtrado) | Sim |
| POST | `/clientes` | Criar cliente | Sim |
| GET | `/clientes/{id}` | Detalhe do cliente | Sim |
| PUT | `/clientes/{id}` | Atualizar cliente | Sim |
| DELETE | `/clientes/{id}` | Remover cliente | Admin |

## Equipamentos
| Metodo | Endpoint | Descricao | Auth |
|--------|----------|-----------|------|
| GET | `/paineis` | Listar paineis (cached 15min) | Sim |
| POST | `/paineis` | Criar painel | Admin |
| GET | `/inversores` | Listar inversores (cached 15min) | Sim |
| POST | `/inversores` | Criar inversor | Admin |
| POST | `/equipamentos/validar-dimensionamento` | Validar painel vs inversor | Sim |

## Premissas
| Metodo | Endpoint | Descricao | Auth |
|--------|----------|-----------|------|
| GET | `/premissas/ativa` | Premissas ativas do tenant | Sim |
| PUT | `/premissas/{id}` | Atualizar premissas | Admin |

## Orcamentos
| Metodo | Endpoint | Descricao | Auth |
|--------|----------|-----------|------|
| GET | `/orcamentos` | Listar orcamentos (paginado) | Sim |
| POST | `/orcamentos` | Criar orcamento (calcula automatico) | Sim |
| GET | `/orcamentos/{id}` | Detalhe com breakdown completo | Sim |
| PUT | `/orcamentos/{id}` | Atualizar orcamento (recalcula) | Sim |
| DELETE | `/orcamentos/{id}` | Remover orcamento | Admin |
| POST | `/orcamentos/{id}/converter-proposta` | Converter em proposta | Sim |
| POST | `/orcamentos/{id}/gerar-pdf` | Gerar PDF dimensionamento | Sim |
| POST | `/orcamentos/calcular-material-eletrico` | Lookup por potencia inversor | Sim |

## Deslocamento
| Metodo | Endpoint | Descricao | Auth |
|--------|----------|-----------|------|
| POST | `/deslocamento/calcular` | Calcular custo de deslocamento | Sim |

## Propostas
| Metodo | Endpoint | Descricao | Auth |
|--------|----------|-----------|------|
| GET | `/propostas` | Listar propostas | Sim |
| GET | `/propostas/{id}` | Detalhe da proposta | Sim |
| POST | `/propostas/{id}/aceitar` | Aceitar proposta | Sim |
| POST | `/propostas/{id}/recusar` | Recusar proposta | Sim |
| POST | `/propostas/{id}/gerar-pdf` | Gerar PDF da proposta | Sim |

## Contratos
| Metodo | Endpoint | Descricao | Auth |
|--------|----------|-----------|------|
| GET | `/contratos` | Listar contratos | Sim |
| GET | `/contratos/{id}` | Detalhe do contrato | Sim |
| PUT | `/contratos/{id}` | Atualizar contrato | Sim |
| GET | `/contratos/{id}/gerar-docx` | Download DOCX | Sim |
| GET | `/contratos/{id}/gerar-pdf` | Download PDF | Sim |

## Templates
| Metodo | Endpoint | Descricao | Auth |
|--------|----------|-----------|------|
| GET | `/templates` | Listar templates do tenant | Admin |
| POST | `/templates` | Upload template DOCX | Admin |
| PUT | `/templates/{id}/ativar` | Ativar template | Admin |
| DELETE | `/templates/{id}` | Remover template | Admin |

## Vendedores
| Metodo | Endpoint | Descricao | Auth |
|--------|----------|-----------|------|
| GET | `/vendedores` | Listar vendedores | Admin |
| POST | `/vendedores` | Criar vendedor | Admin |
| PUT | `/vendedores/{id}` | Atualizar vendedor | Admin |
| POST | `/vendedores/{id}/bloquear` | Bloquear/desbloquear | Admin |
| POST | `/vendedores/{id}/resetar-senha` | Resetar senha | Admin |
| GET | `/vendedores/{id}/resumo` | Stats do vendedor | Sim |
| GET | `/vendedores/{id}/historico-vendas` | Historico de comissoes | Sim |

## Dashboard
| Metodo | Endpoint | Descricao | Auth |
|--------|----------|-----------|------|
| GET | `/dashboard/resumo` | KPIs do tenant (cached 5min) | Sim |

## Health
| Metodo | Endpoint | Descricao | Auth |
|--------|----------|-----------|------|
| GET | `/health` | Health check (db + redis) | Nao |
