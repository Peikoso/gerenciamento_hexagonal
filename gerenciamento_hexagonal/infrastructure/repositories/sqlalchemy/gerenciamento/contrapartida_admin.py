from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoContrapartidaAdmin
from gerenciamento_hexagonal.domain.repositories.gerenciamento import GerenciamentoContrapartidaAdminRepository
from gerenciamento_hexagonal.infrastructure.database.models.gerenciamento_orm import (
    GerenciamentoContrapartidaAdminModel,
)
from gerenciamento_hexagonal.infrastructure.database.sqlalchemyConfig import get_session
from sqlalchemy import select


class GerenciamentoContrapartidaAdminRepository(GerenciamentoContrapartidaAdminRepository):
    async def get_gerenciamento_contrapartida_admin(self) -> list[GerenciamentoContrapartidaAdmin]:
        async with get_session() as session:
            db_gerenciamento_contrapartida_admins = await session.scalars(select(GerenciamentoContrapartidaAdminModel))

            return [GerenciamentoContrapartidaAdmin.model_validate(vars(db_gerenciamento_contrapartida_admin)) for db_gerenciamento_contrapartida_admin in db_gerenciamento_contrapartida_admins]

    async def get_gerenciamento_contrapartida_admin_by_id(self, gerenciamento_contrapartida_admin_id: int) -> GerenciamentoContrapartidaAdmin | None:
        async with get_session() as session:
            db_gerenciamento_contrapartida_admin = await session.scalar(select(GerenciamentoContrapartidaAdminModel).where(GerenciamentoContrapartidaAdminModel.id == gerenciamento_contrapartida_admin_id))

            if not db_gerenciamento_contrapartida_admin:
                return None

            return GerenciamentoContrapartidaAdmin.model_validate(vars(db_gerenciamento_contrapartida_admin))

    async def create_gerenciamento_contrapartida_admin(self, gerenciamento_contrapartida_admin: GerenciamentoContrapartidaAdmin) -> GerenciamentoContrapartidaAdmin:
        async with get_session() as session:
            db_gerenciamento_contrapartida_admin = GerenciamentoContrapartidaAdminModel(quantidade=gerenciamento_contrapartida_admin.quantidade, justificativa=gerenciamento_contrapartida_admin.justificativa, data=gerenciamento_contrapartida_admin.data, gerenciamento_contrapartida_id=gerenciamento_contrapartida_admin.gerenciamento_contrapartida_id)

            session.add(db_gerenciamento_contrapartida_admin)
            await session.commit()
            await session.refresh(db_gerenciamento_contrapartida_admin)

            return GerenciamentoContrapartidaAdmin.model_validate(vars(db_gerenciamento_contrapartida_admin))

    async def update_gerenciamento_contrapartida_admin(self, gerenciamento_contrapartida_admin_id: int, gerenciamento_contrapartida_admin: GerenciamentoContrapartidaAdmin) -> GerenciamentoContrapartidaAdmin:
        async with get_session() as session:
            db_gerenciamento_contrapartida_admin = await session.scalar(select(GerenciamentoContrapartidaAdminModel).where(GerenciamentoContrapartidaAdminModel.id == gerenciamento_contrapartida_admin_id))

            db_gerenciamento_contrapartida_admin.quantidade = gerenciamento_contrapartida_admin.quantidade
            db_gerenciamento_contrapartida_admin.justificativa = gerenciamento_contrapartida_admin.justificativa
            db_gerenciamento_contrapartida_admin.data = gerenciamento_contrapartida_admin.data

            await session.commit()
            await session.refresh(db_gerenciamento_contrapartida_admin)

            return GerenciamentoContrapartidaAdmin.model_validate(vars(db_gerenciamento_contrapartida_admin))

    async def delete_gerenciamento_contrapartida_admin(self, gerenciamento_contrapartida_admin_id: int):
        async with get_session() as session:
            db_gerenciamento_contrapartida_admin = await session.scalar(select(GerenciamentoContrapartidaAdminModel).where(GerenciamentoContrapartidaAdminModel.id == gerenciamento_contrapartida_admin_id))

            await session.delete(db_gerenciamento_contrapartida_admin)
            await session.commit()
