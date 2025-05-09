import os
import re
import unicodedata
from datetime import datetime
from typing import List

TIPOS_VALIDOS = {
    'REGISTRO_DA_META': {'.pdf'},
    'FOTOS_DO_PROJETO': {'.pdf', '.png', '.jpg'},
    'RELATORIO_PARCIAL': {'.pdf'},
    'COMPROVACAO_DA_CONTRAPARTIDA': {'.pdf'},
}


def normalizar_nome_arquivo(nome_arquivo):
    # Normaliza caracteres acentuados para caracteres não acentuados
    nome_arquivo = unicodedata.normalize('NFKD', nome_arquivo).encode('ASCII', 'ignore').decode('ASCII')

    # Substitui espaços por underscore
    nome_arquivo = nome_arquivo.replace(' ', '_')

    # Remove caracteres especiais (se necessário)
    nome_arquivo = re.sub(r'[^a-zA-Z0-9_-]', '', nome_arquivo)

    return nome_arquivo


class ValidacaoArquivoService:
    @staticmethod
    def validar_arquivo_individual(nome_arquivo: str, tipo: str) -> None:
        _, ext = os.path.splitext(nome_arquivo)
        ext = ext.lower()

        if ext not in TIPOS_VALIDOS.get(tipo, set()):
            tipos = ', '.join(TIPOS_VALIDOS[tipo])
            raise ValueError(f"Extensão inválida para tipo '{tipo}': {nome_arquivo}. Permitidas: {tipos}")

    @staticmethod
    def validar_arquivos_metas(nomes_arquivos: List[str]) -> None:
        for nome_arquivo in nomes_arquivos:
            ValidacaoArquivoService.validar_arquivo_individual(nome_arquivo, 'REGISTRO_DA_META')

    @staticmethod
    def validar_fotos_projeto(nomes_arquivos: List[str]) -> None:
        for nome_arquivo in nomes_arquivos:
            ValidacaoArquivoService.validar_arquivo_individual(nome_arquivo, 'FOTOS_DO_PROJETO')

    @staticmethod
    def validar_relatorio_parcial(nomes_arquivos: List[str]) -> None:
        for nome_arquivo in nomes_arquivos:
            ValidacaoArquivoService.validar_arquivo_individual(nome_arquivo, 'RELATORIO_PARCIAL')

    @staticmethod
    def validar_comprovacao_contrapartida(nomes_arquivos: List[str]) -> None:
        for nome_arquivo in nomes_arquivos:
            ValidacaoArquivoService.validar_arquivo_individual(nome_arquivo, 'COMPROVACAO_DA_CONTRAPARTIDA')

    @staticmethod
    def validar_todos(data) -> None:
        ValidacaoArquivoService.validar_arquivos_metas(data.arquivos_metas)
        ValidacaoArquivoService.validar_fotos_projeto(data.fotos_projeto)
        ValidacaoArquivoService.validar_relatorio_parcial(data.arquivo_relatorio_parcial)
        ValidacaoArquivoService.validar_comprovacao_contrapartida(data.comprovacoes_contrapartida)


class ArquivoIndividualService:
    def __init__(self, arquivo, rel_id, base_dir, files_dir):
        self._arquivo = arquivo  # Aqui é genérico, pode ser qualquer tipo de arquivo
        self._rel_id = rel_id
        self.base_dir = base_dir
        self.files_dir = files_dir

        self.nome = None
        self.extensao = None
        self.tamanho = None
        self.uri = None

    def _get_arquivo(self):
        return self._arquivo

    async def processar_arquivo(self):
        nome_original, self.extensao = os.path.splitext(self._get_arquivo().filename)
        self.nome = nome_original
        self.tamanho = len(self._get_arquivo().content)  # Tamanho em bytes, por exemplo

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S%f')[:-3]

        nome_normalizado = normalizar_nome_arquivo(self.nome)
        self.uri = f'arquivos/{nome_normalizado}_{self._rel_id}_{timestamp}{self.extensao}'

        await self._save_file()

    async def _save_file(self):
        full_path = os.path.join(self.uri)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, 'wb+') as destination:
            destination.write(self._get_arquivo().content)  # Assume que o arquivo tem o atributo content

    def get_metadados(self):
        return {
            'nome': self.nome,
            'extensao': self.extensao,
            'tamanho': self.tamanho,
            'rel_id': self._rel_id,
            'uri': self.uri,
        }


class ArquivoServices:
    def __init__(self):
        self.base_dir = os.getcwd()
        self.files_dir = 'arquivos'

    async def processar_arquivos(self, arquivos, rel_id):
        self._arquivos = arquivos  # Lista de arquivos genéricos (não depende do FastAPI)
        self._rel_id = rel_id
        metadados = []
        for arquivo in self._arquivos:
            service = ArquivoIndividualService(arquivo, self._rel_id, self.base_dir, self.files_dir)
            await service.processar_arquivo()  # Processa cada arquivo individualmente
            metadados.append(service.get_metadados())  # Coleta os metadados após o processamento
        return metadados
