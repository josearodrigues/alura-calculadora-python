"""
Módulo responsável pelas operações aritméticas fundamentais.

Este módulo implementa a camada de lógica de negócio (Business Logic) da
calculadora. Todas as funções aqui contidas são puras, determinísticas e
independentes de qualquer biblioteca de interface ou de entrada e saída (I/O).
"""

from typing import Callable, Dict


class DivisaoPorZeroError(Exception):
    """
    Exceção de domínio lançada quando uma operação de divisão tem divisor zero.
    
    Subclasse explícita de Exception para permitir captura pontual pela camada
    de controle/apresentação sem mascarar erros genéricos do sistema.
    """
    pass


class OperacaoInvalidaError(Exception):
    """
    Exceção de domínio lançada quando o símbolo ou identificador de operação
    não é reconhecido pela calculadora.
    """
    pass


def somar(a: float, b: float) -> float:
    """
    Calcula a adição entre dois números reais.

    Parâmetros:
        a (float): Primeiro operando (parcela).
        b (float): Segundo operando (parcela).

    Retorno:
        float: A soma algébrica dos dois operandos.
    """
    return a + b


def subtrair(a: float, b: float) -> float:
    """
    Calcula a subtração entre dois números reais.

    Parâmetros:
        a (float): Minuendo.
        b (float): Subtraendo.

    Retorno:
        float: A diferença resultante da operação (a - b).
    """
    return a - b


def multiplicar(a: float, b: float) -> float:
    """
    Calcula o produto da multiplicação entre dois números reais.

    Parâmetros:
        a (float): Multiplicando (fator).
        b (float): Multiplicador (fator).

    Retorno:
        float: O produto da multiplicação (a * b).
    """
    return a * b


def dividir(a: float, b: float) -> float:
    """
    Calcula o quociente da divisão entre dois números reais.

    Parâmetros:
        a (float): Dividendo.
        b (float): Divisor.

    Retorno:
        float: O quociente resultante da operação (a / b).

    Levanta:
        DivisaoPorZeroError: Se o divisor (b) for numericamente igual a zero.
    """
    if b == 0:
        raise DivisaoPorZeroError("Não é possível realizar divisão por zero.")
    return a / b


# Mapa de despacho das operações permitidas
# Relaciona o símbolo textual da operação à sua respectiva função pura.
MAPA_OPERACOES: Dict[str, Callable[[float, float], float]] = {
    "+": somar,
    "-": subtrair,
    "*": multiplicar,
    "/": dividir,
}


def calcular(a: float, b: float, operacao: str) -> float:
    """
    Despacha a operação solicitada para a função matemática correspondente.

    Utiliza um padrão de dicionário de despacho (Dispatch Table), eliminando
    a necessidade de cadeias aninhadas de 'if/elif/else' e garantindo que
    operações inexistentes sejam rejeitadas de forma segura.

    Parâmetros:
        a (float): Primeiro operando.
        b (float): Segundo operando.
        operacao (str): Símbolo da operação desejada ('+', '-', '*', '/').

    Retorno:
        float: O resultado numérico da operação executada.

    Levanta:
        OperacaoInvalidaError: Caso o símbolo de operação não conste no MAPA_OPERACOES.
        DivisaoPorZeroError: Caso a operação seja divisão e b seja zero.
    """
    funcao_operacao = MAPA_OPERACOES.get(operacao)
    if funcao_operacao is None:
        operacoes_suportadas = ", ".join(repr(op) for op in MAPA_OPERACOES.keys())
        raise OperacaoInvalidaError(
            f"Operação '{operacao}' não suportada. Escolha uma das seguintes: {operacoes_suportadas}."
        )

    return funcao_operacao(a, b)


def formatar_resultado(valor: float, precisao_maxima: int = 8) -> str:
    """
    Formata um valor numérico para exibição amigável ao usuário.

    Regras de formatação:
    - Se o valor for um número inteiro exato (ex.: 5.0), remove o sufixo '.0' e exibe '5'.
    - Se o valor contiver casas decimais, preserva as casas relevantes sem ruído de
      ponto flutuante IEEE 754 (arredondando para até a precisão configurada).

    Parâmetros:
        valor (float): O número a ser formatado.
        precisao_maxima (int): Quantidade máxima de casas decimais para exibição.

    Retorno:
        str: Representação textual limpa do número.
    """
    # Trata caso de precisão finita para evitar dízimas espúrias como 0.30000000000000004
    valor_arredondado = round(valor, precisao_maxima)
    
    # Se o número arredondado for equivalente ao seu valor inteiro, exibe como int
    if valor_arredondado.is_integer():
        return str(int(valor_arredondado))
    
    # Caso contrário, converte para string mantendo o ponto decimal real
    return str(valor_arredondado)
