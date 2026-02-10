-- Criar tabelas do módulo Suporte IA

-- Tabela de Agentes IA
CREATE TABLE IF NOT EXISTS agentes_ia (
    id BIGSERIAL PRIMARY KEY,
    vendedor_id INTEGER NOT NULL UNIQUE REFERENCES auth_user(id) ON DELETE CASCADE,
    nome_agente VARCHAR(100) NOT NULL DEFAULT 'Solar Bot',
    criado_em TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    atualizado_em TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Tabela de Conversas IA
CREATE TABLE IF NOT EXISTS conversas_ia (
    id BIGSERIAL PRIMARY KEY,
    vendedor_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    mensagem TEXT NOT NULL,
    resposta TEXT NOT NULL,
    tipo_acao VARCHAR(50),
    metadata JSONB DEFAULT '{}',
    criado_em TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_conversas_ia_vendedor ON conversas_ia(vendedor_id);
CREATE INDEX IF NOT EXISTS idx_conversas_ia_criado_em ON conversas_ia(criado_em DESC);
CREATE INDEX IF NOT EXISTS idx_agentes_ia_vendedor ON agentes_ia(vendedor_id);

-- Comentários
COMMENT ON TABLE agentes_ia IS 'Configurações personalizadas do agente IA por vendedor';
COMMENT ON TABLE conversas_ia IS 'Histórico de conversas com o agente IA';
