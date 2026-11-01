# Calculadora Python | Engenharia de Software

Este repositório mantém duas versões independentes da calculadora: a baseline publicada `v2.0.0`, preservada na raiz, e a evolução `v2.1.0`, organizada em `v2.1.0/`. Cada versão possui seus próprios arquivos de aplicação, interfaces e testes. A documentação compartilhada permanece na raiz. O projeto foi desenvolvido como atividade prática no contexto da **Imersão Engenharia de Software: Dev na Era da IA**, iniciativa da [**Alura Imersões**](https://www.alura.com.br/), realizada em parceria com o [**Google for Startups**](https://startup.google.com/intl/pt-BR/).

O desenvolvimento contou com o apoio de ferramentas de inteligência artificial em diferentes etapas da jornada: **Google AI Studio**, utilizado no Desafio 1, e **Google Antigravity**, utilizado no Desafio 2. Essas ferramentas apoiaram a concepção, implementação e evolução da aplicação, sem substituir a análise das decisões técnicas, a compreensão do código ou a validação dos resultados.

Este repositório tem finalidade educacional e demonstra conceitos de Engenharia de Software, como modularidade, separação de responsabilidades, validação de entradas e testes automatizados. Não é um produto oficial da Alura ou do Google, nem representa endosso dessas empresas.

 > **Versão publicada:** `v2.0.0` (baseline histórica preservada). **Desenvolvimento:** branch `desafio-2-revisao-final`, evolução `v2.1.0` ainda não publicada. Na validação informada pelo usuário, a suíte Python teve 92/92 aprovações em 31/10/2026 e a suíte Web teve 31/31 aprovações em 01/11/2026. Em 01/11/2026, o usuário também confirmou a execução integrada local via `app.py`, incluindo operação básica, expressão com potência ou raiz, histórico e `ANS`. A evolução `v2.1.0` permanece não publicada.

---

## O que você encontra neste projeto

- **v2.0.0 (raiz):** baseline publicada com calculadora desktop Tkinter e interface Web original, operações básicas, validação dos operandos e testes históricos.
- **v2.1.0 (`v2.1.0/`):** evolução com expressões matemáticas, potenciação (`^`), raízes, valor absoluto, inverso, troca de sinal, percentual contextual, histórico e `ANS`.
- **Memória na interface desktop da v2.1.0:** MC, MR, M+, M- e MS.
- **Interfaces da v2.1.0:** desktop nativa com Tkinter e Web com HTML5, CSS3, JavaScript Vanilla e Pyodide / WebAssembly.
- **Reutilização da lógica Python na v2.1.0:** as interfaces desktop e Web utilizam os módulos Python da própria versão.
- **Entradas localizadas:** aceita ponto ou vírgula como separador decimal (`12,5` ou `12.5`) na evolução documentada.
- **Validação de entradas e tratamento de erros:** incluindo valores não finitos e divisão por zero.
- **Testes independentes por versão:** a baseline mantém seus quantitativos históricos; a evolução possui 92 testes Python e 31 cenários Web, com resultados informados pelo usuário.

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
alura-calculadora-python/
├── calculadora/                 # Aplicação Python da v2.0.0
├── tests/                       # Testes Python da v2.0.0
├── v2.1.0/                      # Aplicação independente da v2.1.0
│   ├── calculadora/
│   ├── tests/
│   ├── app.js
│   ├── app.py
│   ├── index.html
│   ├── main.py
│   ├── style.css
│   ├── testes.html
│   └── tests_web.js
├── docs/                        # Documentação compartilhada
├── .gitignore
├── .nojekyll
├── app.js                       # Interface Web da v2.0.0
├── app.py                       # Servidor HTTP local
├── CHANGELOG.md
├── index.html                   # Entrada Web da v2.0.0
├── LICENSE
├── main.py                      # Entrada desktop da v2.0.0
├── README.md
├── style.css
├── testes.html
└── tests_web.js
```

A raiz serve a versão `v2.0.0`. A pasta `v2.1.0/` contém a evolução sem substituir os arquivos da baseline. `docs/`, `README.md`, `CHANGELOG.md` e `LICENSE` são compartilhados e não foram duplicados dentro da pasta da versão.

---

## Como Executar

A versão executada depende do diretório de trabalho.

### v2.0.0 — aplicação preservada na raiz

**Desktop (Tkinter):**

```bash
python3 main.py
```

**Web (Pyodide):**

```bash
python3 app.py
```

Acesse `http://localhost:3000/` para a calculadora e `http://localhost:3000/testes.html` para os testes Web da v2.0.0.

### v2.1.0 — aplicação em `v2.1.0/`

**Desktop (Tkinter):**

```bash
cd v2.1.0
python3 main.py
```

**Web (Pyodide):**

Com o terminal na raiz do repositório, inicie `python3 app.py` e acesse `http://localhost:3000/v2.1.0/` para a calculadora e `http://localhost:3000/v2.1.0/testes.html` para os testes Web da v2.1.0.

O servidor HTTP serve o diretório em que foi iniciado. Também é possível iniciar `python3 app.py` de dentro de `v2.1.0/` para servir essa versão na raiz de um servidor separado.

**Observação:** as interfaces Web carregam o Pyodide v0.27.8 pela CDN oficial e precisam de conexão com a internet para carregar o runtime.

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

As versões possuem suítes independentes. Execute cada uma a partir do diretório correspondente para evitar importar os módulos da versão errada.

### v2.0.0 — testes Python da raiz

```bash
python3 -m unittest discover -s tests -v
```

A baseline publicada possui 25 testes Python e 11 cenários Web, conforme os registros da versão `v2.0.0`.

### v2.1.0 — testes Python

```bash
cd v2.1.0
python3 -m unittest discover -s tests -v
```

Resultado informado pelo usuário em 31/10/2026: **92/92 testes aprovados**.

### Testes Web

Com o servidor iniciado na raiz:

- v2.0.0: `http://localhost:3000/testes.html`
- v2.1.0: `http://localhost:3000/v2.1.0/testes.html`

Resultado informado pelo usuário em 01/11/2026 para a v2.1.0: **31/31 cenários aprovados, 0 falhas e 0 não executados**.

Os resultados acima são registros das execuções informadas pelo usuário; esta atualização documental não representa uma nova execução dos testes.

---

## Organização Interna

- **Raiz:** aplicação histórica `v2.0.0`, com arquivos Python, interface Web e testes próprios.
- **`v2.1.0/`:** aplicação evoluída, com módulos Python, interface Web e testes próprios.
- **`docs/`:** plano original, registro de divergências e estado atual compartilhados.
- **`README.md`, `CHANGELOG.md` e `LICENSE`:** documentação e licença comuns ao repositório.
- **`.nojekyll`:** permanece na raiz para a publicação estática no GitHub Pages.

As referências de recursos das interfaces Web são relativas ao diretório de cada versão. Assim, a aplicação em `v2.1.0/` carrega os arquivos correspondentes dentro desse subdiretório.

---

## Limitações Conhecidas

- Os cálculos utilizam o tipo `float` de precisão dupla (64 bits). Para aplicações financeiras que exijam arredondamento monetário estrito, o módulo `decimal.Decimal` seria uma alternativa.
- A formatação dos resultados limita a exibição a até oito casas decimais.
- A interface Tkinter requer um ambiente desktop com suporte gráfico.
- A interface web depende do carregamento do Pyodide pela CDN oficial e de conexão com a internet para inicialização do runtime.

---

## Estado das Versões

- **v2.0.0:** baseline publicada, preservada na raiz do repositório.
- **v2.1.0:** evolução validada no escopo documentado, organizada em `v2.1.0/`; ainda não publicada como release.
- A coexistência dos diretórios na branch de trabalho não altera, por si só, a branch `main` nem a publicação existente.
- Os resultados de validação da v2.1.0 estão registrados neste README e em `docs/ESTADO-ATUAL.md`.

---

## Contexto Acadêmico e Ferramentas

O projeto foi desenvolvido no contexto de um desafio educacional da **Imersão Engenharia de Software: Dev na Era da IA**, promovida pela Alura. O enunciado propõe a criação de uma calculadora em Python utilizando recursos de inteligência artificial. Nesta atividade, o **Google AI Studio** foi a ferramenta escolhida para apoiar a concepção e a evolução da aplicação.

O uso dessas ferramentas fez parte do processo de desenvolvimento e não substitui a compreensão dos conceitos de Engenharia de Software, a análise das decisões técnicas ou a execução dos testes automatizados.

Alura e Google são mencionadas exclusivamente para identificar o contexto educacional e a ferramenta de apoio utilizada. Este projeto independente não é afiliado, patrocinado ou oficialmente endossado por essas empresas.

---

## Contribuições e Licença

Sugestões e relatos de problemas podem ser enviados por meio das *Issues* e *Pull Requests* do repositório.

Este projeto está disponibilizado sob a licença [MIT](LICENSE). Consulte o arquivo `LICENSE` para conhecer os termos de uso, modificação e distribuição.
