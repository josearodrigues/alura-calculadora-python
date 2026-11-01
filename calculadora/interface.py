"""
Módulo de interface gráfica com o usuário (GUI) utilizando Tkinter nativo.
Implementa a identidade visual Dark Premium, visor duplo, teclado de funções completo,
histórico lateral interativo, suporte a atalhos de teclado físico e cópia para clipboard.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from calculadora.expressoes import (
    ExpressaoInvalidaError,
    avaliar_expressao,
)
from calculadora.historico import (
    EntradaHistorico,
    HistoricoSessao,
    RegistroNaoEncontradoError,
)
from calculadora.operacoes import (
    DivisaoPorZeroError,
    ErroAritmetico,
    OperacaoInvalidaError,
    RadicandoNegativoError,
    formatar_resultado,
    # Validação numérica para as operações de memória
    somar,
    subtrair,
)
from calculadora.validacao import ErroValidacao

# Paleta Dark Premium Homologada
COR_BG_APP = "#0D1B2A"          # Grafite marinho profundo
COR_BG_CARD = "#1A2744"         # Azul ardósia escuro
COR_BG_DISPLAY = "#0A1424"      # Fundo do visor
COR_BORDA_CARD = "#1E3A5F"      # Borda sutil
COR_TEXTO_PRINCIPAL = "#F1F5F9" # Branco suave
COR_TEXTO_SECUNDARIO = "#94A3B8"# Cinza claro
COR_RESULTADO_CIANO = "#22D3EE" # Ciano elétrico (identidade visual)
COR_BTN_NUM = "#2D3F6A"         # Botões numéricos
COR_BTN_OP = "#2563EB"          # Botões de operação (+, -, *, /)
COR_BTN_FUNCAO = "#7C3AED"      # Botões de funções avançadas (%, √, x², root, etc)
COR_BTN_EXEC = "#22C55E"        # Botão '=' (verde)
COR_BTN_CLEAR = "#EF4444"       # Botão 'C' e '⌫' (vermelho)
COR_BTN_MEMORIA = "#1E293B"     # Botões de memória
COR_TEXTO_DESABILITADO = "#64748B"


class CalculadoraGUI:
    """
    Controladora da interface gráfica Tkinter para a Calculadora 2.1.0.
    """

    def __init__(self, root: Optional[tk.Tk] = None) -> None:
        self.root = root if root is not None else tk.Tk()
        self.historico = HistoricoSessao()
        self.memoria: float | None = None

        # Estado da digitação e do cálculo
        self.var_expressao = tk.StringVar(value="")
        self.var_resultado = tk.StringVar(value="0")
        self.var_status = tk.StringVar(value="Pronta para calcular!")
        self._resultado_calculado: bool = False

        self._configurar_janela()
        self._construir_widgets()
        self._configurar_atalhos_teclado()

    def _configurar_janela(self) -> None:
        """Configurações de dimensões, título e cor da janela."""
        self.root.title("Calculadora 2.1.0")
        self.root.geometry("740x580")
        self.root.minsize(700, 540)
        self.root.configure(bg=COR_BG_APP)

    def _construir_widgets(self) -> None:
        """Monta o layout completo com cabeçalho, visor, teclado e histórico lateral."""
        # Container principal
        self.container_principal = tk.Frame(self.root, bg=COR_BG_APP, padx=16, pady=16)
        self.container_principal.pack(fill=tk.BOTH, expand=True)

        # Cabeçalho
        self._construir_cabecalho()

        # Corpo com duas colunas: Coluna Esquerda (Calculadora) e Coluna Direita (Histórico)
        corpo_frame = tk.Frame(self.container_principal, bg=COR_BG_APP)
        corpo_frame.pack(fill=tk.BOTH, expand=True, pady=(8, 0))

        # Coluna da Calculadora (Visor + Teclado)
        calc_frame = tk.Frame(corpo_frame, bg=COR_BG_CARD, padx=14, pady=14, highlightthickness=1, highlightbackground=COR_BORDA_CARD)
        calc_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self._construir_visor(calc_frame)
        self._construir_teclado(calc_frame)

        # Coluna do Histórico Lateral
        hist_frame = tk.Frame(corpo_frame, bg=COR_BG_CARD, width=240, padx=12, pady=12, highlightthickness=1, highlightbackground=COR_BORDA_CARD)
        hist_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        hist_frame.pack_propagate(False)

        self._construir_historico(hist_frame)

        # Barra de status inferior
        self._construir_status_bar()

    def _construir_cabecalho(self) -> None:
        """Barra superior com título, subtítulo e botões utilitários."""
        cabecalho = tk.Frame(self.container_principal, bg=COR_BG_APP)
        cabecalho.pack(fill=tk.X, pady=(0, 6))

        titulo_box = tk.Frame(cabecalho, bg=COR_BG_APP)
        titulo_box.pack(side=tk.LEFT)

        lbl_titulo = tk.Label(
            titulo_box,
            text="Calculadora 2.1.0",
            font=("Helvetica", 14, "bold"),
            bg=COR_BG_APP,
            fg=COR_TEXTO_PRINCIPAL,
        )
        lbl_titulo.pack(anchor="w")

        lbl_subtitulo = tk.Label(
            titulo_box,
            text="Mais funções, mais possibilidades!",
            font=("Helvetica", 9, "italic"),
            bg=COR_BG_APP,
            fg=COR_TEXTO_SECUNDARIO,
        )
        lbl_subtitulo.pack(anchor="w")

    def _construir_visor(self, pai: tk.Frame) -> None:
        """Visor duplo com expressão secundária e resultado em ciano."""
        visor_frame = tk.Frame(pai, bg=COR_BG_DISPLAY, padx=12, pady=10, highlightthickness=1, highlightbackground=COR_BORDA_CARD)
        visor_frame.pack(fill=tk.X, pady=(0, 10))

        # Linha superior: Expressão em edição
        lbl_expr = tk.Label(
            visor_frame,
            textvariable=self.var_expressao,
            font=("Helvetica", 11),
            bg=COR_BG_DISPLAY,
            fg=COR_TEXTO_SECUNDARIO,
            anchor="e",
        )
        lbl_expr.pack(fill=tk.X)

        # Linha inferior: Resultado em ciano com botão copiar
        resultado_box = tk.Frame(visor_frame, bg=COR_BG_DISPLAY)
        resultado_box.pack(fill=tk.X, pady=(4, 0))

        lbl_res = tk.Label(
            resultado_box,
            textvariable=self.var_resultado,
            font=("Helvetica", 20, "bold"),
            bg=COR_BG_DISPLAY,
            fg=COR_RESULTADO_CIANO,
            anchor="e",
        )
        lbl_res.pack(side=tk.LEFT, fill=tk.X, expand=True)

        btn_copiar = tk.Button(
            resultado_box,
            text="📋",
            font=("Helvetica", 10),
            bg=COR_BG_DISPLAY,
            fg=COR_TEXTO_SECUNDARIO,
            activebackground=COR_BG_CARD,
            activeforeground=COR_RESULTADO_CIANO,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self.copiar_resultado,
        )
        btn_copiar.pack(side=tk.RIGHT, padx=(6, 0))

    def _construir_teclado(self, pai: tk.Frame) -> None:
        """Monta o grid do teclado (memória, funções, numérico e operadores)."""
        teclado_frame = tk.Frame(pai, bg=COR_BG_CARD)
        teclado_frame.pack(fill=tk.BOTH, expand=True)

        for col in range(5):
            teclado_frame.columnconfigure(col, weight=1, uniform="btn_col")
        for row in range(7):
            teclado_frame.rowconfigure(row, weight=1, uniform="btn_row")

        # Linha 0: Botões de memória
        botoes_memoria = [
            ("MC", 0, self.memoria_limpar),
            ("MR", 1, self.memoria_recuperar),
            ("M+", 2, self.memoria_somar),
            ("M-", 3, self.memoria_subtrair),
            ("MS", 4, self.memoria_armazenar),
        ]

        for texto, col, comando in botoes_memoria:
            self._criar_botao_memoria(teclado_frame, texto, comando, row=0, col=col)

        # Linha 1: Funções científicas
        self._criar_botao(teclado_frame, "%", COR_BTN_FUNCAO, lambda: self._adicionar_caractere("%"), 1, 0)
        self._criar_botao(teclado_frame, "√", COR_BTN_FUNCAO, self._aplicar_raiz_quadrada, 1, 1)
        self._criar_botao(teclado_frame, "x²", COR_BTN_FUNCAO, self._aplicar_quadrado, 1, 2)
        self._criar_botao(teclado_frame, "¹/x", COR_BTN_FUNCAO, self._aplicar_inverso, 1, 3)
        self._criar_botao(teclado_frame, "|x|", COR_BTN_FUNCAO, self._aplicar_absoluto, 1, 4)

        # Linha 2: Agrupamento, funções unárias e limpeza
        self._criar_botao(teclado_frame, "(", COR_BTN_NUM, lambda: self._adicionar_caractere("("), 2, 0)
        self._criar_botao(teclado_frame, ")", COR_BTN_NUM, lambda: self._adicionar_caractere(")"), 2, 1)
        self._criar_botao(teclado_frame, "±", COR_BTN_NUM, self._trocar_sinal_display, 2, 2)
        self._criar_botao(teclado_frame, "C", COR_BTN_CLEAR, self.limpar_display, 2, 3)
        self._criar_botao(teclado_frame, "⌫", COR_BTN_CLEAR, self.apagar_ultimo_caractere, 2, 4)

        # Linha 3: 7, 8, 9, ÷, ⁿ√x
        self._criar_botao(teclado_frame, "7", COR_BTN_NUM, lambda: self._adicionar_caractere("7"), 3, 0)
        self._criar_botao(teclado_frame, "8", COR_BTN_NUM, lambda: self._adicionar_caractere("8"), 3, 1)
        self._criar_botao(teclado_frame, "9", COR_BTN_NUM, lambda: self._adicionar_caractere("9"), 3, 2)
        self._criar_botao(teclado_frame, "÷", COR_BTN_OP, lambda: self._adicionar_operador("÷"), 3, 3)
        self._criar_botao(teclado_frame, "ⁿ√x", COR_BTN_FUNCAO, self._aplicar_raiz_n, 3, 4)

        # Linha 4: 4, 5, 6, ×, ^
        self._criar_botao(teclado_frame, "4", COR_BTN_NUM, lambda: self._adicionar_caractere("4"), 4, 0)
        self._criar_botao(teclado_frame, "5", COR_BTN_NUM, lambda: self._adicionar_caractere("5"), 4, 1)
        self._criar_botao(teclado_frame, "6", COR_BTN_NUM, lambda: self._adicionar_caractere("6"), 4, 2)
        self._criar_botao(teclado_frame, "×", COR_BTN_OP, lambda: self._adicionar_operador("×"), 4, 3)
        self._criar_botao(teclado_frame, "^", COR_BTN_FUNCAO, lambda: self._adicionar_operador("^"), 4, 4)

        # Linha 5: 1, 2, 3, −, ;
        self._criar_botao(teclado_frame, "1", COR_BTN_NUM, lambda: self._adicionar_caractere("1"), 5, 0)
        self._criar_botao(teclado_frame, "2", COR_BTN_NUM, lambda: self._adicionar_caractere("2"), 5, 1)
        self._criar_botao(teclado_frame, "3", COR_BTN_NUM, lambda: self._adicionar_caractere("3"), 5, 2)
        self._criar_botao(teclado_frame, "−", COR_BTN_OP, lambda: self._adicionar_operador("-"), 5, 3)
        self._criar_botao(teclado_frame, ";", COR_BTN_NUM, lambda: self._adicionar_caractere(";"), 5, 4)

        # Linha 6: 0, ., = (largo) e +
        self._criar_botao(teclado_frame, "0", COR_BTN_NUM, lambda: self._adicionar_caractere("0"), 6, 0)
        self._criar_botao(teclado_frame, ".", COR_BTN_NUM, lambda: self._adicionar_caractere("."), 6, 1)
        self._criar_botao(teclado_frame, "=", COR_BTN_EXEC, self.executar_calculo, 6, 2, colspan=2)
        self._criar_botao(teclado_frame, "+", COR_BTN_OP, lambda: self._adicionar_operador("+"), 6, 4)

    def _criar_botao(
        self,
        pai: tk.Frame,
        texto: str,
        cor_bg: str,
        comando: Callable[[], None],
        row: int,
        col: int,
        colspan: int = 1,
    ) -> tk.Button:
        """Cria e posiciona um botão de ação rápida padronizado."""
        btn = tk.Button(
            pai,
            text=texto,
            font=("Helvetica", 11, "bold"),
            bg=cor_bg,
            fg=COR_TEXTO_PRINCIPAL,
            activebackground=COR_BORDA_CARD,
            activeforeground=COR_TEXTO_PRINCIPAL,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=comando,
        )
        btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)
        return btn

    def _criar_botao_memoria(self, pai: tk.Frame, texto: str, comando: Callable[[], None], row: int, col: int) -> tk.Button:
        """Cria e posiciona um botão de memória funcional"""
        btn = tk.Button(
            pai,
            text=texto,
            font=("Helvetica", 9, "bold"),
            bg=COR_BTN_MEMORIA,
            fg=COR_TEXTO_PRINCIPAL,
            activebackground=COR_BORDA_CARD,
            activeforeground=COR_RESULTADO_CIANO,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=comando,
        )
        btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        return btn

    def _construir_historico(self, pai: tk.Frame) -> None:
        """Monta o painel lateral com lista de histórico e botão de limpeza."""
        cab_hist = tk.Frame(pai, bg=COR_BG_CARD)
        cab_hist.pack(fill=tk.X, pady=(0, 6))

        lbl_hist = tk.Label(
            cab_hist,
            text="🕐 Histórico",
            font=("Helvetica", 11, "bold"),
            bg=COR_BG_CARD,
            fg=COR_TEXTO_PRINCIPAL,
        )
        lbl_hist.pack(side=tk.LEFT)

        btn_limpar_hist = tk.Button(
            cab_hist,
            text="🗑",
            font=("Helvetica", 10),
            bg=COR_BG_CARD,
            fg=COR_TEXTO_SECUNDARIO,
            activebackground=COR_BORDA_CARD,
            activeforeground=COR_BTN_CLEAR,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self.limpar_historico,
        )
        btn_limpar_hist.pack(side=tk.RIGHT)

        # Área de listagem com scroll
        scroll_frame = tk.Frame(pai, bg=COR_BG_CARD)
        scroll_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas_hist = tk.Canvas(scroll_frame, bg=COR_BG_CARD, highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_frame, orient=tk.VERTICAL, command=self.canvas_hist.yview)
        self.itens_hist_frame = tk.Frame(self.canvas_hist, bg=COR_BG_CARD)

        self.itens_hist_frame.bind(
            "<Configure>",
            lambda e: self.canvas_hist.configure(scrollregion=self.canvas_hist.bbox("all")),
        )
        self.canvas_hist.create_window((0, 0), window=self.itens_hist_frame, anchor="nw")
        self.canvas_hist.configure(yscrollcommand=scrollbar.set)

        self.canvas_hist.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _construir_status_bar(self) -> None:
        """Barra de status inferior com mensagem informativa e indicação de atalhos."""
        status_frame = tk.Frame(self.container_principal, bg=COR_BG_APP)
        status_frame.pack(fill=tk.X, pady=(8, 0))

        lbl_status = tk.Label(
            status_frame,
            textvariable=self.var_status,
            font=("Helvetica", 9),
            bg=COR_BG_APP,
            fg=COR_BTN_EXEC,
            anchor="w",
        )
        lbl_status.pack(side=tk.LEFT)

        lbl_atalhos = tk.Label(
            status_frame,
            text="Atalhos: 0-9, +, -, *, /, ;, Enter, Esc, Ctrl+C",
            font=("Helvetica", 9),
            bg=COR_BG_APP,
            fg=COR_TEXTO_SECUNDARIO,
            anchor="e",
        )
        lbl_atalhos.pack(side=tk.RIGHT)

    # -----------------------------------------------------------------------
    # Ações e Controle de Estado da Calculadora
    # -----------------------------------------------------------------------

    def _adicionar_caractere(self, char: str) -> None:
        """Insere um caractere ou inicia nova expressão se um resultado já estiver exibido."""
        if self._resultado_calculado:
            # Se for dígito logo após o resultado, inicia nova conta descartando o anterior do visor
            if char.isdigit() or char == "(":
                self.var_expressao.set(char)
                self.var_resultado.set("0")
                self._resultado_calculado = False
                return
            self._resultado_calculado = False

        atual = self.var_expressao.get()
        self.var_expressao.set(atual + char)

    def _adicionar_operador(self, op: str) -> None:
        """
        Adiciona operador aritmético. Se um cálculo acabou de ser concluído,
        continua o cálculo a partir do último resultado (ANS).
        """
        if self._resultado_calculado:
            ultimo_res = self.var_resultado.get()
            self.var_expressao.set(ultimo_res + op)
            self._resultado_calculado = False
            return

        atual = self.var_expressao.get()
        self.var_expressao.set(atual + op)

    def _aplicar_quadrado(self) -> None:
        """Aplica potência ao quadrado (^2) ao termo atual ou ao resultado."""
        if self._resultado_calculado:
            ultimo_res = self.var_resultado.get()
            self.var_expressao.set(f"{ultimo_res}^2")
            self._resultado_calculado = False
            self.executar_calculo()
            return

        self._adicionar_operador("^2")

    def _aplicar_raiz_quadrada(self) -> None:
        """Aplica raiz quadrada diretamente ao resultado ou insere no visor."""
        if self._resultado_calculado:
            ultimo_res = self.var_resultado.get()
            self.var_expressao.set(f"sqrt({ultimo_res})")
            self._resultado_calculado = False
            self.executar_calculo()
            return

        self._adicionar_caractere("sqrt(")

    def _aplicar_raiz_n(self) -> None:
        """Insere o template da função root(radicando; indice)."""
        if self._resultado_calculado:
            ultimo_res = self.var_resultado.get()
            self.var_expressao.set(f"root({ultimo_res}; ")
            self._resultado_calculado = False
            return

        self._adicionar_caractere("root(")

    def _aplicar_absoluto(self) -> None:
        """Aplica a função abs() ao resultado ou insere no visor."""
        if self._resultado_calculado:
            ultimo_res = self.var_resultado.get()
            self.var_expressao.set(f"abs({ultimo_res})")
            self._resultado_calculado = False
            self.executar_calculo()
            return

        self._adicionar_caractere("abs(")

    def _aplicar_inverso(self) -> None:
        """Aplica inverso (1/x) ao resultado ou insere no visor."""
        if self._resultado_calculado:
            ultimo_res = self.var_resultado.get()
            self.var_expressao.set(f"inv({ultimo_res})")
            self._resultado_calculado = False
            self.executar_calculo()
            return

        self._adicionar_caractere("inv(")

    def _trocar_sinal_display(self) -> None:
        """Inverte o sinal do resultado atual ou do buffer em edição."""
        if self._resultado_calculado:
            try:
                val = float(self.var_resultado.get())
                self.var_resultado.set(formatar_resultado(-val))
                self.var_expressao.set(formatar_resultado(-val))
            except ValueError:
                pass
            return

        atual = self.var_expressao.get()
        if atual.startswith("-"):
            self.var_expressao.set(atual[1:])
        else:
            self.var_expressao.set("-" + atual)

    def apagar_ultimo_caractere(self) -> None:
        """Apaga o último caractere do buffer de expressão (Backspace)."""
        if self._resultado_calculado:
            self.limpar_display()
            return
        atual = self.var_expressao.get()
        if atual:
            self.var_expressao.set(atual[:-1])

    def limpar_display(self) -> None:
        """Limpa o visor (botão C / Escape). O ANS ativo permanece intacto."""
        self.var_expressao.set("")
        self.var_resultado.set("0")
        self._resultado_calculado = False
        self.var_status.set("Pronta para calcular!")

    def executar_calculo(self) -> None:
        """Avalia a expressão atual via motor seguro e registra no histórico."""
        expr = self.var_expressao.get()
        if not expr.strip():
            return

        ans_atual = self.historico.obter_ans()
        try:
            resultado_bruto = avaliar_expressao(expr, ans=ans_atual)
            resultado_fmt = formatar_resultado(resultado_bruto)

            self.var_resultado.set(resultado_fmt)
            self._resultado_calculado = True
            self.var_status.set("Cálculo realizado com sucesso.")

            # Registra no histórico em memória
            entrada = self.historico.registrar(expr, expr, resultado_bruto)
            self._adicionar_item_historico_visual(entrada)

        except (DivisaoPorZeroError, RadicandoNegativoError, ErroAritmetico, OperacaoInvalidaError) as e:
            self.var_resultado.set("Erro")
            self.var_status.set(f"Erro: {str(e)}")
        except (ErroValidacao, ExpressaoInvalidaError) as e:
            self.var_resultado.set("Inválido")
            self.var_status.set(f"Aviso: {str(e)}")
        except Exception as e:
            self.var_resultado.set("Erro")
            self.var_status.set(f"Erro inesperado: {str(e)}")

    def _adicionar_item_historico_visual(self, entrada: EntradaHistorico) -> None:
        """Renderiza um item clicável no painel lateral de histórico."""
        card = tk.Frame(self.itens_hist_frame, bg=COR_BG_DISPLAY, padx=6, pady=4, highlightthickness=1, highlightbackground=COR_BORDA_CARD)
        card.pack(fill=tk.X, expand=True, pady=3)

        lbl_expr = tk.Label(
            card,
            text=entrada.expressao,
            font=("Helvetica", 9),
            bg=COR_BG_DISPLAY,
            fg=COR_TEXTO_SECUNDARIO,
            anchor="w",
        )
        lbl_expr.pack(fill=tk.X)

        lbl_res = tk.Label(
            card,
            text=f"= {entrada.resultado_formatado}",
            font=("Helvetica", 11, "bold"),
            bg=COR_BG_DISPLAY,
            fg=COR_RESULTADO_CIANO,
            anchor="e",
        )
        lbl_res.pack(fill=tk.X)

        # Vincula clique do mouse para recuperar o histórico
        for widget in (card, lbl_expr, lbl_res):
            widget.bind("<Button-1>", lambda e, id_ent=entrada.id: self._recuperar_historico_por_id(id_ent))
            widget.config(cursor="hand2")

    def _recuperar_historico_por_id(self, id_entrada: int) -> None:
        """Recupera uma entrada do histórico e define o valor como ANS ativo."""
        try:
            entrada = self.historico.recuperar_entrada(id_entrada)
            self.var_expressao.set(entrada.expressao)
            self.var_resultado.set(entrada.resultado_formatado)
            self._resultado_calculado = True
            self.var_status.set(f"Recuperado #{entrada.id}: {entrada.resultado_formatado} pronto para continuar.")
        except RegistroNaoEncontradoError:
            pass

    def limpar_historico(self) -> None:
        """Esvazia o histórico visual e em memória sem apagar o ANS ativo."""
        self.historico.limpar_historico()
        for widget in self.itens_hist_frame.winfo_children():
            widget.destroy()
        self.var_status.set("Histórico limpo. Último resultado (ANS) preservado.")

    def copiar_resultado(self) -> None:
        """Copia o resultado em foco para a área de transferência do sistema."""
        resultado = self.var_resultado.get()
        if resultado and resultado not in ("0", "Erro", "Inválido"):
            self.root.clipboard_clear()
            self.root.clipboard_append(resultado)
            self.var_status.set(f"Resultado '{resultado}' copiado para a área de transferência!")

    def _obter_resultado_atual(self) -> Optional[float]:
        """Retorna o resultado exibido quando há um cálculo válido."""
        if not self._resultado_calculado:
            return None

        try:
            return float(self.var_resultado.get())
        except ValueError:
            return None

    def memoria_limpar(self) -> None:
        """Limpa o valor armazenado na memória."""
        self.memoria = None
        self.var_status.set("Memória limpa.")

    def memoria_recuperar(self) -> None:
        """Recupera o valor da memória para o visor."""
        if self.memoria is None:
            self.var_status.set("Memória vazia.")
            return

        valor = formatar_resultado(self.memoria)
        self.var_expressao.set(valor)
        self.var_resultado.set(valor)
        self._resultado_calculado = True
        self.var_status.set("Valor recuperado da memória.")

    def memoria_armazenar(self) -> None:
        """Armazena o resultado atual na memória."""
        valor = self._obter_resultado_atual()

        if valor is None:
            self.var_status.set("Nenhum resultado disponível para armazenar.")
            return

        self.memoria = valor
        self.var_status.set("Resultado armazenado na memória.")

    def memoria_somar(self) -> None:
        """Adiciona o resultado atual ao valor armazenado."""
        valor = self._obter_resultado_atual()

        if valor is None:
            self.var_status.set("Nenhum resultado disponível para somar.")
            return

        atual = self.memoria if self.memoria is not None else 0.0

        try:
            self.memoria = somar(atual, valor)
            self.var_status.set("Resultado adicionado à memória.")
        except ErroAritmetico as erro:
            self.var_status.set(f"Erro na memória: {erro}")

    def memoria_subtrair(self) -> None:
        """Subtrai o resultado atual do valor armazenado."""
        valor = self._obter_resultado_atual()

        if valor is None:
            self.var_status.set("Nenhum resultado disponível para subtrair.")
            return

        atual = self.memoria if self.memoria is not None else 0.0

        try:
            self.memoria = subtrair(atual, valor)
            self.var_status.set("Resultado subtraído da memória.")
        except ErroAritmetico as erro:
            self.var_status.set(f"Erro na memória: {erro}")

    # -----------------------------------------------------------------------
    # Mapeamento do Teclado Físico
    # -----------------------------------------------------------------------

    def _configurar_atalhos_teclado(self) -> None:
        """Liga as teclas físicas às ações da calculadora."""
        self.root.bind("<Key>", self._ao_pressionar_tecla)

    def _ao_pressionar_tecla(self, evento: tk.Event) -> None:
        """Interpreta os eventos de tecla física."""
        char = evento.char
        tecla = evento.keysym

        # Atalho Ctrl+C para copiar resultado
        if (evento.state & 0x4) and (tecla in ("c", "C")):
            self.copiar_resultado()
            return

        if tecla in ("Return", "KP_Enter"):
            self.executar_calculo()
        elif tecla == "BackSpace":
            self.apagar_ultimo_caractere()
        elif tecla in ("Escape", "Delete"):
            self.limpar_display()
        elif char and char in "0123456789.()^%;":
            self._adicionar_caractere(char)
        elif char == ",":
            # Vírgula decimal converte para ponto
            self._adicionar_caractere(".")
        elif char in "+-*/":
            op_map = {"*": "×", "/": "÷"}
            self._adicionar_operador(op_map.get(char, char))

    def iniciar(self) -> None:
        """Inicia o laço de eventos principal do Tkinter."""
        self.root.mainloop()
