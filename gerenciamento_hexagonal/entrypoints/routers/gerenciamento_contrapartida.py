from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from gerenciamento_hexagonal.application.dependencies import get_gerenciamento_contrapartida_service
from gerenciamento_hexagonal.application.services.gerenciamento.contrapartida import GerenciamentoContrapartidaServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoContrapartida
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import GerenciamentoContrapartidaDTO

router = APIRouter()


Service = Annotated[GerenciamentoContrapartidaServices, Depends(get_gerenciamento_contrapartida_service)]


@router.get('/', response_model=list[GerenciamentoContrapartida])
async def get_gerenciamento_contrapartidas(service: Service):
    gerenciamento_contrapartida = await service.get_gerenciamento_contrapartida()

    return gerenciamento_contrapartida


@router.get('/{gerenciamento_contrapartida_id}', response_model=GerenciamentoContrapartida)
async def get_gerenciamento_contrapartida_by_id(gerenciamento_contrapartida_id: int, service: Service):
    try:
        gerenciamento_contrapartida = await service.get_gerenciamento_contrapartida_by_id(gerenciamento_contrapartida_id)

        return gerenciamento_contrapartida

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.post('/{gerenciamento_proposta_id}', response_model=GerenciamentoContrapartida)
async def create_gerenciamento_contrapartida(gerenciamento_proposta_id: int, gerenciamento_contrapartida: GerenciamentoContrapartidaDTO, service: Service):
    try:
        gerenciamento_contrapartida = await service.create_gerenciamento_contrapartida(gerenciamento_proposta_id, gerenciamento_contrapartida)

        return gerenciamento_contrapartida

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.put('/{gerenciamento_contrapartida_id}', response_model=GerenciamentoContrapartida)
async def update_gerenciamento_contrapartida(gerenciamento_contrapartida_id: int, gerenciamento_contrapartida: GerenciamentoContrapartidaDTO, service: Service):
    try:
        gerenciamento_contrapartida = await service.update_gerenciamento_contrapartida(gerenciamento_contrapartida_id, gerenciamento_contrapartida)

        return gerenciamento_contrapartida

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete('/{gerenciamento_contrapartida_id}')
async def delete_gerenciamento_contrapartida(gerenciamento_contrapartida_id: int, service: Service):
    try:
        result = await service.delete_gerenciamento_contrapartida(gerenciamento_contrapartida_id)

        return result

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
