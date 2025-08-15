from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import DomainValidationError, NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoContrapartidaAdmin
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoContrapartidaAdminDTO
from gerenciamento_hexagonal.infrastructure.handler.annotated import Service_Contrapartida_Admin

router = APIRouter()


@router.get('/', response_model=list[GerenciamentoContrapartidaAdmin])
async def get_gerenciamento_contrapartida_admins(service: Service_Contrapartida_Admin):
    gerenciamento_contrapartida_admin = await service.get_gerenciamento_contrapartida_admin()

    return gerenciamento_contrapartida_admin


@router.get('/{gerenciamento_contrapartida_admin_id}', response_model=GerenciamentoContrapartidaAdmin)
async def get_gerenciamento_contrapartida_admin_by_id(gerenciamento_contrapartida_admin_id: int, service: Service_Contrapartida_Admin):
    try:
        gerenciamento_contrapartida_admin = await service.get_gerenciamento_contrapartida_admin_by_id(gerenciamento_contrapartida_admin_id)

        return gerenciamento_contrapartida_admin

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.post('/{gerenciamento_contrapartida_id}', response_model=GerenciamentoContrapartidaAdmin)
async def create_gerenciamento_contrapartida_admin(gerenciamento_contrapartida_id: int, gerenciamento_contrapartida_admin: GerenciamentoContrapartidaAdminDTO, service: Service_Contrapartida_Admin):
    try:
        gerenciamento_contrapartida_admin = await service.create_gerenciamento_contrapartida_admin(gerenciamento_contrapartida_id, gerenciamento_contrapartida_admin)

        return gerenciamento_contrapartida_admin

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except DomainValidationError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))


@router.put('/{gerenciamento_contrapartida_admin_id}', response_model=GerenciamentoContrapartidaAdmin)
async def update_gerenciamento_contrapartida_admin(gerenciamento_contrapartida_admin_id: int, gerenciamento_contrapartida_admin: GerenciamentoContrapartidaAdminDTO, service: Service_Contrapartida_Admin):
    try:
        gerenciamento_contrapartida_admin = await service.update_gerenciamento_contrapartida_admin(gerenciamento_contrapartida_admin_id, gerenciamento_contrapartida_admin)

        return gerenciamento_contrapartida_admin

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except DomainValidationError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))


@router.delete('/{gerenciamento_contrapartida_admin_id}')
async def delete_gerenciamento_contrapartida_admin(gerenciamento_contrapartida_admin_id: int, service: Service_Contrapartida_Admin):
    try:
        result = await service.delete_gerenciamento_contrapartida_admin(gerenciamento_contrapartida_admin_id)

        return result

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
