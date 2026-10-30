"""
Testes de integração para o fluxo de dados da calculadora.

Verifica o pipeline completo:
Entrada textual do usuário -> Validação e Conversão -> Cálculo Aritmético -> Formatação de Saída.
"""

import unittest
from calculadora.operacoes import (
    calcular,
    formatar_resultado,
    DivisaoPorZeroError,
    OperacaoInvalidaError,
)
from calculadora.validacao import (
    converter_operando,
    ErroValidacao,
)


class TestIntegracaoFluxoCompleto(unittest.TestCase):
    """Testa a integração entre a camada de validação e a camada de operações."""

    def executar_fluxo(self, entrada_a: str, entrada_b: str, operacao: str) -> str:
        """
        Emula a sequência exata de chamadas executada pela interface gráfica.
        """
        # Passo 1: Validação
        a_num = converter_operando(entrada_a, nome_campo="Operando A")
        b_num = converter_operando(entrada_b, nome_campo="Operando B")

        # Passo 2: Cálculo
        resultado_bruto = calcular(a_num, b_num, operacao)

        # Passo 3: Formatação
        return formatar_resultado(resultado_bruto)

    def test_fluxo_sucesso_com_virgulas_e_espacos(self):
        """Verifica fluxo completo com entradas que necessitam de sanitização e normalização."""
        # ' 12,5 ' * ' 2 ' = 25
        resultado = self.executar_fluxo("  12,5  ", "  2  ", "*")
        self.assertEqual(resultado, "25")

    def test_fluxo_sucesso_divisao_decimal(self):
        """Verifica fluxo de divisão com resultado decimal formatado."""
        resultado = self.executar_fluxo("7", "2", "/")
        self.assertEqual(resultado, "3.5")

    def test_fluxo_erro_validacao_interrompe_antes_do_calculo(self):
        """Garante que erro no primeiro operando interrompe o fluxo com ErroValidacao."""
        with self.assertRaises(ErroValidacao) as ctx:
            self.executar_fluxo("texto_invalido", "10", "+")
        self.assertIn("Operando A", str(ctx.exception))

    def test_fluxo_erro_divisao_por_zero_apos_validacao(self):
        """
        Garante que valores válidos passam pela validação, mas a divisão por zero
        é interceptada pela camada matemática.
        """
        with self.assertRaises(DivisaoPorZeroError) as ctx:
            self.executar_fluxo("100", "0", "/")
        self.assertIn("Não é possível realizar divisão por zero", str(ctx.exception))

    def test_fluxo_soma_com_zero_como_operando_legitimo(self):
        """Verifica que o número zero passa pelo fluxo completo sem ser bloqueado."""
        resultado = self.executar_fluxo("0", "15.4", "+")
        self.assertEqual(resultado, "15.4")


if __name__ == "__main__":
    unittest.main()
