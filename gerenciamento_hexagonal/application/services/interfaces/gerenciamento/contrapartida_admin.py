from abc import ABC, abstractmethod

from gerenciamento_hexagonal.application.services.interfaces.gerenciamento.verify_gerenciamento import VerifyGerenciamentoExists
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoContrapartidaAdmin
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoContrapartidaAdminDTO
from gerenciamento_hexagonal.domain.repositories.gerenciamento import GerenciamentoContrapartidaAdminRepository


class GerenciamentoContrapartidaAdminServices(ABC):
    def __init__(self, repository: GerenciamentoContrapartidaAdminRepository, verify: VerifyGerenciamentoExists):
        self.repository = repository
        self.verify = verify

    @abstractmethod
    async def get_gerenciamento_contrapartida_admin(self) -> list[GerenciamentoContrapartidaAdmin]:
        pass

    @abstractmethod
    async def get_gerenciamento_contrapartida_admin_by_id(self, gerenciamento_contrapartida_admin_id: int) -> GerenciamentoContrapartidaAdmin | None:
        pass

    @abstractmethod
    async def create_gerenciamento_contrapartida_admin(self, gerenciamento_contrapartida_id: int, gerenciamento_contrapartida_admin: GerenciamentoContrapartidaAdminDTO) -> GerenciamentoContrapartidaAdmin:
        pass

    @abstractmethod
    async def update_gerenciamento_contrapartida_admin(self, gerenciamento_contrapartida_admin_id: int, gerenciamento_contrapartida_admin: GerenciamentoContrapartidaAdmin) -> GerenciamentoContrapartidaAdmin:
        pass

    @abstractmethod
    async def delete_gerenciamento_contrapartida_admin(self, gerenciamento_contrapartida_admin_id: int):
        pass
