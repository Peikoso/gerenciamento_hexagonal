from http import HTTPStatus

from fastapi import APIRouter, File, HTTPException, UploadFile

from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError, UniqueViolation
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoQualitativo
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoComentarioDTO, GerenciamentoQualitativoDTO
from gerenciamento_hexagonal.entrypoints.annotated import Service_Arquivo, Service_Qualitativo, Validacao_Arquivo
from gerenciamento_hexagonal.entrypoints.arquivo_wrapper import ArquivoWrapper

router = APIRouter()


@router.get('/', response_model=list[GerenciamentoQualitativo])
async def get_gerenciamento_qualitativo(service: Service_Qualitativo):
    gerenciamento_qualitativo = await service.get_gerenciamento_qualitativo()

    return gerenciamento_qualitativo


@router.get('/{gerenciamento_qualitativo_id}', response_model=GerenciamentoQualitativo)
async def get_gerenciamento_qualitativo_by_id(gerenciamento_qualitativo_id: int, service: Service_Qualitativo):
    try:
        gerenciamento_qualitativo = await service.get_gerenciamento_qualitativo_by_id(gerenciamento_qualitativo_id)

        return gerenciamento_qualitativo

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.post('/{gerenciamento_proposta_id}', response_model=GerenciamentoQualitativo)
async def create_gerenciamento_qualitativo(gerenciamento_proposta_id: int, gerenciamento_qualitativo: GerenciamentoQualitativoDTO, service: Service_Qualitativo):
    try:
        gerenciamento_qualitativo = await service.create_gerenciamento_qualitativo(gerenciamento_proposta_id, gerenciamento_qualitativo)

        return gerenciamento_qualitativo

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except UniqueViolation as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))


@router.post('/Comentario/{gerenciamento_qualitativo_id}', response_model=GerenciamentoQualitativo)
async def create_gerenciamento_qualitativo_comentario(gerenciamento_qualitativo_id: int, gerenciamento_comentario: GerenciamentoComentarioDTO, service: Service_Qualitativo):
    try:
        gerenciamento_qualitativo_comentario = await service.create_gerenciamento_qualitativo_comentario(gerenciamento_qualitativo_id, gerenciamento_comentario)

        return gerenciamento_qualitativo_comentario

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.put('/{gerenciamento_qualitativo_id}', response_model=GerenciamentoQualitativo)
async def update_gerenciamento_qualitativo(gerenciamento_qualitativo_id: int, gerenciamento_qualitativo: GerenciamentoQualitativoDTO, service: Service_Qualitativo):
    try:
        gerenciamento_qualitativo = await service.update_gerenciamento_qualitativo(gerenciamento_qualitativo_id, gerenciamento_qualitativo)

        return gerenciamento_qualitativo

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete('/{gerenciamento_qualitativo_id}')
async def delete_gerenciamento_qualitativo(gerenciamento_qualitativo_id: int, service: Service_Qualitativo):
    try:
        result = await service.delete_gerenciamento_qualitativo(gerenciamento_qualitativo_id)

        return result

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))


@router.post('/Arquivo/{gerenciamento_meta_id}')
async def create_gerenciamento_meta_arquivo(service_arquivo: Service_Arquivo, validacao_service: Validacao_Arquivo, gerenciamento_qulitativo_id: int, fotos_projeto: list[UploadFile] = File(...), relatorios_parciais: list[UploadFile] = File(...)):
    try:
        nomes_fotos = [arquivo.filename for arquivo in fotos_projeto]
        nomes_relatorios = [arquivo.filename for arquivo in relatorios_parciais]

        validacao_service.validar_fotos_projeto(nomes_fotos)
        validacao_service.validar_relatorio_parcial(nomes_relatorios)

        fotos = [await ArquivoWrapper.from_upload_file(file) for file in fotos_projeto]
        relatorios = [await ArquivoWrapper.from_upload_file(file) for file in relatorios_parciais]

        fotos_metadados = await service_arquivo.create_gerenciamento_qualitativo_arquivo_fotos(gerenciamento_qualitativo_id=gerenciamento_qulitativo_id, arquivos=fotos)
        relatorios_metadados = await service_arquivo.create_gerenciamento_qualitativo_arquivo_relatorio(gerenciamento_qualitativo_id=gerenciamento_qulitativo_id, arquivos=relatorios)

        return fotos_metadados + relatorios_metadados

    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
