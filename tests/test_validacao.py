"""
Testes unitários para o módulo calculadora.validacao.

Cobre a sanitização, a normalização de separadores decimais (vírgula e ponto),
a rejeição de entradas vazias, malformadas e caracteres especiais, além de
garantir o limite de segurança de até 30 dígitos por literal e magnitude do expoente.
"""

import unittest
from calculadora.validacao import (
    ErroValidacao,
    converter_operando,
    sanitizar_texto,
    validar_literal_numerico,
)


class TestValidacaoEntradas(unittest.TestCase):
    """Suíte de testes para a camada de validação e conversão de entradas."""

    # -----------------------------------------------------------------------
    # Testes Originais da Baseline (Preservados Integralmente)
    # -----------------------------------------------------------------------

    def test_sanitizar_texto(self):
        """Verifica a remoção de espaços em branco antes e depois da string."""
        self.assertEqual(sanitizar_texto("  123  "), "123")
        self.assertEqual(sanitizar_texto("\t 45.6 \n"), "45.6")
        self.assertEqual(sanitizar_texto(None), "")

    # Requisito 7 & 9: Conversão correta de números válidos
    def test_conversao_inteiro_e_decimal_com_ponto(self):
        """Verifica conversão de strings numéricas com notação de ponto."""
        self.assertEqual(converter_operando("42"), 42.0)
        self.assertEqual(converter_operando("3.14159"), 3.14159)
        self.assertEqual(converter_operando("-18.75"), -18.75)

    # Requisito: Localização com vírgula
    def test_conversao_com_virgula(self):
        """Verifica se a vírgula é aceita e convertida adequadamente."""
        self.assertEqual(converter_operando("12,5"), 12.5)
        self.assertEqual(converter_operando("-0,75"), -0.75)

    # Requisito 6 (Guardrail): O número zero NÃO deve ser confundido com entrada vazia
    def test_zero_e_reconhecido_como_numero_valido(self):
        """Garante que '0', '0.0' e '0,0' são convertidos para 0.0 sem erros."""
        self.assertEqual(converter_operando("0"), 0.0)
        self.assertEqual(converter_operando("0.0"), 0.0)
        self.assertEqual(converter_operando("0,0"), 0.0)
        self.assertEqual(converter_operando("  0  "), 0.0)

    # Requisito 5: Validação de entradas vazias
    def test_entrada_vazia_lanca_excecao(self):
        """Verifica que strings vazias ou só com espaços disparam ErroValidacao."""
        with self.assertRaises(ErroValidacao) as ctx1:
            converter_operando("", nome_campo="Operando A")
        self.assertIn("O campo 'Operando A' não pode estar vazio", str(ctx1.exception))

        with self.assertRaises(ErroValidacao) as ctx2:
            converter_operando("    ", nome_campo="Operando B")
        self.assertIn("O campo 'Operando B' não pode estar vazio", str(ctx2.exception))

    # Requisito 7: Entradas inválidas e conversões malformadas
    def test_entrada_com_letras_ou_simbolos_lanca_excecao(self):
        """Verifica que textos alfanuméricos ou com símbolos disparam ErroValidacao."""
        with self.assertRaises(ErroValidacao):
            converter_operando("abc", nome_campo="Operando A")

        with self.assertRaises(ErroValidacao):
            converter_operando("12x", nome_campo="Operando A")

        with self.assertRaises(ErroValidacao):
            converter_operando("12.3.4", nome_campo="Operando A")

        with self.assertRaises(ErroValidacao):
            converter_operando("@!#$", nome_campo="Operando A")

    # Requisito 9: Rejeição de valores especiais não finitos
    def test_rejeicao_de_inf_e_nan(self):
        """Garante que strings como 'nan', 'inf' e '-inf' sejam rejeitadas como números válidos."""
        with self.assertRaises(ErroValidacao):
            converter_operando("nan")

        with self.assertRaises(ErroValidacao):
            converter_operando("inf")

        with self.assertRaises(ErroValidacao):
            converter_operando("-infinity")

    # -----------------------------------------------------------------------
    # Novos Testes — Fase 1: Limite de Literais e Notação Científica
    # -----------------------------------------------------------------------

    def test_validar_literal_ate_30_digitos(self):
        """Verifica que literais com até 30 dígitos numéricos são aceitos."""
        literal_30_digitos = "9" * 30
        resultado = validar_literal_numerico(literal_30_digitos)
        self.assertIsInstance(resultado, float)

        # 20 inteiros e 10 decimais = 30 dígitos
        literal_misto = ("1" * 20) + "," + ("2" * 10)
        resultado_misto = validar_literal_numerico(literal_misto)
        self.assertIsInstance(resultado_misto, float)

    def test_rejeicao_literal_mais_de_30_digitos(self):
        """Verifica que literais com mais de 30 dígitos numéricos disparam ErroValidacao."""
        literal_31_digitos = "9" * 31
        with self.assertRaises(ErroValidacao) as ctx:
            validar_literal_numerico(literal_31_digitos)
        self.assertIn("excede o limite máximo permitido de 30 dígitos", str(ctx.exception))

        # 20 inteiros e 11 decimais = 31 dígitos
        literal_misto_31 = ("1" * 20) + "." + ("2" * 11)
        with self.assertRaises(ErroValidacao):
            validar_literal_numerico(literal_misto_31)

    def test_notacao_cientifica_valida_e_limites(self):
        """Verifica notação científica e teto de magnitude de expoente (|exp| <= 308)."""
        self.assertEqual(validar_literal_numerico("1e3"), 1000.0)
        self.assertEqual(validar_literal_numerico("2.5E2"), 250.0)
        self.assertEqual(validar_literal_numerico("1e+10"), 1e10)
        self.assertEqual(validar_literal_numerico("1e-5"), 1e-5)

        # Expoente no teto máximo
        res_308 = validar_literal_numerico("1e308")
        self.assertEqual(res_308, 1e308)

        # Expoente abusivo que gera overflow ou excede limite
        with self.assertRaises(ErroValidacao):
            validar_literal_numerico("1e309")

        # Expoente com string gigante
        with self.assertRaises(ErroValidacao):
            validar_literal_numerico("1e100000")


if __name__ == "__main__":
    unittest.main()
