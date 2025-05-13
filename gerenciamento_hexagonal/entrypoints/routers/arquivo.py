from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.entrypoints.annotated import Service_Arquivo

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
