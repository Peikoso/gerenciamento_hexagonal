from sqlalchemy import select
from sqlalchemy.orm import selectinload

from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoComentario, GerenciamentoMeta, GerenciamentoProposta
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import GerenciamentoComentarioDTO, GerenciamentoMetaDTO, RelatorioResponse
from gerenciamento_hexagonal.domain.repositories.gerenciamento import (
    GerenciamentoComentarioRepository,
    GerenciamentoMetaRepository,
    GerenciamentoPropostaRepository,
)
from gerenciamento_hexagonal.infrastructure.database.models.gerenciamentoORM import GerenciamentoComentarioModel, GerenciamentoMetaModel, GerenciamentoPropostaModel
from gerenciamento_hexagonal.infrastructure.database.SQLiteConfig import get_session


class RelatorioSQLiteRepository:
    async def get_relatorio(self, gerenciamentoProposta_id: int) -> RelatorioResponse:
        async with get_session() as session:
            relatorio = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id == gerenciamentoProposta_id))
            
            if not relatorio:
                return None
            
        return RelatorioResponse(
            proposta_id=relatorio.proposta_id,
            trimestre_de_referencia=relatorio.trimestre_de_referencia,
            tipo=relatorio.tipo,
            gerenciamento_metas=[
                GerenciamentoMetaDTO(
                    ordem=gerenciamentoMeta.ordem,
                    alcancado=gerenciamentoMeta.alcancado
                )
                for gerenciamentoMeta in relatorio.gerenciamentoMetas
            ]
            
        )

class GerenciamentoComentarioSQLiteRepository(GerenciamentoComentarioRepository):
    async def get_gerenciamentoComentario(self) -> list[GerenciamentoComentario]:
        async with get_session() as session:
            db_gerenciamentoComentarios = await session.scalars(select(GerenciamentoComentarioModel))

            result = [GerenciamentoComentario.model_validate({**vars(db_gerenciamentoComentario)}) for db_gerenciamentoComentario in db_gerenciamentoComentarios if db_gerenciamentoComentario is not None]

            return result

    async def get_gerenciamentoComentario_by_id(self, gerenciamentoComentario_id: int) -> GerenciamentoComentario:
        async with get_session() as session:
            db_gerenciamentoComentario = await session.scalar(select(GerenciamentoComentarioModel).where(GerenciamentoComentarioModel.id == gerenciamentoComentario_id))
            if db_gerenciamentoComentario:
                return GerenciamentoComentario.model_validate(vars(db_gerenciamentoComentario))

            return None

    async def create_gerenciamentoComentario(self, gerenciamentoComentario: GerenciamentoComentario) -> GerenciamentoComentarioModel:
        async with get_session() as session:
            db_gerenciamentoComentario = GerenciamentoComentarioModel(comentario=gerenciamentoComentario.comentario)
            session.add(db_gerenciamentoComentario)
            await session.commit()
            await session.refresh(db_gerenciamentoComentario)

            return db_gerenciamentoComentario

    async def update_gerenciamentoComentario(self, gerenciamentoComentario_id, gerenciamentoComentario_data: GerenciamentoComentarioDTO) -> GerenciamentoComentario:
        async with get_session() as session:
            db_gerenciamentoComentario = await session.scalar(select(GerenciamentoComentarioModel).where(GerenciamentoComentarioModel.id == gerenciamentoComentario_id))

            if db_gerenciamentoComentario:
                db_gerenciamentoComentario.comentario = gerenciamentoComentario_data.comentario

                await session.commit()
                await session.refresh(db_gerenciamentoComentario)

                return GerenciamentoComentario.model_validate(vars(db_gerenciamentoComentario))

    async def delete_gerenciamentoComentario(self, gerenciamentoComentario_id: int) -> bool:
        async with get_session() as session:
            db_gerenciamentoComentario = await session.scalar(select(GerenciamentoComentarioModel).where(GerenciamentoComentarioModel.id == gerenciamentoComentario_id))

            if db_gerenciamentoComentario:
                await session.delete(db_gerenciamentoComentario)
                await session.commit()

                return True

            return False


class GerenciamentoPropostaSQLiteRepository(GerenciamentoPropostaRepository):
    def __init__(self, gerenciamentoComentarioRepository: GerenciamentoComentarioSQLiteRepository):
        self.gerenciamentoComentarioRepository = gerenciamentoComentarioRepository

    async def get_gerenciamentoProposta(self) -> list[GerenciamentoProposta]:
        async with get_session() as session:
            gerenciamentoPropostas = await session.scalars(select(GerenciamentoPropostaModel))

            result = [
                GerenciamentoProposta.model_validate({
                    **vars(gerenciamentoProposta),
                    'metas_comentarios': [GerenciamentoComentario.model_validate(vars(gerenciamentoComentario)) for gerenciamentoComentario in gerenciamentoProposta.metas_comentarios],
                })
                for gerenciamentoProposta in gerenciamentoPropostas
                if gerenciamentoProposta is not None
            ]

        return result

    async def get_gerenciamentoProposta_by_id(self, gerenciamentoProposta_id: int) -> GerenciamentoProposta:
        async with get_session() as session:
            db_gerenciamentoProposta = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id == gerenciamentoProposta_id))
            if db_gerenciamentoProposta:
                return GerenciamentoProposta.model_validate({**vars(db_gerenciamentoProposta), 'metas_comentarios': [GerenciamentoComentario.model_validate(vars(gerenciamentoComentario)) for gerenciamentoComentario in db_gerenciamentoProposta.metas_comentarios]})
            return None

    async def create_gerenciamentoProposta(self, gerenciamentoProposta: GerenciamentoProposta) -> GerenciamentoProposta:
        async with get_session() as session:
            db_gerenciamentoProposta = GerenciamentoPropostaModel(trimestre_de_referencia=gerenciamentoProposta.trimestre_de_referencia, tipo=gerenciamentoProposta.tipo, proposta_id=gerenciamentoProposta.proposta_id)
            session.add(db_gerenciamentoProposta)
            await session.commit()
            await session.refresh(db_gerenciamentoProposta)

            return GerenciamentoProposta.model_validate(vars(db_gerenciamentoProposta))

    async def update_gerenciamentoProposta(self, gerenciamentoProposta_id: int, gerenciamentoProposta: GerenciamentoProposta) -> GerenciamentoProposta:
        async with get_session() as session:
            db_gerenciamentoProposta = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id == gerenciamentoProposta_id))
            if db_gerenciamentoProposta:
                db_gerenciamentoProposta.proposta_id = gerenciamentoProposta.proposta_id
                db_gerenciamentoProposta.trimestre_de_referencia = gerenciamentoProposta.trimestre_de_referencia
                db_gerenciamentoProposta.tipo = gerenciamentoProposta.tipo

                await session.commit()
                await session.refresh(db_gerenciamentoProposta)

                return GerenciamentoProposta.model_validate({**vars(db_gerenciamentoProposta), 'metas_comentarios': [GerenciamentoComentario.model_validate(vars(gerenciamentoComentario)) for gerenciamentoComentario in db_gerenciamentoProposta.metas_comentarios]})

            return None

    async def delete_gerenciamentoProposta(self, gerenciamentoProposta_id: int) -> bool:
        async with get_session() as session:
            gerenciamentoProposta = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id == gerenciamentoProposta_id))
            if gerenciamentoProposta:
                await session.delete(gerenciamentoProposta)
                await session.commit()

                return True

            return False

    async def create_gerenciamentoPropostaComentario(self, gerenciamentoProposta_id: int, gerenciamentoComentario_data: GerenciamentoComentario) -> GerenciamentoProposta:
        async with get_session() as session:
            db_gerenciamentoProposta = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id == gerenciamentoProposta_id))

            if db_gerenciamentoProposta:
                db_gerenciamentoComentario = await self.gerenciamentoComentarioRepository.create_gerenciamentoComentario(gerenciamentoComentario_data)

                if db_gerenciamentoComentario not in session:
                    session.add(db_gerenciamentoComentario)

                db_gerenciamentoProposta.metas_comentarios.append(db_gerenciamentoComentario)

                session.add(db_gerenciamentoProposta)
                await session.commit()
                await session.refresh(db_gerenciamentoProposta)

                return GerenciamentoProposta.model_validate({**vars(db_gerenciamentoProposta), 'metas_comentarios': [GerenciamentoComentario.model_validate(vars(gerenciamentoComentario)) for gerenciamentoComentario in db_gerenciamentoProposta.metas_comentarios]})

            return None


class GerenciamentoMetaSQLiteRepository(GerenciamentoMetaRepository):
    async def get_gerenciamentoMeta(self) -> list[GerenciamentoMeta]:
        async with get_session() as session:
            db_gerenciamentoMetas = await session.scalars(select(GerenciamentoMetaModel))

            result = [GerenciamentoMeta.model_validate({**vars(db_gerenciamentoMeta)}) for db_gerenciamentoMeta in db_gerenciamentoMetas if db_gerenciamentoMeta is not None]

            return result

    async def get_gerenciamentoMeta_by_id(self, gerenciamentoMeta_id: int) -> GerenciamentoMeta:
        async with get_session() as session:
            db_gerenciamentoMeta = await session.scalar(select(GerenciamentoMetaModel).where(GerenciamentoMetaModel.id == gerenciamentoMeta_id))

            if db_gerenciamentoMeta:
                return GerenciamentoMeta.model_validate(vars(db_gerenciamentoMeta))

            return None

    async def create_gerenciamentoMeta(self, gerenciamentoProposta_id: int, gerenciamentoMeta: GerenciamentoMeta) -> GerenciamentoMeta:
        async with get_session() as session:
            db_gerenciamentoProposta = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id == gerenciamentoProposta_id))

            if not db_gerenciamentoProposta:
                raise NotFoundError(f'gerenciamento_proposta_id with ID {gerenciamentoProposta_id} not found')

            db_gerenciamentoMeta = GerenciamentoMetaModel(ordem=gerenciamentoMeta.ordem, alcancado=gerenciamentoMeta.alcancado, gerenciamento_proposta_id=gerenciamentoProposta_id)
            session.add(db_gerenciamentoMeta)
            await session.commit()
            await session.refresh(db_gerenciamentoMeta)

            return GerenciamentoMeta.model_validate(vars(db_gerenciamentoMeta))

    async def update_gerenciamentoMeta(self, gerenciamentoMeta_id: int, gerenciamentoMeta_data: GerenciamentoMeta) -> GerenciamentoMeta:
        async with get_session() as session:
            db_gerenciamentoMeta = await session.scalar(select(GerenciamentoMetaModel).where(GerenciamentoMetaModel.id == gerenciamentoMeta_id))

            if db_gerenciamentoMeta:
                db_gerenciamentoMeta.alcancado = gerenciamentoMeta_data.alcancado
                db_gerenciamentoMeta.ordem = gerenciamentoMeta_data.ordem

                await session.commit()
                await session.refresh(db_gerenciamentoMeta)

                return GerenciamentoMeta.model_validate(vars(db_gerenciamentoMeta))

            return None

    async def delete_gerenciamentoMeta(self, gerenciamentoMeta_id: int) -> bool:
        async with get_session() as session:
            db_gerenciamentoMeta = await session.scalar(select(GerenciamentoMetaModel).where(GerenciamentoMetaModel.id == gerenciamentoMeta_id))

            if db_gerenciamentoMeta:
                await session.delete(db_gerenciamentoMeta)
                await session.commit()

                return True

            return False
