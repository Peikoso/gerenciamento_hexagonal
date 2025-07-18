from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError, NotNullViolationError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoComentario, GerenciamentoProposta
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoComentarioDTO, GerenciamentoPropostaDTO
from gerenciamento_hexagonal.domain.repositories.gerenciamento import GerenciamentoPropostaRepository


class GerenciamentoPropostaServices:
    def __init__(self, repository: GerenciamentoPropostaRepository):
        self.repository = repository

    async def get_gerenciamento_proposta(self) -> list[GerenciamentoProposta]:
        gerenciamento_propostas = await self.repository.get_gerenciamento_proposta()

        return gerenciamento_propostas

    async def get_gerenciamento_proposta_by_id(self, gerenciamento_proposta_id: int):
        gerenciamento_proposta = await self.repository.get_gerenciamento_proposta_by_id(gerenciamento_proposta_id)
        if not gerenciamento_proposta:
            raise NotFoundError(f'gerenciamento_proposta with ID {gerenciamento_proposta_id} not found')

        return gerenciamento_proposta

    async def create_gerenciamento_proposta(self, gerenciamento_proposta: GerenciamentoPropostaDTO) -> GerenciamentoProposta:
        gerenciamento_proposta = GerenciamentoProposta(**gerenciamento_proposta.model_dump())
        gerenciamento_proposta = await self.repository.create_gerenciamento_proposta(gerenciamento_proposta)

        return gerenciamento_proposta

    async def update_gerenciamento_proposta(self, gerenciamento_proposta_id: int, gerenciamento_proposta: GerenciamentoPropostaDTO) -> GerenciamentoProposta:
        await self.get_gerenciamento_proposta_by_id(gerenciamento_proposta_id)

        gerenciamento_proposta = GerenciamentoProposta(**gerenciamento_proposta.model_dump())
        gerenciamento_proposta = await self.repository.update_gerenciamento_proposta(gerenciamento_proposta_id, gerenciamento_proposta)

        return gerenciamento_proposta

    async def delete_gerenciamento_proposta(self, gerenciamento_proposta_id: int):
        gerenciamento_proposta = await self.get_gerenciamento_proposta_by_id(gerenciamento_proposta_id)

        if gerenciamento_proposta.arquivos_ids:
            raise NotNullViolationError('Cannot delete a gerenciamento_proposta because there are associated files.')

        not_null_violation = await self.repository.checar_gerenciamento_caracterizacao_exists(gerenciamento_proposta_id)

        if not_null_violation:
            raise NotNullViolationError('cannot delete a gerenciamento_proposta when there is an associated gerenciamento_caracterizacao')

        await self.repository.delete_gerenciamento_proposta(gerenciamento_proposta_id)

        return {'message': f'gerenciamento_proposta with ID {gerenciamento_proposta_id} deleted'}

    async def create_gerenciamento_proposta_comentario(self, gerenciamento_proposta_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO) -> GerenciamentoProposta:
        await self.get_gerenciamento_proposta_by_id(gerenciamento_proposta_id)

        gerenciamento_comentario = GerenciamentoComentario(**gerenciamento_comentario.model_dump())
        gerenciamento_proposta = await self.repository.create_gerenciamento_proposta_comentario(gerenciamento_proposta_id, gerenciamento_comentario)

        return gerenciamento_proposta
