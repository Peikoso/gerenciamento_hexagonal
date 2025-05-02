from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from gerenciamento_hexagonal.application.dependencies import get_gerenciamento_quantitativo__service
from gerenciamento_hexagonal.application.services import GerenciamentoQuantitativoServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError, NotNullViolationError, UniqueViolation
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoQuantitativo
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import GerenciamentoComentarioDTO, GerenciamentoQuantitativoDTO, GerenciamentoQuantitativoListResponse

router = APIRouter()


Service = Annotated[GerenciamentoQuantitativoServices, Depends(get_gerenciamento_quantitativo__service)]


@router.get('/', response_model=GerenciamentoQuantitativoListResponse)
async def get_gerenciamento_quantitativos(service: Service):
    gerenciamento_quantitativos = await service.get_gerenciamento_quantitativo()

    return {'Gerenciamento_Quantitativos': gerenciamento_quantitativos}


@router.get('/{gerenciamento_quantitativo_id}', response_model=GerenciamentoQuantitativo)
async def get_gerenciamento_quantitativo_by_id(gerenciamento_quantitativo_id: int, service: Service):
    try:
        gerenciamento_quantitativo = await service.get_gerenciamento_quantitativo_by_id(gerenciamento_quantitativo_id)

        return gerenciamento_quantitativo

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.post('/{gerenciamentoProposta_id}', response_model=GerenciamentoQuantitativo)
async def create_gerenciamento_quantitativo(gerenciamentoProposta_id: int, gerenciamento_quantitativo: GerenciamentoQuantitativoDTO, service: Service):
    try:
        gerenciamento_quantitativo = await service.create_gerenciamento_quantitativo(gerenciamentoProposta_id, gerenciamento_quantitativo)

        return gerenciamento_quantitativo

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except UniqueViolation as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))


@router.post('/Comentario/{gerenciamento_quantitativo_id}', response_model=GerenciamentoQuantitativo)
async def create_gerenciamento_quantitativo_comentario(gerenciamento_quantitativo_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO, service: Service):
    try:
        gerenciamento_quantitativo_comentario = await service.create_gerenciamento_quantitativo_comentario(gerenciamento_quantitativo_id, gerenciamento_comentario)

        return gerenciamento_quantitativo_comentario

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.put('/{gerenciamento_quantitativo_id}', response_model=GerenciamentoQuantitativo)
async def update_gerenciamento_quantitativo(gerenciamento_quantitativo_id: int, gerenciamento_quantitativo: GerenciamentoQuantitativoDTO, service: Service):
    try:
        gerenciamento_quantitativo = await service.update_gerenciamento_quantitativo(gerenciamento_quantitativo_id, gerenciamento_quantitativo)

        return gerenciamento_quantitativo

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete('/{gerenciamento_quantitativo_id}')
async def delete_gerenciamento_quantitativo(gerenciamento_quantitativo_id: int, service: Service):
    try:
        result = await service.delete_gerenciamento_quantitativo(gerenciamento_quantitativo_id)

        return result

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except NotNullViolationError as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))
