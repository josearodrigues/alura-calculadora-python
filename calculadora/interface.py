"""
Módulo de interface gráfica com o usuário (GUI) utilizando Tkinter nativo.

Este módulo é responsável exclusivamente pela camada de apresentação (View/Controller).
Ele constrói a janela visual, posiciona os elementos (widgets), escuta os eventos
de interação do usuário (cliques e teclado) e delega a validação e o cálculo
para os módulos especializados (validacao.py e operacoes.py).
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional

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


class CalculadoraGUI:
    """
    Classe controladora da interface gráfica da Calculadora.

    Encapsula o ciclo de vida dos componentes visuais do Tkinter e
    gerencia o fluxo de dados entre a tela e os módulos de lógica.
    """

    def __init__(self, root: Optional[tk.Tk] = None) -> None:
        """
        Inicializa a interface gráfica, configura a janela e monta os widgets.

        Parâmetros:
            root (Optional[tk.Tk]): Instância raiz do Tkinter. Se omitida,
                                    uma nova instância tk.Tk() será criada.
        """
        self.root = root if root is not None else tk.Tk()
        self._configurar_janela()

        # Variáveis de controle observáveis do Tkinter
        self.var_operando_a = tk.StringVar()
        self.var_operando_b = tk.StringVar()
        self.var_operacao = tk.StringVar(value="+")
        self.var_resultado = tk.StringVar(value="")
        self.var_mensagem_erro = tk.StringVar(value="")

        self._construir_widgets()

    def _configurar_janela(self) -> None:
        """Define título, dimensões, cores e comportamento de redimensionamento da janela."""
        self.root.title("Calculadora - Engenharia de Software")
        self.root.geometry("420x520")
        self.root.minsize(380, 480)
        self.root.configure(bg="#F3F4F6")  # Fundo cinza suave neutro

    def _construir_widgets(self) -> None:
        """Cria e organiza todos os elementos visuais na janela usando grid e pack."""
        # Container principal com margens (padding)
        container = tk.Frame(self.root, bg="#F3F4F6", padx=20, pady=20)
        container.pack(fill=tk.BOTH, expand=True)

        # Cabeçalho / Título da Aplicação
        lbl_titulo = tk.Label(
            container,
            text="Calculadora Modular",
            font=("Helvetica", 16, "bold"),
            bg="#F3F4F6",
            fg="#111827",
        )
        lbl_titulo.pack(pady=(0, 4))

        lbl_subtitulo = tk.Label(
            container,
            text="Práticas de Engenharia de Software em Python",
            font=("Helvetica", 9),
            bg="#F3F4F6",
            fg="#6B7280",
        )
        lbl_subtitulo.pack(pady=(0, 16))

        # Card do Formulário (painel branco com borda sutil)
        form_frame = tk.Frame(container, bg="#FFFFFF", padx=16, pady=16, relief=tk.RIDGE, bd=1)
        form_frame.pack(fill=tk.X, pady=(0, 12))

        # --- Campo 1: Operando A ---
        lbl_op_a = tk.Label(
            form_frame,
            text="Primeiro Número (Operando A):",
            font=("Helvetica", 10, "bold"),
            bg="#FFFFFF",
            fg="#374151",
            anchor="w",
        )
        lbl_op_a.pack(fill=tk.X, pady=(0, 4))

        self.entry_a = tk.Entry(
            form_frame,
            textvariable=self.var_operando_a,
            font=("Helvetica", 12),
            bd=1,
            relief=tk.SOLID,
            highlightthickness=1,
            highlightcolor="#2563EB",
        )
        self.entry_a.pack(fill=tk.X, pady=(0, 12), ipady=4)
        self.entry_a.focus_set()  # Inicia com o cursor focado no primeiro campo

        # --- Seleção da Operação ---
        lbl_op = tk.Label(
            form_frame,
            text="Operação Desejada:",
            font=("Helvetica", 10, "bold"),
            bg="#FFFFFF",
            fg="#374151",
            anchor="w",
        )
        lbl_op.pack(fill=tk.X, pady=(0, 4))

        frame_operacoes = tk.Frame(form_frame, bg="#FFFFFF")
        frame_operacoes.pack(fill=tk.X, pady=(0, 12))

        operacoes = [
            ("+", "Adição (+)"),
            ("-", "Subtração (-)"),
            ("*", "Multiplicação (×)"),
            ("/", "Divisão (÷)"),
        ]

        # Cria botões de rádio para seleção explícita da operação
        for simbolo, texto_legenda in operacoes:
            rb = tk.Radiobutton(
                frame_operacoes,
                text=texto_legenda,
                value=simbolo,
                variable=self.var_operacao,
                font=("Helvetica", 10),
                bg="#FFFFFF",
                fg="#1F2937",
                activebackground="#FFFFFF",
                selectcolor="#FFFFFF",
                anchor="w",
            )
            rb.pack(fill=tk.X, pady=2)

        # --- Campo 2: Operando B ---
        lbl_op_b = tk.Label(
            form_frame,
            text="Segundo Número (Operando B):",
            font=("Helvetica", 10, "bold"),
            bg="#FFFFFF",
            fg="#374151",
            anchor="w",
        )
        lbl_op_b.pack(fill=tk.X, pady=(0, 4))

        self.entry_b = tk.Entry(
            form_frame,
            textvariable=self.var_operando_b,
            font=("Helvetica", 12),
            bd=1,
            relief=tk.SOLID,
            highlightthickness=1,
            highlightcolor="#2563EB",
        )
        self.entry_b.pack(fill=tk.X, pady=(0, 4), ipady=4)

        # Atalho de teclado: pressionar Enter em qualquer campo dispara o cálculo
        self.entry_a.bind("<Return>", lambda event: self.executar_calculo())
        self.entry_b.bind("<Return>", lambda event: self.executar_calculo())

        # --- Barra de Ações (Botões) ---
        frame_botoes = tk.Frame(container, bg="#F3F4F6")
        frame_botoes.pack(fill=tk.X, pady=8)

        btn_calcular = tk.Button(
            frame_botoes,
            text="Calcular",
            font=("Helvetica", 11, "bold"),
            bg="#2563EB",  # Azul Royal de alto contraste
            fg="#FFFFFF",
            activebackground="#1D4ED8",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            pady=8,
            command=self.executar_calculo,
        )
        btn_calcular.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))

        btn_limpar = tk.Button(
            frame_botoes,
            text="Limpar",
            font=("Helvetica", 11),
            bg="#E5E7EB",  # Cinza neutro
            fg="#374151",
            activebackground="#D1D5DB",
            activeforeground="#111827",
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            pady=8,
            command=self.limpar_campos,
        )
        btn_limpar.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(6, 0))

        # --- Painel de Resultado e Mensagens ---
        self.frame_resultado = tk.Frame(container, bg="#FFFFFF", padx=16, pady=12, relief=tk.RIDGE, bd=1)
        self.frame_resultado.pack(fill=tk.BOTH, expand=True, pady=(8, 0))

        self.lbl_status_titulo = tk.Label(
            self.frame_resultado,
            text="Resultado:",
            font=("Helvetica", 9, "bold"),
            bg="#FFFFFF",
            fg="#6B7280",
            anchor="w",
        )
        self.lbl_status_titulo.pack(fill=tk.X)

        self.lbl_resultado_conteudo = tk.Label(
            self.frame_resultado,
            textvariable=self.var_resultado,
            font=("Helvetica", 18, "bold"),
            bg="#FFFFFF",
            fg="#059669",  # Verde esmeralda para sucesso
            anchor="w",
            wraplength=340,
            justify=tk.LEFT,
        )
        self.lbl_resultado_conteudo.pack(fill=tk.X, pady=(4, 0))

        # Rótulo de erro com quebra automática de linha
        self.lbl_erro = tk.Label(
            self.frame_resultado,
            textvariable=self.var_mensagem_erro,
            font=("Helvetica", 10),
            bg="#FFFFFF",
            fg="#DC2626",  # Vermelho para mensagens de erro/validação
            anchor="w",
            wraplength=340,
            justify=tk.LEFT,
        )
        self.lbl_erro.pack(fill=tk.X, pady=(4, 0))

    def executar_calculo(self) -> None:
        """
        Handler de evento disparado ao acionar o botão 'Calcular'.

        Coordena o fluxo de execução:
        1. Limpa avisos anteriores.
        2. Coleta strings dos campos.
        3. Chama a camada de validação (validacao.py).
        4. Invoca o motor de cálculo (operacoes.py).
        5. Atualiza a tela com o resultado formatado ou com mensagem de erro controlada.
        """
        # Limpa estados de mensagens anteriores para evitar confusão de dados passados
        self.var_mensagem_erro.set("")
        self.var_resultado.set("")

        operando_a_bruto = self.var_operando_a.get()
        operando_b_bruto = self.var_operando_b.get()
        operacao = self.var_operacao.get()

        try:
            # Passo 1: Validação e conversão das entradas brutas
            valor_a = converter_operando(operando_a_bruto, nome_campo="Operando A")
            valor_b = converter_operando(operando_b_bruto, nome_campo="Operando B")

            # Passo 2: Execução da lógica matemática pura
            resultado_bruto = calcular(valor_a, valor_b, operacao)

            # Passo 3: Formatação amigável para apresentação
            resultado_formatado = formatar_resultado(resultado_bruto)

            # Exibe o resultado e atualiza estilo visual
            self.lbl_status_titulo.config(text="Resultado do Cálculo:")
            self.var_resultado.set(resultado_formatado)

        except ErroValidacao as erro:
            # Captura erro de validação (campo vazio, letras, etc.)
            self.lbl_status_titulo.config(text="Aviso de Validação:")
            self.var_mensagem_erro.set(str(erro))

        except DivisaoPorZeroError as erro:
            # Captura erro de domínio (divisão por zero)
            self.lbl_status_titulo.config(text="Erro Aritmético:")
            self.var_mensagem_erro.set(str(erro))

        except OperacaoInvalidaError as erro:
            # Captura inconsistência de operação
            self.lbl_status_titulo.config(text="Erro de Operação:")
            self.var_mensagem_erro.set(str(erro))

    def limpar_campos(self) -> None:
        """
        Handler de evento para o botão 'Limpar'.

        Restaura os campos de entrada, a seleção padrão de operação e os
        painéis de resultado para o estado inicial neutro, devolvendo o foco
        ao primeiro campo.
        """
        self.var_operando_a.set("")
        self.var_operando_b.set("")
        self.var_operacao.set("+")
        self.var_resultado.set("")
        self.var_mensagem_erro.set("")
        self.lbl_status_titulo.config(text="Resultado:")
        self.entry_a.focus_set()

    def iniciar(self) -> None:
        """Inicia o laço de eventos principal (Main Loop) do Tkinter."""
        self.root.mainloop()
