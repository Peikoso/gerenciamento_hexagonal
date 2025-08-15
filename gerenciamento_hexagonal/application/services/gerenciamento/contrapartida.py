from gerenciamento_hexagonal.application.services.interfaces.gerenciamento.contrapartida import GerenciamentoContrapartidaServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoContrapartida
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoContrapartidaDTO
from gerenciamento_hexagonal.domain.services.validations import ValidacaoService


class GerenciamentoContrapartidaServicesImpl(GerenciamentoContrapartidaServices):
    async def get_gerenciamento_contrapartida(self) -> list[GerenciamentoContrapartida]:
        gerenciamento_contrapartidas = await self.repository.get_gerenciamento_contrapartida()

        return gerenciamento_contrapartidas

    async def get_gerenciamento_contrapartida_by_id(self, gerenciamento_contrapartida_id: int) -> GerenciamentoContrapartida | None:
        gerenciamento_contrapartida = await self.repository.get_gerenciamento_contrapartida_by_id(gerenciamento_contrapartida_id)

        if not gerenciamento_contrapartida:
            raise NotFoundError(f'gerenciamento_contrapartida with ID: {gerenciamento_contrapartida_id} not found')

        return gerenciamento_contrapartida

    async def create_gerenciamento_contrapartida(self, gerenciamento_proposta_id: int, gerenciamento_contrapartida: GerenciamentoContrapartidaDTO) -> GerenciamentoContrapartida:
        await self.verify.gerencimento_proposta_exists(gerenciamento_proposta_id)

        ValidacaoService.validar_num_positivo('gerenciamento contrapartida quantidade', gerenciamento_contrapartida.quantidade)
        ValidacaoService.validar_tamanho_string('gerenciamento contrapartida observacao', gerenciamento_contrapartida.observacao, 300)

        gerenciamento_contrapartida = GerenciamentoContrapartida(gerenciamento_proposta_id=gerenciamento_proposta_id, **gerenciamento_contrapartida.model_dump())
        gerenciamento_contrapartida = await self.repository.create_gerenciamento_contrapartida(gerenciamento_contrapartida)

        return gerenciamento_contrapartida

    async def update_gerenciamento_contrapartida(self, gerenciamento_contrapartida_id: int, gerenciamento_contrapartida: GerenciamentoContrapartidaDTO) -> GerenciamentoContrapartida:
        await self.get_gerenciamento_contrapartida_by_id(gerenciamento_contrapartida_id)

        ValidacaoService.validar_num_positivo('gerenciamento contrapartida quantidade', gerenciamento_contrapartida.quantidade)
        ValidacaoService.validar_tamanho_string('gerenciamento contrapartida observacao', gerenciamento_contrapartida.observacao, 300)

        gerenciamento_contrapartida = GerenciamentoContrapartida(**gerenciamento_contrapartida.model_dump())
        gerenciamento_contrapartida = await self.repository.update_gerenciamento_contrapartida(gerenciamento_contrapartida_id, gerenciamento_contrapartida)

        return gerenciamento_contrapartida

    async def delete_gerenciamento_contrapartida(self, gerenciamento_contrapartida_id: int):
        gerenciamento_contrapartida = await self.get_gerenciamento_contrapartida_by_id(gerenciamento_contrapartida_id)
        if gerenciamento_contrapartida.arquivos_ids:
            raise ValueError(f'gerenciamento_contrapartida with ID: {gerenciamento_contrapartida_id} cannot be deleted because it has associated files with IDs: {gerenciamento_contrapartida.arquivos_ids}.')

        await self.repository.delete_gerenciamento_contrapartida(gerenciamento_contrapartida_id)

        return {'message': f'gerenciamento_contrapartida with ID {gerenciamento_contrapartida_id} deleted'}
