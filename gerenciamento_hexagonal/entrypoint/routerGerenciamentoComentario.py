from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from gerenciamento_hexagonal.application.servicesSQLite import GerenciamentoComentarioSQLiteServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoComentario
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import GerenciamentoComentarioDTO, GerenciamentoComentarioListResponse
from gerenciamento_hexagonal.infrastructure.repositories.SQLiterepository import GerenciamentoComentarioSQLiteRepository

router = APIRouter()


def get_gerenciamento_comentario_sqlite_service() -> GerenciamentoComentarioSQLiteServices:
    gerenciamento_comentario_repository = GerenciamentoComentarioSQLiteRepository()
    return GerenciamentoComentarioSQLiteServices(gerenciamento_comentario_repository)


@router.get('/', response_model=GerenciamentoComentarioListResponse)
async def get_gerenciamento_comentarios(service: GerenciamentoComentarioSQLiteServices = Depends(get_gerenciamento_comentario_sqlite_service)):
    gerenciamento_comentarios = await service.get_gerenciamento_comentario()

    return {'Gerenciamento_Comentarios': gerenciamento_comentarios}


@router.get('/{gerenciamento_comentario_id}', response_model=GerenciamentoComentario)
async def get_by_id_gerenciamento_comentario(gerenciamento_comentario_id: int, service: GerenciamentoComentarioSQLiteServices = Depends(get_gerenciamento_comentario_sqlite_service)):
    try:
        gerenciamento_comentario = await service.get_gerenciamento_comentario_by_id(gerenciamento_comentario_id)

        return gerenciamento_comentario

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.put('/{gerenciamento_comentario_id}', response_model=GerenciamentoComentario)
async def update_gerenciamento_comentario(gerenciamento_comentario_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO, service: GerenciamentoComentarioSQLiteServices = Depends(get_gerenciamento_comentario_sqlite_service)):
    try:
        gerenciamento_comentario = await service.update_gerenciamento_comentario(gerenciamento_comentario_id, gerenciamento_comentario)

        return gerenciamento_comentario

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete('/{gerenciamento_comentario_id}', response_model=str)
async def delete_gerenciamento_comentario(gerenciamento_comentario_id: int, service: GerenciamentoComentarioSQLiteServices = Depends(get_gerenciamento_comentario_sqlite_service)):
    try:
        await service.delete_gerenciamento_comentario(gerenciamento_comentario_id)

        return 'message: gerenciamento_comentario deleted'
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
