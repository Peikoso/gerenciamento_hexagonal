from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from gerenciamento_hexagonal.application.dependencies import get_gerenciamento_caracterizacao_service
from gerenciamento_hexagonal.application.services import GerenciamentoCaracterizacaoServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError, UniqueViolation
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoCaracterizacao
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import GerenciamentoCaracterizacaoDTO

router = APIRouter()


Service = Annotated[GerenciamentoCaracterizacaoServices, Depends(get_gerenciamento_caracterizacao_service)]


@router.get('/', response_model=list[GerenciamentoCaracterizacao])
async def get_gerenciamento_caracterizacao(service: Service):
    gerenciamento_caracterizacoes = await service.get_gerenciamento_caracterizacao()

    return gerenciamento_caracterizacoes


@router.get('/{gerenciamento_caracterizacao_id}', response_model=GerenciamentoCaracterizacao)
async def get_gerenciamento_caracterizacao_by_id(gerenciamento_caracterizacao_id: int, service: Service):
    try:
        gerenciamento_caracterizacao = await service.get_gerenciamento_caracterizacao_by_id(gerenciamento_caracterizacao_id)

        return gerenciamento_caracterizacao

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.post('/{gerencimento_quantitativo_id}', response_model=GerenciamentoCaracterizacao)
async def create_gerenciamento_caracterizacao(gerencimento_quantitativo_id: int, gerenciamento_caracterizacao: GerenciamentoCaracterizacaoDTO, service: Service):
    try:
        gerenciamento_caracterizacao = await service.create_gerenciamento_caracterizacao(gerencimento_quantitativo_id, gerenciamento_caracterizacao)

        return gerenciamento_caracterizacao

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except UniqueViolation as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))


@router.put('/{gerenciamento_caracterizacao_id}', response_model=GerenciamentoCaracterizacao)
async def update_gerenciamento_caracterizacao(gerenciamento_caracterizacao_id: int, gerenciamento_caracterizacao: GerenciamentoCaracterizacaoDTO, service: Service):
    try:
        gerenciamento_caracterizacao = await service.update_gerenciamento_caracterizacao(gerenciamento_caracterizacao_id, gerenciamento_caracterizacao)

        return gerenciamento_caracterizacao

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete('/{gerenciamento_caracterizacao_id}')
async def delete_gerenciamento_caracterizacao(gerenciamento_caracterizacao_id: int, service: Service):
    try:
        result = await service.delete_gerenciamento_caracterizacao(gerenciamento_caracterizacao_id)

        return result

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
