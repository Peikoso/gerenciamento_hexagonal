from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoComentario, GerenciamentoQuantitativo
from gerenciamento_hexagonal.domain.repositories.gerenciamento import GerenciamentoComentarioRepository, GerenciamentoQuantitativoRepository
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.models.gerenciamento_orm import GerenciamentoCaracterizacaoModel, GerenciamentoQuantitativoModel
from gerenciamento_hexagonal.infrastructure.database.sqlalchemyConfig import get_session
from sqlalchemy import select


class GerenciamentoQuantitativoRepository(GerenciamentoQuantitativoRepository):
    def __init__(self, gerenciamento_comentario_repository: GerenciamentoComentarioRepository):
        self.gerenciamento_comentario_repository = gerenciamento_comentario_repository

    async def get_gerenciamento_quantitativo(self) -> list[GerenciamentoQuantitativo]:
        async with get_session() as session:
            db_gerenciamento_quantitativos = await session.scalars(select(GerenciamentoQuantitativoModel))

            result = [GerenciamentoQuantitativo.model_validate({**vars(db_gerenciamento_quantitativo), 'comentarios': [GerenciamentoComentario.model_validate(vars(gerenciamento_comentario)) for gerenciamento_comentario in db_gerenciamento_quantitativo.comentarios]}) for db_gerenciamento_quantitativo in db_gerenciamento_quantitativos if db_gerenciamento_quantitativo is not None]

            return result

    async def get_gerenciamento_quantitativo_by_id(self, gerenciamento_quantitativo_id: int) -> GerenciamentoQuantitativo | None:
        async with get_session() as session:
            db_gerenciamento_quantitativo = await session.scalar(select(GerenciamentoQuantitativoModel).where(GerenciamentoQuantitativoModel.id == gerenciamento_quantitativo_id))

            if not db_gerenciamento_quantitativo:
                return None

            result = GerenciamentoQuantitativo.model_validate({**vars(db_gerenciamento_quantitativo), 'comentarios': [GerenciamentoComentario.model_validate(vars(gerenciamento_comentario)) for gerenciamento_comentario in db_gerenciamento_quantitativo.comentarios]})

            return result

    async def create_gerenciamento_quantitativo(self, gerenciamento_proposta_id: int, gerenciamento_quantitativo: GerenciamentoQuantitativo) -> GerenciamentoQuantitativo:
        async with get_session() as session:
            db_gerenciamento_quantitativo = GerenciamentoQuantitativoModel(
                educacao_financeira_alcancados=gerenciamento_quantitativo.educacao_financeira_alcancados,
                educacao_financeira_impactados=gerenciamento_quantitativo.educacao_financeira_impactados,
                geracao_renda_postos_trabalho_gerados=gerenciamento_quantitativo.geracao_renda_postos_trabalho_gerados,
                alcance_marca_pessoas_alcancadas_publicacao_digitais=gerenciamento_quantitativo.alcance_marca_pessoas_alcancadas_publicacao_digitais,
                pessoas_alcancadas=gerenciamento_quantitativo.pessoas_alcancadas,
                pessoas_impactadas=gerenciamento_quantitativo.pessoas_impactadas,
                gerenciamento_proposta_id=gerenciamento_proposta_id,
            )

            session.add(db_gerenciamento_quantitativo)
            await session.commit()
            await session.refresh(db_gerenciamento_quantitativo)

            return GerenciamentoQuantitativo.model_validate(vars(db_gerenciamento_quantitativo))

    async def update_gerenciamento_quantitativo(self, gerenciamento_quantitativo_id: int, gerenciamento_quantitativo: GerenciamentoQuantitativo) -> GerenciamentoQuantitativo:
        async with get_session() as session:
            db_gerenciamento_quantitativo = await session.scalar(select(GerenciamentoQuantitativoModel).where(GerenciamentoQuantitativoModel.id == gerenciamento_quantitativo_id))

            db_gerenciamento_quantitativo.educacao_financeira_alcancados = gerenciamento_quantitativo.educacao_financeira_alcancados
            db_gerenciamento_quantitativo.educacao_financeira_impactados = gerenciamento_quantitativo.educacao_financeira_impactados
            db_gerenciamento_quantitativo.geracao_renda_postos_trabalho_gerados = gerenciamento_quantitativo.geracao_renda_postos_trabalho_gerados
            db_gerenciamento_quantitativo.alcance_marca_pessoas_alcancadas_publicacao_digitais = gerenciamento_quantitativo.alcance_marca_pessoas_alcancadas_publicacao_digitais
            db_gerenciamento_quantitativo.pessoas_alcancadas = gerenciamento_quantitativo.pessoas_alcancadas
            db_gerenciamento_quantitativo.pessoas_impactadas = gerenciamento_quantitativo.pessoas_impactadas

            await session.commit()
            await session.refresh(db_gerenciamento_quantitativo)

            return GerenciamentoQuantitativo.model_validate({**vars(db_gerenciamento_quantitativo), 'comentarios': [GerenciamentoComentario.model_validate(vars(gerenciamento_comentario)) for gerenciamento_comentario in db_gerenciamento_quantitativo.comentarios]})

    async def delete_gerenciamento_quantitativo(self, gerenciamento_quantitativo_id: int):
        async with get_session() as session:
            db_gerenciamento_quantitativo = await session.scalar(select(GerenciamentoQuantitativoModel).where(GerenciamentoQuantitativoModel.id == gerenciamento_quantitativo_id))

            await session.delete(db_gerenciamento_quantitativo)
            await session.commit()

    async def create_gerenciamento_quantitativo_comentario(self, gerenciamento_quantitativo_id: int, gerenciamento_comentario: GerenciamentoComentario) -> GerenciamentoQuantitativo:
        async with get_session() as session:
            db_gerenciamento_quantitativo = await session.scalar(select(GerenciamentoQuantitativoModel).where(GerenciamentoQuantitativoModel.id == gerenciamento_quantitativo_id))

            db_gerenciamento_comentario = await self.gerenciamento_comentario_repository.create_gerenciamento_comentario(gerenciamento_comentario)

            if db_gerenciamento_comentario not in session:
                session.add(db_gerenciamento_comentario)

            db_gerenciamento_quantitativo.comentarios.append(db_gerenciamento_comentario)

            session.add(db_gerenciamento_quantitativo)
            await session.commit()
            await session.refresh(db_gerenciamento_quantitativo)

            return GerenciamentoQuantitativo.model_validate({**vars(db_gerenciamento_quantitativo), 'comentarios': [GerenciamentoComentario.model_validate(vars(gerenciamento_comentario)) for gerenciamento_comentario in db_gerenciamento_quantitativo.comentarios]})

    async def checar_gerenciamento_caracterizacao_exists(self, gerenciamento_quantitativo_id: int) -> bool:
        async with get_session() as session:
            db_gerenciamento_caracterizacao = await session.scalar(select(GerenciamentoCaracterizacaoModel).where(GerenciamentoCaracterizacaoModel.gerenciamento_quantitativo_id == gerenciamento_quantitativo_id))

            if db_gerenciamento_caracterizacao:
                return True

            return False
