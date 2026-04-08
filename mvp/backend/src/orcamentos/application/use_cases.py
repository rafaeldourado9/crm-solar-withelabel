from decimal import Decimal
from uuid import UUID

from src.clientes.domain.repositories import ClienteRepository
from src.equipamentos.domain.repositories import InversorRepository, PainelRepository
from src.orcamentos.application.dtos import (
    AtualizarOrcamentoRequest,
    CriarOrcamentoRequest,
)
from src.orcamentos.domain.entities import Orcamento, StatusOrcamento
from src.orcamentos.domain.repositories import OrcamentoRepository
from src.orcamentos.domain.services import SolarCalculatorService
from src.orcamentos.domain.value_objects import (
    CustoBreakdown,
    FaixaMaterialEletrico,
    FormaPagamento,
    MargemConfig,
)
from src.premissas.domain.repositories import PremissaRepository
from src.shared.exceptions import ForbiddenError, NotFoundError, ValidationError


class CriarOrcamentoUseCase:
    def __init__(
        self,
        orcamento_repo: OrcamentoRepository,
        premissa_repo: PremissaRepository,
        painel_repo: PainelRepository,
        inversor_repo: InversorRepository,
        cliente_repo: ClienteRepository,
    ):
        self.orcamento_repo = orcamento_repo
        self.premissa_repo = premissa_repo
        self.painel_repo = painel_repo
        self.inversor_repo = inversor_repo
        self.cliente_repo = cliente_repo

    async def execute(
        self, dto: CriarOrcamentoRequest, tenant_id: UUID, user_role: str, user_id: UUID
    ) -> Orcamento:
        # Buscar dependencias
        cliente = await self.cliente_repo.get_by_id(dto.cliente_id, tenant_id)
        if not cliente:
            raise NotFoundError("Cliente", str(dto.cliente_id))
        if user_role != "admin" and cliente.vendedor_id != user_id:
            raise ForbiddenError("Voce nao tem acesso a este cliente")

        painel = await self.painel_repo.get_by_id(dto.painel_id, tenant_id)
        if not painel:
            raise NotFoundError("Painel", str(dto.painel_id))

        inversor = await self.inversor_repo.get_by_id(dto.inversor_id, tenant_id)
        if not inversor:
            raise NotFoundError("Inversor", str(dto.inversor_id))

        premissa = await self.premissa_repo.get_ativa(tenant_id)
        if not premissa:
            raise ValidationError("Premissas nao configuradas para este tenant")

        # Dimensionamento
        dimensionamento = SolarCalculatorService.dimensionar(
            consumo_mensal_kwh=dto.consumo_mensal_kwh,
            painel_potencia_w=painel.potencia_w,
            hsp=premissa.hsp_padrao,
            perda=premissa.perda_padrao,
        )

        # Validar inversor
        SolarCalculatorService.validar_inversor(
            quantidade_paineis=dimensionamento.quantidade_paineis,
            painel_potencia_w=painel.potencia_w,
            inversor_potencia_nominal_w=inversor.potencia_nominal_w,
            overload=premissa.overload_inversor,
        )

        # Material eletrico
        faixas = [
            FaixaMaterialEletrico(
                Decimal(str(f["potencia_min"])),
                Decimal(str(f["potencia_max"])),
                Decimal(str(f["valor"])),
            )
            for f in premissa.faixas_material_eletrico
        ]
        potencia_inversor_kwp = Decimal(str(inversor.potencia_nominal_w)) / 1000
        valor_material_eletrico = SolarCalculatorService.calcular_material_eletrico(
            potencia_inversor_kwp, faixas
        )

        # Itens adicionais
        valor_itens = sum(
            (item.valor for item in dto.itens_adicionais), Decimal("0")
        )

        # Subtotal
        valor_montagem = premissa.montagem_por_painel * dimensionamento.quantidade_paineis
        custos = CustoBreakdown(
            valor_kit=dto.valor_kit,
            montagem=valor_montagem,
            projeto=premissa.valor_projeto,
            estrutura=dto.valor_estrutura,
            material_eletrico=valor_material_eletrico,
            itens_adicionais=valor_itens,
            deslocamento=dto.custo_deslocamento,
        )
        subtotal = SolarCalculatorService.calcular_subtotal(custos)

        # Margens
        margem = MargemConfig(
            lucro=premissa.margem_lucro_percentual,
            comissao=premissa.comissao_percentual,
            imposto=premissa.imposto_percentual,
            desconto_avista=premissa.margem_desconto_avista_percentual,
        )
        valor_final = SolarCalculatorService.aplicar_margens(subtotal, margem)

        # Juros
        taxa = Decimal("0")
        if dto.forma_pagamento != "avista":
            taxa = premissa.taxas_maquininha.get(dto.forma_pagamento, Decimal("0"))
        forma = FormaPagamento(tipo=dto.forma_pagamento, taxa=taxa)
        valor_cobrado, valor_parcela = SolarCalculatorService.aplicar_juros(valor_final, forma)

        numero_parcelas = 0 if dto.forma_pagamento == "avista" else int(dto.forma_pagamento)

        # Economia
        economia = SolarCalculatorService.calcular_economia_25_anos(
            geracao_mensal_kwh=dimensionamento.geracao_mensal_kwh,
            tarifa_atual=premissa.tarifa_energia_atual,
            inflacao_energetica=premissa.inflacao_energetica_anual,
            perda_eficiencia=premissa.perda_eficiencia_anual,
        )

        itens_dict = [item.model_dump() for item in dto.itens_adicionais]
        economia_dict = [
            {
                "ano": e.ano,
                "tarifa": str(e.tarifa),
                "geracao_kwh": str(e.geracao_kwh),
                "economia": str(e.economia),
                "economia_acumulada": str(e.economia_acumulada),
            }
            for e in economia
        ]

        orcamento = Orcamento(
            tenant_id=tenant_id,
            cliente_id=dto.cliente_id,
            vendedor_id=cliente.vendedor_id,
            consumo_mensal_kwh=dto.consumo_mensal_kwh,
            painel_id=dto.painel_id,
            painel_modelo=painel.modelo,
            painel_potencia_w=painel.potencia_w,
            inversor_id=dto.inversor_id,
            inversor_modelo=inversor.modelo,
            inversor_potencia_nominal_w=inversor.potencia_nominal_w,
            quantidade_paineis=dimensionamento.quantidade_paineis,
            potencia_sistema_kwp=dimensionamento.potencia_sistema_kwp,
            geracao_mensal_kwh=dimensionamento.geracao_mensal_kwh,
            valor_kit=dto.valor_kit,
            valor_montagem=valor_montagem,
            valor_projeto=premissa.valor_projeto,
            valor_estrutura=dto.valor_estrutura,
            tipo_estrutura=dto.tipo_estrutura,
            valor_material_eletrico=valor_material_eletrico,
            custo_deslocamento=dto.custo_deslocamento,
            itens_adicionais=itens_dict,
            valor_itens_adicionais=valor_itens,
            subtotal=subtotal,
            margem_lucro=premissa.margem_lucro_percentual,
            comissao=premissa.comissao_percentual,
            imposto=premissa.imposto_percentual,
            margem_desconto_avista=premissa.margem_desconto_avista_percentual,
            valor_final=valor_final,
            forma_pagamento=dto.forma_pagamento,
            taxa_juros=taxa,
            valor_cobrado=valor_cobrado,
            numero_parcelas=numero_parcelas,
            valor_parcela=valor_parcela or Decimal("0"),
            economia_25_anos=economia_dict,
        )

        return await self.orcamento_repo.create(orcamento)


class ListarOrcamentosUseCase:
    def __init__(self, repo: OrcamentoRepository):
        self.repo = repo

    async def execute(
        self,
        tenant_id: UUID,
        user_role: str,
        user_id: UUID,
        cliente_id: UUID | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Orcamento], int]:
        vendedor_id = None if user_role == "admin" else user_id
        items = await self.repo.list_by_tenant(
            tenant_id, vendedor_id=vendedor_id, cliente_id=cliente_id, offset=offset, limit=limit
        )
        total = await self.repo.count_by_tenant(
            tenant_id, vendedor_id=vendedor_id, cliente_id=cliente_id
        )
        return items, total


class ObterOrcamentoUseCase:
    def __init__(self, repo: OrcamentoRepository):
        self.repo = repo

    async def execute(
        self, orcamento_id: UUID, tenant_id: UUID, user_role: str, user_id: UUID
    ) -> Orcamento:
        orcamento = await self.repo.get_by_id(orcamento_id, tenant_id)
        if not orcamento:
            raise NotFoundError("Orcamento", str(orcamento_id))
        if user_role != "admin" and orcamento.vendedor_id != user_id:
            raise ForbiddenError("Voce nao tem acesso a este orcamento")
        return orcamento


class AtualizarOrcamentoUseCase:
    def __init__(
        self,
        orcamento_repo: OrcamentoRepository,
        premissa_repo: PremissaRepository,
        painel_repo: PainelRepository,
        inversor_repo: InversorRepository,
    ):
        self.orcamento_repo = orcamento_repo
        self.premissa_repo = premissa_repo
        self.painel_repo = painel_repo
        self.inversor_repo = inversor_repo

    async def execute(
        self,
        orcamento_id: UUID,
        dto: AtualizarOrcamentoRequest,
        tenant_id: UUID,
        user_role: str,
        user_id: UUID,
    ) -> Orcamento:
        orcamento = await self.orcamento_repo.get_by_id(orcamento_id, tenant_id)
        if not orcamento:
            raise NotFoundError("Orcamento", str(orcamento_id))
        if user_role != "admin" and orcamento.vendedor_id != user_id:
            raise ForbiddenError("Voce nao tem acesso a este orcamento")

        premissa = await self.premissa_repo.get_ativa(tenant_id)
        if not premissa:
            raise ValidationError("Premissas nao configuradas")

        updates = dto.model_dump(exclude_unset=True)

        # Resolve painel/inversor if changed
        painel_id = updates.get("painel_id", orcamento.painel_id)
        inversor_id = updates.get("inversor_id", orcamento.inversor_id)

        painel = await self.painel_repo.get_by_id(painel_id, tenant_id)
        if not painel:
            raise NotFoundError("Painel", str(painel_id))
        inversor = await self.inversor_repo.get_by_id(inversor_id, tenant_id)
        if not inversor:
            raise NotFoundError("Inversor", str(inversor_id))

        consumo = updates.get("consumo_mensal_kwh", orcamento.consumo_mensal_kwh)
        valor_kit = updates.get("valor_kit", orcamento.valor_kit)
        valor_estrutura = updates.get("valor_estrutura", orcamento.valor_estrutura)
        tipo_estrutura = updates.get("tipo_estrutura", orcamento.tipo_estrutura)
        custo_deslocamento = updates.get("custo_deslocamento", orcamento.custo_deslocamento)
        forma_pagamento = updates.get("forma_pagamento", orcamento.forma_pagamento)

        # Recalcular
        dimensionamento = SolarCalculatorService.dimensionar(
            consumo_mensal_kwh=consumo,
            painel_potencia_w=painel.potencia_w,
            hsp=premissa.hsp_padrao,
            perda=premissa.perda_padrao,
        )

        SolarCalculatorService.validar_inversor(
            quantidade_paineis=dimensionamento.quantidade_paineis,
            painel_potencia_w=painel.potencia_w,
            inversor_potencia_nominal_w=inversor.potencia_nominal_w,
            overload=premissa.overload_inversor,
        )

        faixas = [
            FaixaMaterialEletrico(
                Decimal(str(f["potencia_min"])),
                Decimal(str(f["potencia_max"])),
                Decimal(str(f["valor"])),
            )
            for f in premissa.faixas_material_eletrico
        ]
        potencia_inversor_kwp = Decimal(str(inversor.potencia_nominal_w)) / 1000
        valor_material_eletrico = SolarCalculatorService.calcular_material_eletrico(
            potencia_inversor_kwp, faixas
        )

        itens_adicionais_raw = updates.get("itens_adicionais")
        if itens_adicionais_raw is not None:
            itens_dict = [i.model_dump() for i in itens_adicionais_raw]
            valor_itens = sum((i.valor for i in itens_adicionais_raw), Decimal("0"))
        else:
            itens_dict = orcamento.itens_adicionais
            valor_itens = orcamento.valor_itens_adicionais

        valor_montagem = premissa.montagem_por_painel * dimensionamento.quantidade_paineis
        custos = CustoBreakdown(
            valor_kit=valor_kit,
            montagem=valor_montagem,
            projeto=premissa.valor_projeto,
            estrutura=valor_estrutura,
            material_eletrico=valor_material_eletrico,
            itens_adicionais=valor_itens,
            deslocamento=custo_deslocamento,
        )
        subtotal = SolarCalculatorService.calcular_subtotal(custos)

        margem = MargemConfig(
            lucro=premissa.margem_lucro_percentual,
            comissao=premissa.comissao_percentual,
            imposto=premissa.imposto_percentual,
            desconto_avista=premissa.margem_desconto_avista_percentual,
        )
        valor_final = SolarCalculatorService.aplicar_margens(subtotal, margem)

        taxa = Decimal("0")
        if forma_pagamento != "avista":
            taxa = premissa.taxas_maquininha.get(forma_pagamento, Decimal("0"))
        forma = FormaPagamento(tipo=forma_pagamento, taxa=taxa)
        valor_cobrado, valor_parcela = SolarCalculatorService.aplicar_juros(valor_final, forma)
        numero_parcelas = 0 if forma_pagamento == "avista" else int(forma_pagamento)

        economia = SolarCalculatorService.calcular_economia_25_anos(
            geracao_mensal_kwh=dimensionamento.geracao_mensal_kwh,
            tarifa_atual=premissa.tarifa_energia_atual,
            inflacao_energetica=premissa.inflacao_energetica_anual,
            perda_eficiencia=premissa.perda_eficiencia_anual,
        )
        economia_dict = [
            {
                "ano": e.ano,
                "tarifa": str(e.tarifa),
                "geracao_kwh": str(e.geracao_kwh),
                "economia": str(e.economia),
                "economia_acumulada": str(e.economia_acumulada),
            }
            for e in economia
        ]

        # Update orcamento
        orcamento.consumo_mensal_kwh = consumo
        orcamento.painel_id = painel.id
        orcamento.painel_modelo = painel.modelo
        orcamento.painel_potencia_w = painel.potencia_w
        orcamento.inversor_id = inversor.id
        orcamento.inversor_modelo = inversor.modelo
        orcamento.inversor_potencia_nominal_w = inversor.potencia_nominal_w
        orcamento.quantidade_paineis = dimensionamento.quantidade_paineis
        orcamento.potencia_sistema_kwp = dimensionamento.potencia_sistema_kwp
        orcamento.geracao_mensal_kwh = dimensionamento.geracao_mensal_kwh
        orcamento.valor_kit = valor_kit
        orcamento.valor_montagem = valor_montagem
        orcamento.valor_projeto = premissa.valor_projeto
        orcamento.valor_estrutura = valor_estrutura
        orcamento.tipo_estrutura = tipo_estrutura
        orcamento.valor_material_eletrico = valor_material_eletrico
        orcamento.custo_deslocamento = custo_deslocamento
        orcamento.itens_adicionais = itens_dict
        orcamento.valor_itens_adicionais = valor_itens
        orcamento.subtotal = subtotal
        orcamento.margem_lucro = premissa.margem_lucro_percentual
        orcamento.comissao = premissa.comissao_percentual
        orcamento.imposto = premissa.imposto_percentual
        orcamento.margem_desconto_avista = premissa.margem_desconto_avista_percentual
        orcamento.valor_final = valor_final
        orcamento.forma_pagamento = forma_pagamento
        orcamento.taxa_juros = taxa
        orcamento.valor_cobrado = valor_cobrado
        orcamento.numero_parcelas = numero_parcelas
        orcamento.valor_parcela = valor_parcela or Decimal("0")
        orcamento.economia_25_anos = economia_dict

        return await self.orcamento_repo.update(orcamento)


class DeletarOrcamentoUseCase:
    def __init__(self, repo: OrcamentoRepository):
        self.repo = repo

    async def execute(self, orcamento_id: UUID, tenant_id: UUID) -> bool:
        orcamento = await self.repo.get_by_id(orcamento_id, tenant_id)
        if not orcamento:
            raise NotFoundError("Orcamento", str(orcamento_id))
        return await self.repo.delete(orcamento_id, tenant_id)
