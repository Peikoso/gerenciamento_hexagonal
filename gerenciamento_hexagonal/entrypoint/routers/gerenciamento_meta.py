from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from gerenciamento_hexagonal.application.dependencies import get_gerenciamento_meta_service
from gerenciamento_hexagonal.application.services import GerenciamentoMetaServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoMeta
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import GerenciamentoMetaDTO

router = APIRouter()


Service = Annotated[GerenciamentoMetaServices, Depends(get_gerenciamento_meta_service)]


@router.get('/', response_model=list[GerenciamentoMeta])
async def get_gerenciamento_metas(service: Service):
    gerenciamento_meta = await service.get_gerenciamento_meta()

    return gerenciamento_meta


@router.get('/{gerenciamento_meta_id}', response_model=GerenciamentoMeta)
async def get_gerenciamento_meta_by_id(gerenciamento_meta_id: int, service: Service):
    try:
        gerenciamento_meta = await service.get_gerenciamento_meta_by_id(gerenciamento_meta_id)

        return gerenciamento_meta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.post('/{gerenciamento_proposta_id}', response_model=GerenciamentoMeta)
async def create_gerenciamento_meta(gerenciamento_proposta_id: int, gerenciamento_meta: GerenciamentoMetaDTO, service: Service):
    try:
        gerenciamento_meta = await service.create_gerenciamento_meta(gerenciamento_proposta_id, gerenciamento_meta)

        return gerenciamento_meta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.put('/{gerenciamento_meta_id}', response_model=GerenciamentoMeta)
async def update_gerenciamento_meta(gerenciamento_meta_id: int, gerenciamento_meta: GerenciamentoMetaDTO, service: Service):
    try:
        gerenciamento_meta = await service.update_gerenciamento_meta(gerenciamento_meta_id, gerenciamento_meta)

        return gerenciamento_meta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete('/{gerenciamento_meta_id}')
async def delete_gerenciamento_meta(gerenciamento_meta_id: int, service: Service):
    try:
        result = await service.delete_gerenciamento_meta(gerenciamento_meta_id)

        return result

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
