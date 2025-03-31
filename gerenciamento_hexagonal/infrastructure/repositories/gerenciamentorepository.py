import uuid
from typing import List

from domain.models.gerenciamento import GerenciamentoProposta
from domain.repositories.gerenciamento import GerenciamentoPropostaRepository
from infrastructure.database import Database


class GerenciamentoPropostaInMemoryRepository(GerenciamentoPropostaRepository):
    def __init__(self, database: Database):
        self._database = database

    async def get_gerenciamentoProposta_by_id(self, gerenciamentoProposta_id: uuid.UUID) -> GerenciamentoProposta:
        for gerenciamentoProposta in self._database.gerenciamentoPropostaDB:
            if gerenciamentoProposta['id'] == gerenciamentoProposta_id:
                return gerenciamentoProposta
        return None

    async def get_gerenciamentoProposta(self) -> List[GerenciamentoProposta]:
        return {'Gerenciamento_Propostas': self._database.gerenciamentoPropostaDB}

    async def create_gerenciamentoProposta(self, gerenciamentoProposta: GerenciamentoProposta) -> GerenciamentoProposta:
        gerenciamentoProposta_dict = gerenciamentoProposta.model_dump()
        self._database.gerenciamentoPropostaDB.append(gerenciamentoProposta_dict)
        return gerenciamentoProposta_dict

    async def update_gerenciamentoProposta(self, gerenciamentoProposta_id: uuid.UUID, gerenciamentoProposta_data: GerenciamentoProposta) -> GerenciamentoProposta | None:
        for gerenciamentoProposta in self._database.gerenciamentoPropostaDB:
            if isinstance(gerenciamentoProposta, dict):
                if gerenciamentoProposta['id'] == gerenciamentoProposta_id:
                    gerenciamentoProposta.update(gerenciamentoProposta_data)
                    return gerenciamentoProposta_data
        return None

    async def delete_gerenciamentoProposta(self, gerenciamentoProposta_id: uuid.UUID) -> bool:
        for gerenciamentoProposta in self._database.gerenciamentoPropostaDB:
            if gerenciamentoProposta['id'] == gerenciamentoProposta_id:
                self._database.gerenciamentoPropostaDB.remove(gerenciamentoProposta)
                return True
        return False
