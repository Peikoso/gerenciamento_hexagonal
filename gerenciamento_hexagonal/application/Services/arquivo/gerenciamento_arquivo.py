import os

from gerenciamento_hexagonal.application.services.gerenciamento.meta import GerenciamentoMetaServices
from gerenciamento_hexagonal.application.services.arquivo.arquivo_service import ArquivoServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.arquivo import Arquivo
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoContrapartidaArquivo, GerenciamentoMetaArquivo, GerenciamentoQualitativoArquivo
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.arquivo import GerenciamentoArquivoRepository


class GerenciamentoArquivoServices:
    def __init__(self, repository: GerenciamentoArquivoRepository, service_meta: GerenciamentoMetaServices, service_meta_arquivo: ArquivoServices):
        self.repository = repository
        self.service_meta = service_meta
        self.service_meta_arquivo = service_meta_arquivo

    async def get_gerenciamento_arquivo_by_id(self, arquivo_id: int) -> GerenciamentoMetaArquivo | GerenciamentoQualitativoArquivo | GerenciamentoContrapartidaArquivo:
        arquivo = await self.repository.get_gerenciamento_arquivo_by_id(arquivo_id)

        if not arquivo:
            raise NotFoundError(f'arquivo with ID: {arquivo_id} not found')

        return arquivo

    async def create_gerenciamento_meta_arquivo(self, gerenciamento_meta_id: int, arquivos):
        await self.service_meta.get_gerenciamento_meta_by_id(gerenciamento_meta_id)

        metadados = await self.service_meta_arquivo.processar_arquivos(arquivos=arquivos, rel_id=gerenciamento_meta_id)

        arquivos_salvos = []
        for arquivo in metadados:
            arquivo_model = Arquivo(
                tipo_arquivo_id='REGISTRO_DA_META',
                nome=arquivo['nome'],
                extensao=arquivo['extensao'],
                tamanho=arquivo['tamanho'],
                uri=arquivo['uri'],
            )

            arquivo_id = await self.repository.create_arquivo(arquivo_model)
            db_arquivo = await self.repository.create_gerenciamento_meta_arquivo(gerenciamento_meta_id, arquivo_id)
            arquivos_salvos.append(db_arquivo)

        return arquivos_salvos

    async def delete_arquivo(self, arquivo_id):
        arquivo = await self.get_gerenciamento_arquivo_by_id(arquivo_id)

        if os.path.exists(arquivo.uri):
            os.remove(arquivo.uri)

        await self.repository.delete_gerenciamento_arquivo(arquivo_id)

        return {'message': 'arquivo deleted'}
