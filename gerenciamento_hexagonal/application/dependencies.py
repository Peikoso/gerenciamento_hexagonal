from gerenciamento_hexagonal.application.relatorio import RelatorioServices
from gerenciamento_hexagonal.application.services.arquivo.arquivo_service import ArquivoServices
from gerenciamento_hexagonal.application.services.arquivo.gerenciamento_arquivo import GerenciamentoArquivoServices
from gerenciamento_hexagonal.application.services.gerenciamento.caracterizacao import GerenciamentoCaracterizacaoServices
from gerenciamento_hexagonal.application.services.gerenciamento.comentario import GerenciamentoComentarioServices
from gerenciamento_hexagonal.application.services.gerenciamento.contrapartida import GerenciamentoContrapartidaServices
from gerenciamento_hexagonal.application.services.gerenciamento.contrapartida_admin import GerenciamentoContrapartidaAdminServices
from gerenciamento_hexagonal.application.services.gerenciamento.meta import GerenciamentoMetaServices
from gerenciamento_hexagonal.application.services.gerenciamento.proposta import GerenciamentoPropostaServices
from gerenciamento_hexagonal.application.services.gerenciamento.qualitativo import GerenciamentoQualitativoServices
from gerenciamento_hexagonal.application.services.gerenciamento.quantitativo import GerenciamentoQuantitativoServices
from gerenciamento_hexagonal.application.services.gerenciamento.verify_gerenciamento import VerifyGerenciamentoServices
from gerenciamento_hexagonal.domain.services.arquivo_service import ValidacaoArquivoService
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.arquivo import GerenciamentoArquivoRepository
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.verify_gerenciamento import VerifyGerenciamentoRepository
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy_repository import GerenciamentoCaracterizacaoRepository, GerenciamentoComentarioRepository, GerenciamentoContrapartidaAdminRepository, GerenciamentoContrapartidaRepository, GerenciamentoMetaRepository, GerenciamentoPropostaRepository, GerenciamentoQualitativoRepository, GerenciamentoQuantitativoRepository, RelatorioRepository


def get_gerenciamento_proposta_service() -> GerenciamentoPropostaServices:
    gerenciamento_comentario_repository = GerenciamentoComentarioRepository()
    gerenciamento_proposta_repository = GerenciamentoPropostaRepository(gerenciamento_comentario_repository)
    return GerenciamentoPropostaServices(gerenciamento_proposta_repository)


def get_gerenciamento_comentario_service() -> GerenciamentoComentarioServices:
    gerenciamento_comentario_repository = GerenciamentoComentarioRepository()
    return GerenciamentoComentarioServices(gerenciamento_comentario_repository)


def get_gerenciamento_meta_service() -> GerenciamentoMetaServices:
    verify = VerifyGerenciamentoServices(VerifyGerenciamentoRepository())
    gerenciamento_meta_repository = GerenciamentoMetaRepository()
    return GerenciamentoMetaServices(gerenciamento_meta_repository, verify)


def get_gerenciamento_quantitativo_service() -> GerenciamentoQuantitativoServices:
    verify = VerifyGerenciamentoServices(VerifyGerenciamentoRepository())
    gerenciamento_comentario_repository = GerenciamentoComentarioRepository()
    gerenciamento_quantitativo_repository = GerenciamentoQuantitativoRepository(gerenciamento_comentario_repository)
    return GerenciamentoQuantitativoServices(gerenciamento_quantitativo_repository, verify)


def get_gerenciamento_qualitativo_service() -> GerenciamentoQualitativoServices:
    verify = VerifyGerenciamentoServices(VerifyGerenciamentoRepository())
    gerenciamento_comentario_repository = GerenciamentoComentarioRepository()
    gerenciamento_qualitativo_repository = GerenciamentoQualitativoRepository(gerenciamento_comentario_repository)
    return GerenciamentoQualitativoServices(gerenciamento_qualitativo_repository, verify)


def get_gerenciamento_caracterizacao_service() -> GerenciamentoCaracterizacaoServices:
    verify = VerifyGerenciamentoServices(VerifyGerenciamentoRepository())
    gerenciamento_caracterizacao_repository = GerenciamentoCaracterizacaoRepository()
    return GerenciamentoCaracterizacaoServices(gerenciamento_caracterizacao_repository, verify)


def get_gerenciamento_contrapartida_service() -> GerenciamentoContrapartidaServices:
    verify = VerifyGerenciamentoServices(VerifyGerenciamentoRepository())
    gerenciamento_contrapartida_repository = GerenciamentoContrapartidaRepository()
    return GerenciamentoContrapartidaServices(gerenciamento_contrapartida_repository, verify)


def get_gerenciamento_contrapartida_admin_service() -> GerenciamentoContrapartidaAdminServices:
    gerenciamento_contrapartida_service = VerifyGerenciamentoServices()
    gerenciamento_contrapartida_admin_repository = GerenciamentoContrapartidaAdminRepository()
    return GerenciamentoContrapartidaAdminServices(gerenciamento_contrapartida_admin_repository, gerenciamento_contrapartida_service)


def get_arquivo_service() -> GerenciamentoArquivoServices:
    verify = VerifyGerenciamentoServices(VerifyGerenciamentoRepository())
    gerenciamento_meta_repository = GerenciamentoArquivoRepository()
    service_arquivo = ArquivoServices()
    return GerenciamentoArquivoServices(repository=gerenciamento_meta_repository, service_arquivo=service_arquivo, verify=verify)


def get_validacao_arquivo_service() -> ValidacaoArquivoService:
    return ValidacaoArquivoService()


def get_relatorio_service() -> RelatorioServices:
    proposta = get_gerenciamento_proposta_service()
    meta = get_gerenciamento_meta_service()
    quantitativo = get_gerenciamento_quantitativo_service()
    qualitativo = get_gerenciamento_qualitativo_service()
    caracterizacao = get_gerenciamento_caracterizacao_service()
    contrapartida = get_gerenciamento_contrapartida_service()
    relatorio_repository = RelatorioRepository()
    return RelatorioServices(repository_relatorio=relatorio_repository, proposta=proposta, meta=meta, quantitativo=quantitativo, qualitativo=qualitativo, caracterizacao=caracterizacao, contrapartida=contrapartida)
