"""
Testes unitários para o módulo calculadora.historico.

Cobre a criação de registros, geração sequencial de IDs, preservação cronológica,
recuperação de entradas anteriores com atualização do ANS ativo, proteção contra
IDs inexistentes e a independência de estado entre limpeza do histórico e o ANS.
"""

import time
import unittest
from calculadora.historico import (
    EntradaHistorico,
    HistoricoSessao,
    RegistroNaoEncontradoError,
)


class TestHistoricoSessao(unittest.TestCase):
    """Suíte de testes para a gestão de histórico de cálculos e estado do ANS."""

    def setUp(self):
        """Inicializa uma nova sessão de histórico para cada teste."""
        self.historico = HistoricoSessao()

    def test_sessao_inicia_vazia_com_ans_nulo(self):
        """Verifica que uma nova sessão não possui entradas e o ANS é None."""
        self.assertEqual(len(self.historico.obter_todos()), 0)
        self.assertIsNone(self.historico.obter_ans())

    def test_registrar_calculos_incrementa_ids_e_atualiza_ans(self):
        """Verifica registro ordenado com IDs incrementais e atualização do ANS."""
        entrada1 = self.historico.registrar("10 + 20", "10 + 20", 30.0)
        self.assertEqual(entrada1.id, 1)
        self.assertEqual(entrada1.expressao, "10 + 20")
        self.assertEqual(entrada1.resultado, 30.0)
        self.assertEqual(entrada1.resultado_formatado, "30")
        self.assertEqual(self.historico.obter_ans(), 30.0)

        entrada2 = self.historico.registrar("30 * 2", "30 * 2", 60.0)
        self.assertEqual(entrada2.id, 2)
        self.assertEqual(self.historico.obter_ans(), 60.0)

        todas = self.historico.obter_todos()
        self.assertEqual(len(todas), 2)
        self.assertEqual(todas[0].id, 1)
        self.assertEqual(todas[1].id, 2)

    def test_recuperar_entrada_existente_atualiza_ans_ativo(self):
        """Verifica que recuperar uma entrada pelo ID redefine o ANS ativo para aquele resultado."""
        self.historico.registrar("10 + 10", "10 + 10", 20.0)   # ID 1
        self.historico.registrar("20 * 2", "20 * 2", 40.0)     # ID 2
        self.historico.registrar("40 + 60", "40 + 60", 100.0)  # ID 3

        # O ANS atual é 100.0
        self.assertEqual(self.historico.obter_ans(), 100.0)

        # Recupera a entrada #1 (resultado 20.0)
        entrada_recuperada = self.historico.recuperar_entrada(1)
        self.assertEqual(entrada_recuperada.id, 1)
        self.assertEqual(entrada_recuperada.resultado, 20.0)

        # O ANS ativo agora deve ser 20.0
        self.assertEqual(self.historico.obter_ans(), 20.0)

        # Recupera a entrada #2 (resultado 40.0)
        entrada_2 = self.historico.recuperar_entrada(2)
        self.assertEqual(entrada_2.resultado, 40.0)
        self.assertEqual(self.historico.obter_ans(), 40.0)

    def test_recuperar_entrada_inexistente_lanca_excecao(self):
        """Verifica que tentar recuperar um ID inexistente levanta RegistroNaoEncontradoError."""
        self.historico.registrar("5 + 5", "5 + 5", 10.0)
        with self.assertRaises(RegistroNaoEncontradoError) as ctx:
            self.historico.recuperar_entrada(999)
        self.assertIn("#999", str(ctx.exception))

        with self.assertRaises(RegistroNaoEncontradoError):
            self.historico.recuperar_entrada(0)

    def test_limpar_historico_preserva_ans_ativo_obrigatoriamente(self):
        """
        REGRA MANDATÓRIA: Limpar o histórico esvazia a lista de entradas visíveis,
        mas PRESERVA integralmente o valor numérico do ANS para continuidade de cálculo.
        """
        self.historico.registrar("125 + 75", "125 + 75", 200.0)
        self.historico.registrar("200 * 2 + 10%", "(200 * 2) + 10%", 440.0)

        self.assertEqual(len(self.historico.obter_todos()), 2)
        self.assertEqual(self.historico.obter_ans(), 440.0)

        # Ação de limpeza do histórico
        self.historico.limpar_historico()

        # A lista de entradas deve estar vazia
        self.assertEqual(len(self.historico.obter_todos()), 0)

        # O ANS ativo DEVE permanecer 440.0 intacto
        self.assertEqual(self.historico.obter_ans(), 440.0)

    def test_resetar_sessao_zera_historico_e_ans(self):
        """Verifica que resetar_sessao() zera o histórico e redefine o ANS para None."""
        self.historico.registrar("50 + 50", "50 + 50", 100.0)
        self.assertEqual(self.historico.obter_ans(), 100.0)

        self.historico.resetar_sessao()

        self.assertEqual(len(self.historico.obter_todos()), 0)
        self.assertIsNone(self.historico.obter_ans())

        # Novo registro após reset deve recomeçar do ID 1
        nova_entrada = self.historico.registrar("1 + 1", "1 + 1", 2.0)
        self.assertEqual(nova_entrada.id, 1)
        self.assertEqual(self.historico.obter_ans(), 2.0)


    def test_entrada_historico_e_imutavel(self):
        """Garante que instâncias de EntradaHistorico são imutáveis (frozen=True)."""
        from dataclasses import FrozenInstanceError
        entrada = self.historico.registrar("2 + 2", "2 + 2", 4.0)
        with self.assertRaises(FrozenInstanceError):
            entrada.resultado = 999.0
        with self.assertRaises(FrozenInstanceError):
            entrada.expressao = "modificada"


if __name__ == "__main__":
    unittest.main()
