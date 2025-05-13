from gerenciamento_hexagonal.application.services.interfaces.verify_gerenciamento import VerifyGerenciamentoExists
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.repositories.gerenciamento import VerifyGerenciamentoExistsRepository


class VerifyGerenciamentoServices(VerifyGerenciamentoExists):
    def __init__(self, repository: VerifyGerenciamentoExistsRepository):
        self.repository = repository

    async def gerencimento_proposta_exists(self, gerenciamento_proposta_id: int) -> bool:
        exists = await self.repository.gerencimento_proposta_exists(gerenciamento_proposta_id)
        if not exists:
            raise NotFoundError(f'gerenciamento_proposta with ID {gerenciamento_proposta_id} not found')

    async def gerenciamento_meta_exists(self, gerenciamento_meta_id: int) -> bool:
        exists = await self.repository.gerenciamento_meta_exists(gerenciamento_meta_id)

        if not exists:
            raise NotFoundError(f'gerenciamento_meta with ID {gerenciamento_meta_id} not found')

    async def gerenciamento_quantitativo_exists(self, gerenciamento_quantitativo_id: int) -> bool:
        exists = await self.repository.gerenciamento_quantitativo_exists(gerenciamento_quantitativo_id)

        if not exists:
            raise NotFoundError(f'gerenciamento_quantitativo with ID {gerenciamento_quantitativo_id} not found')

    async def gerenciamento_qualitativo_exists(self, gerenciamento_qualitativo_id: int) -> bool:
        exists = await self.repository.gerenciamento_qualitativo_exists(gerenciamento_qualitativo_id)

        if not exists:
            raise NotFoundError(f'gerenciamento_qualitativo with ID {gerenciamento_qualitativo_id} not found')

    async def gerenciamento_contrapartida_exists(self, gerenciamento_contrapartida_id: int) -> bool:
        exists = await self.repository.gerenciamento_contrapartida_exists(gerenciamento_contrapartida_id)

        if not exists:
            raise NotFoundError(f'gerenciamento_contrapartida with ID {gerenciamento_contrapartida_id} not found')
