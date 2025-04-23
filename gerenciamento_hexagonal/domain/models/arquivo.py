"""import uuid
from abc import ABC, abstractmethod
from enum import Enum

from pydantic import BaseModel, Field

from gerenciamento_hexagonal.domain.models.enums_specs import TipoArquivoContexto


class TipoArquivo(BaseModel):
    id: str  # CharField(primary_key=True, max_length=32, blank=False, null=False)
    contexto: TipoArquivoContexto  # CharField(max_length=32, choices=TipoArquivoContexto, null=False, blank=False)
    descricao: str  # CharField(null=False, unique=True, max_length=120)
    info: str  # CharField(max_length=1000, default=None, blank=False)


class Arquivo(ABC):
    tipo: TipoArquivo  # ForeignKey(TipoArquivo, null=False, on_delete=models.CASCADE)
    nome: str  # CharField(max_length=255, null=False, blank=False)
    extensao: str  # CharField(max_length=4, null=False, blank=False)
    tamanho: int  # IntegerField(null=False, db_comment='Tamanho do arquivo em bytes')
    uri: str  # URLField(null=False)
    id: uuid.UUID = Field(default_factory=uuid.uuid4)  # UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    @abstractmethod
    def _get_arquivo(self):
        pass

    @abstractmethod
    def _get_id(self):
        pass

    @abstractmethod
    def _get_rel_id(self):
        pass

    @abstractmethod
    def manipula_arquivo(self):
        pass

    @abstractmethod
    def _save_file(self):
        pass

    @abstractmethod
    def _make_name_extension(self):
        pass

    @abstractmethod
    def _make_tamanho(self):
        pass

    @abstractmethod
    def _make_uri(self):
        pass

    @abstractmethod
    def save(self, *args, **kwargs):
        pass
"""