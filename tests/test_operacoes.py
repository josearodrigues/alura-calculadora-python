"""
Testes unitários para o módulo calculadora.operacoes.

Cobre as 4 operações básicas, casos com números negativos, multiplicação por zero,
divisões exatas e decimais, proteção contra divisão por zero e operações inválidas.
"""

import unittest
from calculadora.operacoes import (
    somar,
    subtrair,
    multiplicar,
    dividir,
    calcular,
    formatar_resultado,
    DivisaoPorZeroError,
    OperacaoInvalidaError,
)


class TestOperacoesMatematicas(unittest.TestCase):
    """Suíte de testes para funções de cálculo aritmético."""

    # Requisito 1: Adição de números positivos
    def test_adicao_numeros_positivos(self):
        """Verifica a soma entre dois números positivos."""
        resultado = somar(15.0, 27.5)
        self.assertEqual(resultado, 42.5)

    # Requisito 8: Verificação do comportamento com números negativos
    def test_adicao_numeros_negativos(self):
        """Verifica a soma envolvendo números negativos."""
        self.assertEqual(somar(-10.0, -5.0), -15.0)
        self.assertEqual(somar(-10.0, 15.0), 5.0)

    # Requisito 2: Subtração com resultado negativo
    def test_subtracao_com_resultado_negativo(self):
        """Verifica subtração onde o subtraendo é maior que o minuendo."""
        resultado = subtrair(10.0, 25.0)
        self.assertEqual(resultado, -15.0)

    def test_subtracao_numeros_negativos(self):
        """Verifica subtração com números negativos (-5 - (-8) = 3)."""
        resultado = subtrair(-5.0, -8.0)
        self.assertEqual(resultado, 3.0)

    # Requisito 3: Multiplicação por zero
    def test_multiplicacao_por_zero(self):
        """Verifica se a multiplicação por zero resulta em zero (elemento nulo)."""
        self.assertEqual(multiplicar(100.0, 0.0), 0.0)
        self.assertEqual(multiplicar(0.0, -50.0), 0.0)

    def test_multiplicacao_numeros_positivos_e_negativos(self):
        """Verifica o produto entre números positivos e com regra de sinais."""
        self.assertEqual(multiplicar(6.0, 7.0), 42.0)
        self.assertEqual(multiplicar(6.0, -7.0), -42.0)

    # Requisito 4: Divisão com resultado inteiro
    def test_divisao_com_resultado_inteiro(self):
        """Verifica divisão exata sem fração residual."""
        resultado = dividir(20.0, 4.0)
        self.assertEqual(resultado, 5.0)

    # Requisito 5: Divisão com resultado decimal
    def test_divisao_com_resultado_decimal(self):
        """Verifica divisão que produz número fracionário."""
        resultado = dividir(7.0, 2.0)
        self.assertEqual(resultado, 3.5)

    def test_divisao_zero_por_numero(self):
        """Verifica se 0 dividido por qualquer número diferente de zero resulta em 0."""
        self.assertEqual(dividir(0.0, 10.0), 0.0)

    # Requisito 6: Divisão por zero deve disparar DivisaoPorZeroError
    def test_divisao_por_zero_lanca_excecao(self):
        """Garante que tentar dividir por zero lança DivisaoPorZeroError controlada."""
        with self.assertRaises(DivisaoPorZeroError) as contexto:
            dividir(10.0, 0.0)
        self.assertIn("Não é possível realizar divisão por zero", str(contexto.exception))

    # Requisito 10: Operação inválida não produz resultado válido
    def test_calcular_operacao_invalida_lanca_excecao(self):
        """Verifica que operadores desconhecidos disparam OperacaoInvalidaError."""
        with self.assertRaises(OperacaoInvalidaError):
            calcular(10.0, 2.0, "%")
        with self.assertRaises(OperacaoInvalidaError):
            calcular(10.0, 2.0, "potencia")

    def test_calcular_despacho_correto(self):
        """Verifica o roteamento correto da função calcular() para todas as operações."""
        self.assertEqual(calcular(10.0, 5.0, "+"), 15.0)
        self.assertEqual(calcular(10.0, 5.0, "-"), 5.0)
        self.assertEqual(calcular(10.0, 5.0, "*"), 50.0)
        self.assertEqual(calcular(10.0, 5.0, "/"), 2.0)

    # Requisito 9: Comportamentos numéricos e formatação
    def test_formatar_resultado(self):
        """Verifica formatação amigável: inteiros sem .0 e decimais limpos."""
        self.assertEqual(formatar_resultado(5.0), "5")
        self.assertEqual(formatar_resultado(-12.0), "-12")
        self.assertEqual(formatar_resultado(3.1415), "3.1415")
        # Correção de precisão IEEE 754: 0.1 + 0.2
        self.assertEqual(formatar_resultado(0.1 + 0.2), "0.3")


if __name__ == "__main__":
    unittest.main()
