from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import DomainValidationError, NotFoundError, NotNullViolationError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoQuantitativo
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoComentarioDTO, GerenciamentoQuantitativoDTO
from gerenciamento_hexagonal.infrastructure.handler.fastapi.annotated import Service_Quantitativo

router = APIRouter()


@router.get('/', response_model=list[GerenciamentoQuantitativo])
async def get_gerenciamento_quantitativos(service: Service_Quantitativo):
    gerenciamento_quantitativos = await service.get_gerenciamento_quantitativo()

    return gerenciamento_quantitativos


@router.get('/{gerenciamento_quantitativo_id}', response_model=GerenciamentoQuantitativo)
async def get_gerenciamento_quantitativo_by_id(gerenciamento_quantitativo_id: int, service: Service_Quantitativo):
    try:
        gerenciamento_quantitativo = await service.get_gerenciamento_quantitativo_by_id(gerenciamento_quantitativo_id)

        return gerenciamento_quantitativo

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.post('/{gerenciamentoProposta_id}', response_model=GerenciamentoQuantitativo)
async def create_gerenciamento_quantitativo(gerenciamentoProposta_id: int, gerenciamento_quantitativo: GerenciamentoQuantitativoDTO, service: Service_Quantitativo):
    try:
        gerenciamento_quantitativo = await service.create_gerenciamento_quantitativo(gerenciamentoProposta_id, gerenciamento_quantitativo)

        return gerenciamento_quantitativo

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except DomainValidationError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))


@router.post('/Comentario/{gerenciamento_quantitativo_id}', response_model=GerenciamentoQuantitativo)
async def create_gerenciamento_quantitativo_comentario(gerenciamento_quantitativo_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO, service: Service_Quantitativo):
    try:
        gerenciamento_quantitativo_comentario = await service.create_gerenciamento_quantitativo_comentario(gerenciamento_quantitativo_id, gerenciamento_comentario)

        return gerenciamento_quantitativo_comentario

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except DomainValidationError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))


@router.put('/{gerenciamento_quantitativo_id}', response_model=GerenciamentoQuantitativo)
async def update_gerenciamento_quantitativo(gerenciamento_quantitativo_id: int, gerenciamento_quantitativo: GerenciamentoQuantitativoDTO, service: Service_Quantitativo):
    try:
        gerenciamento_quantitativo = await service.update_gerenciamento_quantitativo(gerenciamento_quantitativo_id, gerenciamento_quantitativo)

        return gerenciamento_quantitativo

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except DomainValidationError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))


@router.delete('/{gerenciamento_quantitativo_id}')
async def delete_gerenciamento_quantitativo(gerenciamento_quantitativo_id: int, service: Service_Quantitativo):
    try:
        result = await service.delete_gerenciamento_quantitativo(gerenciamento_quantitativo_id)

        return result

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except NotNullViolationError as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))
