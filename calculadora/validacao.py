"""
Módulo de validação e sanitização de entradas da calculadora.

Este módulo atua como uma barreira de proteção (Guardrail / Boundary Adapter)
entre os dados brutos de texto recebidos pela interface do usuário e os
valores numéricos requeridos pela camada de lógica matemática.
"""

import math
from typing import Optional


class ErroValidacao(Exception):
    """
    Exceção de domínio lançada quando uma entrada de texto fornecida pelo
    usuário não pode ser validada ou convertida com segurança para número.
    """
    pass


def sanitizar_texto(texto: Optional[str]) -> str:
    """
    Remove espaços em branco no início e no final da string fornecida.

    Parâmetros:
        texto (Optional[str]): String bruta recebida da interface.

    Retorno:
        str: String sem espaços nas extremidades ou string vazia se for None.
    """
    if texto is None:
        return ""
    return texto.strip()


def converter_operando(valor_bruto: str, nome_campo: str = "Operando") -> float:
    """
    Valida, sanitiza e converte uma entrada textual para um número real (float).

    Regras aplicadas:
    1. Verifica se a entrada está ausente ou composta apenas de espaços.
    2. Substitui a vírgula (',') por ponto ('.') para suportar localização brasileira.
    3. Converte a string tratada para float.
    4. Rejeita valores especiais como 'inf', '-inf' e 'nan' que poderiam ser aceitos
       pelo float() nativo do Python mas são inválidos como entradas do usuário.

    Parâmetros:
        valor_bruto (str): O texto digitado pelo usuário.
        nome_campo (str): Identificador do campo (ex.: 'Operando A', 'Operando B')
                          para compor mensagens de erro precisas e humanizadas.

    Retorno:
        float: O número real correspondente.

    Levanta:
        ErroValidacao: Caso o valor seja vazio, não seja numérico ou seja um valor infinito/NaN.
    """
    texto_limpo = sanitizar_texto(valor_bruto)

    if not texto_limpo:
        raise ErroValidacao(f"O campo '{nome_campo}' não pode estar vazio.")

    # Normaliza separador decimal (aceita tanto 12.5 quanto 12,5)
    texto_normalizado = texto_limpo.replace(",", ".")

    try:
        valor_numerico = float(texto_normalizado)
    except ValueError:
        raise ErroValidacao(
            f"O valor '{texto_limpo}' informado para '{nome_campo}' não é um número válido."
        )

    # Proteção contra valores não finitos (ex: strings como 'nan', 'inf', '-infinity')
    if math.isnan(valor_numerico) or math.isinf(valor_numerico):
        raise ErroValidacao(
            f"O valor informado para '{nome_campo}' não é um número real finito permitido."
        )

    return valor_numerico
