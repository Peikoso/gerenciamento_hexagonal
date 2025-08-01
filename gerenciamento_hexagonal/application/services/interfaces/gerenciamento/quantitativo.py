from abc import ABC, abstractmethod

from gerenciamento_hexagonal.application.services.interfaces.gerenciamento.verify_gerenciamento import VerifyGerenciamentoExists
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoQuantitativo
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoComentarioDTO, GerenciamentoQuantitativoDTO
from gerenciamento_hexagonal.domain.repositories.gerenciamento import GerenciamentoQuantitativoRepository


class GerenciamentoQuantitativoServices(ABC):
    def __init__(self, repository: GerenciamentoQuantitativoRepository, verify: VerifyGerenciamentoExists):
        self.repository = repository
        self.verify = verify

    @abstractmethod
    async def get_gerenciamento_quantitativo(self) -> list[GerenciamentoQuantitativo]:
        pass

    @abstractmethod
    async def get_gerenciamento_quantitativo_by_id(self, gerenciamento_quantitativo_id: int) -> GerenciamentoQuantitativo:
        pass

    @abstractmethod
    async def create_gerenciamento_quantitativo(self, gerenciamento_proposta_id: int, gerenciamento_quantitativo: GerenciamentoQuantitativoDTO) -> GerenciamentoQuantitativo:
        pass

    @abstractmethod
    async def update_gerenciamento_quantitativo(self, gerenciamento_quantitativo_id: int, gerenciamento_quantitativo: GerenciamentoQuantitativoDTO) -> GerenciamentoQuantitativo:
        pass

    @abstractmethod
    async def delete_gerenciamento_quantitativo(self, gerenciamento_quantitativo_id: int):
        pass

    @abstractmethod
    async def create_gerenciamento_quantitativo_comentario(self, gerenciamento_quantitativo_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO) -> GerenciamentoQuantitativo:
        pass
