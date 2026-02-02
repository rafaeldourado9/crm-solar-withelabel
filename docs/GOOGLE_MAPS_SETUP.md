# Guia Rápido: Configurar Google Maps API

## 1. Obter API Key

1. Acesse: https://console.cloud.google.com/
2. Crie um projeto (ou selecione existente)
3. Vá em: **APIs & Services > Library**
4. Busque e habilite: **Distance Matrix API**
5. Vá em: **APIs & Services > Credentials**
6. Clique: **Create Credentials > API Key**
7. Copie a chave gerada

## 2. Configurar no Backend

Edite o arquivo `backend/.env`:

```bash
GOOGLE_MAPS_API_KEY=AIzaSyC...sua_chave_aqui
```

## 3. Reiniciar Backend

```bash
docker-compose restart backend
```

## 4. Testar

Crie um orçamento para um cliente em qualquer cidade. O sistema irá:
- ✅ Calcular distância via Google Maps
- ✅ Se falhar, usar tabela de distâncias (fallback)

## Custos

- **Grátis:** 40.000 requisições/mês
- **Custo:** $5 por 1.000 requisições adicionais

Para um CRM solar, isso é mais que suficiente!

## Sem API Key?

O sistema funciona normalmente usando a tabela de distâncias para cidades principais de MS.
