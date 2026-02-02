# 🔄 ATUALIZAR PARA GERAR PDF

## ✅ Mudanças Implementadas

1. **Dockerfile atualizado** - Adicionado LibreOffice
2. **View atualizada** - Conversão DOCX → PDF automática
3. **Todas as variáveis** - Aliases adicionados

## 🚀 Como Atualizar

Execute estes comandos:

```bash
# 1. Parar os containers
docker-compose down

# 2. Reconstruir o backend (vai demorar ~5 minutos)
docker-compose build --no-cache backend

# 3. Subir novamente
docker-compose up -d

# 4. Aguardar containers iniciarem
docker-compose ps
```

## ⏱️ Tempo Estimado

- Download LibreOffice: ~3 minutos
- Build da imagem: ~2 minutos
- **Total: ~5 minutos**

## ✅ Após Atualizar

1. Acesse: http://localhost:5173/orcamentos
2. Clique em um orçamento
3. Clique em **"Gerar PDF"**
4. ✅ Agora baixa em **PDF**!

## 📊 Tamanho da Imagem

- **Antes:** ~200MB
- **Depois:** ~700MB (LibreOffice)

## 🔍 Verificar se Funcionou

```bash
# Ver logs do backend
docker-compose logs backend | tail -50

# Testar LibreOffice
docker-compose exec backend libreoffice --version
```

Deve mostrar: `LibreOffice 7.x.x.x`

## ⚠️ Problemas?

### Erro: "libreoffice: command not found"
- Execute: `docker-compose build --no-cache backend`
- Aguarde o build completo

### PDF não gera
- Verifique os logs: `docker-compose logs backend`
- Se falhar, retorna DOCX automaticamente

### Build muito lento
- É normal! LibreOffice é grande
- Primeira vez demora mais
- Próximas vezes usa cache

## 🎉 Resultado

Agora ao clicar em "Gerar PDF":
- ✅ Gera DOCX com dados preenchidos
- ✅ Converte automaticamente para PDF
- ✅ Baixa arquivo PDF
- ✅ Se falhar, retorna DOCX (fallback)
