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

    gerenciamentoMetas: Mapped[list['GerenciamentoMetaModel']] = relationship('GerenciamentoMetaModel', back_populates=None, cascade='all, delete-orphan', default_factory=list, lazy='selectin')
    metas_comentarios: Mapped[Optional[list['GerenciamentoComentarioModel']]] = relationship(secondary='gerenciamento_comentario_association', back_populates='gerenciamentoPropostas', cascade='all, delete', default_factory=list, lazy='selectin')


@table_registry.mapped_as_dataclass
class GerenciamentoComentarioModel:
    __tablename__ = 'gerenciamento_comentario'
    __table_args__ = {'sqlite_autoincrement': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True, init=False)
    comentario: Mapped[str] = mapped_column(String(100), nullable=False)
    data_criacao: Mapped[datetime] = mapped_column(DateTime, init=False, nullable=False, server_default=func.now())

    gerenciamentoPropostas: Mapped[list['GerenciamentoPropostaModel']] = relationship(secondary='gerenciamento_comentario_association', back_populates='metas_comentarios', cascade='save-update, merge', default_factory=list)


gerenciamento_comentario_association = Table(
    'gerenciamento_comentario_association',
    table_registry.metadata,
    Column('gerenciamento_id', ForeignKey('gerenciamento_proposta.id', ondelete='CASCADE'), primary_key=True),
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
