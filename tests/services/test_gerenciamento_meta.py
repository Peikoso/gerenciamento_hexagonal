import pytest
from unittest.mock import AsyncMock, MagicMock
from gerenciamento_hexagonal.application.services.gerenciamento.meta import GerenciamentoMetaServicesImpl
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError
from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoMeta
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoMetaDTO

pytestmark = pytest.mark.asyncio

@pytest.fixture
def service():
    # Cria mocks para repository e verify
    repository_mock = MagicMock()
    repository_mock.get_gerenciamento_meta = AsyncMock()
    repository_mock.get_gerenciamento_meta_by_id = AsyncMock()
    repository_mock.create_gerenciamento_meta = AsyncMock()
    repository_mock.update_gerenciamento_meta = AsyncMock()
    repository_mock.delete_gerenciamento_meta = AsyncMock()

    verify_mock = MagicMock()
    verify_mock.gerencimento_proposta_exists = AsyncMock()

    # Passa os mocks para o construtor
    svc = GerenciamentoMetaServicesImpl(repository=repository_mock, verify=verify_mock)
    return svc

async def test_get_gerenciamento_meta(mocker, service):
    mock_data = [GerenciamentoMeta(id=1, alcancado=10, ordem=1, arquivos_ids=[])]
    mocker.patch.object(service, 'repository', create=True)
    service.repository.get_gerenciamento_meta = mocker.AsyncMock(return_value=mock_data)

    result = await service.get_gerenciamento_meta()
    assert result == mock_data
    service.repository.get_gerenciamento_meta.assert_awaited_once()

async def test_get_gerenciamento_meta_by_id_found(mocker, service):
    mock_meta = GerenciamentoMeta(id=1, alcancado=10, ordem=1, arquivos_ids=[])
    mocker.patch.object(service, 'repository', create=True)
    service.repository.get_gerenciamento_meta_by_id = mocker.AsyncMock(return_value=mock_meta)

    result = await service.get_gerenciamento_meta_by_id(1)
    assert result == mock_meta
    service.repository.get_gerenciamento_meta_by_id.assert_awaited_once_with(1)

async def test_get_gerenciamento_meta_by_id_not_found(mocker, service):
    mocker.patch.object(service, 'repository', create=True)
    service.repository.get_gerenciamento_meta_by_id = mocker.AsyncMock(return_value=None)

    with pytest.raises(NotFoundError):
        await service.get_gerenciamento_meta_by_id(999)

async def test_create_gerenciamento_meta(mocker, service):
    dto = GerenciamentoMetaDTO(alcancado=5, ordem=1)
    created_meta = GerenciamentoMeta(id=1, alcancado=5, ordem=1, arquivos_ids=[])

    mocker.patch.object(service, 'repository', create=True)
    mocker.patch.object(service, 'verify', create=True)
    service.repository.create_gerenciamento_meta = mocker.AsyncMock(return_value=created_meta)
    service.verify.gerencimento_proposta_exists = mocker.AsyncMock()

    result = await service.create_gerenciamento_meta(1, dto)
    assert result == created_meta
    service.verify.gerencimento_proposta_exists.assert_awaited_once_with(1)
    service.repository.create_gerenciamento_meta.assert_awaited_once()

async def test_update_gerenciamento_meta(mocker, service):
    dto = GerenciamentoMetaDTO(alcancado=20, ordem=2)
    existing_meta = GerenciamentoMeta(id=1, alcancado=10, ordem=1, arquivos_ids=[])
    updated_meta = GerenciamentoMeta(id=1, alcancado=20, ordem=2, arquivos_ids=[])

    mocker.patch.object(service, 'repository', create=True)
    service.repository.update_gerenciamento_meta = mocker.AsyncMock(return_value=updated_meta)
    service.get_gerenciamento_meta_by_id = mocker.AsyncMock(return_value=existing_meta)

    result = await service.update_gerenciamento_meta(1, dto)
    assert result == updated_meta
    service.repository.update_gerenciamento_meta.assert_awaited_once()

async def test_delete_gerenciamento_meta_success(mocker, service):
    meta = GerenciamentoMeta(id=1, alcancado=10, ordem=1, arquivos_ids=[])
    mocker.patch.object(service, 'repository', create=True)
    service.repository.delete_gerenciamento_meta = mocker.AsyncMock()
    service.get_gerenciamento_meta_by_id = mocker.AsyncMock(return_value=meta)

    result = await service.delete_gerenciamento_meta(1)
    assert result['message'] == 'gerenciamento_meta with ID 1 deleted'
    service.repository.delete_gerenciamento_meta.assert_awaited_once_with(1)

async def test_delete_gerenciamento_meta_with_files(mocker, service):
    meta = GerenciamentoMeta(id=1, alcancado=10, ordem=1, arquivos_ids=[101, 102])
    service.get_gerenciamento_meta_by_id = mocker.AsyncMock(return_value=meta)

    with pytest.raises(ValueError) as exc:
        await service.delete_gerenciamento_meta(1)
    assert 'cannot be deleted because it has associated files' in str(exc.value)
