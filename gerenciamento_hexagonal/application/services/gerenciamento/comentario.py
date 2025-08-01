from gerenciamento_hexagonal.application.services.interfaces.gerenciamento.comentario import GerenciamentoComentarioServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoComentario
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoComentarioDTO


class GerenciamentoComentarioServicesImpl(GerenciamentoComentarioServices):
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

        return {'message': f'gerenciamento_comentario with ID {gerenciamento_comentario_id} deleted'}
