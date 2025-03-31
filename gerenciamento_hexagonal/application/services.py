import datetime
import uuid
from typing import List

from infrastructure.repositories.gerenciamentorepository import GerenciamentoPropostaInMemoryRepository

from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoProposta, GerenciamentoPropostaDTO


class GerenciamentoPropostaServices:
    def __init__(self, repositoryGerenciamentoProposta: GerenciamentoPropostaInMemoryRepository):
        self.repositoryGerenciamentoProposta = repositoryGerenciamentoProposta

    async def get_gerenciamentoProposta(self) -> List[GerenciamentoProposta]:
        gerenciamentoPropostas = await self.repositoryGerenciamentoProposta.get_gerenciamentoProposta()

        return gerenciamentoPropostas

    async def get_gerenciamentoProposta_by_id(self, gerenciamentoProposta_id: uuid.UUID):
        gerenciamentoProposta = await self.repositoryGerenciamentoProposta.get_gerenciamentoProposta_by_id(gerenciamentoProposta_id)
        return gerenciamentoProposta

    async def create_gerenciamentoProposta(self, gerenciamentoPropostaDTO: GerenciamentoPropostaDTO) -> GerenciamentoProposta:
        gerenciamentoProposta = GerenciamentoProposta(id=uuid.uuid4(), criado_em=datetime.datetime.now(), **gerenciamentoPropostaDTO.model_dump())
        gerenciamentoProposta = await self.repositoryGerenciamentoProposta.create_gerenciamentoProposta(gerenciamentoProposta)
        return gerenciamentoProposta

    async def delete_gerenciamentoProposta(self, gerenciamentoProposta_id: uuid.UUID):
        delete = await self.repositoryGerenciamentoProposta.delete_gerenciamentoProposta(gerenciamentoProposta_id)
        return delete

    async def update_gerenciamentoProposta(self, gerenciamentoProposta_id: uuid.UUID, gerenciamentoProposta_data: GerenciamentoProposta):
        gerenciamentoProposta = await self.repositoryGerenciamentoProposta.update_gerenciamentoProposta(gerenciamentoProposta_id, gerenciamentoProposta_data)
        return gerenciamentoProposta
