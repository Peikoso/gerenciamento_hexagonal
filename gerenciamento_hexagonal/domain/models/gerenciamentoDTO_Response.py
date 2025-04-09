from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from gerenciamento_hexagonal.domain.models.gerenciamento import (
    GerenciamentoComentario,
    GerenciamentoMeta,
    GerenciamentoProposta,
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


class RelatorioResponse(BaseModel):
    proposta_id: int
    trimestre_de_referencia: date
    tipo: TipoGerenciamento = Field(default_factory=TipoGerenciamento.TRIMESTRAL)
    gerenciamento_metas: list[GerenciamentoMetaDTO]

class WrappedRelatorioResponse(BaseModel):
    gerenciamento_proposta: RelatorioResponse