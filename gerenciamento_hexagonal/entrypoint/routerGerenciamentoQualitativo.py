from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from gerenciamento_hexagonal.application.dependencies import get_gerenciamento_qualitativo__service
from gerenciamento_hexagonal.application.services import GerenciamentoQualitativoServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError, UniqueViolation
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoQualitativo
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import GerenciamentoComentarioDTO, GerenciamentoQualitativoDTO

router = APIRouter()


Service = Annotated[GerenciamentoQualitativoServices, Depends(get_gerenciamento_qualitativo__service)]


@router.get('/', response_model=list[GerenciamentoQualitativo])
async def get_gerenciamento_qualitativo(service: Service):
    gerenciamento_qualitativo = await service.get_gerenciamento_qualitativo()

    return gerenciamento_qualitativo


@router.get('/{gerenciamento_qualitativo_id}', response_model=GerenciamentoQualitativo)
async def get_gerenciamento_qualitativo_by_id(gerenciamento_qualitativo_id: int, service: Service):
    try:
        gerenciamento_qualitativo = await service.get_gerenciamento_qualitativo_by_id(gerenciamento_qualitativo_id)

        return gerenciamento_qualitativo

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.post('/{gerenciamento_proposta_id}', response_model=GerenciamentoQualitativo)
async def create_gerenciamento_qualitativo(gerenciamento_proposta_id: int, gerenciamento_qualitativo: GerenciamentoQualitativoDTO, service: Service):
    try:
        gerenciamento_qualitativo = await service.create_gerenciamento_qualitativo(gerenciamento_proposta_id, gerenciamento_qualitativo)

        return gerenciamento_qualitativo

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except UniqueViolation as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))


@router.post('/Comentario/{gerenciamento_qualitativo_id}', response_model=GerenciamentoQualitativo)
async def create_gerenciamento_qualitativo_comentario(gerenciamento_qualitativo_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO, service: Service):
    try:
        gerenciamento_qualitativo_comentario = await service.create_gerenciamento_qualitativo_comentario(gerenciamento_qualitativo_id, gerenciamento_comentario)

        return gerenciamento_qualitativo_comentario

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.put('/{gerenciamento_qualitativo_id}', response_model=GerenciamentoQualitativo)
async def update_gerenciamento_qualitativo(gerenciamento_qualitativo_id: int, gerenciamento_qualitativo: GerenciamentoQualitativoDTO, service: Service):
    try:
        gerenciamento_qualitativo = await service.update_gerenciamento_qualitativo(gerenciamento_qualitativo_id, gerenciamento_qualitativo)

        return gerenciamento_qualitativo

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete('/{gerenciamento_qualitativo_id}')
async def delete_gerenciamento_qualitativo(gerenciamento_qualitativo_id: int, service: Service):
    try:
        result = await service.delete_gerenciamento_qualitativo(gerenciamento_qualitativo_id)

        return result

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
