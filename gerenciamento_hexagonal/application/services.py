from typing import List

from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import (
    NotFoundError,
)
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoComentario, GerenciamentoMeta, GerenciamentoProposta, GerenciamentoQualitativo, GerenciamentoQuantitativo
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import (
    GerenciamentoComentarioDTO,
    GerenciamentoMetaDTO,
    GerenciamentoPropostaDTO,
    GerenciamentoQualitativoDTO,
    GerenciamentoQuantitativoDTO,
    RelatorioResponse,
)
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy_repository import (
    GerenciamentoComentarioRepository,
    GerenciamentoMetaRepository,
    GerenciamentoPropostaRepository,
    GerenciamentoQualitativoRepository,
    GerenciamentoQuantitativoRepository,
    RelatorioRepository,
)


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
        gerenciamento_proposta = GerenciamentoProposta(**gerenciamento_proposta.model_dump())
        gerenciamento_proposta = await self.repository.update_gerenciamento_proposta(gerenciamento_proposta_id, gerenciamento_proposta)
        if not gerenciamento_proposta:
            raise NotFoundError(f'gerenciamento_proposta with ID {gerenciamento_proposta_id} not found')

        return gerenciamento_proposta

    async def delete_gerenciamento_proposta(self, gerenciamento_proposta_id: int):
        delete = await self.repository.delete_gerenciamento_proposta(gerenciamento_proposta_id)
        if not delete:
            raise NotFoundError(f'gerenciamento_proposta with ID {gerenciamento_proposta_id} not found')

        return delete

    async def create_gerenciamento_proposta_comentario(self, gerenciamento_proposta_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO) -> GerenciamentoProposta:
        gerenciamento_comentario = GerenciamentoComentario(**gerenciamento_comentario.model_dump())
        gerenciamento_proposta = await self.repository.create_gerenciamento_proposta_comentario(gerenciamento_proposta_id, gerenciamento_comentario)
        if not gerenciamento_proposta:
            raise NotFoundError(f'gerenciamento_proposta with ID {gerenciamento_proposta_id} not found')

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
        gerenciamento_comentario = GerenciamentoComentario(**gerenciamento_comentario.model_dump())
        gerenciamento_comentario = await self.repository.update_gerenciamento_comentario(gerenciamento_comentario_id, gerenciamento_comentario)
        if not gerenciamento_comentario:
            raise NotFoundError(f'gerenciamento_comentario with ID {gerenciamento_comentario_id} not found')

        return gerenciamento_comentario

    async def delete_gerenciamento_comentario(self, gerenciamento_comentario_id: int) -> None:
        delete = await self.repository.delete_gerenciamento_comentario(gerenciamento_comentario_id)

        if not delete:
            raise NotFoundError(f'gerenciamento_comentario with ID {gerenciamento_comentario_id} not found')

        return delete


class GerenciamentoMetaServices:
    def __init__(self, repository_gerenciamento: GerenciamentoMetaRepository):
        self.repository = repository_gerenciamento

    async def get_gerenciamento_meta(self) -> list[GerenciamentoMeta]:
        gerenciamento_metas = await self.repository.get_gerenciamento_meta()

        return gerenciamento_metas

    async def get_gerenciamento_meta_by_id(self, gerenciamento_meta_id: int) -> GerenciamentoMeta:
        gerenciamento_meta = await self.repository.get_gerenciamento_meta_by_id(gerenciamento_meta_id)
        if not gerenciamento_meta:
            raise NotFoundError(f'gerenciamento_meta with ID {gerenciamento_meta_id} not found')

        return gerenciamento_meta

    async def create_gerenciamento_meta(self, gerenciamento_proposta_id: int, gerenciamento_meta: GerenciamentoMetaDTO) -> GerenciamentoMeta:
        try:
            gerenciamento_meta = GerenciamentoMeta(**gerenciamento_meta.model_dump())
            gerenciamento_meta = await self.repository.create_gerenciamento_meta(gerenciamento_proposta_id, gerenciamento_meta)

            return gerenciamento_meta

        except NotFoundError as e:
            raise e

    async def update_gerenciamento_meta(self, gerenciamento_meta_id: int, gerenciamento_meta: GerenciamentoMetaDTO) -> GerenciamentoMeta:
        gerenciamento_meta = GerenciamentoMeta(**gerenciamento_meta.model_dump())
        gerenciamento_meta = await self.repository.update_gerenciamento_meta(gerenciamento_meta_id, gerenciamento_meta)
        if not gerenciamento_meta:
            raise NotFoundError(f'gerenciamento_meta with ID {gerenciamento_meta_id} not found')

        return gerenciamento_meta

    async def delete_gerenciamento_meta(self, gerenciamento_meta_id: int) -> bool:
        delete = await self.repository.delete_gerenciamento_meta(gerenciamento_meta_id)
        if not delete:
            raise NotFoundError(f'gerenciamento_meta with ID {gerenciamento_meta_id} not found')

        return True


class GerenciamentoQuantitativoServices:
    def __init__(self, repository_gerenciamento: GerenciamentoQuantitativoRepository):
        self.repository = repository_gerenciamento

    async def get_gerenciamento_quantitativo(self) -> list[GerenciamentoQuantitativo]:
        gerenciamento_quantitativos = await self.repository.get_gerenciamento_quantitativo()

        return gerenciamento_quantitativos

    async def get_gerenciamento_quantitativo_by_id(self, gerenciamento_quantitativo_id: int) -> GerenciamentoQuantitativo:
        try:
            gerenciamento_quantitativo = await self.repository.get_gerenciamento_quantitativo_by_id(gerenciamento_quantitativo_id)

            return gerenciamento_quantitativo

        except NotFoundError as e:
            raise e

    async def create_gerenciamento_quantitativo(self, gerenciamento_proposta_id: int, gerenciamento_quantitativo: GerenciamentoQuantitativoDTO) -> GerenciamentoQuantitativo:
        try:
            gerenciamento_quantitativo = GerenciamentoQuantitativo(**gerenciamento_quantitativo.model_dump())
            gerenciamento_quantitativo = await self.repository.create_gerenciamento_quantitativo(gerenciamento_proposta_id, gerenciamento_quantitativo)

            return gerenciamento_quantitativo

        except NotFoundError as e:
            raise e

    async def update_gerenciamento_quantitativo(self, gerenciamento_quantitativo_id: int, gerenciamento_quantitativo: GerenciamentoQuantitativo) -> GerenciamentoQuantitativo:
        try:
            gerenciamento_quantitativo = GerenciamentoQuantitativo(**gerenciamento_quantitativo.model_dump())
            gerenciamento_quantitativo = await self.repository.update_gerenciamento_quantitativo(gerenciamento_quantitativo_id, gerenciamento_quantitativo)

            return gerenciamento_quantitativo

        except NotFoundError as e:
            raise e

    async def delete_gerenciamento_quantitativo(self, gerenciamento_quantitativo_id: int):
        try:
            result = await self.repository.delete_gerenciamento_quantitativo(gerenciamento_quantitativo_id)

            return result
        except NotFoundError as e:
            raise e

    async def create_gerenciamento_quantitativo_comentario(self, gerenciamento_quantitativo_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO) -> GerenciamentoQuantitativo:
        try:
            gerenciamento_comentario = GerenciamentoComentario(**gerenciamento_comentario.model_dump())
            gerenciamento_quantitativo_comentario = await self.repository.create_gerenciamento_quantitativo_comentario(gerenciamento_quantitativo_id, gerenciamento_comentario)

            return gerenciamento_quantitativo_comentario

        except NotFoundError as e:
            raise e


class GerenciamentoQualitativoServices:
    def __init__(self, repository_gerenciamento: GerenciamentoQualitativoRepository):
        self.repository = repository_gerenciamento

    async def get_gerenciamento_qualitativo(self) -> list[GerenciamentoQualitativo]:
        gerenciamento_qualitativos = await self.repository.get_gerenciamento_qualitativo()

        return gerenciamento_qualitativos

    async def get_gerenciamento_qualitativo_by_id(self, gerenciamento_qualitativo_id: int) -> GerenciamentoQualitativo:
        try:
            gerenciamento_qualitativo = await self.repository.get_gerenciamento_qualitativo_by_id(gerenciamento_qualitativo_id)

            return gerenciamento_qualitativo

        except NotFoundError:
            raise NotFoundError(f'gerenciamento_qualitativo with ID: {gerenciamento_qualitativo_id} not found')

    async def create_gerenciamento_qualitativo(self, gerenciamento_proposta_id: int, gerenciamento_qualitativo: GerenciamentoQualitativoDTO) -> GerenciamentoQualitativo:
        try:
            gerenciamento_qualitativo = GerenciamentoQualitativo(**gerenciamento_qualitativo.model_dump())
            gerenciamento_qualitativo = await self.repository.create_gerenciamento_qualitativo(gerenciamento_proposta_id, gerenciamento_qualitativo)

            return gerenciamento_qualitativo

        except NotFoundError as e:
            raise e

    async def update_gerenciamento_qualitativo(self, gerenciamento_qualitativo_id: int, gerenciamento_qualitativo: GerenciamentoQualitativoDTO) -> GerenciamentoQualitativo | None:
        try:
            gerenciamento_qualitativo = GerenciamentoQualitativo(**gerenciamento_qualitativo.model_dump())
            gerenciamento_qualitativo = await self.repository.update_gerenciamento_qualitativo(gerenciamento_qualitativo_id, gerenciamento_qualitativo)

            return gerenciamento_qualitativo

        except NotFoundError as e:
            raise e

    async def delete_gerenciamento_qualitativo(self, gerenciamento_qualitativo_id: int):
        try:
            result = await self.repository.delete_gerenciamento_qualitativo(gerenciamento_qualitativo_id)

            return result

        except NotFoundError as e:
            raise e

    async def create_gerenciamento_qualitativo_comentario(self, gerenciamento_qualitativo_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO) -> GerenciamentoQualitativo:
        try:
            gerenciamento_comentario = GerenciamentoComentario(**gerenciamento_comentario.model_dump())
            gerenciamento_qualitativo_comentario = await self.repository.create_gerenciamento_qualitativo_comentario(gerenciamento_qualitativo_id, gerenciamento_comentario)

            return gerenciamento_qualitativo_comentario

        except NotFoundError as e:
            raise e
