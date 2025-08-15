from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import DomainValidationError, NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoMeta
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoMetaDTO
from gerenciamento_hexagonal.infrastructure.handler.annotated import Service_Meta

router = APIRouter()


@router.get('/', response_model=list[GerenciamentoMeta])
async def get_gerenciamento_metas(service: Service_Meta):
    gerenciamento_meta = await service.get_gerenciamento_meta()

    return gerenciamento_meta


@router.get('/{gerenciamento_meta_id}', response_model=GerenciamentoMeta)
async def get_gerenciamento_meta_by_id(gerenciamento_meta_id: int, service: Service_Meta):
    try:
        gerenciamento_meta = await service.get_gerenciamento_meta_by_id(gerenciamento_meta_id)

        return gerenciamento_meta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.post('/{gerenciamento_proposta_id}', response_model=GerenciamentoMeta)
async def create_gerenciamento_meta(gerenciamento_proposta_id: int, gerenciamento_meta: GerenciamentoMetaDTO, service: Service_Meta):
    try:
        gerenciamento_meta = await service.create_gerenciamento_meta(gerenciamento_proposta_id, gerenciamento_meta)

        return gerenciamento_meta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except DomainValidationError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))


@router.put('/{gerenciamento_meta_id}', response_model=GerenciamentoMeta)
async def update_gerenciamento_meta(gerenciamento_meta_id: int, gerenciamento_meta: GerenciamentoMetaDTO, service: Service_Meta):
    try:
        gerenciamento_meta = await service.update_gerenciamento_meta(gerenciamento_meta_id, gerenciamento_meta)

        return gerenciamento_meta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except DomainValidationError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))


@router.delete('/{gerenciamento_meta_id}')
async def delete_gerenciamento_meta(gerenciamento_meta_id: int, service: Service_Meta):
    try:
        result = await service.delete_gerenciamento_meta(gerenciamento_meta_id)

        return result

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))
