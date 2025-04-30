from typing import Optional

from pydantic import BaseModel


class TipoCategorizacaoBeneficiario(BaseModel):
    descricao: str
    info: str
    id: Optional[int] = None


class CategorizacaoBeneficiario(BaseModel):
    tipo_categ_beneficiario_id: int
    valor = str
    id: Optional[int] = None
