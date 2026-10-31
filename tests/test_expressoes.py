"""
Testes unitários exaustivos para o módulo calculadora.expressoes.

Valida a gramática EBNF, precedência matemática formal (ex.: -2^2 = -4),
associatividade à direita para potências (2^3^2 = 512), resolução contextual
de percentual, funções matemáticas seguras (sqrt, root, abs, inv), continuidade
com ANS, delimitação estrita de raiz quadrada e proteção completa contra injeção
de código arbitrário e estouro de limites.
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
    RadicandoNegativoError,
)
from calculadora.validacao import ErroValidacao


class TestAvaliadorExpressoes(unittest.TestCase):
    """Suíte de testes para o motor de expressões matemáticas."""

    # -----------------------------------------------------------------------
    # 1. Operações Básicas e Precedência Tradicional
    # -----------------------------------------------------------------------

    def test_operacoes_basicas_e_precedencia(self):
        """Verifica quatro operações básicas e precedência multiplicativa natural."""
        self.assertEqual(avaliar_expressao("2 + 3"), 5.0)
        self.assertEqual(avaliar_expressao("10 - 4"), 6.0)
        self.assertEqual(avaliar_expressao("6 * 7"), 42.0)
        self.assertEqual(avaliar_expressao("20 / 4"), 5.0)
        self.assertEqual(avaliar_expressao("2 + 3 * 4"), 14.0)
        self.assertEqual(avaliar_expressao("(2 + 3) * 4"), 20.0)
        self.assertEqual(avaliar_expressao("10 - 3 + 2"), 9.0)
        self.assertEqual(avaliar_expressao("20 / 2 * 5"), 50.0)

    # -----------------------------------------------------------------------
    # 2. Precedência de Potenciação e Sinais Unários (Mandatório)
    # -----------------------------------------------------------------------

    def test_precedencia_unario_e_potencia(self):
        """
        Garante que a potenciação tem precedência sobre o sinal unário negativo:
        -2^2 = -(2^2) = -4.0
        (-2)^2 = 4.0
        """
        self.assertEqual(avaliar_expressao("-2^2"), -4.0)
        self.assertEqual(avaliar_expressao("(-2)^2"), 4.0)
        self.assertEqual(avaliar_expressao("-2^3"), -8.0)
        self.assertEqual(avaliar_expressao("-(2+3)^2"), -25.0)
        self.assertEqual(avaliar_expressao("2^-2"), 0.25)
        self.assertEqual(avaliar_expressao("+5"), 5.0)

    def test_associatividade_a_direita_da_potencia(self):
        """Verifica associatividade à direita: 2^3^2 = 2^(3^2) = 2^9 = 512."""
        self.assertEqual(avaliar_expressao("2^3^2"), 512.0)
        self.assertEqual(avaliar_expressao("-2^3^2"), -512.0)
        self.assertEqual(avaliar_expressao("(2^3)^2"), 64.0)

    # -----------------------------------------------------------------------
    # 3. Percentual Contextual e Agrupamentos (Regras Aprovadas)
    # -----------------------------------------------------------------------

    def test_percentual_contextual_aditivo_e_subtrativo(self):
        """Verifica semântica contextual de base: 400 + 10% = 440; 400 - 10% = 360."""
        self.assertEqual(avaliar_expressao("400 + 10%"), 440.0)
        self.assertEqual(avaliar_expressao("400 - 10%"), 360.0)

    def test_percentual_multiplicativo_e_divisivo(self):
        """Verifica percentual fracionário em produto e quociente."""
        self.assertEqual(avaliar_expressao("200 * 10%"), 20.0)
        self.assertEqual(avaliar_expressao("200 / 10%"), 2000.0)

    def test_expressao_mockup_calculadora_2_0(self):
        """Verifica a expressão de referência do mockup: (125 + 75) * 2 + 10% = 440.0."""
        self.assertEqual(avaliar_expressao("(125 + 75) * 2 + 10%"), 440.0)
        # Com caracteres visuais tipográficos de multiplicação
        self.assertEqual(avaliar_expressao("(125 + 75) × 2 + 10%"), 440.0)

    def test_percentuais_encadeados_sucessivos(self):
        """Verifica encadeamento: 100 + 10% + 10% = (110) + 10% = 121.0."""
        self.assertEqual(avaliar_expressao("100 + 10% + 10%"), 121.0)

    def test_percentual_respeita_precedencia_multiplicativa(self):
        """Verifica que 100 + 2 * 10% = 100 + (2 * 0.10) = 100.2."""
        self.assertEqual(avaliar_expressao("100 + 2 * 10%"), 100.2)

    def test_percentual_com_agrupamento(self):
        """
        Verifica que parênteses delimitam o escopo do percentual:
        100 + (10%) = 100 + 0.10 = 100.1
        100 + (5 + 5)% = 100 + 10 = 110.0 (taxa agrupada aplicada à base externa 100)
        (100 + 10%) * 2 = 110 * 2 = 220.0
        """
        self.assertEqual(avaliar_expressao("100 + (10%)"), 100.1)
        self.assertEqual(avaliar_expressao("100 + (5 + 5)%"), 110.0)
        self.assertEqual(avaliar_expressao("(100 + 10%) * 2"), 220.0)

    def test_percentual_isolado_e_termo_inicial(self):
        """Verifica percentual simples isolado."""
        self.assertEqual(avaliar_expressao("10%"), 0.10)
        self.assertEqual(avaliar_expressao("(10%)"), 0.10)
        self.assertEqual(avaliar_expressao("10% + 20"), 20.10)

    # -----------------------------------------------------------------------
    # 4. Funções Matemáticas Seguras e Escopo da Raiz Quadrada
    # -----------------------------------------------------------------------

    def test_escopo_raiz_quadrada(self):
        """
        Garante delimitação exata:
        sqrt(9 + 16) = 5.0
        sqrt(9) + 16 = 19.0
        √(9 + 16) = 5.0
        √9 + 16 = 19.0
        """
        self.assertEqual(avaliar_expressao("sqrt(9 + 16)"), 5.0)
        self.assertEqual(avaliar_expressao("sqrt(9) + 16"), 19.0)
        self.assertEqual(avaliar_expressao("√(9 + 16)"), 5.0)
        self.assertEqual(avaliar_expressao("√9 + 16"), 19.0)
        self.assertEqual(avaliar_expressao("√144"), 12.0)
        self.assertEqual(avaliar_expressao("√144 * 2"), 24.0)

    def test_raiz_n_sintaxe_e_casos_reais(self):
        """Verifica chamadas da função root(radicando; indice)."""
        self.assertEqual(avaliar_expressao("root(8; 3)"), 2.0)
        self.assertEqual(avaliar_expressao("root(-8; 3)"), -2.0)
        self.assertEqual(avaliar_expressao("root(8; -3)"), 0.5)
        self.assertEqual(avaliar_expressao("root(-8; -3)"), -0.5)
        self.assertEqual(avaliar_expressao("root(8; 0.5)"), 64.0)

        # Suporte a vírgula decimal com ponto e vírgula separador
        self.assertAlmostEqual(avaliar_expressao("root(12,5; 3)"), 12.5 ** (1.0 / 3.0))

    def test_separador_argumentos_exclusivamente_ponto_e_virgula(self):
        """Garante que vírgula solta como separador de argumento é rejeitada e apenas ';' é aceito."""
        # Com ponto e vírgula: aceito
        self.assertEqual(avaliar_expressao("root(8; 3)"), 2.0)

        # Com vírgula como separador: rejeitado com ExpressaoInvalidaError
        with self.assertRaises(ExpressaoInvalidaError) as ctx:
            avaliar_expressao("root(8, 3)")
        self.assertIn("ponto e vírgula ';'", str(ctx.exception))

    def test_funcoes_unarias_abs_e_inv(self):
        """Verifica abs() e inv()."""
        self.assertEqual(avaliar_expressao("abs(-42)"), 42.0)
        self.assertEqual(avaliar_expressao("abs(42)"), 42.0)
        self.assertEqual(avaliar_expressao("inv(4)"), 0.25)
        self.assertEqual(avaliar_expressao("inv(-2)"), -0.5)

    # -----------------------------------------------------------------------
    # 5. Continuidade com ANS
    # -----------------------------------------------------------------------

    def test_continuidade_com_ans(self):
        """Verifica a resolução do identificador ANS."""
        self.assertEqual(avaliar_expressao("ANS + 60", ans=440.0), 500.0)
        self.assertEqual(avaliar_expressao("ANS + 5%", ans=400.0), 420.0)
        self.assertEqual(avaliar_expressao("ans * 2", ans=15.0), 30.0)

        # Sem valor de ANS disponível levanta ExpressaoInvalidaError
        with self.assertRaises(ExpressaoInvalidaError) as ctx:
            avaliar_expressao("ANS + 10", ans=None)
        self.assertIn("nenhum resultado anterior está disponível", str(ctx.exception))

    # -----------------------------------------------------------------------
    # 6. Segurança, Rejeição de Injeções e Limites
    # -----------------------------------------------------------------------

    def test_rejeicao_de_injecoes_de_codigo(self):
        """Garante que qualquer tentativa de execução de código Python seja rejeitada."""
        entradas_maliciosas = [
            "__import__('os').system('ls')",
            "exec('import os')",
            "open('/etc/passwd')",
            "eval('1+1')",
            "lambda x: x",
            "[x for x in range(10)]",
            "1 + 1; import sys",
            "math.sqrt(4)",  # Ponto não é atributo em identificador
        ]
        for payload in entradas_maliciosas:
            with self.assertRaises(ExpressaoInvalidaError):
                avaliar_expressao(payload)

    def test_rejeicao_de_funcoes_nao_autorizadas(self):
        """Verifica que funções fora do catálogo autorizado são rejeitadas."""
        with self.assertRaises(ExpressaoInvalidaError) as ctx:
            avaliar_expressao("sin(30)")
        self.assertIn("não autorizada", str(ctx.exception))

        with self.assertRaises(ExpressaoInvalidaError):
            avaliar_expressao("cos(0)")

    def test_validacao_de_aridade_de_funcoes(self):
        """Verifica que aridade incorreta dispara ExpressaoInvalidaError."""
        with self.assertRaises(ExpressaoInvalidaError):
            avaliar_expressao("sqrt(4; 2)")  # sqrt requer 1 argumento
        with self.assertRaises(ExpressaoInvalidaError):
            avaliar_expressao("root(8)")     # root requer 2 argumentos

    def test_expressoes_vazias_ou_excedendo_tamanho(self):
        """Verifica rejeição de string vazia e string excedendo 200 caracteres."""
        with self.assertRaises(ExpressaoInvalidaError):
            avaliar_expressao("")
        with self.assertRaises(ExpressaoInvalidaError):
            avaliar_expressao("   ")

        expressao_longa = "1 + " * 70  # Mais de 200 chars
        with self.assertRaises(ExpressaoInvalidaError):
            avaliar_expressao(expressao_longa)

    def test_profundidade_aninhamento_excessiva(self):
        """Verifica barreira contra aninhamento excessivo de parênteses (> 50 níveis)."""
        expr_profunda = "(" * 52 + "1" + ")" * 52
        with self.assertRaises(ExpressaoInvalidaError):
            avaliar_expressao(expr_profunda)

    def test_divisao_por_zero_em_expressao(self):
        """Verifica que 1/0 dentro de expressão levanta DivisaoPorZeroError."""
        with self.assertRaises(DivisaoPorZeroError):
            avaliar_expressao("10 / 0")
        with self.assertRaises(DivisaoPorZeroError):
            avaliar_expressao("(125 + 75) / (5 - 5)")

    def test_erros_aritmeticos_e_overflow(self):
        """Verifica que overflow em expressões levanta ErroAritmetico controlado."""
        with self.assertRaises(ErroAritmetico):
            avaliar_expressao("1e200 * 1e200")


if __name__ == "__main__":
    unittest.main()
