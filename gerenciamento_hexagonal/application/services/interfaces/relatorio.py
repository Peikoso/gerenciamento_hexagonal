from abc import ABC

from gerenciamento_hexagonal.application.services.gerenciamento.caracterizacao import GerenciamentoCaracterizacaoServices
from gerenciamento_hexagonal.application.services.gerenciamento.contrapartida import GerenciamentoContrapartidaServices
from gerenciamento_hexagonal.application.services.gerenciamento.meta import GerenciamentoMetaServices
from gerenciamento_hexagonal.application.services.gerenciamento.proposta import GerenciamentoPropostaServices
from gerenciamento_hexagonal.application.services.gerenciamento.qualitativo import GerenciamentoQualitativoServices
from gerenciamento_hexagonal.application.services.gerenciamento.quantitativo import GerenciamentoQuantitativoServices
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import RelatorioDTO, RelatorioResponse
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.relatorio import RelatorioRepository


class RelatorioServices(ABC):
    def __init__(  # noqa: PLR0913, PLR0917
        self, repository_relatorio: RelatorioRepository, proposta: GerenciamentoPropostaServices, meta: GerenciamentoMetaServices, quantitativo: GerenciamentoQuantitativoServices, qualitativo: GerenciamentoQualitativoServices, caracterizacao: GerenciamentoCaracterizacaoServices, contrapartida: GerenciamentoContrapartidaServices
    ):
        self.repository = repository_relatorio
        self.proposta = proposta
        self.meta = meta
        self.quantitativo = quantitativo
        self.qualitativo = qualitativo
        self.caracterizacao = caracterizacao
        self.contrapartida = contrapartida

    async def get_relatorio(self, gerenciamento_proposta_id: int) -> RelatorioResponse:
        pass

    async def create_relatorio(self, relatorio: RelatorioDTO):
        pass
