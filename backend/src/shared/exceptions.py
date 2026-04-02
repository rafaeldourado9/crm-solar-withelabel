class DomainError(Exception):
    def __init__(self, message: str = "Erro de dominio"):
        self.message = message
        super().__init__(self.message)


class NotFoundError(DomainError):
    def __init__(self, entity: str = "Recurso", identifier: str = ""):
        msg = f"{entity} nao encontrado"
        if identifier:
            msg = f"{entity} '{identifier}' nao encontrado"
        super().__init__(msg)


class ForbiddenError(DomainError):
    def __init__(self, message: str = "Acesso negado"):
        super().__init__(message)


class ValidationError(DomainError):
    def __init__(self, message: str = "Dados invalidos"):
        super().__init__(message)


class ConflictError(DomainError):
    def __init__(self, message: str = "Conflito de dados"):
        super().__init__(message)
