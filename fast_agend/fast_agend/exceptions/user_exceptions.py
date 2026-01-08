class InvalidCPFException(Exception):
    def __init__(self, message: str = "CPF inválido"):
        super().__init__(message)

class UsernameAlreadyExistsException(Exception):
    def __init__(self, message: str = "Nome de usuário já registrado!"):
        super().__init__(message)

class EmailAlreadyExistsException(Exception):
    def __init__(self, message: str = "E-mail já registrado!"):
        super().__init__(message)

class CPFAlreadyExistsException(Exception):
    def __init__(self, message: str = "CPF já registrado!"):
        super().__init__(message)

class ExistingNumberException(Exception):
    def __init__(self, message: str = "Número já registrado!"):
        super().__init__(message)