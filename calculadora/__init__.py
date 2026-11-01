"""
Pacote da Calculadora Modular.
Desenvolvido com foco em boas práticas de Engenharia de Software.
"""

from .operacoes import (
    somar,
    subtrair,
    multiplicar,
    dividir,
    calcular,
    formatar_resultado,
    DivisaoPorZeroError,
    OperacaoInvalidaError,
)
from .validacao import (
    converter_operando,
    sanitizar_texto,
    ErroValidacao,
)

__all__ = [
    "somar",
    "subtrair",
    "multiplicar",
    "dividir",
    "calcular",
    "formatar_resultado",
    "DivisaoPorZeroError",
    "OperacaoInvalidaError",
    "converter_operando",
    "sanitizar_texto",
    "ErroValidacao",
]
