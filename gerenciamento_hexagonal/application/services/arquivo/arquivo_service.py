import os
from datetime import datetime

from gerenciamento_hexagonal.domain.services.arquivo_service import normalizar_nome_arquivo
from gerenciamento_hexagonal.domain.services.validations import ValidacaoService


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

    async def verifica_tamanho(self):
        self.tamanho = len(self._get_arquivo().content)  # Tamanho em bytes
        limite_mb = 10
        limite_bytes = limite_mb * 1024 * 1024  # 10MB
        if self.tamanho > limite_bytes:
            print(f'Tamanho excedido: {self.tamanho} bytes')
            raise ValueError(f'size exceeded {limite_mb} MB')

    async def processar_arquivo(self):
        self.tamanho = len(self._get_arquivo().content)
        nome_original, self.extensao = os.path.splitext(self._get_arquivo().filename)
        self.extensao = self.extensao.lower().lstrip('.')
        self.nome = nome_original
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S%f')

        nome_normalizado = normalizar_nome_arquivo(self.nome)
        self.uri = f'arquivos/{nome_normalizado}_{self._rel_id}_{timestamp}.{self.extensao}'

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
            ValidacaoService.validar_tamanho_string('Nome Arquivo', arquivo.filename, 30)
            await service.verifica_tamanho()
            await service.processar_arquivo()  # Processa cada arquivo individualmente
            metadados.append(service.get_metadados())  # Coleta os metadados após o processamento
        return metadados
