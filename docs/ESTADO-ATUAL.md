# Estado Atual — Desafio 2: Calculadora Python

**Última atualização:** 01/11/2026  
**Repositório:** `josearodrigues/alura-calculadora-python`  
**Branch de referência remota:** `main`  
**Último commit remoto conhecido antes desta revisão documental:** `b915990` — `docs: consolidar estado atual do desafio 2`  
**Plano de referência:** [calculadora-2.0-plano.md](calculadora-2.0-plano.md)  
**Adendo técnico:** [calculadora-2.0-adendo.md](calculadora-2.0-adendo.md)  
**Registro de decisões:** [REGISTRO-DIVERGENCIAS.md](REGISTRO-DIVERGENCIAS.md)

> Este é o registro operacional de continuidade. Os dados locais abaixo refletem a última saída de terminal informada pelo usuário; não foram revalidados nesta revisão. Os resultados de testes e as validações de interface são confirmações do usuário, não execuções realizadas pelo assistente.

## 1. Identificação e objetivo

Desafio 2 da Imersão Engenharia de Software: Dev na Era da IA, iniciativa da Alura Imersões em parceria com Google for Startups.

Objetivo pedagógico: compreender um código existente, implementar melhorias e verificar se o funcionamento anterior foi preservado.

Princípio de trabalho: **Compreender, implementar, validar e explicar.**

As cinco fases do plano foram concluídas no escopo acordado. A aplicação evoluída está integrada à `main` e acessível no GitHub Pages. A criação da tag e da release formal `v2.1.0` permanece como etapa pendente de versionamento.

## 2. Estado Git e versionamento

| Item | Estado confirmado |
|---|---|
| Repositório | `josearodrigues/alura-calculadora-python` |
| Branch principal remota | `main` |
| Último commit remoto conhecido antes desta revisão | `b915990` — `docs: consolidar estado atual do desafio 2` |
| Branch remota de desenvolvimento | `desafio-2-revisao-final` — excluída por autorização do usuário |
| Branch local de desenvolvimento | `desafio-2-revisao-final` — excluída por autorização do usuário |
| Backup local `backup-v2.1.0` | Excluído por autorização do usuário |
| Última verificação das branches remotas | Apenas `main` listada |
| Último estado local informado | Branch `main` limpa, em `cff94f2`, 83 commits atrás de `origin/main` |
| Último `origin/main` observado após `git fetch origin` | `b915990` |
| Sincronização local após o fetch | Pendente de confirmação; foi recomendado `git pull --ff-only origin main`, mas não há resultado informado de sua execução |
| Baseline histórica | `v2.0.0`, preservada na raiz e sem alteração pretendida |
| Evolução | `v2.1.0/`, integrada à `main` e servida pelo GitHub Pages |
| Tag `v2.1.0` | Ainda não criada |
| Release GitHub `v2.1.0` | Ainda não criada; não solicitada |

Os commits documentais desta revisão estão sendo gravados diretamente na `main` via GitHub. O SHA mais recente deve ser consultado no GitHub ao retomar. Não se deve tratar a `main` local como sincronizada até o usuário confirmar o pull e o estado do Git.

## 3. Situação das cinco fases

| Fase | Escopo | Situação documentada |
|---|---|---|
| 1 | Motor matemático, segurança e avaliador AST | Implementada e coberta pela suíte Python |
| 2 | Histórico e gestão de ANS | Implementada e coberta pela suíte Python |
| 3 | Interface desktop Tkinter | Concluída; adaptações A-01 e A-02 aceitas |
| 4 | Interface Web com Pyodide, tema e responsividade | Concluída e validada pelo usuário |
| 5 | Validação integrada, regressão e documentação | Concluída no escopo acordado |

### 3.1 Adaptações aceitas

- **A-01:** janela desktop de 740×580 px, mínimo de 700×540 px, em vez de 720×560 px.
- **A-02:** botões MC, MR, M+, M- e MS funcionais, embora o plano original previsse esses controles desabilitados.

Detalhes e rastreabilidade: [REGISTRO-DIVERGENCIAS.md](REGISTRO-DIVERGENCIAS.md).

## 4. Funcionalidades e resultados de validação

### 4.1 Funcionalidades da evolução

- Avaliador de expressões matemáticas com parser/AST próprio, sem uso de `eval()`.
- Operações básicas e avançadas, percentual contextual e raiz de índice n.
- Histórico de cálculos, recuperação de registros e continuidade com `ANS`.
- Memória na interface desktop.
- Interfaces desktop Tkinter e Web com Pyodide.
- Suítes de testes independentes para a baseline e para a evolução.

### 4.2 Resultados informados pelo usuário

| Validação | Resultado | Situação |
|---|---:|---|
| Suíte Python da v2.1.0 | 92/92 aprovados | Confirmado pelo usuário em 31/10/2026 |
| Testes direcionados da interface desktop | 21/21 aprovados | Confirmado pelo usuário |
| Suíte Web da v2.1.0 | 31/31 aprovados, 0 falhas e 0 não executados | Confirmado pelo usuário em 01/11/2026, após a última melhoria visual |
| Duração aproximada da suíte Web | 1 minuto | Informada pelo usuário |
| Validação manual desktop | Funcionamento confirmado | Confirmado pelo usuário |
| Validação integrada local via `python3 app.py` | Operação básica, potência/raiz, histórico e ANS funcionando | Confirmado pelo usuário em 01/11/2026 |
| GitHub Pages — raiz | Baseline `v2.0.0` acessível | Confirmado pelo usuário |
| GitHub Pages — `/v2.1.0/` | Evolução acessível e funcional | Confirmado pelo usuário |
| GitHub Pages — `/v2.1.0/testes.html` | Página funcional; 31/31 testes aprovados | Confirmado pelo usuário |
| Comparação com testes legados da baseline | 25 métodos preservados; nenhuma asserção original identificada como removida | Análise comparativa registrada |

Esta documentação registra evidências comunicadas pelo usuário. Não houve nova execução de testes durante a revisão documental. Não repetir as suítes sem alteração de código ou justificativa técnica.

## 5. Organização das versões

- Raiz do repositório: baseline `v2.0.0`, preservada.
- Diretório `v2.1.0/`: aplicação evoluída, interfaces e testes próprios.
- Diretório `docs/`, README, CHANGELOG e LICENSE: documentação e recursos compartilhados.

O usuário confirmou que a raiz do GitHub Pages continuou apresentando a baseline e que as rotas da evolução e da página de testes estavam acessíveis.

## 6. Documentação revisada nesta etapa

Em 01/11/2026, foi iniciada revisão integral dos seis documentos abaixo, considerando seu conteúdo completo e confrontando afirmações de estado com as confirmações disponíveis:

- [README.md](../README.md): descrição das versões, execução, testes e estado de publicação.
- [CHANGELOG.md](../CHANGELOG.md): registro das alterações e resultados da evolução.
- [calculadora-2.0-plano.md](calculadora-2.0-plano.md): requisitos originais e situação de execução.
- [calculadora-2.0-adendo.md](calculadora-2.0-adendo.md): decisões técnicas originais e atualização posterior.
- [REGISTRO-DIVERGENCIAS.md](REGISTRO-DIVERGENCIAS.md): adaptações aceitas e histórico das fases.
- Este documento: estado operacional atual.

A revisão busca eliminar instruções de trabalho já superadas, corrigir afirmações contraditórias e evitar duplicação de estados operacionais. Requisitos originais, decisões técnicas e evidências históricas relevantes foram preservados.

## 7. Decisões e cuidados vigentes

- Preservar a baseline `v2.0.0`; não alterar sua tag nem seus arquivos.
- Não reabrir as cinco fases nem ampliar funcionalidades sem evidência ou solicitação.
- Não repetir testes aprovados sem mudança relevante ou justificativa.
- Diferenciar GitHub Pages funcional de tag/release formal.
- Não criar tag ou release sem autorização explícita.
- Não presumir que o repositório local está sincronizado com a `main` remota.
- Manter a rastreabilidade entre requisitos, adaptações aceitas, implementação e validações.

## 8. Pendências reais e próxima ação

- [x] Concluir as cinco fases no escopo acordado.
- [x] Integrar a evolução à branch remota `main`.
- [x] Excluir as branches de desenvolvimento locais e remotas, conforme autorização do usuário.
- [x] Validar as três rotas do GitHub Pages.
- [x] Confirmar 31/31 testes Web após a última melhoria visual.
- [x] Revisar e alinhar os seis documentos do projeto.
- [ ] Confirmar a sincronização da `main` local com `origin/main`; última informação disponível indicava 83 commits de atraso.
- [ ] Após concluir a revisão documental e confirmar o estado remoto, obter autorização específica para criar a tag `v2.1.0`.
- [ ] Não criar release GitHub sem solicitação.

**Próxima ação recomendada:** concluir a conferência documental dos arquivos atualizados e, em seguida, tratar exclusivamente da sincronização local e da autorização para criar a tag `v2.1.0`. Não há justificativa identificada para novas funcionalidades ou repetição dos testes já aprovados.

## 9. Histórico resumido de encerramento

- **31/10/2026:** suíte Python informada como 92/92 aprovada; testes direcionados da interface desktop 21/21.
- **01/11/2026:** usuário confirmou validação integrada local, funcionamento das rotas públicas do GitHub Pages e reteste Web 31/31 após a melhoria visual final.
- **01/11/2026:** branch de desenvolvimento integrada à `main`; commit remoto de consolidação anterior à revisão documental: `b915990`.
- **01/11/2026:** branches de desenvolvimento local e remota e backup local excluídos mediante autorização.
- **01/11/2026:** revisão documental dos seis arquivos iniciada. Tag e release formal `v2.1.0` continuam pendentes.

