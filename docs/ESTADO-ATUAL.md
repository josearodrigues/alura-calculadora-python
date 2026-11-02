# Estado Atual — Desafio 2: Calculadora Python

**Última atualização:** 01/11/2026  
**Repositório:** `josearodrigues/alura-calculadora-python`  
**Branch de trabalho:** `desafio-2-revisao-final`  
**Branch principal:** `main`  
**Plano de referência:** [calculadora-2.0-plano.md](calculadora-2.0-plano.md)  
**Registro de decisões:** [REGISTRO-DIVERGENCIAS.md](REGISTRO-DIVERGENCIAS.md)

> Este documento é a referência operacional de continuidade. Registra o estado confirmado, as validações conhecidas e as pendências reais. O plano original e os registros históricos continuam sendo as fontes de requisitos e decisões.

## 1. Identificação e objetivo

Desafio 2 da Imersão Engenharia de Software: Dev na Era da IA, iniciativa da Alura Imersões em parceria com Google for Startups.

Objetivo pedagógico: compreender um código existente, implementar melhorias e verificar se o funcionamento anterior foi preservado.

Princípio de trabalho: **Compreender, implementar, validar e explicar.**

A evolução da calculadora foi organizada em cinco fases, conforme o plano original. As fases de implementação estão concluídas no escopo acordado. A integração na branch principal e a publicação da evolução ainda não foram realizadas.

## 2. Estado do Git e versionamento

| Item | Estado confirmado |
|---|---|
| Repositório | `josearodrigues/alura-calculadora-python` |
| Branch de trabalho | `desafio-2-revisao-final` |
| Branch principal | `main` |
| Último commit local informado pelo usuário | `89482b1` — `docs: remover espaço indevido do plano` |
| Sincronização local/remota | Confirmada pelo usuário; `git push` retornou `Everything up-to-date` e `git status -sb` não indicou divergência nem alterações locais |
| Comparação com `main` consultada no GitHub | 82 commits à frente, 0 atrás |
| Último commit de `main` observado | `cff94f2` |
| Arquivos no diff da branch | 27: 25 adicionados, 2 modificados, nenhum removido |
| PR aberto para a branch | Nenhum encontrado na consulta realizada |
| Última versão publicada conhecida | `v2.0.0` |
| Evolução em desenvolvimento | `v2.1.0`, organizada em `v2.1.0/`; ainda não publicada como release |

A comparação confirma que a branch de trabalho está baseada na versão observada de `main`, sem commits faltantes em relação a ela. A contagem de commits pode mudar e deve ser consultada novamente antes de uma integração futura.

O diff remoto confirma que nenhum arquivo foi removido em relação à `main`. A aplicação existente na raiz permanece presente na branch, enquanto a evolução está organizada no subdiretório `v2.1.0/`. Essa comparação estrutural não substitui a validação funcional das rotas públicas.

## 3. Situação das fases

| Fase | Escopo | Situação |
|---|---|---|
| 1 | Motor matemático, segurança e avaliador AST | Implementada. Funcionalidades cobertas pela suíte Python. |
| 2 | Histórico e gestão de ANS | Implementada. Histórico, recuperação e ANS cobertos pela suíte Python. |
| 3 | Interface desktop Tkinter | Concluída e validada no escopo informado pelo usuário. |
| 4 | Interface Web com Pyodide, tema e responsividade | Implementada; interface e página de testes ajustadas e verificadas localmente pelo usuário. |
| 5 | Validação integrada, regressão e documentação | Concluída no escopo documentado. A publicação e a integração na `main` permanecem pendentes. |

### 3.1 Adaptações aceitas

As diferenças abaixo foram aceitas pelo usuário e estão detalhadas em [REGISTRO-DIVERGENCIAS.md](REGISTRO-DIVERGENCIAS.md):

- **A-01:** janela desktop de 740×580 px, mínimo de 700×540 px, em vez de 720×560 px.
- **A-02:** botões MC, MR, M+, M- e MS funcionais, embora o plano original previsse esses controles desabilitados.

## 4. Funcionalidades e validações confirmadas

### 4.1 Aplicação

- Motor de expressões matemáticas com avaliação AST, sem uso de `eval()`.
- Operações matemáticas, percentual contextual e raiz de índice n.
- Histórico de cálculos e recuperação de registros.
- ANS atualizado conforme as regras implementadas.
- Interface desktop Tkinter com tema Dark.
- Interface Web com Pyodide, tema e layout responsivo.
- Estrutura independente para a versão `v2.1.0/`, mantendo a aplicação da raiz.

### 4.2 Resultados de testes e validações

| Validação | Resultado conhecido | Evidência |
|---|---:|---|
| Testes da interface desktop | 21/21 aprovados | Resultado informado pelo usuário |
| Suíte completa Python | 92/92 aprovados | Resultado informado pelo usuário |
| Validação manual desktop | Confirmada | Confirmação do usuário |
| Suíte Web antes da última melhoria visual | 31/31 aprovados | Resultado informado pelo usuário em 01/11/2026 |
| Validação manual integrada Web | Confirmada | Usuário confirmou execução local via `python3 app.py`, operação básica, potência/raiz, histórico e ANS |
| Comparação com testes legados da baseline | 25 métodos preservados; nenhuma asserção original identificada como removida | Análise comparativa registrada |
| Experiência visual da página de testes após a última melhoria | Aprovada pelo usuário | Confirmação após o commit `49a5215` |

**Limite importante:** não há confirmação numérica de uma nova execução dos 31 testes Web após a última alteração de apresentação em `v2.1.0/testes.html`. Portanto, 31/31 não deve ser apresentado como resultado repetido após essa alteração. Essa confirmação será obtida na validação da página pública.

Os testes Python e desktop não precisam ser repetidos sem alteração de código ou outra justificativa técnica. A pendência numérica específica é a execução da suíte Web após a melhoria visual final.

## 5. Estrutura e preservação das versões

A comparação da branch com `main` identificou 27 arquivos alterados: 25 adicionados e 2 modificados, sem arquivos removidos.

| Local | Conteúdo | Situação |
|---|---|---|
| Raiz | Aplicação e testes da baseline `v2.0.0` | Preservados no diff |
| `v2.1.0/` | Aplicação evoluída, módulos Python, interfaces e testes próprios | Adicionados |
| `docs/` | Plano, adendo, registro de divergências e estado atual | Documentação do desafio |
| Raiz | README, CHANGELOG e arquivos de configuração compartilhados | Mantidos/atualizados |

As verificações estáticas registradas indicam que os recursos HTML, JavaScript e Python de cada versão usam seus próprios caminhos relativos. Isso ainda não comprova o funcionamento das rotas publicadas no GitHub Pages.

## 6. Decisões e cuidados vigentes

- Preservar a baseline `v2.0.0` e não alterar sua tag.
- Não reescrever o plano original; divergências aceitas permanecem no registro próprio.
- Não repetir testes aprovados sem mudança relevante ou justificativa.
- Não confundir implementação, validação local, commit, push, merge e publicação.
- Não integrar a branch à `main`, criar tag, release ou excluir branches sem autorização expressa.
- A versão `v2.1.0` está implementada, mas ainda não é uma release publicada.

## 7. Pendências reais e próxima ação

As fases de implementação estão concluídas. Não há necessidade identificada de reabrir fases anteriores ou ampliar funcionalidades.

- [x] Implementar as cinco fases no escopo acordado.
- [x] Registrar as adaptações aceitas.
- [x] Confirmar os resultados conhecidos das suítes Python e Web e as validações manuais informadas.
- [x] Preservar a aplicação da raiz e organizar a evolução em `v2.1.0/`.
- [x] Sincronizar a branch local com a remota até o commit `89482b1`.
- [x] Revisar a comparação remota com `main`: 82 commits à frente, 0 atrás, 27 arquivos alterados e nenhuma remoção.
- [ ] Abrir e validar no navegador a rota pública [`/v2.1.0/`](https://josearodrigues.github.io/alura-calculadora-python/v2.1.0/).
- [ ] Abrir [`/v2.1.0/testes.html`](https://josearodrigues.github.io/alura-calculadora-python/v2.1.0/testes.html), executar a bateria e confirmar o resultado numérico após a última melhoria visual.
- [ ] Conferir que a rota raiz continua apresentando a baseline `v2.0.0`: [GitHub Pages](https://josearodrigues.github.io/alura-calculadora-python/).
- [ ] Após as validações e nova revisão do estado Git, decidir com o usuário se a branch deve ser integrada à `main`.

**Próxima ação recomendada:** validar as três rotas do GitHub Pages no navegador, com atenção à execução dos 31 testes Web na página pública. Não repetir a suíte Python nem reabrir as fases anteriores sem evidência de regressão. Não realizar merge, criar tag/release ou excluir branches nesta etapa.

## 8. Registro histórico resumido

Esta seção preserva decisões e evidências relevantes das etapas anteriores sem manter várias cópias de estados operacionais que já ficaram desatualizados.

### Fases 3 a 5

- Fase 3: interface desktop revisada; adaptações A-01 e A-02 aceitas.
- Fase 4: compatibilidade legada removida da interface Web; suíte reorganizada em 31 cenários; detalhes dos cenários aprovados restaurados; apresentação da página de testes ajustada.
- Fase 5: testes Python, testes Web, comparação com a baseline e validação manual integrada registrados conforme resultados informados pelo usuário.
- Commits documentais e de implementação permanecem rastreáveis no histórico Git e em [REGISTRO-DIVERGENCIAS.md](REGISTRO-DIVERGENCIAS.md).

### Investigação e melhoria da experiência visual da suíte Web

A investigação inicial identificou que a página limpava a tabela no início, aguardava a execução completa e só então renderizava os resultados. Isso explicava a impressão de interface estática, sem caracterizar falha funcional do executor.

Uma implementação intermediária com controles temporários e atualização progressiva foi avaliada. A solução final simplificou a página para um único botão, informou o estado da espera pelo iframe/Pyodide e apresentou o relatório ao término, sem introduzir atraso artificial ou alterar os 31 cenários.

- Commit da solução final: `49a521556a6e400b4c4df85507e3c1de81573ad5`.
- Mensagem: `refactor: simplifica visualização da suíte web`.
- O usuário aprovou a experiência visual após testar a alteração.
- A aprovação visual não substitui a confirmação numérica de uma nova execução 31/31 após essa alteração; essa confirmação permanece na pendência da seção 7.

### Histórico documental

As seções antigas do documento registravam, em momentos diferentes, o estado das Fases 4 e 5, a coexistência das versões e a investigação da página de testes. Suas informações relevantes foram consolidadas nas seções atuais; detalhes de decisões e divergências permanecem no registro complementar e no histórico de commits.
