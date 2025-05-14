from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoContrapartida
from gerenciamento_hexagonal.domain.repositories.gerenciamento import GerenciamentoContrapartidaRepository
from gerenciamento_hexagonal.infrastructure.database.models.gerenciamento_orm import GerenciamentoContrapartidaModel
from gerenciamento_hexagonal.infrastructure.database.sqlalchemyConfig import get_session
from sqlalchemy import select


class GerenciamentoContrapartidaRepository(GerenciamentoContrapartidaRepository):
    async def get_gerenciamento_contrapartida(self) -> list[GerenciamentoContrapartida]:
        async with get_session() as session:
            db_gerenciamento_contrapartidas = await session.scalars(select(GerenciamentoContrapartidaModel))

            return [GerenciamentoContrapartida.model_validate({**vars(db_gerenciamento_contrapartida), 'arquivos_ids': [arquivo.arquivo_id for arquivo in db_gerenciamento_contrapartida.arquivos]}) for db_gerenciamento_contrapartida in db_gerenciamento_contrapartidas]

    async def get_gerenciamento_contrapartida_by_id(self, gerenciamento_contrapartida_id: int) -> GerenciamentoContrapartida | None:
        async with get_session() as session:
            db_gerenciamento_contrapartida = await session.scalar(select(GerenciamentoContrapartidaModel).where(GerenciamentoContrapartidaModel.id == gerenciamento_contrapartida_id))

            if not db_gerenciamento_contrapartida:
                return None

            return GerenciamentoContrapartida.model_validate({**vars(db_gerenciamento_contrapartida), 'arquivos_ids': [arquivo.arquivo_id for arquivo in db_gerenciamento_contrapartida.arquivos]})

    async def create_gerenciamento_contrapartida(self, gerenciamento_contrapartida: GerenciamentoContrapartida) -> GerenciamentoContrapartida:
        async with get_session() as session:
            db_gerenciamento_contrapartida = GerenciamentoContrapartidaModel(
                quantidade=gerenciamento_contrapartida.quantidade, observacao=gerenciamento_contrapartida.observacao, data=gerenciamento_contrapartida.data, status=gerenciamento_contrapartida.status, proposta_contrapartida_id=gerenciamento_contrapartida.proposta_contrapartida_id, gerenciamento_proposta_id=gerenciamento_contrapartida.gerenciamento_proposta_id
            )

            session.add(db_gerenciamento_contrapartida)
            await session.commit()
            await session.refresh(db_gerenciamento_contrapartida)

            return GerenciamentoContrapartida.model_validate(vars(db_gerenciamento_contrapartida))

    async def update_gerenciamento_contrapartida(self, gerenciamento_contrapartida_id: int, gerenciamento_contrapartida: GerenciamentoContrapartida) -> GerenciamentoContrapartida:
        async with get_session() as session:
            db_gerenciamento_contrapartida = await session.scalar(select(GerenciamentoContrapartidaModel).where(GerenciamentoContrapartidaModel.id == gerenciamento_contrapartida_id))

            db_gerenciamento_contrapartida.quantidade = gerenciamento_contrapartida.quantidade
            db_gerenciamento_contrapartida.observacao = gerenciamento_contrapartida.observacao
            db_gerenciamento_contrapartida.data = gerenciamento_contrapartida.data
            db_gerenciamento_contrapartida.status = gerenciamento_contrapartida.status
            db_gerenciamento_contrapartida.proposta_contrapartida_id = gerenciamento_contrapartida.proposta_contrapartida_id

            await session.commit()
            await session.refresh(db_gerenciamento_contrapartida)

            return GerenciamentoContrapartida.model_validate(vars(db_gerenciamento_contrapartida))

    async def delete_gerenciamento_contrapartida(self, gerenciamento_contrapartida_id: int):
        async with get_session() as session:
            db_gerenciamento_contrapartida = await session.scalar(select(GerenciamentoContrapartidaModel).where(GerenciamentoContrapartidaModel.id == gerenciamento_contrapartida_id))

            await session.delete(db_gerenciamento_contrapartida)
            await session.commit()
