from abc import ABC, abstractmethod

from gerenciamento_hexagonal.domain.models.arquivo import Arquivo
from gerenciamento_hexagonal.domain.models.gerenciamento import (
    GerenciamentoCaracterizacao,
    GerenciamentoComentario,
    GerenciamentoContrapartida,
    GerenciamentoContrapartidaAdmin,
    GerenciamentoContrapartidaArquivo,
    GerenciamentoMeta,
    GerenciamentoMetaArquivo,
    GerenciamentoProposta,
    GerenciamentoQualitativo,
    GerenciamentoQualitativoArquivo,
    GerenciamentoQuantitativo,
    # GerenciamentoMetaArquivo,
    # GerenciamentoContrapartidaArquivo,
    # GerenciamentoQualitativoArquivo,
)


class GerenciamentoComentarioRepository(ABC):
    @abstractmethod
    async def get_gerenciamento_comentario(self) -> list[GerenciamentoComentario]:
        pass

    @abstractmethod
    async def get_gerenciamento_comentario_by_id(self, gerenciamento_comentario_id: int) -> GerenciamentoComentario | None:
        pass

    @abstractmethod
    async def create_gerenciamento_comentario(self, gerenciamento_comentario: GerenciamentoComentario) -> GerenciamentoComentario:
        pass

    @abstractmethod
    async def update_gerenciamento_comentario(self, gerenciamento_comentario_id: int, gerenciamento_comentario: GerenciamentoComentario) -> GerenciamentoComentario:
        pass

    @abstractmethod
    async def delete_gerenciamento_comentario(self, gerenciamento_comentario_id: int):
        pass


class GerenciamentoPropostaRepository(ABC):
    @abstractmethod
    async def get_gerenciamento_proposta(self) -> list[GerenciamentoProposta]:
        pass

    @abstractmethod
    async def get_gerenciamento_proposta_by_id(self, gerenciamento_proposta_id: int) -> GerenciamentoProposta | None:
        pass

    @abstractmethod
    async def create_gerenciamento_proposta(self, gerenciamento_proposta: GerenciamentoProposta) -> GerenciamentoProposta:
        pass

    @abstractmethod
    async def update_gerenciamento_proposta(self, gerenciamento_proposta_id: int, gerenciamento_proposta: GerenciamentoProposta) -> GerenciamentoProposta:
        pass

    @abstractmethod
    async def delete_gerenciamento_proposta(self, gerenciamento_proposta_id: int):
        pass

    @abstractmethod
    async def create_gerenciamento_proposta_comentario(self, gerenciamento_proposta_id: int, gerenciamento_comentario: GerenciamentoComentario) -> GerenciamentoProposta:
        pass

    @abstractmethod
    async def checar_gerenciamento_caracterizacao_exists(self, gerenciamento_proposta_id: int) -> bool:
        pass


class GerenciamentoMetaRepository(ABC):
    @abstractmethod
    async def get_gerenciamento_meta(self) -> list[GerenciamentoMeta]:
        pass

    @abstractmethod
    async def get_gerenciamento_meta_by_id(self, gerenciamento_meta_id: int) -> GerenciamentoMeta | None:
        pass

    @abstractmethod
    async def create_gerenciamento_meta(self, gerenciamento_proposta_id: int, gerenciamento_meta: GerenciamentoMeta) -> GerenciamentoMeta:
        pass

    @abstractmethod
    async def update_gerenciamento_meta(self, gerenciamento_meta_id: int, gerenciamento_meta: GerenciamentoMeta) -> GerenciamentoMeta:
        pass

    @abstractmethod
    async def delete_gerenciamento_meta(self, gerenciamento_meta_id: int):
        pass


class GerenciamentoQuantitativoRepository(ABC):
    @abstractmethod
    async def get_gerenciamento_quantitativo(self) -> list[GerenciamentoQuantitativo]:
        pass

    @abstractmethod
    async def get_gerenciamento_quantitativo_by_id(self, gerenciamento_quantitativo_id: int) -> GerenciamentoQuantitativo | None:
        pass

    @abstractmethod
    async def create_gerenciamento_quantitativo(self, gerenciamento_proposta_id: int, gerenciamento_quantitativo: GerenciamentoQuantitativo) -> GerenciamentoQuantitativo:
        pass

    @abstractmethod
    async def update_gerenciamento_quantitativo(self, gerenciamento_quantitativo_id: int, gerenciamento_quantitativo: GerenciamentoQuantitativo) -> GerenciamentoQuantitativo:
        pass

    @abstractmethod
    async def delete_gerenciamento_quantitativo(self, gerenciamento_quantitativo_id: int):
        pass

    @abstractmethod
    async def create_gerenciamento_quantitativo_comentario(self, gerenciamento_quantitativo_id: int, gerenciamento_comentario: GerenciamentoComentario) -> GerenciamentoQuantitativo:
        pass

    @abstractmethod
    async def checar_gerenciamento_caracterizacao_exists(self, gerenciamento_quantitativo_id: int) -> bool:
        pass


class GerenciamentoQualitativoRepository(ABC):
    @abstractmethod
    async def get_gerenciamento_qualitativo(self) -> list[GerenciamentoQualitativo]:
        pass

    @abstractmethod
    async def get_gerenciamento_qualitativo_by_id(self, gerenciamento_qualitativo_id: int) -> GerenciamentoQualitativo | None:
        pass

    @abstractmethod
    async def create_gerenciamento_qualitativo(self, gerenciamento_proposta_id: int, gerenciamento_qualitativo: GerenciamentoQualitativo) -> GerenciamentoQualitativo:
        pass

    @abstractmethod
    async def update_gerenciamento_qualitativo(self, gerenciamento_qualitativo_id: int, gerenciamento_qualitativo: GerenciamentoQualitativo) -> GerenciamentoQualitativo:
        pass

    @abstractmethod
    async def delete_gerenciamento_qualitativo(self, gerenciamento_qualitativo_id: int):
        pass

    @abstractmethod
    async def create_gerenciamento_qualitativo_comentario(self, gerenciamento_qualitativo_id: int, gerenciamento_comentario: GerenciamentoComentario) -> GerenciamentoQualitativo:
        pass


class GerenciamentoCaracterizacaoRepository(ABC):
    @abstractmethod
    async def get_gerenciamento_caracterizacao(self) -> list[GerenciamentoCaracterizacao]:
        pass

    @abstractmethod
    async def get_gerenciamento_caracterizacao_by_id(self, gerenciamento_caracterizacao_id: int) -> GerenciamentoCaracterizacao | None:
        pass

    @abstractmethod
    async def create_gerenciamento_caracterizacao(self, gerenciamento_quantitativo_id: int, gerenciamento_caracterizacao: GerenciamentoCaracterizacao) -> GerenciamentoCaracterizacao:
        pass

    @abstractmethod
    async def update_gerenciamento_caracterizacao(self, gerenciamento_caracterizacao_id: int, gerenciamento_caracterizacao: GerenciamentoCaracterizacao) -> GerenciamentoCaracterizacao:
        pass

    @abstractmethod
    async def delete_gerenciamento_caracterizacao(self, gerenciamento_caracterizacao_id: int):
        pass

    @abstractmethod
    async def find_categorizacoes_by_ids(self, categorizacoes_ids: list[int]) -> bool:
        pass


class GerenciamentoContrapartidaRepository(ABC):
    @abstractmethod
    async def get_gerenciamento_contrapartida(self) -> list[GerenciamentoContrapartida]:
        pass

    @abstractmethod
    async def get_gerenciamento_contrapartida_by_id(self, gerenciamento_contrapartida_id: int) -> GerenciamentoContrapartida | None:
        pass

    @abstractmethod
    async def create_gerenciamento_contrapartida(self, gerenciamento_proposta_id: int, gerenciamento_contrapartida: GerenciamentoContrapartida) -> GerenciamentoContrapartida:
        pass

    @abstractmethod
    async def update_gerenciamento_contrapartida(self, gerenciamento_contrapartida_id: int, gerenciamento_contrapartida: GerenciamentoContrapartida) -> GerenciamentoContrapartida:
        pass

    @abstractmethod
    async def delete_gerenciamento_contrapartida(self, gerenciamento_contrapartida_id: int):
        pass


class GerenciamentoContrapartidaAdminRepository(ABC):
    @abstractmethod
    async def get_gerenciamento_contrapartida_admin(self) -> list[GerenciamentoContrapartidaAdmin]:
        pass

    @abstractmethod
    async def get_gerenciamento_contrapartida_admin_by_id(self, gerenciamento_contrapartida_admin_id: int) -> GerenciamentoContrapartidaAdmin | None:
        pass

    @abstractmethod
    async def create_gerenciamento_contrapartida_admin(self, gerenciamento_contrapartida_id: int, gerenciamento_contrapartida_admin: GerenciamentoContrapartidaAdmin) -> GerenciamentoContrapartidaAdmin:
        pass

    @abstractmethod
    async def update_gerenciamento_contrapartida_admin(self, gerenciamento_contrapartida_admin_id: int, gerenciamento_contrapartida_admin: GerenciamentoContrapartidaAdmin) -> GerenciamentoContrapartidaAdmin:
        pass

    @abstractmethod
    async def delete_gerenciamento_contrapartida_admin(self, gerenciamento_contrapartida_admin_id: int):
        pass


class GerenciamentoArquivoRepository(ABC):
    @abstractmethod
    async def get_gerenciamento_arquivo_by_id(self, gerenciamento_arquivo_id: int) -> GerenciamentoMetaArquivo | GerenciamentoQualitativoArquivo | GerenciamentoContrapartidaArquivo | None:
        pass

    @abstractmethod
    async def create_arquivo(self, arquivo: Arquivo) -> int:
        pass

    @abstractmethod
    async def create_gerenciamento_meta_arquivo(self, gerenciamentoMetaArquivo: GerenciamentoMetaArquivo) -> GerenciamentoMetaArquivo:
        pass

    @abstractmethod
    async def create_gerenciamento_qualitativo_arquivo(self, gerenciamentoMetaArquivo: GerenciamentoQualitativoArquivo) -> GerenciamentoQualitativoArquivo:
        pass

    @abstractmethod
    async def create_gerenciamento_contrapartida_arquivo(self, gerenciamentoMetaArquivo: GerenciamentoContrapartidaArquivo) -> GerenciamentoContrapartidaArquivo:
        pass

    @abstractmethod
    async def delete_gerenciamento_arquivo(self, gerenciamentoMetaArquivo_id: int):
        pass
