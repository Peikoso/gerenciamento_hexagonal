import datetime
import uuid
from typing import List

from infrastructure.repositories.gerenciamentorepository import GerenciamentoPropostaInMemoryRepository

from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoComentario, GerenciamentoProposta
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import GerenciamentoComentarioDTO, GerenciamentoPropostaDTO


class GerenciamentoPropostaServices:
    def __init__(self, repositoryGerenciamento: GerenciamentoPropostaInMemoryRepository):
        self.repositoryGerenciamento = repositoryGerenciamento

    async def get_gerenciamentoProposta(self) -> List[GerenciamentoProposta]:
        gerenciamentoPropostas = await self.repositoryGerenciamento.get_gerenciamentoProposta()

        return gerenciamentoPropostas

    async def get_gerenciamentoProposta_by_id(self, gerenciamentoProposta_id: uuid.UUID):
        gerenciamentoProposta = await self.repositoryGerenciamento.get_gerenciamentoProposta_by_id(gerenciamentoProposta_id)

        return gerenciamentoProposta

    async def create_gerenciamentoProposta(self, gerenciamentoPropostaDTO: GerenciamentoPropostaDTO) -> GerenciamentoProposta:
        gerenciamentoProposta = GerenciamentoProposta(id=uuid.uuid4(), criado_em=datetime.datetime.now(), **gerenciamentoPropostaDTO.model_dump())
        gerenciamentoProposta = await self.repositoryGerenciamento.create_gerenciamentoProposta(gerenciamentoProposta)

        return gerenciamentoProposta

    async def delete_gerenciamentoProposta(self, gerenciamentoProposta_id: uuid.UUID):
        delete = await self.repositoryGerenciamento.delete_gerenciamentoProposta(gerenciamentoProposta_id)

        return delete

    async def update_gerenciamentoProposta(self, gerenciamentoProposta_id: uuid.UUID, gerenciamentoProposta_data: GerenciamentoProposta):
        gerenciamentoProposta = await self.repositoryGerenciamento.update_gerenciamentoProposta(gerenciamentoProposta_id, gerenciamentoProposta_data)

        return gerenciamentoProposta

    async def create_gerenciamentoPropostaComentario(self, gerenciamentoProposta_id: uuid.UUID, gerenciamentoComentarioDTO: GerenciamentoComentarioDTO) -> GerenciamentoProposta:
        gerenciamentoComentario = GerenciamentoComentario(id=uuid.uuid4(), data_cricao=datetime.datetime.now(), **gerenciamentoComentarioDTO.model_dump())
        gerenciamentoProposta = await self.repositoryGerenciamento.create_gerenciamentoPropostaComentario(gerenciamentoProposta_id, gerenciamentoComentario)

        return gerenciamentoProposta


class GerenciamentoComentarioServices: ...
