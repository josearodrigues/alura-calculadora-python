"""
Testes unitários para o controlador da interface gráfica desktop CalculadoraGUI.
"""

import unittest
from calculadora.interface import CalculadoraGUI


class TestCalculadoraGUI(unittest.TestCase):
    """Testa os métodos do controlador CalculadoraGUI em modo desacoplado."""

    def setUp(self):
        try:
            import tkinter as tk
            self.root = tk.Tk()
            self.root.withdraw()  # Oculta a janela durante os testes
            self.app = CalculadoraGUI(root=self.root)
        except Exception:
            self.skipTest("Ambiente gráfico Tkinter não disponível para teste headless.")

    def tearDown(self):
        if hasattr(self, "root") and self.root:
            try:
                self.root.destroy()
            except Exception:
                pass

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


if __name__ == "__main__":
    unittest.main()
