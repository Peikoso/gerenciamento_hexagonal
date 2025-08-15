from typing import Optional

from pydantic import BaseModel


class Arquivo(BaseModel):
    tipo_arquivo_id: str
    nome: str
    extensao: str
    tamanho: int
    uri: str
    arquivo_id: Optional[int] = None
