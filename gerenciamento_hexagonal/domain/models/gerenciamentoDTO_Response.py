from datetime import date

from pydantic import BaseModel, Field

from gerenciamento_hexagonal.domain.models.gerenciamento import (
    GerenciamentoProposta,
    TipoGerenciamento,
)


class GerenciamentoComentarioDTO(BaseModel):
    comentario: str


class GerenciamentoPropostaDTO(BaseModel):
    proposta_id: int
    trimestre_de_referencia: date
    tipo: TipoGerenciamento = Field(default_factory=TipoGerenciamento.TRIMESTRAL)


class GerenciamentoPropostaListResponse(BaseModel):
    Gerenciamento_Propostas: list[GerenciamentoProposta]
