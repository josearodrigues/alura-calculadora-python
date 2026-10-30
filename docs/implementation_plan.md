# Integração do Pyodide (Python via WebAssembly) na Calculadora Web

Transição da aplicação para a web utilizando **Pyodide (CPython compilado para WebAssembly)**, executando os módulos originais `operacoes.py` e `validacao.py` diretamente no navegador do usuário, com interface moderna e painel de depuração do runtime WebAssembly.

---

## Decisões Confirmadas com o Usuário

> [!IMPORTANT]
> Decisões alinhadas na Fase 1:
> - **Papel do Pyodide:** Executar os arquivos Python reais no navegador via WebAssembly, comprovando o desacoplamento arquitetural.
> - **Estilo da Interface:** Interface visual moderna com botões intuitivos e painel de depuração em tempo real mostrando as chamadas e o estado do runtime Pyodide.
> - **Escopo de Execução:** Foco na execução interativa dos cálculos, mantendo a suíte de testes `unittest` executável no ambiente de desenvolvimento/terminal local para manter o carregamento web ágil e veloz.

---

## 1. Visão Geral e Conceito Central

### O que a aplicação faz
A aplicação carrega o runtime oficial do **Pyodide (v0.26+)** no navegador. Ao inicializar, o Pyodide monta em seu sistema de arquivos virtual em memória (`MEMFS`) o código exato de `operacoes.py` e `validacao.py` que construímos nas etapas anteriores. 

Quando o usuário interage com os botões e campos na web:
1. O React coleta os valores brutos.
2. Invoca o interpretador Python real no navegador através do bridge `pyodide.runPython()`.
3. O Python executa a validação, o cálculo e a formatação nativa.
4. O resultado e os logs de execução do interpretador são exibidos em tempo real na tela.

### Valor Pedagógico e de Engenharia
- **Prova Prática do Desacoplamento:** Demonstra na prática que as camadas de regra de negócio (`operacoes.py`) e validação (`validacao.py`) não precisaram sofrer **nenhuma alteração** para sair do desktop (Tkinter) e rodar na Web (Pyodide).
- **Zero Servidor Backend:** A execução do Python ocorre 100% no cliente (máquina do usuário), sem necessidade de contêineres, servidores Flask/Django ou custos de infraestrutura de nuvem.

---

## 2. Experiência do Usuário e Design Visual

A interface adotará o layout **Two-Zone Sandbox (Laboratório Educacional)**:

### Zona Esquerda (Calculadora Web Nativa)
- **Status do Runtime WebAssembly:** Indicador de status do motor Pyodide (Inicializando runtime Wasm $\to$ Carregando módulos Python $\to$ Pronto para calcular).
- **Campos de Entrada:** Inputs elegantes para Operando A e Operando B com suporte total a números decimais com vírgula ou ponto.
- **Grade de Operações:** Seletores interativos para Adição ($+$), Subtração ($-$), Multiplicação ($\times$) e Divisão ($\div$).
- **Ações:** Botão primário "Calcular" e botão neutro "Limpar".
- **Painel de Resposta:** Exibição do resultado formatado em destaque (verde esmeralda) ou avisos semânticos de validação/aritmética em vermelho suave.

### Zona Direita (Console de Depuração e Inspeção do Pyodide)
- **Terminal de Logs do WebAssembly:** Exibe a transcrição em tempo real do código Python executado a cada cálculo (ex.: `validacao.converter_operando('12,5') -> 12.5`).
- **Inspetor de Módulos em Memória:** Visualização dos arquivos `calculadora/operacoes.py` e `calculadora/validacao.py` carregados no sistema de arquivos virtual do Pyodide.
- **Métricas do Runtime:** Tempo de execução do cálculo em milissegundos dentro do WebAssembly.

---

## 3. Decisões Técnicas e Trade-Offs

### Decisão 1: Carregamento do Pyodide via CDN oficial
- **Abordagem Escolhida:** Carregar o script do Pyodide (`https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js`) dinamicamente sob demanda, com tela de carregamento visual e barra de progresso.
- **Por que:** Evita inchar o bundle do Vite com mais de 30MB de binários WebAssembly pré-empacotados, aproveitando cache de CDN e inicialização assíncrona limpa.
- **Alternativa Descartada:** Empacotar o Pyodide via npm (adicionaria dependências complexas de Webpack/Rollup WASM polyfills desnecessárias).

### Decisão 2: Ponte de Execução Isolada (Python Bridge)
- **Abordagem Escolhida:** Criar uma função controladora em Python registrada no runtime que recebe os parâmetros brutos do React, executa `validacao.converter_operando` e `operacoes.calcular`, capturando as exceções de domínio (`ErroValidacao`, `DivisaoPorZeroError`) e retornando um dicionário serializado para o JavaScript.
- **Por que:** Garante que o tratamento de exceções de domínio permaneça estritamente regido pelo Python, entregando ao React uma resposta segura e determinística.

---

## 4. Arquitetura Técnica e Fluxo de Dados

```
┌───────────────────────────────────────────────────────────────┐
│                     NAVEGADOR WEB (CLIENTE)                   │
│                                                               │
│  ┌─────────────────────────┐     ┌─────────────────────────┐  │
│  │   Interface React (UI)  │     │ Console de Depuração    │  │
│  │   • Inputs A e B        │     │ • Logs do interpretador │  │
│  │   • Seleção de operador │     │ • Métricas de tempo     │  │
│  └────────────┬────────────┘     └────────────▲────────────┘  │
│               │                               │               │
│               │ Chamada via JS Bridge         │ Telemetria    │
│               ▼                               │               │
│  ┌────────────────────────────────────────────┴────────────┐  │
│  │             RUNTIME PYODIDE (WebAssembly CPython)       │  │
│  │                                                         │  │
│  │   Virtual File System:                                  │  │
│  │   ├── /calculadora/operacoes.py (Código Original)       │  │
│  │   └── /calculadora/validacao.py (Código Original)       │  │
│  │                                                         │  │
│  │   Execução:                                             │  │
│  │   converter_operando() ──► calcular() ──► formatar()    │  │
│  └─────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘
```

### Mapeamento dos Arquivos
- **`calculadora/operacoes.py`:** Mantido **intacto**, importado pelo Pyodide.
- **`calculadora/validacao.py`:** Mantido **intacto**, importado pelo Pyodide.
- **`src/pyodide/runner.ts`:** Módulo TypeScript responsável por carregar o script do Pyodide, injetar os arquivos Python no MEMFS e expor a função assíncrona `executarCalculoPython(a, b, op)`.
- **`src/App.tsx`:** Interface visual React com visualização em duas zonas (Calculadora + Console de Depuração).
