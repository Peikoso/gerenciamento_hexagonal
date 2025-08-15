from gerenciamento_hexagonal.application.services.interfaces.gerenciamento.quantitativo import GerenciamentoQuantitativoServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError, NotNullViolationError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoComentario, GerenciamentoQuantitativo
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoComentarioDTO, GerenciamentoQuantitativoDTO
from gerenciamento_hexagonal.domain.services.validations import ValidacaoService


class GerenciamentoQuantitativoServicesImpl(GerenciamentoQuantitativoServices):
    async def get_gerenciamento_quantitativo(self) -> list[GerenciamentoQuantitativo]:
        gerenciamento_quantitativos = await self.repository.get_gerenciamento_quantitativo()

        return gerenciamento_quantitativos

    async def get_gerenciamento_quantitativo_by_id(self, gerenciamento_quantitativo_id: int) -> GerenciamentoQuantitativo:
        gerenciamento_quantitativo = await self.repository.get_gerenciamento_quantitativo_by_id(gerenciamento_quantitativo_id)

        if not gerenciamento_quantitativo:
            raise NotFoundError(f'gerenciamento_quantitativo with ID: {gerenciamento_quantitativo_id} not found')

        return gerenciamento_quantitativo

    async def create_gerenciamento_quantitativo(self, gerenciamento_proposta_id: int, gerenciamento_quantitativo: GerenciamentoQuantitativoDTO) -> GerenciamentoQuantitativo:
        await self.verify.gerencimento_proposta_exists(gerenciamento_proposta_id)

        ValidacaoService.validar_num_positivo('gerenciamento quantitativo educacao_financeira_impactados', gerenciamento_quantitativo.educacao_financeira_impactados)
        ValidacaoService.validar_num_positivo('gerenciamento quantitativo educacao_financeira_alcancados', gerenciamento_quantitativo.educacao_financeira_alcancados)
        ValidacaoService.validar_num_positivo('gerenciamento quantitativo geracao_renda_postos_trabalho_gerados', gerenciamento_quantitativo.geracao_renda_postos_trabalho_gerados)
        ValidacaoService.validar_num_positivo('gerenciamento quantitativo alcance_marca_pessoas_alcancadas_publicacao_digitais', gerenciamento_quantitativo.alcance_marca_pessoas_alcancadas_publicacao_digitais)
        ValidacaoService.validar_num_positivo('gerenciamento quantitativo pessoas_alcancadas', gerenciamento_quantitativo.pessoas_alcancadas)
        ValidacaoService.validar_num_positivo('gerenciamento quantitativo pessoas_impactadas', gerenciamento_quantitativo.pessoas_impactadas)

        gerenciamento_quantitativo = GerenciamentoQuantitativo(**gerenciamento_quantitativo.model_dump())
        gerenciamento_quantitativo = await self.repository.create_gerenciamento_quantitativo(gerenciamento_proposta_id, gerenciamento_quantitativo)

        return gerenciamento_quantitativo

    async def update_gerenciamento_quantitativo(self, gerenciamento_quantitativo_id: int, gerenciamento_quantitativo: GerenciamentoQuantitativoDTO) -> GerenciamentoQuantitativo:
        await self.get_gerenciamento_quantitativo_by_id(gerenciamento_quantitativo_id)

        ValidacaoService.validar_num_positivo('gerenciamento quantitativo educacao_financeira_impactados', gerenciamento_quantitativo.educacao_financeira_impactados)
        ValidacaoService.validar_num_positivo('gerenciamento quantitativo educacao_financeira_alcancados', gerenciamento_quantitativo.educacao_financeira_alcancados)
        ValidacaoService.validar_num_positivo('gerenciamento quantitativo geracao_renda_postos_trabalho_gerados', gerenciamento_quantitativo.geracao_renda_postos_trabalho_gerados)
        ValidacaoService.validar_num_positivo('gerenciamento quantitativo alcance_marca_pessoas_alcancadas_publicacao_digitais', gerenciamento_quantitativo.alcance_marca_pessoas_alcancadas_publicacao_digitais)
        ValidacaoService.validar_num_positivo('gerenciamento quantitativo pessoas_alcancadas', gerenciamento_quantitativo.pessoas_alcancadas)
        ValidacaoService.validar_num_positivo('gerenciamento quantitativo pessoas_impactadas', gerenciamento_quantitativo.pessoas_impactadas)

        gerenciamento_quantitativo = GerenciamentoQuantitativo(**gerenciamento_quantitativo.model_dump())
        gerenciamento_quantitativo = await self.repository.update_gerenciamento_quantitativo(gerenciamento_quantitativo_id, gerenciamento_quantitativo)

        return gerenciamento_quantitativo

    async def delete_gerenciamento_quantitativo(self, gerenciamento_quantitativo_id: int):
        await self.get_gerenciamento_quantitativo_by_id(gerenciamento_quantitativo_id)

        not_null_violation = await self.repository.checar_gerenciamento_caracterizacao_exists(gerenciamento_quantitativo_id)

        if not_null_violation:
            raise NotNullViolationError('cannot delete a gerenciamento_quantitativo when there is an associated gerenciamento_caracterizacao')

        await self.repository.delete_gerenciamento_quantitativo(gerenciamento_quantitativo_id)

        return {'message': f'gerenciamento_quantitativo with ID {gerenciamento_quantitativo_id} deleted'}

    async def create_gerenciamento_quantitativo_comentario(self, gerenciamento_quantitativo_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO) -> GerenciamentoQuantitativo:
        await self.get_gerenciamento_quantitativo_by_id(gerenciamento_quantitativo_id)

        gerenciamento_comentario = GerenciamentoComentario(**gerenciamento_comentario.model_dump())
        gerenciamento_quantitativo_comentario = await self.repository.create_gerenciamento_quantitativo_comentario(gerenciamento_quantitativo_id, gerenciamento_comentario)

        return gerenciamento_quantitativo_comentario
