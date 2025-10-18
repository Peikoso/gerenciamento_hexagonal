import pytest
from unittest.mock import AsyncMock, patch
from datetime import date, datetime

from gerenciamento_hexagonal.domain.models.gerenciamento import GerenciamentoProposta, TipoGerenciamento
from gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.gerenciamento.proposta import GerenciamentoPropostaRepository
from gerenciamento_hexagonal.domain.repositories.gerenciamento import GerenciamentoComentarioRepository

@pytest.mark.asyncio
async def test_create_gerenciamento_proposta():
    mock_comentario_repo = AsyncMock(spec=GerenciamentoComentarioRepository)

    # Context manager mock
    mock_session = AsyncMock()
    mock_ctx_manager = AsyncMock()
    mock_ctx_manager.__aenter__.return_value = mock_session
    mock_ctx_manager.__aexit__.return_value = None

    with patch(
        "gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.gerenciamento.proposta.get_session",
        return_value=mock_ctx_manager
    ):
        repo = GerenciamentoPropostaRepository(mock_comentario_repo)

        proposta = GerenciamentoProposta(
            trimestre_de_referencia=date(2025, 10, 1),
            tipo=TipoGerenciamento.TRIMESTRAL,
            proposta_id=1
        )

        db_model_mock = AsyncMock()
        db_model_mock.id = 1
        db_model_mock.trimestre_de_referencia = proposta.trimestre_de_referencia
        db_model_mock.tipo = proposta.tipo
        db_model_mock.proposta_id = proposta.proposta_id
        db_model_mock.criado_em = datetime.now()

        with patch(
            "gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.gerenciamento.proposta.GerenciamentoPropostaModel",
            return_value=db_model_mock
        ):
            result = await repo.create_gerenciamento_proposta(proposta)

        assert result.id == 1
        assert result.trimestre_de_referencia == proposta.trimestre_de_referencia
        assert result.tipo == proposta.tipo
        assert result.proposta_id == proposta.proposta_id
        mock_session.add.assert_called_once_with(db_model_mock)
        mock_session.commit.assert_awaited_once()
        mock_session.refresh.assert_awaited_once_with(db_model_mock)

@pytest.mark.asyncio
async def test_update_gerenciamento_proposta():
    mock_comentario_repo = AsyncMock(spec=GerenciamentoComentarioRepository)
    mock_session = AsyncMock()
    mock_ctx_manager = AsyncMock()
    mock_ctx_manager.__aenter__.return_value = mock_session
    mock_ctx_manager.__aexit__.return_value = None

    with patch("gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.gerenciamento.proposta.get_session", return_value=mock_ctx_manager):
        repo = GerenciamentoPropostaRepository(mock_comentario_repo)

        proposta = GerenciamentoProposta(
            trimestre_de_referencia=date(2025, 10, 1),
            tipo=TipoGerenciamento.TRIMESTRAL,
            proposta_id=1
        )

        db_model_mock = AsyncMock()
        db_model_mock.id = 1
        db_model_mock.trimestre_de_referencia = proposta.trimestre_de_referencia
        db_model_mock.tipo = proposta.tipo
        db_model_mock.proposta_id = proposta.proposta_id
        db_model_mock.criado_em = datetime.now()

        mock_session.scalar.return_value = db_model_mock

        result = await repo.update_gerenciamento_proposta(1, proposta)

        assert result.id == 1
        assert result.trimestre_de_referencia == proposta.trimestre_de_referencia
        mock_session.commit.assert_awaited_once()
        mock_session.refresh.assert_awaited_once_with(db_model_mock)

@pytest.mark.asyncio
async def test_delete_gerenciamento_proposta():
    mock_comentario_repo = AsyncMock(spec=GerenciamentoComentarioRepository)
    mock_session = AsyncMock()
    mock_ctx_manager = AsyncMock()
    mock_ctx_manager.__aenter__.return_value = mock_session
    mock_ctx_manager.__aexit__.return_value = None

    with patch("gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.gerenciamento.proposta.get_session", return_value=mock_ctx_manager):
        repo = GerenciamentoPropostaRepository(mock_comentario_repo)

        db_model_mock = AsyncMock()
        mock_session.scalar.return_value = db_model_mock

        await repo.delete_gerenciamento_proposta(1)

        mock_session.delete.assert_awaited_once_with(db_model_mock)
        mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_gerenciamento_proposta_by_id():
    mock_comentario_repo = AsyncMock(spec=GerenciamentoComentarioRepository)
    mock_session = AsyncMock()
    mock_ctx_manager = AsyncMock()
    mock_ctx_manager.__aenter__.return_value = mock_session
    mock_ctx_manager.__aexit__.return_value = None

    with patch("gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.gerenciamento.proposta.get_session", return_value=mock_ctx_manager):
        repo = GerenciamentoPropostaRepository(mock_comentario_repo)

        db_model_mock = AsyncMock()
        db_model_mock.id = 1
        db_model_mock.trimestre_de_referencia = date(2025, 10, 1)
        db_model_mock.tipo = TipoGerenciamento.TRIMESTRAL
        db_model_mock.proposta_id = 1
        db_model_mock.metas_comentarios = []

        mock_session.scalar.return_value = db_model_mock

        result = await repo.get_gerenciamento_proposta_by_id(1)

        assert result.id == 1
        assert result.trimestre_de_referencia == db_model_mock.trimestre_de_referencia

@pytest.mark.asyncio
async def test_checar_gerenciamento_caracterizacao_exists_true():
    mock_comentario_repo = AsyncMock(spec=GerenciamentoComentarioRepository)
    mock_session = AsyncMock()
    mock_ctx_manager = AsyncMock()
    mock_ctx_manager.__aenter__.return_value = mock_session
    mock_ctx_manager.__aexit__.return_value = None

    with patch("gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.gerenciamento.proposta.get_session", return_value=mock_ctx_manager):
        repo = GerenciamentoPropostaRepository(mock_comentario_repo)

        # Simula encontrar quantitativo e caracterizacao
        mock_session.scalar.side_effect = [AsyncMock(id=1), AsyncMock()]

        result = await repo.checar_gerenciamento_caracterizacao_exists(1)
        assert result is True

@pytest.mark.asyncio
async def test_checar_gerenciamento_caracterizacao_exists_false():
    mock_comentario_repo = AsyncMock(spec=GerenciamentoComentarioRepository)
    mock_session = AsyncMock()
    mock_ctx_manager = AsyncMock()
    mock_ctx_manager.__aenter__.return_value = mock_session
    mock_ctx_manager.__aexit__.return_value = None

    with patch("gerenciamento_hexagonal.infrastructure.repositories.sqlalchemy.gerenciamento.proposta.get_session", return_value=mock_ctx_manager):
        repo = GerenciamentoPropostaRepository(mock_comentario_repo)

        # Simula não encontrar quantitativo
        mock_session.scalar.return_value = None

        result = await repo.checar_gerenciamento_caracterizacao_exists(1)
        assert result is False
