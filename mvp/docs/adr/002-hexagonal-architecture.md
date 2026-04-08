# ADR-002: Arquitetura Hexagonal (Ports & Adapters)

## Status
Aceita

## Contexto
O projeto Django mistura logica de negocio com views, serializers e models.
O SolarCalculator esta no services.py mas depende diretamente do ORM.
Contratos tem dados hardcoded no model.

## Decisao
Adotar Arquitetura Hexagonal com 3 camadas claras:
- **Domain**: Entidades, Value Objects, Services (logica pura, zero dependencia)
- **Application**: Use Cases, DTOs (orquestracao)
- **Infrastructure**: SQLAlchemy models, FastAPI routers, adapters externos

## Consequencias

### Positivas
- Domain testavel sem banco de dados
- Troca de framework sem reescrever regras de negocio
- CC baixa (cada camada tem responsabilidade unica)
- Facilita TDD (domain services sao funcoes puras)

### Negativas
- Mais arquivos por modulo (3 camadas vs 1 views.py)
- Boilerplate de interfaces/protocols
- Curva de aprendizado para devs junior

### Trade-off
Complexidade estrutural maior, mas complexidade logica MUITO menor.
Cada funcao faz UMA coisa. CC < 5 garantido.
