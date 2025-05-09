from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from gerenciamento_hexagonal.application.dependencies import get_arquivo_service
from gerenciamento_hexagonal.application.services.arquivo.gerenciamento_arquivo import GerenciamentoArquivoServices
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError

router = APIRouter()

Service_Arquivo = Annotated[GerenciamentoArquivoServices, Depends(get_arquivo_service)]


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
        result = await service.get_gerenciamento_arquivo_by_id(arquivo_id)

        return FileResponse(result.uri, headers={'Content-Disposition': 'attachment'})

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete('/{arquivo_id}')
async def delete_arquivo(arquivo_id: int, service: Service_Arquivo):
    try:
        result = await service.delete_arquivo(arquivo_id)
        return result

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
