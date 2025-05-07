from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from gerenciamento_hexagonal.application.services import RelatorioServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import WrappedRelatorioResponse
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy_repository import RelatorioRepository

router = APIRouter()


def get_relatorio_service() -> RelatorioServices:
    relatorio_repository = RelatorioRepository()
    return RelatorioServices(relatorio_repository)


@router.get('/{gerenciamento_proposta_id}', response_model=WrappedRelatorioResponse)
async def get_relatorio(gerenciamento_proposta_id: int, service: RelatorioServices = Depends(get_relatorio_service)):
    try:
        relatorio = await service.get_relatorio(gerenciamento_proposta_id)

        return {'gerenciamento_proposta': relatorio}

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
