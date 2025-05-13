from abc import ABC, abstractmethod


class VerifyGerenciamentoExists(ABC):
    @abstractmethod
    async def gerencimento_proposta_exists(self, gerenciamento_proposta_id: int):
        pass

    @abstractmethod
    async def gerenciamento_meta_exists(self, gerenciamento_meta_id: int):
        pass

    @abstractmethod
    async def gerenciamento_quantitativo_exists(self, gerenciamento_quantitativo_id: int):
        pass

    @abstractmethod
    async def gerenciamento_qualitativo_exists(self, gerenciamento_qualitativo_id: int):
        pass

    @abstractmethod
    async def gerenciamento_contrapartida_exists(self, gerenciamento_contrapartida_id: int):
        pass
