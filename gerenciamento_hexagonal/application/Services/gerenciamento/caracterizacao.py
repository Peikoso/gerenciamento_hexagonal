from gerenciamento_hexagonal.application.services.gerenciamento.quantitativo import GerenciamentoQuantitativoServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoCaracterizacao
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import GerenciamentoCaracterizacaoDTO
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy_repository import GerenciamentoCaracterizacaoRepository


class GerenciamentoCaracterizacaoServices:
    def __init__(self, repository: GerenciamentoCaracterizacaoRepository, service_quantitativo: GerenciamentoQuantitativoServices):
        self.repository = repository
        self.service_quantitativo = service_quantitativo

    async def get_gerenciamento_caracterizacao(self) -> list[GerenciamentoCaracterizacao]:
        gerenciamento_caracterizacoes = await self.repository.get_gerenciamento_caracterizacao()

        return gerenciamento_caracterizacoes

    async def get_gerenciamento_caracterizacao_by_id(self, gerenciamento_caracterizacao_id: int) -> GerenciamentoCaracterizacao:
        gerenciamento_caracterizacao = await self.repository.get_gerenciamento_caracterizacao_by_id(gerenciamento_caracterizacao_id)

        if not gerenciamento_caracterizacao:
            raise NotFoundError(f'gerenciamento_caracterizacao with ID: {gerenciamento_caracterizacao_id} not found')

        return gerenciamento_caracterizacao

    async def create_gerenciamento_caracterizacao(self, gerenciamento_quantitativo_id: int, gerenciamento_caracterizacao: GerenciamentoCaracterizacaoDTO) -> GerenciamentoCaracterizacao:
        await self.service_quantitativo.get_gerenciamento_quantitativo_by_id(gerenciamento_quantitativo_id)

        gerenciamento_caracterizacao.categorizacoes_ids = list(set(gerenciamento_caracterizacao.categorizacoes_ids))
        categorizacao = await self.repository.find_categorizacoes_by_ids(gerenciamento_caracterizacao.categorizacoes_ids)

        if categorizacao:
            raise NotFoundError(f'categorizacao with ID: {categorizacao} not found')

        gerenciamento_caracterizacao = GerenciamentoCaracterizacao(**gerenciamento_caracterizacao.model_dump())
        gerenciamento_caracterizacao = await self.repository.create_gerenciamento_caracterizacao(gerenciamento_quantitativo_id, gerenciamento_caracterizacao)

        return gerenciamento_caracterizacao

    async def update_gerenciamento_caracterizacao(self, gerenciamento_caracterizacao_id: int, gerenciamento_caracterizacao: GerenciamentoCaracterizacaoDTO) -> GerenciamentoCaracterizacao:
        await self.get_gerenciamento_caracterizacao_by_id(gerenciamento_caracterizacao_id)

        gerenciamento_caracterizacao.categorizacoes_ids = list(set(gerenciamento_caracterizacao.categorizacoes_ids))
        categorizacao = await self.repository.find_categorizacoes_by_ids(gerenciamento_caracterizacao.categorizacoes_ids)

        if categorizacao:
            raise NotFoundError(f'categorizacao with ID: {categorizacao} not found')

        gerenciamento_caracterizacao = GerenciamentoCaracterizacao(**gerenciamento_caracterizacao.model_dump())
        gerenciamento_caracterizacao = await self.repository.update_gerenciamento_caracterizacao(gerenciamento_caracterizacao_id, gerenciamento_caracterizacao)

        return gerenciamento_caracterizacao

    async def delete_gerenciamento_caracterizacao(self, gerenciamento_caracterizacao_id: int):
        await self.get_gerenciamento_caracterizacao_by_id(gerenciamento_caracterizacao_id)

        await self.repository.delete_gerenciamento_caracterizacao(gerenciamento_caracterizacao_id)

        return {'message': f'gerenciamento_caracterizacao with ID {gerenciamento_caracterizacao_id} deleted'}
