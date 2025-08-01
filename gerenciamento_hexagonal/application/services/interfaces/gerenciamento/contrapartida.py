from abc import ABC, abstractmethod

from gerenciamento_hexagonal.application.services.interfaces.gerenciamento.verify_gerenciamento import VerifyGerenciamentoExists
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoContrapartida
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoContrapartidaDTO
from gerenciamento_hexagonal.domain.repositories.gerenciamento import GerenciamentoContrapartidaRepository


class GerenciamentoContrapartidaServices(ABC):
    def __init__(self, repository: GerenciamentoContrapartidaRepository, verify: VerifyGerenciamentoExists):
        self.repository = repository
        self.verify = verify

    @abstractmethod
    async def get_gerenciamento_contrapartida(self) -> list[GerenciamentoContrapartida]:
        pass

    @abstractmethod
    async def get_gerenciamento_contrapartida_by_id(self, gerenciamento_contrapartida_id: int) -> GerenciamentoContrapartida | None:
        pass

    @abstractmethod
    async def create_gerenciamento_contrapartida(self, gerenciamento_proposta_id: int, gerenciamento_contrapartida: GerenciamentoContrapartidaDTO) -> GerenciamentoContrapartida:
        pass

    @abstractmethod
    async def update_gerenciamento_contrapartida(self, gerenciamento_contrapartida_id: int, gerenciamento_contrapartida: GerenciamentoContrapartidaDTO) -> GerenciamentoContrapartida:
        pass

    @abstractmethod
    async def delete_gerenciamento_contrapartida(self, gerenciamento_contrapartida_id: int):
        pass
