import datetime
import uuid
from abc import abstractmethod
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Optional, Set

from Arquivo import Arquivo


class TipoGerenciamento(Enum):
    TRIMESTRAL = 'TRIMESTRAL'
    FINAL = 'FINAL'


class StatusGereciamentoContrapartida(Enum):
    PLANEJADO = 'Planejado'  # padrão
    EM_APROVACAO = 'Em aprovação'
    EM_AJUSTE = 'Em ajuste'
    ENTREGUE = 'Entregue'
    JUSTIFICADA = 'Justificada'
    NAO_ENTREGUE = 'Não entregue'


@dataclass
class GerenciamentoComentario:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    comentario: str
    data_cricao: datetime.datetime = field(default_factory=datetime.datetime.now)
    gerenciamentoproposta: Set['GerenciamentoProposta'] = field(default_factory=set)
    gerenciamentoquantitativo: Set['GerenciamentoQuantitativo'] = field(default_factory=set)
    gerenciamentoqualitativos: Set['GerenciamentoQualitativo'] = field(default_factory=set)

    # relação Many to Many
    def adicionar_gerenciamentoproposta(self, proposta: 'GerenciamentoProposta'):
        self.gerenciamentoproposta.add(proposta)
        proposta.metas_comentarios.add(self)

    def adicionar_gerenciamentoquantitativo(self, quantitativo: 'GerenciamentoQuantitativo'):
        self.gerenciamentoquantitativo.add(quantitativo)
        quantitativo.comentarios.add(self)

    def adicionar_gerenciamentoqualitativos(self, qualitativo: 'GerenciamentoQualitativo'):
        self.gerenciamentoqualitativos.add(qualitativo)
        qualitativo.comentarios.add(self)


@dataclass
class GerenciamentoProposta:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    proposta: any
    criado_em: datetime.datetime = field(default_factory=datetime.datetime.now)
    trimestre_de_referencia: date
    tipo: TipoGerenciamento
    metas_comentarios: Set[GerenciamentoComentario] = field(default_factory=set)  # relação Many to Many

    def adicionar_comentario(self, comentario: GerenciamentoComentario):
        self.metas_comentarios.add(comentario)
        comentario.gerenciamentoproposta.add(self)


@dataclass
class GerenciamentoMeta:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    gerenciamento_proposta: GerenciamentoProposta
    ordem: Optional[int] = None
    alcancado: int


@dataclass
class GerenciamentoQuantitativo:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    gerenciamento_proposta: GerenciamentoProposta
    educacao_financeira_impactados: int
    educacao_financeira_alcancados: int
    geracao_renda_postos_trabalho_gerados: int
    alcance_marca_pessoas_alcancadas_publicacao_digitais: int
    pessoas_alcancadas: int
    pessoas_impactadas: int
    comentarios: Set[GerenciamentoComentario] = field(default_factory=set)  # relação Many to Many

    def adicionar_comentario(self, comentario: GerenciamentoComentario):
        self.comentarios.add(comentario)
        comentario.gerenciamentoquantitativo.add(self)


@dataclass
class GerenciamentoQualitativo:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    gerenciamento_proposta: GerenciamentoProposta
    acoes_realizadas: Optional[str] = None
    acoes_previstas: Optional[str] = None
    visao_proponente: Optional[str] = None
    comentarios: Set[GerenciamentoComentario] = field(default_factory=set)  # relação Many to Many

    def adicionar_comentario(self, comentario: GerenciamentoComentario):
        self.comentarios.add(comentario)
        comentario.gerenciamentoqualitativos.add(self)


# Arquivo de especificações de modelos
class GerenciamentoBeneficiarioCategorizacaoSpec:
    MODEL_NAME = 'GerenciamentoBeneficiarioCategorizacao'
    FIELD_GERENCIAMENTO_BENEFICIARIO = 'gerenciamento_beneficiario'
    FIELD_CATEGORIZACAO = 'categorizacao'
    CONSTRAINT_GERENCIAMENTO_BENEFICIARIO_CATEGORIZACAO_UQ = 'gerenciamento_beneficiario_categorizacao_uq'


@dataclass
class GerenciamentoCaracterizacao:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    gerenciamento_quantitativo: GerenciamentoQualitativo
    quantidade: int
    categorizacoes: any  # Many to Many com categorizacaoBeneficiario, through=GerenciamentoBeneficiarioCategorizacaoSpec.MODEL_NAME


@dataclass
class GerenciamentoBeneficiarioCategorizacao:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    gerenciamento_beneficiario: GerenciamentoCaracterizacao
    categorizacao: any

    # unique Constraint com  (GerenciamentoBeneficiarioCategorizacaoSpec.FIELD_GERENCIAMENTO_BENEFICIARIO,
    # GerenciamentoBeneficiarioCategorizacaoSpec.FIELD_CATEGORIZACAO),
    # name=GerenciamentoBeneficiarioCategorizacaoSpec.CONSTRAINT_GERENCIAMENTO_BENEFICIARIO_CATEGORIZACAO_UQ)


@dataclass
class GerenciamentoMetaArquivo(Arquivo):
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


@dataclass
class GerenciamentoQualitativoArquivo(Arquivo):
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


@dataclass
class GerenciamentoContrapartida:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    gerenciamento_proposta: GerenciamentoProposta
    proposta_contrapartida: any
    quantidade: int
    observacao: str = ''
    data: datetime = field(default_factory=datetime.now)
    status: StatusGereciamentoContrapartida = field(default=StatusGereciamentoContrapartida.PLANEJADO)
    # TODO:falta arquivo


@dataclass
class GerenciamentoContrapartidaArquivo(Arquivo):
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


@dataclass
class GerenciamentoContrapartidaAdmin:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    # campo usuario em um futuro não muito distante
    gerenciamento_contrapartida: GerenciamentoContrapartida
    quantidade: int
    justificativa: str  # O campo é obrigatório
    data: datetime = field(default_factory=datetime.now)
