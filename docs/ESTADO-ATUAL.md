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

| Item | Estado conhecido |
|---|---|
| Repositório | `josearodrigues/alura-calculadora-python` |
| Branch de trabalho | `desafio-2-revisao-final` |
| Branch principal | `main` |
| Último commit de implementação identificado nesta revisão | `9ca9d1a` — ajuste visual da página de testes (Fase 4). |
| Último commit remoto da branch verificado nesta atualização | `2b02e027d93ed247b8ed3fda951144d19a5e5d85` — `docs: consolidar changelog da calculadora 2.1`. |
| Commits documentais desta atualização | `702f2d3` — README; `2b02e02` — CHANGELOG. |
| Estado remoto da branch de trabalho | Confirmado pela API do GitHub no commit `2b02e027d93ed247b8ed3fda951144d19a5e5d85`. |
| Estado local | Não acessível nesta revisão remota. É necessário executar `git pull` e conferir `git status`; não presumir sincronização. |
| Última versão publicada conhecida | `v2.0.0` |
| Próxima versão prevista no plano | `v2.1.0`, condicionada à conclusão das fases previstas e validações da Fase 5. Ainda não publicada. |

Não foi feita nesta atualização uma conferência da branch `main`, das tags remotas ou do estado de publicação do GitHub Pages. Não presumir que estejam sincronizados com a branch de trabalho.

## 3. Situação das fases do plano

| Fase | Escopo | Situação registrada |
|---|---|---|
| 1 | Motor matemático, segurança e avaliador AST | Implementada anteriormente; funcionalidades cobertas pela suíte Python atual. Não foi realizada nova auditoria individual de cada critério nesta atualização. |
| 2 | Histórico e gestão de ANS em Python | Implementada anteriormente; histórico, recuperação e ANS possuem testes na suíte atual. Não foi realizada nova auditoria individual de cada critério nesta atualização. |
| 3 | Interface desktop Tkinter | **Concluída.** Implementação conferida; 21/21 testes de interface e 92/92 testes da suíte completa aprovados, conforme execução informada pelo usuário. Validação manual da GUI confirmada pelo usuário. Revisão documental concluída em 31/10/2026. Adaptações A-01 e A-02 aceitas e registradas. |
| 4 | Interface web com Pyodide, tema e responsividade | **Implementada e validada pelo usuário no escopo executado.** Remoção do fluxo legado, suíte Web atualizada para 31 cenários, evidências restauradas e página de testes ajustada. A validação integrada e a regressão final pertencem à Fase 5. |
| 5 | Validação integrada, regressão e documentação da versão | **Parcialmente concluída.** Suítes Python e Web aprovadas conforme resultados informados; testes legados comparados sem perda de asserções identificada; README e CHANGELOG atualizados. Execução local integrada via `app.py` e conferência final da documentação/estado local ainda pendentes. |

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
| `docs/ESTADO-ATUAL.md` | Atualizado em 01/11/2026 para registrar a Fase 4 e as pendências da Fase 5. |
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

**Fases 3 e 4 encerradas no escopo executado:** a Fase 3 foi validada e documentada em 31/10/2026. A Fase 4 foi implementada e validada pelo usuário em 01/11/2026. As decisões de escopo da interface Web estão registradas em `docs/REGISTRO-DIVERGENCIAS.md`; o plano original permanece preservado.

Pendências gerais do desafio:

- [ ] Sincronizar o ambiente local com os commits documentais remotos `702f2d3` e `2b02e02`; o estado local não foi acessível nesta revisão.
- [x] Executar e validar a Fase 4 — Interface Web, com as adaptações registradas em `docs/REGISTRO-DIVERGENCIAS.md`.
- [ ] Confirmar a execução local da interface Web por `python3 app.py` e validar o acesso à calculadora e à página `testes.html`.
- [x] Registrar 92/92 testes Python e 31/31 cenários Web aprovados, conforme resultados informados pelo usuário.
- [x] Comparar os 25 métodos de teste da baseline `v2.0.0` com a branch atual; não foi identificada remoção de teste ou asserção original.
- [x] Atualizar README e CHANGELOG para a evolução em desenvolvimento `v2.1.0`.
- [ ] Fazer revisão final da Fase 5 após a validação local e sincronização do ambiente.

As Fases 3 e 4 estão concluídas no escopo registrado, mas **o Desafio 2 como um todo não está concluído**. A versão `v2.0.0` continua sendo a última versão publicada conhecida; `v2.1.0` permanece condicionada à conclusão das fases previstas.

**Próxima ação operacional recomendada:** sincronizar os commits documentais e confirmar o servidor local:

```bash
git pull
git status --short --branch
git log -1 --oneline
python3 app.py
```

Com o servidor iniciado, abrir `http://127.0.0.1:3000` e `http://127.0.0.1:3000/testes.html`. Encerrar com `Ctrl+C`. A execução local ainda depende de confirmação no ambiente do usuário.

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

### Critério ainda necessário para encerrar a Fase 5
Executar `python3 app.py` no ambiente local, confirmar o acesso à interface e à página de testes, e então atualizar este documento com o resultado observado. Até lá, não declarar a Fase 5 nem o Desafio 2 concluídos.
