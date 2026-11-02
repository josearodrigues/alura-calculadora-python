# Estado Atual — Desafio 2: Calculadora Python

**Última atualização:** 02/11/2026

**Repositório:** `josearodrigues/alura-calculadora-python`

**Branch de referência remota:** `main`

**Último commit remoto confirmado antes da atualização de versionamento:** `c681745` — `feat(testes): adicionar barra de progresso à suíte web`

**Tag corretiva publicada:** `v2.1.1`, apontando para `1e33727`.

**Plano de referência:** [calculadora-2.0-plano.md](calculadora-2.0-plano.md)

**Adendo técnico:** [calculadora-2.0-adendo.md](calculadora-2.0-adendo.md)

**Registro de decisões:** [REGISTRO-DIVERGENCIAS.md](REGISTRO-DIVERGENCIAS.md)

> Este é o registro operacional de continuidade. O estado remoto foi consultado em 02/11/2026. O estado local do repositório não foi verificado nesta revisão. Os resultados de testes e as validações de interface são confirmações do usuário, não execuções realizadas pelo assistente.

## 1. Identificação e objetivo

Desafio 2 da Imersão Engenharia de Software: Dev na Era da IA, iniciativa da Alura Imersões em parceria com Google for Startups.

Objetivo pedagógico: compreender um código existente, implementar melhorias e verificar se o funcionamento anterior foi preservado.

Princípio de trabalho: **Compreender, implementar, validar e explicar.**

As cinco fases do plano foram concluídas no escopo acordado. A aplicação evoluída está integrada à `main`, identificada pela tag publicada `v2.1.0` e acessível no GitHub Pages. A melhoria posterior na página de testes Web foi formalizada pela tag publicada `v2.1.1`. A release formal do GitHub não foi criada.

## 2. Estado Git e versionamento

| Item | Estado confirmado |
|---|---|
| Repositório | `josearodrigues/alura-calculadora-python` |
| Branch principal remota | `main` |
| Último commit remoto confirmado | `c681745` — `feat(testes): adicionar barra de progresso à suíte web` |
| Branch remota de desenvolvimento | `desafio-2-revisao-final` — excluída por autorização do usuário |
| Branch local de desenvolvimento | `desafio-2-revisao-final` — excluída por autorização do usuário |
| Backup local `backup-v2.1.0` | Excluído por autorização do usuário |
| Última verificação das branches remotas | Apenas `main` listada |
| Estado local atual | Não verificado nesta revisão; conferir com o usuário antes de orientar operações locais |
| `origin/main` | Atualizada pelo push do commit `c681745`, confirmado no GitHub em 02/11/2026 |
| Sincronização local | O usuário informou que realizou o push da melhoria; o estado atual do clone local não foi consultado nesta revisão |
| Baseline histórica | `v2.0.0`, preservada na raiz e sem alteração pretendida |
| Evolução | `v2.1.0/`, integrada à `main` e servida pelo GitHub Pages |
| Tag `v2.1.0` | Publicada; aponta para o commit `481bbaa` e permanece intacta |
| Tag `v2.1.1` | Publicada pelo usuário em 02/11/2026; aponta para `1e33727` |
| Release GitHub | Não criada; não solicitada |

As atualizações documentais desta sessão são gravadas diretamente na `main` via GitHub. O SHA de cada atualização é informado ao usuário. Não se deve presumir que o clone local está sincronizado apenas porque o push anterior foi realizado; o estado local precisa ser confirmado separadamente.

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
- Página de testes Web com barra de progresso, percentual, contagem de cenários concluídos e contadores de resultados, melhoria posterior à tag `v2.1.0`.

### 4.2 Resultados informados pelo usuário

| Validação | Resultado | Situação |
|---|---:|---|
| Suíte Python da v2.1.0 | 92/92 aprovados | Confirmado pelo usuário em 31/10/2026 |
| Testes direcionados da interface desktop | 21/21 aprovados | Confirmado pelo usuário |
| Suíte Web da v2.1.0 | 31/31 aprovados, 0 falhas e 0 não executados | Confirmado pelo usuário em 01/11/2026, antes da inclusão posterior da barra de progresso |
| Duração aproximada da suíte Web | 1 minuto | Informada pelo usuário para a execução de 31/31 anterior à barra de progresso |
| Validação manual desktop | Funcionamento confirmado | Confirmado pelo usuário |
| Validação integrada local via `python3 app.py` | Operação básica, potência/raiz, histórico e ANS funcionando | Confirmado pelo usuário em 01/11/2026 |
| GitHub Pages — raiz | Baseline `v2.0.0` acessível | Confirmado pelo usuário |
| GitHub Pages — `/v2.1.0/` | Evolução acessível e funcional | Confirmado pelo usuário |
| GitHub Pages — `/v2.1.0/testes.html` | Página funcional; a execução numérica de 31/31 é anterior à barra de progresso | Confirmado pelo usuário |
| Comparação com testes legados da baseline | 25 métodos preservados; nenhuma asserção original identificada como removida | Análise comparativa registrada |

Esta documentação registra evidências comunicadas pelo usuário. Após a inclusão da barra de progresso, o usuário confirmou novos testes localmente e no GitHub Pages e aprovou o funcionamento e a apresentação. Não foi informado o quantitativo final exibido nessas execuções. A revisão estática do código não identificou bloqueios técnicos; observou apenas que o total de 31 cenários está fixado em `testes.html` e precisará acompanhar futuras mudanças na quantidade de testes. Não houve execução de testes pelo assistente. Não repetir as suítes sem justificativa técnica.

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
- Preservar as tags publicadas `v2.1.0` e `v2.1.1`; não alterar versões já publicadas.
- Não criar tag ou release sem autorização explícita.
- Não presumir que o repositório local está sincronizado com a `main` remota.
- Manter a rastreabilidade entre requisitos, adaptações aceitas, implementação e validações.

## 8. Pendências reais e próxima ação

- [x] Concluir as cinco fases no escopo acordado.
- [x] Integrar a evolução à branch remota `main`.
- [x] Excluir as branches de desenvolvimento locais e remotas, conforme autorização do usuário.
- [x] Validar as três rotas do GitHub Pages.
- [x] Confirmar 31/31 testes Web na versão anterior à barra de progresso.
- [x] Integrar a barra de progresso à página de testes Web após a publicação da tag `v2.1.0`.
- [x] Confirmar visual e funcionalmente a barra de progresso com o usuário.
- [x] Confirmar testes locais e no GitHub Pages após a inclusão da barra de progresso.
- [x] Revisar e alinhar os seis documentos do projeto.
- [ ] Confirmar o estado do clone local e sua sincronização com `origin/main`.
- [x] Formalizar a melhoria posterior como `v2.1.1`; tag criada localmente e enviada ao GitHub pelo usuário.
- [ ] Não criar release GitHub sem solicitação.

**Próxima ação recomendada:** se desejar continuar o trabalho, confirmar a sincronização do clone local com `origin/main`. A tag `v2.1.1` já foi publicada e a tag `v2.1.0` permanece intacta. O quantitativo da execução posterior da suíte não foi informado; não atribuir a ela o resultado histórico de 31/31. Não há justificativa identificada para reabrir as cinco fases.

## 9. Histórico resumido de encerramento

- **31/10/2026:** suíte Python informada como 92/92 aprovada; testes direcionados da interface desktop 21/21.
- **01/11/2026:** usuário confirmou validação integrada local, funcionamento das rotas públicas do GitHub Pages e reteste Web 31/31 após a melhoria visual final.
- **01/11/2026:** branch de desenvolvimento integrada à `main`; commit remoto de consolidação anterior à revisão documental: `b915990`.
- **01/11/2026:** branches de desenvolvimento local e remota e backup local excluídos mediante autorização.
- **01/11/2026:** revisão documental dos seis arquivos iniciada; naquele momento, a tag `v2.1.0` ainda estava pendente.
- **02/11/2026:** tag `v2.1.0` confirmada como publicada; commit `481bbaa`.
- **02/11/2026:** melhoria da barra de progresso integrada à `main` no commit `c681745`; usuário confirmou testes locais e no GitHub Pages e aprovou a validação visual e funcional. O quantitativo final dessas execuções não foi informado.
- **02/11/2026:** documentação atualizada para refletir a tag publicada `v2.1.1`, a melhoria posterior e a ausência de uma nova confirmação numérica dos testes após a barra de progresso.

