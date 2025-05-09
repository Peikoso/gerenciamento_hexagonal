from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import RelatorioResponse
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy_repository import RelatorioRepository


class RelatorioServices:
    def __init__(self, repository_relatorio: RelatorioRepository):
        self.repository = repository_relatorio

    async def get_relatorio(self, gerenciamento_proposta_id: int) -> RelatorioResponse:
        relatorio = await self.repository.get_relatorio(gerenciamento_proposta_id)
        if not relatorio:
            raise NotFoundError(f'gerenciamento_proposta with {gerenciamento_proposta_id} ID not found')

        return relatorio
