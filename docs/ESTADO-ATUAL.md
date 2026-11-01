# Estado Atual — Desafio 2: Calculadora Python

**Última atualização:** 01/11/2026  
**Repositório:** `josearodrigues/alura-calculadora-python`  
**Branch de trabalho:** `desafio-2-revisao-final`  
**Branch principal:** `main`  
**Plano de referência:** [calculadora-2.0-plano.md](calculadora-2.0-plano.md)  
**Registro complementar:** [REGISTRO-DIVERGENCIAS.md](REGISTRO-DIVERGENCIAS.md)

> Este documento registra o estado conhecido para continuidade do desafio. Distingue implementação, testes, commits, sincronização remota e publicação. Informações locais que não puderam ser verificadas nesta atualização estão identificadas como pendentes de confirmação.

## 1. Identificação e objetivo

Desafio 2 da Imersão Engenharia de Software: Dev na Era da IA, iniciativa da Alura Imersões em parceria com Google for Startups.

Objetivo pedagógico: praticar uma atividade comum na Engenharia de Software — compreender um código existente, implementar melhorias e verificar se o funcionamento anterior foi preservado.

Princípio de trabalho: **Compreender, implementar, validar e explicar.**

O escopo da Calculadora 2.0 está organizado no plano original em cinco fases. Este documento não substitui nem reescreve esse plano.

## 2. Repositório, branches e versionamento

| Item | Estado confirmado em 01/11/2026 |
|---|---|
| Repositório | `josearodrigues/alura-calculadora-python` |
| Branch de trabalho | `desafio-2-revisao-final` |
| Branch principal | `main` |
| Último commit local informado pelo usuário | `c15bce5` — documentação da coexistência das versões. |
| Commit que consolidou a atualização operacional do estado | `201da2f` — atualização do estado operacional da coexistência das versões; houve depois um commit curto de correção da referência histórica deste registro. |
| Estado local conhecido | Working tree limpa após fast-forward até `c15bce5`, conforme saída enviada pelo usuário. Os dois commits documentais posteriores feitos diretamente no GitHub ainda precisam ser buscados localmente. |
| Comparação remota com `main` | `desafio-2-revisao-final` está 65 commits à frente e 0 atrás; comparação consultada no GitHub em 01/11/2026. |
| Último commit de `main` observado | `cff94f2` — não alterado nesta revisão. |
| Última versão publicada conhecida | `v2.0.0` |
| Evolução em desenvolvimento | `v2.1.0`, organizada em `v2.1.0/`; ainda não publicada como release. |

A comparação remota confirma que a branch de trabalho contém a linha de desenvolvimento em relação à `main`. A contagem de commits é dinâmica e deve ser consultada novamente antes do merge.

Os commits documentais mais recentes foram feitos diretamente no GitHub. Portanto, antes de qualquer merge, execute `git fetch origin` e atualize a branch local por fast-forward, depois confira o estado da working tree. Não presumir que a branch local já contém esses commits.

## 3. Situação das fases do plano

| Fase | Escopo | Situação registrada |
|---|---|---|
| 1 | Motor matemático, segurança e avaliador AST | Implementada anteriormente; funcionalidades cobertas pela suíte Python atual. Não foi realizada nova auditoria individual de cada critério nesta atualização. |
| 2 | Histórico e gestão de ANS em Python | Implementada anteriormente; histórico, recuperação e ANS possuem testes na suíte atual. Não foi realizada nova auditoria individual de cada critério nesta atualização. |
| 3 | Interface desktop Tkinter | **Concluída.** Implementação conferida; 21/21 testes de interface e 92/92 testes da suíte completa aprovados, conforme execução informada pelo usuário. Validação manual da GUI confirmada pelo usuário. Revisão documental concluída em 31/10/2026. Adaptações A-01 e A-02 aceitas e registradas. |
| 4 | Interface web com Pyodide, tema e responsividade | **Implementada e validada pelo usuário no escopo executado.** Remoção do fluxo legado, suíte Web atualizada para 31 cenários, evidências restauradas e página de testes ajustada. A validação integrada e a regressão final pertencem à Fase 5. |
| 5 | Validação integrada, regressão e documentação da versão | **Concluída no escopo documentado.** Python 92/92, Web 31/31, comparação da baseline sem remoção de asserções identificada, execução integrada via `app.py` e verificações manuais de operação básica, potência/raiz, histórico e ANS confirmadas pelo usuário. Documentação atualizada. A release `v2.1.0` ainda não foi publicada. |

### 3.1 Adaptações aceitas na Fase 3

As seguintes diferenças em relação aos requisitos originais foram aceitas pelo usuário e não devem ser tratadas como defeitos pendentes:

- **A-01:** manter a janela desktop em 740×580 px, com mínimo de 700×540 px, em vez de 720×560 px.
- **A-02:** manter funcionais os botões MC, MR, M+, M- e MS, embora o plano original previsse botões desabilitados com indicação “Em breve”.

As decisões estão detalhadas em [REGISTRO-DIVERGENCIAS.md](REGISTRO-DIVERGENCIAS.md). O plano original permanece preservado.

## 4. Funcionalidades da Fase 3 verificadas

- Interface desktop Tkinter com tema Dark, visor duplo e teclado completo.
- Botão de raiz enésima insere o template `root(` e, após resultado, `root(valor; `.
- Recuperação de item do histórico restaura expressão e resultado e atualiza o ANS.
- Operador após recuperação permite continuar o cálculo a partir do valor recuperado.
- Limpeza do histórico preserva o ANS.
- Atalhos físicos são encaminhados aos métodos correspondentes.
- Botões de memória permanecem funcionais por decisão aceita.

## 5. Testes e validações

**Resultados informados pelo usuário em 31/10 e 01/11/2026:**

| Validação | Resultado |
|---|---:|
| Testes da interface desktop | 21/21 aprovados |
| Suíte completa Python | 92/92 aprovados |
| Validação manual da interface desktop | Confirmada pelo usuário |
| Suíte Web | 31/31 aprovados; 0 falhas; 0 não executados (01/11/2026) |
| Integração local via `app.py` | Confirmada pelo usuário em 01/11/2026 |
| Verificação manual integrada | Operação básica, potência ou raiz, histórico e ANS: todos funcionando, conforme confirmação do usuário em 01/11/2026 |
| Comparação dos testes legados da baseline | 25 métodos preservados; nenhuma asserção original removida na análise comparativa |

Os cinco testes direcionados adicionados foram:

1. Template de raiz enésima com e sem resultado anterior.
2. Recuperação do histórico e atualização do ANS.
3. Continuidade do cálculo após recuperação.
4. Limpeza do histórico preservando ANS.
5. Encaminhamento dos atalhos físicos.

Os testes foram executados pelo usuário. Este registro não afirma que foram reexecutados durante a atualização documental.

## 6. Arquivos e documentação envolvidos

| Arquivo | Situação |
|---|---|
| `calculadora/interface.py` | Interface desktop implementada; referência da Fase 3. |
| `calculadora/historico.py` | Modelo de histórico e ANS utilizado pela interface. |
| `tests/test_interface_desktop.py` | 21 métodos de teste, com resultado informado de 21/21 aprovados. |
| Demais testes em `tests/` | Integram a suíte completa, com resultado informado de 92/92 aprovados. |
| `docs/calculadora-2.0-plano.md` | Plano original preservado. |
| `docs/REGISTRO-DIVERGENCIAS.md` | Atualizado em 01/11/2026 com decisões de escopo, arquivos, commits e validação da Fase 4. |
| `docs/ESTADO-ATUAL.md` | Atualizado em 01/11/2026 para registrar a conclusão da Fase 5 no escopo documentado. |
| `README.md` | Atualizado nesta revisão com recursos matemáticos, sintaxe `root(rad; ind)`, percentual contextual, atalhos por interface e resultados 92/92 e 31/31. Commit `702f2d3`. |
| `CHANGELOG.md` | Consolidado para registrar as funcionalidades da evolução `v2.1.0`, mudanças da Fase 4 e resultados conhecidos, sem declarar release. Commit `2b02e02`. |

## 7. Decisões e cuidados

- Preservar os requisitos originais e registrar separadamente as adaptações aceitas.
- Não ampliar o escopo da Fase 3 nem reimplementar funcionalidades já validadas.
- Não repetir testes aprovados sem justificativa técnica.
- Não confundir o commit local de implementação com os commits documentais feitos diretamente na branch remota.
- Antes de novas operações Git, conferir o estado local e remoto. Não executar operações destrutivas.
- A interface web da Fase 4 possui requisitos próprios; as dimensões da janela desktop não determinam o layout web.
- A versão `v2.1.0` é uma previsão do plano, não uma release já criada.

## 8. Pendências e próxima ação

**Fases 1 a 5 concluídas no escopo documentado.** A evolução `v2.1.0` está implementada e validada localmente pelo usuário, mas ainda não foi publicada.

- [x] Concluir as fases de implementação e validação previstas no plano, com adaptações aceitas registradas separadamente.
- [x] Confirmar 92/92 testes Python e 31/31 cenários Web aprovados, conforme resultados informados pelo usuário.
- [x] Confirmar execução integrada local via `app.py` e fluxos manuais de operação básica, potência/raiz, histórico e ANS.
- [x] Preservar a aplicação `v2.0.0` na raiz e organizar a aplicação `v2.1.0` em subdiretório próprio.
- [x] Atualizar README, CHANGELOG, ESTADO-ATUAL e REGISTRO-DIVERGENCIAS para descrever a coexistência.
- [ ] Validar publicamente a rota `/v2.1.0/` e a página `/v2.1.0/testes.html` no GitHub Pages. A verificação estática dos caminhos relativos não substitui essa validação.
- [ ] Buscar localmente os dois commits documentais mais recentes (`77c36dc` e `9b9891e`) e confirmar sincronização e working tree limpa.
- [ ] Revisar o diff final de `desafio-2-revisao-final` em relação à `main`, confirmando que a baseline `v2.0.0` permanece preservada.
- [ ] Somente após as validações e autorização do usuário, integrar a branch na `main`, validar a publicação e considerar a remoção das branches temporárias.

**Próxima ação operacional:** no ambiente local, execute `git fetch origin`; em seguida, atualize a branch por fast-forward e confira `git status --short --branch`. Não executar merge na `main`, criar tag/release ou excluir branches antes da validação do GitHub Pages e da revisão final do diff.

## 9. Estado da Fase 4 — 01/11/2026

### Implementação registrada
- Remoção da seção de compatibilidade legada em `index.html`, das funções/ponte e eventos exclusivos em `app.js`, e da regra CSS correspondente.
- Reescrita da suíte Web para a interface atual; remoção autorizada do cenário estrutural TW-03; total atual: 31 cenários.
- Correção da inicialização e da sintaxe do executor após problemas identificados na primeira alteração.
- Restauração da captura de detalhes retornados pelos cenários aprovados.
- Ajuste visual do cabeçalho e da responsividade da página `testes.html`.

### Commits da Fase 4
| Commit | Resumo |
|---|---|
| `3711a5e` | Remoção da compatibilidade legada e reescrita da suíte |
| `106bb55` | Correção da inicialização e sintaxe do executor |
| `1b896ce` | Remoção autorizada do TW-03 |
| `dcc96af` | Atualização da contagem para 31 cenários |
| `c9f4ee7` | Restauração dos detalhes dos cenários aprovados |
| `9ca9d1a` | Ajuste visual da página de testes |

### Validação informada pelo usuário
Em 01/11/2026, o usuário confirmou após `git pull`:
- Suíte Web funcionando após a remoção do legado.
- Evidências/detalhes visíveis nos cenários que fornecem retorno.
- Cabeçalho e layout aprovados visualmente.
- Tabela e última coluna visíveis na apresentação testada.

Resultado numérico confirmado pelo usuário na página: **31/31 aprovados, 0 falhas e 0 não executados (100% OK)**. A execução local integrada via `app.py` permanece pendente.

### Estado documental e limites
- O plano `docs/calculadora-2.0-plano.md` permanece preservado, sem reescrever requisitos originais.
- Decisões e divergências da Fase 4 estão em `docs/REGISTRO-DIVERGENCIAS.md`.
- A baseline publicada continua identificada como `v2.0.0`; não há confirmação de publicação da evolução `v2.1.0`.
- A sincronização do ambiente local do usuário ainda precisa ser conferida; o commit remoto mais recente desta atualização é `2b02e027d93ed247b8ed3fda951144d19a5e5d85`.


## 10. Atualização da Fase 5 — 01/11/2026

### Resultados consolidados
- Python: 92/92 aprovados, conforme execução informada pelo usuário em 31/10/2026.
- Web: 31/31 aprovados, 0 falhas e 0 não executados, conforme resultado exibido e informado pelo usuário em 01/11/2026.
- Baseline `v2.0.0`: comparação dos 25 métodos de teste legados; nenhum método ou asserção original foi identificado como removido. Cinco testes de integração passaram a chamar o método auxiliar `executar_fluxo_legado()`, cuja sequência de validação, cálculo e formatação foi comparada à implementação anterior.
- README e CHANGELOG atualizados nesta revisão remota. Não foi criada tag ou release.
- Execução local real por `app.py`: ainda não confirmada.

### Commits documentais desta atualização
| Commit | Arquivo |
|---|---|
| `702f2d3` | `README.md` |
| `2b02e02` | `CHANGELOG.md` |

### Estado remoto e local
A branch remota foi consultada após as atualizações e está em `2b02e027d93ed247b8ed3fda951144d19a5e5d85`. O estado local do usuário não é verificável por esta consulta remota e precisa ser sincronizado. A versão publicada conhecida continua `v2.0.0`; `v2.1.0` permanece não publicada.

### Critério que estava pendente naquele registro
A confirmação local foi recebida posteriormente e está documentada na seção 11. A Fase 5 está concluída no escopo documentado.


## 11. Encerramento da Fase 5 — 01/11/2026

### Confirmação integrada do usuário
O usuário confirmou que executou os testes manuais solicitados e que todos funcionaram:
- Operação aritmética básica.
- Expressão envolvendo potência ou raiz.
- Histórico.
- Continuidade com `ANS`.

A execução local da aplicação Web via `python3 app.py` também foi confirmada. Não se atribui ao assistente a execução local: os resultados são declarações de validação realizadas pelo usuário.

### Situação final
- Suíte Python: 92/92 aprovados (resultado informado pelo usuário).
- Suíte Web: 31/31 aprovados, 0 falhas e 0 não executados (resultado informado pelo usuário).
- Interface desktop: validação manual confirmada anteriormente pelo usuário.
- Interface Web local: funcionamento confirmado pelo usuário, incluindo os cenários integrados acima.
- Baseline `v2.0.0`: comparação estática dos 25 métodos legados, sem remoção identificada de métodos ou asserções.
- Fase 5: concluída no escopo documentado.
- Última versão publicada conhecida: `v2.0.0`. A evolução `v2.1.0` permanece não publicada.

### Commits documentais
- `b96c845` — README atualizado com validação integrada.
- `254de03` — CHANGELOG atualizado com conclusão da Fase 5.
- `0fcc3ce` — registro inicial da validação integrada em `REGISTRO-DIVERGENCIAS.md` (posteriormente harmonizado em `3de5628`).
- `5bb1a15` — atualização inicial do `ESTADO-ATUAL.md` (posteriormente harmonizado neste commit).
- `3de5628` — harmonização do histórico da Fase 5 e atualização de `REGISTRO-DIVERGENCIAS.md`.
- `91478c6` — harmonização do histórico e situação final da Fase 5 neste `ESTADO-ATUAL.md`.
- `HEAD` remoto consultado antes deste commit: `3de562803890e3cb901c836d0d5557824702403e`.

### Limite da verificação
A branch remota foi consultada; o estado da working tree local do usuário não é acessível por esta atualização. A sincronização local continua sendo uma tarefa operacional antes da publicação.


## 12. Coexistência das versões — atualização de 01/11/2026

### Estrutura confirmada na branch remota

Consulta direta ao GitHub confirmou na branch `desafio-2-revisao-final`:

| Local | Conteúdo | Situação |
|---|---|---|
| Raiz | Aplicação e testes da baseline `v2.0.0` | Preservados |
| `v2.1.0/` | Aplicação evoluída, módulos Python, interfaces e testes próprios | Presente |
| `docs/` | Plano, adendo, registro de divergências e estado atual | Compartilhado |
| Raiz | `README.md`, `CHANGELOG.md`, `LICENSE`, `.gitignore` e `.nojekyll` | Compartilhados |

### Verificações estáticas de coexistência

- O HTML da raiz usa referências relativas para os recursos da aplicação da raiz.
- O HTML em `v2.1.0/` usa referências relativas para os recursos do próprio subdiretório.
- Os dois arquivos `app.js` carregam os módulos Python correspondentes à sua versão em caminhos relativos.
- Os dois servidores `app.py` usam o diretório de trabalho em que são iniciados; o README orienta a execução de cada versão no diretório correto.
- O README distingue comandos, testes e endereços locais das duas versões.
- O CHANGELOG registra a organização sem declarar uma release da v2.1.0.
- O plano original e o adendo permanecem preservados.

Essas verificações são estáticas. A rota pública `/v2.1.0/` e a página `/v2.1.0/testes.html` no GitHub Pages ainda precisam ser verificadas no navegador antes do merge. Não há confirmação de publicação pública da v2.1.0.

### Estado Git e publicação

- Branch de trabalho remota: `desafio-2-revisao-final`.
- Comparação consultada com `main`: 65 commits à frente e 0 atrás.
- Último commit da `main` observado: `cff94f2`; nenhuma alteração na `main` foi realizada nesta revisão.
- Branch local do usuário: sincronizada e limpa até `c15bce5`, conforme saída fornecida. Os dois commits documentais subsequentes feitos diretamente no GitHub (`77c36dc` e `9b9891e`) ainda precisam ser buscados localmente.
- Última versão publicada conhecida: `v2.0.0`.
- `v2.1.0`: implementada e validada no escopo informado pelo usuário; não publicada como release.

### Próxima ação recomendada

Buscar os dois commits documentais no ambiente local, confirmar sincronização e working tree limpa, validar as duas rotas públicas no GitHub Pages e revisar o diff completo contra `main`. Somente então decidir o merge. Não excluir branches temporárias nem criar tag/release antes dessas etapas e da autorização do usuário.



## 13. Investigação da experiência visual do reteste Web — 01/11/2026

### Sintoma relatado

Na suíte Web da `v2.1.0`, ao clicar em Executar Bateria de Testes, a atualização é tão rápida que o usuário tem a impressão de que a tabela e as mensagens permanecem estáticas.

Na comparação com a `v2.0.0`, o comportamento visual do reteste parece diferente.

### Depuração realizada

Investigação acompanhada pelo usuário no Firefox Developer Tools, utilizando breakpoint no manipulador de clique de `v2.1.0/testes.html`.

Foram confirmados:

1. O clique alcança o `addEventListener`.
2. O botão é desabilitado durante a execução.
3. A mensagem de status é atualizada.
4. A tabela anterior é limpa por `corpoTabela.replaceChildren()`.
5. O fluxo de espera pelo iframe/Pyodide é executado.
6. A bateria de testes é executada.
7. Os resultados são renderizados.
8. O botão volta a ficar habilitado.

Após a depuração, o usuário repetiu o reteste sem pausas do depurador e confirmou que tudo funcionou.

### Análise do fluxo de renderização

Na implementação atual de `v2.1.0/testes.html`:

- A tabela é limpa no início.
- O código aguarda a conclusão de `executarTodosOsTestesWeb()`.
- Somente depois do retorno da função, `renderizarResultados(resultados)` apresenta os resultados.

Consequentemente, a interface não apresenta cada teste à medida que ele é executado. A tabela permanece vazia durante o processamento e é preenchida ao final.

### Conclusão

**Funcionamento:** reteste operacional, confirmado pelo usuário.

**Experiência visual:** melhoria necessária. A atualização atual não oferece acompanhamento progressivo suficientemente perceptível, causando a impressão de que o processo está estático.

### Pendência para a continuidade

O usuário deseja melhorar a experiência do reteste na `v2.1.0`, permitindo que quem utiliza a aplicação perceba que os testes estão sendo executados.

Essa melhoria permanece pendente e deve ser tratada antes do fechamento final do desafio.

Na retomada:

- Examinar o fluxo atual de execução e renderização.
- Avaliar alternativas de feedback visual e atualização progressiva.
- Apresentar uma proposta técnica objetiva, explicando as implicações.
- Aguardar a decisão do usuário antes de implementar.
- Após autorização, implementar e validar a melhoria.
- Preservar os 31 cenários existentes e confirmar que a suíte continua aprovada.

Não introduzir atrasos artificiais apenas para tornar a execução mais perceptível sem antes avaliar uma solução adequada de feedback visual.

### Limites desta investigação

Nenhum arquivo de código foi alterado durante a depuração. Nenhum teste foi removido ou modificado. Nenhum commit, push, merge ou publicação foi realizado como consequência desta investigação.

**Estado:** defeito funcional não reproduzido; melhoria de experiência do usuário identificada e pendente.
