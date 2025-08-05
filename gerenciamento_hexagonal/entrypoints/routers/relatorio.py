from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from gerenciamento_hexagonal.application.dependencies import get_relatorio_service
from gerenciamento_hexagonal.application.services.relatorio import RelatorioServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import RelatorioDTO, RelatorioUpdateDTO, WrappedRelatorioResponse

router = APIRouter()


@router.get('/{gerenciamento_proposta_id}', response_model=WrappedRelatorioResponse)
async def get_relatorio(gerenciamento_proposta_id: int, service: RelatorioServices = Depends(get_relatorio_service)):
    try:
        relatorio = await service.get_relatorio(gerenciamento_proposta_id)

        return {'gerenciamento_proposta': relatorio}

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.post('/')
async def create_relatorio(relatorio: RelatorioDTO, service: RelatorioServices = Depends(get_relatorio_service)):
    relatorio = await service.create_relatorio(relatorio)

    return relatorio


@router.put('/{gerenciamento_proposta_id}')
async def update_relatorio(gerenciamento_proposta_id: int, relatorio: RelatorioUpdateDTO, service: RelatorioServices = Depends(get_relatorio_service)):
    try:
        relatorio = await service.update_relatorio(relatorio, gerenciamento_proposta_id)

        return relatorio

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))