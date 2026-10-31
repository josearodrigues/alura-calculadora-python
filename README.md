# Calculadora Python | Engenharia de Software

Uma calculadora com duas interfaces complementares: desktop nativa com **Tkinter** e web client-side com **Pyodide / WebAssembly**, desenvolvida como atividade acadêmica do desafio proposto na **Imersão Engenharia de Software: Dev na Era da IA**, da [Alura](https://www.alura.com.br/).

O desafio foi realizado com o **Google AI Studio** como ferramenta de apoio à geração e evolução da aplicação. A solução foi organizada em módulos Python, acompanhada de testes automatizados e documentada para facilitar a compreensão de sua estrutura e funcionamento.

Este repositório tem finalidade educacional e demonstra conceitos de Engenharia de Software, como modularidade, separação de responsabilidades, validação de entradas e testes automatizados. Não é um produto oficial da Alura ou do Google, nem representa endosso dessas empresas.

> **Status:** a publicação da versão `v2.0.0` ainda está pendente. A aplicação possui a interface desktop original em Tkinter e uma interface web complementar que executa Python no navegador via Pyodide v0.27.8. As duas suítes de testes foram aprovadas: 25 testes Python (`unittest`) e 11 testes web.

---

## O que você encontra neste projeto

- **Quatro operações aritméticas:** adição, subtração, multiplicação e divisão.
- **Duas interfaces complementares:**
  - **Desktop (Tkinter):** janela nativa do Python.
  - **Web (Pyodide / WebAssembly):** interface HTML5, CSS3 e JavaScript Vanilla que executa os módulos Python existentes diretamente no navegador, sem Node.js, npm ou frameworks.
- **Reutilização da lógica Python:** as duas interfaces utilizam os mesmos módulos de validação e operações matemáticas.
- **Entradas localizadas:** aceita ponto ou vírgula como separador decimal (`12,5` ou `12.5`).
- **Validação de entradas:** rejeita campos vazios, entradas alfanuméricas e valores não finitos (`inf`, `nan`).
- **Divisão por zero controlada:** apresenta mensagem específica e amigável.
- **Recursos de acessibilidade:** navegação por teclado, identificação textual dos estados e agrupamento semântico dos controles.
- **Duas suítes de testes automatizados independentes:** 25 testes Python no terminal e 11 testes web no navegador.

---

## Tecnologias Utilizadas

| Tecnologia / Recurso | Uso no Projeto |
|---|---|
| Python | Linguagem principal e lógica das operações |
| Tkinter | Interface gráfica desktop |
| Pyodide v0.27.8 | Execução de Python no navegador via WebAssembly |
| HTML5 e CSS3 | Estrutura e apresentação da interface web |
| JavaScript Vanilla | Interação com a interface web |
| `unittest` | Testes automatizados da aplicação Python |
| `tests_web.js` | Testes automatizados da interface web |

---

## Estrutura do Projeto

```text
calculadora-python/
├── calculadora/
│   ├── __init__.py
│   ├── interface.py          # Interface desktop Tkinter
│   ├── operacoes.py          # Operações matemáticas e formatação
│   └── validacao.py          # Validação e conversão de entradas
├── tests/
│   ├── __init__.py
│   ├── test_integracao.py
│   ├── test_operacoes.py
│   └── test_validacao.py
├── docs/
│   └── implementation_plan.md
├── index.html                # Interface web
├── style.css                 # Estilos da interface web
├── app.js                    # Integração da interface web com Python
├── tests_web.js              # Testes automatizados web
├── testes.html               # Executador visual dos testes web
├── app.py                    # Servidor HTTP local
├── main.py                   # Ponto de entrada desktop
├── CHANGELOG.md
├── LICENSE
└── README.md
```

---

## Como Executar

### 1. Aplicação Desktop (Tkinter)

#### Pré-requisitos
- Python 3 com suporte ao módulo `tkinter`.
- Ambiente desktop com servidor gráfico ativo.

Para verificar a disponibilidade do Tkinter:

```bash
python3 -m tkinter
```

No Ubuntu/Debian, se necessário:

```bash
sudo apt update && sudo apt install python3-tk
```

#### Executar

```bash
# Windows
python main.py

# Linux / macOS
python3 main.py
```

---

### 2. Interface Web (Pyodide / WebAssembly)

A interface web pode ser servida localmente utilizando o servidor HTTP da Biblioteca Padrão do Python, sem necessidade de Node.js ou npm.

```bash
python3 app.py
```

Alternativamente:

```bash
python3 -m http.server 3000 --bind 127.0.0.1
```

- Calculadora web: `http://localhost:3000`
- Testes web: `http://localhost:3000/testes.html`

**Observação:** a interface web carrega o Pyodide v0.27.8 pela CDN oficial e, portanto, necessita de conexão com a internet para carregar o runtime.

---

## Como Executar os Testes Automatizados

O projeto possui duas suítes de testes independentes e complementares.

### A. Testes Python (`unittest`) — 25 testes

Testam as operações matemáticas, a validação de entradas e os fluxos de integração, sem necessidade de abrir a interface gráfica.

```bash
python3 -m unittest discover -s tests -v
```

<details>
<summary>Ver resumo dos 25 testes Python</summary>

- 13 testes de operações matemáticas e formatação.
- 7 testes de validação de entradas.
- 5 testes de integração dos fluxos da aplicação.

**Resultado confirmado:** 25 testes aprovados.

</details>

### B. Testes Web (`tests_web.js`) — 11 testes

Validam o funcionamento da interface web no navegador, incluindo inicialização do Pyodide, carregamento dos módulos Python, operações matemáticas, validações, limpeza dos campos e gerenciamento dos recursos utilizados na integração.

Para executar:

1. Inicie o servidor local conforme as instruções anteriores.
2. Acesse `http://localhost:3000/testes.html`.
3. Acompanhe os resultados apresentados na página.

**Resultado confirmado:** 11 testes aprovados.

---

## Organização Interna

- **`calculadora/operacoes.py`:** implementação das operações matemáticas e formatação dos resultados.
- **`calculadora/validacao.py`:** validação e conversão dos operandos.
- **`calculadora/interface.py`:** interface gráfica desktop com Tkinter.
- **`app.js`:** integração da interface web com os módulos Python executados pelo Pyodide.
- **`index.html` e `style.css`:** estrutura e apresentação da interface web.
- **`app.py`:** servidor HTTP local para disponibilizar a interface web.
- **`tests/` e `tests_web.js`:** suítes de testes automatizados.

A lógica das operações e validações permanece nos módulos Python, compartilhados pelas duas interfaces.

---

## Limitações Conhecidas

- Os cálculos utilizam o tipo `float` de precisão dupla (64 bits). Para aplicações financeiras que exijam arredondamento monetário estrito, o módulo `decimal.Decimal` seria uma alternativa.
- A formatação dos resultados limita a exibição a até oito casas decimais.
- A interface Tkinter requer um ambiente desktop com suporte gráfico.
- A interface web depende do carregamento do Pyodide pela CDN oficial e de conexão com a internet para inicialização do runtime.

---

## Próximas Evoluções

- Histórico de cálculos durante a sessão, mantido em memória.
- Atalhos de teclado numérico para seleção rápida de operadores (`+`, `-`, `*`, `/`).
- Reutilização do resultado da operação anterior como Operando A do próximo cálculo.

---

## Contexto Acadêmico e Ferramentas

O projeto foi desenvolvido no contexto de um desafio educacional da **Imersão Engenharia de Software: Dev na Era da IA**, promovida pela Alura. O enunciado propõe a criação de uma calculadora em Python utilizando recursos de inteligência artificial. Nesta atividade, o **Google AI Studio** foi a ferramenta escolhida para apoiar a concepção e a evolução da aplicação.

O uso dessas ferramentas fez parte do processo de desenvolvimento e não substitui a compreensão dos conceitos de Engenharia de Software, a análise das decisões técnicas ou a execução dos testes automatizados.

Alura e Google são mencionadas exclusivamente para identificar o contexto educacional e a ferramenta de apoio utilizada. Este projeto independente não é afiliado, patrocinado ou oficialmente endossado por essas empresas.

---

## Contribuições e Licença

Sugestões e relatos de problemas podem ser enviados por meio das *Issues* e *Pull Requests* do repositório.

Este projeto está disponibilizado sob a licença [MIT](LICENSE). Consulte o arquivo `LICENSE` para conhecer os termos de uso, modificação e distribuição.
