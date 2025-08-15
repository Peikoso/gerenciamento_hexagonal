from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoCaracterizacaoRelatorioResponse, GerenciamentoContrapartidaRelatorioResponse, GerenciamentoMetaRelatorioResponse, GerenciamentoQualitativoRelatorioResponse, GerenciamentoQuantitativoRelatorioResponse, RelatorioResponse
from gerenciamento_hexagonal.infrastructure.database.sqlalchemyConfig import get_session
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.models.gerenciamento_orm import GerenciamentoPropostaModel
from sqlalchemy import select


class RelatorioRepository:
    async def get_relatorio(self, gerenciamento_proposta_id: int) -> RelatorioResponse:
        async with get_session() as session:
            relatorio = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id == gerenciamento_proposta_id))

            if not relatorio:
                return None

            gerenciamento_metas = [GerenciamentoMetaRelatorioResponse(id=gerenciamento_meta.id, ordem=gerenciamento_meta.ordem, alcancado=gerenciamento_meta.alcancado, arquivos_ids=[arquivo.arquivo_id for arquivo in gerenciamento_meta.arquivos]) for gerenciamento_meta in relatorio.gerenciamento_metas]

            gerenciamento_qualitativos = [
                GerenciamentoQualitativoRelatorioResponse(id=gerenciamento_qualitativo.id, acoes_previstas=gerenciamento_qualitativo.acoes_previstas, acoes_realizadas=gerenciamento_qualitativo.acoes_realizadas, visao_proponente=gerenciamento_qualitativo.visao_proponente, arquivos_ids=[arquivo.arquivo_id for arquivo in gerenciamento_qualitativo.arquivos])
                for gerenciamento_qualitativo in relatorio.gerenciamento_qualitativo
            ]

            gerenciamento_caracterizacoes = [
                GerenciamentoCaracterizacaoRelatorioResponse(id=gerenciamento_caracterizacao.id, quantidade=gerenciamento_caracterizacao.quantidade, categorizacoes_ids=gerenciamento_caracterizacao.categorizacoes_ids) for gerenciamento_quantitativo in relatorio.gerenciamento_quantitativo for gerenciamento_caracterizacao in gerenciamento_quantitativo.gerenciamento_caracterizacao
            ]

            gerenciamento_quantitativos = [
                GerenciamentoQuantitativoRelatorioResponse(
                    id=gerenciamento_quantitativo.id,
                    educacao_financeira_alcancados=gerenciamento_quantitativo.educacao_financeira_alcancados,
                    educacao_financeira_impactados=gerenciamento_quantitativo.educacao_financeira_impactados,
                    geracao_renda_postos_trabalho_gerados=gerenciamento_quantitativo.geracao_renda_postos_trabalho_gerados,
                    alcance_marca_pessoas_alcancadas_publicacao_digitais=gerenciamento_quantitativo.alcance_marca_pessoas_alcancadas_publicacao_digitais,
                    pessoas_alcancadas=gerenciamento_quantitativo.pessoas_alcancadas,
                    pessoas_impactadas=gerenciamento_quantitativo.pessoas_impactadas,
                    gerenciamento_caracterizacao=gerenciamento_caracterizacoes,
                )
                for gerenciamento_quantitativo in relatorio.gerenciamento_quantitativo
            ]

            gerenciamento_contrapartidas = [
                GerenciamentoContrapartidaRelatorioResponse(
                    id=gerenciamento_contrapartida.id,
                    proposta_contrapartida_id=gerenciamento_contrapartida.proposta_contrapartida_id,
                    quantidade=gerenciamento_contrapartida.quantidade,
                    observacao=gerenciamento_contrapartida.observacao,
                    data=gerenciamento_contrapartida.data,
                    status=gerenciamento_contrapartida.status,
                    arquivos_ids=[arquivo.arquivo_id for arquivo in gerenciamento_contrapartida.arquivos],
                )
                for gerenciamento_contrapartida in relatorio.gerenciamento_contrapartida
            ]

        return RelatorioResponse(id=relatorio.id, proposta_id=relatorio.proposta_id, trimestre_de_referencia=relatorio.trimestre_de_referencia, tipo=relatorio.tipo, gerenciamento_metas=gerenciamento_metas, gerenciamento_qualitativo=gerenciamento_qualitativos, gerenciamento_quantitativo=gerenciamento_quantitativos, gerenciamento_contrapartida=gerenciamento_contrapartidas)
