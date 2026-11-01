"""
Testes unitários para o controlador da interface gráfica desktop CalculadoraGUI.
"""

import unittest
import tkinter as tk
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
