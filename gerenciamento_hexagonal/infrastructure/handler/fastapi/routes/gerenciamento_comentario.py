from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import DomainValidationError, NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoComentario
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoComentarioDTO
from gerenciamento_hexagonal.infrastructure.handler.fastapi.annotated import Service_Comentario

router = APIRouter()


@router.get('/', response_model=list[GerenciamentoComentario])
async def get_gerenciamento_comentarios(service: Service_Comentario):
    gerenciamento_comentarios = await service.get_gerenciamento_comentario()

    return gerenciamento_comentarios


@router.get('/{gerenciamento_comentario_id}', response_model=GerenciamentoComentario)
async def get_by_id_gerenciamento_comentario(gerenciamento_comentario_id: int, service: Service_Comentario):
    try:
        gerenciamento_comentario = await service.get_gerenciamento_comentario_by_id(gerenciamento_comentario_id)

        return gerenciamento_comentario

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.put('/{gerenciamento_comentario_id}', response_model=GerenciamentoComentario)
async def update_gerenciamento_comentario(gerenciamento_comentario_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO, service: Service_Comentario):
    try:
        gerenciamento_comentario = await service.update_gerenciamento_comentario(gerenciamento_comentario_id, gerenciamento_comentario)

        return gerenciamento_comentario

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except DomainValidationError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))


@router.delete('/{gerenciamento_comentario_id}')
async def delete_gerenciamento_comentario(gerenciamento_comentario_id: int, service: Service_Comentario):
    try:
        result = await service.delete_gerenciamento_comentario(gerenciamento_comentario_id)

        return result

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
