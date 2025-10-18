import pytest
from datetime import date, datetime, timezone
from pydantic import ValidationError

from gerenciamento_hexagonal.domain.models.gerenciamento import (
    GerenciamentoComentario,
    GerenciamentoProposta,
    GerenciamentoMeta,
    GerenciamentoQuantitativo,
    GerenciamentoQualitativo,
    GerenciamentoCaracterizacao,
    GerenciamentoBeneficiarioCategorizacao,
    GerenciamentoContrapartida,
    GerenciamentoContrapartidaAdmin,
)

from gerenciamento_hexagonal.domain.models.enums_specs import (
    StatusGereciamentoContrapartida,
    TipoGerenciamento
)


# ==================== GerenciamentoComentario ====================
def test_gerenciamento_comentario_criacao():
    comentario = GerenciamentoComentario(comentario="Comentário teste")
    assert comentario.comentario == "Comentário teste"
    assert comentario.id is None
    assert isinstance(comentario.data_cricao, datetime)

# ==================== GerenciamentoProposta ====================
def test_gerenciamento_proposta_criacao():
    proposta = GerenciamentoProposta(
        proposta_id=1,
        trimestre_de_referencia=date(2025, 10, 18),
        tipo=TipoGerenciamento.TRIMESTRAL
    )
    assert proposta.proposta_id == 1
    assert proposta.tipo == TipoGerenciamento.TRIMESTRAL
    assert isinstance(proposta.criado_em, datetime)
    assert proposta.metas_comentarios == []
    assert proposta.arquivos_ids == []

# ==================== GerenciamentoMeta ====================
def test_gerenciamento_meta_criacao():
    meta = GerenciamentoMeta(alcancado=10)
    assert meta.alcancado == 10
    assert meta.ordem is None
    assert meta.arquivos_ids == []

# ==================== GerenciamentoQuantitativo ====================
def test_gerenciamento_quantitativo_criacao():
    quantitativo = GerenciamentoQuantitativo(
        educacao_financeira_impactados=100,
        educacao_financeira_alcancados=80,
        geracao_renda_postos_trabalho_gerados=5,
        alcance_marca_pessoas_alcancadas_publicacao_digitais=200,
        pessoas_alcancadas=150,
        pessoas_impactadas=150
    )
    assert quantitativo.educacao_financeira_impactados == 100
    assert quantitativo.comentarios == []

# ==================== GerenciamentoQualitativo ====================
def test_gerenciamento_qualitativo_criacao():
    qualitativo = GerenciamentoQualitativo()
    assert qualitativo.acoes_realizadas is None
    assert qualitativo.comentarios == []
    assert qualitativo.arquivos_ids == []

# ==================== GerenciamentoCaracterizacao ====================
def test_gerenciamento_caracterizacao_criacao():
    caracterizacao = GerenciamentoCaracterizacao(
        quantidade=5,
        categorizacoes_ids=[1,2,3]
    )
    assert caracterizacao.quantidade == 5
    assert caracterizacao.categorizacoes_ids == [1,2,3]

# ==================== GerenciamentoBeneficiarioCategorizacao ====================
def test_gerenciamento_beneficiario_categorizacao_criacao():
    beneficiario = GerenciamentoBeneficiarioCategorizacao(
        gerenciamento_id=1,
        categorizacoes_ids=[10,20]
    )
    assert beneficiario.gerenciamento_id == 1
    assert beneficiario.categorizacoes_ids == [10,20]

# ==================== GerenciamentoContrapartida ====================
def test_gerenciamento_contrapartida_criacao():
    contrapartida = GerenciamentoContrapartida(
        proposta_contrapartida_id=1,
        quantidade=5,
        observacao="Obs teste",
        data=date(2025,10,18),
        status=StatusGereciamentoContrapartida.PLANEJADO
    )
    assert contrapartida.quantidade == 5
    assert contrapartida.arquivos_ids == []

# ==================== GerenciamentoContrapartidaAdmin ====================
def test_gerenciamento_contrapartida_admin_criacao():
    admin = GerenciamentoContrapartidaAdmin(
        quantidade=3,
        justificativa="Justificativa teste",
        data=date(2025,10,18)
    )
    assert admin.quantidade == 3
    assert admin.justificativa == "Justificativa teste"
