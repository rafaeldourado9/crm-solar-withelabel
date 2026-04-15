from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import traceback
import logging

from src.orcamentos.domain.exceptions import OrcamentoError
from src.shared.exceptions import (
    ConflictError,
    DomainError,
    ForbiddenError,
    NotFoundError,
    ValidationError,
)

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(title="SunOps SaaS", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _register_exception_handlers(app)
    _register_routes(app)

    return app


def _register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": exc.message})

    @app.exception_handler(ForbiddenError)
    async def forbidden_handler(request: Request, exc: ForbiddenError) -> JSONResponse:
        return JSONResponse(status_code=403, content={"detail": exc.message})

    @app.exception_handler(ValidationError)
    async def validation_handler(request: Request, exc: ValidationError) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": exc.message})

    @app.exception_handler(ConflictError)
    async def conflict_handler(request: Request, exc: ConflictError) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": exc.message})

    @app.exception_handler(DomainError)
    async def domain_handler(request: Request, exc: DomainError) -> JSONResponse:
        return JSONResponse(status_code=400, content={"detail": exc.message})

    @app.exception_handler(OrcamentoError)
    async def orcamento_handler(request: Request, exc: OrcamentoError) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": exc.message})

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(f"Erro não tratado: {exc}")
        logger.error(f"URL: {request.url}")
        logger.error(f"Método: {request.method}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Erro interno do servidor",
                "error": str(exc),
                "type": type(exc).__name__
            }
        )


def _register_routes(app: FastAPI) -> None:
    from src.auth.infrastructure.api import router as auth_router
    from src.clientes.infrastructure.api import router as clientes_router
    from src.contratos.infrastructure.api import router as contratos_router
    from src.dashboard.infrastructure.api import router as dashboard_router
    from src.deslocamento.infrastructure.api import router as deslocamento_router
    from src.equipamentos.infrastructure.api import router as equipamentos_router
    from src.orcamentos.infrastructure.api import router as orcamentos_router
    from src.premissas.infrastructure.api import router as premissas_router
    from src.propostas.infrastructure.api import router as propostas_router
    from src.templates.infrastructure.api import router as templates_router
    from src.tenant.infrastructure.api import router as tenant_router
    from src.vendedores.infrastructure.api import router as vendedores_router

    app.include_router(auth_router)
    app.include_router(clientes_router)
    app.include_router(contratos_router)
    app.include_router(dashboard_router)
    app.include_router(deslocamento_router)
    app.include_router(equipamentos_router)
    app.include_router(orcamentos_router)
    app.include_router(premissas_router)
    app.include_router(propostas_router)
    app.include_router(templates_router)
    app.include_router(tenant_router)
    app.include_router(vendedores_router)

    @app.get("/api/v1/health")
    async def health_check() -> dict[str, str]:
        return {"status": "healthy", "service": "sunops-saas"}


app = create_app()
