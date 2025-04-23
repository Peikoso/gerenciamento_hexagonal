from sqlalchemy import select

from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoComentario, GerenciamentoMeta, GerenciamentoProposta, GerenciamentoQualitativo, GerenciamentoQuantitativo
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import GerenciamentoComentarioDTO, GerenciamentoMetaDTO, GerenciamentoQuantitativoDTO, RelatorioResponse
from gerenciamento_hexagonal.domain.repositories.gerenciamento import (
    GerenciamentoComentarioRepository,
    GerenciamentoMetaRepository,
    GerenciamentoPropostaRepository,
    GerenciamentoQualitativoRepository,
    GerenciamentoQuantitativoRepository,
)
from gerenciamento_hexagonal.infrastructure.database.models.gerenciamentoORM import GerenciamentoComentarioModel, GerenciamentoMetaModel, GerenciamentoPropostaModel, GerenciamentoQualitativoModel, GerenciamentoQuantitativoModel
from gerenciamento_hexagonal.infrastructure.database.sqlalchemyConfig import get_session


class RelatorioRepository:
    async def get_relatorio(self, gerenciamento_proposta_id: int) -> RelatorioResponse:
        async with get_session() as session:
            relatorio = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id == gerenciamento_proposta_id))

            if not relatorio:
                return None

        return RelatorioResponse(
            proposta_id=relatorio.proposta_id,
            trimestre_de_referencia=relatorio.trimestre_de_referencia,
            tipo=relatorio.tipo,
            gerenciamento_metas=[GerenciamentoMetaDTO(ordem=gerenciamento_meta.ordem, alcancado=gerenciamento_meta.alcancado) for gerenciamento_meta in relatorio.gerenciamentoMetas],
            gerenciamento_quantitativos=[
                GerenciamentoQuantitativoDTO(
                    educacao_financeira_alcancados=gerenciamento_quantitativo.educacao_financeira_alcancados,
                    educacao_financeira_impactados=gerenciamento_quantitativo.educacao_financeira_impactados,
                    geracao_renda_postos_trabalho_gerados=gerenciamento_quantitativo.geracao_renda_postos_trabalho_gerados,
                    alcance_marca_pessoas_alcancadas_publicacao_digitais=gerenciamento_quantitativo.alcance_marca_pessoas_alcancadas_publicacao_digitais,
                    pessoas_alcancadas=gerenciamento_quantitativo.pessoas_alcancadas,
                    pessoas_impactadas=gerenciamento_quantitativo.pessoas_impactadas,
                )
                for gerenciamento_quantitativo in relatorio.gerenciamentoQuantitativos
            ],
        )


class GerenciamentoComentarioRepository(GerenciamentoComentarioRepository):
    async def get_gerenciamento_comentario(self) -> list[GerenciamentoComentario]:
        async with get_session() as session:
            db_gerenciamento_comentarios = await session.scalars(select(GerenciamentoComentarioModel))

            result = [GerenciamentoComentario.model_validate(vars(db_gerenciamento_comentario)) for db_gerenciamento_comentario in db_gerenciamento_comentarios if db_gerenciamento_comentario is not None]

            return result

    async def get_gerenciamento_comentario_by_id(self, gerenciamento_comentario_id: int) -> GerenciamentoComentario:
        async with get_session() as session:
            db_gerenciamento_comentario = await session.scalar(select(GerenciamentoComentarioModel).where(GerenciamentoComentarioModel.id == gerenciamento_comentario_id))
            if db_gerenciamento_comentario:
                return GerenciamentoComentario.model_validate(vars(db_gerenciamento_comentario))

            return None

    async def create_gerenciamento_comentario(self, gerenciamento_comentario: GerenciamentoComentario) -> GerenciamentoComentarioModel:
        async with get_session() as session:
            db_gerenciamento_comentario = GerenciamentoComentarioModel(comentario=gerenciamento_comentario.comentario)
            session.add(db_gerenciamento_comentario)
            await session.commit()
            await session.refresh(db_gerenciamento_comentario)

            return db_gerenciamento_comentario

    async def update_gerenciamento_comentario(self, gerenciamento_comentario_id, gerenciamento_comentario: GerenciamentoComentarioDTO) -> GerenciamentoComentario:
        async with get_session() as session:
            db_gerenciamento_comentario = await session.scalar(select(GerenciamentoComentarioModel).where(GerenciamentoComentarioModel.id == gerenciamento_comentario_id))

            if db_gerenciamento_comentario:
                db_gerenciamento_comentario.comentario = gerenciamento_comentario.comentario

                await session.commit()
                await session.refresh(db_gerenciamento_comentario)

                return GerenciamentoComentario.model_validate(vars(db_gerenciamento_comentario))

    async def delete_gerenciamento_comentario(self, gerenciamento_comentario_id: int) -> bool:
        async with get_session() as session:
            db_gerenciamento_comentario = await session.scalar(select(GerenciamentoComentarioModel).where(GerenciamentoComentarioModel.id == gerenciamento_comentario_id))

            if db_gerenciamento_comentario:
                await session.delete(db_gerenciamento_comentario)
                await session.commit()

                return True

            return False


class GerenciamentoPropostaRepository(GerenciamentoPropostaRepository):
    def __init__(self, gerenciamento_comentario_repository: GerenciamentoComentarioRepository):
        self.gerenciamento_comentario_repository = gerenciamento_comentario_repository

    async def get_gerenciamento_proposta(self) -> list[GerenciamentoProposta]:
        async with get_session() as session:
            gerenciamento_propostas = await session.scalars(select(GerenciamentoPropostaModel))

            result = [GerenciamentoProposta.model_validate({**vars(gerenciamento_proposta), 'metas_comentarios': [GerenciamentoComentario.model_validate(vars(gerenciamento_comentario)) for gerenciamento_comentario in gerenciamento_proposta.metas_comentarios]}) for gerenciamento_proposta in gerenciamento_propostas if gerenciamento_proposta is not None]

        return result

    async def get_gerenciamento_proposta_by_id(self, gerenciamento_proposta_id: int) -> GerenciamentoProposta:
        async with get_session() as session:
            db_gerenciamento_proposta = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id == gerenciamento_proposta_id))
            if db_gerenciamento_proposta:
                return GerenciamentoProposta.model_validate({**vars(db_gerenciamento_proposta), 'metas_comentarios': [GerenciamentoComentario.model_validate(vars(gerenciamento_comentario)) for gerenciamento_comentario in db_gerenciamento_proposta.metas_comentarios]})
            return None

    async def create_gerenciamento_proposta(self, gerenciamento_proposta: GerenciamentoProposta) -> GerenciamentoProposta:
        async with get_session() as session:
            db_gerenciamento_proposta = GerenciamentoPropostaModel(trimestre_de_referencia=gerenciamento_proposta.trimestre_de_referencia, tipo=gerenciamento_proposta.tipo, proposta_id=gerenciamento_proposta.proposta_id)
            session.add(db_gerenciamento_proposta)
            await session.commit()
            await session.refresh(db_gerenciamento_proposta)

            return GerenciamentoProposta.model_validate(vars(db_gerenciamento_proposta))

    async def update_gerenciamento_proposta(self, gerenciamento_proposta_id: int, gerenciamento_proposta: GerenciamentoProposta) -> GerenciamentoProposta:
        async with get_session() as session:
            db_gerenciamento_proposta = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id == gerenciamento_proposta_id))
            if db_gerenciamento_proposta:
                db_gerenciamento_proposta.proposta_id = gerenciamento_proposta.proposta_id
                db_gerenciamento_proposta.trimestre_de_referencia = gerenciamento_proposta.trimestre_de_referencia
                db_gerenciamento_proposta.tipo = gerenciamento_proposta.tipo

                await session.commit()
                await session.refresh(db_gerenciamento_proposta)

                return GerenciamentoProposta.model_validate({**vars(db_gerenciamento_proposta), 'metas_comentarios': [GerenciamentoComentario.model_validate(vars(gerenciamento_comentario)) for gerenciamento_comentario in db_gerenciamento_proposta.metas_comentarios]})

            return None

    async def delete_gerenciamento_proposta(self, gerenciamento_proposta_id: int) -> bool:
        async with get_session() as session:
            gerenciamento_proposta = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id == gerenciamento_proposta_id))
            if gerenciamento_proposta:
                await session.delete(gerenciamento_proposta)
                await session.commit()

                return True

            return False

    async def create_gerenciamento_proposta_comentario(self, gerenciamento_proposta_id: int, gerenciamento_comentario: GerenciamentoComentario) -> GerenciamentoProposta:
        async with get_session() as session:
            db_gerenciamento_proposta = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id == gerenciamento_proposta_id))

            if db_gerenciamento_proposta:
                db_gerenciamento_comentario = await self.gerenciamento_comentario_repository.create_gerenciamento_comentario(gerenciamento_comentario)

                if db_gerenciamento_comentario not in session:
                    session.add(db_gerenciamento_comentario)

                db_gerenciamento_proposta.metas_comentarios.append(db_gerenciamento_comentario)

                session.add(db_gerenciamento_proposta)
                await session.commit()
                await session.refresh(db_gerenciamento_proposta)

                return GerenciamentoProposta.model_validate({**vars(db_gerenciamento_proposta), 'metas_comentarios': [GerenciamentoComentario.model_validate(vars(gerenciamento_comentario)) for gerenciamento_comentario in db_gerenciamento_proposta.metas_comentarios]})

            return None


class GerenciamentoMetaRepository(GerenciamentoMetaRepository):
    async def get_gerenciamento_meta(self) -> list[GerenciamentoMeta]:
        async with get_session() as session:
            db_gerenciamento_metas = await session.scalars(select(GerenciamentoMetaModel))

            result = [GerenciamentoMeta.model_validate(vars(db_gerenciamento_meta)) for db_gerenciamento_meta in db_gerenciamento_metas if db_gerenciamento_meta is not None]

            return result

    async def get_gerenciamento_meta_by_id(self, gerenciamento_meta_id: int) -> GerenciamentoMeta:
        async with get_session() as session:
            db_gerenciamento_meta = await session.scalar(select(GerenciamentoMetaModel).where(GerenciamentoMetaModel.id == gerenciamento_meta_id))

            if db_gerenciamento_meta:
                return GerenciamentoMeta.model_validate(vars(db_gerenciamento_meta))

            return None

    async def create_gerenciamento_meta(self, gerenciamento_proposta_id: int, gerenciamento_meta: GerenciamentoMeta) -> GerenciamentoMeta:
        async with get_session() as session:
            db_gerenciamento_proposta = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id == gerenciamento_proposta_id))

            if not db_gerenciamento_proposta:
                raise NotFoundError(f'gerenciamento_proposta with ID {gerenciamento_proposta_id} not found')

            db_gerenciamento_meta = GerenciamentoMetaModel(ordem=gerenciamento_meta.ordem, alcancado=gerenciamento_meta.alcancado, gerenciamento_proposta_id=gerenciamento_proposta_id)
            session.add(db_gerenciamento_meta)
            await session.commit()
            await session.refresh(db_gerenciamento_meta)

            return GerenciamentoMeta.model_validate(vars(db_gerenciamento_meta))

    async def update_gerenciamento_meta(self, gerenciamento_meta_id: int, gerenciamento_meta: GerenciamentoMeta) -> GerenciamentoMeta:
        async with get_session() as session:
            db_gerenciamento_meta = await session.scalar(select(GerenciamentoMetaModel).where(GerenciamentoMetaModel.id == gerenciamento_meta_id))

            if db_gerenciamento_meta:
                db_gerenciamento_meta.alcancado = gerenciamento_meta.alcancado
                db_gerenciamento_meta.ordem = gerenciamento_meta.ordem

                await session.commit()
                await session.refresh(db_gerenciamento_meta)

                return GerenciamentoMeta.model_validate(vars(db_gerenciamento_meta))

            return None

    async def delete_gerenciamento_meta(self, gerenciamento_meta_id: int) -> bool:
        async with get_session() as session:
            db_gerenciamento_meta = await session.scalar(select(GerenciamentoMetaModel).where(GerenciamentoMetaModel.id == gerenciamento_meta_id))

            if db_gerenciamento_meta:
                await session.delete(db_gerenciamento_meta)
                await session.commit()

                return True

            return False


class GerenciamentoQuantitativoRepository(GerenciamentoQuantitativoRepository):
    def __init__(self, gerenciamento_comentario_repository: GerenciamentoComentarioRepository):
        self.gerenciamento_comentario_repository = gerenciamento_comentario_repository

    async def get_gerenciamento_quantitativo(self) -> list[GerenciamentoQuantitativo]:
        async with get_session() as session:
            db_gerenciamento_quantitativos = await session.scalars(select(GerenciamentoQuantitativoModel))

            result = [GerenciamentoQuantitativo.model_validate({**vars(db_gerenciamento_quantitativo), 'comentarios': [GerenciamentoComentario.model_validate(vars(gerenciamento_comentario)) for gerenciamento_comentario in db_gerenciamento_quantitativo.comentarios]}) for db_gerenciamento_quantitativo in db_gerenciamento_quantitativos if db_gerenciamento_quantitativo is not None]

            return result

    async def get_gerenciamento_quantitativo_by_id(self, gerenciamento_quantitativo_id: int) -> GerenciamentoQuantitativo:
        async with get_session() as session:
            db_gerenciamento_quantitativo = await session.scalar(select(GerenciamentoQuantitativoModel).where(GerenciamentoQuantitativoModel.id == gerenciamento_quantitativo_id))

            if not db_gerenciamento_quantitativo:
                raise NotFoundError(f'gerenciamento_quantitativo with ID: {gerenciamento_quantitativo_id} not found')

            result = GerenciamentoQuantitativo.model_validate({**vars(db_gerenciamento_quantitativo), 'comentarios': [GerenciamentoComentario.model_validate(vars(gerenciamento_comentario)) for gerenciamento_comentario in db_gerenciamento_quantitativo.comentarios]})

            return result

    async def create_gerenciamento_quantitativo(self, gerenciamento_proposta_id: int, gerenciamento_quantitativo: GerenciamentoQuantitativo) -> GerenciamentoQuantitativo:
        async with get_session() as session:
            db_gerenciamento_proposta = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id == gerenciamento_proposta_id))

            if not db_gerenciamento_proposta:
                raise NotFoundError(f'gerenciamento_proposta with ID: {gerenciamento_proposta_id} not found')

            db_gerenciamento_quantitativo = GerenciamentoQuantitativoModel(
                educacao_financeira_alcancados=gerenciamento_quantitativo.educacao_financeira_alcancados,
                educacao_financeira_impactados=gerenciamento_quantitativo.educacao_financeira_impactados,
                geracao_renda_postos_trabalho_gerados=gerenciamento_quantitativo.geracao_renda_postos_trabalho_gerados,
                alcance_marca_pessoas_alcancadas_publicacao_digitais=gerenciamento_quantitativo.alcance_marca_pessoas_alcancadas_publicacao_digitais,
                pessoas_alcancadas=gerenciamento_quantitativo.pessoas_alcancadas,
                pessoas_impactadas=gerenciamento_quantitativo.pessoas_impactadas,
                gerenciamento_proposta_id=gerenciamento_proposta_id,
            )

            session.add(db_gerenciamento_quantitativo)
            await session.commit()
            await session.refresh(db_gerenciamento_quantitativo)

            return GerenciamentoQuantitativo.model_validate(vars(db_gerenciamento_quantitativo))

    async def update_gerenciamento_quantitativo(self, gerenciamento_quantitativo_id: int, gerenciamento_quantitativo: GerenciamentoQuantitativo) -> GerenciamentoQuantitativo:
        async with get_session() as session:
            db_gerenciamento_quantitativo = await session.scalar(select(GerenciamentoQuantitativoModel).where(GerenciamentoQuantitativoModel.id == gerenciamento_quantitativo_id))

            if not db_gerenciamento_quantitativo:
                raise NotFoundError(f'gerenciamento_quantitativo with ID: {gerenciamento_quantitativo_id} not found')

            db_gerenciamento_quantitativo.educacao_financeira_alcancados = gerenciamento_quantitativo.educacao_financeira_alcancados
            db_gerenciamento_quantitativo.educacao_financeira_impactados = gerenciamento_quantitativo.educacao_financeira_impactados
            db_gerenciamento_quantitativo.geracao_renda_postos_trabalho_gerados = gerenciamento_quantitativo.geracao_renda_postos_trabalho_gerados
            db_gerenciamento_quantitativo.alcance_marca_pessoas_alcancadas_publicacao_digitais = gerenciamento_quantitativo.alcance_marca_pessoas_alcancadas_publicacao_digitais
            db_gerenciamento_quantitativo.pessoas_alcancadas = gerenciamento_quantitativo.pessoas_alcancadas
            db_gerenciamento_quantitativo.pessoas_impactadas = gerenciamento_quantitativo.pessoas_impactadas

            await session.commit()
            await session.refresh(db_gerenciamento_quantitativo)

            return GerenciamentoQuantitativo.model_validate({**vars(db_gerenciamento_quantitativo), 'comentarios': [GerenciamentoComentario.model_validate(vars(gerenciamento_comentario)) for gerenciamento_comentario in db_gerenciamento_quantitativo.comentarios]})

    async def delete_gerenciamento_quantitativo(self, gerenciamento_quantitativo_id: int):
        async with get_session() as session:
            db_gerenciamento_quantitativo = await session.scalar(select(GerenciamentoQuantitativoModel).where(GerenciamentoQuantitativoModel.id == gerenciamento_quantitativo_id))

            if not db_gerenciamento_quantitativo:
                raise NotFoundError(f'gerenciamento_quantitativo with ID: {gerenciamento_quantitativo_id} not found')

            await session.delete(db_gerenciamento_quantitativo)
            await session.commit()

            return {'message': f'gerenciamento_quantitativo with ID {gerenciamento_quantitativo_id} deleted'}

    async def create_gerenciamento_quantitativo_comentario(self, gerenciamento_quantitativo_id: int, gerenciamento_comentario: GerenciamentoComentario) -> GerenciamentoQuantitativo:
        async with get_session() as session:
            db_gerenciamento_quantitativo = await session.scalar(select(GerenciamentoQuantitativoModel).where(GerenciamentoQuantitativoModel.id == gerenciamento_quantitativo_id))

            if not db_gerenciamento_quantitativo:
                raise NotFoundError(f'gerenciamento_quantitativo with ID: {gerenciamento_quantitativo_id} not found')

            db_gerenciamento_comentario = await self.gerenciamento_comentario_repository.create_gerenciamento_comentario(gerenciamento_comentario)

            if db_gerenciamento_comentario not in session:
                session.add(db_gerenciamento_comentario)

            db_gerenciamento_quantitativo.comentarios.append(db_gerenciamento_comentario)

            session.add(db_gerenciamento_quantitativo)
            await session.commit()
            await session.refresh(db_gerenciamento_quantitativo)

            return GerenciamentoQuantitativo.model_validate({**vars(db_gerenciamento_quantitativo), 'comentarios': [GerenciamentoComentario.model_validate(vars(gerenciamento_comentario)) for gerenciamento_comentario in db_gerenciamento_quantitativo.comentarios]})


class GerenciamentoQualitativoRepository(GerenciamentoQualitativoRepository):
    def __init__(self, gerenciamento_comentario_repository: GerenciamentoComentarioRepository):
        self.gerenciamento_comentario_repository = gerenciamento_comentario_repository

    async def get_gerenciamento_qualitativo(self) -> list[GerenciamentoQualitativo]:
        async with get_session() as session:
            db_gerenciamento_qualitativos = await session.scalars(select(GerenciamentoQualitativoModel))

            result = [GerenciamentoQualitativo.model_validate({**vars(db_gerenciamento_qualitativo), 'comentarios': [GerenciamentoComentario.model_validate(vars(gerenciamento_comentario)) for gerenciamento_comentario in db_gerenciamento_qualitativo.comentarios]}) for db_gerenciamento_qualitativo in db_gerenciamento_qualitativos if db_gerenciamento_qualitativo is not None]

            return result

    async def get_gerenciamento_qualitativo_by_id(self, gerenciamento_qualitativo_id: int) -> GerenciamentoQualitativo:
        async with get_session() as session:
            db_gerenciamento_qualitativo = await session.scalar(select(GerenciamentoQualitativoModel).where(GerenciamentoQualitativoModel.id==gerenciamento_qualitativo_id))
            
            if not db_gerenciamento_qualitativo:
                raise NotFoundError()
            
            result = GerenciamentoQualitativo.model_validate({**vars(db_gerenciamento_qualitativo), 'comentarios': [GerenciamentoComentario.model_validate(vars(comentario)) for comentario in db_gerenciamento_qualitativo.comentarios]})
            
            return result
            
    async def create_gerenciamento_qualitativo(self, gerenciamento_proposta_id: int, gerenciamento_qualitativo: GerenciamentoQualitativo) -> GerenciamentoQualitativo:
        async with get_session() as session:
            db_gerenciamento_proposta = await session.scalar(select(GerenciamentoPropostaModel).where(GerenciamentoPropostaModel.id==gerenciamento_proposta_id))

            if not db_gerenciamento_proposta:
                raise NotFoundError(f'gerenciamento_proposta with ID: {gerenciamento_proposta_id} not found')

            db_gerenciamento_qualitativo = GerenciamentoQualitativoModel(acoes_previstas=gerenciamento_qualitativo.acoes_previstas, acoes_realizadas=gerenciamento_qualitativo.acoes_realizadas, visao_proponente=gerenciamento_qualitativo.visao_proponente, gerenciamento_proposta_id=gerenciamento_proposta_id)

            session.add(db_gerenciamento_qualitativo)
            await session.commit()
            await session.refresh(db_gerenciamento_qualitativo)

            return GerenciamentoQualitativo.model_validate(vars(db_gerenciamento_qualitativo))

    async def update_gerenciamento_qualitativo(self, gerenciamento_qualitativo_id: int, gerenciamento_qualitativo: GerenciamentoQualitativo) -> GerenciamentoQualitativo | None:
        async with get_session() as session:
            db_gerenciamento_qualitativo = await session.scalar(select(GerenciamentoQualitativoModel).where(GerenciamentoQualitativoModel.id==gerenciamento_qualitativo_id))
            
            if not db_gerenciamento_qualitativo:
                raise NotFoundError(f'gerenciamento_qualitativo with ID: {gerenciamento_qualitativo_id} not found')
            
            db_gerenciamento_qualitativo.acoes_previstas = gerenciamento_qualitativo.acoes_previstas
            db_gerenciamento_qualitativo.acoes_realizadas = gerenciamento_qualitativo.acoes_realizadas
            db_gerenciamento_qualitativo.visao_proponente = gerenciamento_qualitativo.visao_proponente
            
            await session.commit()
            await session.refresh(db_gerenciamento_qualitativo)
            
            result = GerenciamentoQualitativo.model_validate({**vars(db_gerenciamento_qualitativo), 'comentarios': [GerenciamentoComentario.model_validate(vars(comentario)) for comentario in db_gerenciamento_qualitativo.comentarios]})
            
            return result

    async def delete_gerenciamento_qualitativo(self, gerenciamento_qualitativo_id: int):
        async with get_session() as session:
            db_gerenciamento_qualitativo = await session.scalar(select(GerenciamentoQualitativoModel).where(GerenciamentoQualitativoModel.id==gerenciamento_qualitativo_id))
            
            if not db_gerenciamento_qualitativo:
                raise NotFoundError(f'gerenciamento_qualitativo with ID: {gerenciamento_qualitativo_id} not found')
            
            await session.delete(db_gerenciamento_qualitativo)
            await session.commit()
            
            return {'message': f'gerenciamento_qualitativo with ID {gerenciamento_qualitativo_id} deleted'}
    
    async def create_gerenciamento_qualitativo_comentario(self, gerenciamento_qualitativo_id: int, gerenciamento_comentario: GerenciamentoComentario) -> GerenciamentoQualitativo:
        async with get_session() as session:
            db_gerenciamento_qualitativo = await session.scalar(select(GerenciamentoQualitativoModel).where(GerenciamentoQualitativoModel.id==gerenciamento_qualitativo_id))
            
            if not db_gerenciamento_qualitativo:
                raise NotFoundError(f'gerenciamento_qualitativo with ID: {gerenciamento_qualitativo_id} not found')
            
            db_gerenciamento_comentario = await self.gerenciamento_comentario_repository.create_gerenciamento_comentario(gerenciamento_comentario)
            
            if db_gerenciamento_comentario not in session:
                session.add(db_gerenciamento_comentario)
                
            db_gerenciamento_qualitativo.comentarios.append(db_gerenciamento_comentario)
            
            session.add(db_gerenciamento_qualitativo)
            await session.commit()
            await session.refresh(db_gerenciamento_qualitativo)
            
            result = GerenciamentoQualitativo.model_validate({**vars(db_gerenciamento_qualitativo), 'comentarios': [GerenciamentoComentario.model_validate(vars(comentario)) for comentario in db_gerenciamento_qualitativo.comentarios]})
            
            return result
        