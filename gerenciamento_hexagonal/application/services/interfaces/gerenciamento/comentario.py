from abc import ABC, abstractmethod

from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoComentario
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoComentarioDTO
from gerenciamento_hexagonal.domain.repositories.gerenciamento import GerenciamentoComentarioRepository


class GerenciamentoComentarioServices(ABC):
    def __init__(self, repository: GerenciamentoComentarioRepository):
        self.repository = repository

    @abstractmethod
    async def get_gerenciamento_comentario(self) -> list[GerenciamentoComentario]:
        pass

    @abstractmethod
    async def get_gerenciamento_comentario_by_id(self, gerenciamento_comentario_id: int) -> GerenciamentoComentario:
        pass

    @abstractmethod
    async def update_gerenciamento_comentario(self, gerenciamento_comentario_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO) -> GerenciamentoComentario:
        pass

    @abstractmethod
    async def delete_gerenciamento_comentario(self, gerenciamento_comentario_id: int) -> None:
        pass
