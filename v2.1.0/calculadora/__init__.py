"""
Pacote da Calculadora Modular.
Desenvolvido com foco em boas práticas de Engenharia de Software.
"""

from .expressoes import (
    ExpressaoInvalidaError,
    avaliar_expressao,
)
from .historico import (
    EntradaHistorico,
    HistoricoSessao,
    RegistroNaoEncontradoError,
)
from .operacoes import (
    DivisaoPorZeroError,
    ErroAritmetico,
    OperacaoInvalidaError,
    RadicandoNegativoError,
    calcular,
    dividir,
    executar_operacao_segura,
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
from .validacao import (
    ErroValidacao,
    converter_operando,
    sanitizar_texto,
    validar_literal_numerico,
)

__all__ = [
    # Operações fundamentais e avançadas
    "somar",
    "subtrair",
    "multiplicar",
    "dividir",
    "potencia",
    "raiz_quadrada",
    "raiz_n",
    "valor_absoluto",
    "inverso",
    "trocar_sinal",
    "calcular",
    "formatar_resultado",
    "executar_operacao_segura",
    # Exceções de domínio
    "ErroAritmetico",
    "DivisaoPorZeroError",
    "RadicandoNegativoError",
    "OperacaoInvalidaError",
    "ErroValidacao",
    "ExpressaoInvalidaError",
    "RegistroNaoEncontradoError",
    # Validação e sanitização
    "converter_operando",
    "sanitizar_texto",
    "validar_literal_numerico",
    # Motor de expressões
    "avaliar_expressao",
    # Histórico e Sessão
    "EntradaHistorico",
    "HistoricoSessao",
]
