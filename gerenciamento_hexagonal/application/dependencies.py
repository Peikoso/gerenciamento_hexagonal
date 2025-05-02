from gerenciamento_hexagonal.application.services import GerenciamentoCaracterizacaoServices, GerenciamentoComentarioServices, GerenciamentoMetaServices, GerenciamentoPropostaServices, GerenciamentoQualitativoServices, GerenciamentoQuantitativoServices
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy_repository import GerenciamentoCaracterizacaoRepository, GerenciamentoComentarioRepository, GerenciamentoMetaRepository, GerenciamentoPropostaRepository, GerenciamentoQualitativoRepository, GerenciamentoQuantitativoRepository


def get_gerenciamento_proposta__service() -> GerenciamentoPropostaServices:
    gerenciamento_comentario_repository = GerenciamentoComentarioRepository()
    gerenciamento_proposta_repository = GerenciamentoPropostaRepository(gerenciamento_comentario_repository)
    return GerenciamentoPropostaServices(gerenciamento_proposta_repository)


def get_gerenciamento_comentario__service() -> GerenciamentoComentarioServices:
    gerenciamento_comentario_repository = GerenciamentoComentarioRepository()
    return GerenciamentoComentarioServices(gerenciamento_comentario_repository)


def get_gerenciamento_meta__service() -> GerenciamentoMetaServices:
    gerenciamento_meta_repository = GerenciamentoMetaRepository()
    return GerenciamentoMetaServices(gerenciamento_meta_repository)


def get_gerenciamento_quantitativo__service() -> GerenciamentoQuantitativoServices:
    gerenciamento_proposta__service = get_gerenciamento_proposta__service()
    gerenciamento_comentario_repository = GerenciamentoComentarioRepository()
    gerenciamento_quantitativo_repository = GerenciamentoQuantitativoRepository(gerenciamento_comentario_repository)
    return GerenciamentoQuantitativoServices(gerenciamento_quantitativo_repository, gerenciamento_proposta__service)


def get_gerenciamento_qualitativo__service() -> GerenciamentoQualitativoServices:
    gerenciamento_comentario_repository = GerenciamentoComentarioRepository()
    gerenciamento_qualitativo_repository = GerenciamentoQualitativoRepository(gerenciamento_comentario_repository)
    return GerenciamentoQualitativoServices(gerenciamento_qualitativo_repository)


def get_gerenciamento_caracterizacao_services() -> GerenciamentoCaracterizacaoServices:
    gerenciamento_quantitativo__service = get_gerenciamento_quantitativo__service()
    gerenciamento_caracterizacao_repository = GerenciamentoCaracterizacaoRepository()
    return GerenciamentoCaracterizacaoServices(gerenciamento_caracterizacao_repository, gerenciamento_quantitativo__service)
