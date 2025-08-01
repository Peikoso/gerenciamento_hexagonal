from abc import ABC, abstractmethod

from gerenciamento_hexagonal.application.services.interfaces.gerenciamento.verify_gerenciamento import VerifyGerenciamentoExists
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoQualitativo
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoComentarioDTO, GerenciamentoQualitativoDTO
from gerenciamento_hexagonal.domain.repositories.gerenciamento import GerenciamentoQualitativoRepository


class GerenciamentoQualitativoServices(ABC):
    def __init__(self, repository: GerenciamentoQualitativoRepository, verify: VerifyGerenciamentoExists):
        self.repository = repository
        self.verify = verify

    @abstractmethod
    async def get_gerenciamento_qualitativo(self) -> list[GerenciamentoQualitativo]:
        pass

    @abstractmethod
    async def get_gerenciamento_qualitativo_by_id(self, gerenciamento_qualitativo_id: int) -> GerenciamentoQualitativo:
        pass

    @abstractmethod
    async def create_gerenciamento_qualitativo(self, gerenciamento_proposta_id: int, gerenciamento_qualitativo: GerenciamentoQualitativoDTO) -> GerenciamentoQualitativo:
        pass

    @abstractmethod
    async def update_gerenciamento_qualitativo(self, gerenciamento_qualitativo_id: int, gerenciamento_qualitativo: GerenciamentoQualitativoDTO) -> GerenciamentoQualitativo | None:
        pass

    @abstractmethod
    async def delete_gerenciamento_qualitativo(self, gerenciamento_qualitativo_id: int):
        pass

    @abstractmethod
    async def create_gerenciamento_qualitativo_comentario(self, gerenciamento_qualitativo_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO) -> GerenciamentoQualitativo:
        pass
