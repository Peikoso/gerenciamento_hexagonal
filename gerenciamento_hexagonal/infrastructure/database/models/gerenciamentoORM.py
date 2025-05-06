from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Integer, SmallInteger, String, Table, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

from gerenciamento_hexagonal.domain.models.enums_specs import GerenciamentoBeneficiarioCategorizacaoSpec, StatusGereciamentoContrapartida
from gerenciamento_hexagonal.domain.models.gerenciamento import TipoGerenciamento

table_registry = registry()


@table_registry.mapped_as_dataclass
class GerenciamentoPropostaModel:
    __tablename__ = 'gerenciamento_proposta'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True, init=False)
    trimestre_de_referencia: Mapped[Date] = mapped_column(Date, nullable=False)
    tipo: Mapped[TipoGerenciamento] = mapped_column(Enum(TipoGerenciamento), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, init=False, nullable=False, server_default=func.now())
    proposta_id: Mapped[int] = mapped_column(Integer, nullable=False)

    gerenciamento_quantitativo: Mapped['GerenciamentoQuantitativoModel'] = relationship('GerenciamentoQuantitativoModel', back_populates='gerenciamento_proposta', cascade='all, delete-orphan', uselist=False, lazy='selectin', init=False)
    gerenciamento_qualitativo: Mapped['GerenciamentoQualitativoModel'] = relationship('GerenciamentoQualitativoModel', back_populates='gerenciamento_proposta', cascade='all, delete-orphan', uselist=False, lazy='selectin', init=False)
    gerenciamento_metas: Mapped[list['GerenciamentoMetaModel']] = relationship('GerenciamentoMetaModel', back_populates='gerenciamento_proposta', cascade='all, delete-orphan', default_factory=list, lazy='selectin')
    gerenciamento_contrapartida: Mapped[list['GerenciamentoContrapartidaModel']] = relationship('GerenciamentoContrapartidaModel', back_populates='gerenciamento_proposta', cascade='all, delete-orphan', default_factory=list, lazy='selectin')

    metas_comentarios: Mapped[list['GerenciamentoComentarioModel']] = relationship(secondary='gerenciamento_proposta_comentario_association', back_populates='comentario_gerenciamento_propostas', cascade='all, delete', default_factory=list, lazy='selectin')


@table_registry.mapped_as_dataclass
class GerenciamentoComentarioModel:
    __tablename__ = 'gerenciamento_comentario'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True, init=False)
    comentario: Mapped[str] = mapped_column(String(100), nullable=False)
    data_criacao: Mapped[datetime] = mapped_column(DateTime, init=False, nullable=False, server_default=func.now())

    comentario_gerenciamento_propostas: Mapped[list['GerenciamentoPropostaModel']] = relationship(secondary='gerenciamento_proposta_comentario_association', back_populates='metas_comentarios', cascade='save-update, merge', default_factory=list)
    comentario_gerenciamento_quantitativos: Mapped[list['GerenciamentoQuantitativoModel']] = relationship(secondary='gerenciamento_quantitativo_comentario_association', back_populates='comentarios', cascade='save-update, merge', default_factory=list)
    comentario_gerenciamento_qualitativos: Mapped[list['GerenciamentoQualitativoModel']] = relationship(secondary='gerenciamento_qualitativo_comentario_association', back_populates='comentarios', cascade='save-update, merge', default_factory=list)


gerenciamento_proposta_comentario_association = Table(
    'gerenciamento_proposta_comentario_association',
    table_registry.metadata,
    Column('gerenciamentoProposta_id', ForeignKey('gerenciamento_proposta.id', ondelete='CASCADE'), primary_key=True),
    Column('comentario_id', ForeignKey('gerenciamento_comentario.id', ondelete='CASCADE'), primary_key=True),
)


@table_registry.mapped_as_dataclass
class GerenciamentoMetaModel:
    __tablename__ = 'gerenciamento_meta'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True, init=False)
    ordem: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    alcancado: Mapped[int] = mapped_column(Integer, nullable=False)

    gerenciamento_proposta_id: Mapped[int] = mapped_column(Integer, ForeignKey('gerenciamento_proposta.id', ondelete='CASCADE'), nullable=False)
    gerenciamento_proposta: Mapped['GerenciamentoPropostaModel'] = relationship(back_populates='gerenciamento_metas', lazy='selectin', init=False)


@table_registry.mapped_as_dataclass
class GerenciamentoQuantitativoModel:
    __tablename__ = 'gerenciamento_quantitativo'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True, init=False)
    educacao_financeira_impactados: Mapped[int] = mapped_column(Integer, nullable=False)
    educacao_financeira_alcancados: Mapped[int] = mapped_column(Integer, nullable=False)
    geracao_renda_postos_trabalho_gerados: Mapped[int] = mapped_column(Integer, nullable=False)
    alcance_marca_pessoas_alcancadas_publicacao_digitais: Mapped[int] = mapped_column(Integer, nullable=False)
    pessoas_alcancadas: Mapped[int] = mapped_column(Integer, nullable=False)
    pessoas_impactadas: Mapped[int] = mapped_column(Integer, nullable=False)

    gerenciamento_caracterizacao: Mapped['GerenciamentoCaracterizacaoModel'] = relationship('GerenciamentoCaracterizacaoModel', back_populates='gerenciamento_quantitativo', uselist=False, lazy='selectin', init=False)

    gerenciamento_proposta_id: Mapped[int] = mapped_column(Integer, ForeignKey('gerenciamento_proposta.id', ondelete='CASCADE'), nullable=False, unique=True)
    gerenciamento_proposta: Mapped['GerenciamentoPropostaModel'] = relationship('GerenciamentoPropostaModel', back_populates='gerenciamento_quantitativo', lazy='selectin', init=False)

    comentarios: Mapped[list['GerenciamentoComentarioModel']] = relationship(secondary='gerenciamento_quantitativo_comentario_association', back_populates='comentario_gerenciamento_quantitativos', cascade='all, delete', default_factory=list, lazy='selectin')


gerenciamento_quantitativo_comentario_association = Table(
    'gerenciamento_quantitativo_comentario_association',
    table_registry.metadata,
    Column('gerenciamentoQuantitativo_id', ForeignKey('gerenciamento_quantitativo.id', ondelete='CASCADE'), primary_key=True),
    Column('comentario_id', ForeignKey('gerenciamento_comentario.id', ondelete='CASCADE'), primary_key=True),
)


@table_registry.mapped_as_dataclass
class GerenciamentoQualitativoModel:
    __tablename__ = 'gerenciamento_qualitativo'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True, init=False)
    acoes_realizadas: Mapped[str] = mapped_column(String(500))
    acoes_previstas: Mapped[str] = mapped_column(String(500))
    visao_proponente: Mapped[str] = mapped_column(String(500))

    gerenciamento_proposta_id: Mapped[int] = mapped_column(Integer, ForeignKey('gerenciamento_proposta.id', ondelete='CASCADE'), nullable=False, unique=True)
    gerenciamento_proposta: Mapped['GerenciamentoPropostaModel'] = relationship('GerenciamentoPropostaModel', back_populates='gerenciamento_qualitativo', lazy='selectin', init=False)

    comentarios: Mapped[list['GerenciamentoComentarioModel']] = relationship(secondary='gerenciamento_qualitativo_comentario_association', back_populates='comentario_gerenciamento_qualitativos', cascade='all, delete', default_factory=list, lazy='selectin')


gerenciamento_qualitativo_comentario_association = Table('gerenciamento_qualitativo_comentario_association', table_registry.metadata, Column('gerenciamentoQualitativo_id', ForeignKey('gerenciamento_qualitativo.id', ondelete='CASCADE'), primary_key=True), Column('comentario_id', ForeignKey('gerenciamento_comentario.id', ondelete='CASCADE'), primary_key=True))


@table_registry.mapped_as_dataclass
class TipoCategorizacaoBeneficiarioModel:
    __tablename__ = 'tipo_categorizacao_beneficiario'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True, init=False)
    info: Mapped[str] = mapped_column(String(50), nullable=False)
    descricao: Mapped[str] = mapped_column(String(150))


@table_registry.mapped_as_dataclass
class CategorizacaoBeneficiarioModel:
    __tablename__ = 'categorizacao_beneficiario'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True, init=False)
    tipo_categ_beneficiario_id: Mapped[int] = mapped_column(ForeignKey('tipo_categorizacao_beneficiario.id', ondelete='RESTRICT'))
    valor: Mapped[str] = mapped_column(String(64), nullable=False)
    tipo: Mapped[TipoCategorizacaoBeneficiarioModel] = relationship()

    gerenciamentos: Mapped[list['GerenciamentoCaracterizacaoModel']] = relationship(secondary=GerenciamentoBeneficiarioCategorizacaoSpec.MODEL_NAME, back_populates='categorizacoes', default_factory=list, lazy='selectin')

    __table_args__ = (UniqueConstraint('tipo_categ_beneficiario_id', 'valor', name='categorizacao_beneficiario_tipo_valor_uq'),)


@table_registry.mapped_as_dataclass
class GerenciamentoCaracterizacaoModel:
    __tablename__ = 'gerenciamento_caracterizacao'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True, init=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)

    gerenciamento_quantitativo_id: Mapped[int] = mapped_column(Integer, ForeignKey('gerenciamento_quantitativo.id', ondelete='RESTRICT'), nullable=False, unique=True)
    gerenciamento_quantitativo: Mapped['GerenciamentoQuantitativoModel'] = relationship('GerenciamentoQuantitativoModel', back_populates='gerenciamento_caracterizacao', lazy='selectin', init=False)

    categorizacoes: Mapped[list['CategorizacaoBeneficiarioModel']] = relationship(secondary=GerenciamentoBeneficiarioCategorizacaoSpec.MODEL_NAME, back_populates='gerenciamentos', default_factory=list, lazy='selectin')


gerenciamento_beneficiario_categorizacao = Table(
    'gerenciamento_beneficiario_categorizacao',
    table_registry.metadata,
    Column('gerenciamento_beneficiario_id', ForeignKey('gerenciamento_caracterizacao.id', ondelete='CASCADE'), primary_key=True),
    Column('categorizacao_id', ForeignKey('categorizacao_beneficiario.id', ondelete='CASCADE'), primary_key=True),
    UniqueConstraint(GerenciamentoBeneficiarioCategorizacaoSpec.FIELD_GERENCIAMENTO_BENEFICIARIO, GerenciamentoBeneficiarioCategorizacaoSpec.FIELD_CATEGORIZACAO, name=GerenciamentoBeneficiarioCategorizacaoSpec.CONSTRAINT_GERENCIAMENTO_BENEFICIARIO_CATEGORIZACAO_UQ),
)


@table_registry.mapped_as_dataclass
class GerenciamentoContrapartidaModel:
    __tablename__ = 'gerenciamento_contrapartida'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True, init=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    observacao: Mapped[str] = mapped_column(String(300), nullable=False)
    data: Mapped[Date] = mapped_column(Date, nullable=False)
    status: Mapped[StatusGereciamentoContrapartida] = mapped_column(Enum(StatusGereciamentoContrapartida), nullable=False)
    proposta_contrapartida_id: Mapped[int] = mapped_column(Integer, nullable=False)

    gerenciamento_proposta_id: Mapped[int] = mapped_column(Integer, ForeignKey('gerenciamento_proposta.id', ondelete='CASCADE'), nullable=False)
    gerenciamento_proposta: Mapped['GerenciamentoPropostaModel'] = relationship(back_populates='gerenciamento_contrapartida', lazy='selectin', init=False)

    gerenciamento_contrapartida_admin: Mapped[list['GerenciamentoContrapartidaAdminModel']] = relationship('GerenciamentoContrapartidaAdminModel', back_populates='gerenciamento_contrapartida', cascade='all, delete-orphan', default_factory=list, lazy='selectin')


@table_registry.mapped_as_dataclass
class GerenciamentoContrapartidaAdminModel:
    __tablename__ = 'gerenciamento_contrapartida_admin'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True, init=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    justificativa: Mapped[str] = mapped_column(String(150), nullable=False)
    data: Mapped[Date] = mapped_column(Date, nullable=False)

    gerenciamento_contrapartida_id: Mapped[int] = mapped_column(Integer, ForeignKey('gerenciamento_contrapartida.id', ondelete='CASCADE'), nullable=False)
    gerenciamento_contrapartida: Mapped['GerenciamentoContrapartidaModel'] = relationship(back_populates='gerenciamento_contrapartida_admin', lazy='selectin', init=False)
