"""
Módulo responsável pelas operações aritméticas fundamentais.

Este módulo implementa a camada de lógica de negócio (Business Logic) da
calculadora. Todas as funções aqui contidas são puras, determinísticas e
independentes de qualquer biblioteca de interface ou de entrada e saída (I/O).
"""

import math
from typing import Any, Callable, Dict


class ErroAritmetico(Exception):
    """
    Exceção base para falhas de cálculo numérico na calculadora
    (ex.: overflow, valores indefinidos ou infinitos).
    """
    pass


class DivisaoPorZeroError(ErroAritmetico):
    """
    Exceção de domínio lançada quando uma operação de divisão tem divisor zero
    ou quando ocorre inversão aritmética de zero.
    """
    pass


class RadicandoNegativoError(ErroAritmetico):
    """
    Exceção lançada quando uma operação com radicando negativo não possui
    resultado no domínio dos números reais.
    """
    pass


class OperacaoInvalidaError(Exception):
    """
    Exceção de domínio lançada quando o símbolo ou identificador de operação
    não é reconhecido ou quando parâmetros violam restrições matemáticas (ex.: índice 0).
    """
    pass


def _assegurar_numero_valido(valor: Any) -> float:
    """
    Valida e sanitiza numericamente resultados intermediários e finais.
    Rejeita tipos complexos, conversões falhas, valores infinitos e NaN.

    Parâmetros:
        valor (Any): Valor numérico a ser inspecionado.

    Retorno:
        float: Número real finito representável.

    Levanta:
        RadicandoNegativoError: Se o resultado for complexo.
        ErroAritmetico: Se o valor for infinito, NaN ou não conversível para float.
    """
    if isinstance(valor, complex):
        raise RadicandoNegativoError("Resultado complexo não é suportado no domínio dos números reais.")

    try:
        val_float = float(valor)
    except OverflowError:
        raise ErroAritmetico("Resultado excedeu a capacidade de representação numérica (Overflow).")
    except (ValueError, TypeError):
        raise ErroAritmetico("Valor não conversível para ponto flutuante real.")

    if math.isnan(val_float) or math.isinf(val_float):
        raise ErroAritmetico("Operação matemática resultou em valor infinito ou indefinido (Overflow/NaN).")

    return val_float


def executar_operacao_segura(operacao_fn: Callable[..., Any], *args: Any) -> float:
    """
    Executa uma operação matemática capturando exceções nativas e mapeando-as
    para exceções de domínio padronizadas da calculadora.
    """
    try:
        resultado = operacao_fn(*args)
    except OverflowError:
        raise ErroAritmetico("Resultado excedeu a capacidade de representação numérica (Overflow).")
    except ZeroDivisionError:
        raise DivisaoPorZeroError("Não é possível realizar divisão por zero.")
    except (ValueError, TypeError) as e:
        raise ErroAritmetico(f"Operação matemática inválida: {str(e)}")

    return _assegurar_numero_valido(resultado)


def somar(a: float, b: float) -> float:
    """Calcula a adição entre dois números reais."""
    try:
        res = a + b
    except OverflowError:
        raise ErroAritmetico("Resultado da adição excedeu a capacidade de representação numérica (Overflow).")
    return _assegurar_numero_valido(res)


def subtrair(a: float, b: float) -> float:
    """Calcula a subtração entre dois números reais."""
    try:
        res = a - b
    except OverflowError:
        raise ErroAritmetico("Resultado da subtração excedeu a capacidade de representação numérica (Overflow).")
    return _assegurar_numero_valido(res)


def multiplicar(a: float, b: float) -> float:
    """Calcula o produto da multiplicação entre dois números reais."""
    try:
        res = a * b
    except OverflowError:
        raise ErroAritmetico("Resultado da multiplicação excedeu a capacidade de representação numérica (Overflow).")
    return _assegurar_numero_valido(res)


def dividir(a: float, b: float) -> float:
    """
    Calcula o quociente da divisão entre dois números reais.
    Levanta DivisaoPorZeroError se o divisor b for zero.
    """
    if b == 0:
        raise DivisaoPorZeroError("Não é possível realizar divisão por zero.")
    try:
        res = a / b
    except OverflowError:
        raise ErroAritmetico("Resultado da divisão excedeu a capacidade de representação numérica (Overflow).")
    return _assegurar_numero_valido(res)


def potencia(base: float, expoente: float) -> float:
    """
    Calcula a potenciação (base ** expoente) no domínio dos números reais.
    """
    # 0 ** expoente negativo implica divisão por zero (1 / 0)
    if base == 0.0 and expoente < 0.0:
        raise DivisaoPorZeroError("Não é possível elevar zero a um expoente negativo.")

    # Base negativa com expoente não inteiro resulta em número complexo
    if base < 0.0:
        expoente_inteiro = isinstance(expoente, int) or (math.isfinite(expoente) and float(expoente).is_integer())
        if not expoente_inteiro:
            raise RadicandoNegativoError(
                f"Potência de base negativa ({base}) com expoente não inteiro ({expoente}) não pertence aos Reais."
            )

    try:
        res = base ** expoente
    except OverflowError:
        raise ErroAritmetico("Resultado da potenciação excedeu a capacidade de representação numérica (Overflow).")

    return _assegurar_numero_valido(res)


def raiz_quadrada(radicando: float) -> float:
    """
    Calcula a raiz quadrada de um número real não negativo.
    """
    if not math.isfinite(radicando):
        raise ErroAritmetico("Radicando deve ser um número real finito.")
    if radicando < 0.0:
        raise RadicandoNegativoError(
            f"Raiz quadrada de número negativo ({radicando}) não é permitida no domínio dos números reais."
        )
    try:
        res = math.sqrt(radicando)
    except OverflowError:
        raise ErroAritmetico("Resultado da raiz quadrada excedeu a capacidade de representação numérica.")

    return _assegurar_numero_valido(res)


def raiz_n(radicando: float, indice: float) -> float:
    """
    Calcula a raiz de índice n (radicando ** (1 / indice)) no domínio dos números reais.

    Regras:
    1. Radicando e índice devem ser números reais finitos.
    2. Índice zero é inválido (levanta OperacaoInvalidaError).
    3. Radicando zero com índice negativo implica divisão por zero.
    4. Índice negativo inverte o resultado: 1.0 / raiz_n(radicando, |indice|).
    5. Radicando negativo é permitido exclusivamente se o índice for inteiro ímpar.
    6. Radicando positivo é permitido para qualquer índice real finito não nulo (inclusive fracionário).
    """
    if not (math.isfinite(radicando) and math.isfinite(indice)):
        raise ErroAritmetico("Radicando e índice devem ser números reais finitos.")

    if indice == 0.0:
        raise OperacaoInvalidaError("O índice da raiz não pode ser zero.")

    if radicando == 0.0:
        if indice < 0.0:
            raise DivisaoPorZeroError("Raiz de zero com índice negativo implica divisão por zero.")
        return 0.0

    # Trata índice negativo por inversão aritmética
    if indice < 0.0:
        resultado_positivo = raiz_n(radicando, abs(indice))
        if resultado_positivo == 0.0:
            raise DivisaoPorZeroError("Divisão por zero ao inverter raiz de índice negativo.")
        try:
            return _assegurar_numero_valido(1.0 / resultado_positivo)
        except OverflowError:
            raise ErroAritmetico("Resultado da inversão da raiz excedeu a capacidade de representação numérica.")

    # Verifica se o índice é inteiro
    indice_e_inteiro = isinstance(indice, int) or float(indice).is_integer()

    if radicando < 0.0:
        if indice_e_inteiro and (int(indice) % 2 != 0):
            # Índice inteiro ímpar com radicando negativo: resultado real negativo
            try:
                res = -(abs(radicando) ** (1.0 / indice))
            except OverflowError:
                raise ErroAritmetico("Resultado da raiz excedeu a capacidade de representação numérica (Overflow).")
            return _assegurar_numero_valido(res)
        else:
            raise RadicandoNegativoError(
                f"Raiz de número negativo ({radicando}) não possui resultado real para índice não inteiro ou par ({indice})."
            )

    # Radicando positivo (índice inteiro ou fracionário)
    try:
        res = radicando ** (1.0 / indice)
    except OverflowError:
        raise ErroAritmetico("Resultado da raiz excedeu a capacidade de representação numérica (Overflow).")

    return _assegurar_numero_valido(res)


def valor_absoluto(a: float) -> float:
    """Calcula o valor absoluto de um número real."""
    if not math.isfinite(a):
        raise ErroAritmetico("Valor deve ser um número real finito.")
    return _assegurar_numero_valido(abs(a))


def inverso(a: float) -> float:
    """Calcula o inverso aritmético (1 / a)."""
    if a == 0.0:
        raise DivisaoPorZeroError("Não é possível calcular o inverso de zero (divisão por zero).")
    try:
        res = 1.0 / a
    except OverflowError:
        raise ErroAritmetico("Resultado do inverso excedeu a capacidade de representação numérica.")
    return _assegurar_numero_valido(res)


def trocar_sinal(a: float) -> float:
    """Inverte o sinal algébrico (-a)."""
    if not math.isfinite(a):
        raise ErroAritmetico("Valor deve ser um número real finito.")
    return _assegurar_numero_valido(-a)


# Mapa de despacho das operações binárias fundamentais
MAPA_OPERACOES: Dict[str, Callable[[float, float], float]] = {
    "+": somar,
    "-": subtrair,
    "*": multiplicar,
    "/": dividir,
    "^": potencia,
}


def calcular(a: float, b: float, operacao: str) -> float:
    """
    Despacha a operação solicitada para a função matemática correspondente.
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
    - Se for inteiro exato (ex.: 5.0), exibe '5'.
    - Remove ruídos IEEE 754 arredondando para até a precisão configurada.
    """
    valor_arredondado = round(valor, precisao_maxima)
    if valor_arredondado.is_integer():
        return str(int(valor_arredondado))
    return str(valor_arredondado)
