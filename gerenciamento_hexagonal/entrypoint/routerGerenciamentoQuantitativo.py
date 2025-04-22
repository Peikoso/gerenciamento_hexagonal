from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from gerenciamento_hexagonal.application.servicesSQLite import GerenciamentoQuantitativoSQLiteServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoQuantitativo
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import GerenciamentoComentarioDTO, GerenciamentoQuantitativoDTO, GerenciamentoQuantitativoListResponse
from gerenciamento_hexagonal.infrastructure.repositories.SQLiterepository import GerenciamentoComentarioSQLiteRepository, GerenciamentoQuantitativoSQLiteRepository


router = APIRouter()

def get_gerenciamentoQuantitativoSQLite_Service() -> GerenciamentoQuantitativoSQLiteServices:
    gerenciamentoComentario_repository = GerenciamentoComentarioSQLiteRepository()
    gerenciamentoQuantitativo_repository = GerenciamentoQuantitativoSQLiteRepository(gerenciamentoComentario_repository)
    return GerenciamentoQuantitativoSQLiteServices(gerenciamentoQuantitativo_repository)


@router.get('/', response_model=GerenciamentoQuantitativoListResponse)
async def get_gerenciamentoQuantitativos(service: GerenciamentoQuantitativoSQLiteServices = Depends(get_gerenciamentoQuantitativoSQLite_Service)):
    gerenciamentoQuantitativos = await service.get_gerenciamentoQuantitativo()
    
    return {'Gerenciamento_Quantitativos': gerenciamentoQuantitativos}

@router.get('/{gerenciamentoQuantitativo_id}', response_model=GerenciamentoQuantitativo)
async def get_gerenciamentoQuantitativo_by_id(gerenciamentoQuantitativo_id: int, service: GerenciamentoQuantitativoSQLiteServices = Depends(get_gerenciamentoQuantitativoSQLite_Service)):
    try:
        gerenciamentoQuantitativo = await service.get_gerenciamentoQuantitativo_by_id(gerenciamentoQuantitativo_id)
        
        return gerenciamentoQuantitativo
    
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

@router.post('/{gerenciamentoProposta_id}', response_model=GerenciamentoQuantitativo)
async def create_gerenciamentoQuantitativo(
    gerenciamentoProposta_id: int, gerenciamentoQuantitativo: GerenciamentoQuantitativoDTO, service: GerenciamentoQuantitativoSQLiteServices  = Depends(get_gerenciamentoQuantitativoSQLite_Service)
):
    try:
        gerenciamentoQuantitativo = await service.create_gerenciamentoQuantitativo(gerenciamentoProposta_id, gerenciamentoQuantitativo)
        
        return gerenciamentoQuantitativo
    
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
    
@router.post('/Comentario/{gerenciamentoQuantitativo_id}', response_model=GerenciamentoQuantitativo)
async def create_gerenciamentoQuantitativoComentario(gerenciamentoQuantitativo_id: int, gerenciamentoComentario: GerenciamentoComentarioDTO, service: GerenciamentoQuantitativoSQLiteServices = Depends(get_gerenciamentoQuantitativoSQLite_Service)):
    try:
        gerenciamentoQuantitativoComentario = await service.create_gerenciamentoQuantitativoComentario(gerenciamentoQuantitativo_id, gerenciamentoComentario)
        
        return gerenciamentoQuantitativoComentario
    
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
    
@router.put('/{gerenciamentoQuantitativo_id}', response_model=GerenciamentoQuantitativo)
async def update_gerenciamentoQuantitativo(gerenciamentoQuantitativo_id: int, gerenciamentoQuantitativo: GerenciamentoQuantitativoDTO, service: GerenciamentoQuantitativoSQLiteServices = Depends(get_gerenciamentoQuantitativoSQLite_Service)):
    try:
        gerenciamentoQuantitativo = await service.update_gerenciamentoQuantitativo(gerenciamentoQuantitativo_id, gerenciamentoQuantitativo)
        
        return gerenciamentoQuantitativo
    
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
    
@router.delete('/{gerenciamentoQuantitativo_id}')
async def delete_gerenciamentoQuantitativo(gerenciamentoQuantitativo_id: int, service: GerenciamentoQuantitativoSQLiteServices = Depends(get_gerenciamentoQuantitativoSQLite_Service)):
    try:
        result = await service.delete_gerenciamentoQuantitativo(gerenciamentoQuantitativo_id)
        
        return result
    
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))