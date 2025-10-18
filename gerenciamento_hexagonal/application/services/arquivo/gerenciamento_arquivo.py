import os

from gerenciamento_hexagonal.application.services.arquivo.arquivo_service import ArquivoServices
from gerenciamento_hexagonal.application.services.interfaces.gerenciamento.verify_gerenciamento import VerifyGerenciamentoExists
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.arquivo import Arquivo
from gerenciamento_hexagonal.domain.models.enums_specs import TipoGerenciamentoArquivo
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoContrapartidaArquivo, GerenciamentoMetaArquivo, GerenciamentoQualitativoArquivo
from gerenciamento_hexagonal.domain.services.arquivo_service import ValidacaoArquivoService
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.arquivo import GerenciamentoArquivoRepository


class GerenciamentoArquivoServices:
    def __init__(self, repository: GerenciamentoArquivoRepository, service_arquivo: ArquivoServices, verify: VerifyGerenciamentoExists):
        self.repository = repository
        self.service_arquivo = service_arquivo
        self.verify = verify

    async def get_gerenciamento_arquivo_by_id(self, arquivo_id: int) -> GerenciamentoMetaArquivo | GerenciamentoQualitativoArquivo | GerenciamentoContrapartidaArquivo:
        arquivo = await self.repository.get_gerenciamento_arquivo_by_id(arquivo_id)

        if not arquivo:
            raise NotFoundError(f'arquivo with ID: {arquivo_id} not found')

        return arquivo

    async def get_gerenciamento_arquivo_download_by_id(self, arquivo_id: int):
        arquivo = await self.get_gerenciamento_arquivo_by_id(arquivo_id)

        if not os.path.exists(arquivo.uri):
            raise NotFoundError(f'arquivo with ID: {arquivo_id} not found in directory')

        return arquivo

    async def create_arquivo(self, gerenciamento_id: int, arquivos, tipo_gerenciamento: TipoGerenciamentoArquivo):
        metadados = await self.service_arquivo.processar_arquivos(arquivos=arquivos, rel_id=gerenciamento_id)

        arquivos_salvos = []
        for arquivo in metadados:
            arquivo_model = Arquivo(
                tipo_arquivo_id=tipo_gerenciamento,
                nome=arquivo['nome'],
                extensao=arquivo['extensao'],
                tamanho=arquivo['tamanho'],
                uri=arquivo['uri'],
            )

            arquivo_id = await self.repository.create_arquivo(arquivo_model)

            arquivos_salvos.append(arquivo_id)

        return arquivos_salvos

    async def create_gerenciamento_meta_arquivo(self, gerenciamento_meta_id: int, arquivos):
        await self.verify.gerenciamento_meta_exists(gerenciamento_meta_id)

        nomes_arquivos = [arquivo.filename for arquivo in arquivos]

        ValidacaoArquivoService.validar_arquivos_metas(nomes_arquivos)

        arquivos_ids = await self.create_arquivo(gerenciamento_id=gerenciamento_meta_id, arquivos=arquivos, tipo_gerenciamento=TipoGerenciamentoArquivo.gerenciamento_meta)

        arquivos_meta_salvos = []
        for arquivo_id in arquivos_ids:
            db_arquivo = await self.repository.create_gerenciamento_meta_arquivo(gerenciamento_meta_id=gerenciamento_meta_id, arquivo_id=arquivo_id)
            arquivos_meta_salvos.append(db_arquivo)

        return arquivos_meta_salvos

    async def create_gerenciamento_qualitativo_arquivo(self, gerenciamento_qualitativo_id: int, fotos, relatorios):
        await self.verify.gerenciamento_qualitativo_exists(gerenciamento_qualitativo_id)

        nomes_fotos = [foto.filename for foto in fotos]
        nomes_relatorios = [relatorio.filename for relatorio in relatorios]

        ValidacaoArquivoService.validar_fotos_projeto(nomes_fotos)
        ValidacaoArquivoService.validar_relatorio_parcial(nomes_relatorios)

        fotos_ids = await self.create_arquivo(gerenciamento_id=gerenciamento_qualitativo_id, arquivos=fotos, tipo_gerenciamento=TipoGerenciamentoArquivo.gerenciamento_qualitativo_fotos_do_projeto)
        relatorios_ids = await self.create_arquivo(gerenciamento_id=gerenciamento_qualitativo_id, arquivos=relatorios, tipo_gerenciamento=TipoGerenciamentoArquivo.gerenciamento_qualitativo_relatorio_parcial)

        arquivos_ids = fotos_ids + relatorios_ids

        arquivos_qualitativo_salvos = []
        for arquivo_id in arquivos_ids:
            db_arquivo = await self.repository.create_gerenciamento_qualitativo_arquivo(gerenciamento_qualitativo_id=gerenciamento_qualitativo_id, arquivo_id=arquivo_id)
            arquivos_qualitativo_salvos.append(db_arquivo)

        return arquivos_qualitativo_salvos

    async def create_gerenciamento_contrapartida_arquivo(self, gerenciamento_contrapartida_id: int, arquivos):
        await self.verify.gerenciamento_contrapartida_exists(gerenciamento_contrapartida_id)

        nomes_arquivos = [arquivo.filename for arquivo in arquivos]

        ValidacaoArquivoService.validar_comprovacao_contrapartida(nomes_arquivos)

        arquivos_ids = await self.create_arquivo(gerenciamento_id=gerenciamento_contrapartida_id, arquivos=arquivos, tipo_gerenciamento=TipoGerenciamentoArquivo.gerenciamento_contrapartida)

        arquivos_qualitativo_salvos = []
        for arquivo_id in arquivos_ids:
            db_arquivo = await self.repository.create_gerenciamento_contrapartida_arquivo(gerenciamento_contrapartida_id=gerenciamento_contrapartida_id, arquivo_id=arquivo_id)
            arquivos_qualitativo_salvos.append(db_arquivo)

        return arquivos_qualitativo_salvos

    async def delete_arquivo(self, arquivo_id):
        arquivo = await self.get_gerenciamento_arquivo_by_id(arquivo_id)

        if os.path.exists(arquivo.uri):
            os.remove(arquivo.uri)

        await self.repository.delete_gerenciamento_arquivo(arquivo_id)

        return {'message': 'arquivo deleted'}
