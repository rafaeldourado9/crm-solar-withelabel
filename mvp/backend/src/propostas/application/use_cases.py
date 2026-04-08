"""Use cases do módulo Propostas."""
from uuid import UUID

from src.auth.domain.entities import User
from src.clientes.domain.repositories import ClienteRepository
from src.orcamentos.domain.repositories import OrcamentoRepository
from src.propostas.application.dtos import (
    AtualizarPropostaRequest,
    CriarPropostaRequest,
    PropostaListResponse,
    PropostaResponse,
)
from src.propostas.domain.entities import Proposta
from src.propostas.domain.repositories import PropostaRepository
from src.shared.exceptions import ForbiddenError, NotFoundError


class CriarPropostaUseCase:
    def __init__(
        self,
        proposta_repo: PropostaRepository,
        orcamento_repo: OrcamentoRepository,
        cliente_repo: ClienteRepository,
    ):
        self.proposta_repo = proposta_repo
        self.orcamento_repo = orcamento_repo
        self.cliente_repo = cliente_repo

    async def execute(
        self, dto: CriarPropostaRequest, tenant_id: UUID, user: User
    ) -> PropostaResponse:
        orcamento = await self.orcamento_repo.get_by_id(dto.orcamento_id, tenant_id)
        if not orcamento:
            raise NotFoundError("Orçamento não encontrado")

        cliente = await self.cliente_repo.get_by_id(orcamento.cliente_id, tenant_id)
        if not cliente:
            raise NotFoundError("Cliente não encontrado")

        numero = await self.proposta_repo.next_numero(tenant_id)

        proposta = Proposta(
            tenant_id=tenant_id,
            orcamento_id=dto.orcamento_id,
            cliente_id=orcamento.cliente_id,
            vendedor_id=orcamento.vendedor_id,
            numero=numero,
            # Snapshot do cliente
            cliente_nome=cliente.nome,
            cliente_cpf_cnpj=cliente.cpf_cnpj,
            cliente_email=cliente.email,
            cliente_telefone=cliente.telefone,
            cliente_endereco=cliente.endereco,
            cliente_cidade=cliente.cidade,
            cliente_estado=cliente.estado,
            cliente_cep=cliente.cep,
            # Dimensionamento
            potencia_sistema_kwp=orcamento.potencia_sistema_kwp,
            quantidade_paineis=orcamento.quantidade_paineis,
            painel_modelo=orcamento.painel_modelo,
            inversor_modelo=orcamento.inversor_modelo,
            geracao_mensal_kwh=orcamento.geracao_mensal_kwh,
            # Financeiro
            valor_final=orcamento.valor_final,
            forma_pagamento=orcamento.forma_pagamento,
            numero_parcelas=orcamento.numero_parcelas,
            valor_parcela=orcamento.valor_parcela,
            taxa_juros=orcamento.taxa_juros,
            data_validade=dto.data_validade,
            observacoes=dto.observacoes,
        )

        criada = await self.proposta_repo.create(proposta)
        return PropostaResponse.model_validate(criada)


class ListarPropostasUseCase:
    def __init__(self, proposta_repo: PropostaRepository):
        self.proposta_repo = proposta_repo

    async def execute(
        self,
        tenant_id: UUID,
        user: User,
        cliente_id: UUID | None = None,
        status: str | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> PropostaListResponse:
        items = await self.proposta_repo.list_by_tenant(
            tenant_id, cliente_id, status, offset, limit
        )
        total = await self.proposta_repo.count_by_tenant(tenant_id, cliente_id, status)
        return PropostaListResponse(
            items=[PropostaResponse.model_validate(p) for p in items],
            total=total,
            offset=offset,
            limit=limit,
        )


class ObterPropostaUseCase:
    def __init__(self, proposta_repo: PropostaRepository):
        self.proposta_repo = proposta_repo

    async def execute(self, proposta_id: UUID, tenant_id: UUID) -> PropostaResponse:
        proposta = await self.proposta_repo.get_by_id(proposta_id, tenant_id)
        if not proposta:
            raise NotFoundError("Proposta não encontrada")
        return PropostaResponse.model_validate(proposta)


class AceitarPropostaUseCase:
    def __init__(self, proposta_repo: PropostaRepository):
        self.proposta_repo = proposta_repo

    async def execute(self, proposta_id: UUID, tenant_id: UUID) -> PropostaResponse:
        proposta = await self.proposta_repo.get_by_id(proposta_id, tenant_id)
        if not proposta:
            raise NotFoundError("Proposta não encontrada")
        proposta.aceitar()
        atualizada = await self.proposta_repo.update(proposta)
        return PropostaResponse.model_validate(atualizada)


class RecusarPropostaUseCase:
    def __init__(self, proposta_repo: PropostaRepository):
        self.proposta_repo = proposta_repo

    async def execute(self, proposta_id: UUID, tenant_id: UUID) -> PropostaResponse:
        proposta = await self.proposta_repo.get_by_id(proposta_id, tenant_id)
        if not proposta:
            raise NotFoundError("Proposta não encontrada")
        proposta.recusar()
        atualizada = await self.proposta_repo.update(proposta)
        return PropostaResponse.model_validate(atualizada)
