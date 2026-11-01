# Calculadora Python | Engenharia de Software

Uma calculadora com duas interfaces complementares: desktop nativa com **Tkinter** e web client-side com **Pyodide / WebAssembly**, desenvolvida como atividade prática no contexto da **Imersão Engenharia de Software: Dev na Era da IA**, iniciativa da [**Alura Imersões**](https://www.alura.com.br/), realizada em parceria com o [**Google for Startups**](https://startup.google.com/intl/pt-BR/).

O desenvolvimento contou com o apoio de ferramentas de inteligência artificial em diferentes etapas da jornada: **Google AI Studio**, utilizado no Desafio 1, e **Google Antigravity**, utilizado no Desafio 2. Essas ferramentas apoiaram a concepção, implementação e evolução da aplicação, sem substituir a análise das decisões técnicas, a compreensão do código ou a validação dos resultados.

Este repositório tem finalidade educacional e demonstra conceitos de Engenharia de Software, como modularidade, separação de responsabilidades, validação de entradas e testes automatizados. Não é um produto oficial da Alura ou do Google, nem representa endosso dessas empresas.

 > **Versão publicada:** `v2.0.0` (baseline histórica preservada). **Desenvolvimento:** branch `desafio-2-revisao-final`, evolução `v2.1.0` ainda não publicada. Na validação informada pelo usuário, a suíte Python teve 92/92 aprovações em 31/10/2026 e a suíte Web teve 31/31 aprovações em 01/11/2026. Em 01/11/2026, o usuário também confirmou a execução integrada local via `app.py`, incluindo operação básica, expressão com potência ou raiz, histórico e `ANS`. A evolução `v2.1.0` permanece não publicada.

---

## O que você encontra neste projeto

- **Expressões matemáticas:** operações aritméticas, potenciação (`^`), raízes, valor absoluto, inverso e troca de sinal.
- **Percentual contextual:** por exemplo, `100 + 10%` resulta em `110`.
- **Raiz de índice n:** função `root(rad; ind)`, com ponto e vírgula como separador de argumentos.
- **Histórico e ANS:** recuperação de cálculos anteriores e continuidade de expressões com o último resultado.
- **Memória na interface desktop:** MC, MR, M+, M- e MS.
- **Duas interfaces complementares:**
  - **Desktop (Tkinter):** janela nativa do Python.
  - **Web (Pyodide / WebAssembly):** interface HTML5, CSS3 e JavaScript Vanilla que executa os módulos Python existentes diretamente no navegador, sem Node.js, npm ou frameworks.
- **Reutilização da lógica Python:** as duas interfaces utilizam os mesmos módulos de validação e operações matemáticas.
- **Entradas localizadas:** aceita ponto ou vírgula como separador decimal (`12,5` ou `12.5`).
- **Validação de entradas:** rejeita campos vazios, entradas alfanuméricas e valores não finitos (`inf`, `nan`).
- **Divisão por zero controlada:** apresenta mensagem específica e amigável.
- **Recursos de acessibilidade:** navegação por teclado, identificação textual dos estados e agrupamento semântico dos controles.
- **Duas suítes de testes automatizados independentes:** 92 testes Python no terminal e 31 cenários web no navegador na branch de desenvolvimento. A baseline publicada `v2.0.0` permanece preservada com seus quantitativos históricos.

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
│   ├── calculadora-2.0-plano.md\n│   ├── ESTADO-ATUAL.md\n│   └── REGISTRO-DIVERGENCIAS.md
├── .nojekyll                 # Desativa o processamento Jekyll no GitHub Pages
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

## Sintaxe de Expressões

A calculadora avalia expressões completas, com parênteses e precedência matemática.

| Recurso | Sintaxe | Exemplo |
|---|---|---|
| Operações básicas | `+`, `-`, `*`, `/` | `10 + 5 * 2` |
| Potenciação | `^` | `2^3` |
| Raiz quadrada | `sqrt(valor)` ou `√valor` | `sqrt(144)` |
| Raiz de índice n | `root(rad; ind)` | `root(12,5; 3)` |
| Valor absoluto | `abs(valor)` | `abs(-8)` |
| Inverso | `inv(valor)` | `inv(4)` |
| Percentual | `valor%` | `10%` |
| Percentual contextual | `base + taxa%` ou `base - taxa%` | `100 + 10%` resulta em `110` |
| Resultado anterior | `ANS` | `ANS + 5` |

O ponto e vírgula (`;`) separa argumentos de funções com mais de um parâmetro. A vírgula continua disponível como separador decimal: `root(12,5; 3)`.

## Atalhos de Teclado

Os atalhos variam ligeiramente entre as interfaces:

- **Desktop (Tkinter):** dígitos, ponto ou vírgula decimal, operadores `+`, `-`, `*`, `/`, `^`, parênteses, `;` e `%`; `Enter` calcula, `Backspace` apaga, `Esc` ou `Delete` limpa e `Ctrl+C` copia o resultado.
- **Web:** dígitos, ponto decimal, operadores `+`, `-`, `*`, `/` e parênteses; `Enter` ou `=` calcula, `Backspace` apaga e `Esc` limpa. Os demais recursos podem ser inseridos pelos botões da interface.

---

## Como Executar os Testes Automatizados

O projeto possui duas suítes de testes independentes e complementares.

### A. Testes Python (`unittest`) — 92 testes na branch de desenvolvimento

Testam as operações matemáticas, a validação de entradas e os fluxos de integração, sem necessidade de abrir a interface gráfica.

```bash
python3 -m unittest discover -s tests -v
```

<details>
<summary>Ver resumo dos testes Python da baseline publicada</summary>

- 13 testes de operações matemáticas e formatação.
- 7 testes de validação de entradas.
- 5 testes de integração dos fluxos da aplicação.

**Baseline `v2.0.0`:** 25 testes aprovados na validação da publicação. **Branch de desenvolvimento:** 92/92 aprovados, conforme execução informada pelo usuário em 31/10/2026.

</details>

### B. Testes Web (`tests_web.js`) — 31 cenários na branch de desenvolvimento

Validam o funcionamento da interface web no navegador, incluindo inicialização do Pyodide, carregamento dos módulos Python, operações matemáticas, validações, limpeza dos campos e gerenciamento dos recursos utilizados na integração.

Para executar:

1. Inicie o servidor local conforme as instruções anteriores.
2. Acesse `http://localhost:3000/testes.html`.
3. Acompanhe os resultados apresentados na página.

**Baseline `v2.0.0`:** 11 testes web. **Branch de desenvolvimento:** 31/31 aprovados, 0 falhas e 0 não executados, conforme resultado exibido na página e informado pelo usuário em 01/11/2026.

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

## Estado da Evolução

O histórico de sessão, a recuperação de resultados anteriores via `ANS`, a continuidade de expressões, os atalhos de teclado e as operações de memória já fazem parte da implementação em desenvolvimento nesta branch. A validação integrada local via `app.py` foi confirmada pelo usuário em 01/11/2026. A Fase 5 está concluída no escopo documentado; a evolução `v2.1.0` ainda não foi publicada.

---

## Contexto Acadêmico e Ferramentas

O projeto foi desenvolvido no contexto de um desafio educacional da **Imersão Engenharia de Software: Dev na Era da IA**, promovida pela Alura. O enunciado propõe a criação de uma calculadora em Python utilizando recursos de inteligência artificial. Nesta atividade, o **Google AI Studio** foi a ferramenta escolhida para apoiar a concepção e a evolução da aplicação.

O uso dessas ferramentas fez parte do processo de desenvolvimento e não substitui a compreensão dos conceitos de Engenharia de Software, a análise das decisões técnicas ou a execução dos testes automatizados.

Alura e Google são mencionadas exclusivamente para identificar o contexto educacional e a ferramenta de apoio utilizada. Este projeto independente não é afiliado, patrocinado ou oficialmente endossado por essas empresas.

---

## Contribuições e Licença

Sugestões e relatos de problemas podem ser enviados por meio das *Issues* e *Pull Requests* do repositório.

Este projeto está disponibilizado sob a licença [MIT](LICENSE). Consulte o arquivo `LICENSE` para conhecer os termos de uso, modificação e distribuição.
