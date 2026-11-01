"""
Testes de integração para o fluxo de dados da calculadora.

Verifica o pipeline completo:
1. Entrada textual do usuário -> Validação e Conversão -> Cálculo Aritmético -> Formatação de Saída (Baseline).
2. Avaliação de expressões matemáticas encadeadas -> Formatação de Saída (Fase 1).
"""

import unittest
from calculadora.expressoes import (
    ExpressaoInvalidaError,
    avaliar_expressao,
)
from calculadora.operacoes import (
    DivisaoPorZeroError,
    ErroAritmetico,
    OperacaoInvalidaError,
    calcular,
    formatar_resultado,
)
from calculadora.validacao import (
    ErroValidacao,
    converter_operando,
)


class TestIntegracaoFluxoCompleto(unittest.TestCase):
    """Testa a integração entre as camadas de validação, operações e expressões."""

    def executar_fluxo_legado(self, entrada_a: str, entrada_b: str, operacao: str) -> str:
        """
        Emula a sequência exata de chamadas executada pela interface gráfica legado.
        """
        # Passo 1: Validação
        a_num = converter_operando(entrada_a, nome_campo="Operando A")
        b_num = converter_operando(entrada_b, nome_campo="Operando B")

        # Passo 2: Cálculo
        resultado_bruto = calcular(a_num, b_num, operacao)

        # Passo 3: Formatação
        return formatar_resultado(resultado_bruto)

    # -----------------------------------------------------------------------
    # Testes Originais da Baseline (Preservados Integralmente)
    # -----------------------------------------------------------------------

    def test_fluxo_sucesso_com_virgulas_e_espacos(self):
        """Verifica fluxo completo com entradas que necessitam de sanitização e normalização."""
        # ' 12,5 ' * ' 2 ' = 25
        resultado = self.executar_fluxo_legado("  12,5  ", "  2  ", "*")
        self.assertEqual(resultado, "25")

    def test_fluxo_sucesso_divisao_decimal(self):
        """Verifica fluxo de divisão com resultado decimal formatado."""
        resultado = self.executar_fluxo_legado("7", "2", "/")
        self.assertEqual(resultado, "3.5")

    def test_fluxo_erro_validacao_interrompe_antes_do_calculo(self):
        """Garante que erro no primeiro operando interrompe o fluxo com ErroValidacao."""
        with self.assertRaises(ErroValidacao) as ctx:
            self.executar_fluxo_legado("texto_invalido", "10", "+")
        self.assertIn("Operando A", str(ctx.exception))

    def test_fluxo_erro_divisao_por_zero_apos_validacao(self):
        """
        Garante que valores válidos passam pela validação, mas a divisão por zero
        é interceptada pela camada matemática.
        """
        with self.assertRaises(DivisaoPorZeroError) as ctx:
            self.executar_fluxo_legado("100", "0", "/")
        self.assertIn("Não é possível realizar divisão por zero", str(ctx.exception))

    def test_fluxo_soma_com_zero_como_operando_legitimo(self):
        """Verifica que o número zero passa pelo fluxo completo sem ser bloqueado."""
        resultado = self.executar_fluxo_legado("0", "15.4", "+")
        self.assertEqual(resultado, "15.4")

    # -----------------------------------------------------------------------
    # Novos Testes de Integração — Fase 1 (Calculadora 2.1)
    # -----------------------------------------------------------------------

    def test_fluxo_expressao_mockup_completo(self):
        """Verifica o pipeline da expressão principal do mockup formatada para o visor."""
        res_num = avaliar_expressao("(125 + 75) * 2 + 10%")
        res_formatado = formatar_resultado(res_num)
        self.assertEqual(res_formatado, "440")

    def test_fluxo_expressao_com_raiz_e_continuidade(self):
        """Verifica fluxo encadeado de raiz quadrada com ANS acumulado."""
        # Passo 1: calcula raiz quadrada de 144
        ans1 = avaliar_expressao("√144")
        self.assertEqual(formatar_resultado(ans1), "12")

        # Passo 2: continua a partir de ANS (+ 88)
        ans2 = avaliar_expressao("ANS + 88", ans=ans1)
        self.assertEqual(formatar_resultado(ans2), "100")

        # Passo 3: aplica percentual contextual sobre ANS
        ans3 = avaliar_expressao("ANS + 10%", ans=ans2)
        self.assertEqual(formatar_resultado(ans3), "110")


if __name__ == "__main__":
    unittest.main()
