from abc import ABC, abstractmethod

from gerenciamento_hexagonal.application.services.interfaces.gerenciamento.verify_gerenciamento import VerifyGerenciamentoExists
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoMeta
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoMetaDTO
from gerenciamento_hexagonal.domain.repositories.gerenciamento import GerenciamentoMetaRepository


class GerenciamentoMetaServices(ABC):
    def __init__(self, repository: GerenciamentoMetaRepository, verify: VerifyGerenciamentoExists):
        self.repository = repository
        self.verify = verify

    @abstractmethod
    async def get_gerenciamento_meta(self) -> list[GerenciamentoMeta]:
        pass

    @abstractmethod
    async def get_gerenciamento_meta_by_id(self, gerenciamento_meta_id: int) -> GerenciamentoMeta:
        pass

    @abstractmethod
    async def create_gerenciamento_meta(self, gerenciamento_proposta_id: int, gerenciamento_meta: GerenciamentoMetaDTO) -> GerenciamentoMeta:
        pass

    @abstractmethod
    async def update_gerenciamento_meta(self, gerenciamento_meta_id: int, gerenciamento_meta: GerenciamentoMetaDTO) -> GerenciamentoMeta:
        pass

    @abstractmethod
    async def delete_gerenciamento_meta(self, gerenciamento_meta_id: int) -> bool:
        pass
