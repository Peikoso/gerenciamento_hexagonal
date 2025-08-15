from enum import Enum


class TipoGerenciamentoArquivo(str, Enum):
    gerenciamento_meta = ('REGISTRO_DA_META',)
    gerenciamento_qualitativo_fotos_do_projeto = ('FOTOS_DO_PROJETO',)
    gerenciamento_qualitativo_relatorio_parcial = ('RELATORIO_PARCIAL',)
    gerenciamento_contrapartida = 'COMPROVACAO_DA_CONTRAPARTIDA'


class TipoGerenciamento(str, Enum):
    TRIMESTRAL = 'TRIMESTRAL'
    FINAL = 'FINAL'


class StatusGereciamentoContrapartida(str, Enum):
    PLANEJADO = 'Planejado'
    EM_APROVACAO = 'Em aprovação'
    EM_AJUSTE = 'Em ajuste'
    ENTREGUE = 'Entregue'
    JUSTIFICADA = 'Justificada'
    NAO_ENTREGUE = 'Não entregue'


class GerenciamentoBeneficiarioCategorizacaoSpec:
    MODEL_NAME = 'gerenciamento_beneficiario_categorizacao'
    FIELD_GERENCIAMENTO_BENEFICIARIO = 'gerenciamento_beneficiario_id'
    FIELD_CATEGORIZACAO = 'categorizacao_id'
    CONSTRAINT_GERENCIAMENTO_BENEFICIARIO_CATEGORIZACAO_UQ = 'gerenciamento_beneficiario_categorizacao_uq'
