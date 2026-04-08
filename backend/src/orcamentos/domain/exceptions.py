class OrcamentoError(Exception):
    def __init__(self, message: str = "Erro no orcamento"):
        self.message = message
        super().__init__(self.message)


class InversorExcedidoError(OrcamentoError):
    def __init__(self, potencia_paineis: int, potencia_maxima_inversor: int):
        msg = (
            f"Potencia dos paineis ({potencia_paineis}W) excede "
            f"capacidade do inversor ({potencia_maxima_inversor}W com overload)"
        )
        super().__init__(msg)
