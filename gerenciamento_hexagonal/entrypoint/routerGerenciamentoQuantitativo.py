from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from gerenciamento_hexagonal.application.servicesSQLite import GerenciamentoQuantitativoSQLiteServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoQuantitativo
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import GerenciamentoComentarioDTO, GerenciamentoQuantitativoDTO, GerenciamentoQuantitativoListResponse
from gerenciamento_hexagonal.infrastructure.repositories.SQLiterepository import GerenciamentoComentarioSQLiteRepository, GerenciamentoQuantitativoSQLiteRepository

router = APIRouter()


def get_gerenciamento_quantitativo_sqlite_service() -> GerenciamentoQuantitativoSQLiteServices:
    gerenciamento_comentario_repository = GerenciamentoComentarioSQLiteRepository()
    gerenciamento_quantitativo_repository = GerenciamentoQuantitativoSQLiteRepository(gerenciamento_comentario_repository)
    return GerenciamentoQuantitativoSQLiteServices(gerenciamento_quantitativo_repository)


@router.get('/', response_model=GerenciamentoQuantitativoListResponse)
async def get_gerenciamento_quantitativos(service: GerenciamentoQuantitativoSQLiteServices = Depends(get_gerenciamento_quantitativo_sqlite_service)):
    gerenciamento_quantitativos = await service.get_gerenciamento_quantitativo()

    return {'Gerenciamento_Quantitativos': gerenciamento_quantitativos}


@router.get('/{gerenciamento_quantitativo_id}', response_model=GerenciamentoQuantitativo)
async def get_gerenciamento_quantitativo_by_id(gerenciamento_quantitativo_id: int, service: GerenciamentoQuantitativoSQLiteServices = Depends(get_gerenciamento_quantitativo_sqlite_service)):
    try:
        gerenciamento_quantitativo = await service.get_gerenciamento_quantitativo_by_id(gerenciamento_quantitativo_id)

        return gerenciamento_quantitativo

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.post('/{gerenciamentoProposta_id}', response_model=GerenciamentoQuantitativo)
async def create_gerenciamento_quantitativo(gerenciamentoProposta_id: int, gerenciamento_quantitativo: GerenciamentoQuantitativoDTO, service: GerenciamentoQuantitativoSQLiteServices = Depends(get_gerenciamento_quantitativo_sqlite_service)):
    try:
        gerenciamento_quantitativo = await service.create_gerenciamento_quantitativo(gerenciamentoProposta_id, gerenciamento_quantitativo)

        return gerenciamento_quantitativo

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.post('/Comentario/{gerenciamento_quantitativo_id}', response_model=GerenciamentoQuantitativo)
async def create_gerenciamento_quantitativo_comentario(gerenciamento_quantitativo_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO, service: GerenciamentoQuantitativoSQLiteServices = Depends(get_gerenciamento_quantitativo_sqlite_service)):
    try:
        gerenciamento_quantitativo_comentario = await service.create_gerenciamento_quantitativo_comentario(gerenciamento_quantitativo_id, gerenciamento_comentario)

        return gerenciamento_quantitativo_comentario

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.put('/{gerenciamento_quantitativo_id}', response_model=GerenciamentoQuantitativo)
async def update_gerenciamento_quantitativo(gerenciamento_quantitativo_id: int, gerenciamento_quantitativo: GerenciamentoQuantitativoDTO, service: GerenciamentoQuantitativoSQLiteServices = Depends(get_gerenciamento_quantitativo_sqlite_service)):
    try:
        gerenciamento_quantitativo = await service.update_gerenciamento_quantitativo(gerenciamento_quantitativo_id, gerenciamento_quantitativo)

        return gerenciamento_quantitativo

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete('/{gerenciamento_quantitativo_id}')
async def delete_gerenciamento_quantitativo(gerenciamento_quantitativo_id: int, service: GerenciamentoQuantitativoSQLiteServices = Depends(get_gerenciamento_quantitativo_sqlite_service)):
    try:
        result = await service.delete_gerenciamento_quantitativo(gerenciamento_quantitativo_id)

        return result

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
