import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException
from datetime import date, datetime
from gerenciamento_hexagonal.domain.models.gerenciamento import TipoGerenciamento, GerenciamentoProposta, GerenciamentoComentario
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import GerenciamentoPropostaDTO, GerenciamentoComentarioDTO, GerenciamentoPropostaResponse
from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import NotFoundError, DomainValidationError, NotNullViolationError
from gerenciamento_hexagonal.infrastructure.handler.fastapi.routes import gerenciamento_proposta


@pytest.mark.asyncio
async def test_create_gerenciamento_proposta_success():
    mock_service = AsyncMock()
    dto = GerenciamentoPropostaDTO(trimestre_de_referencia=date(2025, 10, 1), tipo=TipoGerenciamento.TRIMESTRAL, proposta_id=1)
    response = GerenciamentoPropostaResponse(id=1, trimestre_de_referencia=date(2025, 10, 1), tipo=TipoGerenciamento.TRIMESTRAL, proposta_id=1, criado_em=datetime.now())

    mock_service.create_gerenciamento_proposta.return_value = response

    result = await gerenciamento_proposta.create_gerenciamento_proposta(dto, service=mock_service)

    assert result == response
    mock_service.create_gerenciamento_proposta.assert_awaited_once_with(dto)


@pytest.mark.asyncio
async def test_create_gerenciamento_proposta_comentario_not_found():
    mock_service = AsyncMock()
    dto = GerenciamentoComentarioDTO(comentario="Teste")
    mock_service.create_gerenciamento_proposta_comentario.side_effect = NotFoundError("Not found")

    with pytest.raises(HTTPException) as exc:
        await gerenciamento_proposta.create_gerenciamento_propostaComentario(1, dto, service=mock_service)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Not found"


@pytest.mark.asyncio
async def test_create_gerenciamento_proposta_comentario_domain_validation():
    mock_service = AsyncMock()
    dto = GerenciamentoComentarioDTO(comentario="Teste")
    mock_service.create_gerenciamento_proposta_comentario.side_effect = DomainValidationError("Invalid")

    with pytest.raises(HTTPException) as exc:
        await gerenciamento_proposta.create_gerenciamento_propostaComentario(1, dto, service=mock_service)

    assert exc.value.status_code == 422
    assert exc.value.detail == "Invalid"


@pytest.mark.asyncio
async def test_get_gerenciamento_propostas():
    mock_service = AsyncMock()
    response = [GerenciamentoPropostaResponse(id=1, trimestre_de_referencia=date(2025, 10, 1), tipo=TipoGerenciamento.TRIMESTRAL, proposta_id=1, criado_em=datetime.now())]
    mock_service.get_gerenciamento_proposta.return_value = response

    result = await gerenciamento_proposta.get_gerencimentoPropostas(service=mock_service)

    assert result == response
    mock_service.get_gerenciamento_proposta.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_gerenciamento_proposta_by_id_success():
    mock_service = AsyncMock()
    response = GerenciamentoProposta(id=1, trimestre_de_referencia=date(2025, 10, 1), tipo=TipoGerenciamento.TRIMESTRAL, proposta_id=1)
    mock_service.get_gerenciamento_proposta_by_id.return_value = response

    result = await gerenciamento_proposta.get_by_id_gerenciamento_proposta(1, service=mock_service)

    assert result == response
    mock_service.get_gerenciamento_proposta_by_id.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_get_gerenciamento_proposta_by_id_not_found():
    mock_service = AsyncMock()
    mock_service.get_gerenciamento_proposta_by_id.side_effect = NotFoundError("Not found")

    with pytest.raises(HTTPException) as exc:
        await gerenciamento_proposta.get_by_id_gerenciamento_proposta(1, service=mock_service)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Not found"


@pytest.mark.asyncio
async def test_update_gerenciamento_proposta_success():
    mock_service = AsyncMock()
    dto = GerenciamentoPropostaDTO(trimestre_de_referencia=date(2025, 10, 1), tipo=TipoGerenciamento.TRIMESTRAL, proposta_id=1)
    response = GerenciamentoPropostaResponse(id=1, trimestre_de_referencia=date(2025, 10, 1), tipo=TipoGerenciamento.TRIMESTRAL, proposta_id=1, criado_em=datetime.now())
    mock_service.update_gerenciamento_proposta.return_value = response

    result = await gerenciamento_proposta.update_gerenciamento_proposta(1, dto, service=mock_service)

    assert result == response
    mock_service.update_gerenciamento_proposta.assert_awaited_once_with(1, dto)


@pytest.mark.asyncio
async def test_update_gerenciamento_proposta_not_found():
    mock_service = AsyncMock()
    dto = GerenciamentoPropostaDTO(trimestre_de_referencia=date(2025, 10, 1), tipo=TipoGerenciamento.TRIMESTRAL, proposta_id=1)
    mock_service.update_gerenciamento_proposta.side_effect = NotFoundError("Not found")

    with pytest.raises(HTTPException) as exc:
        await gerenciamento_proposta.update_gerenciamento_proposta(1, dto, service=mock_service)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Not found"


@pytest.mark.asyncio
async def test_delete_gerenciamento_proposta_success():
    mock_service = AsyncMock()
    mock_service.delete_gerenciamento_proposta.return_value = {"deleted": True}

    result = await gerenciamento_proposta.delete_gerenciamento_proposta(1, service=mock_service)

    assert result == {"deleted": True}
    mock_service.delete_gerenciamento_proposta.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_delete_gerenciamento_proposta_not_found():
    mock_service = AsyncMock()
    mock_service.delete_gerenciamento_proposta.side_effect = NotFoundError("Not found")

    with pytest.raises(HTTPException) as exc:
        await gerenciamento_proposta.delete_gerenciamento_proposta(1, service=mock_service)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Not found"


@pytest.mark.asyncio
async def test_delete_gerenciamento_proposta_not_null_violation():
    mock_service = AsyncMock()
    mock_service.delete_gerenciamento_proposta.side_effect = NotNullViolationError("Conflict")

    with pytest.raises(HTTPException) as exc:
        await gerenciamento_proposta.delete_gerenciamento_proposta(1, service=mock_service)

    assert exc.value.status_code == 409
    assert exc.value.detail == "Conflict"
