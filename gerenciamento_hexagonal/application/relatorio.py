from gerenciamento_hexagonal.application.services.gerenciamento.caracterizacao import GerenciamentoCaracterizacaoServices
from gerenciamento_hexagonal.application.services.gerenciamento.contrapartida import GerenciamentoContrapartidaServices
from gerenciamento_hexagonal.application.services.gerenciamento.meta import GerenciamentoMetaServices
from gerenciamento_hexagonal.application.services.gerenciamento.proposta import GerenciamentoPropostaServices
from gerenciamento_hexagonal.application.services.gerenciamento.qualitativo import GerenciamentoQualitativoServices
from gerenciamento_hexagonal.application.services.gerenciamento.quantitativo import GerenciamentoQuantitativoServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import (
    GerenciamentoCaracterizacaoDTO, GerenciamentoContrapartidaDTO, GerenciamentoMetaDTO, GerenciamentoPropostaDTO, GerenciamentoQualitativoDTO, GerenciamentoQuantitativoDTO, RelatorioDTO, RelatorioResponse)
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.relatorio import RelatorioRepository


class RelatorioServices:
    def __init__(  # noqa: PLR0913, PLR0917
        self, 
        repository_relatorio: RelatorioRepository, 
        proposta: GerenciamentoPropostaServices, 
        meta: GerenciamentoMetaServices, 
        quantitativo: GerenciamentoQuantitativoServices, 
        qualitativo: GerenciamentoQualitativoServices, 
        caracterizacao: GerenciamentoCaracterizacaoServices, 
        contrapartida: GerenciamentoContrapartidaServices
    ):
        self.repository = repository_relatorio
        self.proposta = proposta
        self.meta = meta
        self.quantitativo = quantitativo
        self.qualitativo = qualitativo
        self.caracterizacao = caracterizacao
        self.contrapartida = contrapartida

    async def get_relatorio(self, gerenciamento_proposta_id: int) -> RelatorioResponse:
        relatorio = await self.repository.get_relatorio(gerenciamento_proposta_id)
        if not relatorio:
            raise NotFoundError(f'gerenciamento_proposta with {gerenciamento_proposta_id} ID not found')

        return relatorio

    async def create_relatorio(self, relatorio: RelatorioDTO):
        proposta = GerenciamentoPropostaDTO.model_validate(relatorio.model_dump())

        proposta = await self.proposta.create_gerenciamento_proposta(proposta)

        proposta_id = proposta.id

        for meta in relatorio.gerenciamento_metas:
            meta_dto = GerenciamentoMetaDTO.model_validate(meta.model_dump())
            await self.meta.create_gerenciamento_meta(gerenciamento_proposta_id=proposta_id, gerenciamento_meta=meta_dto)

        for quantitativo in relatorio.gerenciamento_quantitativo:
            categorizacoes = quantitativo.gerenciamento_caracterizacao
            quantitativo_dto = GerenciamentoQuantitativoDTO.model_validate(quantitativo.model_dump())

            db_quantitativo = await self.quantitativo.create_gerenciamento_quantitativo(gerenciamento_proposta_id=proposta_id, gerenciamento_quantitativo=quantitativo_dto)

            quantitativo_id = db_quantitativo.id

            for categorizacao in categorizacoes:
                categorizacao_dto = GerenciamentoCaracterizacaoDTO.model_validate(categorizacao.model_dump())
                await self.caracterizacao.create_gerenciamento_caracterizacao(gerenciamento_quantitativo_id=quantitativo_id, gerenciamento_caracterizacao=categorizacao_dto)

        for qualitativo in relatorio.gerenciamento_qualitativo:
            qualitativo_dto = GerenciamentoQualitativoDTO.model_validate(qualitativo)
            await self.qualitativo.create_gerenciamento_qualitativo(gerenciamento_proposta_id=proposta_id, gerenciamento_qualitativo=qualitativo_dto)

        for contrapartida in relatorio.gerenciamento_contrapartida:
            contrapartida_dto = GerenciamentoContrapartidaDTO.model_validate(contrapartida)
            await self.contrapartida.create_gerenciamento_contrapartida(gerenciamento_proposta_id=proposta_id, gerenciamento_contrapartida=contrapartida_dto)

        relatorio = await self.repository.get_relatorio(gerenciamento_proposta_id=proposta_id)

        return relatorio

