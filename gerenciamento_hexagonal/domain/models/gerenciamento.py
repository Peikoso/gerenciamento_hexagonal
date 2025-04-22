from datetime import date, datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TipoGerenciamento(str, Enum):
    TRIMESTRAL = 'TRIMESTRAL'
    FINAL = 'FINAL'


class StatusGereciamentoContrapartida(str, Enum):
    PLANEJADO = 'Planejado'  # padrão
    EM_APROVACAO = 'Em aprovação'
    EM_AJUSTE = 'Em ajuste'
    ENTREGUE = 'Entregue'
    JUSTIFICADA = 'Justificada'
    NAO_ENTREGUE = 'Não entregue'


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
    metas_comentarios: list[GerenciamentoComentario] = Field(default_factory=list)  # relação Many to Many


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
    comentarios: list[GerenciamentoComentario] = Field(default_factory=list)  # relação Many to Many


class GerenciamentoQualitativo(BaseModel):
    acoes_realizadas: Optional[str] = None #500
    acoes_previstas: Optional[str] = None
    visao_proponente: Optional[str] = None
    gerenciamento_proposta_id: int
    id: Optional[int] = None
    comentarios: list[GerenciamentoComentario] = Field(default_factory=list)  # relação Many to Many


"""
# Arquivo de especificações de modelos
class GerenciamentoBeneficiarioCategorizacaoSpec:
    MODEL_NAME = 'GerenciamentoBeneficiarioCategorizacao'
    Field_GERENCIAMENTO_BENEFICIARIO = 'gerenciamento_beneficiario'
    Field_CATEGORIZACAO = 'categorizacao'
    CONSTRAINT_GERENCIAMENTO_BENEFICIARIO_CATEGORIZACAO_UQ = 'gerenciamento_beneficiario_categorizacao_uq'


class GerenciamentoCaracterizacao(BaseModel):
    gerenciamento_quantitativo: GerenciamentoQualitativo
    quantidade: int
    categorizacoes: str  # Many to Many com categorizacaoBeneficiario, through=GerenciamentoBeneficiarioCategorizacaoSpec.MODEL_NAME
    id: uuid.UUID = Field(default_factory=uuid.uuid4)


class GerenciamentoBeneficiarioCategorizacao(BaseModel):
    gerenciamento_beneficiario: GerenciamentoCaracterizacao
    categorizacao: str
    id: uuid.UUID = Field(default_factory=uuid.uuid4)

    # unique Constraint com  (GerenciamentoBeneficiarioCategorizacaoSpec.Field_GERENCIAMENTO_BENEFICIARIO,
    # GerenciamentoBeneficiarioCategorizacaoSpec.Field_CATEGORIZACAO),
    # name=GerenciamentoBeneficiarioCategorizacaoSpec.CONSTRAINT_GERENCIAMENTO_BENEFICIARIO_CATEGORIZACAO_UQ)


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


class GerenciamentoContrapartida(BaseModel):
    gerenciamento_proposta: GerenciamentoProposta
    proposta_contrapartida: str
    quantidade: int
    observacao: str = ''
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    data: datetime.datetime = Field(default_factory=datetime.datetime.now)
    status: StatusGereciamentoContrapartida = Field(default=StatusGereciamentoContrapartida.PLANEJADO)
    # TODO:falta arquivo


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


class GerenciamentoContrapartidaAdmin(BaseModel):
    # campo usuario em um futuro não muito distante
    gerenciamento_contrapartida: GerenciamentoContrapartida
    quantidade: int
    justificativa: str  # O campo é obrigatório
    data: datetime.date = Field(default_factory=datetime.datetime.now)
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
"""
