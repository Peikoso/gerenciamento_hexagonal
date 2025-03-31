import uuid
from abc import ABC, abstractmethod

from domain.models.gerenciamento import (
    GerenciamentoBeneficiarioCategorizacao,
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
)


class GerenciamentoComentarioRepository(ABC):
    @abstractmethod
    async def get_gerenciamentoComentario_by_id(self, gerenciamentoComentario_id: uuid) -> GerenciamentoComentario | None:
        pass

    @abstractmethod
    async def create_gerenciamentoComentario(self, gerenciamentoComentario: GerenciamentoComentario) -> GerenciamentoComentario:
        pass

    @abstractmethod
    async def update_gerenciamentoComentario(self, gerenciamentoComentario: GerenciamentoComentario) -> GerenciamentoComentario | None:
        pass

    @abstractmethod
    async def delete_gerenciamentoComentario(self, gerenciamentoComentario_id: uuid) -> None:
        pass

    @abstractmethod
    async def get_gerenciamentoComentario(self) -> list[GerenciamentoComentario]:
        pass


class GerenciamentoPropostaRepository(ABC):
    @abstractmethod
    async def get_gerenciamentoProposta_by_id(self, gerenciamentoProposta_id: uuid) -> GerenciamentoProposta | None:
        pass

    @abstractmethod
    async def create_gerenciamentoProposta(self, gerenciamentoProposta: GerenciamentoProposta) -> GerenciamentoProposta:
        pass

    @abstractmethod
    async def update_gerenciamentoProposta(self, gerenciamentoProposta: GerenciamentoProposta) -> GerenciamentoProposta | None:
        pass

    @abstractmethod
    async def delete_gerenciamentoProposta(self, gerenciamentoProposta_id: uuid):
        pass

    @abstractmethod
    async def get_gerenciamentoProposta(self) -> list[GerenciamentoProposta]:
        pass


class GerenciamentoMetaRepository(ABC):
    @abstractmethod
    async def get_gerenciamentoMeta_by_id(self, gerenciamentoMeta_id: uuid) -> GerenciamentoMeta | None:
        pass

    @abstractmethod
    async def create_gerenciamentoMeta(self, gerenciamentoMeta: GerenciamentoMeta) -> GerenciamentoMeta:
        pass

    @abstractmethod
    async def update_gerenciamentoMeta(self, gerenciamentoMeta: GerenciamentoMeta) -> GerenciamentoMeta | None:
        pass

    @abstractmethod
    async def delete_gerenciamentoMeta(self, gerenciamentoMeta_id: uuid):
        pass

    @abstractmethod
    async def get_gerenciamentoMeta(self) -> list[GerenciamentoMeta]:
        pass


class GerenciamentoQuantitativoRepository(ABC):
    @abstractmethod
    def get_gerenciamentoQuantitativo_by_id(self, gerenciamentoQuantitativo_id: uuid) -> GerenciamentoQuantitativo | None:
        pass

    @abstractmethod
    def create_gerenciamentoQuantitativo(self, gerenciamentoQuantitativo: GerenciamentoQuantitativo) -> GerenciamentoQuantitativo:
        pass

    @abstractmethod
    def update_gerenciamentoQuantitativo(self, gerenciamentoQuantitativo: GerenciamentoQuantitativo) -> GerenciamentoQuantitativo | None:
        pass

    @abstractmethod
    def delete_gerenciamentoQuantitativo(self, gerenciamentoQuantitativo_id: uuid):
        pass

    @abstractmethod
    def get_gerenciamentoQuantitativo(self) -> list[GerenciamentoQuantitativo]:
        pass


class GerenciamentoQualitativoRepository(ABC):
    @abstractmethod
    def get_gerenciamentoQualitativo_by_id(self, gerenciamentoQualitativo_id: uuid) -> GerenciamentoQualitativo | None:
        pass

    @abstractmethod
    def create_gerenciamentoQualitativo(self, gerenciamentoQuantitativo: GerenciamentoQualitativo) -> GerenciamentoQualitativo:
        pass

    @abstractmethod
    def update_gerenciamentoQualitativo(self, gerenciamentoQualitativo: GerenciamentoQualitativo) -> GerenciamentoQualitativo | None:
        pass

    @abstractmethod
    def delete_gerenciamentoQualitativo(self, gerenciamentoQualitativo_id: uuid):
        pass

    @abstractmethod
    def get_gerenciamentoQualitativo(self) -> list[GerenciamentoQualitativo]:
        pass


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
