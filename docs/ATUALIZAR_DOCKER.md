# Instruções para Atualizar o Docker

## 🔄 Atualizar Backend para Suportar Conversão PDF

### Passo 1: Reconstruir o Container

```bash
# Parar os containers
docker-compose down

# Reconstruir o backend com as novas dependências
docker-compose build backend

# Subir novamente
docker-compose up -d
```

### Passo 2: Verificar se Funcionou

```bash
# Ver logs do backend
docker-compose logs -f backend
```

Procure por erros relacionados a `docx2pdf`.

## ⚠️ Nota sobre docx2pdf

A biblioteca `docx2pdf` funciona melhor no Windows. Se você estiver usando Docker no Linux/Mac, a conversão pode falhar.

**Neste caso, o sistema automaticamente retornará o arquivo DOCX em vez de PDF.**

## 🔧 Alternativa: Usar LibreOffice para Conversão

Se `docx2pdf` não funcionar no seu ambiente Docker, você pode usar LibreOffice:

### Atualizar Dockerfile

Adicione estas linhas no `backend/Dockerfile`:

```dockerfile
# Instalar LibreOffice para conversão DOCX → PDF
RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-writer \
    && rm -rf /var/lib/apt/lists/*
```

### Atualizar requirements.txt

Remova `docx2pdf` e o sistema usará LibreOffice automaticamente.

## ✅ Resultado Esperado

Após atualizar:

1. Acesse um orçamento
2. Clique em "Gerar PDF"
3. **Se conversão funcionar:** Baixa arquivo `.pdf`
4. **Se conversão falhar:** Baixa arquivo `.docx` (funcional)

Ambos os formatos funcionam perfeitamente!
