from gerenciamento_hexagonal.domain.models.arquivo import Arquivo
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoContrapartidaArquivo, GerenciamentoMetaArquivo, GerenciamentoQualitativoArquivo
from gerenciamento_hexagonal.domain.repositories.gerenciamento import GerenciamentoArquivoRepository
from gerenciamento_hexagonal.infrastructure.database.models.gerenciamento_orm import ArquivoModel, GerenciamentoContrapartidaArquivoModel, GerenciamentoMetaArquivoModel, GerenciamentoQualitativoArquivoModel
from gerenciamento_hexagonal.infrastructure.database.sqlalchemyConfig import get_session
from sqlalchemy import select


class GerenciamentoArquivoRepository(GerenciamentoArquivoRepository):
    async def get_gerenciamento_arquivo_by_id(self, arquivo_id: int) -> GerenciamentoMetaArquivo | GerenciamentoQualitativoArquivo | GerenciamentoContrapartidaArquivo | None:
        async with get_session() as session:
            db_meta_arquivo = await session.scalar(select(GerenciamentoMetaArquivoModel).where(GerenciamentoMetaArquivoModel.arquivo_id == arquivo_id))
            if db_meta_arquivo:
                return GerenciamentoMetaArquivo.model_validate({
                    'id': db_meta_arquivo.id,
                    'gerenciamento_meta_id': db_meta_arquivo.gerenciamento_meta_id,
                    'arquivo_id': db_meta_arquivo.arquivo_id,
                    'tipo_arquivo_id': db_meta_arquivo.arquivo.tipo_arquivo_id,
                    'nome': db_meta_arquivo.arquivo.nome,
                    'extensao': db_meta_arquivo.arquivo.extensao,
                    'tamanho': db_meta_arquivo.arquivo.tamanho,
                    'uri': db_meta_arquivo.arquivo.uri,
                })

            db_qualitativo_arquivo = await session.scalar(select(GerenciamentoQualitativoArquivoModel).where(GerenciamentoQualitativoArquivoModel.arquivo_id == arquivo_id))
            if db_qualitativo_arquivo:
                return GerenciamentoQualitativoArquivo.model_validate({
                    'id': db_qualitativo_arquivo.id,
                    'gerenciamento_qualitativo_id': db_qualitativo_arquivo.gerenciamento_qualitativo_id,
                    'arquivo_id': db_qualitativo_arquivo.arquivo_id,
                    'tipo_arquivo_id': db_qualitativo_arquivo.arquivo.tipo_arquivo_id,
                    'nome': db_qualitativo_arquivo.arquivo.nome,
                    'extensao': db_qualitativo_arquivo.arquivo.extensao,
                    'tamanho': db_qualitativo_arquivo.arquivo.tamanho,
                    'uri': db_qualitativo_arquivo.arquivo.uri,
                })

            db_contrapartida_arquivo = await session.scalar(select(GerenciamentoContrapartidaArquivoModel).where(GerenciamentoContrapartidaArquivoModel.arquivo_id == arquivo_id))
            if db_contrapartida_arquivo:
                return GerenciamentoContrapartidaArquivo.model_validate({
                    'id': db_contrapartida_arquivo.id,
                    'gerenciamento_contrapartida_id': db_contrapartida_arquivo.gerenciamento_contrapartida_id,
                    'arquivo_id': db_contrapartida_arquivo.arquivo_id,
                    'tipo_arquivo_id': db_contrapartida_arquivo.arquivo.tipo_arquivo_id,
                    'nome': db_contrapartida_arquivo.arquivo.nome,
                    'extensao': db_contrapartida_arquivo.arquivo.extensao,
                    'tamanho': db_contrapartida_arquivo.arquivo.tamanho,
                    'uri': db_contrapartida_arquivo.arquivo.uri,
                })

            return None

    async def create_arquivo(self, arquivo: Arquivo) -> int:
        async with get_session() as session:
            db_arquivo = ArquivoModel(nome=arquivo.nome, extensao=arquivo.extensao, tamanho=arquivo.tamanho, uri=arquivo.uri, tipo_arquivo_id=arquivo.tipo_arquivo_id)

            session.add(db_arquivo)
            await session.commit()
            await session.refresh(db_arquivo)

            return db_arquivo.arquivo_id

    async def create_gerenciamento_meta_arquivo(self, gerenciamento_meta_id: int, arquivo_id: int) -> GerenciamentoMetaArquivo:
        async with get_session() as session:
            db_meta_arquivo = GerenciamentoMetaArquivoModel(gerenciamento_meta_id=gerenciamento_meta_id, arquivo_id=arquivo_id)

            session.add(db_meta_arquivo)
            await session.commit()
            await session.refresh(db_meta_arquivo)

            return GerenciamentoMetaArquivo.model_validate({
                'id': db_meta_arquivo.id,
                'gerenciamento_meta_id': db_meta_arquivo.gerenciamento_meta_id,
                'arquivo_id': db_meta_arquivo.arquivo_id,
                'tipo_arquivo_id': db_meta_arquivo.arquivo.tipo_arquivo_id,
                'nome': db_meta_arquivo.arquivo.nome,
                'extensao': db_meta_arquivo.arquivo.extensao,
                'tamanho': db_meta_arquivo.arquivo.tamanho,
                'uri': db_meta_arquivo.arquivo.uri,
            })

    async def create_gerenciamento_qualitativo_arquivo(self, gerenciamento_qualitativo_id: int, arquivo_id: int) -> GerenciamentoQualitativoArquivo:
        async with get_session() as session:
            db_qualitativo_arquivo = GerenciamentoQualitativoArquivoModel(gerenciamento_qualitativo_id=gerenciamento_qualitativo_id, arquivo_id=arquivo_id)

            session.add(db_qualitativo_arquivo)
            await session.commit()
            await session.refresh(db_qualitativo_arquivo)

            return GerenciamentoQualitativoArquivo.model_validate({
                'id': db_qualitativo_arquivo.id,
                'gerenciamento_qualitativo_id': db_qualitativo_arquivo.gerenciamento_qualitativo_id,
                'arquivo_id': db_qualitativo_arquivo.arquivo_id,
                'tipo_arquivo_id': db_qualitativo_arquivo.arquivo.tipo_arquivo_id,
                'nome': db_qualitativo_arquivo.arquivo.nome,
                'extensao': db_qualitativo_arquivo.arquivo.extensao,
                'tamanho': db_qualitativo_arquivo.arquivo.tamanho,
                'uri': db_qualitativo_arquivo.arquivo.uri,
            })

    async def create_gerenciamento_contrapartida_arquivo(self, gerenciamento_contrapartida_id: int, arquivo_id: int) -> GerenciamentoContrapartidaArquivo:
        async with get_session() as session:
            db_contrapartida_arquivo = GerenciamentoContrapartidaArquivoModel(gerenciamento_contrapartida_id=gerenciamento_contrapartida_id, arquivo_id=arquivo_id)

            session.add(db_contrapartida_arquivo)
            await session.commit()
            await session.refresh(db_contrapartida_arquivo)

            return GerenciamentoContrapartidaArquivo.model_validate({
                'id': db_contrapartida_arquivo.id,
                'gerenciamento_contrapartida_id': db_contrapartida_arquivo.gerenciamento_contrapartida_id,
                'arquivo_id': db_contrapartida_arquivo.arquivo_id,
                'tipo_arquivo_id': db_contrapartida_arquivo.arquivo.tipo_arquivo_id,
                'nome': db_contrapartida_arquivo.arquivo.nome,
                'extensao': db_contrapartida_arquivo.arquivo.extensao,
                'tamanho': db_contrapartida_arquivo.arquivo.tamanho,
                'uri': db_contrapartida_arquivo.arquivo.uri,
            })

    async def delete_gerenciamento_arquivo(self, arquivo_id: int):
        async with get_session() as session:
            arquivo = await session.scalar(select(ArquivoModel).where(ArquivoModel.arquivo_id == arquivo_id))

            await session.delete(arquivo)
            await session.commit()
