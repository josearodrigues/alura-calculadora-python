"""
Testes unitários para o controlador da interface gráfica desktop CalculadoraGUI.
"""

import unittest
import tkinter as tk
from unittest.mock import patch
from calculadora.interface import CalculadoraGUI

def ambiente_grafico_indisponivel(erro):
    """Identifica erros causados pela ausência de um servidor gráfico."""
    mensagem = str(erro).lower()

    mensagens_conhecidas = (
        "no display name",
        "couldn't connect to display",
        "window server is not available",
    )

    return any(texto in mensagem for texto in mensagens_conhecidas)


class TestCalculadoraGUI(unittest.TestCase):
    """Testa os métodos do controlador CalculadoraGUI em modo desacoplado."""

    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as erro:
            # Aqui precisamos verificar se a falha
            # realmente decorre da ausência de ambiente gráfico.
            if ambiente_grafico_indisponivel(erro):
                self.skipTest("Ambiente gráfico indisponível.")
            raise

        self.root.withdraw()  # Oculta a janela durante os testes
        self.app = CalculadoraGUI(root=self.root)

    def tearDown(self):
        if hasattr(self, "root") and self.root:
            self.root.destroy()

    def test_inicializacao_padrao(self):
        """Verifica os estados iniciais dos componentes do visor."""
        self.assertEqual(self.app.var_expressao.get(), "")
        self.assertEqual(self.app.var_resultado.get(), "0")
        self.assertIn("Pronta", self.app.var_status.get())

    def test_digitacao_e_calculo(self):
        """Verifica o fluxo de digitação de expressão e execução do cálculo."""
        self.app._adicionar_caractere("1")
        self.app._adicionar_caractere("0")
        self.app._adicionar_operador("+")
        self.app._adicionar_caractere("5")
        self.assertEqual(self.app.var_expressao.get(), "10+5")

        self.app.executar_calculo()
        self.assertEqual(self.app.var_resultado.get(), "15")

    def test_aplicar_raiz_n_com_e_sem_resultado_anterior(self):
        """Verifica a inserção do modelo de raiz enésima nos dois estados."""
        # Sem resultado anterior
        self.app._aplicar_raiz_n()
        self.assertEqual(self.app.var_expressao.get(), "root(")

        # Após um resultado calculado
        self.app.limpar_display()
        self.app.var_expressao.set("25")
        self.app.executar_calculo()

        self.app._aplicar_raiz_n()
        self.assertEqual(self.app.var_expressao.get(), "root(25; ")

    def test_recuperar_historico_atualiza_visores_e_ans(self):
        """Verifica a recuperação de uma entrada e a atualização do ANS."""
        self.app.var_expressao.set("10+5")
        self.app.executar_calculo()
        primeira_entrada = self.app.historico.obter_todos()[0]

        self.app.var_expressao.set("20+5")
        self.app.executar_calculo()
        self.assertEqual(self.app.historico.obter_ans(), 25.0)

        self.app._recuperar_historico_por_id(primeira_entrada.id)

        self.assertEqual(self.app.var_expressao.get(), "10+5")
        self.assertEqual(self.app.var_resultado.get(), "15")
        self.assertEqual(self.app.historico.obter_ans(), 15.0)

    def test_continuidade_apos_recuperar_historico(self):
        """Verifica a continuidade do cálculo após recuperar uma entrada."""
        self.app.var_expressao.set("10+5")
        self.app.executar_calculo()
        entrada = self.app.historico.obter_todos()[0]

        self.app.var_expressao.set("20+5")
        self.app.executar_calculo()

        self.app._recuperar_historico_por_id(entrada.id)
        self.app._adicionar_operador("+")

        self.assertEqual(self.app.var_expressao.get(), "15+")

        self.app._adicionar_caractere("5")
        self.app.executar_calculo()

        self.assertEqual(self.app.var_resultado.get(), "20")

    def test_limpar_historico_preserva_ans(self):
        """Verifica que limpar o histórico mantém o ANS ativo."""
        self.app.var_expressao.set("10+5")
        self.app.executar_calculo()

        self.assertEqual(self.app.historico.obter_ans(), 15.0)
        self.assertEqual(len(self.app.historico.obter_todos()), 1)

        self.app.limpar_historico()

        self.assertEqual(self.app.historico.obter_todos(), [])
        self.assertEqual(self.app.historico.obter_ans(), 15.0)

    def test_mapeamento_atalhos_teclado(self):
        """Verifica o encaminhamento das teclas físicas para as ações da interface."""

        def pressionar(char="", keysym="", state=0):
            evento = tk.Event()
            evento.char = char
            evento.keysym = keysym
            evento.state = state
            self.app._ao_pressionar_tecla(evento)

        with patch.object(self.app, "_adicionar_caractere") as adicionar_caractere, \
            patch.object(self.app, "_adicionar_operador") as adicionar_operador, \
            patch.object(self.app, "executar_calculo") as executar_calculo, \
            patch.object(self.app, "apagar_ultimo_caractere") as apagar, \
            patch.object(self.app, "limpar_display") as limpar, \
            patch.object(self.app, "copiar_resultado") as copiar:

            for digito in "0123456789":
                pressionar(digito, digito)

            for char in ".()^%;":
                pressionar(char, char)

            pressionar(",", "comma")

            for char in "+-*/":
                pressionar(char, char)

            pressionar("", "Return")
            pressionar("", "KP_Enter")
            pressionar("", "BackSpace")
            pressionar("", "Escape")
            pressionar("", "Delete")
            pressionar("c", "c", 0x4)

            caracteres_esperados = list("0123456789") + list(".()^%;") + ["."]
            self.assertEqual(
                [chamada.args[0] for chamada in adicionar_caractere.call_args_list],
                caracteres_esperados,
            )

            self.assertEqual(
                [chamada.args[0] for chamada in adicionar_operador.call_args_list],
                ["+", "-", "×", "÷"],
            )

            self.assertEqual(executar_calculo.call_count, 2)
            apagar.assert_called_once()
            self.assertEqual(limpar.call_count, 2)
            copiar.assert_called_once()

    def test_continuidade_ans_ao_pressionar_operador(self):
        """Verifica que após o cálculo, pressionar operador continua com o resultado."""
        self.app.var_expressao.set("20*2")
        self.app.executar_calculo()
        self.assertEqual(self.app.var_resultado.get(), "40")

        # Pressiona operador '+'
        self.app._adicionar_operador("+")
        self.assertEqual(self.app.var_expressao.get(), "40+")

    def test_limpar_display_preserva_ans(self):
        """Verifica que C limpa o visor mas mantém o ANS no histórico."""
        self.app.var_expressao.set("50+50")
        self.app.executar_calculo()
        self.assertEqual(self.app.var_resultado.get(), "100")

        self.app.limpar_display()
        self.assertEqual(self.app.var_expressao.get(), "")
        self.assertEqual(self.app.var_resultado.get(), "0")
        self.assertEqual(self.app.historico.obter_ans(), 100.0)

    def test_tecla_sem_caractere_nao_altera_expressao(self):
        """Teclas como Shift não devem alterar a expressão."""
        expressao_original = "12+3"
        self.app.var_expressao.set(expressao_original)

        evento = tk.Event()
        evento.char = ""
        evento.keysym = "Shift_L"
        evento.state = 0

        self.app._ao_pressionar_tecla(evento)

        self.assertEqual(
            self.app.var_expressao.get(),
            expressao_original
        )

    def test_memoria_inicia_vazia(self):
        self.assertIsNone(self.app.memoria)


    def test_memoria_armazenar_resultado(self):
        self.app.var_expressao.set("10+5")
        self.app.executar_calculo()

        self.app.memoria_armazenar()

        self.assertEqual(self.app.memoria, 15.0)

    def test_memoria_recuperar_preserva_ans_e_historico(self):
        self.app.var_expressao.set("10+5")
        self.app.executar_calculo()
        self.app.memoria_armazenar()

        self.app.var_expressao.set("20+5")
        self.app.executar_calculo()

        ans_antes_recuperacao = self.app.historico.obter_ans()
        historico_antes_recuperacao = self.app.historico.obter_todos()

        self.app.memoria_recuperar()

        self.assertEqual(self.app.var_expressao.get(), "15")
        self.assertEqual(self.app.var_resultado.get(), "15")
        self.assertEqual(self.app.historico.obter_ans(), ans_antes_recuperacao)
        self.assertEqual(
            self.app.historico.obter_todos(),
            historico_antes_recuperacao
        )

    def test_memoria_somar_com_memoria_vazia(self):
        self.app.var_expressao.set("10+5")
        self.app.executar_calculo()

        self.app.memoria_somar()

        self.assertEqual(self.app.memoria, 15.0)


    def test_memoria_subtrair_com_memoria_vazia(self):
        self.app.var_expressao.set("10+5")
        self.app.executar_calculo()

        self.app.memoria_subtrair()

        self.assertEqual(self.app.memoria, -15.0)

    def test_memoria_somar_com_valor_existente(self):
        self.app.memoria = 10.0
        self.app.var_expressao.set("5+3")
        self.app.executar_calculo()

        self.app.memoria_somar()

        self.assertEqual(self.app.memoria, 18.0)


    def test_memoria_subtrair_com_valor_existente(self):
        self.app.memoria = 10.0
        self.app.var_expressao.set("5+3")
        self.app.executar_calculo()

        self.app.memoria_subtrair()

        self.assertEqual(self.app.memoria, 2.0)

    def test_memoria_limpar(self):
        self.app.memoria = 25.0

        self.app.memoria_limpar()

        self.assertIsNone(self.app.memoria)

    def test_memoria_armazenar_sem_resultado(self):
        self.app.memoria = 10.0

        self.app.memoria_armazenar()

        self.assertEqual(self.app.memoria, 10.0)


    def test_memoria_somar_sem_resultado(self):
        self.app.memoria = 10.0

        self.app.memoria_somar()

        self.assertEqual(self.app.memoria, 10.0)


    def test_memoria_subtrair_sem_resultado(self):
        self.app.memoria = 10.0

        self.app.memoria_subtrair()

        self.assertEqual(self.app.memoria, 10.0)

if __name__ == "__main__":
    unittest.main()
