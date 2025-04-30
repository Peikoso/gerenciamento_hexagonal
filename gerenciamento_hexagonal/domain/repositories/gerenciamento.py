from abc import ABC, abstractmethod

from gerenciamento_hexagonal.domain.models.gerenciamento import (
    # GerenciamentoBeneficiarioCategorizacao,
    # GerenciamentoCaracterizacao,
    GerenciamentoComentario,
    GerenciamentoMeta,
    # GerenciamentoContrapartida,
    # GerenciamentoContrapartidaAdmin,
    # GerenciamentoContrapartidaArquivo,
    # GerenciamentoMeta,
    # GerenciamentoMetaArquivo,
    GerenciamentoProposta,
    GerenciamentoQualitativo,
    GerenciamentoQuantitativo,
    # GerenciamentoQualitativo,
    # GerenciamentoQualitativoArquivo,
    # GerenciamentoQuantitativo,
)


class GerenciamentoComentarioRepository(ABC):
    @abstractmethod
    async def get_gerenciamento_comentario(self) -> list[GerenciamentoComentario]:
        pass

    @abstractmethod
    async def get_gerenciamento_comentario_by_id(self, gerenciamento_comentario_id: int) -> GerenciamentoComentario:
        pass

    @abstractmethod
    async def create_gerenciamento_comentario(self, gerenciamento_comentario: GerenciamentoComentario) -> GerenciamentoComentario:
        pass

    @abstractmethod
    async def update_gerenciamento_comentario(self, gerenciamento_comentario_id: int, gerenciamento_comentario: GerenciamentoComentario) -> GerenciamentoComentario:
        pass

    @abstractmethod
    async def delete_gerenciamento_comentario(self, gerenciamento_comentario_id: int) -> bool:
        pass


class GerenciamentoPropostaRepository(ABC):
    @abstractmethod
    async def get_gerenciamento_proposta(self) -> list[GerenciamentoProposta]:
        pass

    @abstractmethod
    async def get_gerenciamento_proposta_by_id(self, gerenciamento_proposta_id: int) -> GerenciamentoProposta:
        pass

    @abstractmethod
    async def create_gerenciamento_proposta(self, gerenciamento_proposta: GerenciamentoProposta) -> GerenciamentoProposta:
        pass

    @abstractmethod
    async def update_gerenciamento_proposta(self, gerenciamento_proposta_id: int, gerenciamento_proposta: GerenciamentoProposta) -> GerenciamentoProposta:
        pass

    @abstractmethod
    async def delete_gerenciamento_proposta(self, gerenciamento_proposta_id: int) -> bool:
        pass

    @abstractmethod
    async def create_gerenciamento_proposta_comentario(self, gerenciamento_proposta_id: int, gerenciamento_comentario: GerenciamentoComentario) -> GerenciamentoProposta:
        pass


class GerenciamentoMetaRepository(ABC):
    @abstractmethod
    async def get_gerenciamento_meta(self) -> list[GerenciamentoMeta]:
        pass

    @abstractmethod
    async def get_gerenciamento_meta_by_id(self, gerenciamento_meta_id: int) -> GerenciamentoMeta:
        pass

    @abstractmethod
    async def create_gerenciamento_meta(self, gerenciamento_proposta_id: int, gerenciamento_meta: GerenciamentoMeta) -> GerenciamentoMeta:
        pass

    @abstractmethod
    async def update_gerenciamento_meta(self, gerenciamento_meta_id: int, gerenciamento_meta: GerenciamentoMeta) -> GerenciamentoMeta:
        pass

    @abstractmethod
    async def delete_gerenciamento_meta(self, gerenciamento_meta_id: int) -> bool:
        pass


class GerenciamentoQuantitativoRepository(ABC):
    @abstractmethod
    async def get_gerenciamento_quantitativo(self) -> list[GerenciamentoQuantitativo]:
        pass

    @abstractmethod
    async def get_gerenciamento_quantitativo_by_id(self, gerenciamento_quantitativo_id: int) -> GerenciamentoQuantitativo:
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


class GerenciamentoQualitativoRepository(ABC):
    @abstractmethod
    async def get_gerenciamento_qualitativo(self) -> list[GerenciamentoQualitativo]:
        pass

    @abstractmethod
    async def get_gerenciamento_qualitativo_by_id(self, gerenciamento_qualitativo_id: int) -> GerenciamentoQualitativo:
        pass

    @abstractmethod
    async def create_gerenciamento_qualitativo(self, gerenciamento_proposta_id: int, gerenciamento_qualitativo: GerenciamentoQualitativo) -> GerenciamentoQualitativo:
        pass

    @abstractmethod
    async def update_gerenciamento_qualitativo(self, gerenciamento_qualitativo_id: int, gerenciamento_qualitativo: GerenciamentoQualitativo) -> GerenciamentoQualitativo | None:
        pass

    @abstractmethod
    async def delete_gerenciamento_qualitativo(self, gerenciamento_qualitativo_id: int):
        pass

    @abstractmethod
    async def create_gerenciamento_qualitativo_comentario(self, gerenciamento_qualitativo_id: int, gerenciamento_comentario: GerenciamentoComentario) -> GerenciamentoQualitativo:
        pass


"""
class GerenciamentoCaracterizacaoRepository(ABC):
    @abstractmethod
    def get_gerenciamentoCaracterizacao_by_id(self, gerenciamentoCaracterizacao_id: uuid) -> GerenciamentoCaracterizacao | None:
        pass

    @abstractmethod
    def create_gerenciamentoCaracterizacao(self, gerenciamentoCaracterizacao: GerenciamentoCaracterizacao) -> GerenciamentoCaracterizacao:
        pass

    @abstractmethod
    def update_gerenciamentoCaracterizacao(self, gerenciamentoCaracterizacao: GerenciamentoCaracterizacao) -> GerenciamentoCaracterizacao | None:
        pass

    @abstractmethod
    def delete_gerenciamentoCaracterizacao(self, gerenciamentoCaracterizacao_id: uuid):
        pass

    @abstractmethod
    def get_gerenciamentoCaracterizacao(self) -> list[GerenciamentoCaracterizacao]:
        pass


class GerenciamentoBeneficiarioCategorizacaoRepository(ABC):
    @abstractmethod
    def get_gerenciamentoBeneficiarioCategorizacao_by_id(self, gerenciamentoBeneficiarioCategorizacao_id: uuid) -> GerenciamentoBeneficiarioCategorizacao | None:
        pass

    @abstractmethod
    def create_gerenciamentoBeneficiarioCategorizacao(
        self, gerenciamentoBeneficiarioCategorizacao: GerenciamentoBeneficiarioCategorizacao
    ) -> GerenciamentoBeneficiarioCategorizacao:
        pass

    @abstractmethod
    def update_gerenciamentoBeneficiarioCategorizacao(
        self, gerenciamentoBeneficiarioCategorizacao: GerenciamentoBeneficiarioCategorizacao
    ) -> GerenciamentoBeneficiarioCategorizacao | None:
        pass

    @abstractmethod
    def delete_gerenciamentoBeneficiarioCategorizacao(self, gerenciamentoBeneficiarioCategorizacao_id: uuid):
        pass

    @abstractmethod
    def get_gerenciamentoBeneficiarioCategorizacao(self) -> list[GerenciamentoBeneficiarioCategorizacao]:
        pass


class GerenciamentoMetaArquivoRepository(ABC):
    @abstractmethod
    def get_gerenciamentoMetaArquivo_by_id(self, gerenciamentoMetaArquivo_id: uuid) -> GerenciamentoMetaArquivo | None:
        pass

    @abstractmethod
    def create_gerenciamentoMetaArquivo(self, gerenciamentoMetaArquivo: GerenciamentoMetaArquivo) -> GerenciamentoMetaArquivo:
        pass

    @abstractmethod
    def update_gerenciamentoMetaArquivo(self, gerenciamentoMetaArquivo: GerenciamentoMetaArquivo) -> GerenciamentoMetaArquivo | None:
        pass

    @abstractmethod
    def delete_gerenciamentoMetaArquivo(self, gerenciamentoMetaArquivo_id: uuid):
        pass

    @abstractmethod
    def get_gerenciamentoMetaArquivo(self) -> list[GerenciamentoMetaArquivo]:
        pass


class GerenciamentoQualitativoArquivoRepository(ABC):
    @abstractmethod
    def get_gerenciamentoQualitativoArquivo_by_id(self, gerenciamentoQualitativoArquivo_id: uuid) -> GerenciamentoQualitativoArquivo | None:
        pass

    @abstractmethod
    def create_gerenciamentoQualitativoArquivo(self, gerenciamentoQualitativoArquivo: GerenciamentoQualitativoArquivo) -> GerenciamentoQualitativoArquivo:
        pass

    @abstractmethod
    def update_gerenciamentoQualitativoArquivo(self, gerenciamentoQualitativoArquivo: GerenciamentoQualitativoArquivo) -> GerenciamentoQualitativoArquivo | None:
        pass

    @abstractmethod
    def delete_gerenciamentoQualitativoArquivo(self, gerenciamentoQualitativoArquivo_id: uuid):
        pass

    @abstractmethod
    def get_gerenciamentoQualitativoArquivo(self) -> list[GerenciamentoQualitativoArquivo]:
        pass


class GerenciamentoContrapartidaRepository(ABC):
    @abstractmethod
    def get_gerenciamentoContrapartida_by_id(self, gerenciamentoContrapartida_id: uuid) -> GerenciamentoContrapartida | None:
        pass

    @abstractmethod
    def create_gerenciamentoContrapartida(self, gerenciamentoContrapartida: GerenciamentoContrapartida) -> GerenciamentoContrapartida:
        pass

    @abstractmethod
    def update_gerenciamentoContrapartida(self, gerenciamentoContrapartida: GerenciamentoContrapartida) -> GerenciamentoContrapartida | None:
        pass

    @abstractmethod
    def delete_gerenciamentoContrapartida(self, gerenciamentoContrapartida_id: uuid):
        pass

    @abstractmethod
    def get_gerenciamentoContrapartida(self) -> list[GerenciamentoContrapartida]:
        pass


class GerenciamentoContrapartidaArquivoRepository(ABC):
    @abstractmethod
    def get_gerenciamentoContrapartidaArquivo_by_id(self, gerenciamentoContrapartidaArquivo_id: uuid) -> GerenciamentoContrapartidaArquivo | None:
        pass

    @abstractmethod
    def create_gerenciamentoContrapartidaArquivo(self, gerenciamentoContrapartidaArquivo: GerenciamentoContrapartidaArquivo) -> GerenciamentoContrapartidaArquivo:
        pass

    @abstractmethod
    def update_gerenciamentoContrapartidaArquivo(self, gerenciamentoContrapartidaArquivo: GerenciamentoContrapartidaArquivo) -> GerenciamentoContrapartidaArquivo | None:
        pass

    @abstractmethod
    def delete_gerenciamentoContrapartidaArquivo(self, gerenciamentoContrapartidaArquivo_id: uuid):
        pass

    @abstractmethod
    def get_gerenciamentoContrapartidaArquivo(self) -> list[GerenciamentoContrapartidaArquivo]:
        pass


class GerenciamentoContrapartidaAdminRepository(ABC):
    @abstractmethod
    def get_gerenciamentoContrapartidaAdmin_by_id(self, gerenciamentoContrapartidaAdmin_id: uuid) -> GerenciamentoContrapartidaAdmin | None:
        pass

    @abstractmethod
    def create_gerenciamentoContrapartidaAdmin(self, gerenciamentoContrapartidaAdmin: GerenciamentoContrapartidaAdmin) -> GerenciamentoContrapartidaAdmin:
        pass

    @abstractmethod
    def update_gerenciamentoContrapartidaAdmin(self, gerenciamentoContrapartidaAdmin: GerenciamentoContrapartidaAdmin) -> GerenciamentoContrapartidaAdmin | None:
        pass

    @abstractmethod
    def delete_gerenciamentoContrapartidaAdmin(self, gerenciamentoContrapartidaAdmin_id: uuid):
        pass

    @abstractmethod
    def get_gerenciamentoContrapartidaAdmin(self) -> list[GerenciamentoContrapartidaAdmin]:
        pass
"""
