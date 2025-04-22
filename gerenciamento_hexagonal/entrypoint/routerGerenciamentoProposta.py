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


def get_gerenciamentoPropostaSQLite_service() -> GerenciamentoPropostaSQLiteServices:
    gerenciamentoComentario_repository = GerenciamentoComentarioSQLiteRepository()
    gerenciamentoProposta_repository = GerenciamentoPropostaSQLiteRepository(gerenciamentoComentario_repository)
    return GerenciamentoPropostaSQLiteServices(gerenciamentoProposta_repository)


@router.post('/', response_model=GerenciamentoProposta)
async def create_gerenciamentoProposta(gerenciamentoProposta_data: GerenciamentoPropostaDTO, service: GerenciamentoPropostaSQLiteServices = Depends(get_gerenciamentoPropostaSQLite_service)):
    gerenciamentoProposta = await service.create_gerenciamentoProposta(gerenciamentoProposta_data)

    return gerenciamentoProposta


@router.post('/Comentario/{gerenciamentoProposta_id}', response_model=GerenciamentoProposta)
async def create_gerenciamentoPropostaComentario(gerenciamentoProposta_id: int, gerenciamentoComentarioDTO: GerenciamentoComentarioDTO, service: GerenciamentoPropostaSQLiteServices = Depends(get_gerenciamentoPropostaSQLite_service)):
    try:
        gerenciamentoComentario = await service.create_gerenciamentoPropostaComentario(gerenciamentoProposta_id, gerenciamentoComentarioDTO)

        return gerenciamentoComentario

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.get('/', response_model=GerenciamentoPropostaListResponse)
async def get_gerencimentoPropostas(service: GerenciamentoPropostaSQLiteServices = Depends(get_gerenciamentoPropostaSQLite_service)):
    gerenciamentoProposta = await service.get_gerenciamentoProposta()

    return {'Gerenciamento_Propostas': gerenciamentoProposta}


@router.get('/{gerenciamentoProposta_id}', response_model=GerenciamentoProposta)
async def get_by_id_gerenciamentoProposta(gerenciamentoProposta_id: int, service: GerenciamentoPropostaSQLiteServices = Depends(get_gerenciamentoPropostaSQLite_service)):
    try:
        gerenciamentoProposta_by_id = await service.get_gerenciamentoProposta_by_id(gerenciamentoProposta_id)

        return gerenciamentoProposta_by_id

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.put('/{gerenciamentoProposta_id}', response_model=GerenciamentoProposta)
async def update_gerenciamentoProposta(gerenciamentoProposta_id: int, gerenciamentoProposta_data: GerenciamentoPropostaDTO, service: GerenciamentoPropostaSQLiteServices = Depends(get_gerenciamentoPropostaSQLite_service)):
    try:
        gerencimentoProposta = await service.update_gerenciamentoProposta(gerenciamentoProposta_id, gerenciamentoProposta_data)

        return gerencimentoProposta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete('/{gerenciamentoProposta_id}', response_model=str)
async def delete_gerenciamentoProposta(gerenciamentoProposta_id: int, service: GerenciamentoPropostaSQLiteServices = Depends(get_gerenciamentoPropostaSQLite_service)):
    try:
        await service.delete_gerenciamentoProposta(gerenciamentoProposta_id)

        return 'message: gerenciamento_proposta deleted'

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
