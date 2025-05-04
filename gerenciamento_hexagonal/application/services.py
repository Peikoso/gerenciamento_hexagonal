from typing import List

from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import (
    NotFoundError,
    NotNullViolationError,
    UniqueViolation,
)
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoCaracterizacao, GerenciamentoComentario, GerenciamentoMeta, GerenciamentoProposta, GerenciamentoQualitativo, GerenciamentoQuantitativo
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import (
    GerenciamentoCaracterizacaoDTO,
    GerenciamentoComentarioDTO,
    GerenciamentoMetaDTO,
    GerenciamentoPropostaDTO,
    GerenciamentoQualitativoDTO,
    GerenciamentoQuantitativoDTO,
    RelatorioResponse,
)
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy_repository import GerenciamentoCaracterizacaoRepository, GerenciamentoComentarioRepository, GerenciamentoMetaRepository, GerenciamentoPropostaRepository, GerenciamentoQualitativoRepository, GerenciamentoQuantitativoRepository, RelatorioRepository


class RelatorioServices:
    def __init__(self, repository_relatorio: RelatorioRepository):
        self.repository = repository_relatorio

    async def get_relatorio(self, gerenciamento_proposta_id: int) -> RelatorioResponse:
        relatorio = await self.repository.get_relatorio(gerenciamento_proposta_id)
        if not relatorio:
            raise NotFoundError(f'gerenciamento_proposta with {gerenciamento_proposta_id} ID not found')

        return relatorio


class GerenciamentoPropostaServices:
    def __init__(self, repository_gerenciamento: GerenciamentoPropostaRepository):
        self.repository = repository_gerenciamento

    async def get_gerenciamento_proposta(self) -> List[GerenciamentoProposta]:
        gerenciamento_propostas = await self.repository.get_gerenciamento_proposta()

        return gerenciamento_propostas

    async def get_gerenciamento_proposta_by_id(self, gerenciamento_proposta_id: int):
        gerenciamento_proposta = await self.repository.get_gerenciamento_proposta_by_id(gerenciamento_proposta_id)
        if not gerenciamento_proposta:
            raise NotFoundError(f'gerenciamento_proposta with ID {gerenciamento_proposta_id} not found')

        return gerenciamento_proposta

    async def create_gerenciamento_proposta(self, gerenciamento_proposta: GerenciamentoPropostaDTO) -> GerenciamentoProposta:
        gerenciamento_proposta = GerenciamentoProposta(**gerenciamento_proposta.model_dump())
        gerenciamento_proposta = await self.repository.create_gerenciamento_proposta(gerenciamento_proposta)

        return gerenciamento_proposta

    async def update_gerenciamento_proposta(self, gerenciamento_proposta_id: int, gerenciamento_proposta: GerenciamentoPropostaDTO) -> GerenciamentoProposta:
        await self.get_gerenciamento_proposta_by_id(gerenciamento_proposta_id)

        gerenciamento_proposta = GerenciamentoProposta(**gerenciamento_proposta.model_dump())
        gerenciamento_proposta = await self.repository.update_gerenciamento_proposta(gerenciamento_proposta_id, gerenciamento_proposta)

        return gerenciamento_proposta

    async def delete_gerenciamento_proposta(self, gerenciamento_proposta_id: int):
        await self.get_gerenciamento_proposta_by_id(gerenciamento_proposta_id)

        NotNullViolation = await self.repository.checar_gerenciamento_caracterizacao_exists(gerenciamento_proposta_id)

        if NotNullViolation:
            raise NotNullViolationError('cannot delete a gerenciamento_proposta when there is an associated gerenciamento_caracterizacao')

        await self.repository.delete_gerenciamento_proposta(gerenciamento_proposta_id)

        return {'message': f'gerenciamento_proposta with ID {gerenciamento_proposta_id} deleted'}

    async def create_gerenciamento_proposta_comentario(self, gerenciamento_proposta_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO) -> GerenciamentoProposta:
        await self.get_gerenciamento_proposta_by_id(gerenciamento_proposta_id)

        gerenciamento_comentario = GerenciamentoComentario(**gerenciamento_comentario.model_dump())
        gerenciamento_proposta = await self.repository.create_gerenciamento_proposta_comentario(gerenciamento_proposta_id, gerenciamento_comentario)

        return gerenciamento_proposta


class GerenciamentoComentarioServices:
    def __init__(self, repository_gerenciamento: GerenciamentoComentarioRepository):
        self.repository = repository_gerenciamento

    async def get_gerenciamento_comentario(self) -> list[GerenciamentoComentario]:
        gerenciamento_comentarios = await self.repository.get_gerenciamento_comentario()

        return gerenciamento_comentarios

    async def get_gerenciamento_comentario_by_id(self, gerenciamento_comentario_id: int) -> GerenciamentoComentario:
        gerenciamento_comentario = await self.repository.get_gerenciamento_comentario_by_id(gerenciamento_comentario_id)

        if not gerenciamento_comentario:
            raise NotFoundError(f'gerenciamento_comentario with ID {gerenciamento_comentario_id} not found')

        return gerenciamento_comentario

    async def update_gerenciamento_comentario(self, gerenciamento_comentario_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO) -> GerenciamentoComentario:
        await self.get_gerenciamento_comentario_by_id(gerenciamento_comentario_id)

        gerenciamento_comentario = GerenciamentoComentario(**gerenciamento_comentario.model_dump())
        gerenciamento_comentario = await self.repository.update_gerenciamento_comentario(gerenciamento_comentario_id, gerenciamento_comentario)

        return gerenciamento_comentario

    async def delete_gerenciamento_comentario(self, gerenciamento_comentario_id: int) -> None:
        await self.get_gerenciamento_comentario_by_id(gerenciamento_comentario_id)

        await self.repository.delete_gerenciamento_comentario(gerenciamento_comentario_id)

        return {'message': 'gerenciamento_comentario with ID {gerenciamento_comentario_id} deleted'}


class GerenciamentoMetaServices:
    def __init__(self, repository_gerenciamento: GerenciamentoMetaRepository, service_proposta: GerenciamentoPropostaServices):
        self.repository = repository_gerenciamento
        self.service_proposta = service_proposta

    async def get_gerenciamento_meta(self) -> list[GerenciamentoMeta]:
        gerenciamento_metas = await self.repository.get_gerenciamento_meta()

        return gerenciamento_metas

    async def get_gerenciamento_meta_by_id(self, gerenciamento_meta_id: int) -> GerenciamentoMeta:
        gerenciamento_meta = await self.repository.get_gerenciamento_meta_by_id(gerenciamento_meta_id)
        if not gerenciamento_meta:
            raise NotFoundError(f'gerenciamento_meta with ID {gerenciamento_meta_id} not found')

        return gerenciamento_meta

    async def create_gerenciamento_meta(self, gerenciamento_proposta_id: int, gerenciamento_meta: GerenciamentoMetaDTO) -> GerenciamentoMeta:
        await self.service_proposta.get_gerenciamento_proposta_by_id(gerenciamento_proposta_id)

        gerenciamento_meta = GerenciamentoMeta(**gerenciamento_meta.model_dump())
        gerenciamento_meta = await self.repository.create_gerenciamento_meta(gerenciamento_proposta_id, gerenciamento_meta)

        return gerenciamento_meta

    async def update_gerenciamento_meta(self, gerenciamento_meta_id: int, gerenciamento_meta: GerenciamentoMetaDTO) -> GerenciamentoMeta:
        await self.get_gerenciamento_meta_by_id(gerenciamento_meta_id)

        gerenciamento_meta = GerenciamentoMeta(**gerenciamento_meta.model_dump())
        gerenciamento_meta = await self.repository.update_gerenciamento_meta(gerenciamento_meta_id, gerenciamento_meta)

        return gerenciamento_meta

    async def delete_gerenciamento_meta(self, gerenciamento_meta_id: int) -> bool:
        await self.get_gerenciamento_meta_by_id(gerenciamento_meta_id)

        await self.repository.delete_gerenciamento_meta(gerenciamento_meta_id)

        return {'message': f'gerenciamento_meta with ID {gerenciamento_meta_id} deleted'}


class GerenciamentoQuantitativoServices:
    def __init__(self, repository_gerenciamento: GerenciamentoQuantitativoRepository, service_proposta: GerenciamentoPropostaServices):
        self.repository = repository_gerenciamento
        self.service_proposta = service_proposta

    async def get_gerenciamento_quantitativo(self) -> list[GerenciamentoQuantitativo]:
        gerenciamento_quantitativos = await self.repository.get_gerenciamento_quantitativo()

        return gerenciamento_quantitativos

    async def get_gerenciamento_quantitativo_by_id(self, gerenciamento_quantitativo_id: int) -> GerenciamentoQuantitativo:
        gerenciamento_quantitativo = await self.repository.get_gerenciamento_quantitativo_by_id(gerenciamento_quantitativo_id)

        if not gerenciamento_quantitativo:
            raise NotFoundError(f'gerenciamento_quantitativo with ID: {gerenciamento_quantitativo_id} not found')

        return gerenciamento_quantitativo

    async def create_gerenciamento_quantitativo(self, gerenciamento_proposta_id: int, gerenciamento_quantitativo: GerenciamentoQuantitativoDTO) -> GerenciamentoQuantitativo:
        await self.service_proposta.get_gerenciamento_proposta_by_id(gerenciamento_proposta_id)

        UniqueViolationCheck = await self.repository.checar_associacao_existente(gerenciamento_proposta_id)

        if UniqueViolationCheck:
            raise UniqueViolation(f'gerenciamento_quantitativo already exist for gerenciamento_proposta ID: {gerenciamento_proposta_id}')

        gerenciamento_quantitativo = GerenciamentoQuantitativo(**gerenciamento_quantitativo.model_dump())
        gerenciamento_quantitativo = await self.repository.create_gerenciamento_quantitativo(gerenciamento_proposta_id, gerenciamento_quantitativo)

        return gerenciamento_quantitativo

    async def update_gerenciamento_quantitativo(self, gerenciamento_quantitativo_id: int, gerenciamento_quantitativo: GerenciamentoQuantitativo) -> GerenciamentoQuantitativo:
        await self.get_gerenciamento_quantitativo_by_id(gerenciamento_quantitativo_id)

        gerenciamento_quantitativo = GerenciamentoQuantitativo(**gerenciamento_quantitativo.model_dump())
        gerenciamento_quantitativo = await self.repository.update_gerenciamento_quantitativo(gerenciamento_quantitativo_id, gerenciamento_quantitativo)

        return gerenciamento_quantitativo

    async def delete_gerenciamento_quantitativo(self, gerenciamento_quantitativo_id: int):
        await self.get_gerenciamento_quantitativo_by_id(gerenciamento_quantitativo_id)

        NotNullViolation = await self.repository.checar_gerenciamento_caracterizacao_exists(gerenciamento_quantitativo_id)

        if NotNullViolation:
            raise NotNullViolationError('cannot delete a gerenciamento_quantitativo when there is an associated gerenciamento_caracterizacao')

        await self.repository.delete_gerenciamento_quantitativo(gerenciamento_quantitativo_id)

        return {'message': f'gerenciamento_quantitativo with ID {gerenciamento_quantitativo_id} deleted'}

    async def create_gerenciamento_quantitativo_comentario(self, gerenciamento_quantitativo_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO) -> GerenciamentoQuantitativo:
        await self.get_gerenciamento_quantitativo_by_id(gerenciamento_quantitativo_id)

        gerenciamento_comentario = GerenciamentoComentario(**gerenciamento_comentario.model_dump())
        gerenciamento_quantitativo_comentario = await self.repository.create_gerenciamento_quantitativo_comentario(gerenciamento_quantitativo_id, gerenciamento_comentario)

        return gerenciamento_quantitativo_comentario


class GerenciamentoQualitativoServices:
    def __init__(self, repository_gerenciamento: GerenciamentoQualitativoRepository, service_proposta: GerenciamentoPropostaServices):
        self.repository = repository_gerenciamento
        self.service_proposta = service_proposta

    async def get_gerenciamento_qualitativo(self) -> list[GerenciamentoQualitativo]:
        gerenciamento_qualitativos = await self.repository.get_gerenciamento_qualitativo()

        return gerenciamento_qualitativos

    async def get_gerenciamento_qualitativo_by_id(self, gerenciamento_qualitativo_id: int) -> GerenciamentoQualitativo:
        gerenciamento_qualitativo = await self.repository.get_gerenciamento_qualitativo_by_id(gerenciamento_qualitativo_id)

        if not gerenciamento_qualitativo:
            raise NotFoundError(f'gerenciamento_qualitativo with ID: {gerenciamento_qualitativo_id} not found')

        return gerenciamento_qualitativo

    async def create_gerenciamento_qualitativo(self, gerenciamento_proposta_id: int, gerenciamento_qualitativo: GerenciamentoQualitativoDTO) -> GerenciamentoQualitativo:
        await self.service_proposta.get_gerenciamento_proposta_by_id(gerenciamento_proposta_id)

        UniqueViolationCheck = await self.repository.checar_associacao_existente(gerenciamento_proposta_id)

        if UniqueViolationCheck:
            raise UniqueViolation(f'gerenciamento_qualitativo already exist for gerenciamento_proposta ID: {gerenciamento_proposta_id}')

        gerenciamento_qualitativo = GerenciamentoQualitativo(**gerenciamento_qualitativo.model_dump())
        gerenciamento_qualitativo = await self.repository.create_gerenciamento_qualitativo(gerenciamento_proposta_id, gerenciamento_qualitativo)

        return gerenciamento_qualitativo

    async def update_gerenciamento_qualitativo(self, gerenciamento_qualitativo_id: int, gerenciamento_qualitativo: GerenciamentoQualitativoDTO) -> GerenciamentoQualitativo | None:
        await self.get_gerenciamento_qualitativo_by_id(gerenciamento_qualitativo_id)

        gerenciamento_qualitativo = GerenciamentoQualitativo(**gerenciamento_qualitativo.model_dump())
        gerenciamento_qualitativo = await self.repository.update_gerenciamento_qualitativo(gerenciamento_qualitativo_id, gerenciamento_qualitativo)

        return gerenciamento_qualitativo

    async def delete_gerenciamento_qualitativo(self, gerenciamento_qualitativo_id: int):
        await self.get_gerenciamento_qualitativo_by_id(gerenciamento_qualitativo_id)

        await self.repository.delete_gerenciamento_qualitativo(gerenciamento_qualitativo_id)

        return {'message': f'gerenciamento_qualitativo with ID {gerenciamento_qualitativo_id} deleted'}

    async def create_gerenciamento_qualitativo_comentario(self, gerenciamento_qualitativo_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO) -> GerenciamentoQualitativo:
        await self.repository.get_gerenciamento_qualitativo_by_id(gerenciamento_qualitativo_id)

        gerenciamento_comentario = GerenciamentoComentario(**gerenciamento_comentario.model_dump())
        gerenciamento_qualitativo_comentario = await self.repository.create_gerenciamento_qualitativo_comentario(gerenciamento_qualitativo_id, gerenciamento_comentario)

        return gerenciamento_qualitativo_comentario


class GerenciamentoCaracterizacaoServices:
    def __init__(self, repository_gerenciamento: GerenciamentoCaracterizacaoRepository, service_quantitativo: GerenciamentoQuantitativoServices):
        self.repository = repository_gerenciamento
        self.service_quantitativo = service_quantitativo

    async def get_gerenciamento_caracterizacao(self) -> list[GerenciamentoCaracterizacao]:
        gerenciamento_caracterizacoes = await self.repository.get_gerenciamento_caracterizacao()

        return gerenciamento_caracterizacoes

    async def get_gerenciamento_caracterizacao_by_id(self, gerenciamento_caracterizacao_id: int) -> GerenciamentoCaracterizacao:
        gerenciamento_caracterizacao = await self.repository.get_gerenciamento_caracterizacao_by_id(gerenciamento_caracterizacao_id)

        if not gerenciamento_caracterizacao:
            raise NotFoundError(f'gerenciamento_caracterizacao with ID: {gerenciamento_caracterizacao_id} not found')

        return gerenciamento_caracterizacao

    async def create_gerenciamento_caracterizacao(self, gerenciamento_quantitativo_id: int, gerenciamento_caracterizacao: GerenciamentoCaracterizacaoDTO) -> GerenciamentoCaracterizacao:
        await self.service_quantitativo.get_gerenciamento_quantitativo_by_id(gerenciamento_quantitativo_id)

        UniqueViolationCheck = await self.repository.checar_associacao_existente(gerenciamento_quantitativo_id)

        if UniqueViolationCheck:
            raise UniqueViolation(f'gerenciamento_caracterizacao already exist for gerenciamento_quantitativo ID: {gerenciamento_quantitativo_id}')

        gerenciamento_caracterizacao.categorizacoes_ids = list(set(gerenciamento_caracterizacao.categorizacoes_ids))

        categorizacao = await self.repository.find_categorizacoes_by_ids(gerenciamento_caracterizacao.categorizacoes_ids)

        if not categorizacao:
            raise NotFoundError('one or more categorizacoes not found')

        gerenciamento_caracterizacao = GerenciamentoCaracterizacao(**gerenciamento_caracterizacao.model_dump())
        gerenciamento_caracterizacao = await self.repository.create_gerenciamento_caracterizacao(gerenciamento_quantitativo_id, gerenciamento_caracterizacao)

        return gerenciamento_caracterizacao

    async def update_gerenciamento_caracterizacao(self, gerenciamento_caracterizacao_id: int, gerenciamento_caracterizacao: GerenciamentoCaracterizacaoDTO) -> GerenciamentoCaracterizacao:
        await self.get_gerenciamento_caracterizacao_by_id(gerenciamento_caracterizacao_id)

        gerenciamento_caracterizacao.categorizacoes_ids = list(set(gerenciamento_caracterizacao.categorizacoes_ids))
        categorizacao = await self.repository.find_categorizacoes_by_ids(gerenciamento_caracterizacao.categorizacoes_ids)

        if not categorizacao:
            raise NotFoundError('one or more categorizacoes not found')

        gerenciamento_caracterizacao = GerenciamentoCaracterizacao(**gerenciamento_caracterizacao.model_dump())
        gerenciamento_caracterizacao = await self.repository.update_gerenciamento_caracterizacao(gerenciamento_caracterizacao_id, gerenciamento_caracterizacao)

        return gerenciamento_caracterizacao

    async def delete_gerenciamento_caracterizacao(self, gerenciamento_caracterizacao_id: int):
        await self.get_gerenciamento_caracterizacao_by_id(gerenciamento_caracterizacao_id)

        await self.repository.delete_gerenciamento_caracterizacao(gerenciamento_caracterizacao_id)

        return {'message': f'gerenciamento_caracterizacao with ID {gerenciamento_caracterizacao_id} deleted'}
