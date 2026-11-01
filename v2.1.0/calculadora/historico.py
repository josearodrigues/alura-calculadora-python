"""
Módulo responsável pelo modelo de dados e gestão de sessão de histórico e ANS.

Implementa o controle de histórico de cálculos em memória durante a sessão e a gestão
independente do valor do último resultado (ANS), garantindo que a limpeza do histórico
não anule a capacidade de continuidade dos cálculos matemáticos.
"""

import time
from dataclasses import dataclass, field
from typing import List, Optional

from calculadora.operacoes import formatar_resultado


class RegistroNaoEncontradoError(Exception):
    """Exceção levantada quando um registro de histórico solicitado por ID não é encontrado."""
    pass


@dataclass(frozen=True)
class EntradaHistorico:
    """
    Representa uma entrada individual de cálculo registrada no histórico da sessão (imutável).
    """
    id: int
    expressao: str
    expressao_formatada: str
    resultado: float
    resultado_formatado: str
    timestamp: float = field(default_factory=time.time)


class HistoricoSessao:
    """
    Gerenciador da sessão de histórico de cálculos e do estado de ANS em memória.

    Regras fundamentais:
    1. Mantém uma lista ordenada de entradas com IDs sequenciais.
    2. O estado do ANS é atualizado a cada cálculo registrado.
    3. Recuperar uma entrada anterior define explicitamente o resultado daquela entrada como o ANS ativo.
    4. A ação limpar_historico() limpa as entradas visíveis, mas PRESERVA o valor do ANS ativo.
    5. Apenas resetar_sessao() zera o histórico e o ANS simultaneamente.
    """

    def __init__(self) -> None:
        self._entradas: List[EntradaHistorico] = []
        self._ans: Optional[float] = None
        self._proximo_id: int = 1

    def registrar(self, expressao: str, expressao_formatada: str, resultado: float) -> EntradaHistorico:
        """
        Registra uma operação concluída no histórico e atualiza o ANS ativo.

        Parâmetros:
            expressao (str): Expressão bruta original informada pelo usuário.
            expressao_formatada (str): Expressão normalizada para exibição.
            resultado (float): Valor numérico real resultante do cálculo.

        Retorno:
            EntradaHistorico: Instância imutável da entrada registrada.
        """
        entrada = EntradaHistorico(
            id=self._proximo_id,
            expressao=expressao,
            expressao_formatada=expressao_formatada,
            resultado=resultado,
            resultado_formatado=formatar_resultado(resultado),
        )
        self._entradas.append(entrada)
        self._ans = resultado
        self._proximo_id += 1
        return entrada

    def obter_todos(self) -> List[EntradaHistorico]:
        """
        Retorna uma cópia da lista de entradas do histórico ordenadas cronologicamente.
        """
        return list(self._entradas)

    def recuperar_entrada(self, id_entrada: int) -> EntradaHistorico:
        """
        Localiza uma entrada pelo seu identificador único, atualiza o ANS ativo
        para o resultado dessa entrada e a retorna.

        Parâmetros:
            id_entrada (int): ID da entrada a ser recuperada.

        Retorno:
            EntradaHistorico: Entrada localizada.

        Levanta:
            RegistroNaoEncontradoError: Caso o ID não exista no histórico atual.
        """
        for entrada in self._entradas:
            if entrada.id == id_entrada:
                self._ans = entrada.resultado
                return entrada
        raise RegistroNaoEncontradoError(f"Registro de histórico #{id_entrada} não encontrado.")

    def obter_ans(self) -> Optional[float]:
        """
        Retorna o valor numérico puro do último resultado calculado (ANS),
        ou None se nenhum cálculo foi realizado ou se a sessão foi resetada.
        """
        return self._ans

    def limpar_historico(self) -> None:
        """
        Esvazia a lista de entradas de histórico da sessão.
        IMPORTANTE: O valor de _ans é preservado integralmente para continuidade.
        """
        self._entradas.clear()

    def resetar_sessao(self) -> None:
        """
        Redefine completamente a sessão, esvaziando o histórico e anulando o ANS.
        """
        self._entradas.clear()
        self._ans = None
        self._proximo_id = 1
