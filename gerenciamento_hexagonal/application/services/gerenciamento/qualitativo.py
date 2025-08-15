from gerenciamento_hexagonal.application.services.interfaces.gerenciamento.qualitativo import GerenciamentoQualitativoServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoComentario, GerenciamentoQualitativo
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoComentarioDTO, GerenciamentoQualitativoDTO
from gerenciamento_hexagonal.domain.services.validations import ValidacaoService


class GerenciamentoQualitativoServicesImpl(GerenciamentoQualitativoServices):
    async def get_gerenciamento_qualitativo(self) -> list[GerenciamentoQualitativo]:
        gerenciamento_qualitativos = await self.repository.get_gerenciamento_qualitativo()

        return gerenciamento_qualitativos

    async def get_gerenciamento_qualitativo_by_id(self, gerenciamento_qualitativo_id: int) -> GerenciamentoQualitativo:
        gerenciamento_qualitativo = await self.repository.get_gerenciamento_qualitativo_by_id(gerenciamento_qualitativo_id)

        if not gerenciamento_qualitativo:
            raise NotFoundError(f'gerenciamento_qualitativo with ID: {gerenciamento_qualitativo_id} not found')

        return gerenciamento_qualitativo

    async def create_gerenciamento_qualitativo(self, gerenciamento_proposta_id: int, gerenciamento_qualitativo: GerenciamentoQualitativoDTO) -> GerenciamentoQualitativo:
        await self.verify.gerencimento_proposta_exists(gerenciamento_proposta_id)

        ValidacaoService.validar_tamanho_string('gerenciamento qualitativo acoes_realizadas', gerenciamento_qualitativo.acoes_realizadas, 500)
        ValidacaoService.validar_tamanho_string('gerenciamento qualitativo acoes_previstas', gerenciamento_qualitativo.acoes_previstas, 500)
        ValidacaoService.validar_tamanho_string('gerenciamento qualitativo visao_proponente', gerenciamento_qualitativo.visao_proponente, 500)

        gerenciamento_qualitativo = GerenciamentoQualitativo(**gerenciamento_qualitativo.model_dump())
        gerenciamento_qualitativo = await self.repository.create_gerenciamento_qualitativo(gerenciamento_proposta_id, gerenciamento_qualitativo)

        return gerenciamento_qualitativo

    async def update_gerenciamento_qualitativo(self, gerenciamento_qualitativo_id: int, gerenciamento_qualitativo: GerenciamentoQualitativoDTO) -> GerenciamentoQualitativo | None:
        await self.get_gerenciamento_qualitativo_by_id(gerenciamento_qualitativo_id)

        ValidacaoService.validar_tamanho_string('gerenciamento qualitativo acoes_realizadas', gerenciamento_qualitativo.acoes_realizadas, 500)
        ValidacaoService.validar_tamanho_string('gerenciamento qualitativo acoes_previstas', gerenciamento_qualitativo.acoes_previstas, 500)
        ValidacaoService.validar_tamanho_string('gerenciamento qualitativo visao_proponente', gerenciamento_qualitativo.visao_proponente, 500)

        gerenciamento_qualitativo = GerenciamentoQualitativo(**gerenciamento_qualitativo.model_dump())
        gerenciamento_qualitativo = await self.repository.update_gerenciamento_qualitativo(gerenciamento_qualitativo_id, gerenciamento_qualitativo)

        return gerenciamento_qualitativo

    async def delete_gerenciamento_qualitativo(self, gerenciamento_qualitativo_id: int):
        gerenciamento_qualitativo = await self.get_gerenciamento_qualitativo_by_id(gerenciamento_qualitativo_id)
        if gerenciamento_qualitativo.arquivos_ids:
            raise ValueError(f'gerenciamento_contrapartida with ID: {gerenciamento_qualitativo_id} cannot be deleted because it has associated files with IDs: {gerenciamento_qualitativo.arquivos_ids}.')

        await self.repository.delete_gerenciamento_qualitativo(gerenciamento_qualitativo_id)

        return {'message': f'gerenciamento_qualitativo with ID {gerenciamento_qualitativo_id} deleted'}

    async def create_gerenciamento_qualitativo_comentario(self, gerenciamento_qualitativo_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO) -> GerenciamentoQualitativo:
        await self.repository.get_gerenciamento_qualitativo_by_id(gerenciamento_qualitativo_id)

        gerenciamento_comentario = GerenciamentoComentario(**gerenciamento_comentario.model_dump())
        gerenciamento_qualitativo_comentario = await self.repository.create_gerenciamento_qualitativo_comentario(gerenciamento_qualitativo_id, gerenciamento_comentario)

        return gerenciamento_qualitativo_comentario
