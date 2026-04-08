"""Use cases do módulo Contratos."""
from decimal import Decimal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.domain.entities import User
from src.contratos.application.dtos import (
    AtualizarContratoRequest,
    ContratoListResponse,
    ContratoResponse,
    CriarContratoRequest,
)
from src.contratos.domain.entities import Contrato, StatusContrato
from src.contratos.domain.repositories import ContratoRepository
from src.propostas.domain.repositories import PropostaRepository
from src.shared.exceptions import ConflictError, NotFoundError
from src.tenant.domain.repositories import TenantRepository


class CriarContratoUseCase:
    def __init__(
        self,
        contrato_repo: ContratoRepository,
        proposta_repo: PropostaRepository,
        tenant_repo: TenantRepository,
    ):
        self.contrato_repo = contrato_repo
        self.proposta_repo = proposta_repo
        self.tenant_repo = tenant_repo

    async def execute(
        self, dto: CriarContratoRequest, tenant_id: UUID, user: User
    ) -> ContratoResponse:
        proposta = await self.proposta_repo.get_by_id(dto.proposta_id, tenant_id)
        if not proposta:
            raise NotFoundError("Proposta não encontrada")

        existente = await self.contrato_repo.get_by_proposta(dto.proposta_id, tenant_id)
        if existente:
            raise ConflictError("Já existe um contrato para esta proposta")

        tenant = await self.tenant_repo.get_by_id(tenant_id)
        if not tenant:
            raise NotFoundError("Tenant não encontrado")

        numero = await self.contrato_repo.next_numero(tenant_id)

        valor_parcela = (
            proposta.valor_parcela
            if proposta.numero_parcelas > 0
            else Decimal("0")
        )

        contrato = Contrato(
            tenant_id=tenant_id,
            proposta_id=dto.proposta_id,
            cliente_id=proposta.cliente_id,
            vendedor_id=proposta.vendedor_id,
            numero=numero,
            # Dados do cliente
            cliente_nome=proposta.cliente_nome,
            cliente_cpf_cnpj=proposta.cliente_cpf_cnpj,
            cliente_endereco=proposta.cliente_endereco,
            cliente_cidade=proposta.cliente_cidade,
            cliente_estado=proposta.cliente_estado,
            cliente_cep=proposta.cliente_cep,
            # Dados da empresa (do Tenant)
            empresa_razao_social=tenant.razao_social,
            empresa_cnpj=tenant.cnpj,
            empresa_endereco=getattr(tenant, "endereco", ""),
            empresa_cidade=getattr(tenant, "cidade", ""),
            empresa_cep=getattr(tenant, "cep", ""),
            empresa_representante_nome=getattr(tenant, "representante_nome", ""),
            empresa_representante_cpf=getattr(tenant, "representante_cpf", ""),
            empresa_representante_rg=getattr(tenant, "representante_rg", ""),
            # Dados bancários
            banco_nome=getattr(tenant, "banco_nome", ""),
            banco_agencia=getattr(tenant, "banco_agencia", ""),
            banco_conta=getattr(tenant, "banco_conta", ""),
            banco_titular=getattr(tenant, "banco_titular", ""),
            # Equipamentos / Valores
            potencia_total_kwp=proposta.potencia_sistema_kwp,
            quantidade_paineis=proposta.quantidade_paineis,
            valor_total=proposta.valor_final,
            numero_parcelas=proposta.numero_parcelas,
            valor_parcela=valor_parcela,
            # Termos
            prazo_execucao_dias=dto.prazo_execucao_dias,
            garantia_instalacao_meses=dto.garantia_instalacao_meses,
            foro_comarca=dto.foro_comarca,
        )

        criado = await self.contrato_repo.create(contrato)
        return ContratoResponse.model_validate(criado)


class ListarContratosUseCase:
    def __init__(self, contrato_repo: ContratoRepository):
        self.contrato_repo = contrato_repo

    async def execute(
        self,
        tenant_id: UUID,
        cliente_id: UUID | None = None,
        status: str | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> ContratoListResponse:
        items = await self.contrato_repo.list_by_tenant(tenant_id, cliente_id, status, offset, limit)
        total = await self.contrato_repo.count_by_tenant(tenant_id, cliente_id, status)
        return ContratoListResponse(
            items=[ContratoResponse.model_validate(c) for c in items],
            total=total,
            offset=offset,
            limit=limit,
        )


class ObterContratoUseCase:
    def __init__(self, contrato_repo: ContratoRepository):
        self.contrato_repo = contrato_repo

    async def execute(self, contrato_id: UUID, tenant_id: UUID) -> ContratoResponse:
        contrato = await self.contrato_repo.get_by_id(contrato_id, tenant_id)
        if not contrato:
            raise NotFoundError("Contrato não encontrado")
        return ContratoResponse.model_validate(contrato)


class AtualizarContratoUseCase:
    def __init__(self, contrato_repo: ContratoRepository, session: AsyncSession | None = None):
        self.contrato_repo = contrato_repo
        self.session = session

    async def execute(
        self, contrato_id: UUID, tenant_id: UUID, dto: AtualizarContratoRequest
    ) -> ContratoResponse:
        contrato = await self.contrato_repo.get_by_id(contrato_id, tenant_id)
        if not contrato:
            raise NotFoundError("Contrato não encontrado")

        status_anterior = contrato.status

        if dto.prazo_execucao_dias is not None:
            contrato.prazo_execucao_dias = dto.prazo_execucao_dias
        if dto.garantia_instalacao_meses is not None:
            contrato.garantia_instalacao_meses = dto.garantia_instalacao_meses
        if dto.foro_comarca is not None:
            contrato.foro_comarca = dto.foro_comarca
        if dto.status is not None:
            contrato.status = StatusContrato(dto.status)

        atualizado = await self.contrato_repo.update(contrato)

        # Comissão automática ao assinar contrato
        novo_status = StatusContrato(dto.status) if dto.status else status_anterior
        if (
            novo_status == StatusContrato.ASSINADO
            and status_anterior != StatusContrato.ASSINADO
            and atualizado.vendedor_id
            and self.session
        ):
            from src.vendedores.application.use_cases import RegistrarVendaUseCase
            await RegistrarVendaUseCase(self.session).execute(
                tenant_id=tenant_id,
                contrato_id=atualizado.id,
                vendedor_id=atualizado.vendedor_id,
                valor_venda=atualizado.valor_total,
            )

        return ContratoResponse.model_validate(atualizado)
