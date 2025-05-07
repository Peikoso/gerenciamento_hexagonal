from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from gerenciamento_hexagonal.application.dependencies import get_gerenciamento_proposta_service
from gerenciamento_hexagonal.application.services import (
    GerenciamentoPropostaServices,
)
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import (
    NotFoundError,
    NotNullViolationError,
)
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoProposta
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import (
    GerenciamentoComentarioDTO,
    GerenciamentoPropostaDTO,
)

router = APIRouter()


Service = Annotated[GerenciamentoPropostaServices, Depends(get_gerenciamento_proposta_service)]


@router.post('/', response_model=GerenciamentoProposta)
async def create_gerenciamento_proposta(gerenciamento_proposta: GerenciamentoPropostaDTO, service: Service):
    gerenciamento_proposta = await service.create_gerenciamento_proposta(gerenciamento_proposta)

    return gerenciamento_proposta


@router.post('/Comentario/{gerenciamento_proposta_id}', response_model=GerenciamentoProposta)
async def create_gerenciamento_propostaComentario(gerenciamento_proposta_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO, service: Service):
    try:
        gerenciamento_comentario = await service.create_gerenciamento_proposta_comentario(gerenciamento_proposta_id, gerenciamento_comentario)

        return gerenciamento_comentario

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.get('/', response_model=list[GerenciamentoProposta])
async def get_gerencimentoPropostas(service: Service):
    gerenciamento_propostas = await service.get_gerenciamento_proposta()

    return gerenciamento_propostas


@router.get('/{gerenciamento_proposta_id}', response_model=GerenciamentoProposta)
async def get_by_id_gerenciamento_proposta(gerenciamento_proposta_id: int, service: Service):
    try:
        gerenciamento_proposta = await service.get_gerenciamento_proposta_by_id(gerenciamento_proposta_id)

        return gerenciamento_proposta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.put('/{gerenciamento_proposta_id}', response_model=GerenciamentoProposta)
async def update_gerenciamento_proposta(gerenciamento_proposta_id: int, gerenciamento_proposta: GerenciamentoPropostaDTO, service: Service):
    try:
        gerenciamento_proposta = await service.update_gerenciamento_proposta(gerenciamento_proposta_id, gerenciamento_proposta)

        return gerenciamento_proposta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete('/{gerenciamento_proposta_id}')
async def delete_gerenciamento_proposta(gerenciamento_proposta_id: int, service: Service):
    try:
        result = await service.delete_gerenciamento_proposta(gerenciamento_proposta_id)

        return result

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except NotNullViolationError as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))
