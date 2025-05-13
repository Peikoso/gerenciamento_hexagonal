from http import HTTPStatus

from fastapi import APIRouter, File, HTTPException, UploadFile

from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoMeta
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoMetaDTO
from gerenciamento_hexagonal.entrypoints.annotated import Service_Arquivo, Service_Meta, Validacao_Arquivo
from gerenciamento_hexagonal.entrypoints.arquivo_wrapper import ArquivoWrapper

router = APIRouter()


@router.get('/', response_model=list[GerenciamentoMeta])
async def get_gerenciamento_metas(service: Service_Meta):
    gerenciamento_meta = await service.get_gerenciamento_meta()

    return gerenciamento_meta


@router.get('/{gerenciamento_meta_id}', response_model=GerenciamentoMeta)
async def get_gerenciamento_meta_by_id(gerenciamento_meta_id: int, service: Service_Meta):
    try:
        gerenciamento_meta = await service.get_gerenciamento_meta_by_id(gerenciamento_meta_id)

        return gerenciamento_meta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.post('/{gerenciamento_proposta_id}', response_model=GerenciamentoMeta)
async def create_gerenciamento_meta(gerenciamento_proposta_id: int, gerenciamento_meta: GerenciamentoMetaDTO, service: Service_Meta):
    try:
        gerenciamento_meta = await service.create_gerenciamento_meta(gerenciamento_proposta_id, gerenciamento_meta)

        return gerenciamento_meta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.put('/{gerenciamento_meta_id}', response_model=GerenciamentoMeta)
async def update_gerenciamento_meta(gerenciamento_meta_id: int, gerenciamento_meta: GerenciamentoMetaDTO, service: Service_Meta):
    try:
        gerenciamento_meta = await service.update_gerenciamento_meta(gerenciamento_meta_id, gerenciamento_meta)

        return gerenciamento_meta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete('/{gerenciamento_meta_id}')
async def delete_gerenciamento_meta(gerenciamento_meta_id: int, service: Service_Meta):
    try:
        result = await service.delete_gerenciamento_meta(gerenciamento_meta_id)

        return result

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))


@router.post('/Arquivo/{gerenciamento_meta_id}')
async def create_gerenciamento_meta_arquivo(service_arquivo: Service_Arquivo, validacao_service: Validacao_Arquivo, gerenciamento_meta_id: int, gerenciamento_meta_arquivo: list[UploadFile] = File(...)):
    try:
        nomes_arquivos = [arquivo.filename for arquivo in gerenciamento_meta_arquivo]

        validacao_service.validar_arquivos_metas(nomes_arquivos)

        arquivos = [await ArquivoWrapper.from_upload_file(file) for file in gerenciamento_meta_arquivo]

        metadados = await service_arquivo.create_gerenciamento_meta_arquivo(gerenciamento_meta_id=gerenciamento_meta_id, arquivos=arquivos)

        return metadados

    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
