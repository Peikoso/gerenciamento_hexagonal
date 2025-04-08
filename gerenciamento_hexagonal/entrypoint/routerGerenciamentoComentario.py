from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from gerenciamento_hexagonal.application.servicesSQLite import GerenciamentoComentarioSQLiteServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoComentario
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import GerenciamentoComentarioDTO, GerenciamentoComentarioListResponse
from gerenciamento_hexagonal.infrastructure.repositories.SQLiterepository import GerenciamentoComentarioSQLiteRepository

router = APIRouter()


def get_gerenciamentoComentarioSQlite_service() -> GerenciamentoComentarioSQLiteServices:
    gerenciamentoComentario_repository = GerenciamentoComentarioSQLiteRepository()
    return GerenciamentoComentarioSQLiteServices(gerenciamentoComentario_repository)


@router.get('/', response_model=GerenciamentoComentarioListResponse)
async def get_gerenciamentoComentarios(service: GerenciamentoComentarioSQLiteServices = Depends(get_gerenciamentoComentarioSQlite_service)):
    gerenciamentoComentarios = await service.get_gerenciamentoComentario()

    return {'Gerenciamento_Comentarios': gerenciamentoComentarios}


@router.get('/{gerenciamentoComentario_id}', response_model=GerenciamentoComentario)
async def get_by_id_gerenciamentoComentario(gerenciamentoComentario_id: int, service: GerenciamentoComentarioSQLiteServices = Depends(get_gerenciamentoComentarioSQlite_service)):
    try:
        gerenciamentoComentario = await service.get_gerenciamentoComentario_by_id(gerenciamentoComentario_id)

        return gerenciamentoComentario

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.put('/{gerenciamentoComentario_id}', response_model=GerenciamentoComentario)
async def update_gerenciamentoComentario(gerenciamentoComentario_id: int, gerenciamentoComentario_data: GerenciamentoComentarioDTO, service: GerenciamentoComentarioSQLiteServices = Depends(get_gerenciamentoComentarioSQlite_service)):
    try:
        gerenciamentoComentario = await service.update_gerenciamentoComentario(gerenciamentoComentario_id, gerenciamentoComentario_data)

        return gerenciamentoComentario

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete('/{gerenciamentoComentario_id}', response_model=str)
async def delete_gerenciamentoComentario(gerenciamentoComentario_id: int, service: GerenciamentoComentarioSQLiteServices = Depends(get_gerenciamentoComentarioSQlite_service)):
    try:
        await service.delete_gerenciamentoComentario(gerenciamentoComentario_id)

        return 'message: gerenciamento_comentario deleted'
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
