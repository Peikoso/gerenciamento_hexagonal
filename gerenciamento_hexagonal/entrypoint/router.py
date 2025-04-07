from http import HTTPStatus

from domain.models.gerenciamento import GerenciamentoProposta
from domain.models.gerenciamentoDTO_Response import (
    GerenciamentoComentarioDTO,
    GerenciamentoPropostaDTO,
    GerenciamentoPropostaListResponse,
)
from fastapi import APIRouter, Depends, HTTPException

from gerenciamento_hexagonal.application.servicesSQLite import (
    GerenciamentoPropostaSQLiteServices,
)
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import (
    NotFoundError,
)
from gerenciamento_hexagonal.infrastructure.repositories.SQLiterepository import (
    GerenciamentoComentarioSQLiteRepository,
    GerenciamentoPropostaSQLiteRepository,
)

# from infrastructure.database import Database

router = APIRouter()

# database = Database()


def get_gerenciamentoPropostaSQLite_service() -> GerenciamentoPropostaSQLiteServices:
    gerenciamentoComentario_repository = GerenciamentoComentarioSQLiteRepository()
    gerenciamentoProposta_repository = GerenciamentoPropostaSQLiteRepository(gerenciamentoComentario_repository)
    return GerenciamentoPropostaSQLiteServices(gerenciamentoProposta_repository)


@router.post('/GerenciamentoProposta/', response_model=GerenciamentoProposta)
async def create_gerenciamentoProposta(gerenciamentoProposta_data: GerenciamentoPropostaDTO, service: GerenciamentoPropostaSQLiteServices = Depends(get_gerenciamentoPropostaSQLite_service)):
    gerenciamentoProposta = await service.create_gerenciamentoProposta(gerenciamentoProposta_data)

    return gerenciamentoProposta


@router.get('/GerenciamentoProposta/', response_model=GerenciamentoPropostaListResponse)
async def get_gerencimentoPropostas(service: GerenciamentoPropostaSQLiteServices = Depends(get_gerenciamentoPropostaSQLite_service)):
    gerenciamentoProposta = await service.get_gerenciamentoProposta()

    return {'Gerenciamento_Propostas': gerenciamentoProposta}


@router.get('/GerenciamentoProposta/{gerenciamentoProposta_id}', response_model=GerenciamentoProposta)
async def get_by_id_gerenciamentoProposta(gerenciamentoProposta_id: int, service: GerenciamentoPropostaSQLiteServices = Depends(get_gerenciamentoPropostaSQLite_service)):
    try:
        gerenciamentoProposta_by_id = await service.get_gerenciamentoProposta_by_id(gerenciamentoProposta_id)

        return gerenciamentoProposta_by_id

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete('/GerenciamentoProposta/{gerenciamentoProposta_id}')
async def delete_gerenciamentoProposta(gerenciamentoProposta_id: int, service: GerenciamentoPropostaSQLiteServices = Depends(get_gerenciamentoPropostaSQLite_service)):
    try:
        await service.delete_gerenciamentoProposta(gerenciamentoProposta_id)

        return {'message': 'gerenciamento_proposta deleted'}

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.put('/GerenciamentoProposta/{gerenciamentoProposta_id}')
async def update_gerenciamentoProposta(gerenciamentoProposta_id: int, gerenciamentoProposta_data: GerenciamentoPropostaDTO, service: GerenciamentoPropostaSQLiteServices = Depends(get_gerenciamentoPropostaSQLite_service)):
    try:
        gerencimentoProposta = await service.update_gerenciamentoProposta(gerenciamentoProposta_id, gerenciamentoProposta_data)

        return gerencimentoProposta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.post('/gerenciamentoProposta/{gerenciamentoProposta_id}/Comentario')
async def create_gerenciamentoPropostaComentario(gerenciamentoProposta_id: int, gerenciamentoComentarioDTO: GerenciamentoComentarioDTO, service: GerenciamentoPropostaSQLiteServices = Depends(get_gerenciamentoPropostaSQLite_service)):
    gerenciamentoComentario = await service.create_gerenciamentoPropostaComentario(gerenciamentoProposta_id, gerenciamentoComentarioDTO)

    return gerenciamentoComentario


"""
def get_gerenciamentoProposta_service() -> GerenciamentoPropostaServices:
    repository = GerenciamentoPropostaInMemoryRepository(database)
    return GerenciamentoPropostaServices(repository)


def get_gerenciamentoComentario_service() -> GerenciamentoComentarioServices:
    repository = GerenciamentoComentarioInMemoryRepository(database)
    return GerenciamentoComentarioServices(repository)

@router.get('/GerenciamentoProposta/', response_model=GerenciamentoPropostaListResponse)
async def get_gerenciamentoPropostas(service: GerenciamentoPropostaServices = Depends(get_gerenciamentoProposta_service)):
    gerenciamentoPropostas = await service.get_gerenciamentoProposta()

    return gerenciamentoPropostas


@router.get('/GerenciamentoProposta/{gerenciamentoProposta_id}', response_model=GerenciamentoProposta)
async def get_gerenciamentoProposta_by_id(gerenciamentoProposta_id: uuid.UUID, service: GerenciamentoPropostaServices = Depends(get_gerenciamentoProposta_service)):
    gerenciamentoProposta = await service.get_gerenciamentoProposta_by_id(gerenciamentoProposta_id)
    if gerenciamentoProposta is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    return gerenciamentoProposta


@router.post('/GerenciamentoProposta/', response_model=GerenciamentoProposta)
async def create_gerenciamentoProposta(gerenciamentoProposta_data: GerenciamentoPropostaDTO, service: GerenciamentoPropostaServices = Depends(get_gerenciamentoProposta_service)):
    gerenciamentoProposta = await service.create_gerenciamentoProposta(gerenciamentoProposta_data)

    return gerenciamentoProposta


@router.put('/gerenciamentoProposta/', response_model=GerenciamentoPropostaDTO)
async def update_gerenciamentoProposta(
    gerenciamentoProposta_id: uuid.UUID, gerenciamentoProposta_data: GerenciamentoPropostaDTO, service: GerenciamentoPropostaServices = Depends(get_gerenciamentoProposta_service)
):
    update = await service.update_gerenciamentoProposta(gerenciamentoProposta_id, gerenciamentoProposta_data)
    if update is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    return update


@router.delete('/GerenciamentoProposta/')
async def delete_gerenciamentoProposta(gerenciamentoProposta_id: uuid.UUID, service: GerenciamentoPropostaServices = Depends(get_gerenciamentoProposta_service)):
    delete = await service.delete_gerenciamentoProposta(gerenciamentoProposta_id)
    if delete:
        return {'message': 'Gerenciamento Proposta deletada'}

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')


@router.get('/gerenciamentoComentario/{gerenciamentoProposta_id}/{gerenciamentoComentario_id}')
async def get_gerenciamentoCometarios(service: GerenciamentoPropostaServices = Depends(get_gerenciamentoComentario_service)): ...


@router.post('/gerenciamentoProposta/{gerenciamentoProposta_id}/Comentario')
async def create_gerenciamentoPropostaComentario(
    gerenciamentoProposta_id: uuid.UUID, gerenciamentoComentarioDTO: GerenciamentoComentarioDTO, service: GerenciamentoPropostaServices = Depends(get_gerenciamentoProposta_service)
):
    gerenciamentoComentario = gerenciamentoComentarioDTO
    gerenciamentoComentario = await service.create_gerenciamentoPropostaComentario(gerenciamentoProposta_id, gerenciamentoComentario)

    return gerenciamentoComentario
"""
