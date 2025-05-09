from gerenciamento_hexagonal.application.services.arquivo.arquivo_service import ArquivoServices, ValidacaoArquivoService
from gerenciamento_hexagonal.application.services.arquivo.gerenciamento_arquivo import GerenciamentoArquivoServices
from gerenciamento_hexagonal.application.services.gerenciamento.caracterizacao import GerenciamentoCaracterizacaoServices
from gerenciamento_hexagonal.application.services.gerenciamento.comentario import GerenciamentoComentarioServices
from gerenciamento_hexagonal.application.services.gerenciamento.contrapartida import GerenciamentoContrapartidaServices
from gerenciamento_hexagonal.application.services.gerenciamento.contrapartida_admin import GerenciamentoContrapartidaAdminServices
from gerenciamento_hexagonal.application.services.gerenciamento.meta import GerenciamentoMetaServices
from gerenciamento_hexagonal.application.services.gerenciamento.proposta import GerenciamentoPropostaServices
from gerenciamento_hexagonal.application.services.gerenciamento.qualitativo import GerenciamentoQualitativoServices
from gerenciamento_hexagonal.application.services.gerenciamento.quantitativo import GerenciamentoQuantitativoServices
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.arquivo import GerenciamentoArquivoRepository
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy_repository import GerenciamentoCaracterizacaoRepository, GerenciamentoComentarioRepository, GerenciamentoContrapartidaAdminRepository, GerenciamentoContrapartidaRepository, GerenciamentoMetaRepository, GerenciamentoPropostaRepository, GerenciamentoQualitativoRepository, GerenciamentoQuantitativoRepository


def get_gerenciamento_proposta_service() -> GerenciamentoPropostaServices:
    gerenciamento_comentario_repository = GerenciamentoComentarioRepository()
    gerenciamento_proposta_repository = GerenciamentoPropostaRepository(gerenciamento_comentario_repository)
    return GerenciamentoPropostaServices(gerenciamento_proposta_repository)


def get_gerenciamento_comentario_service() -> GerenciamentoComentarioServices:
    gerenciamento_comentario_repository = GerenciamentoComentarioRepository()
    return GerenciamentoComentarioServices(gerenciamento_comentario_repository)


def get_gerenciamento_meta_service() -> GerenciamentoMetaServices:
    gerenciamento_proposta_service = get_gerenciamento_proposta_service()
    gerenciamento_meta_repository = GerenciamentoMetaRepository()
    return GerenciamentoMetaServices(gerenciamento_meta_repository, gerenciamento_proposta_service)


def get_gerenciamento_quantitativo_service() -> GerenciamentoQuantitativoServices:
    gerenciamento_proposta_service = get_gerenciamento_proposta_service()
    gerenciamento_comentario_repository = GerenciamentoComentarioRepository()
    gerenciamento_quantitativo_repository = GerenciamentoQuantitativoRepository(gerenciamento_comentario_repository)
    return GerenciamentoQuantitativoServices(gerenciamento_quantitativo_repository, gerenciamento_proposta_service)


def get_gerenciamento_qualitativo_service() -> GerenciamentoQualitativoServices:
    gerenciamento_proposta_service = get_gerenciamento_proposta_service()
    gerenciamento_comentario_repository = GerenciamentoComentarioRepository()
    gerenciamento_qualitativo_repository = GerenciamentoQualitativoRepository(gerenciamento_comentario_repository)
    return GerenciamentoQualitativoServices(gerenciamento_qualitativo_repository, gerenciamento_proposta_service)


def get_gerenciamento_caracterizacao_service() -> GerenciamentoCaracterizacaoServices:
    gerenciamento_quantitativo_service = get_gerenciamento_quantitativo_service()
    gerenciamento_caracterizacao_repository = GerenciamentoCaracterizacaoRepository()
    return GerenciamentoCaracterizacaoServices(gerenciamento_caracterizacao_repository, gerenciamento_quantitativo_service)


def get_gerenciamento_contrapartida_service() -> GerenciamentoContrapartidaServices:
    gerenciamento_proposta_service = get_gerenciamento_proposta_service()
    gerenciamento_contrapartida_repository = GerenciamentoContrapartidaRepository()
    return GerenciamentoContrapartidaServices(gerenciamento_contrapartida_repository, gerenciamento_proposta_service)


def get_gerenciamento_contrapartida_admin_service() -> GerenciamentoContrapartidaAdminServices:
    gerenciamento_contrapartida_service = get_gerenciamento_contrapartida_service()
    gerenciamento_contrapartida_admin_repository = GerenciamentoContrapartidaAdminRepository()
    return GerenciamentoContrapartidaAdminServices(gerenciamento_contrapartida_admin_repository, gerenciamento_contrapartida_service)


def get_arquivo_service() -> GerenciamentoArquivoServices:
    gerenciamento_meta_service = get_gerenciamento_meta_service()
    gerenciamento_meta_repository = GerenciamentoArquivoRepository()
    service_meta_arquivo = ArquivoServices()
    return GerenciamentoArquivoServices(repository=gerenciamento_meta_repository, service_meta=gerenciamento_meta_service, service_meta_arquivo=service_meta_arquivo)


def get_validacao_arquivo_service() -> ValidacaoArquivoService:
    return ValidacaoArquivoService()
