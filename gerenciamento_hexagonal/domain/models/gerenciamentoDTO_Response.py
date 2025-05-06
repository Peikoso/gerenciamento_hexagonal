from datetime import date
from typing import Annotated, Optional

from pydantic import BaseModel, Field

from gerenciamento_hexagonal.domain.models.gerenciamento import (
    GerenciamentoComentario,
    GerenciamentoMeta,
    GerenciamentoProposta,
    GerenciamentoQuantitativo,
    TipoGerenciamento,
)

PositiveInt = Annotated[int, Field(gt=0)]


class GerenciamentoPropostaDTO(BaseModel):
    proposta_id: int
    trimestre_de_referencia: date
    tipo: TipoGerenciamento = Field(default_factory=TipoGerenciamento.TRIMESTRAL)


class GerenciamentoPropostaListResponse(BaseModel):
    Gerenciamento_Propostas: list[GerenciamentoProposta]


class GerenciamentoComentarioDTO(BaseModel):
    comentario: str


class GerenciamentoComentarioListResponse(BaseModel):
    Gerenciamento_Comentarios: list[GerenciamentoComentario]


class GerenciamentoMetaDTO(BaseModel):
    alcancado: int
    ordem: Optional[int] = None


class GerenciamentoMetaListResponse(BaseModel):
    Gerenciamento_Metas: list[GerenciamentoMeta]


class GerenciamentoQuantitativoDTO(BaseModel):
    educacao_financeira_impactados: int
    educacao_financeira_alcancados: int
    geracao_renda_postos_trabalho_gerados: int
    alcance_marca_pessoas_alcancadas_publicacao_digitais: int
    pessoas_alcancadas: int
    pessoas_impactadas: int


class GerenciamentoQuantitativoListResponse(BaseModel):
    Gerenciamento_Quantitativos: list[GerenciamentoQuantitativo]


class GerenciamentoQualitativoDTO(BaseModel):
    acoes_realizadas: Optional[str] = None
    acoes_previstas: Optional[str] = None
    visao_proponente: Optional[str] = None


class GerenciamentoCaracterizacaoDTO(BaseModel):
    quantidade: int = Field(..., gt=0)
    categorizacoes_ids: list[PositiveInt]


class GerenciamentoMetaRelatorioResponse(BaseModel):
    id: int
    alcancado: int
    ordem: Optional[int] = None


class GerenciamentoQualitativoRelatorioResponse(BaseModel):
    id: int
    acoes_realizadas: Optional[str] = None
    acoes_previstas: Optional[str] = None
    visao_proponente: Optional[str] = None


class GerenciamentoCaracterizacaoRelatorioResponse(BaseModel):
    id: int
    quantidade: int = Field(..., gt=0)
    categorizacoes_ids: list[PositiveInt]


class GerenciamentoQuantitativoRelatorioResponse(BaseModel):
    id: int
    educacao_financeira_impactados: int
    educacao_financeira_alcancados: int
    geracao_renda_postos_trabalho_gerados: int
    alcance_marca_pessoas_alcancadas_publicacao_digitais: int
    pessoas_alcancadas: int
    pessoas_impactadas: int
    gerenciamento_caracterizacao: Optional[GerenciamentoCaracterizacaoRelatorioResponse]


class RelatorioResponse(BaseModel):
    proposta_id: int
    trimestre_de_referencia: date
    tipo: TipoGerenciamento
    gerenciamento_metas: list[GerenciamentoMetaRelatorioResponse]
    gerenciamento_qualitativo: Optional[GerenciamentoQualitativoRelatorioResponse]
    gerenciamento_quantitativo: Optional[GerenciamentoQuantitativoRelatorioResponse]


class WrappedRelatorioResponse(BaseModel):
    gerenciamento_proposta: RelatorioResponse
