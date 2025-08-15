from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoCaracterizacao
from gerenciamento_hexagonal.domain.repositories.gerenciamento import GerenciamentoCaracterizacaoRepository
from gerenciamento_hexagonal.infrastructure.database.sqlalchemyConfig import get_session
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.models.gerenciamento_orm import GerenciamentoCaracterizacaoModel
from sqlalchemy import select


class GerenciamentoCaracterizacaoRepository(GerenciamentoCaracterizacaoRepository):
    async def get_gerenciamento_caracterizacao(self) -> list[GerenciamentoCaracterizacao]:
        async with get_session() as session:
            db_gerenciamento_caracterizacao = await session.scalars(select(GerenciamentoCaracterizacaoModel))

            result = [GerenciamentoCaracterizacao.model_validate(vars(gerenciamento_caracterizacao)) for gerenciamento_caracterizacao in db_gerenciamento_caracterizacao]

            return result

    async def get_gerenciamento_caracterizacao_by_id(self, gerenciamento_caracterizacao_id: int) -> GerenciamentoCaracterizacao | None:
        async with get_session() as session:
            db_gerenciamento_caracterizacao = await session.scalar(select(GerenciamentoCaracterizacaoModel).where(GerenciamentoCaracterizacaoModel.id == gerenciamento_caracterizacao_id))

            if not db_gerenciamento_caracterizacao:
                return None

            result = GerenciamentoCaracterizacao.model_validate(vars(db_gerenciamento_caracterizacao))

            return result

    async def create_gerenciamento_caracterizacao(self, gerenciamento_quantitativo_id: int, gerenciamento_caracterizacao: GerenciamentoCaracterizacao) -> GerenciamentoCaracterizacao:
        async with get_session() as session:
            db_gerenciamento_caracterizacao = GerenciamentoCaracterizacaoModel(quantidade=gerenciamento_caracterizacao.quantidade, gerenciamento_quantitativo_id=gerenciamento_quantitativo_id, categorizacoes_ids=gerenciamento_caracterizacao.categorizacoes_ids)

            session.add(db_gerenciamento_caracterizacao)
            await session.commit()
            await session.refresh(db_gerenciamento_caracterizacao)

            result = GerenciamentoCaracterizacao.model_validate(vars(db_gerenciamento_caracterizacao))

            return result

    async def update_gerenciamento_caracterizacao(self, gerenciamento_caracterizacao_id: int, gerenciamento_caracterizacao: GerenciamentoCaracterizacao) -> GerenciamentoCaracterizacao:
        async with get_session() as session:
            db_gerenciamento_caracterizacao = await session.scalar(select(GerenciamentoCaracterizacaoModel).where(GerenciamentoCaracterizacaoModel.id == gerenciamento_caracterizacao_id))

            db_gerenciamento_caracterizacao.quantidade = gerenciamento_caracterizacao.quantidade
            db_gerenciamento_caracterizacao.categorizacoes_ids = gerenciamento_caracterizacao.categorizacoes_ids

            await session.commit()
            await session.refresh(db_gerenciamento_caracterizacao)

            result = GerenciamentoCaracterizacao.model_validate((db_gerenciamento_caracterizacao))

            return result

    async def delete_gerenciamento_caracterizacao(self, gerenciamento_caracterizacao_id: int):
        async with get_session() as session:
            db_gerenciamento_caracterizacao = await session.scalar(select(GerenciamentoCaracterizacaoModel).where(GerenciamentoCaracterizacaoModel.id == gerenciamento_caracterizacao_id))

            await session.delete(db_gerenciamento_caracterizacao)
            await session.commit()
