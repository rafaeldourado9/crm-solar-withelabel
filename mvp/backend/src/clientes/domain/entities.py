from enum import StrEnum
from uuid import UUID

from pydantic import EmailStr, Field

from src.shared.base_entity import BaseEntity


class StatusCliente(StrEnum):
    ORCAMENTO = "orcamento"
    PROPOSTA = "proposta"
    CONTRATO = "contrato"


TRANSICOES_VALIDAS: dict[StatusCliente, list[StatusCliente]] = {
    StatusCliente.ORCAMENTO: [StatusCliente.PROPOSTA],
    StatusCliente.PROPOSTA: [StatusCliente.CONTRATO, StatusCliente.ORCAMENTO],
    StatusCliente.CONTRATO: [],
}


class Cliente(BaseEntity):
    tenant_id: UUID
    vendedor_id: UUID | None = None
    nome: str
    cpf_cnpj: str
    telefone: str = ""
    email: str = ""
    endereco: str = ""
    bairro: str = ""
    cidade: str = ""
    estado: str = Field(default="", max_length=2)
    cep: str = ""
    status: StatusCliente = StatusCliente.ORCAMENTO
    ativo: bool = True

    def pode_transicionar(self, novo_status: StatusCliente) -> bool:
        return novo_status in TRANSICOES_VALIDAS.get(self.status, [])

    def transicionar(self, novo_status: StatusCliente) -> None:
        if not self.pode_transicionar(novo_status):
            from src.shared.exceptions import ValidationError
            raise ValidationError(
                f"Transicao invalida: {self.status} -> {novo_status}"
            )
        self.status = novo_status
