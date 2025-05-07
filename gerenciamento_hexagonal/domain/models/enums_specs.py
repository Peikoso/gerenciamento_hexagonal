from enum import Enum


class TipoArquivoContexto(str, Enum):
    PROPONENTE = 'PROPONENTE'
    PROJETO = 'PROJETO'
    DADOS_BANCARIOS = 'DADOS_BANCARIOS'
    EDITAL = 'EDITAL'
    GERENCIAMENTO_META = 'GERENCIAMENTO_META'
    GERENCIAMENTO_QUALITATIVO = 'GERENCIAMENTO_QUALITATIVO'
    GERENCIAMENTO_CONTRAPARTIDA = 'GERENCIAMENTO_CONTRAPARTIDA'


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
