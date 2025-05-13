from gerenciamento_hexagonal.application.services.interfaces.verify_gerenciamento import VerifyGerenciamentoExists
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError, NotNullViolationError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoComentario, GerenciamentoQuantitativo
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoComentarioDTO, GerenciamentoQuantitativoDTO
from gerenciamento_hexagonal.domain.repositories.gerenciamento import GerenciamentoQuantitativoRepository


class GerenciamentoQuantitativoServices:
    def __init__(self, repository: GerenciamentoQuantitativoRepository, verify: VerifyGerenciamentoExists):
        self.repository = repository
        self.verify = verify

    async def get_gerenciamento_quantitativo(self) -> list[GerenciamentoQuantitativo]:
        gerenciamento_quantitativos = await self.repository.get_gerenciamento_quantitativo()

        return gerenciamento_quantitativos

    async def get_gerenciamento_quantitativo_by_id(self, gerenciamento_quantitativo_id: int) -> GerenciamentoQuantitativo:
        gerenciamento_quantitativo = await self.repository.get_gerenciamento_quantitativo_by_id(gerenciamento_quantitativo_id)

        if not gerenciamento_quantitativo:
            raise NotFoundError(f'gerenciamento_quantitativo with ID: {gerenciamento_quantitativo_id} not found')

        return gerenciamento_quantitativo

    async def create_gerenciamento_quantitativo(self, gerenciamento_proposta_id: int, gerenciamento_quantitativo: GerenciamentoQuantitativoDTO) -> GerenciamentoQuantitativo:
        await self.verify.gerencimento_proposta_exists(gerenciamento_proposta_id)

        gerenciamento_quantitativo = GerenciamentoQuantitativo(**gerenciamento_quantitativo.model_dump())
        gerenciamento_quantitativo = await self.repository.create_gerenciamento_quantitativo(gerenciamento_proposta_id, gerenciamento_quantitativo)

        return gerenciamento_quantitativo

    async def update_gerenciamento_quantitativo(self, gerenciamento_quantitativo_id: int, gerenciamento_quantitativo: GerenciamentoQuantitativoDTO) -> GerenciamentoQuantitativo:
        await self.get_gerenciamento_quantitativo_by_id(gerenciamento_quantitativo_id)

        gerenciamento_quantitativo = GerenciamentoQuantitativo(**gerenciamento_quantitativo.model_dump())
        gerenciamento_quantitativo = await self.repository.update_gerenciamento_quantitativo(gerenciamento_quantitativo_id, gerenciamento_quantitativo)

        return gerenciamento_quantitativo

    async def delete_gerenciamento_quantitativo(self, gerenciamento_quantitativo_id: int):
        await self.get_gerenciamento_quantitativo_by_id(gerenciamento_quantitativo_id)

        not_null_violation = await self.repository.checar_gerenciamento_caracterizacao_exists(gerenciamento_quantitativo_id)

        if not_null_violation:
            raise NotNullViolationError('cannot delete a gerenciamento_quantitativo when there is an associated gerenciamento_caracterizacao')

        await self.repository.delete_gerenciamento_quantitativo(gerenciamento_quantitativo_id)

        return {'message': f'gerenciamento_quantitativo with ID {gerenciamento_quantitativo_id} deleted'}

    async def create_gerenciamento_quantitativo_comentario(self, gerenciamento_quantitativo_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO) -> GerenciamentoQuantitativo:
        await self.get_gerenciamento_quantitativo_by_id(gerenciamento_quantitativo_id)

        gerenciamento_comentario = GerenciamentoComentario(**gerenciamento_comentario.model_dump())
        gerenciamento_quantitativo_comentario = await self.repository.create_gerenciamento_quantitativo_comentario(gerenciamento_quantitativo_id, gerenciamento_comentario)

        return gerenciamento_quantitativo_comentario
