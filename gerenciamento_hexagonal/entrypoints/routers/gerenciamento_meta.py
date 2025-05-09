from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from gerenciamento_hexagonal.application.dependencies import get_arquivo_service, get_gerenciamento_meta_service, get_validacao_arquivo_service
from gerenciamento_hexagonal.application.services.gerenciamento.meta import GerenciamentoMetaServices
from gerenciamento_hexagonal.application.services.arquivo.arquivo_service import ValidacaoArquivoService
from gerenciamento_hexagonal.application.services.arquivo.gerenciamento_arquivo import GerenciamentoArquivoServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoMeta
from gerenciamento_hexagonal.domain.models.gerenciamentoDTO_Response import GerenciamentoMetaDTO

router = APIRouter()


Service = Annotated[GerenciamentoMetaServices, Depends(get_gerenciamento_meta_service)]
Service_Arquivo = Annotated[GerenciamentoArquivoServices, Depends(get_arquivo_service)]
Validacao_Arquivo = Annotated[ValidacaoArquivoService, Depends(get_validacao_arquivo_service)]


@router.get('/', response_model=list[GerenciamentoMeta])
async def get_gerenciamento_metas(service: Service):
    gerenciamento_meta = await service.get_gerenciamento_meta()

    return gerenciamento_meta


@router.get('/{gerenciamento_meta_id}', response_model=GerenciamentoMeta)
async def get_gerenciamento_meta_by_id(gerenciamento_meta_id: int, service: Service):
    try:
        gerenciamento_meta = await service.get_gerenciamento_meta_by_id(gerenciamento_meta_id)

        return gerenciamento_meta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.post('/{gerenciamento_proposta_id}', response_model=GerenciamentoMeta)
async def create_gerenciamento_meta(gerenciamento_proposta_id: int, gerenciamento_meta: GerenciamentoMetaDTO, service: Service):
    try:
        gerenciamento_meta = await service.create_gerenciamento_meta(gerenciamento_proposta_id, gerenciamento_meta)

        return gerenciamento_meta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.put('/{gerenciamento_meta_id}', response_model=GerenciamentoMeta)
async def update_gerenciamento_meta(gerenciamento_meta_id: int, gerenciamento_meta: GerenciamentoMetaDTO, service: Service):
    try:
        gerenciamento_meta = await service.update_gerenciamento_meta(gerenciamento_meta_id, gerenciamento_meta)

        return gerenciamento_meta

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete('/{gerenciamento_meta_id}')
async def delete_gerenciamento_meta(gerenciamento_meta_id: int, service: Service):
    try:
        result = await service.delete_gerenciamento_meta(gerenciamento_meta_id)

        return result

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


class ArquivoWrapper:
    def __init__(self, filename: str, content: bytes):
        self.filename = filename
        self.content = content

    @classmethod
    async def from_upload_file(cls, file: UploadFile):
        content = await file.read()  # Assíncrono!
        return cls(filename=file.filename, content=content)


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
