from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from gerenciamento_hexagonal.domain.models.gerenciamento import (
    GerenciamentoComentario,
    GerenciamentoMeta,
    GerenciamentoProposta,
    GerenciamentoQuantitativo,
    TipoGerenciamento,
)


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

class RelatorioResponse(BaseModel):
    proposta_id: int
    trimestre_de_referencia: date
    tipo: TipoGerenciamento = Field(default_factory=TipoGerenciamento.TRIMESTRAL)
    gerenciamento_metas: list[GerenciamentoMetaDTO]
    gerenciamento_quantitativos: list[GerenciamentoQuantitativoDTO]

class WrappedRelatorioResponse(BaseModel):
    gerenciamento_proposta: RelatorioResponse