from http import HTTPStatus

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.entrypoints.annotated import Service_Arquivo, Validacao_Arquivo
from gerenciamento_hexagonal.entrypoints.arquivo_wrapper import ArquivoWrapper

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


@router.post('/Qualitativo/{gerenciamento_qualitativo_id}')
async def create_gerenciamento_qualitativo_arquivo(service_arquivo: Service_Arquivo, validacao_service: Validacao_Arquivo, gerenciamento_qualitativo_id: int, fotos_projeto: list[UploadFile] = File(...), relatorios_parciais: list[UploadFile] = File(...)):
    try:
        nomes_fotos = [arquivo.filename for arquivo in fotos_projeto]
        nomes_relatorios = [arquivo.filename for arquivo in relatorios_parciais]

        validacao_service.validar_fotos_projeto(nomes_fotos)
        validacao_service.validar_relatorio_parcial(nomes_relatorios)

        fotos = [await ArquivoWrapper.from_upload_file(file) for file in fotos_projeto]
        relatorios = [await ArquivoWrapper.from_upload_file(file) for file in relatorios_parciais]

        fotos_metadados = await service_arquivo.create_gerenciamento_qualitativo_arquivo_fotos(gerenciamento_qualitativo_id=gerenciamento_qualitativo_id, arquivos=fotos)
        relatorios_metadados = await service_arquivo.create_gerenciamento_qualitativo_arquivo_relatorio(gerenciamento_qualitativo_id=gerenciamento_qualitativo_id, arquivos=relatorios)

        return fotos_metadados + relatorios_metadados

    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.post('/Contrapartida/{gerenciamento_contrapartida_id}')
async def create_gerenciamento_contrapartida_arquivo(service_arquivo: Service_Arquivo, validacao_service: Validacao_Arquivo, gerenciamento_contrapartida_id: int, gerenciamento_meta_arquivo: list[UploadFile] = File(...)):
    try:
        nomes_arquivos = [arquivo.filename for arquivo in gerenciamento_meta_arquivo]

        validacao_service.validar_comprovacao_contrapartida(nomes_arquivos)

        arquivos = [await ArquivoWrapper.from_upload_file(file) for file in gerenciamento_meta_arquivo]

        metadados = await service_arquivo.create_gerenciamento_contrapartida_arquivo(gerenciamento_contrapartida_id=gerenciamento_contrapartida_id, arquivos=arquivos)
        return metadados

    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
