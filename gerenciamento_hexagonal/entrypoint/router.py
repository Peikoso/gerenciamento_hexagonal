import uuid
from http import HTTPStatus

from application.services import GerenciamentoPropostaServices
from domain.models.gerenciamento import GerenciamentoProposta, GerenciamentoPropostaDTO, GerenciamentoPropostaListResponse
from fastapi import APIRouter, Depends, HTTPException
from infrastructure.database import Database
from infrastructure.repositories.gerenciamentorepository import GerenciamentoPropostaInMemoryRepository

router = APIRouter()

database = Database()


def get_gerenciamentoProposta_service() -> GerenciamentoPropostaServices:
    repository = GerenciamentoPropostaInMemoryRepository(database)
    return GerenciamentoPropostaServices(repository)


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
    if not gerenciamentoProposta:
        raise HTTPException(status_code=400, detail='Proposta não criada')
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
