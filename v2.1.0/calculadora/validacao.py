"""
Módulo de validação e sanitização de entradas da calculadora.

Este módulo atua como uma barreira de proteção (Guardrail / Boundary Adapter)
entre os dados brutos de texto recebidos pela interface do usuário e os
valores numéricos requeridos pela camada de lógica matemática.
"""

import math
import re
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


def validar_literal_numerico(texto_literal: str) -> float:
    """
    Valida um literal numérico isolado aplicando as políticas de segurança da calculadora:
    1. Limite de Entrada vs. Precisão Numérica:
       - Restringe a entrada a no máximo 30 algarismos numéricos significativos na mantissa
         como salvaguarda de entrada (I/O Security Guard contra sobrecarga de parsing).
       - Observação de precisão: a representação interna e os cálculos ocorrem em ponto
         flutuante de 64 bits (IEEE 754 float do Python), cuja precisão real é de
         aproximadamente 15 a 17 dígitos decimais significativos.
    2. Notação Científica e Expoente:
       - O trecho textual do expoente (após o caractere 'e' ou 'E') é restrito a no
         máximo 4 caracteres (ex.: '+308', '-308', '308').
       - A magnitude numérica do expoente é limitada a |expoente| <= 308 (política de projeto).
    3. Proteção contra Overflow na Conversão:
       - Detecta overflow no ato da conversão para ponto flutuante, rejeitando literais que
         resultem em Infinito.
    4. Localização:
       - Suporta tanto a vírgula decimal brasileira (12,5) quanto o ponto (12.5).

    Parâmetros:
        texto_literal (str): String do literal numérico.

    Retorno:
        float: Valor numérico real convertido.

    Levanta:
        ErroValidacao: Caso o número viole limites de tamanho ou resulte em valor não finito.
    """
    texto = sanitizar_texto(texto_literal)
    if not texto:
        raise ErroValidacao("Literal numérico não pode estar vazio.")

    # Remove sinal inicial para análise dos dígitos do literal
    corpo = texto
    if corpo.startswith(("+", "-")):
        corpo = corpo[1:]

    # Divide em mantissa e expoente (se houver notação científica e/E)
    partes_exp = re.split(r"[eE]", corpo)
    if len(partes_exp) > 2:
        raise ErroValidacao(f"O literal '{texto}' possui formato de notação científica inválido.")

    parte_mantissa = partes_exp[0]
    parte_expoente = partes_exp[1] if len(partes_exp) == 2 else None

    # Contagem de dígitos significativos da mantissa (excluindo separador decimal '.' ou ',')
    digitos_mantissa = re.sub(r"[,.]", "", parte_mantissa)
    if not digitos_mantissa:
        raise ErroValidacao(f"O literal '{texto}' não contém dígitos numéricos válidos.")

    if len(digitos_mantissa) > 30:
        raise ErroValidacao(
            f"O literal numérico excede o limite máximo permitido de 30 dígitos (informados: {len(digitos_mantissa)})."
        )

    # Validação do expoente (se presente)
    if parte_expoente is not None:
        if not parte_expoente or not re.match(r"^[+-]?\d+$", parte_expoente):
            raise ErroValidacao(f"Expoente inválido no literal '{texto}'.")

        # Tamanho do trecho textual do expoente (após e/E) limitado a 4 caracteres (ex.: +308, -308, 308)
        if len(parte_expoente) > 4:
            raise ErroValidacao("Trecho do expoente (após e/E) excede o limite textual de segurança permitido de 4 caracteres.")

        try:
            val_exp = int(parte_expoente)
        except ValueError:
            raise ErroValidacao("Expoente inválido.")

        if abs(val_exp) > 308:
            raise ErroValidacao(
                f"Magnitude do expoente ({val_exp}) excede o limite máximo permitido de 308."
            )

    # Normalização de vírgula para ponto e conversão segura
    texto_normalizado = texto.replace(",", ".")
    try:
        valor_numerico = float(texto_normalizado)
    except (ValueError, OverflowError):
        raise ErroValidacao(f"O literal numérico '{texto}' excede a capacidade de representação (gera Infinito).")

    if math.isnan(valor_numerico) or math.isinf(valor_numerico):
        raise ErroValidacao(f"O literal numérico '{texto}' resulta em valor infinito ou indefinido.")

    return valor_numerico


def converter_operando(valor_bruto: str, nome_campo: str = "Operando") -> float:
    """
    Valida, sanitiza e converte uma entrada textual de operando para número real (float).
    Mantém 100% de compatibilidade com a baseline existente e aplica validação rigorosa.
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
