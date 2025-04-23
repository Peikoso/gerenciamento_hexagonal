from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from gerenciamento_hexagonal.application.servicesSQLite import RelatorioSQLiteServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import WrappedRelatorioResponse
from gerenciamento_hexagonal.infrastructure.repositories.SQLiterepository import RelatorioSQLiteRepository

router = APIRouter()


def get_relatorio_sqlite_service() -> RelatorioSQLiteServices:
    relatorio_repository = RelatorioSQLiteRepository()
    return RelatorioSQLiteServices(relatorio_repository)


@router.get('/{gerenciamento_proposta_id}', response_model=WrappedRelatorioResponse)
async def get_relatorio(gerenciamento_proposta_id: int, service: RelatorioSQLiteServices = Depends(get_relatorio_sqlite_service)):
    try:
        relatorio = await service.get_relatorio(gerenciamento_proposta_id)

        return {'gerenciamento_proposta': relatorio}

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
