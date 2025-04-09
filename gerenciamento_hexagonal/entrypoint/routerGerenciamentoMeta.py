from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from gerenciamento_hexagonal.application.servicesSQLite import GerenciamentoMetaSQLiteServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoMeta
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import GerenciamentoMetaDTO, GerenciamentoMetaListResponse
from gerenciamento_hexagonal.infrastructure.repositories.SQLiterepository import GerenciamentoMetaSQLiteRepository

router = APIRouter()


def get_gerenciamentoMetaSQLite_Service() -> GerenciamentoMetaSQLiteServices:
    gerenciamentoMeto_repository = GerenciamentoMetaSQLiteRepository()
    return GerenciamentoMetaSQLiteServices(gerenciamentoMeto_repository)


@router.get('/', response_model=GerenciamentoMetaListResponse)
async def get_gerenciamentoMetas(service: GerenciamentoMetaSQLiteServices = Depends(get_gerenciamentoMetaSQLite_Service)):
    gerenciamentoMetas = await service.get_gerenciamentoMeta()

    return {'Gerenciamento_Metas': gerenciamentoMetas}


@router.get('/{gerenciamentoMeta_id}', response_model=GerenciamentoMeta)
async def get_gerenciamentoMeto_by_id(gerenciamentoMeta_id: int, service: GerenciamentoMetaSQLiteServices = Depends(get_gerenciamentoMetaSQLite_Service)):
    try:
        gerenciamentoMeta = await service.get_gerenciamentoMeta_by_id(gerenciamentoMeta_id)

        return gerenciamentoMeta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.post('/', response_model=GerenciamentoMeta)
async def create_gerenciamentoMeta(gerenciamentoProposta_id: int, gerenciamentoMeta_data: GerenciamentoMetaDTO, service: GerenciamentoMetaSQLiteServices = Depends(get_gerenciamentoMetaSQLite_Service)):
    try:
        gerenciamentoMeta = await service.create_gerenciamentoMeta(gerenciamentoProposta_id, gerenciamentoMeta_data)

        return gerenciamentoMeta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.put('/{gerenciamentoMeta_id}', response_model=GerenciamentoMeta)
async def update_gerenciamentoMeta(gerenciamentoMeta_id: int, gerenciamentoMeta_data: GerenciamentoMetaDTO, service: GerenciamentoMetaSQLiteServices = Depends(get_gerenciamentoMetaSQLite_Service)):
    try:
        gerenciamentoMeta = await service.update_gerenciamentoMeta(gerenciamentoMeta_id, gerenciamentoMeta_data)

        return gerenciamentoMeta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete('/{gerenciamentoMeta_id}', response_model=str)
async def delete_gerenciamentoMeta(gerenciamentoMeta_id: int, service: GerenciamentoMetaSQLiteServices = Depends(get_gerenciamentoMetaSQLite_Service)):
    try:
        await service.delete_gerenciamentoMeta(gerenciamentoMeta_id)

        return 'message: gerenciamento_meta deleted'

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
