from abc import ABC, abstractmethod

from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoProposta
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoComentarioDTO, GerenciamentoPropostaDTO
from gerenciamento_hexagonal.domain.repositories.gerenciamento import GerenciamentoPropostaRepository


class GerenciamentoPropostaServices(ABC):
    def __init__(self, repository: GerenciamentoPropostaRepository):
        self.repository = repository

    @abstractmethod
    async def get_gerenciamento_proposta(self) -> list[GerenciamentoProposta]:
        pass

    @abstractmethod
    async def get_gerenciamento_proposta_by_id(self, gerenciamento_proposta_id: int):
        pass

    @abstractmethod
    async def create_gerenciamento_proposta(self, gerenciamento_proposta: GerenciamentoPropostaDTO) -> GerenciamentoProposta:
        pass

    @abstractmethod
    async def update_gerenciamento_proposta(self, gerenciamento_proposta_id: int, gerenciamento_proposta: GerenciamentoPropostaDTO) -> GerenciamentoProposta:
        pass

    @abstractmethod
    async def delete_gerenciamento_proposta(self, gerenciamento_proposta_id: int):
        pass

    @abstractmethod
    async def create_gerenciamento_proposta_comentario(self, gerenciamento_proposta_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO) -> GerenciamentoProposta:
        pass
