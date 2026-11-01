"""
Testes unitários para o módulo calculadora.operacoes.

Cobre as 4 operações básicas originais e as novas operações matemáticas da versão 2.1:
potenciação, raiz quadrada, raiz de índice n (incluindo números negativos com índice ímpar,
índices negativos e fracionários), valor absoluto, inverso, troca de sinal, além de
proteções contra overflow, divisão por zero e números complexos.
"""

import math
import unittest
from calculadora.operacoes import (
    DivisaoPorZeroError,
    ErroAritmetico,
    OperacaoInvalidaError,
    RadicandoNegativoError,
    _assegurar_numero_valido,
    calcular,
    dividir,
    formatar_resultado,
    inverso,
    multiplicar,
    potencia,
    raiz_n,
    raiz_quadrada,
    somar,
    subtrair,
    trocar_sinal,
    valor_absoluto,
)


class TestOperacoesMatematicas(unittest.TestCase):
    """Suíte de testes para funções de cálculo aritmético."""

    # -----------------------------------------------------------------------
    # Testes Originais da Baseline (Preservados Integralmente)
    # -----------------------------------------------------------------------

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
        # Suporte ao operador ^ no dispatch
        self.assertEqual(calcular(2.0, 3.0, "^"), 8.0)

    # Requisito 9: Comportamentos numéricos e formatação
    def test_formatar_resultado(self):
        """Verifica formatação amigável: inteiros sem .0 e decimais limpos."""
        self.assertEqual(formatar_resultado(5.0), "5")
        self.assertEqual(formatar_resultado(-12.0), "-12")
        self.assertEqual(formatar_resultado(3.1415), "3.1415")
        # Correção de precisão IEEE 754: 0.1 + 0.2
        self.assertEqual(formatar_resultado(0.1 + 0.2), "0.3")

    # -----------------------------------------------------------------------
    # Novos Testes — Fase 1 (Calculadora 2.1)
    # -----------------------------------------------------------------------

    def test_potencia_casos_reais(self):
        """Verifica potenciação com expoentes inteiros, negativos e zero."""
        self.assertEqual(potencia(2.0, 3.0), 8.0)
        self.assertEqual(potencia(2.0, 10.0), 1024.0)
        self.assertEqual(potencia(5.0, 0.0), 1.0)
        self.assertEqual(potencia(2.0, -2.0), 0.25)
        self.assertEqual(potencia(-2.0, 3.0), -8.0)
        self.assertEqual(potencia(-2.0, 4.0), 16.0)

    def test_potencia_casos_invalidos(self):
        """Verifica que zero elevado a negativo e base negativa com expoente fracionário são rejeitados."""
        with self.assertRaises(DivisaoPorZeroError):
            potencia(0.0, -1.0)
        with self.assertRaises(RadicandoNegativoError):
            potencia(-4.0, 0.5)

    def test_raiz_quadrada(self):
        """Verifica raiz quadrada com valores exatos, decimais e rejeição de negativos."""
        self.assertEqual(raiz_quadrada(144.0), 12.0)
        self.assertEqual(raiz_quadrada(0.0), 0.0)
        self.assertAlmostEqual(raiz_quadrada(2.0), math.sqrt(2.0))
        with self.assertRaises(RadicandoNegativoError):
            raiz_quadrada(-1.0)

    def test_raiz_n_casos_reais_positivos(self):
        """Verifica raiz n com radicando positivo para índices inteiros e fracionários."""
        self.assertEqual(raiz_n(8.0, 3.0), 2.0)
        self.assertEqual(raiz_n(16.0, 4.0), 2.0)
        self.assertEqual(raiz_n(8.0, 0.5), 64.0)  # 8^(1/0.5) = 8^2 = 64
        self.assertEqual(raiz_n(16.0, 0.25), 65536.0)  # 16^4 = 65536
        self.assertEqual(raiz_n(0.0, 3.0), 0.0)

    def test_raiz_n_radicando_negativo_indice_impar(self):
        """Verifica que radicando negativo com índice inteiro ímpar retorna resultado real negativo."""
        self.assertEqual(raiz_n(-8.0, 3.0), -2.0)
        self.assertEqual(raiz_n(-32.0, 5.0), -2.0)
        self.assertEqual(raiz_n(-1.0, 7.0), -1.0)

    def test_raiz_n_indice_negativo(self):
        """Verifica raiz n com índice negativo por inversão aritmética."""
        self.assertEqual(raiz_n(8.0, -3.0), 0.5)  # 8^(-1/3) = 1/2 = 0.5
        self.assertEqual(raiz_n(-8.0, -3.0), -0.5)  # -8^(-1/3) = 1/-2 = -0.5

    def test_raiz_n_casos_invalidos(self):
        """Verifica que índice zero, índice não inteiro com radicando negativo e raiz de zero com exp negativo falham."""
        with self.assertRaises(OperacaoInvalidaError):
            raiz_n(5.0, 0.0)
        with self.assertRaises(RadicandoNegativoError):
            raiz_n(-8.0, 2.0)  # Índice par
        with self.assertRaises(RadicandoNegativoError):
            raiz_n(-8.0, 3.5)  # Índice fracionário com radicando negativo
        with self.assertRaises(RadicandoNegativoError):
            raiz_n(-8.0, 0.5)
        with self.assertRaises(DivisaoPorZeroError):
            raiz_n(0.0, -3.0)

    def test_valor_absoluto(self):
        """Verifica valor absoluto para positivos, negativos e zero."""
        self.assertEqual(valor_absoluto(42.0), 42.0)
        self.assertEqual(valor_absoluto(-42.0), 42.0)
        self.assertEqual(valor_absoluto(0.0), 0.0)

    def test_inverso(self):
        """Verifica o inverso aritmético (1/x) e proteção contra divisão por zero."""
        self.assertEqual(inverso(4.0), 0.25)
        self.assertEqual(inverso(-2.0), -0.5)
        with self.assertRaises(DivisaoPorZeroError):
            inverso(0.0)

    def test_trocar_sinal(self):
        """Verifica a inversão algébrica de sinal (-x)."""
        self.assertEqual(trocar_sinal(5.0), -5.0)
        self.assertEqual(trocar_sinal(-3.14), 3.14)
        self.assertEqual(trocar_sinal(0.0), 0.0)

    def test_overflow_aritmetico(self):
        """Verifica que estouro de ponto flutuante IEEE 754 levanta ErroAritmetico controlado."""
        with self.assertRaises(ErroAritmetico):
            potencia(1e200, 2.0)
        with self.assertRaises(ErroAritmetico):
            multiplicar(1e308, 10.0)
        with self.assertRaises(ErroAritmetico):
            somar(1e308, 1e308)

    def test_assegurar_numero_valido_com_inteiro_excessivamente_grande(self):
        """Garante que inteiro gigante (> float max) dispara ErroAritmetico por OverflowError na conversão."""
        inteiro_gigante = 10 ** 1000
        with self.assertRaises(ErroAritmetico) as ctx:
            _assegurar_numero_valido(inteiro_gigante)
        self.assertIn("Overflow", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
