class ValidacaoService:
    @staticmethod
    def validar_tamanho_string(string: str, max_length: int):
        if len(string) > max_length:
            raise ValueError(f"Tamanhão inválido, maximo permitido: {max_length}")