from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Integer, SmallInteger, String, Table, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

from gerenciamento_hexagonal.domain.models.gerenciamento import TipoGerenciamento

table_registry = registry()


@table_registry.mapped_as_dataclass
class GerenciamentoPropostaModel:
    __tablename__ = 'gerenciamento_proposta'
    __table_args__ = {'sqlite_autoincrement': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True, init=False)
    trimestre_de_referencia: Mapped[Date] = mapped_column(Date, nullable=False)
    tipo: Mapped[TipoGerenciamento] = mapped_column(Enum(TipoGerenciamento), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, init=False, nullable=False, server_default=func.now())
    proposta_id: Mapped[int] = mapped_column(Integer, nullable=False)

    
    metas_comentarios: Mapped[Optional[list['GerenciamentoComentarioModel']]] = relationship(secondary='gerenciamentoProposta_comentario_association', back_populates='comentario_gerenciamentoPropostas', cascade='all, delete', default_factory=list, lazy='selectin')
    
    gerenciamentoMetas: Mapped[list['GerenciamentoMetaModel']] = relationship('GerenciamentoMetaModel', cascade='all, delete-orphan', default_factory=list, lazy='selectin')
    gerenciamentoQuantitativos: Mapped[list['GerenciamentoQuantitativoModel']] = relationship('GerenciamentoQuantitativoModel', cascade='all, delete-orphan', default_factory=list, lazy='selectin')

@table_registry.mapped_as_dataclass
class GerenciamentoComentarioModel:
    __tablename__ = 'gerenciamento_comentario'
    __table_args__ = {'sqlite_autoincrement': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True, init=False)
    comentario: Mapped[str] = mapped_column(String(100), nullable=False)
    data_criacao: Mapped[datetime] = mapped_column(DateTime, init=False, nullable=False, server_default=func.now())

    comentario_gerenciamentoPropostas: Mapped[list['GerenciamentoPropostaModel']] = relationship(secondary='gerenciamentoProposta_comentario_association', back_populates='metas_comentarios', cascade='save-update, merge', default_factory=list)
    comentario_gerenciamentoQuantitativos: Mapped[list['GerenciamentoQuantitativoModel']] = relationship(secondary='gerenciamentoQuantitativo_comentario_association', back_populates='comentarios', cascade='save-update, merge', default_factory=list)


gerenciamentoProposta_comentario_association = Table(
    'gerenciamentoProposta_comentario_association',
    table_registry.metadata,
    Column('gerenciamentoProposta_id', ForeignKey('gerenciamento_proposta.id', ondelete='CASCADE'), primary_key=True),
    Column('comentario_id', ForeignKey('gerenciamento_comentario.id', ondelete='CASCADE'), primary_key=True),
)


@table_registry.mapped_as_dataclass
class GerenciamentoMetaModel:
    __tablename__ = 'gerenciamento_meta'
    __table_args__ = {'sqlite_autoincrement': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True, init=False)
    ordem: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    alcancado: Mapped[int] = mapped_column(Integer, nullable=False)
    
    gerenciamento_proposta_id: Mapped[int] = mapped_column(Integer, ForeignKey('gerenciamento_proposta.id', ondelete='CASCADE'), nullable=False)


@table_registry.mapped_as_dataclass
class GerenciamentoQuantitativoModel:
    __tablename__ = 'gerenciamento_quantitativo'
    __table_args__ = {'sqlite_autoincrement': True}
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True, init=False)
    educacao_financeira_impactados: Mapped[int] = mapped_column(Integer, nullable=False)
    educacao_financeira_alcancados: Mapped[int] = mapped_column(Integer, nullable=False)
    geracao_renda_postos_trabalho_gerados: Mapped[int] = mapped_column(Integer, nullable=False)
    alcance_marca_pessoas_alcancadas_publicacao_digitais: Mapped[int] = mapped_column(Integer, nullable=False)
    pessoas_alcancadas: Mapped[int] = mapped_column(Integer, nullable=False)
    pessoas_impactadas: Mapped[int] = mapped_column(Integer, nullable=False)
    
    gerenciamento_proposta_id: Mapped[int] = mapped_column(Integer, ForeignKey('gerenciamento_proposta.id', ondelete='CASCADE'), nullable=False)
    comentarios: Mapped[Optional[list['GerenciamentoComentarioModel']]] = relationship(secondary='gerenciamentoQuantitativo_comentario_association', back_populates='comentario_gerenciamentoQuantitativos', cascade='all, delete', default_factory=list, lazy='selectin')


gerenciamentoQuantitativo_comentario_association = Table(
    'gerenciamentoQuantitativo_comentario_association',
    table_registry.metadata,
    Column('gerenciamentoQuantitativo_id', ForeignKey('gerenciamento_quantitativo.id', ondelete='CASCADE'), primary_key=True),
    Column('comentario_id', ForeignKey('gerenciamento_comentario.id', ondelete='CASCADE'), primary_key=True),
)

