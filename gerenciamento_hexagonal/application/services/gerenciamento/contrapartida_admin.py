from gerenciamento_hexagonal.application.services.interfaces.gerenciamento.contrapartida_admin import GerenciamentoContrapartidaAdminServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoContrapartidaAdmin
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoContrapartidaAdminDTO


class GerenciamentoContrapartidaAdminServicesImpl(GerenciamentoContrapartidaAdminServices):
    async def get_gerenciamento_contrapartida_admin(self) -> list[GerenciamentoContrapartidaAdmin]:
        gerenciamento_contrapartida_admins = await self.repository.get_gerenciamento_contrapartida_admin()

        return gerenciamento_contrapartida_admins

    async def get_gerenciamento_contrapartida_admin_by_id(self, gerenciamento_contrapartida_admin_id: int) -> GerenciamentoContrapartidaAdmin | None:
        gerenciamento_contrapartida_admin = await self.repository.get_gerenciamento_contrapartida_admin_by_id(gerenciamento_contrapartida_admin_id)

        if not gerenciamento_contrapartida_admin:
            raise NotFoundError(f'gerenciamento_contrapartida_admin with ID: {gerenciamento_contrapartida_admin_id} not found')

        return gerenciamento_contrapartida_admin

    async def create_gerenciamento_contrapartida_admin(self, gerenciamento_contrapartida_id: int, gerenciamento_contrapartida_admin: GerenciamentoContrapartidaAdminDTO) -> GerenciamentoContrapartidaAdmin:
        await self.verify.gerenciamento_contrapartida_exists(gerenciamento_contrapartida_id)

        gerenciamento_contrapartida_admin = GerenciamentoContrapartidaAdmin(gerenciamento_contrapartida_id=gerenciamento_contrapartida_id, **gerenciamento_contrapartida_admin.model_dump())
        gerenciamento_contrapartida_admin = await self.repository.create_gerenciamento_contrapartida_admin(gerenciamento_contrapartida_admin)

        return gerenciamento_contrapartida_admin

    async def update_gerenciamento_contrapartida_admin(self, gerenciamento_contrapartida_admin_id: int, gerenciamento_contrapartida_admin: GerenciamentoContrapartidaAdmin) -> GerenciamentoContrapartidaAdmin:
        await self.service_contrapartida.get_gerenciamento_contrapartida_by_id(gerenciamento_contrapartida_admin_id)

        gerenciamento_contrapartida_admin = GerenciamentoContrapartidaAdmin(**gerenciamento_contrapartida_admin.model_dump())
        gerenciamento_contrapartida_admin = await self.repository.update_gerenciamento_contrapartida_admin(gerenciamento_contrapartida_admin_id, gerenciamento_contrapartida_admin)

        return gerenciamento_contrapartida_admin

    async def delete_gerenciamento_contrapartida_admin(self, gerenciamento_contrapartida_admin_id: int):
        await self.service_contrapartida.get_gerenciamento_contrapartida_by_id(gerenciamento_contrapartida_admin_id)

        await self.repository.delete_gerenciamento_contrapartida_admin(gerenciamento_contrapartida_admin_id)

        return {'message': f'gerenciamento_contrapartida with ID {gerenciamento_contrapartida_admin_id} deleted'}
