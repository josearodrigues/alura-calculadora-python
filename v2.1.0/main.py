"""
Ponto de entrada (Entrypoint) da aplicação Calculadora Python.

Executa a inicialização do Tkinter e inicia o laço de eventos da interface.
"""
import sys


def main() -> None:
    """Função principal de inicialização da calculadora."""
    try:
        import tkinter as tk
        from calculadora.interface import CalculadoraGUI

        app = CalculadoraGUI()
        print("Iniciando a Calculadora Modular Python...")
        app.iniciar()
    except (ImportError, ModuleNotFoundError) as erro_modulo:
        print("\n" + "=" * 60)
        print("AVISO DE AMBIENTE: Pacote Tkinter não instalado neste sistema Linux.")
        print("O Tkinter é uma biblioteca gráfica incluída por padrão no Python")
        print("para Windows e macOS, e instalável via 'sudo apt install python3-tk' no Linux.")
        print(f"Detalhes: {erro_modulo}")
        print("\nPara executar a interface visual completa:")
        print("1. Execute este projeto na sua máquina desktop local:")
        print("   python main.py")
        print("2. Para rodar a suíte de testes automatizados sem precisar de interface:")
        print("   python -m unittest discover tests -v")
        print("=" * 60 + "\n")
        sys.exit(0)
    except Exception as erro_tcl:
        print("\n" + "=" * 60)
        print("AVISO DE AMBIENTE GRÁFICO (DISPLAY):")
        print("O Tkinter requer um monitor/display X11 ativo para renderizar janelas.")
        print(f"Detalhes: {erro_tcl}")
        print("\nExecute localmente na sua máquina: python main.py")
        print("=" * 60 + "\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
