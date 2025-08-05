from gerenciamento_hexagonal.application.services.interfaces.relatorio import RelatorioServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoCaracterizacaoDTO, GerenciamentoContrapartidaDTO, GerenciamentoMetaDTO, GerenciamentoPropostaDTO, GerenciamentoQualitativoDTO, GerenciamentoQuantitativoDTO, RelatorioDTO, RelatorioResponse, RelatorioUpdateDTO


class RelatorioServicesImpl(RelatorioServices):
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

    async def update_relatorio(self, relatorio: RelatorioUpdateDTO, gerenciamento_proposta_id: int):
        proposta = GerenciamentoPropostaDTO.model_validate(relatorio.model_dump())

        proposta = await self.proposta.update_gerenciamento_proposta(gerenciamento_proposta_id, proposta)

        proposta_id = proposta.id

        for meta in relatorio.gerenciamento_metas:
            meta_dto = GerenciamentoMetaDTO.model_validate(meta.model_dump())
            await self.meta.update_gerenciamento_meta(gerenciamento_meta_id=meta.id, gerenciamento_meta=meta_dto)

        for quantitativo in relatorio.gerenciamento_quantitativo:
            categorizacoes = quantitativo.gerenciamento_caracterizacao
            quantitativo_dto = GerenciamentoQuantitativoDTO.model_validate(quantitativo.model_dump())

            await self.quantitativo.update_gerenciamento_quantitativo(gerenciamento_quantitativo_id=quantitativo.id, gerenciamento_quantitativo=quantitativo_dto)


            for categorizacao in categorizacoes:
                categorizacao_dto = GerenciamentoCaracterizacaoDTO.model_validate(categorizacao.model_dump())
                await self.caracterizacao.update_gerenciamento_caracterizacao(gerenciamento_caracterizacao_id=categorizacao.id, gerenciamento_caracterizacao=categorizacao_dto)

        for qualitativo in relatorio.gerenciamento_qualitativo:
            qualitativo_dto = GerenciamentoQualitativoDTO.model_validate(qualitativo)
            await self.qualitativo.update_gerenciamento_qualitativo(gerenciamento_qualitativo_id=qualitativo.id, gerenciamento_qualitativo=qualitativo_dto)

        for contrapartida in relatorio.gerenciamento_contrapartida:
            contrapartida_dto = GerenciamentoContrapartidaDTO.model_validate(contrapartida)
            await self.contrapartida.update_gerenciamento_contrapartida(gerenciamento_contrapartida_id=contrapartida.id, gerenciamento_contrapartida=contrapartida_dto)

        relatorio = await self.repository.get_relatorio(gerenciamento_proposta_id=proposta_id)

        return relatorio