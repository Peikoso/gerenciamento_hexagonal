from typing import Optional

from pydantic import BaseModel

from gerenciamento_hexagonal.domain.models.enums_specs import TipoArquivoContexto


class TipoArquivo(BaseModel):
    id: str
    contexto: TipoArquivoContexto
    descricao: str
    info: str


class Arquivo(BaseModel):
    tipo_arquivo_id: str
    nome: str
    extensao: str
    tamanho: int
    uri: str
    arquivo_id: Optional[int] = None
