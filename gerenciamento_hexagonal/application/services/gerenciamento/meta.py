from gerenciamento_hexagonal.application.services.interfaces.verify_gerenciamento import VerifyGerenciamentoExists
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoMeta
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoMetaDTO
from gerenciamento_hexagonal.domain.repositories.gerenciamento import GerenciamentoMetaRepository


class GerenciamentoMetaServices:
    def __init__(self, repository: GerenciamentoMetaRepository, verify: VerifyGerenciamentoExists):
        self.repository = repository
        self.verify = verify

    async def get_gerenciamento_meta(self) -> list[GerenciamentoMeta]:
        gerenciamento_metas = await self.repository.get_gerenciamento_meta()

        return gerenciamento_metas

    async def get_gerenciamento_meta_by_id(self, gerenciamento_meta_id: int) -> GerenciamentoMeta:
        gerenciamento_meta = await self.repository.get_gerenciamento_meta_by_id(gerenciamento_meta_id)
        if not gerenciamento_meta:
            raise NotFoundError(f'gerenciamento_meta with ID {gerenciamento_meta_id} not found')

        return gerenciamento_meta

    async def create_gerenciamento_meta(self, gerenciamento_proposta_id: int, gerenciamento_meta: GerenciamentoMetaDTO) -> GerenciamentoMeta:
        await self.verify.gerencimento_proposta_exists(gerenciamento_proposta_id)

        gerenciamento_meta = GerenciamentoMeta(**gerenciamento_meta.model_dump())
        gerenciamento_meta = await self.repository.create_gerenciamento_meta(gerenciamento_proposta_id, gerenciamento_meta)

        return gerenciamento_meta

    async def update_gerenciamento_meta(self, gerenciamento_meta_id: int, gerenciamento_meta: GerenciamentoMetaDTO) -> GerenciamentoMeta:
        await self.get_gerenciamento_meta_by_id(gerenciamento_meta_id)

        gerenciamento_meta = GerenciamentoMeta(**gerenciamento_meta.model_dump())
        gerenciamento_meta = await self.repository.update_gerenciamento_meta(gerenciamento_meta_id, gerenciamento_meta)

        return gerenciamento_meta

    async def delete_gerenciamento_meta(self, gerenciamento_meta_id: int) -> bool:
        gerenciamento_meta = await self.get_gerenciamento_meta_by_id(gerenciamento_meta_id)
        if gerenciamento_meta.arquivos_ids:
            raise ValueError(f'gerenciament_meta with ID: {gerenciamento_meta_id} cannot be deleted because it has associated files with IDs: {gerenciamento_meta.arquivos_ids}.')

        await self.repository.delete_gerenciamento_meta(gerenciamento_meta_id)

        return {'message': f'gerenciamento_meta with ID {gerenciamento_meta_id} deleted'}
