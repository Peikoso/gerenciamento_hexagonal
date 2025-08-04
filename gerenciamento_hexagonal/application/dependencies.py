from gerenciamento_hexagonal.application.services.relatorio import RelatorioServicesImpl
from gerenciamento_hexagonal.application.services.arquivo.arquivo_service import ArquivoServices
from gerenciamento_hexagonal.application.services.arquivo.gerenciamento_arquivo import GerenciamentoArquivoServices
from gerenciamento_hexagonal.application.services.gerenciamento.caracterizacao import GerenciamentoCaracterizacaoServicesImpl
from gerenciamento_hexagonal.application.services.gerenciamento.comentario import GerenciamentoComentarioServicesImpl
from gerenciamento_hexagonal.application.services.gerenciamento.contrapartida import GerenciamentoContrapartidaServicesImpl
from gerenciamento_hexagonal.application.services.gerenciamento.contrapartida_admin import GerenciamentoContrapartidaAdminServicesImpl
from gerenciamento_hexagonal.application.services.gerenciamento.meta import GerenciamentoMetaServicesImpl
from gerenciamento_hexagonal.application.services.gerenciamento.proposta import GerenciamentoPropostaServicesImpl
from gerenciamento_hexagonal.application.services.gerenciamento.qualitativo import GerenciamentoQualitativoServicesImpl
from gerenciamento_hexagonal.application.services.gerenciamento.quantitativo import GerenciamentoQuantitativoServicesImpl
from gerenciamento_hexagonal.application.services.gerenciamento.verify_gerenciamento import VerifyGerenciamentoServices
from gerenciamento_hexagonal.domain.services.arquivo_service import ValidacaoArquivoService
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.arquivo import GerenciamentoArquivoRepository
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.gerenciamento.caracterizacao import GerenciamentoCaracterizacaoRepository
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.gerenciamento.comentario import GerenciamentoComentarioRepository
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.gerenciamento.contrapartida import GerenciamentoContrapartidaRepository
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.gerenciamento.contrapartida_admin import GerenciamentoContrapartidaAdminRepository
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.gerenciamento.meta import GerenciamentoMetaRepository
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.gerenciamento.proposta import GerenciamentoPropostaRepository
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.gerenciamento.qualitativo import GerenciamentoQualitativoRepository
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.gerenciamento.quantitativo import GerenciamentoQuantitativoRepository
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.relatorio import RelatorioRepository
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.verify_gerenciamento import VerifyGerenciamentoRepository


def get_gerenciamento_proposta_service() -> GerenciamentoPropostaServicesImpl:
    gerenciamento_comentario_repository = GerenciamentoComentarioRepository()
    gerenciamento_proposta_repository = GerenciamentoPropostaRepository(gerenciamento_comentario_repository)
    return GerenciamentoPropostaServicesImpl(gerenciamento_proposta_repository)


def get_gerenciamento_comentario_service() -> GerenciamentoComentarioServicesImpl:
    gerenciamento_comentario_repository = GerenciamentoComentarioRepository()
    return GerenciamentoComentarioServicesImpl(gerenciamento_comentario_repository)


def get_gerenciamento_meta_service() -> GerenciamentoMetaServicesImpl:
    verify = VerifyGerenciamentoServices(VerifyGerenciamentoRepository())
    gerenciamento_meta_repository = GerenciamentoMetaRepository()
    return GerenciamentoMetaServicesImpl(gerenciamento_meta_repository, verify)


def get_gerenciamento_quantitativo_service() -> GerenciamentoQuantitativoServicesImpl:
    verify = VerifyGerenciamentoServices(VerifyGerenciamentoRepository())
    gerenciamento_comentario_repository = GerenciamentoComentarioRepository()
    gerenciamento_quantitativo_repository = GerenciamentoQuantitativoRepository(gerenciamento_comentario_repository)
    return GerenciamentoQuantitativoServicesImpl(gerenciamento_quantitativo_repository, verify)


def get_gerenciamento_qualitativo_service() -> GerenciamentoQualitativoServicesImpl:
    verify = VerifyGerenciamentoServices(VerifyGerenciamentoRepository())
    gerenciamento_comentario_repository = GerenciamentoComentarioRepository()
    gerenciamento_qualitativo_repository = GerenciamentoQualitativoRepository(gerenciamento_comentario_repository)
    return GerenciamentoQualitativoServicesImpl(gerenciamento_qualitativo_repository, verify)


def get_gerenciamento_caracterizacao_service() -> GerenciamentoCaracterizacaoServicesImpl:
    verify = VerifyGerenciamentoServices(VerifyGerenciamentoRepository())
    gerenciamento_caracterizacao_repository = GerenciamentoCaracterizacaoRepository()
    return GerenciamentoCaracterizacaoServicesImpl(gerenciamento_caracterizacao_repository, verify)


def get_gerenciamento_contrapartida_service() -> GerenciamentoContrapartidaServicesImpl:
    verify = VerifyGerenciamentoServices(VerifyGerenciamentoRepository())
    gerenciamento_contrapartida_repository = GerenciamentoContrapartidaRepository()
    return GerenciamentoContrapartidaServicesImpl(gerenciamento_contrapartida_repository, verify)


def get_gerenciamento_contrapartida_admin_service() -> GerenciamentoContrapartidaAdminServicesImpl:
    gerenciamento_contrapartida_service = VerifyGerenciamentoServices()
    gerenciamento_contrapartida_admin_repository = GerenciamentoContrapartidaAdminRepository()
    return GerenciamentoContrapartidaAdminServicesImpl(gerenciamento_contrapartida_admin_repository, gerenciamento_contrapartida_service)


def get_arquivo_service() -> GerenciamentoArquivoServices:
    verify = VerifyGerenciamentoServices(VerifyGerenciamentoRepository())
    gerenciamento_meta_repository = GerenciamentoArquivoRepository()
    service_arquivo = ArquivoServices()
    return GerenciamentoArquivoServices(repository=gerenciamento_meta_repository, service_arquivo=service_arquivo, verify=verify)


def get_validacao_arquivo_service() -> ValidacaoArquivoService:
    return ValidacaoArquivoService()


def get_relatorio_service() -> RelatorioServicesImpl:
    proposta = get_gerenciamento_proposta_service()
    meta = get_gerenciamento_meta_service()
    quantitativo = get_gerenciamento_quantitativo_service()
    qualitativo = get_gerenciamento_qualitativo_service()
    caracterizacao = get_gerenciamento_caracterizacao_service()
    contrapartida = get_gerenciamento_contrapartida_service()
    relatorio_repository = RelatorioRepository()
    return RelatorioServicesImpl(repository_relatorio=relatorio_repository, proposta=proposta, meta=meta, quantitativo=quantitativo, qualitativo=qualitativo, caracterizacao=caracterizacao, contrapartida=contrapartida)
