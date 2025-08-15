from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import DomainValidationError


class ValidacaoService:
    @staticmethod
    def validar_tamanho_string(context: str, string: str, max_length: int):
        if string:
            string = string.strip()

        if len(string) > max_length:
            raise DomainValidationError(f'{context}: max length permitted: {max_length}.')

        if len(string) < 1:
            raise DomainValidationError('Field cannot be empty')

    @staticmethod
    def validar_num_positivo(context: str, num: int):
        if num < 0:
            raise DomainValidationError(f"{context}: number can't be negative")
