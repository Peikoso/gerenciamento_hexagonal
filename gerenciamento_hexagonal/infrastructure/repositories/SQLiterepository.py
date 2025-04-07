from domain.models.gerenciamento import GerenciamentoComentario, GerenciamentoProposta
from domain.repositories.gerenciamento import (
    GerenciamentoComentarioRepository,
    GerenciamentoPropostaRepository,
)
from infrastructure.database.models.gerenciamentoORM import GerenciamentoComentarioModel, GerenciamentoPropostaModel
from infrastructure.database.SQLiteConfig import get_session
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import (
    ClientError,
)


class GerenciamentoComentarioSQLiteRepository(GerenciamentoComentarioRepository):
    async def get_gerenciamentoComentario_by_id(self, gerenciamentoComentario_id: int) -> GerenciamentoComentario | None:
        pass

    async def create_gerenciamentoComentario(self, gerenciamentoComentario: GerenciamentoComentario) -> GerenciamentoComentarioModel:
        async with get_session() as session:
            try:
                db_gerenciamentoComentario = GerenciamentoComentarioModel(comentario=gerenciamentoComentario.comentario)
                session.add(db_gerenciamentoComentario)
                await session.commit()
                await session.refresh(db_gerenciamentoComentario)

                return db_gerenciamentoComentario

            except ClientError as e:
                raise Exception(f'Failed to create gerenciamento_comentario: {str(e)}')

    async def update_gerenciamentoComentario(self, gerenciamentoComentario: GerenciamentoComentario) -> GerenciamentoComentario | None:
        pass

    async def delete_gerenciamentoComentario(self, gerenciamentoComentario_id: int) -> None:
        pass

    async def get_gerenciamentoComentario(self) -> list[GerenciamentoComentario]:
        pass


class GerenciamentoPropostaSQLiteRepository(GerenciamentoPropostaRepository):
    def __init__(self, gerenciamentoComentarioRepository: GerenciamentoComentarioSQLiteRepository):
        self.gerenciamentoComentarioRepository = gerenciamentoComentarioRepository

    async def get_gerenciamentoProposta_by_id(self, gerenciamentoProposta_id: int) -> GerenciamentoProposta | None:
        async with get_session() as session:
            try:
                db_gerenciamentoProposta = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id == gerenciamentoProposta_id))
                if db_gerenciamentoProposta:
                    await session.refresh(db_gerenciamentoProposta, ['metas_comentarios'])
                    return GerenciamentoProposta.model_validate({**db_gerenciamentoProposta.__dict__, 'metas_comentarios': [GerenciamentoComentario.model_validate(gerenciamentoComentario.__dict__) for gerenciamentoComentario in db_gerenciamentoProposta.metas_comentarios]})
                return None
            except ClientError as e:
                raise Exception(f'Failed to fetch gerenciamento_proposta from SQLite: {str(e)}')

    async def create_gerenciamentoProposta(self, gerenciamentoProposta: GerenciamentoProposta) -> GerenciamentoProposta:
        async with get_session() as session:
            try:
                db_gerenciamentoProposta = GerenciamentoPropostaModel(trimestre_de_referencia=gerenciamentoProposta.trimestre_de_referencia, tipo=gerenciamentoProposta.tipo, proposta_id=gerenciamentoProposta.proposta_id)
                session.add(db_gerenciamentoProposta)
                await session.commit()
                await session.refresh(db_gerenciamentoProposta)

                return GerenciamentoProposta.model_validate(db_gerenciamentoProposta.__dict__)

            except ClientError as e:
                raise Exception(f'Failed to create gerenciamento_proposta: {str(e)}')

    async def update_gerenciamentoProposta(self, gerenciamentoProposta_id: int, gerenciamentoProposta: GerenciamentoProposta) -> GerenciamentoProposta | None:
        async with get_session() as session:
            try:
                db_gerenciamentoProposta = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id == gerenciamentoProposta_id))
                if db_gerenciamentoProposta:
                    db_gerenciamentoProposta.proposta_id = gerenciamentoProposta.proposta_id
                    db_gerenciamentoProposta.trimestre_de_referencia = gerenciamentoProposta.trimestre_de_referencia
                    db_gerenciamentoProposta.tipo = gerenciamentoProposta.tipo

                    await session.commit()
                    await session.refresh(db_gerenciamentoProposta)

                    await session.refresh(db_gerenciamentoProposta, ['metas_comentarios'])
                    return GerenciamentoProposta.model_validate({**db_gerenciamentoProposta.__dict__, 'metas_comentarios': [GerenciamentoComentario.model_validate(gerenciamentoComentario.__dict__) for gerenciamentoComentario in db_gerenciamentoProposta.metas_comentarios]})

                return None

            except ClientError as e:
                raise Exception(f'Failed to update gerenciamento_proposta from SQLite: {str(e)}')

    async def delete_gerenciamentoProposta(self, gerenciamentoProposta_id: int) -> bool:
        async with get_session() as session:
            try:
                gerenciamentoProposta = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id == gerenciamentoProposta_id))
                if gerenciamentoProposta:
                    await session.delete(gerenciamentoProposta)
                    await session.commit()

                    return True

                return False

            except ClientError as e:
                raise Exception(f'Failed to delete gerenciamento_proposta from SQLite: {str(e)}')

    async def get_gerenciamentoProposta(self) -> list[GerenciamentoProposta]:
        async with get_session() as session:
            gerenciamentoPropostas = await session.scalars(select(GerenciamentoPropostaModel).options(selectinload(GerenciamentoPropostaModel.metas_comentarios)))

            result = [
                GerenciamentoProposta.model_validate({
                    **gerenciamentoProposta.__dict__,
                    'metas_comentarios': [
                        GerenciamentoComentario.model_validate(gerenciamentoComentario.__dict__)
                        for gerenciamentoComentario in gerenciamentoProposta.metas_comentarios  # Converte os comentários
                    ],
                })
                for gerenciamentoProposta in gerenciamentoPropostas.all()
                if gerenciamentoProposta is not None
            ]

        return result

    async def create_gerenciamentoPropostaComentario(self, gerenciamentoProposta_id: int, gerenciamentoComentario_data: GerenciamentoComentario) -> GerenciamentoProposta:
        async with get_session() as session:
            try:
                db_gerenciamentoProposta = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id == gerenciamentoProposta_id))

                if db_gerenciamentoProposta:
                    db_gerenciamentoComentario = await self.gerenciamentoComentarioRepository.create_gerenciamentoComentario(gerenciamentoComentario_data)

                    if db_gerenciamentoComentario not in session:
                        session.add(db_gerenciamentoComentario)

                    await session.refresh(db_gerenciamentoProposta, ['metas_comentarios'])

                    db_gerenciamentoProposta.metas_comentarios.append(db_gerenciamentoComentario)

                    session.add(db_gerenciamentoProposta)
                    await session.commit()
                    await session.refresh(db_gerenciamentoProposta)

                    await session.refresh(db_gerenciamentoProposta, ['metas_comentarios'])
                    return GerenciamentoProposta.model_validate({**db_gerenciamentoProposta.__dict__, 'metas_comentarios': [GerenciamentoComentario.model_validate(gerenciamentoComentario.__dict__) for gerenciamentoComentario in db_gerenciamentoProposta.metas_comentarios]})

                return False

            except ClientError as e:
                raise Exception(f'Failed to fetch gerenciamento_proposta from SQLite: {str(e)}')
