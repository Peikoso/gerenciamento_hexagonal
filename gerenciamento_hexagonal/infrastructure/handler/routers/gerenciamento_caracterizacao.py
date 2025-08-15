from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoCaracterizacao
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoCaracterizacaoDTO
from gerenciamento_hexagonal.infrastructure.handler.annotated import Service_Caracterizacao

router = APIRouter()


@router.get('/', response_model=list[GerenciamentoCaracterizacao])
async def get_gerenciamento_caracterizacao(service: Service_Caracterizacao):
    gerenciamento_caracterizacoes = await service.get_gerenciamento_caracterizacao()

    return gerenciamento_caracterizacoes


@router.get('/{gerenciamento_caracterizacao_id}', response_model=GerenciamentoCaracterizacao)
async def get_gerenciamento_caracterizacao_by_id(gerenciamento_caracterizacao_id: int, service: Service_Caracterizacao):
    try:
        gerenciamento_caracterizacao = await service.get_gerenciamento_caracterizacao_by_id(gerenciamento_caracterizacao_id)

        return gerenciamento_caracterizacao

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.post('/{gerencimento_quantitativo_id}', response_model=GerenciamentoCaracterizacao)
async def create_gerenciamento_caracterizacao(gerencimento_quantitativo_id: int, gerenciamento_caracterizacao: GerenciamentoCaracterizacaoDTO, service: Service_Caracterizacao):
    try:
        gerenciamento_caracterizacao = await service.create_gerenciamento_caracterizacao(gerencimento_quantitativo_id, gerenciamento_caracterizacao)

        return gerenciamento_caracterizacao

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.put('/{gerenciamento_caracterizacao_id}', response_model=GerenciamentoCaracterizacao)
async def update_gerenciamento_caracterizacao(gerenciamento_caracterizacao_id: int, gerenciamento_caracterizacao: GerenciamentoCaracterizacaoDTO, service: Service_Caracterizacao):
    try:
        gerenciamento_caracterizacao = await service.update_gerenciamento_caracterizacao(gerenciamento_caracterizacao_id, gerenciamento_caracterizacao)

        return gerenciamento_caracterizacao

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete('/{gerenciamento_caracterizacao_id}')
async def delete_gerenciamento_caracterizacao(gerenciamento_caracterizacao_id: int, service: Service_Caracterizacao):
    try:
        result = await service.delete_gerenciamento_caracterizacao(gerenciamento_caracterizacao_id)

        return result

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
