"""
Testes unitários para o módulo calculadora.validacao.

Cobre a sanitização, a normalização de separadores decimais (vírgula e ponto),
a rejeição de entradas vazias, malformadas e caracteres especiais, além de
garantir que o número zero não seja confundido com entrada vazia.
"""

import unittest
from calculadora.validacao import (
    converter_operando,
    sanitizar_texto,
    ErroValidacao,
)


class TestValidacaoEntradas(unittest.TestCase):
    """Suíte de testes para a camada de validação e conversão de entradas."""

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


if __name__ == "__main__":
    unittest.main()
