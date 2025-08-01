from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoMeta
from gerenciamento_hexagonal.domain.repositories.gerenciamento import GerenciamentoMetaRepository
from gerenciamento_hexagonal.infrastructure.database.models.gerenciamento_orm import GerenciamentoMetaModel
from gerenciamento_hexagonal.infrastructure.database.sqlalchemyConfig import get_session
from sqlalchemy import select


class GerenciamentoMetaRepository(GerenciamentoMetaRepository):
    async def get_gerenciamento_meta(self) -> list[GerenciamentoMeta]:
        async with get_session() as session:
            db_gerenciamento_metas = await session.scalars(select(GerenciamentoMetaModel))

            result = [GerenciamentoMeta.model_validate({**vars(db_gerenciamento_meta), 'arquivos_ids': [arquivo.arquivo_id for arquivo in db_gerenciamento_meta.arquivos]}) for db_gerenciamento_meta in db_gerenciamento_metas]

            return result

    async def get_gerenciamento_meta_by_id(self, gerenciamento_meta_id: int) -> GerenciamentoMeta | None:
        async with get_session() as session:
            db_gerenciamento_meta = await session.scalar(select(GerenciamentoMetaModel).where(GerenciamentoMetaModel.id == gerenciamento_meta_id))

            if db_gerenciamento_meta:
                return GerenciamentoMeta.model_validate({**vars(db_gerenciamento_meta), 'arquivos_ids': [arquivo.arquivo_id for arquivo in db_gerenciamento_meta.arquivos]})

            return None

    async def create_gerenciamento_meta(self, gerenciamento_proposta_id: int, gerenciamento_meta: GerenciamentoMeta) -> GerenciamentoMeta:
        async with get_session() as session:
            db_gerenciamento_meta = GerenciamentoMetaModel(ordem=gerenciamento_meta.ordem, alcancado=gerenciamento_meta.alcancado, gerenciamento_proposta_id=gerenciamento_proposta_id)
            session.add(db_gerenciamento_meta)
            await session.commit()
            await session.refresh(db_gerenciamento_meta)

            return GerenciamentoMeta.model_validate(vars(db_gerenciamento_meta))

    async def update_gerenciamento_meta(self, gerenciamento_meta_id: int, gerenciamento_meta: GerenciamentoMeta) -> GerenciamentoMeta:
        async with get_session() as session:
            db_gerenciamento_meta = await session.scalar(select(GerenciamentoMetaModel).where(GerenciamentoMetaModel.id == gerenciamento_meta_id))

            db_gerenciamento_meta.alcancado = gerenciamento_meta.alcancado
            db_gerenciamento_meta.ordem = gerenciamento_meta.ordem

            await session.commit()
            await session.refresh(db_gerenciamento_meta)

            return GerenciamentoMeta.model_validate(vars(db_gerenciamento_meta))

    async def delete_gerenciamento_meta(self, gerenciamento_meta_id: int):
        async with get_session() as session:
            db_gerenciamento_meta = await session.scalar(select(GerenciamentoMetaModel).where(GerenciamentoMetaModel.id == gerenciamento_meta_id))

            await session.delete(db_gerenciamento_meta)
            await session.commit()
