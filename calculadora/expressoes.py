"""
Módulo responsável pela análise léxica, sintática e avaliação recursiva de expressões matemáticas.

Implementa um parser e avaliador seguro, determinístico e livre de eval(), com base em
uma árvore sintática abstrata (AST) própria. Suporta funções unárias, raiz de índice n,
precedência formal estrita (ex.: -2^2 = -4), associatividade à direita para potências,
e resolução semântica contextual de porcentagem.
"""

import math
import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union

from calculadora.operacoes import (
    DivisaoPorZeroError,
    ErroAritmetico,
    OperacaoInvalidaError,
    RadicandoNegativoError,
    _assegurar_numero_valido,
    dividir,
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
from calculadora.validacao import ErroValidacao, sanitizar_texto, validar_literal_numerico

LIMITE_TAMANHO_EXPRESSAO = 200
LIMITE_PROFUNDIDADE_AST = 50


class ExpressaoInvalidaError(Exception):
    """Exceção levantada quando a expressão contém erro de sintaxe ou nós inválidos."""
    pass


# ---------------------------------------------------------------------------
# Nós da Árvore Sintática Abstrata (AST) Própria
# ---------------------------------------------------------------------------

@dataclass
class NoAST:
    """Classe base para nós da árvore sintática."""
    pass


@dataclass
class NoNumero(NoAST):
    valor: float


@dataclass
class NoIdentificador(NoAST):
    nome: str


@dataclass
class NoOperacaoBinaria(NoAST):
    operador: str
    esquerda: NoAST
    direita: NoAST


@dataclass
class NoOperacaoUnaria(NoAST):
    operador: str
    operando: NoAST


@dataclass
class NoPercentual(NoAST):
    termo: NoAST


@dataclass
class NoAgrupamento(NoAST):
    expressao: NoAST


@dataclass
class NoChamadaFuncao(NoAST):
    nome_funcao: str
    argumentos: List[NoAST]


# ---------------------------------------------------------------------------
# Tokenização e Análise Léxica
# ---------------------------------------------------------------------------

@dataclass
class Token:
    tipo: str
    valor: str
    posicao: int


def _normalizar_simbolos(expressao_bruta: str) -> str:
    """
    Normaliza caracteres tipográficos e mapeia operadores visuais antes do parse:
    - Símbolos de multiplicação e divisão (×, ÷)
    - Operador visual de raiz quadrada (√) para sqrt()
    """
    texto = expressao_bruta.replace("×", "*").replace("÷", "/")

    # Normaliza raiz quadrada: se for √(expr) vira sqrt(expr)
    texto = texto.replace("√(", "sqrt(")

    # Normaliza √numero para sqrt(numero)
    # Exemplo: √144 -> sqrt(144); √9 + 16 -> sqrt(9) + 16
    def _substituir_raiz_literal(match: re.Match) -> str:
        numero = match.group(1)
        return f"sqrt({numero})"

    # Captura √ seguido imediatamente por número inteiro ou decimal
    texto = re.sub(r"√(\d+(?:[.,]\d+)?(?:[eE][+-]?\d+)?)", _substituir_raiz_literal, texto)

    return texto


def _tokenizar(expressao: str) -> List[Token]:
    """
    Analisa a expressão e gera uma sequência de tokens tipados.
    Valida limites de literais numéricos de até 30 dígitos diretamente no tokenizer.
    """
    tokens: List[Token] = []
    i = 0
    tamanho = len(expressao)

    while i < tamanho:
        char = expressao[i]

        # Ignora espaços em branco
        if char.isspace():
            i += 1
            continue

        # Números: inteiros, decimais (com ponto ou vírgula) e notação científica
        if char.isdigit():
            inicio = i
            # Captura dígitos inteiros
            while i < tamanho and expressao[i].isdigit():
                i += 1

            # Parte decimal com ponto '.' ou vírgula ',' seguida de dígito
            if i < tamanho and expressao[i] in ".,":
                if expressao[i] == ",":
                    # Vírgula só integra o número se for seguida imediatamente por dígito decimal
                    if i + 1 < tamanho and expressao[i + 1].isdigit():
                        i += 1  # consome a vírgula
                        while i < tamanho and expressao[i].isdigit():
                            i += 1
                else:
                    # Ponto decimal '.'
                    i += 1
                    while i < tamanho and expressao[i].isdigit():
                        i += 1

            # Verifica se há notação científica imediatamente após
            if i < tamanho and expressao[i] in "eE":
                # Confirma se é notação científica válida (e seguido de dígitos ou +/- e dígitos)
                pos_exp = i + 1
                if pos_exp < tamanho and expressao[pos_exp] in "+-":
                    pos_exp += 1
                if pos_exp < tamanho and expressao[pos_exp].isdigit():
                    i = pos_exp
                    while i < tamanho and expressao[i].isdigit():
                        i += 1

            literal_str = expressao[inicio:i]
            # Valida literal contra o limite de 30 dígitos e magnitude de expoente
            validar_literal_numerico(literal_str)
            tokens.append(Token("NUMERO", literal_str, inicio))
            continue

        # Identificadores (funções e palavras reservadas como ANS, sqrt, root, abs, inv)
        if char.isalpha() or char == "_":
            inicio = i
            while i < tamanho and (expressao[i].isalnum() or expressao[i] == "_"):
                i += 1
            identificador = expressao[inicio:i]
            tokens.append(Token("IDENTIFICADOR", identificador, inicio))
            continue

        # Operadores simples e delimitadores
        if char == "+":
            tokens.append(Token("MAIS", "+", i))
        elif char == "-":
            tokens.append(Token("MENOS", "-", i))
        elif char == "*":
            tokens.append(Token("VEZES", "*", i))
        elif char == "/":
            tokens.append(Token("DIVIDIR", "/", i))
        elif char == "^":
            tokens.append(Token("POTENCIA", "^", i))
        elif char == "%":
            tokens.append(Token("PERCENT", "%", i))
        elif char == "(":
            tokens.append(Token("ABRE_PAR", "(", i))
        elif char == ")":
            tokens.append(Token("FECHA_PAR", ")", i))
        elif char == ";":
            tokens.append(Token("PONTO_VIRGULA", ";", i))
        elif char == ",":
            raise ExpressaoInvalidaError(
                f"Caractere ',' não permitido na posição {i}. Utilize ponto e vírgula ';' exclusivamente para separar argumentos de funções."
            )
        else:
            raise ExpressaoInvalidaError(f"Caractere não reconhecido na expressão: '{char}' na posição {i}.")

        i += 1

    tokens.append(Token("EOF", "", tamanho))
    return tokens


# ---------------------------------------------------------------------------
# Parser Recursivo Descendente (Gramática EBNF Corrigida)
# ---------------------------------------------------------------------------

class _Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.pos = 0

    def _token_atual(self) -> Token:
        return self.tokens[self.pos]

    def _consumir(self, tipo_esperado: str) -> Token:
        token = self._token_atual()
        if token.tipo != tipo_esperado:
            raise ExpressaoInvalidaError(
                f"Sintaxe inválida: esperado '{tipo_esperado}', mas encontrado '{token.tipo}' na posição {token.posicao}."
            )
        self.pos += 1
        return token

    def parse(self) -> NoAST:
        arvore = self._expressao()
        if self._token_atual().tipo != "EOF":
            token_sobra = self._token_atual()
            raise ExpressaoInvalidaError(
                f"Sintaxe inválida: símbolo inesperado '{token_sobra.valor}' na posição {token_sobra.posicao}."
            )
        return arvore

    def _expressao(self) -> NoAST:
        return self._termo_aditivo()

    def _termo_aditivo(self) -> NoAST:
        no = self._termo_multiplicativo()

        while self._token_atual().tipo in ("MAIS", "MENOS"):
            op_token = self._token_atual()
            self.pos += 1
            direita = self._termo_multiplicativo()
            no = NoOperacaoBinaria(operador=op_token.valor, esquerda=no, direita=direita)

        return no

    def _termo_multiplicativo(self) -> NoAST:
        no = self._fator_unario()

        while self._token_atual().tipo in ("VEZES", "DIVIDIR"):
            op_token = self._token_atual()
            self.pos += 1
            direita = self._fator_unario()
            no = NoOperacaoBinaria(operador=op_token.valor, esquerda=no, direita=direita)

        return no

    def _fator_unario(self) -> NoAST:
        """
        FatorUnario := ('+' | '-') FatorUnario | FatorPotencia
        Garante que a potenciação tenha precedência sobre o sinal unário (-2^2 = -(2^2) = -4).
        """
        token = self._token_atual()
        if token.tipo in ("MAIS", "MENOS"):
            self.pos += 1
            operando = self._fator_unario()
            return NoOperacaoUnaria(operador=token.valor, operando=operando)

        return self._fator_potencia()

    def _fator_potencia(self) -> NoAST:
        """
        FatorPotencia := FatorPosfixado ('^' FatorUnario)?
        Associatividade à direita para potenciação: 2^3^2 = 2^(3^2) = 512.
        """
        no = self._fator_posfixado()

        if self._token_atual().tipo == "POTENCIA":
            self.pos += 1
            # Chama _fator_unario na direita para associatividade à direita (right-associative)
            direita = self._fator_unario()
            return NoOperacaoBinaria(operador="^", esquerda=no, direita=direita)

        return no

    def _fator_posfixado(self) -> NoAST:
        """
        FatorPosfixado := Primario '%'?
        Reconhece o operador percentual como operador pós-fixado imediato.
        """
        no = self._primario()

        if self._token_atual().tipo == "PERCENT":
            self.pos += 1
            no = NoPercentual(termo=no)

        return no

    def _primario(self) -> NoAST:
        token = self._token_atual()

        # Número literal
        if token.tipo == "NUMERO":
            self.pos += 1
            valor_num = validar_literal_numerico(token.valor)
            return NoNumero(valor=valor_num)

        # Identificador (chamada de função ou ANS)
        if token.tipo == "IDENTIFICADOR":
            self.pos += 1
            nome = token.valor

            # Se for seguido por '(', é chamada de função
            if self._token_atual().tipo == "ABRE_PAR":
                self.pos += 1
                args: List[NoAST] = []
                if self._token_atual().tipo != "FECHA_PAR":
                    args.append(self._expressao())
                    # Separador oficial e exclusivo de argumentos: ponto e vírgula ';'
                    while self._token_atual().tipo == "PONTO_VIRGULA":
                        self.pos += 1
                        args.append(self._expressao())
                self._consumir("FECHA_PAR")
                return NoChamadaFuncao(nome_funcao=nome, argumentos=args)

            # Caso contrário, é identificador avulso (como ANS)
            return NoIdentificador(nome=nome)

        # Agrupamento explícito entre parênteses
        if token.tipo == "ABRE_PAR":
            self.pos += 1
            expr_interna = self._expressao()
            self._consumir("FECHA_PAR")
            # Envolve no nó NoAgrupamento para delimitação formal de escopo
            return NoAgrupamento(expressao=expr_interna)

        raise ExpressaoInvalidaError(
            f"Sintaxe inválida: termo inesperado '{token.valor or token.tipo}' na posição {token.posicao}."
        )


# ---------------------------------------------------------------------------
# Avaliador Recursivo da AST (Sem eval())
# ---------------------------------------------------------------------------

CATALOGO_FUNCOES_AUTORIZADAS: Dict[str, Callable[..., float]] = {
    "sqrt": raiz_quadrada,
    "raiz": raiz_quadrada,
    "root": raiz_n,
    "abs": valor_absoluto,
    "inv": inverso,
}


class _AvaliadorAST:
    def __init__(self, ans: Optional[float] = None) -> None:
        self.ans = ans

    def avaliar(self, no: NoAST, profundidade: int = 0) -> float:
        if profundidade > LIMITE_PROFUNDIDADE_AST:
            raise ExpressaoInvalidaError("Expressão excessivamente complexa ou aninhada (limite de profundidade excedido).")

        # Nó Numérico
        if isinstance(no, NoNumero):
            return _assegurar_numero_valido(no.valor)

        # Nó Identificador (ANS)
        if isinstance(no, NoIdentificador):
            if no.nome.upper() == "ANS":
                if self.ans is None:
                    raise ExpressaoInvalidaError("Identificador ANS utilizado, mas nenhum resultado anterior está disponível.")
                return _assegurar_numero_valido(self.ans)
            raise ExpressaoInvalidaError(f"Identificador não reconhecido: '{no.nome}'.")

        # Nó Agrupamento '(' expr ')'
        if isinstance(no, NoAgrupamento):
            return self.avaliar(no.expressao, profundidade + 1)

        # Nó Operação Unária (+ ou -)
        if isinstance(no, NoOperacaoUnaria):
            val = self.avaliar(no.operando, profundidade + 1)
            if no.operador == "+":
                return _assegurar_numero_valido(+val)
            elif no.operador == "-":
                return trocar_sinal(val)
            raise ExpressaoInvalidaError(f"Operador unário não suportado: '{no.operador}'.")

        # Nó Percentual Isolado (fora de operador binário aditivo direto)
        if isinstance(no, NoPercentual):
            val_termo = self.avaliar(no.termo, profundidade + 1)
            # Percentual isolado ou termo livre: avalia como fração decimal pura (x / 100)
            return _assegurar_numero_valido(val_termo / 100.0)

        # Nó Operação Binária (+, -, *, /, ^)
        if isinstance(no, NoOperacaoBinaria):
            return self._avaliar_binario(no, profundidade)

        # Nó Chamada de Função
        if isinstance(no, NoChamadaFuncao):
            return self._avaliar_funcao(no, profundidade)

        raise ExpressaoInvalidaError(f"Tipo de nó sintático desconhecido: {type(no).__name__}.")

    def _avaliar_binario(self, no: NoOperacaoBinaria, profundidade: int) -> float:
        # Verifica se o operando direito é um percentual direto
        # Caso 1: Percentual Contextual Aditivo (A + B% ou A - B%)
        if isinstance(no.direita, NoPercentual):
            val_esquerda = self.avaliar(no.esquerda, profundidade + 1)
            taxa_num = self.avaliar(no.direita.termo, profundidade + 1)

            if no.operador == "+":
                # A + (taxa/100 * A)
                delta = multiplicar(val_esquerda, taxa_num / 100.0)
                return somar(val_esquerda, delta)
            elif no.operador == "-":
                # A - (taxa/100 * A)
                delta = multiplicar(val_esquerda, taxa_num / 100.0)
                return subtrair(val_esquerda, delta)
            elif no.operador == "*":
                # A * (taxa / 100)
                return multiplicar(val_esquerda, taxa_num / 100.0)
            elif no.operador == "/":
                # A / (taxa / 100)
                return dividir(val_esquerda, taxa_num / 100.0)
            elif no.operador == "^":
                return potencia(val_esquerda, taxa_num / 100.0)

        # Caso Geral: Sem percentual contextual no operando direito
        val_esq = self.avaliar(no.esquerda, profundidade + 1)
        val_dir = self.avaliar(no.direita, profundidade + 1)

        if no.operador == "+":
            return somar(val_esq, val_dir)
        elif no.operador == "-":
            return subtrair(val_esq, val_dir)
        elif no.operador == "*":
            return multiplicar(val_esq, val_dir)
        elif no.operador == "/":
            return dividir(val_esq, val_dir)
        elif no.operador == "^":
            return potencia(val_esq, val_dir)

        raise ExpressaoInvalidaError(f"Operador binário desconhecido: '{no.operador}'.")

    def _avaliar_funcao(self, no: NoChamadaFuncao, profundidade: int) -> float:
        nome_lower = no.nome_funcao.lower()
        fn = CATALOGO_FUNCOES_AUTORIZADAS.get(nome_lower)

        if fn is None:
            funcoes_disponiveis = ", ".join(CATALOGO_FUNCOES_AUTORIZADAS.keys())
            raise ExpressaoInvalidaError(
                f"Função '{no.nome_funcao}' não autorizada. Funções disponíveis: {funcoes_disponiveis}."
            )

        # Validação de aridade
        args_avaliados = [self.avaliar(arg, profundidade + 1) for arg in no.argumentos]

        if nome_lower in ("sqrt", "raiz", "abs", "inv"):
            if len(args_avaliados) != 1:
                raise ExpressaoInvalidaError(
                    f"A função '{no.nome_funcao}' requer exatamente 1 argumento ({len(args_avaliados)} fornecidos)."
                )
            return fn(args_avaliados[0])

        if nome_lower == "root":
            if len(args_avaliados) != 2:
                raise ExpressaoInvalidaError(
                    f"A função 'root' requer exatamente 2 argumentos (radicando; índice) ({len(args_avaliados)} fornecidos). "
                    "Utilize ponto e vírgula ';' exclusivamente para separar argumentos."
                )
            return fn(args_avaliados[0], args_avaliados[1])

        raise ExpressaoInvalidaError(f"Execução não suportada para função '{no.nome_funcao}'.")


# ---------------------------------------------------------------------------
# Ponto de Entrada Público do Avaliador de Expressões
# ---------------------------------------------------------------------------

def avaliar_expressao(expressao_bruta: str, ans: Optional[float] = None) -> float:
    """
    Avalia uma expressão matemática encadeada de forma pura, determinística e segura.

    Parâmetros:
        expressao_bruta (str): Texto da expressão a ser avaliada.
        ans (Optional[float]): Valor opcional do resultado da última operação (ANS).

    Retorno:
        float: Resultado numérico computado.

    Levanta:
        ExpressaoInvalidaError: Caso a expressão contenha sintaxe inválida, nós desconhecidos
                                ou exceda limites de tamanho e complexidade.
        ErroValidacao: Caso literais numéricos violem limites de segurança.
        ErroAritmetico / DivisaoPorZeroError / RadicandoNegativoError: Em erros de cálculo numérico.
    """
    texto_limpo = sanitizar_texto(expressao_bruta)

    if not texto_limpo:
        raise ExpressaoInvalidaError("A expressão matemática não pode estar vazia.")

    if len(texto_limpo) > LIMITE_TAMANHO_EXPRESSAO:
        raise ExpressaoInvalidaError(
            f"A expressão excede o limite máximo permitido de {LIMITE_TAMANHO_EXPRESSAO} caracteres."
        )

    # 1. Normalização prévia de símbolos visuais
    expressao_normalizada = _normalizar_simbolos(texto_limpo)

    # 2. Análise Léxica (Tokenização)
    tokens = _tokenizar(expressao_normalizada)

    # 3. Análise Sintática (Geração da AST própria)
    parser = _Parser(tokens)
    arvore_ast = parser.parse()

    # 4. Avaliação Recursiva da AST
    avaliador = _AvaliadorAST(ans=ans)
    resultado = avaliador.avaliar(arvore_ast)

    return _assegurar_numero_valido(resultado)
