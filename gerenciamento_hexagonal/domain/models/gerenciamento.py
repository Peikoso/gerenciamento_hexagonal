from datetime import date, datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field

from gerenciamento_hexagonal.domain.models.enums_specs import StatusGereciamentoContrapartida, TipoGerenciamento


class GerenciamentoComentario(BaseModel):
    comentario: str
    id: Optional[int] = None
    data_cricao: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class GerenciamentoProposta(BaseModel):
    proposta_id: int
    trimestre_de_referencia: date
    tipo: TipoGerenciamento = Field(default_factory=TipoGerenciamento.TRIMESTRAL)
    id: Optional[int] = None
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metas_comentarios: list[GerenciamentoComentario] = Field(default_factory=list)


class GerenciamentoMeta(BaseModel):
    alcancado: int
    gerenciamento_proposta_id: Optional[int] = None
    ordem: Optional[int] = None
    id: Optional[int] = None


class GerenciamentoQuantitativo(BaseModel):
    educacao_financeira_impactados: int
    educacao_financeira_alcancados: int
    geracao_renda_postos_trabalho_gerados: int
    alcance_marca_pessoas_alcancadas_publicacao_digitais: int
    pessoas_alcancadas: int
    pessoas_impactadas: int
    gerenciamento_proposta_id: Optional[int] = None
    id: Optional[int] = None
    comentarios: list[GerenciamentoComentario] = Field(default_factory=list)


class GerenciamentoQualitativo(BaseModel):
    acoes_realizadas: Optional[str] = None
    acoes_previstas: Optional[str] = None
    visao_proponente: Optional[str] = None
    gerenciamento_proposta_id: Optional[int] = None
    id: Optional[int] = None
    comentarios: list[GerenciamentoComentario] = Field(default_factory=list)


class GerenciamentoCaracterizacao(BaseModel):
    quantidade: int
    categorizacoes_ids: list[int]
    gerenciamento_quantitativo_id: Optional[int] = None
    id: Optional[int] = None


class GerenciamentoBeneficiarioCategorizacao(BaseModel):
    gerenciamento_id: int
    categorizacoes_ids: list[int]


class GerenciamentoContrapartida(BaseModel):
    proposta_contrapartida_id: int
    quantidade: int
    observacao: str
    data: date
    status: StatusGereciamentoContrapartida
    gerenciamento_proposta_id: Optional[int] = None
    id: Optional[int] = None


class GerenciamentoContrapartidaAdmin(BaseModel):
    quantidade: int
    justificativa: str
    data: date
    gerenciamento_contrapartida_id: Optional[int] = None
    id: Optional[int] = None


"""
class GerenciamentoMetaArquivo(Arquivo, BaseModel):
    gerenciamento_meta: GerenciamentoMeta

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def _get_id(self):
        return self.id

    @abstractmethod
    def _get_rel_id(self):
        return self.gerenciamento_meta.id

    @abstractmethod
    def _get_arquivo(self):
        pass


class GerenciamentoQualitativoArquivo(Arquivo, BaseModel):
    gerenciamento_qualitativo: GerenciamentoQualitativo

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def _get_id(self):
        return self.id

    @abstractmethod
    def _get_rel_id(self):
        return self.gerenciamento_qualitativo.id

    @abstractmethod
    def _get_arquivo(self):
        pass




class GerenciamentoContrapartidaArquivo(Arquivo, BaseModel):
    gerenciamento_contrapartida: GerenciamentoContrapartida

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def _get_id(self):
        return self.id

    @abstractmethod
    def _get_rel_id(self):
        return self.gerenciamento_contrapartida.id

    @abstractmethod
    def _get_arquivo(self):
        pass


"""
