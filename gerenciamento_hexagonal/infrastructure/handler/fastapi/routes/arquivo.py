from http import HTTPStatus

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import DomainValidationError, NotFoundError
from gerenciamento_hexagonal.infrastructure.handler.fastapi.annotated import Service_Arquivo
from gerenciamento_hexagonal.infrastructure.handler.fastapi.arquivo_wrapper import ArquivoWrapper

router = APIRouter()


@router.get('/{arquivo_id}')
async def get_arquivo_by_id(arquivo_id: int, service: Service_Arquivo):
    try:
        result = await service.get_gerenciamento_arquivo_by_id(arquivo_id)

        return result

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.get('/download/{arquivo_id}')
async def download_arquivo_by_id(arquivo_id: int, service: Service_Arquivo):
    try:
        result = await service.get_gerenciamento_arquivo_download_by_id(arquivo_id)

        return FileResponse(result, headers={'Content-Disposition': 'attachment'})

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete('/{arquivo_id}')
async def delete_arquivo(arquivo_id: int, service: Service_Arquivo):
    try:
        result = await service.delete_arquivo(arquivo_id)
        return result

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.post('/Meta/{gerenciamento_meta_id}')
async def create_gerenciamento_meta_arquivo(service_arquivo: Service_Arquivo, gerenciamento_meta_id: int, gerenciamento_meta_arquivo: list[UploadFile] = File(...)):
    try:
        arquivos = [await ArquivoWrapper.from_upload_file(file) for file in gerenciamento_meta_arquivo]

        metadados = await service_arquivo.create_gerenciamento_meta_arquivo(gerenciamento_meta_id=gerenciamento_meta_id, arquivos=arquivos)

        return metadados

    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except DomainValidationError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))


@router.post('/Qualitativo/{gerenciamento_qualitativo_id}')
async def create_gerenciamento_qualitativo_arquivo(service_arquivo: Service_Arquivo, gerenciamento_qualitativo_id: int, fotos_projeto: list[UploadFile] = File(...), relatorios_parciais: list[UploadFile] = File(...)):
    try:
        fotos = [await ArquivoWrapper.from_upload_file(file) for file in fotos_projeto]
        relatorios = [await ArquivoWrapper.from_upload_file(file) for file in relatorios_parciais]

        metadados = await service_arquivo.create_gerenciamento_qualitativo_arquivo(gerenciamento_qualitativo_id=gerenciamento_qualitativo_id, fotos=fotos, relatorios=relatorios)

        return metadados

    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except DomainValidationError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))


@router.post('/Contrapartida/{gerenciamento_contrapartida_id}')
async def create_gerenciamento_contrapartida_arquivo(service_arquivo: Service_Arquivo, gerenciamento_contrapartida_id: int, gerenciamento_contrapartida_arquivo: list[UploadFile] = File(...)):
    try:
        arquivos = [await ArquivoWrapper.from_upload_file(file) for file in gerenciamento_contrapartida_arquivo]

        metadados = await service_arquivo.create_gerenciamento_contrapartida_arquivo(gerenciamento_contrapartida_id=gerenciamento_contrapartida_id, arquivos=arquivos)
        return metadados

    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except DomainValidationError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))
