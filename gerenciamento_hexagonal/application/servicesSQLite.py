from typing import List

from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import (
    NotFoundError,
)
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoComentario, GerenciamentoProposta
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import (
    GerenciamentoComentarioDTO,
    GerenciamentoPropostaDTO,
)
from gerenciamento_hexagonal.infrastructure.repositories.SQLiterepository import (
    GerenciamentoComentarioSQLiteRepository,
    GerenciamentoPropostaSQLiteRepository,
)


class GerenciamentoPropostaSQLiteServices:
    def __init__(self, repositoryGerenciamento: GerenciamentoPropostaSQLiteRepository):
        self.repositoryGerenciamento = repositoryGerenciamento

    async def get_gerenciamentoProposta(self) -> List[GerenciamentoProposta]:
        gerenciamentoPropostas = await self.repositoryGerenciamento.get_gerenciamentoProposta()

        return gerenciamentoPropostas

    async def get_gerenciamentoProposta_by_id(self, gerenciamentoProposta_id: int):
        gerenciamentoProposta = await self.repositoryGerenciamento.get_gerenciamentoProposta_by_id(gerenciamentoProposta_id)
        if not gerenciamentoProposta:
            raise NotFoundError(f'gerenciamento_proposta with ID {gerenciamentoProposta_id} not found')

        return gerenciamentoProposta

    async def create_gerenciamentoProposta(self, gerenciamentoPropostaDTO: GerenciamentoPropostaDTO) -> GerenciamentoProposta:
        gerenciamentoProposta = GerenciamentoProposta(**gerenciamentoPropostaDTO.model_dump())
        gerenciamentoProposta = await self.repositoryGerenciamento.create_gerenciamentoProposta(gerenciamentoProposta)

        return gerenciamentoProposta

    async def delete_gerenciamentoProposta(self, gerenciamentoProposta_id: int):
        delete = await self.repositoryGerenciamento.delete_gerenciamentoProposta(gerenciamentoProposta_id)
        if not delete:
            raise NotFoundError(f'gerenciamento_proposta with ID {gerenciamentoProposta_id} not found')

        return delete

    async def update_gerenciamentoProposta(self, gerenciamentoProposta_id: int, gerenciamentoProposta_data: GerenciamentoPropostaDTO) -> GerenciamentoProposta:
        gerenciamentoProposta = GerenciamentoProposta(**gerenciamentoProposta_data.model_dump())
        gerenciamentoProposta = await self.repositoryGerenciamento.update_gerenciamentoProposta(gerenciamentoProposta_id, gerenciamentoProposta)
        if not gerenciamentoProposta:
            raise NotFoundError(f'gerenciamento_proposta with ID {gerenciamentoProposta_id} not found')

        return gerenciamentoProposta

    async def create_gerenciamentoPropostaComentario(self, gerenciamentoProposta_id: int, gerenciamentoComentarioDTO: GerenciamentoComentarioDTO) -> GerenciamentoProposta:
        gerenciamentoComentario = GerenciamentoComentario(**gerenciamentoComentarioDTO.model_dump())
        gerenciamentoProposta = await self.repositoryGerenciamento.create_gerenciamentoPropostaComentario(gerenciamentoProposta_id, gerenciamentoComentario)
        if not gerenciamentoProposta:
            raise NotFoundError(f'gerenciamento_proposta with ID {gerenciamentoProposta_id} not found')

        return gerenciamentoProposta


class GerenciamentoComentarioSQLiteServices:
    def __init__(self, repositoryGerenciamento: GerenciamentoComentarioSQLiteRepository):
        self.repositoryGerenciamento = repositoryGerenciamento

    async def get_gerenciamentoComentario_by_id(self, gerenciamentoComentario_id: int) -> GerenciamentoComentario:
        gerenciamentoComentario = await self.repositoryGerenciamento.get_gerenciamentoComentario_by_id(gerenciamentoComentario_id)
        if not gerenciamentoComentario:
            raise NotFoundError(f'gerenciamento_comentario with ID {gerenciamentoComentario_id} not found')

        return gerenciamentoComentario

    async def update_gerenciamentoComentario(self, gerenciamentoComentario_id: int, gerenciamentoComentario_data: GerenciamentoComentarioDTO) -> GerenciamentoComentario:
        gerenciamentoComentario = GerenciamentoComentario(**gerenciamentoComentario_data.model_dump())
        gerenciamentoComentario = await self.repositoryGerenciamento.update_gerenciamentoComentario(gerenciamentoComentario_id, gerenciamentoComentario)
        if not gerenciamentoComentario:
            raise NotFoundError(f'gerenciamento_comentario with ID {gerenciamentoComentario_id} not found')

        return gerenciamentoComentario

    async def delete_gerenciamentoComentario(self, gerenciamentoComentario_id: int) -> None:
        delete = await self.repositoryGerenciamento.delete_gerenciamentoComentario(gerenciamentoComentario_id)

        if not delete:
            raise NotFoundError(f'gerenciamento_comentario with ID {gerenciamentoComentario_id} not found')

        return delete

    async def get_gerenciamentoComentario(self) -> list[GerenciamentoComentario]:
        gerenciamentoComentarios = await self.repositoryGerenciamento.get_gerenciamentoComentario()

        return gerenciamentoComentarios
