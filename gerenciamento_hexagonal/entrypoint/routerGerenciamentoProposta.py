from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from gerenciamento_hexagonal.application.servicesSQLite import (
    GerenciamentoPropostaSQLiteServices,
)
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import (
    NotFoundError,
)
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoProposta
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import (
    GerenciamentoComentarioDTO,
    GerenciamentoPropostaDTO,
    GerenciamentoPropostaListResponse,
)
from gerenciamento_hexagonal.infrastructure.repositories.SQLiterepository import (
    GerenciamentoComentarioSQLiteRepository,
    GerenciamentoPropostaSQLiteRepository,
)

router = APIRouter()


def get_gerenciamento_proposta_sqlite_service() -> GerenciamentoPropostaSQLiteServices:
    gerenciamento_comentario_repository = GerenciamentoComentarioSQLiteRepository()
    gerenciamento_proposta_repository = GerenciamentoPropostaSQLiteRepository(gerenciamento_comentario_repository)
    return GerenciamentoPropostaSQLiteServices(gerenciamento_proposta_repository)


@router.post('/', response_model=GerenciamentoProposta)
async def create_gerenciamentoProposta(gerenciamento_proposta: GerenciamentoPropostaDTO, service: GerenciamentoPropostaSQLiteServices = Depends(get_gerenciamento_proposta_sqlite_service)):
    gerenciamento_proposta = await service.create_gerenciamento_proposta(gerenciamento_proposta)

    return gerenciamento_proposta


@router.post('/Comentario/{gerenciamento_proposta_id}', response_model=GerenciamentoProposta)
async def create_gerenciamentoPropostaComentario(gerenciamento_proposta_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO, service: GerenciamentoPropostaSQLiteServices = Depends(get_gerenciamento_proposta_sqlite_service)):
    try:
        gerenciamento_comentario = await service.create_gerenciamento_proposta_comentario(gerenciamento_proposta_id, gerenciamento_comentario)

        return gerenciamento_comentario

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.get('/', response_model=GerenciamentoPropostaListResponse)
async def get_gerencimentoPropostas(service: GerenciamentoPropostaSQLiteServices = Depends(get_gerenciamento_proposta_sqlite_service)):
    gerenciamento_propostas = await service.get_gerenciamento_proposta()

    return {'Gerenciamento_Propostas': gerenciamento_propostas}


@router.get('/{gerenciamento_proposta_id}', response_model=GerenciamentoProposta)
async def get_by_id_gerenciamentoProposta(gerenciamento_proposta_id: int, service: GerenciamentoPropostaSQLiteServices = Depends(get_gerenciamento_proposta_sqlite_service)):
    try:
        gerenciamento_proposta = await service.get_gerenciamento_proposta_by_id(gerenciamento_proposta_id)

        return gerenciamento_proposta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.put('/{gerenciamento_proposta_id}', response_model=GerenciamentoProposta)
async def update_gerenciamentoProposta(gerenciamento_proposta_id: int, gerenciamento_proposta: GerenciamentoPropostaDTO, service: GerenciamentoPropostaSQLiteServices = Depends(get_gerenciamento_proposta_sqlite_service)):
    try:
        gerenciamento_proposta = await service.update_gerenciamento_proposta(gerenciamento_proposta_id, gerenciamento_proposta)

        return gerenciamento_proposta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete('/{gerenciamento_proposta_id}', response_model=str)
async def delete_gerenciamentoProposta(gerenciamento_proposta_id: int, service: GerenciamentoPropostaSQLiteServices = Depends(get_gerenciamento_proposta_sqlite_service)):
    try:
        await service.delete_gerenciamento_proposta(gerenciamento_proposta_id)

        return 'message: gerenciamento_proposta deleted'

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
