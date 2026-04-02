# ADR-004: JWT com Access + Refresh Tokens

## Status
Aceita

## Contexto
Django atual usa Token auth sem expiracao. Tokens ficam no banco indefinidamente.
Vulnerabilidade: token roubado = acesso permanente.

## Decisao
JWT com par access/refresh token.

## Implementacao

- **Access Token**: 15min, contem user_id + tenant_id + role
- **Refresh Token**: 7 dias, rotativo (invalida anterior ao renovar)
- **Blacklist**: Redis para tokens revogados
- **Logout**: Invalida refresh token

## Consequencias

### Positivas
- Stateless (sem consulta ao banco por request)
- Expiracao automatica
- Tenant embutido no token (sem lookup extra)
- Refresh token rotativo previne replay attacks

### Negativas
- Access token nao pode ser revogado antes do expiry (15min de janela)
- Precisa de Redis para blacklist
