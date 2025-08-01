from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoComentario, GerenciamentoProposta
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoPropostaResponse
from gerenciamento_hexagonal.domain.repositories.gerenciamento import GerenciamentoComentarioRepository, GerenciamentoPropostaRepository
from gerenciamento_hexagonal.infrastructure.database.models.gerenciamento_orm import GerenciamentoCaracterizacaoModel, GerenciamentoPropostaModel, GerenciamentoQuantitativoModel
from gerenciamento_hexagonal.infrastructure.database.sqlalchemyConfig import get_session
from sqlalchemy import select


class GerenciamentoPropostaRepository(GerenciamentoPropostaRepository):
    def __init__(self, gerenciamento_comentario_repository: GerenciamentoComentarioRepository):
        self.gerenciamento_comentario_repository = gerenciamento_comentario_repository

    async def get_gerenciamento_proposta(self) -> list[GerenciamentoProposta]:
        async with get_session() as session:
            gerenciamento_propostas = await session.scalars(select(GerenciamentoPropostaModel))

            result = [GerenciamentoPropostaResponse.model_validate(vars(gerenciamento_proposta)) for gerenciamento_proposta in gerenciamento_propostas]

            return result

    async def get_gerenciamento_proposta_by_id(self, gerenciamento_proposta_id: int) -> GerenciamentoProposta | None:
        async with get_session() as session:
            db_gerenciamento_proposta = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id == gerenciamento_proposta_id))

            if not db_gerenciamento_proposta:
                return None

        arquivos_ids = []

        for meta in db_gerenciamento_proposta.gerenciamento_metas:
            arquivos_ids.extend([arq.arquivo_id for arq in meta.arquivos])

        for contrapartida in db_gerenciamento_proposta.gerenciamento_contrapartida:
            arquivos_ids.extend([arq.arquivo_id for arq in contrapartida.arquivos])

        for qualitativo in db_gerenciamento_proposta.gerenciamento_qualitativo:
            arquivos_ids.extend([arq.arquivo_id for arq in qualitativo.arquivos])

        if db_gerenciamento_proposta:
            return GerenciamentoProposta.model_validate({**vars(db_gerenciamento_proposta), 'metas_comentarios': [GerenciamentoComentario.model_validate(vars(gerenciamento_comentario)) for gerenciamento_comentario in db_gerenciamento_proposta.metas_comentarios], 'arquivos_ids': arquivos_ids})

    async def create_gerenciamento_proposta(self, gerenciamento_proposta: GerenciamentoProposta) -> GerenciamentoProposta:
        async with get_session() as session:
            db_gerenciamento_proposta = GerenciamentoPropostaModel(trimestre_de_referencia=gerenciamento_proposta.trimestre_de_referencia, tipo=gerenciamento_proposta.tipo, proposta_id=gerenciamento_proposta.proposta_id)
            session.add(db_gerenciamento_proposta)
            await session.commit()
            await session.refresh(db_gerenciamento_proposta)

            return GerenciamentoPropostaResponse.model_validate(vars(db_gerenciamento_proposta))

    async def update_gerenciamento_proposta(self, gerenciamento_proposta_id: int, gerenciamento_proposta: GerenciamentoProposta) -> GerenciamentoProposta:
        async with get_session() as session:
            db_gerenciamento_proposta = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id == gerenciamento_proposta_id))

            db_gerenciamento_proposta.proposta_id = gerenciamento_proposta.proposta_id
            db_gerenciamento_proposta.trimestre_de_referencia = gerenciamento_proposta.trimestre_de_referencia
            db_gerenciamento_proposta.tipo = gerenciamento_proposta.tipo

            await session.commit()
            await session.refresh(db_gerenciamento_proposta)

            return GerenciamentoPropostaResponse.model_validate(vars(db_gerenciamento_proposta))

    async def delete_gerenciamento_proposta(self, gerenciamento_proposta_id: int):
        async with get_session() as session:
            gerenciamento_proposta = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id == gerenciamento_proposta_id))

            await session.delete(gerenciamento_proposta)
            await session.commit()

    async def create_gerenciamento_proposta_comentario(self, gerenciamento_proposta_id: int, gerenciamento_comentario: GerenciamentoComentario) -> GerenciamentoProposta:
        async with get_session() as session:
            db_gerenciamento_proposta = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id == gerenciamento_proposta_id))

            if db_gerenciamento_proposta:
                db_gerenciamento_comentario = await self.gerenciamento_comentario_repository.create_gerenciamento_comentario(gerenciamento_comentario)

                if db_gerenciamento_comentario not in session:
                    session.add(db_gerenciamento_comentario)

                db_gerenciamento_proposta.metas_comentarios.append(db_gerenciamento_comentario)

                session.add(db_gerenciamento_proposta)
                await session.commit()
                await session.refresh(db_gerenciamento_proposta)

                return GerenciamentoComentario.model_validate(vars(db_gerenciamento_comentario))

            return None

    async def checar_gerenciamento_caracterizacao_exists(self, gerenciamento_proposta_id: int) -> bool:
        async with get_session() as session:
            db_gerenciamento_quantitativo = await session.scalar(select(GerenciamentoQuantitativoModel).where(GerenciamentoQuantitativoModel.gerenciamento_proposta_id == gerenciamento_proposta_id))
            if not db_gerenciamento_quantitativo:
                return False

            db_gerenciamento_caracterizacao = await session.scalar(select(GerenciamentoCaracterizacaoModel).where(GerenciamentoCaracterizacaoModel.gerenciamento_quantitativo_id == db_gerenciamento_quantitativo.id))
            if db_gerenciamento_caracterizacao:
                return True

            return False
