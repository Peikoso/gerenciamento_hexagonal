from abc import ABC, abstractmethod

from gerenciamento_hexagonal.application.services.interfaces.gerenciamento.verify_gerenciamento import VerifyGerenciamentoExists
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoCaracterizacao
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoCaracterizacaoDTO
from gerenciamento_hexagonal.domain.repositories.gerenciamento import GerenciamentoCaracterizacaoRepository


class GerenciamentoCaracterizacaoServices(ABC):
    def __init__(self, repository: GerenciamentoCaracterizacaoRepository, verify: VerifyGerenciamentoExists):
        self.repository = repository
        self.verify = verify

    @abstractmethod
    async def get_gerenciamento_caracterizacao(self) -> list[GerenciamentoCaracterizacao]:
        pass

    @abstractmethod
    async def get_gerenciamento_caracterizacao_by_id(self, gerenciamento_caracterizacao_id: int) -> GerenciamentoCaracterizacao:
        pass

    @abstractmethod
    async def create_gerenciamento_caracterizacao(self, gerenciamento_quantitativo_id: int, gerenciamento_caracterizacao: GerenciamentoCaracterizacaoDTO) -> GerenciamentoCaracterizacao:
        pass

    @abstractmethod
    async def update_gerenciamento_caracterizacao(self, gerenciamento_caracterizacao_id: int, gerenciamento_caracterizacao: GerenciamentoCaracterizacaoDTO) -> GerenciamentoCaracterizacao:
        pass

    @abstractmethod
    async def delete_gerenciamento_caracterizacao(self, gerenciamento_caracterizacao_id: int):
        pass
