from datetime import date
from typing import Annotated, Optional

from pydantic import BaseModel, Field

from gerenciamento_hexagonal.domain.models.enums_specs import StatusGereciamentoContrapartida
from gerenciamento_hexagonal.domain.models.gerenciamento import (
    TipoGerenciamento,
)

PositiveInt = Annotated[int, Field(gt=0)]


class GerenciamentoPropostaDTO(BaseModel):
    proposta_id: int
    trimestre_de_referencia: date
    tipo: TipoGerenciamento = Field(default_factory=TipoGerenciamento.TRIMESTRAL)


class GerenciamentoComentarioDTO(BaseModel):
    comentario: str


class GerenciamentoMetaDTO(BaseModel):
    alcancado: int
    ordem: Optional[int] = None


class GerenciamentoQuantitativoDTO(BaseModel):
    educacao_financeira_impactados: int
    educacao_financeira_alcancados: int
    geracao_renda_postos_trabalho_gerados: int
    alcance_marca_pessoas_alcancadas_publicacao_digitais: int
    pessoas_alcancadas: int
    pessoas_impactadas: int


class GerenciamentoQualitativoDTO(BaseModel):
    acoes_realizadas: Optional[str] = None
    acoes_previstas: Optional[str] = None
    visao_proponente: Optional[str] = None


class GerenciamentoCaracterizacaoDTO(BaseModel):
    quantidade: int = Field(..., gt=0)
    categorizacoes_ids: list[PositiveInt]


class GerenciamentoContrapartidaDTO(BaseModel):
    proposta_contrapartida_id: int
    quantidade: int
    observacao: str = Field(..., max_length=300)
    data: date
    status: StatusGereciamentoContrapartida = Field(default_factory=StatusGereciamentoContrapartida.EM_APROVACAO)


class GerenciamentoContrapartidaAdminDTO(BaseModel):
    quantidade: int
    justificativa: str = Field(..., max_length=150)
    data: date


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
    gerenciamento_caracterizacao: list[GerenciamentoCaracterizacaoRelatorioResponse]


class GerenciamentoContrapartidaRelatorioResponse(BaseModel):
    id: int
    proposta_contrapartida_id: int
    quantidade: int
    observacao: str
    data: date
    status: StatusGereciamentoContrapartida


class RelatorioResponse(BaseModel):
    proposta_id: int
    trimestre_de_referencia: date
    tipo: TipoGerenciamento
    gerenciamento_metas: list[GerenciamentoMetaRelatorioResponse]
    gerenciamento_qualitativo: list[GerenciamentoQualitativoRelatorioResponse]
    gerenciamento_quantitativo: list[GerenciamentoQuantitativoRelatorioResponse]
    gerenciamento_contrapartida: list[GerenciamentoContrapartidaRelatorioResponse]


class WrappedRelatorioResponse(BaseModel):
    gerenciamento_proposta: RelatorioResponse
