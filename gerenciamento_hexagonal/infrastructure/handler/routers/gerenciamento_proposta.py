from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import (
    DomainValidationError,
    NotFoundError,
    NotNullViolationError,
)
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoComentario, GerenciamentoProposta
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import (
    GerenciamentoComentarioDTO,
    GerenciamentoPropostaDTO,
    GerenciamentoPropostaResponse,
)
from gerenciamento_hexagonal.infrastructure.handler.annotated import Service_Proposta

router = APIRouter()


@router.post('/', response_model=GerenciamentoPropostaResponse)
async def create_gerenciamento_proposta(gerenciamento_proposta: GerenciamentoPropostaDTO, service: Service_Proposta):
    gerenciamento_proposta = await service.create_gerenciamento_proposta(gerenciamento_proposta)

    return gerenciamento_proposta


@router.post('/Comentario/{gerenciamento_proposta_id}', response_model=GerenciamentoComentario)
async def create_gerenciamento_propostaComentario(gerenciamento_proposta_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO, service: Service_Proposta):
    try:
        gerenciamento_comentario = await service.create_gerenciamento_proposta_comentario(gerenciamento_proposta_id, gerenciamento_comentario)

        return gerenciamento_comentario

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except DomainValidationError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))


@router.get('/', response_model=list[GerenciamentoPropostaResponse])
async def get_gerencimentoPropostas(service: Service_Proposta):
    gerenciamento_propostas = await service.get_gerenciamento_proposta()

    return gerenciamento_propostas


@router.get('/{gerenciamento_proposta_id}', response_model=GerenciamentoProposta)
async def get_by_id_gerenciamento_proposta(gerenciamento_proposta_id: int, service: Service_Proposta):
    try:
        gerenciamento_proposta = await service.get_gerenciamento_proposta_by_id(gerenciamento_proposta_id)

        return gerenciamento_proposta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.put('/{gerenciamento_proposta_id}', response_model=GerenciamentoPropostaResponse)
async def update_gerenciamento_proposta(gerenciamento_proposta_id: int, gerenciamento_proposta: GerenciamentoPropostaDTO, service: Service_Proposta):
    try:
        gerenciamento_proposta = await service.update_gerenciamento_proposta(gerenciamento_proposta_id, gerenciamento_proposta)

        return gerenciamento_proposta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete('/{gerenciamento_proposta_id}')
async def delete_gerenciamento_proposta(gerenciamento_proposta_id: int, service: Service_Proposta):
    try:
        result = await service.delete_gerenciamento_proposta(gerenciamento_proposta_id)

        return result

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except NotNullViolationError as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))
