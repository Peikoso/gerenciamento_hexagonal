from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from gerenciamento_hexagonal.application.dependencies import get_gerenciamento_contrapartida_admin_service
from gerenciamento_hexagonal.application.services import GerenciamentoContrapartidaAdminServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoContrapartidaAdmin
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import GerenciamentoContrapartidaAdminDTO
router = APIRouter()


Service = Annotated[GerenciamentoContrapartidaAdminServices, Depends(get_gerenciamento_contrapartida_admin_service)]


@router.get('/', response_model=list[GerenciamentoContrapartidaAdmin])
async def get_gerenciamento_contrapartida_admins(service: Service):
    gerenciamento_contrapartida_admin = await service.get_gerenciamento_contrapartida_admin()

    return gerenciamento_contrapartida_admin


@router.get('/{gerenciamento_contrapartida_admin_id}', response_model=GerenciamentoContrapartidaAdmin)
async def get_gerenciamento_contrapartida_admin_by_id(gerenciamento_contrapartida_admin_id: int, service: Service):
    try:
        gerenciamento_contrapartida_admin = await service.get_gerenciamento_contrapartida_admin_by_id(gerenciamento_contrapartida_admin_id)

        return gerenciamento_contrapartida_admin

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.post('/{gerenciamento_contrapartida_id}', response_model=GerenciamentoContrapartidaAdmin)
async def create_gerenciamento_contrapartida_admin(gerenciamento_contrapartida_id: int, gerenciamento_contrapartida_admin: GerenciamentoContrapartidaAdminDTO, service: Service):
    try:
        gerenciamento_contrapartida_admin = await service.create_gerenciamento_contrapartida_admin(gerenciamento_contrapartida_id, gerenciamento_contrapartida_admin)

        return gerenciamento_contrapartida_admin

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.put('/{gerenciamento_contrapartida_admin_id}', response_model=GerenciamentoContrapartidaAdmin)
async def update_gerenciamento_contrapartida_admin(gerenciamento_contrapartida_admin_id: int, gerenciamento_contrapartida_admin: GerenciamentoContrapartidaAdminDTO, service: Service):
    try:
        gerenciamento_contrapartida_admin = await service.update_gerenciamento_contrapartida_admin(gerenciamento_contrapartida_admin_id, gerenciamento_contrapartida_admin)

        return gerenciamento_contrapartida_admin

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete('/{gerenciamento_contrapartida_admin_id}')
async def delete_gerenciamento_contrapartida_admin(gerenciamento_contrapartida_admin_id: int, service: Service):
    try:
        result = await service.delete_gerenciamento_contrapartida_admin(gerenciamento_contrapartida_admin_id)

        return result

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
