from http import HTTPStatus

from fastapi import APIRouter, File, HTTPException, UploadFile

from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoContrapartida
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoContrapartidaDTO
from gerenciamento_hexagonal.entrypoints.annotated import Service_Arquivo, Service_Contrapartida, Validacao_Arquivo
from gerenciamento_hexagonal.entrypoints.arquivo_wrapper import ArquivoWrapper

router = APIRouter()


@router.get('/', response_model=list[GerenciamentoContrapartida])
async def get_gerenciamento_contrapartidas(service: Service_Contrapartida):
    gerenciamento_contrapartida = await service.get_gerenciamento_contrapartida()

    return gerenciamento_contrapartida


@router.get('/{gerenciamento_contrapartida_id}', response_model=GerenciamentoContrapartida)
async def get_gerenciamento_contrapartida_by_id(gerenciamento_contrapartida_id: int, service: Service_Contrapartida):
    try:
        gerenciamento_contrapartida = await service.get_gerenciamento_contrapartida_by_id(gerenciamento_contrapartida_id)

        return gerenciamento_contrapartida

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.post('/{gerenciamento_proposta_id}', response_model=GerenciamentoContrapartida)
async def create_gerenciamento_contrapartida(gerenciamento_proposta_id: int, gerenciamento_contrapartida: GerenciamentoContrapartidaDTO, service: Service_Contrapartida):
    try:
        gerenciamento_contrapartida = await service.create_gerenciamento_contrapartida(gerenciamento_proposta_id, gerenciamento_contrapartida)

        return gerenciamento_contrapartida

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.put('/{gerenciamento_contrapartida_id}', response_model=GerenciamentoContrapartida)
async def update_gerenciamento_contrapartida(gerenciamento_contrapartida_id: int, gerenciamento_contrapartida: GerenciamentoContrapartidaDTO, service: Service_Contrapartida):
    try:
        gerenciamento_contrapartida = await service.update_gerenciamento_contrapartida(gerenciamento_contrapartida_id, gerenciamento_contrapartida)

        return gerenciamento_contrapartida

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete('/{gerenciamento_contrapartida_id}')
async def delete_gerenciamento_contrapartida(gerenciamento_contrapartida_id: int, service: Service_Contrapartida):
    try:
        result = await service.delete_gerenciamento_contrapartida(gerenciamento_contrapartida_id)

        return result

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))


@router.post('/Arquivo/{gerenciamento_contrapartida_id}')
async def create_gerenciamento_contrapartida_arquivo(service_arquivo: Service_Arquivo, validacao_service: Validacao_Arquivo, gerenciamento_contrapartida_id: int, gerenciamento_meta_arquivo: list[UploadFile] = File(...)):
    try:
        nomes_arquivos = [arquivo.filename for arquivo in gerenciamento_meta_arquivo]

        validacao_service.validar_comprovacao_contrapartida(nomes_arquivos)

        arquivos = [await ArquivoWrapper.from_upload_file(file) for file in gerenciamento_meta_arquivo]

        metadados = await service_arquivo.create_gerenciamento_contrapartida_arquivo(gerenciamento_contrapartida_id=gerenciamento_contrapartida_id, arquivos=arquivos)
        return metadados

    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
