from gerenciamento_hexagonal.application.services.gerenciamento.proposta import GerenciamentoPropostaServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoContrapartida
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import GerenciamentoContrapartidaDTO
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy_repository import GerenciamentoContrapartidaRepository


class GerenciamentoContrapartidaServices:
    def __init__(self, repository: GerenciamentoContrapartidaRepository, service_proposta: GerenciamentoPropostaServices):
        self.repository = repository
        self.service_proposta = service_proposta

    async def get_gerenciamento_contrapartida(self) -> list[GerenciamentoContrapartida]:
        gerenciamento_contrapartidas = await self.repository.get_gerenciamento_contrapartida()

        return gerenciamento_contrapartidas

    async def get_gerenciamento_contrapartida_by_id(self, gerenciamento_contrapartida_id: int) -> GerenciamentoContrapartida | None:
        gerenciamento_contrapartida = await self.repository.get_gerenciamento_contrapartida_by_id(gerenciamento_contrapartida_id)

        if not gerenciamento_contrapartida:
            raise NotFoundError(f'gerenciamento_contrapartida with ID: {gerenciamento_contrapartida_id} not found')

        return gerenciamento_contrapartida

    async def create_gerenciamento_contrapartida(self, gerenciamento_proposta_id: int, gerenciamento_contrapartida: GerenciamentoContrapartidaDTO) -> GerenciamentoContrapartida:
        await self.service_proposta.get_gerenciamento_proposta_by_id(gerenciamento_proposta_id)

        gerenciamento_contrapartida = GerenciamentoContrapartida(gerenciamento_proposta_id=gerenciamento_proposta_id, **gerenciamento_contrapartida.model_dump())
        gerenciamento_contrapartida = await self.repository.create_gerenciamento_contrapartida(gerenciamento_contrapartida)

        return gerenciamento_contrapartida

    async def update_gerenciamento_contrapartida(self, gerenciamento_contrapartida_id: int, gerenciamento_contrapartida: GerenciamentoContrapartidaDTO) -> GerenciamentoContrapartida:
        await self.get_gerenciamento_contrapartida_by_id(gerenciamento_contrapartida_id)

        gerenciamento_contrapartida = GerenciamentoContrapartida(**gerenciamento_contrapartida.model_dump())
        gerenciamento_contrapartida = await self.repository.update_gerenciamento_contrapartida(gerenciamento_contrapartida_id, gerenciamento_contrapartida)

        return gerenciamento_contrapartida

    async def delete_gerenciamento_contrapartida(self, gerenciamento_contrapartida_id: int):
        await self.get_gerenciamento_contrapartida_by_id(gerenciamento_contrapartida_id)

        await self.repository.delete_gerenciamento_contrapartida(gerenciamento_contrapartida_id)

        return {'message': f'gerenciamento_contrapartida with ID {gerenciamento_contrapartida_id} deleted'}
