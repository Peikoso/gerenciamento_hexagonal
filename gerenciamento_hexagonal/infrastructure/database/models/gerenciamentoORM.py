from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, Table, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

from gerenciamento_hexagonal.domain.models.gerenciamento import TipoGerenciamento

table_registry = registry()


@table_registry.mapped_as_dataclass
class GerenciamentoPropostaModel:
    __tablename__ = 'gerenciamento_proposta'

    id: Mapped[int] = mapped_column(init=False, primary_key=True, unique=True, nullable=False, autoincrement=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, init=False, nullable=False, server_default=func.now())
    trimestre_de_referencia: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    tipo: Mapped[TipoGerenciamento] = mapped_column(Enum(TipoGerenciamento), nullable=False)
    proposta_id: Mapped[int] = mapped_column(nullable=False)

    metas_comentarios: Mapped[list['GerenciamentoComentarioModel']] = relationship(secondary='gerenciamento_comentario_association', back_populates='gerenciamentoPropostas', cascade='all, delete', default_factory=list)


@table_registry.mapped_as_dataclass
class GerenciamentoComentarioModel:
    __tablename__ = 'gerenciamento_comentario'

    id: Mapped[int] = mapped_column(init=False, primary_key=True, unique=True, nullable=False, autoincrement=True)
    comentario: Mapped[str] = mapped_column(String(100), nullable=False)
    data_criacao: Mapped[datetime] = mapped_column(DateTime, init=False, nullable=False, server_default=func.now())

    gerenciamentoPropostas: Mapped[list['GerenciamentoPropostaModel']] = relationship(secondary='gerenciamento_comentario_association', back_populates='metas_comentarios', cascade='all, delete', default_factory=list)


gerenciamento_comentario_association = Table(
    'gerenciamento_comentario_association',
    table_registry.metadata,
    Column('gerenciamento_id', ForeignKey('gerenciamento_proposta.id', ondelete='CASCADE'), primary_key=True),
    Column('comentario_id', ForeignKey('gerenciamento_comentario.id', ondelete='CASCADE'), primary_key=True),
)
