from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoComentario, GerenciamentoQualitativo
from gerenciamento_hexagonal.domain.repositories.gerenciamento import GerenciamentoComentarioRepository, GerenciamentoQualitativoRepository
from gerenciamento_hexagonal.infrastructure.database.sqlalchemyConfig import get_session
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.models.gerenciamento_orm import GerenciamentoQualitativoModel
from sqlalchemy import select


class GerenciamentoQualitativoRepository(GerenciamentoQualitativoRepository):
    def __init__(self, gerenciamento_comentario_repository: GerenciamentoComentarioRepository):
        self.gerenciamento_comentario_repository = gerenciamento_comentario_repository

    async def get_gerenciamento_qualitativo(self) -> list[GerenciamentoQualitativo]:
        async with get_session() as session:
            db_gerenciamento_qualitativos = await session.scalars(select(GerenciamentoQualitativoModel))

            result = [
                GerenciamentoQualitativo.model_validate({**vars(db_gerenciamento_qualitativo), 'comentarios': [GerenciamentoComentario.model_validate(vars(gerenciamento_comentario)) for gerenciamento_comentario in db_gerenciamento_qualitativo.comentarios], 'arquivos_ids': [arquivo.arquivo_id for arquivo in db_gerenciamento_qualitativo.arquivos]})
                for db_gerenciamento_qualitativo in db_gerenciamento_qualitativos
                if db_gerenciamento_qualitativo is not None
            ]

            return result

    async def get_gerenciamento_qualitativo_by_id(self, gerenciamento_qualitativo_id: int) -> GerenciamentoQualitativo | None:
        async with get_session() as session:
            db_gerenciamento_qualitativo = await session.scalar(select(GerenciamentoQualitativoModel).where(GerenciamentoQualitativoModel.id == gerenciamento_qualitativo_id))

            if not db_gerenciamento_qualitativo:
                return None

            result = GerenciamentoQualitativo.model_validate({**vars(db_gerenciamento_qualitativo), 'comentarios': [GerenciamentoComentario.model_validate(vars(comentario)) for comentario in db_gerenciamento_qualitativo.comentarios], 'arquivos_ids': [arquivo.arquivo_id for arquivo in db_gerenciamento_qualitativo.arquivos]})

            return result

    async def create_gerenciamento_qualitativo(self, gerenciamento_proposta_id: int, gerenciamento_qualitativo: GerenciamentoQualitativo) -> GerenciamentoQualitativo:
        async with get_session() as session:
            db_gerenciamento_qualitativo = GerenciamentoQualitativoModel(acoes_previstas=gerenciamento_qualitativo.acoes_previstas, acoes_realizadas=gerenciamento_qualitativo.acoes_realizadas, visao_proponente=gerenciamento_qualitativo.visao_proponente, gerenciamento_proposta_id=gerenciamento_proposta_id)

            session.add(db_gerenciamento_qualitativo)
            await session.commit()
            await session.refresh(db_gerenciamento_qualitativo)

            return GerenciamentoQualitativo.model_validate(vars(db_gerenciamento_qualitativo))

    async def update_gerenciamento_qualitativo(self, gerenciamento_qualitativo_id: int, gerenciamento_qualitativo: GerenciamentoQualitativo) -> GerenciamentoQualitativo:
        async with get_session() as session:
            db_gerenciamento_qualitativo = await session.scalar(select(GerenciamentoQualitativoModel).where(GerenciamentoQualitativoModel.id == gerenciamento_qualitativo_id))

            db_gerenciamento_qualitativo.acoes_previstas = gerenciamento_qualitativo.acoes_previstas
            db_gerenciamento_qualitativo.acoes_realizadas = gerenciamento_qualitativo.acoes_realizadas
            db_gerenciamento_qualitativo.visao_proponente = gerenciamento_qualitativo.visao_proponente

            await session.commit()
            await session.refresh(db_gerenciamento_qualitativo)

            result = GerenciamentoQualitativo.model_validate({**vars(db_gerenciamento_qualitativo), 'comentarios': [GerenciamentoComentario.model_validate(vars(comentario)) for comentario in db_gerenciamento_qualitativo.comentarios]})

            return result

    async def delete_gerenciamento_qualitativo(self, gerenciamento_qualitativo_id: int):
        async with get_session() as session:
            db_gerenciamento_qualitativo = await session.scalar(select(GerenciamentoQualitativoModel).where(GerenciamentoQualitativoModel.id == gerenciamento_qualitativo_id))

            await session.delete(db_gerenciamento_qualitativo)
            await session.commit()

    async def create_gerenciamento_qualitativo_comentario(self, gerenciamento_qualitativo_id: int, gerenciamento_comentario: GerenciamentoComentario) -> GerenciamentoQualitativo:
        async with get_session() as session:
            db_gerenciamento_qualitativo = await session.scalar(select(GerenciamentoQualitativoModel).where(GerenciamentoQualitativoModel.id == gerenciamento_qualitativo_id))

            db_gerenciamento_comentario = await self.gerenciamento_comentario_repository.create_gerenciamento_comentario(gerenciamento_comentario)

            if db_gerenciamento_comentario not in session:
                session.add(db_gerenciamento_comentario)

            db_gerenciamento_qualitativo.comentarios.append(db_gerenciamento_comentario)

            session.add(db_gerenciamento_qualitativo)
            await session.commit()
            await session.refresh(db_gerenciamento_qualitativo)

            result = GerenciamentoQualitativo.model_validate({**vars(db_gerenciamento_qualitativo), 'comentarios': [GerenciamentoComentario.model_validate(vars(comentario)) for comentario in db_gerenciamento_qualitativo.comentarios]})

            return result
