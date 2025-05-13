import os
import re
import unicodedata

TIPOS_VALIDOS = {
    'REGISTRO_DA_META': {'pdf'},
    'FOTOS_DO_PROJETO': {'jpg', 'jpeg', 'png', 'bmp', 'webp'},
    'RELATORIO_PARCIAL': {'pdf'},
    'COMPROVACAO_DA_CONTRAPARTIDA': {'pdf'},
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
        ext = ext.lower().lstrip('.')

        if ext not in TIPOS_VALIDOS.get(tipo, set()):
            tipos = ', '.join(TIPOS_VALIDOS[tipo])
            raise ValueError(f"Extensão inválida para tipo '{tipo}': {nome_arquivo}. Permitidas: {tipos}")

    @staticmethod
    def validar_arquivos_metas(nomes_arquivos: list[str]) -> None:
        for nome_arquivo in nomes_arquivos:
            ValidacaoArquivoService.validar_arquivo_individual(nome_arquivo, 'REGISTRO_DA_META')

    @staticmethod
    def validar_fotos_projeto(nomes_arquivos: list[str]) -> None:
        count = 0
        min = 5
        max = 10
        for nome_arquivo in nomes_arquivos:
            ValidacaoArquivoService.validar_arquivo_individual(nome_arquivo, 'FOTOS_DO_PROJETO')
            count += 1

        if count < min:
            raise ValueError('min of 5 FOTOS_DO_PROJETO')
        if count > max:
            raise ValueError('max of 10 FOTOS_DO_PROJETO')

    @staticmethod
    def validar_relatorio_parcial(nomes_arquivos: list[str]) -> None:
        for nome_arquivo in nomes_arquivos:
            ValidacaoArquivoService.validar_arquivo_individual(nome_arquivo, 'RELATORIO_PARCIAL')

    @staticmethod
    def validar_comprovacao_contrapartida(nomes_arquivos: list[str]) -> None:
        for nome_arquivo in nomes_arquivos:
            ValidacaoArquivoService.validar_arquivo_individual(nome_arquivo, 'COMPROVACAO_DA_CONTRAPARTIDA')
