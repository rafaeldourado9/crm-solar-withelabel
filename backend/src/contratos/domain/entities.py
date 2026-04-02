from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID

from src.shared.base_entity import TenantEntity


class StatusContrato(str, Enum):
    RASCUNHO = "rascunho"
    ASSINADO = "assinado"
    EM_EXECUCAO = "em_execucao"
    CONCLUIDO = "concluido"


class Contrato(TenantEntity):
    proposta_id: UUID
    cliente_id: UUID
    vendedor_id: UUID | None = None
    numero: str
    status: StatusContrato = StatusContrato.RASCUNHO

    # Dados do cliente
    cliente_nome: str
    cliente_cpf_cnpj: str
    cliente_endereco: str = ""
    cliente_bairro: str = ""
    cliente_cidade: str = ""
    cliente_estado: str = ""
    cliente_cep: str = ""

    # Dados da empresa (do Tenant — WhiteLabel)
    empresa_razao_social: str
    empresa_cnpj: str
    empresa_endereco: str = ""
    empresa_cidade: str = ""
    empresa_cep: str = ""
    empresa_representante_nome: str = ""
    empresa_representante_cpf: str = ""
    empresa_representante_rg: str = ""

    # Dados bancários (do Tenant)
    banco_nome: str = ""
    banco_agencia: str = ""
    banco_conta: str = ""
    banco_titular: str = ""

    # Equipamentos / Valores
    potencia_total_kwp: Decimal
    quantidade_paineis: int
    valor_total: Decimal
    numero_parcelas: int = 0
    valor_parcela: Decimal = Decimal("0")

    # Termos
    prazo_execucao_dias: int = 30
    garantia_instalacao_meses: int = 12
    foro_comarca: str = ""

    def assinar(self) -> None:
        if self.status != StatusContrato.RASCUNHO:
            raise ValueError("Contrato só pode ser assinado quando em rascunho")
        self.status = StatusContrato.ASSINADO
        self.updated_at = datetime.utcnow()

    def iniciar_execucao(self) -> None:
        if self.status != StatusContrato.ASSINADO:
            raise ValueError("Contrato deve estar assinado para iniciar execução")
        self.status = StatusContrato.EM_EXECUCAO
        self.updated_at = datetime.utcnow()

    def concluir(self) -> None:
        if self.status != StatusContrato.EM_EXECUCAO:
            raise ValueError("Contrato deve estar em execução para ser concluído")
        self.status = StatusContrato.CONCLUIDO
        self.updated_at = datetime.utcnow()
