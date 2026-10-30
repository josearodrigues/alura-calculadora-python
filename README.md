# Calculadora Python | Engenharia de Software

Uma calculadora desktop desenvolvida em **Python e Tkinter** como atividade acadêmica do desafio proposto na **Imersão Engenharia de Software: Dev na Era da IA**, da [Alura](https://www.alura.com.br/).

O desafio foi realizado com o **Google AI Studio** como ferramenta de apoio à geração da aplicação. A solução resultante foi organizada em módulos Python, acompanhada de testes automatizados e documentada para permitir a compreensão de sua estrutura e de suas decisões técnicas.

Este repositório tem finalidade educacional e demonstra conceitos de organização de código, separação de responsabilidades, validação de entradas e testes. Não é um produto oficial da Alura ou do Google, nem representa endosso dessas empresas.

> **Status:** preparação da versão `v1.0.0`. A aplicação já foi executada manualmente pelo responsável pelo projeto em ambiente desktop, que confirmou seu funcionamento. A suíte automatizada também foi executada: 25 testes aprovados.

## O que você encontra neste projeto

- **Quatro operações:** adição, subtração, multiplicação e divisão.
- **Entradas localizadas:** aceita ponto ou vírgula como separador decimal.
- **Validação de dados:** trata campos vazios, entradas inválidas e valores não finitos.
- **Divisão por zero controlada:** apresenta uma mensagem específica em vez de interromper o fluxo normal da aplicação.
- **Uso contínuo:** permite realizar cálculos sucessivos e limpar os campos para uma nova operação.
- **Atalho de teclado:** pressione `Enter` em um dos campos para calcular.
- **Testes automatizados:** cobertura das operações, validações e fluxos integrados com `unittest`.

## Interface

A aplicação utiliza Tkinter, biblioteca gráfica da distribuição padrão do Python. A janela reúne os campos dos dois operandos, a seleção da operação, os botões de ação e a área de resultado ou mensagem de erro.

## Tecnologias e decisões técnicas

| Tecnologia / recurso | Uso no projeto |
|---|---|
| Python 3 | Linguagem da aplicação |
| Tkinter | Interface gráfica desktop |
| `unittest` | Testes automatizados, sem dependências externas |
| Type hints e docstrings | Documentação e legibilidade do código |
| Tabela de despacho | Encaminhamento da operação escolhida para a função correspondente |
| Exceções específicas | Tratamento explícito de erros de validação, operação e divisão por zero |

A lógica matemática e a validação ficam em módulos próprios, sem depender da interface gráfica. Essa separação permite testar as regras principais sem abrir uma janela.

## Estrutura do projeto

```text
calculadora-python/
├── calculadora/
│   ├── __init__.py
│   ├── interface.py       # Interface gráfica Tkinter
│   ├── operacoes.py       # Operações matemáticas e formatação
│   └── validacao.py       # Sanitização, validação e conversão
├── tests/
│   ├── __init__.py
│   ├── test_integracao.py
│   ├── test_operacoes.py
│   └── test_validacao.py
├── docs/
│   └── implementation_plan.md  # Planejamento de uma possível evolução com Pyodide
├── .gitignore
├── main.py                # Ponto de entrada
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## Como executar

### Pré-requisitos

- Python 3.8 ou superior.
- Tkinter disponível na instalação do Python.
- Um ambiente desktop com suporte gráfico para abrir a janela.

Para verificar se o Tkinter está disponível:

```bash
python3 -m tkinter
```

No Ubuntu ou Debian, caso o módulo não esteja instalado:

```bash
sudo apt update
sudo apt install python3-tk
```

No Windows, normalmente use o interpretador Python instalado pelo instalador oficial. No macOS, a disponibilidade do Tkinter depende da distribuição do Python utilizada; verifique com o comando acima.

### Iniciar a calculadora

Na pasta raiz do projeto, execute:

```bash
python main.py
```

Em ambientes nos quais o comando `python` aponta para outra versão, use:

```bash
python3 main.py
```

## Como executar os testes

Os testes não precisam abrir a interface gráfica e não exigem bibliotecas de terceiros.

Na raiz do projeto, execute:

```bash
python3 -m unittest discover -s tests -v
```

### Resultado da última execução registrada

<details>
<summary>Ver resumo dos testes</summary>

```text
Ran 25 tests
OK
```

Execução de verificação em 30/10/2026, com Python 3.13.5: **25 testes passaram**.

</details>

Esse resultado valida a suíte automatizada nesse ambiente. Separadamente, a interface gráfica foi executada em ambiente desktop pelo responsável pelo projeto, que confirmou seu funcionamento.

## Organização interna

- **`calculadora/operacoes.py`:** implementa as funções de adição, subtração, multiplicação e divisão. Também contém a tabela que associa os símbolos às operações e a formatação do resultado.
- **`calculadora/validacao.py`:** remove espaços nas extremidades, normaliza a vírgula decimal, converte os operandos e rejeita entradas vazias, inválidas ou não finitas.
- **`calculadora/interface.py`:** constrói a janela, recebe as entradas e encaminha os dados para os módulos de validação e cálculo.
- **`main.py`:** ponto de entrada que inicializa a aplicação e apresenta orientações quando o ambiente gráfico ou o Tkinter não estão disponíveis.

A aplicação não utiliza `eval()` para interpretar entradas ou executar operações. Os cálculos são realizados por funções Python explícitas.

## Limitações conhecidas

- Os cálculos utilizam `float` (ponto flutuante binário). Portanto, não são indicados para aplicações financeiras que exijam precisão decimal estrita.
- A apresentação do resultado limita a formatação a até oito casas decimais. Isso melhora a legibilidade, mas pode arredondar valores com mais casas relevantes.
- A interface Tkinter requer um ambiente gráfico; os testes de lógica podem ser executados em ambientes sem monitor ou display.

## Próximas evoluções

As ideias abaixo são possibilidades futuras, não funcionalidades incluídas nesta versão:

- Histórico de cálculos durante a sessão.
- Atalhos de teclado para selecionar operações.
- Reutilização do resultado anterior como operando de um novo cálculo.
- Investigação de uma execução no navegador com Pyodide, mantendo clara a distinção entre o aplicativo desktop atual e uma eventual versão web.

O planejamento dessa possível evolução está em [`docs/implementation_plan.md`](docs/implementation_plan.md).

## Contexto acadêmico e ferramentas

O projeto foi desenvolvido no contexto de um desafio educacional da Imersão Engenharia de Software: Dev na Era da IA, promovida pela Alura. O enunciado propõe a criação de uma calculadora em Python utilizando recursos de inteligência artificial; nesta atividade, o Google AI Studio foi a ferramenta escolhida para apoiar a geração inicial da aplicação.

O uso dessas ferramentas faz parte do contexto de desenvolvimento e não substitui a análise do código, a compreensão das decisões técnicas ou a execução dos testes. Este README descreve o estado efetivo do projeto: funcionalidades implementadas, verificações realizadas e evoluções que permanecem apenas como possibilidades.

Alura e Google são mencionadas exclusivamente para identificar o contexto educacional e a ferramenta utilizada. Este projeto independente não é afiliado, patrocinado ou oficialmente endossado por essas empresas.

## Contribuições e licença

Depois da publicação do repositório, sugestões, relatos de problemas e melhorias poderão ser enviados por meio das *Issues* e *Pull Requests* do GitHub. Ao contribuir, descreva o problema ou a motivação da mudança e, quando aplicável, inclua evidências de teste.

Este projeto está disponibilizado sob a licença [MIT](LICENSE). Consulte o arquivo `LICENSE` para conhecer os termos de uso, modificação e distribuição.
