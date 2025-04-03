import uuid
from typing import List

from domain.models.gerenciamento import GerenciamentoComentario, GerenciamentoProposta
from domain.repositories.gerenciamento import GerenciamentoComentarioRepository, GerenciamentoPropostaRepository
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
            if isinstance(gerenciamentoProposta, dict) and gerenciamentoProposta['id'] == gerenciamentoProposta_id:
                gerenciamentoProposta.update(gerenciamentoProposta_data)

                return gerenciamentoProposta_data

        return None

    async def delete_gerenciamentoProposta(self, gerenciamentoProposta_id: uuid.UUID) -> bool:
        for gerenciamentoProposta in self._database.gerenciamentoPropostaDB:
            if gerenciamentoProposta['id'] == gerenciamentoProposta_id:
                self._database.gerenciamentoPropostaDB.remove(gerenciamentoProposta)

                return True

        return False

    async def create_gerenciamentoPropostaComentario(self, gerenciamentoProposta_id: uuid.UUID, gerenciamentoComentario_data: GerenciamentoComentario) -> GerenciamentoProposta:
        gerenciamentoComentario_dict = gerenciamentoComentario_data.model_dump()
        for gerenciamentoProposta in self._database.gerenciamentoPropostaDB:
            if isinstance(gerenciamentoProposta, dict) and gerenciamentoProposta['id'] == gerenciamentoProposta_id:
                if isinstance(gerenciamentoProposta['metas_comentarios'], list):
                    gerenciamentoProposta['metas_comentarios'].append(gerenciamentoComentario_dict)

                    return gerenciamentoProposta

        return None


class GerenciamentoComentarioInMemoryRepository(GerenciamentoComentarioRepository):
    def __init__(self, database: Database):
        self._database = database

    async def get_gerenciamentoComentario_by_id(self, gerenciamentoComentario_id: uuid) -> GerenciamentoComentario | None:
        pass

    async def create_gerenciamentoComentario(self, gerenciamentoComentario: GerenciamentoComentario) -> GerenciamentoComentario:
        gerenciamentoComentario_dict = gerenciamentoComentario.model_dump()
        self._database.gerenciamentoComentarioDB.append(gerenciamentoComentario_dict)
        return gerenciamentoComentario_dict

    async def update_gerenciamentoComentario(self, gerenciamentoComentario: GerenciamentoComentario) -> GerenciamentoComentario | None:
        pass

    async def delete_gerenciamentoComentario(self, gerenciamentoComentario_id: uuid) -> None:
        pass

    async def get_gerenciamentoComentario(self) -> list[GerenciamentoComentario]:
        return {'Gerenciamento_Comentarios': self._database.gerenciamentoComentarioDB}
