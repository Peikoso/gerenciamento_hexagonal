from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoComentario
from gerenciamento_hexagonal.domain.repositories.gerenciamento import GerenciamentoComentarioRepository
from gerenciamento_hexagonal.infrastructure.database.models.gerenciamento_orm import GerenciamentoComentarioModel
from gerenciamento_hexagonal.infrastructure.database.sqlalchemyConfig import get_session
from sqlalchemy import select


class GerenciamentoComentarioRepository(GerenciamentoComentarioRepository):
    async def get_gerenciamento_comentario(self) -> list[GerenciamentoComentario]:
        async with get_session() as session:
            db_gerenciamento_comentarios = await session.scalars(select(GerenciamentoComentarioModel))

            result = [GerenciamentoComentario.model_validate(vars(db_gerenciamento_comentario)) for db_gerenciamento_comentario in db_gerenciamento_comentarios if db_gerenciamento_comentario is not None]

            return result

    async def get_gerenciamento_comentario_by_id(self, gerenciamento_comentario_id: int) -> GerenciamentoComentario | None:
        async with get_session() as session:
            db_gerenciamento_comentario = await session.scalar(select(GerenciamentoComentarioModel).where(GerenciamentoComentarioModel.id == gerenciamento_comentario_id))
            if db_gerenciamento_comentario:
                return GerenciamentoComentario.model_validate(vars(db_gerenciamento_comentario))

            return None

    async def create_gerenciamento_comentario(self, gerenciamento_comentario: GerenciamentoComentario) -> GerenciamentoComentarioModel:
        async with get_session() as session:
            db_gerenciamento_comentario = GerenciamentoComentarioModel(comentario=gerenciamento_comentario.comentario)
            session.add(db_gerenciamento_comentario)
            await session.commit()
            await session.refresh(db_gerenciamento_comentario)

            return db_gerenciamento_comentario

    async def update_gerenciamento_comentario(self, gerenciamento_comentario_id, gerenciamento_comentario: GerenciamentoComentario) -> GerenciamentoComentario:
        async with get_session() as session:
            db_gerenciamento_comentario = await session.scalar(select(GerenciamentoComentarioModel).where(GerenciamentoComentarioModel.id == gerenciamento_comentario_id))

            db_gerenciamento_comentario.comentario = gerenciamento_comentario.comentario

            await session.commit()
            await session.refresh(db_gerenciamento_comentario)

            return GerenciamentoComentario.model_validate(vars(db_gerenciamento_comentario))

    async def delete_gerenciamento_comentario(self, gerenciamento_comentario_id: int):
        async with get_session() as session:
            db_gerenciamento_comentario = await session.scalar(select(GerenciamentoComentarioModel).where(GerenciamentoComentarioModel.id == gerenciamento_comentario_id))

            await session.delete(db_gerenciamento_comentario)
            await session.commit()
