# Calculadora 2.0 — Plano de Implementação (Revisão 4 — Final)

> [!IMPORTANT]
> Este documento é **estritamente para planejamento e alinhamento técnico**. Nenhum arquivo de código foi modificado, nenhuma dependência foi alterada e nenhum commit ou tag foi gerado. A implementação aguarda autorização expressa.

---

## 1. Diagnóstico da Arquitetura Atual

### 1.1 Visão Geral da Baseline

A versão baseline atual (`v2.0.0`, homologada em 2026-10-30) opera em modelo de formulário de dois operandos isolados com botões de rádio para o operador aritmético:

```mermaid
graph TD
    subgraph "Motor Matemático Python Compartilhado (calculadora/)"
        V[validacao.py\nconverter_operando\nsanitizar_texto]
        O[operacoes.py\nsomar, subtrair, multiplicar, dividir\ncalcular, formatar_resultado]
        I[__init__.py\nFachada pública da biblioteca]
    end

    subgraph "Interface Desktop"
        TK[interface.py\nCalculadoraGUI (Tkinter)\nCampos A e B + Radios]
    end

    subgraph "Interface Web (GitHub Pages)"
        HTML[index.html\nCampos A e B + Radios + Telemetria]
        CSS[style.css\nEstilos Light/Dark baseados em media query]
        JS[app.js\nPonte Pyodide e controle de DOM]
        PY[Pyodide v0.27.8 WebAssembly\nMEMFS com /calculadora]
    end

    V --> O --> I
    I --> TK
    I --> PY
    PY --> JS --> HTML
    CSS --> HTML
```

### 1.2 Pontos Fortes Preservados da Baseline

| Dimensão | Situação Atual | Impacto na Evolução |
|---|---|---|
| **Separação de Camadas** | Lógica matemática 100% contida em Python puro. | Mantida. Interfaces web e desktop permanecem como clientes visuais estritos. |
| **Gerenciamento de Memória Pyodide** | Destruição determinística de `PyProxy` em bloco `finally`. | Mantida e expandida para chamadas de avaliação e recuperação. |
| **Suíte de Testes Baseline** | 25 testes Python (`unittest`) + 11 testes de browser (`tests_web.js`). | Preservada integralmente como barreira inegociável de regressão. |
| **Publicação Estática** | Zero build-step no GitHub Pages com `.nojekyll`. | Mantida integralmente sem introduzir empacotadores (Webpack, Vite, etc.). |

---

## 2. Inventário de Funcionalidades Baseline

### Motor Python (`calculadora/`)
- `somar(a, b)`, `subtrair(a, b)`, `multiplicar(a, b)`, `dividir(a, b)`: Funções binárias determinísticas.
- `dividir` com barreira para $b = 0$ gerando `DivisaoPorZeroError`.
- `calcular(a, b, op)`: Dispatch table por dicionário (`MAPA_OPERACOES`).
- `formatar_resultado(valor, precisao_maxima=8)`: Limpeza de sufixos `.0` e tratamento contra ruído flutuante IEEE 754.
- `converter_operando(texto)`: Suporte a vírgula decimal brasileira, rejeição de entradas vazias, `inf` e `nan`.
- `sanitizar_texto(texto)`: Trimming seguro.

### Interfaces Baseline
- **Desktop (Tkinter):** Janela 420×520px com formulário claro (`#F3F4F6`), campos `Entry` para operando A e B, seleção por `Radiobutton`, cálculo com exibição direta.
- **Web (Vanilla JS + Pyodide):** Inicialização assíncrona do WebAssembly, montagem de `/calculadora` no MEMFS, execução de `bridge_calcular`, exibição de telemetria e teste automatizado embutido em `testes.html`.

---

## 3. Comparação: Estado Atual × Requisitos Calculadora 2.0

| Requisito | Baseline Atual | Especificação 2.0 | Solução Técnica |
|---|---|---|---|
| **Operações Básicas (+, -, \*, /)** | Operações binárias isoladas | Encadeadas com precedência matemática | Avaliador recursivo de expressões |
| **Porcentagem (%)** | Ausente | Contextual e isolada com regras formais | Resolução sintática na árvore AST |
| **Potenciação (x² e x^y)** | Ausente | Suporte a potências e quadrados | Operador `^` no avaliador e botão $x^2$ |
| **Raiz Quadrada (√)** | Ausente | Suporte no visor e via teclado | Normalização de `√` e função segura `sqrt()` |
| **Raiz de Índice n (ⁿ√x)** | Ausente | Suporte a reais e negativos com índice ímpar | Função canônica `root(radicando; indice)` |
| **Valor Absoluto (\|x\|)** | Ausente | Suporte via botão e expressão | Função canônica `abs(x)` |
| **Inverso (1/x)** | Ausente | Inversão aritmética com guarda de divisão por zero | Função canônica `inv(x)` |
| **Troca de Sinal (±)** | Ausente | Inversão do termo/resultado | Operador unário `-` contextual |
| **Parênteses** | Ausente | Agrupamento arbitrário com validação | Árvore sintática AST e precedência natural |
| **Continuidade (ANS)** | Ausente | Operador continua; número inicia novo | Gestão de estado unificada em Python |
| **Histórico e Recuperação** | Ausente | Sessão em memória e recuperação ativa | `HistoricoSessao` em Python com método explícito |
| **Área de Transferência** | Ausente | Cópia rápida com feedback visual | Web API Clipboard / Tkinter clipboard |
| **Design Dark Premium** | Formulário claro | Fundo grafite/marinho, ciano, verde, vermelho | CSS customizado + Tkinter Flat Frames |
| **Memória (MC/MR/M+/M-/MS)** | Ausente | **Fora de escopo desta versão** | Botões desabilitados ("Em breve") |

---

## 4. Proposta de Arquitetura e Engenharia Detalhada

```
calculadora/
├── __init__.py          # Fachada pública do pacote
├── operacoes.py         # Funções matemáticas puras com guarda numérica em cada etapa
├── validacao.py         # Higienização de strings e validação de literais numéricos
├── expressoes.py        # Tokenização segura, limites, AST estrita e avaliador recursivo
└── historico.py         # Modelo de dados, Histórico e controle explícito do ANS
```

---

### 4.1. Formalização Sintática do Percentual Contextual

Para superar as limitações de heurísticas textuais e tratar expressões arbitrariamente aninhadas, o operador de porcentagem (`%`) é tratado formalmente durante o estágio de **análise sintática**:

#### A. Gramática e Representação Sintática
Na gramática da calculadora, `%` é classificado como um **operador unário pós-fixado** de maior precedência que as operações aditivas, mas com semântica dependente do operador binário ancestral imediato na árvore de sintaxe:

```
Expressao    := Termo (( '+' | '-' ) Termo)*
Termo        := Fator (( '*' | '/' ) Fator)*
Fator        := Base ('^' Fator)?
Base         := ('+' | '-')? Primario '%'?
Primario     := Numero | Identificador '(' Argumentos ')' | '(' Expressao ')'
```

#### B. Resolução Semântica na Árvore Sintática (AST Transformation)
Quando o parser encontra um nó com operador percentual pós-fixado `PercentOp(Taxa)`:

1. **Caso Aditivo / Subtrativo (`A + B%` ou `A - B%`):**
   - O nó binário aditivo `BinOp(op='+', esq=A, dir=PercentOp(B))` é transformado estruturalmente em:
     $$\text{BinOp}\left(\text{op}='+', \text{esq}=A, \text{dir}=\text{BinOp}\left(\text{op}='*', \text{esq}=\text{BinOp}\left(\text{op}='/', \text{esq}=B, \text{dir}=100\right), \text{dir}=A\right)\right)$$
   - Essa transformação garante que $A$ seja a **subárvore completa** à esquerda do operador aditivo.
   - **Exemplos Formais Resolvidos:**
     - `(125 + 75) * 2 + 10%`: A subárvore esquerda de `+` é `((125 + 75) * 2)`. O termo direito torna-se $(10/100) \times ((125 + 75) * 2)$. Avaliação exata: $400 + 40 = 440.0$.
     - `100 * 2 + 10%`: Base do `+` é `(100 * 2) = 200`. Resultado: $200 + 20 = 220.0$.
     - `100 + 2 * 10%`: Aqui o operador ligado a `10%` é `*`, não `+` (devido à precedência de `*`). Transforma-se em `100 + (2 * (10 / 100)) = 100 + 0.2 = 100.2`.
     - `(A + B%) * C`: O parêntese isola o percentual aditivo internamente. Avalia $(A + (B/100 \times A)) \times C$.

2. **Caso Multiplicativo / Divisivo (`A * B%` ou `A / B%`):**
   - O nó `PercentOp(B)` transforma-se simplesmente em `BinOp(op='/', esq=B, dir=100)`.
   - `200 * 10%` $\rightarrow$ $200 \times (10 / 100) = 20.0$.
   - `200 / 10%` $\rightarrow$ $200 / (10 / 100) = 2000.0$.

3. **Caso Isolado ou Primeiro Termo:**
   - Se `PercentOp(B)` não for filho direto de operador binário aditivo (ex.: `10%`, `(10%)`, `10% + 20`):
     - `10%` $\rightarrow$ $10 / 100 = 0.10$.
     - `10% + 20`: O primeiro termo é isolado ($0.10$), e soma-se $20 \rightarrow 20.10$.

4. **Encadeamentos Sucessivos (`A + B% + C%`):**
   - Respeitando a associatividade à esquerda das operações aditivas:
     - $((A + B\%) + C\%)$: A primeira operação gera uma subárvore $R_1 = A + (B/100 \times A)$. O segundo percentual tem como base todo o nó $R_1$: $R_1 + (C/100 \times R_1)$.
     - Exemplo: `100 + 10% + 10%` $\rightarrow$ $(100 + 10) = 110 \rightarrow 110 + (10/100 \times 110) = 110 + 11 = 121.0$.

---

### 4.2. Raiz de Índice n: Especificação Numérica Rigorosa

A função `raiz_n(radicando, indice)` em `calculadora/operacoes.py` implementa suporte estrito aos números reais:

```python
def raiz_n(radicando: float, indice: float) -> float:
    # 1. Validação de Finitude
    if not (math.isfinite(radicando) and math.isfinite(indice)):
        raise ErroValidacao("Radicando e índice devem ser números reais finitos.")

    # 2. Índice Zero
    if indice == 0.0:
        raise OperacaoInvalidaError("O índice da raiz não pode ser zero.")

    # 3. Radicando Zero
    if radicando == 0.0:
        if indice < 0.0:
            raise DivisaoPorZeroError("Raiz de zero com índice negativo implica divisão por zero.")
        return 0.0

    # 4. Índice Negativo: converte para 1 / raiz_n(radicando, |indice|)
    if indice < 0.0:
        resultado_positivo = raiz_n(radicando, abs(indice))
        if resultado_positivo == 0.0:
            raise DivisaoPorZeroError("Divisão por zero ao inverter raiz de índice negativo.")
        return 1.0 / resultado_positivo

    # 5. Verificação de Integralidade do Índice (compatível com int e float)
    indice_e_inteiro = (isinstance(indice, int) or float(indice).is_integer())

    # 6. Radicando Negativo
    if radicando < 0.0:
        if indice_e_inteiro and (int(indice) % 2 != 0):
            # Índice inteiro ímpar: resultado real negativo
            return -(abs(radicando) ** (1.0 / indice))
        else:
            # Índice par ou não inteiro com radicando negativo: não pertence aos Reais
            raise RadicandoNegativoError(
                f"Raiz de radicando negativo ({radicando}) com índice {indice} não possui resultado real."
            )

    # 7. Radicando Positivo (índice inteiro ou fracionário)
    return radicando ** (1.0 / indice)
```

---

### 4.3. Limite de Literais sem Efeitos Colaterais Globais

Para neutralizar riscos de negação de serviço (DoS) por strings com centenas de milhares de dígitos, **não** utilizaremos `sys.set_int_max_str_digits()`, evitando mutação global que afetaria o interpretador compartilhado do Pyodide ou outros processos.

**Abordagem Adotada:**
A restrição de tamanho de literais é aplicada **diretamente no estágio de tokenização léxica** em `calculadora/expressoes.py`:
- Durante a varredura da expressão, qualquer sequência contínua de caracteres numéricos (antes ou depois da vírgula/ponto decimal) é inspecionada.
- Se um bloco de dígitos contíguos exceder **30 caracteres**, o tokenizer interrompe imediatamente a análise antes de tentar instanciar o número:
  ```python
  if len(token_digitos) > 30:
      raise ErroValidacao(
          f"O literal numérico informado excede o limite máximo permitido de 30 dígitos."
      )
  ```
- Essa barreira protege o parser AST contra parsing quadrático de números gigantescos com custo de verificação $O(n)$ linear e sem tocar no runtime global do sistema.

---

### 4.4. Segurança Numérica Abrangente em Resultados Intermediários e Finais

Todas as operações primitivas (`operacoes.py`) e nós avaliados recursivamente (`expressoes.py`) passam por uma rotina centralizada de sanitização numérica: `_assegurar_numero_valido(valor: float) -> float`:

```python
def _assegurar_numero_valido(valor: Any) -> float:
    # 1. Rejeição de tipos complexos
    if isinstance(valor, complex):
        raise RadicandoNegativoError("A operação resultou em um número complexo, não suportado pela calculadora.")

    # 2. Conversão segura para float
    try:
        val_float = float(valor)
    except (ValueError, TypeError):
        raise ErroAritmetico("Falha na representação numérica do resultado intermediário.")

    # 3. Barreira contra Infinito e NaN
    if math.isnan(val_float) or math.isinf(val_float):
        raise ErroAritmetico("A operação resultou em um valor indefinido (NaN) ou infinito (Overflow).")

    return val_float
```

**Aplicação em cada nó da AST:**
- Em `BinOp` (adição, subtração, multiplicação, divisão, potência):
  - Blocos `try/except OverflowError` capturam estouro de ponto flutuante IEEE 754 imediatamente e levantam `ErroAritmetico`.
  - O resultado produzido é submetido a `_assegurar_numero_valido()`.
- Em `UnaryOp` (sinais `+` e `-`): validação contra `inf`/`nan`.
- Em chamadas de funções (`sqrt`, `root`, `abs`, `inv`):
  - `sqrt(x)`: valida $x \ge 0$.
  - `inv(x)`: valida $x \neq 0$.
  - `root(rad, ind)`: valida finitude, índice não nulo e domínio real.

---

### 4.5. Gestão de Estado: Recuperação Explícita de Histórico e ANS no Motor Python

Para garantir integridade de dados e evitar divergências entre interfaces:

1. **Método Canônico em `calculadora/historico.py`:**
   ```python
   class HistoricoSessao:
       def __init__(self) -> None:
           self._entradas: list[EntradaHistorico] = []
           self._ans: Optional[float] = None
           self._proximo_id: int = 1

       def registrar(self, expressao: str, expressao_formatada: str, resultado: float) -> EntradaHistorico:
           entrada = EntradaHistorico(
               id=self._proximo_id,
               expressao=expressao,
               expressao_formatada=expressao_formatada,
               resultado=resultado,
               resultado_formatado=formatar_resultado(resultado)
           )
           self._entradas.append(entrada)
           self._ans = resultado
           self._proximo_id += 1
           return entrada

       def recuperar_entrada(self, id_entrada: int) -> EntradaHistorico:
           """
           Localiza a entrada pelo ID, atualiza explicitamente o _ans interno
           para o resultado daquela entrada e a retorna.
           """
           for entrada in self._entradas:
               if entrada.id == id_entrada:
                   self._ans = entrada.resultado
                   return entrada
           raise RegistroNaoEncontradoError(f"Registro de histórico #{id_entrada} não encontrado.")

       def obter_ans(self) -> Optional[float]:
           return self._ans

       def limpar_historico(self) -> None:
           """Esvazia a lista de entradas visíveis. PRESERVA o _ans ativo."""
           self._entradas.clear()

       def resetar_sessao(self) -> None:
           """Redefine o histórico e anula o ANS."""
           self._entradas.clear()
           self._ans = None
   ```

2. **Fluxo de Recuperação no JavaScript e no Tkinter:**
   - O usuário clica no item #3 do histórico visual.
   - O cliente apenas dispara:
     - Web: `pyodide.globals.get('bridge_recuperar_historico')(3)`
     - Desktop: `self.historico.recuperar_entrada(3)`
   - O motor Python atualiza `_ans = resultado_da_entrada_3` e retorna o objeto.
   - O cliente atualiza sua tela:
     - Linha de resultado: exibe o valor recuperado em ciano.
     - Linha secundária de expressão: exibe a expressão original daquela entrada.
     - Próxima tecla de operador (ex.: `+`): utiliza imediatamente o novo ANS recuperado como base (`400+`).

---

### 4.6. Especificação UX e Sintaxe das Funções (Resolução de Ambiguidade de Vírgula)

Para garantir compatibilidade sem atritos com o padrão brasileiro (onde a vírgula `,` é o separador decimal oficial):

#### A. Separador Oficial de Argumentos
- **Definição Técnica:** O **ponto e vírgula (`;`)** é o separador inequívoco de argumentos em funções de múltiplos parâmetros.
- **Exemplo Canônico:**
  - `root(12,5; 3)` $\rightarrow$ raiz cúbica de 12,5.
  - `root(-8; 3)` $\rightarrow$ raiz cúbica de -8.
- **Regra de Normalização:** Durante a tokenização, se o usuário digitar vírgula `,` entre dígitos numéricos, ela é reconhecida como separador decimal. O caractere `;` é reservado com exclusividade para separar os argumentos de funções.

#### B. UX de Inserção nas Interfaces (Web e Tkinter)
1. **Botão `ⁿ√x` (Raiz de Índice n):**
   - Ao clicar no botão `ⁿ√x`:
     - Se o visor já contiver um número ou resultado ativo $V$: insere `root(V; ` e posiciona o cursor para digitação do índice.
     - Se o visor estiver vazio: insere `root(` aguardando o primeiro argumento.
2. **Botões Unários (`√`, `|x|`, `¹/x`, `x²`, `±`):**
   - **`√` (Raiz Quadrada):**
     - Se houver valor $V$ no visor: envolve o valor em `sqrt(V)` ou calcula imediatamente se $V$ for o resultado final.
     - Se visor vazio: insere `√(` ou `sqrt(`.
   - **`|x|` (Valor Absoluto):**
     - Envolve o termo atual em `abs(...)`.
   - **`¹/x` (Inverso):**
     - Transforma o termo atual $V$ em `inv(V)` ou `1/(V)`.
   - **`x²` (Quadrado):**
     - Acrescenta `^2` ao termo atual.
   - **`±` (Troca de Sinal):**
     - Se aplicado a um número em digitação: inverte seu sinal diretamente (`5` $\rightarrow$ `-5`; `-5` $\rightarrow$ `5`).
     - Se aplicado a uma expressão complexa: envolve em `- (...)`.

---

### 4.7. Tabela Formal de Precedência e Associatividade

Para evitar divergências matemáticas, a calculadora adota a seguinte tabela rígida de precedência de operadores:

| Nível | Operador / Construção | Notação | Associatividade | Exemplo / Comportamento Canônico |
|---|---|---|---|---|
| **1 (Maior)** | Parênteses | `(...)` | N/A | Força prioridade absoluta interna. |
| **2** | Funções Nomeadas | `sqrt`, `root`, `abs`, `inv` | Prefixo | `abs(-5) + 2` $\rightarrow$ $5 + 2 = 7$. |
| **3** | Potenciação | `^` | **Direita** | `2^3^2` $\rightarrow$ $2^{(3^2)} = 2^9 = 512$. |
| **4** | Sinais Unários | `+`, `-` | Prefixo | **`-2^2 = -4`** (potenciação tem precedência sobre o sinal unário). Para $(-2)^2$, exige-se `(-2)^2 = 4`. |
| **5** | Multiplicação e Divisão | `*`, `/` | **Esquerda** | `20 / 2 * 5` $\rightarrow$ $(20 / 2) \times 5 = 10 \times 5 = 50$. |
| **6** | Adição e Subtração | `+`, `-` | **Esquerda** | `10 - 3 + 2` $\rightarrow$ $(10 - 3) + 2 = 7 + 2 = 9$. |
| **7 (Menor)** | Percentual Contextual | `%` | Dependente do pai | `100 + 10%` $\rightarrow$ $100 + 10 = 110$. |

---

## 5. Proposta de Identidade Visual

### 5.1. Paleta de Cores Homologada

```
Fundo da Aplicação:   #0D1B2A  (Grafite marinho profundo)
Fundo dos Cards:      #1A2744  (Azul ardósia escuro com borda #1E3A5F)
Visor da Calculadora: #0A1424  (Marinho escuro com moldura sutil em ciano/azul)
Resultado em Foco:    #22D3EE  (Ciano elétrico vibrante)
Expressão Secundária: #94A3B8  (Cinza ardósia claro)
Operadores (+, -, *,/):#2563EB (Azul elétrico intenso)
Ação Executar (=):    #22C55E  (Verde esmeralda / lima vibrante)
Ação Limpar (C, ⌫):   #EF4444  (Vermelho coral vivo)
Funções Avançadas:    #7C3AED  (Violeta / índigo elétrico)
Teclado Numérico:     #2D3F6A  (Ardósia neutro com texto branco #F1F5F9)
Botões Memória:       #1E293B  (Texto cinza esmaecido #64748B - Desabilitados com tooltip "Em breve")
```

### 5.2. Adaptação por Plataforma

- **Web (HTML/CSS):**
  - Implementação via variáveis CSS (`--bg-app`, `--btn-num`, `--accent-cyan`).
  - Alternância manual de tema via botão 🌙 / ☀️ no topo direito.
  - O tema selecionado é salvo em `localStorage.getItem("theme_calculadora")`.
  - Tema Light alternativo mapeia as mesmas intenções semânticas para alto contraste em fundo `#F8FAFC`.
- **Desktop (Python + Tkinter):**
  - Tema Dark Premium fixo (sem toggle nesta versão).
  - Janela padronizada em 720×560px com `ttk.Style` e frames estilizados com `relief=tk.FLAT`.
  - Botões desenhados com contraste rigoroso e padding confortável para mouse e toque.

---

## 6. Estratégia de Versionamento

1. **Preservação da Tag Existente:**
   - A tag `v2.0.0` marca a baseline histórica (calculadora de dois operandos) e **não será alterada nem sobrescrita**.
2. **Marcos Internos de Desenvolvimento (Milestones):**
   - As Fases 1 a 4 constituem marcos internos de desenvolvimento demarcados por commits semânticos rastreáveis (ex.: `feat(engine): implementar avaliador ast recursivo`).
   - Não serão geradas tags Git prematuras para fases parciais.
3. **Tag de Release Oficial da Evolução:**
   - A versão evoluída completa será selada sob a tag:
     $$\mathbf{v2.1.0}$$
   - Patches corretivos futuros adotarão `v2.1.1`, `v2.1.2`. Evoluções estruturais (ex.: ativação de botões de memória) receberão `v2.2.0`.

---

## 7. Plano de Implementação em Cinco Fases

### Fase 1 — Motor Matemático, Segurança e Avaliador AST

- **Objetivo:** Implementar regras matemáticas puras com guarda em resultados intermediários/finais, limite de literais de 30 dígitos, resolução de raiz de índice $n$, desaçucaramento sintático do `%` e avaliador recursivo estrito sem `eval()`.
- **Arquivos Envolvidos:**
  - `calculadora/operacoes.py` (funções puras: `raiz_n`, `raiz_quadrada`, `potencia`, `valor_absoluto`, `inverso`, `trocar_sinal`).
  - `calculadora/validacao.py` (validador de literais de até 30 dígitos).
  - `calculadora/expressoes.py` (criação: parser, árvore AST estrita, avaliador recursivo, normalização com separador `;`).
  - `calculadora/__init__.py` (exposição da fachada pública).
  - `tests/test_operacoes.py` (novos testes unitários).
  - `tests/test_expressoes.py` (criação da suíte exaustiva do avaliador).
- **Critérios de Aceitação da Fase 1:**
  - [ ] 25 testes legados de `test_operacoes.py`, `test_validacao.py` e `test_integracao.py` continuam passando sem modificação.
  - [ ] `raiz_n(8, 3)` retorna `2.0`.
  - [ ] `raiz_n(-8, 3)` retorna `-2.0` (sem geração de números complexos).
  - [ ] `raiz_n(8, -3)` retorna `0.5` ($1 / 2$).
  - [ ] `raiz_n(-8, -3)` retorna `-0.5` ($1 / -2$).
  - [ ] `raiz_n(-8, 2)` levanta `RadicandoNegativoError`.
  - [ ] `raiz_n(-8, 3.5)` levanta `RadicandoNegativoError` (índice não inteiro com radicando negativo).
  - [ ] `raiz_n(5, 0)` levanta `OperacaoInvalidaError`.
  - [ ] `raiz_n(5, float('inf'))` levanta `ErroValidacao`.
  - [ ] `avaliar_expressao("-2^2")` retorna `-4.0` (precedência canônica).
  - [ ] `avaliar_expressao("(-2)^2")` retorna `4.0`.
  - [ ] `avaliar_expressao("2^3^2")` retorna `512.0` (associatividade à direita).
  - [ ] `avaliar_expressao("(125 + 75) * 2 + 10%")` retorna `440.0`.
  - [ ] `avaliar_expressao("100 + 10% + 10%")` retorna `121.0` (percentuais encadeados sucessivos).
  - [ ] `avaliar_expressao("100 + 2 * 10%")` retorna `100.2` (respeito à precedência multiplicativa no percentual).
  - [ ] `avaliar_expressao("root(-8; 3)")` avalia e retorna `-2.0`.
  - [ ] `avaliar_expressao("root(12,5; 3)")` aceita vírgula decimal brasileira e retorna `2.32079442` formatado.
  - [ ] `avaliar_expressao("√144")` avalia e retorna `12.0`.
  - [ ] Literal com 31 dígitos (ex.: `1234567890123456789012345678901`) dispara `ErroValidacao` sem chamar `sys.set_int_max_str_digits`.
  - [ ] Tentativas de injeção (`__import__`, `open`, `exec`, `eval`) disparam `ExpressaoInvalidaError`.
  - [ ] Funções matemáticas não homologadas (ex.: `sin(1)`, `cos(0)`) disparam `ExpressaoInvalidaError`.
  - [ ] Operação com overflow intermediário ($10^{1000}$) levanta `ErroAritmetico`.

---

### Fase 2 — Módulo de Histórico e Gestão de ANS em Python

- **Objetivo:** Implementar o `HistoricoSessao` com método explícito de recuperação de entrada anterior (`recuperar_entrada`) que define o resultado selecionado como o ANS ativo da sessão.
- **Arquivos Envolvidos:**
  - `calculadora/historico.py` (`EntradaHistorico`, `HistoricoSessao`).
  - `calculadora/__init__.py` (exportação).
  - `tests/test_historico.py` (suíte de testes unitários).
- **Critérios de Aceitação da Fase 2:**
  - [ ] `registrar(...)` gera registros encadeados com ID incremental.
  - [ ] `recuperar_entrada(id)` atualiza o `_ans` interno para o resultado da entrada recuperada e retorna o registro.
  - [ ] `recuperar_entrada(999)` inexistente dispara `RegistroNaoEncontradoError`.
  - [ ] `limpar_historico()` esvazia a lista de entradas visíveis.
  - [ ] **Independência Rigorosa:** Após `limpar_historico()`, `obter_ans()` retorna intacto o valor numérico da última operação, permitindo continuidade imediata.
  - [ ] `resetar_sessao()` redefine tanto o histórico quanto o ANS para `None`.

---

### Fase 3 — Interface Desktop Tkinter (Calculadora 2.0 Dark)

- **Objetivo:** Implementar a interface Tkinter Dark Premium com visor duplo, histórico lateral interativo com recuperação por clique, suporte ao teclado físico e separador de argumentos `;`.
- **Arquivos Envolvidos:**
  - `calculadora/interface.py` (reestruturação completa).
  - `main.py` (entrypoint preservado).
- **Critérios de Aceitação da Fase 3:**
  - [ ] Janela abre em 720×560px com tema Dark `#0D1B2A`.
  - [ ] Visor duplo: linha de expressão em cinza claro e linha de resultado em ciano `#22D3EE`.
  - [ ] Teclado interativo completo com botões coloridos respeitando a paleta homologada.
  - [ ] Botão `ⁿ√x` insere template `root(` para preenchimento com separador `;`.
  - [ ] Clique no item de histórico invoca `recuperar_entrada()` no motor, atualizando o visor e definindo o ANS ativo.
  - [ ] Pressionar tecla de operador aritmético após recuperação continua o cálculo a partir do valor recuperado.
  - [ ] Botão "Limpar Histórico" limpa a coluna lateral sem afetar o ANS do visor.
  - [ ] Botões de memória (`MC`, `MR`, `M+`, `M-`, `MS`) visíveis, desabilitados (`state=DISABLED`) com indicação visual "Em breve".
  - [ ] Suporte a atalhos físicos: dígitos, operadores, parênteses, `Enter` (calcular), `Backspace` (apagar), `Esc` (limpar), `Ctrl+C` (copiar resultado).

---

### Fase 4 — Interface Web (Pyodide, Dark Premium e Responsividade)

- **Objetivo:** Reconstruir a aplicação web Vanilla HTML/CSS/JS, montando os novos módulos Python no MEMFS do Pyodide, implementando a ponte para `recuperar_entrada` e alternância manual de temas (Dark/Light).
- **Arquivos Envolvidos:**
  - `index.html` (estrutura semântica: visor duplo, grid de botões, histórico lateral, toggle de tema).
  - `style.css` (design system Dark Premium + variáveis para tema Light).
  - `app.js` (montagem de `expressoes.py` e `historico.py` no MEMFS, ponte de dados, eventos de teclado).
  - `tests_web.js` (atualização e expansão da suíte de testes de browser).
  - `testes.html` (painel de acompanhamento de validação).
- **Critérios de Aceitação da Fase 4:**
  - [ ] Inicialização assíncrona do Pyodide monta com sucesso todos os arquivos em `/calculadora` no MEMFS.
  - [ ] Layout web fiel ao mockup aprovado em desktop e responsivo para telas menores.
  - [ ] Botão 🌙/☀️ alterna entre tema Dark Premium e Light sem recarregar a página e sem afetar a lógica matemática.
  - [ ] Escolha de tema é preservada em `localStorage.getItem("theme_calculadora")`.
  - [ ] Clique no item do histórico dispara `bridge_recuperar_historico(id)` e atualiza o visor com o ANS ativo.
  - [ ] Botão "Copiar resultado" copia o valor ativo para o clipboard via `navigator.clipboard.writeText` com feedback visual.
  - [ ] Todas as chamadas de ponte liberam proxies via `proxy.destroy()` em bloco `finally`.
  - [ ] Operação no teclado físico emite os mesmos comandos que o teclado na tela.

---

### Fase 5 — Validação Integrada, Regressão e Documentação

- **Objetivo:** Executar a bateria completa de testes de regressão, verificar a integridade da publicação estática no GitHub Pages e documentar a versão final `v2.1.0`.
- **Arquivos Envolvidos:**
  - `tests/test_integracao.py` (fluxos completos fim a fim).
  - `tests_web.js` e `testes.html` (bateria de validação no navegador).
  - `README.md` e `CHANGELOG.md` (documentação da versão).
  - `docs/implementation_plan.md` (arquivamento do plano executado).
- **Critérios de Aceitação da Fase 5:**
  - [ ] 100% de aprovação na suíte de testes Python (`python3 -m unittest discover tests`), cobrindo no mínimo 60 cenários.
  - [ ] 100% de aprovação na suíte de browser em `testes.html`, cobrindo no mínimo 25 cenários automatizados.
  - [ ] Zero regressão nas funcionalidades e testes da baseline histórica.
  - [ ] Execução local via `app.py` em conformidade antes da publicação.
  - [ ] `README.md` atualizado com documentação completa da sintaxe (`root(rad; ind)`, `%`, atalhos de teclado).
  - [ ] `CHANGELOG.md` registra formalmente todas as adições sob a nova versão `v2.1.0`.

---

## 8. Resumo Comparativo Final

| Dimensão | Baseline Existente | Calculadora 2.0 (Revisão 4) |
|---|---|---|
| **Versão Git** | `v2.0.0` (preservada) | `v2.1.0` (nova release ao final) |
| **Entrada Matemática** | Dois campos isolados | Expressões completas com parênteses e funções |
| **Avaliador** | Dispatch simples | AST recursivo estrito sem `eval()` |
| **Porcentagem** | Não suportada | Contextual e encadeada via reescrita formal de AST |
| **Raiz n-ésima** | Não suportada | `root(rad; ind)` suportando negativos com índice ímpar |
| **Separador de Argumentos** | Não aplicável | Ponto e vírgula (`;`), convivendo com vírgula decimal |
| **Histórico e ANS** | Ausentes | Centralizados no motor Python com `recuperar_entrada` |
| **Limite DoS Literais** | Sem limite | Máximo de 30 dígitos inspecionados no tokenizer |
| **Memória** | Ausente | Fora de escopo desta versão (botões "Em breve") |
| **Design** | Formulário claro clássico | Dark Premium homologado com toggle Light na web |

> [!IMPORTANT]
> **Próxima Ação:** O plano está completamente alinhado, rigoroso e fechado. Aguardo sua avaliação final e **autorização expressa** para iniciar o desenvolvimento da **Fase 1**.
