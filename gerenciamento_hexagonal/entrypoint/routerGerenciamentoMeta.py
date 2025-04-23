from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from gerenciamento_hexagonal.application.services import GerenciamentoMetaServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoMeta
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import GerenciamentoMetaDTO, GerenciamentoMetaListResponse
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy_repository import GerenciamentoMetaRepository

router = APIRouter()


def get_gerenciamento_meta__service() -> GerenciamentoMetaServices:
    gerenciamento_meta_repository = GerenciamentoMetaRepository()
    return GerenciamentoMetaServices(gerenciamento_meta_repository)


@router.get('/', response_model=GerenciamentoMetaListResponse)
async def get_gerenciamento_metas(service: GerenciamentoMetaServices = Depends(get_gerenciamento_meta__service)):
    gerenciamento_meta = await service.get_gerenciamento_meta()

    return {'Gerenciamento_Metas': gerenciamento_meta}


@router.get('/{gerenciamento_meta_id}', response_model=GerenciamentoMeta)
async def get_gerenciamento_meta_by_id(gerenciamento_meta_id: int, service: GerenciamentoMetaServices = Depends(get_gerenciamento_meta__service)):
    try:
        gerenciamento_meta = await service.get_gerenciamento_meta_by_id(gerenciamento_meta_id)

        return gerenciamento_meta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.post('/{gerenciamento_proposta_id}', response_model=GerenciamentoMeta)
async def create_gerenciamento_meta(gerenciamento_proposta_id: int, gerenciamento_meta: GerenciamentoMetaDTO, service: GerenciamentoMetaServices = Depends(get_gerenciamento_meta__service)):
    try:
        gerenciamento_meta = await service.create_gerenciamento_meta(gerenciamento_proposta_id, gerenciamento_meta)

        return gerenciamento_meta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.put('/{gerenciamento_meta_id}', response_model=GerenciamentoMeta)
async def update_gerenciamento_meta(gerenciamento_meta_id: int, gerenciamento_meta: GerenciamentoMetaDTO, service: GerenciamentoMetaServices = Depends(get_gerenciamento_meta__service)):
    try:
        gerenciamento_meta = await service.update_gerenciamento_meta(gerenciamento_meta_id, gerenciamento_meta)

        return gerenciamento_meta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete('/{gerenciamento_meta_id}', response_model=str)
async def delete_gerenciamento_meta(gerenciamento_meta_id: int, service: GerenciamentoMetaServices = Depends(get_gerenciamento_meta__service)):
    try:
        await service.delete_gerenciamento_meta(gerenciamento_meta_id)

        return 'message: gerenciamento_meta deleted'

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
