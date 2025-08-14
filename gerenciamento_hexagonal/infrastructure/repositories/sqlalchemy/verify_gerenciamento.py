from gerenciamento_hexagonal.domain.repositories.gerenciamento import VerifyGerenciamentoExistsRepository
from gerenciamento_hexagonal.infrastructure.database.sqlalchemyConfig import get_session
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.models.gerenciamento_orm import GerenciamentoContrapartidaModel, GerenciamentoMetaModel, GerenciamentoPropostaModel, GerenciamentoQualitativoModel, GerenciamentoQuantitativoModel
from sqlalchemy import select


class VerifyGerenciamentoRepository(VerifyGerenciamentoExistsRepository):
    async def gerencimento_proposta_exists(self, gerenciamento_proposta_id: int) -> bool:
        async with get_session() as session:
            exists = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id == gerenciamento_proposta_id))

            if exists:
                return True

            return False

    async def gerenciamento_meta_exists(self, gerenciamento_meta_id: int) -> bool:
        async with get_session() as session:
            exists = await session.scalar(select(GerenciamentoMetaModel).where(GerenciamentoMetaModel.id == gerenciamento_meta_id))

            if exists:
                return True

            return False

    async def gerenciamento_quantitativo_exists(self, gerenciamento_quantitativo_id: int) -> bool:
        async with get_session() as session:
            exists = await session.scalar(select(GerenciamentoQuantitativoModel).where(GerenciamentoQuantitativoModel.id == gerenciamento_quantitativo_id))

            if exists:
                return True

            return False

    async def gerenciamento_qualitativo_exists(self, gerenciamento_qualitativo_id: int) -> bool:
        async with get_session() as session:
            exists = await session.scalar(select(GerenciamentoQualitativoModel).where(GerenciamentoQualitativoModel.id == gerenciamento_qualitativo_id))

            if exists:
                return True

            return False

    async def gerenciamento_contrapartida_exists(self, gerenciamento_contrapartida_id: int) -> bool:
        async with get_session() as session:
            exists = await session.scalar(select(GerenciamentoContrapartidaModel).where(GerenciamentoContrapartidaModel.id == gerenciamento_contrapartida_id))

            if exists:
                return True

            return False
