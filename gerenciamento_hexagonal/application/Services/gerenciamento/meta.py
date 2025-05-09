from gerenciamento_hexagonal.application.services.gerenciamento.proposta import GerenciamentoPropostaServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoMeta
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import GerenciamentoMetaDTO
from gerenciamento_hexagonal.domain.repositories.gerenciamento import GerenciamentoMetaRepository


class GerenciamentoMetaServices:
    def __init__(self, repository: GerenciamentoMetaRepository, service_proposta: GerenciamentoPropostaServices):
        self.repository = repository
        self.service_proposta = service_proposta

    async def get_gerenciamento_meta(self) -> list[GerenciamentoMeta]:
        gerenciamento_metas = await self.repository.get_gerenciamento_meta()

        return gerenciamento_metas

    async def get_gerenciamento_meta_by_id(self, gerenciamento_meta_id: int) -> GerenciamentoMeta:
        gerenciamento_meta = await self.repository.get_gerenciamento_meta_by_id(gerenciamento_meta_id)
        if not gerenciamento_meta:
            raise NotFoundError(f'gerenciamento_meta with ID {gerenciamento_meta_id} not found')

        return gerenciamento_meta

    async def create_gerenciamento_meta(self, gerenciamento_proposta_id: int, gerenciamento_meta: GerenciamentoMetaDTO) -> GerenciamentoMeta:
        await self.service_proposta.get_gerenciamento_proposta_by_id(gerenciamento_proposta_id)

        gerenciamento_meta = GerenciamentoMeta(**gerenciamento_meta.model_dump())
        gerenciamento_meta = await self.repository.create_gerenciamento_meta(gerenciamento_proposta_id, gerenciamento_meta)

        return gerenciamento_meta

    async def update_gerenciamento_meta(self, gerenciamento_meta_id: int, gerenciamento_meta: GerenciamentoMetaDTO) -> GerenciamentoMeta:
        await self.get_gerenciamento_meta_by_id(gerenciamento_meta_id)

        gerenciamento_meta = GerenciamentoMeta(**gerenciamento_meta.model_dump())
        gerenciamento_meta = await self.repository.update_gerenciamento_meta(gerenciamento_meta_id, gerenciamento_meta)

        return gerenciamento_meta

    async def delete_gerenciamento_meta(self, gerenciamento_meta_id: int) -> bool:
        await self.get_gerenciamento_meta_by_id(gerenciamento_meta_id)

        await self.repository.delete_gerenciamento_meta(gerenciamento_meta_id)

        return {'message': f'gerenciamento_meta with ID {gerenciamento_meta_id} deleted'}
