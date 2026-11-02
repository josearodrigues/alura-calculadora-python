# Adendo Técnico à Revisão 4 — Calculadora 2.1 (Consolidado)

> [!IMPORTANT]
> Este documento registra o **adendo técnico complementar à Revisão 4** do plano. As seções 1 a 8 preservam as decisões e especificações concebidas antes da implementação; afirmações de estado nelas contidas devem ser lidas como registros daquele momento. A evolução posterior efetivamente implementada está documentada na seção 9 e o estado consolidado atual em `docs/ESTADO-ATUAL.md`.

---

## 1. Gramática Formal e Precedência: Correção de Sinal Unário, Potenciação e Percentual

### 1.1. Correção Estrutural da Gramática (Seção 4.1.A da Revisão 4)
Na Revisão 4, a regra `Base := ('+' | '-')? Primario '%'?` posicionava o sinal unário abaixo da potenciação na árvore, o que induziria a avaliação de `-2^2` como `(-2)^2 = 4`.

Para assegurar que **a potenciação tenha precedência estrita sobre o sinal unário**, que a **potenciação seja associativa à direita** e que o **percentual seja reconhecido como operador pós-fixado**, a gramática é formalizada na seguinte hierarquia clássica:

```ebnf
Expressao           := TermoAditivo
TermoAditivo        := TermoMultiplicativo ( ( '+' | '-' ) TermoMultiplicativo )*
TermoMultiplicativo := FatorUnario ( ( '*' | '/' ) FatorUnario )*
FatorUnario         := ( '+' | '-' ) FatorUnario 
                     | FatorPotencia
FatorPotencia       := FatorPosfixado ( '^' FatorUnario )?
FatorPosfixado      := Primario '%'?
Primario            := Numero 
                     | Identificador '(' ListaArgumentos ')' 
                     | '(' Expressao ')'
ListaArgumentos     := Expressao ( ';' Expressao )*
```

#### Efeitos Formais da Nova Gramática:
1. **Precedência de `-2^2 = -4`:** 
   - A entrada `-2^2` é derivada como `FatorUnario('-', FatorPotencia(Primario(2), '^', FatorPotencia(Primario(2))))`.
   - O nó de potenciação `2^2` é avaliado primeiro ($\rightarrow 4$), e o unário `-` é aplicado ao resultado final ($\rightarrow -4$).
2. **Associatividade de `(-2)^2 = 4`:** 
   - Os parênteses fecham a derivação no nível `Primario`, contendo o `FatorUnario` internamente. Avalia $(-2)^2 = 4$.
3. **Associatividade à Direita de `2^3^2 = 512`:**
   - A recursão em `FatorPotencia := FatorPosfixado ('^' FatorUnario)?` garante que `2^(3^2) = 2^9 = 512`.
4. **Percentual como Operador Pós-fixado:**
   - `FatorPosfixado` captura `Primario '%'?`. O `%` liga-se sintaticamente de forma imediata ao seu operando primário.

---

### 1.2. Alinhamento da Tabela de Precedência (Seção 4.7 da Revisão 4)
A tabela da Seção 4.7 é corrigida para refletir a gramática acima, eliminando contradições:

| Nível | Operador / Construção | Notação | Posição / Sintaxe | Associatividade | Comportamento Canônico |
|---|---|---|---|---|---|
| **1 (Maior)** | Parênteses e Chamadas | `(...)`, `fn(...)` | Primário | N/A | Prioridade absoluta. |
| **2** | Percentual Sintático | `%` | **Pós-fixado** | N/A | Liga-se ao `Primario` antecedente imediato. |
| **3** | Potenciação | `^` | Binário infixo | **Direita** | `2^3^2 = 2^(3^2) = 512`. |
| **4** | Sinais Unários | `+`, `-` | Prefixo | Direita | **`-2^2 = -4`**; `-(2^2) = -4`; `(-2)^2 = 4`. |
| **5** | Multiplicação e Divisão | `*`, `/` | Binário infixo | **Esquerda** | `20 / 2 * 5 = (20 / 2) * 5 = 50`. |
| **6 (Menor)**| Adição e Subtração | `+`, `-` | Binário infixo | **Esquerda** | `10 - 3 + 2 = (10 - 3) + 2 = 9`. |

---

## 2. Percentual Contextual e Agrupamentos na AST (Seção 4.1 da Revisão 4)

### 2.1. Reconhecimento Sintático vs. Resolução Semântica na AST
- **No Parser (Sintaxe):** O `%` é estritamente um operador pós-fixado ligado ao seu operando primário, gerando o nó sintático `PercentOp(valor)`.
- **No Avaliador (Semântica Contextual na AST):** A semântica contextual (percentual de base vs. percentual fracionário) é resolvida durante a descida recursiva da AST:
  - Ao avaliar um nó aditivo `BinOp('+', esq, dir)` ou `BinOp('-', esq, dir)`: se `dir` for um `PercentOp`, a base do cálculo percentual é a subárvore completa `esq`.
  - Ao avaliar um nó multiplicativo `BinOp('*', esq, dir)` ou `BinOp('/', esq, dir)`: o `PercentOp` atua apenas convertendo o valor em fração decimal (`valor / 100`).
  - Em qualquer outro contexto (termo inicial ou isolado): atua como fração decimal absoluta (`valor / 100`).

### 2.2. Preservação de Agrupamentos via Nó Sintático Próprio
Para distinguir formalmente `100 + 10%` de `100 + (10%)`, **o parser introduz explicitamente o nó sintático `Agrupamento(expressao)`** ao reduzir a regra `Primario := '(' Expressao ')'`:

1. **Caso `100 + 10%`:**
   - AST: `BinOp('+', Numero(100), PercentOp(Numero(10)))`.
   - O ancestral imediato de `PercentOp` é o `BinOp('+')`.
   - Avaliação: base $100 \rightarrow 100 + (10\% \times 100) = \mathbf{110.0}$.
2. **Caso `100 + (10%)`:**
   - AST: `BinOp('+', Numero(100), Agrupamento(PercentOp(Numero(10))))`.
   - O ancestral imediato de `PercentOp` é o nó `Agrupamento`, que encapsula e isola o escopo sintático interno.
   - Avaliação: o termo isolado resolve para $10 / 100 = 0.10$, e o `BinOp('+')` soma o valor absoluto $\rightarrow 100 + 0.10 = \mathbf{100.10}$.
3. **Caso `100 + (5 + 5)%`:**
   - AST: `BinOp('+', Numero(100), PercentOp(Agrupamento(BinOp('+', 5, 5))))`.
   - O `%` pós-fixado tem como taxa o bloco agrupado $(5 + 5) = 10\%$.
   - O ancestral do `PercentOp` é o `BinOp('+')` cuja base aditiva à esquerda é **`100`** (e não o termo interno $5+5$).
   - Avaliação: $100 + (10\% \times 100) = 100 + 10 = \mathbf{110.0}$.

---

## 3. Estratégia Centralizada de Exceções e Segurança Numérica (Seção 4.4 da Revisão 4)

Para eliminar duplicações de blocos `try/except` espalhados pelas funções matemáticas, todas as operações convergem em uma rotina centralizada de despacho e sanitização:

```python
def executar_operacao_segura(operacao_fn, *args):
    """Executa a operação matemática capturando exceções internas e padronizando-as."""
    try:
        resultado = operacao_fn(*args)
    except OverflowError:
        raise ErroAritmetico("Resultado excedeu a capacidade de representação numérica (Overflow).")
    except ZeroDivisionError:
        raise DivisaoPorZeroError("Não é possível realizar divisão por zero.")
    except (ValueError, TypeError) as e:
        raise ErroAritmetico(f"Operação matemática inválida: {str(e)}")

    return _assegurar_numero_valido(resultado)

def _assegurar_numero_valido(valor: Any) -> float:
    """Valida tipos complexos, conversão para float e barreiras contra Inf e NaN."""
    if isinstance(valor, complex):
        raise RadicandoNegativoError("Resultado complexo não é suportado no domínio dos números reais.")
    try:
        val_float = float(valor)
    except (ValueError, TypeError):
        raise ErroAritmetico("Valor não conversível para ponto flutuante real.")
    if math.isnan(val_float) or math.isinf(val_float):
        raise ErroAritmetico("Operação resultou em valor infinito ou indefinido (Overflow/NaN).")
    return val_float
```

### Exceções de Domínio Padronizadas para a Interface:
- `ErroAritmetico`: Overflow, valores indefinidos ou infinitos.
- `RadicandoNegativoError`: Resultados fora do domínio dos Reais.
- `DivisaoPorZeroError`: Divisões ou inversões de zero.
- `ErroValidacao`: Violações de tamanho léxico e limites.
- `ExpressaoInvalidaError`: Sintaxe malformada ou nós não permitidos.

---

## 4. Limite de Literais, Expoente Científico e Precisão Float (Seção 4.3 da Revisão 4)

### 4.1. Regras de Limite no Tokenizer Léxico
1. **Contagem dos 30 Dígitos:** A soma dos algarismos da parte inteira e decimal é limitada a no máximo **30 dígitos numéricos**. Sinais (`+`, `-`) e separadores decimais (`,`, `.`) não entram nessa contagem.
2. **Magnitude do Expoente (Política de Projeto):** O limite $|expoente| \le 308$ é documentado como **política de segurança do projeto Calculadora 2.1** para evitar entradas com magnitudes que excedem a capacidade de representação de ponto flutuante de precisão dupla de 64 bits. Tamanho textual do expoente limitado a 4 caracteres (ex.: `e+308`).
3. **Detecção de Overflow na Conversão de Literais:** Se a conversão léxica via `float(literal_str)` disparar `OverflowError` ou produzir `math.isinf()`, o tokenizer interrompe o processamento imediatamente com:
   `ErroValidacao(f"O literal numérico '{literal_str}' excede a capacidade de representação (gera Infinito).")`

### 4.2. Registro Formal de Precisão Numérica
Fica expressamente documentado que o limite de 30 dígitos atua como uma barreira de segurança de entrada (**I/O Security Guard**), mas que a representação e os cálculos matemáticos internos ocorrem em ponto flutuante de 64 bits (`float` do Python / padrão IEEE 754), cuja **precisão real é de aproximadamente 15 a 17 dígitos decimais significativos**.

---

## 5. Formalização Rigorosa da Raiz $n$ (Seção 4.2 da Revisão 4)

A função `raiz_n(radicando, indice)` implementa a seguinte regra formal no domínio dos números reais:

1. **Radicando Positivo ($radicando > 0$):**
   - Válido para qualquer índice real finito não nulo ($indice \in \mathbb{R}^*$), incluindo **índices inteiros e índices fracionários / não inteiros**.
   - Exemplo: `raiz_n(8, 0.5)` $\rightarrow 8^{1 / 0.5} = 8^2 = \mathbf{64.0}$.
2. **Radicando Negativo ($radicando < 0$):**
   - **Somente índices inteiros ímpares** ($indice \in \mathbb{Z}$ tal que $|indice| \pmod 2 = 1$) são admitidos.
   - Qualquer índice não inteiro ou fracionário com radicando negativo (ex.: `raiz_n(-8, 3.5)` ou `raiz_n(-8, 0.5)`) é sumariamente rejeitado com `RadicandoNegativoError("Raiz de número negativo não possui resultado real para índices não inteiros ou pares.")`.
3. **Índice Negativo:**
   - Inverte o resultado: `raiz_n(rad, -ind) = 1.0 / raiz_n(rad, ind)`.
   - Exemplo: `raiz_n(8, -3) = 0.5` ($1/2$); `raiz_n(-8, -3) = -0.5` ($1/-2$).
4. **Índice Zero ou Não Finito:**
   - Índice zero $\rightarrow$ `OperacaoInvalidaError`.
   - Índice `inf` ou `nan` $\rightarrow$ `ErroValidacao`.

---

## 6. Normalização e Escopo Delimitado da Raiz Quadrada (Seção 4.1 da Revisão 4)

- **Com parênteses:** `√(9 + 16)` e `sqrt(9 + 16)` $\rightarrow$ atuam sobre todo o bloco delimitado por parênteses ($9 + 16 = 25 \rightarrow \mathbf{5.0}$).
- **Sem parênteses:** `√9 + 16` e `sqrt(9) + 16` $\rightarrow$ o escopo sem parênteses captura apenas o literal contínuo imediato ($\sqrt{9} + 16 = 3 + 16 = \mathbf{19.0}$).

---

## 7. Matriz Consolidada de Testes Adicionais (Fase 1)

### 7.1. Precedência e Sinais Unários (`test_expressoes.py`)
- `avaliar_expressao("-2^2")` $\rightarrow$ `-4.0` (mandatório).
- `avaliar_expressao("(-2)^2")` $\rightarrow$ `4.0` (mandatório).
- `avaliar_expressao("2^3^2")` $\rightarrow$ `512.0` (associatividade à direita: $2^{(3^2)}$).
- `avaliar_expressao("-2^3^2")` $\rightarrow$ `-512.0`.
- `avaliar_expressao("2^-2")` $\rightarrow$ `0.25`.

### 7.2. Agrupamentos e Percentuais Contextuais (`test_expressoes.py`)
- `avaliar_expressao("400 + 10%")` $\rightarrow$ `440.0`.
- `avaliar_expressao("400 - 10%")` $\rightarrow$ `360.0`.
- `avaliar_expressao("200 * 10%")` $\rightarrow$ `20.0`.
- `avaliar_expressao("200 / 10%")` $\rightarrow$ `2000.0`.
- `avaliar_expressao("100 + 10% + 10%")` $\rightarrow$ `121.0`.
- `avaliar_expressao("100 + (10%)")` $\rightarrow$ `100.1` (isolamento por agrupamento).
- `avaliar_expressao("100 + (5 + 5)%")` $\rightarrow$ `110.0` (taxa agrupada sobre base aditiva externa 100).

### 7.3. Raízes Fracionárias, Negativas e Casos de Borda (`test_operacoes.py`)
- `raiz_n(8, -3)` $\rightarrow$ `0.5`.
- `raiz_n(-8, -3)` $\rightarrow$ `-0.5`.
- `raiz_n(8, 0.5)` $\rightarrow$ `64.0` (índice fracionário real positivo).
- `raiz_n(16, 0.25)` $\rightarrow$ `65536.0` ($16^4$).
- `raiz_n(-8, 3.5)` $\rightarrow$ dispara `RadicandoNegativoError` (índice fracionário com radicando negativo).
- `raiz_n(0, -3)` $\rightarrow$ dispara `DivisaoPorZeroError`.
- `raiz_n(5, 0)` $\rightarrow$ dispara `OperacaoInvalidaError`.

### 7.4. Escopo da Raiz Quadrada e Literais Extremos (`test_expressoes.py` e `test_validacao.py`)
- `avaliar_expressao("sqrt(9 + 16)")` $\rightarrow$ `5.0`.
- `avaliar_expressao("sqrt(9) + 16")` $\rightarrow$ `19.0`.
- Literal com 30 dígitos numéricos $\rightarrow$ aceito na validação.
- Literal com 31 dígitos numéricos $\rightarrow$ dispara `ErroValidacao`.
- `avaliar_expressao("1e309")` $\rightarrow$ dispara `ErroValidacao` (overflow detectado na conversão do literal).

---

## 8. Registro do estado de planejamento original

> **Registro histórico:** os itens desta seção descrevem o estado do projeto quando o adendo foi consolidado, antes da implementação. Não representam o estado atual nem prevalecem sobre as decisões posteriores registradas na seção 9.

As decisões técnicas aqui especificadas serviram como referência para a implementação. Algumas escolhas foram posteriormente adaptadas, como a memória funcional na interface desktop, conforme decisão do usuário e registro de divergências. A baseline `v2.0.0` foi preservada.

---

## 9. Atualização posterior — Evolução para a versão 2.1.0

Esta seção registra a evolução realizada após o estado documentado na seção 8, preservando o histórico das decisões anteriores.

### 9.1. Funcionalidades matemáticas e operacionais implementadas

- Ampliação do motor matemático com:
  - Potenciação (`potencia` / `^`).
  - Raiz quadrada (`raiz_quadrada` / `sqrt`).
  - Raiz de índice qualquer (`raiz_n` / `root`).
  - Valor absoluto (`valor_absoluto` / `abs`).
  - Inverso (`inverso` / `inv`).
  - Troca de sinal por operadores unários.

- Evolução do avaliador de expressões:
  - Suporte a expressões combinadas e parênteses.
  - Percentual contextual (`%`).
  - Continuidade do resultado anterior (`ANS`).
  - Parser próprio para avaliação controlada das expressões.

- Implementação do histórico de operações.

- Implementação das operações de memória na interface Tkinter:
  - MC — limpar memória.
  - MR — recuperar memória.
  - M+ — somar resultado à memória.
  - M- — subtrair resultado da memória.
  - MS — armazenar resultado na memória.

### 9.2. Validação automatizada

- Suíte completa executada com `python3 -m unittest discover -s tests -v`.
- Resultado: 87 testes aprovados.
- Testes específicos da interface desktop: 16 testes aprovados.
- Verificação de integridade do diff com `git diff --check`, sem erros.

### 9.3. Estado da versão no registro intermediário

> **Registro histórico:** este era o estado documentado antes da conclusão das fases seguintes. A situação atual está consolidada em `docs/ESTADO-ATUAL.md`.

- A versão `v2.0.0` permanece preservada como baseline histórica.
- A versão `v2.1.0` foi implementada posteriormente, integrada à `main` e validada no GitHub Pages.
- A tag e a release formal `v2.1.0` permanecem pendentes.

---

## 10. Situação consolidada após a implementação — 01/11/2026

As decisões técnicas deste adendo foram utilizadas como referência para a evolução `v2.1.0`, com adaptações registradas separadamente. As cinco fases foram concluídas no escopo acordado; a aplicação está integrada à `main` e as rotas públicas da baseline e da evolução foram verificadas pelo usuário.

A suíte Python foi aprovada em 92/92 testes. A suíte Web foi retestada após a última melhoria visual e aprovada em 31/31 cenários, com duração aproximada de 1 minuto, conforme confirmação do usuário. A baseline `v2.0.0` permanece preservada. A tag e a release formal `v2.1.0` ainda não foram criadas.
