# Estado Atual — Desafio 2: Calculadora Python

**Última atualização:** 31/10/2026  
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
| Último commit de implementação informado pelo usuário | `ff8f6def9ad01b93887e5f9ba989600be34bbaa6` — `test: amplia cobertura da interface desktop` |
| Commit documental mais recente nesta branch | `60bc52597e819fa4f615fdbafd0937e53864ae5b` — `docs: atualiza validação da fase 3` |
| Estado remoto da branch de trabalho | GitHub confirma o commit `ff8f6de` na ancestralidade e um commit documental posterior. A branch remota está um commit à frente de `ff8f6de`. |
| Estado local | Último estado informado pelo usuário: HEAD em `ff8f6de`, um commit à frente do remoto anterior. Após o commit documental feito diretamente no GitHub, a sincronização local precisa ser conferida. Working tree local atual não verificada. |
| Última versão publicada conhecida | `v2.0.0` |
| Próxima versão prevista no plano | `v2.1.0`, condicionada à conclusão das fases previstas e validações da Fase 5. Ainda não publicada. |

Não foi feita nesta atualização uma conferência da branch `main`, das tags remotas ou do estado de publicação do GitHub Pages. Não presumir que estejam sincronizados com a branch de trabalho.

## 3. Situação das fases do plano

| Fase | Escopo | Situação registrada |
|---|---|---|
| 1 | Motor matemático, segurança e avaliador AST | Implementada anteriormente; funcionalidades cobertas pela suíte Python atual. Não foi realizada nova auditoria individual de cada critério nesta atualização. |
| 2 | Histórico e gestão de ANS em Python | Implementada anteriormente; histórico, recuperação e ANS possuem testes na suíte atual. Não foi realizada nova auditoria individual de cada critério nesta atualização. |
| 3 | Interface desktop Tkinter | Implementação conferida e validada. Testes direcionados adicionados; 21/21 testes de interface e 92/92 testes da suíte completa aprovados, conforme execução informada pelo usuário. Validação manual da GUI confirmada pelo usuário. Revisão documental ainda precisa ser concluída. |
| 4 | Interface web com Pyodide, tema e responsividade | Pendente. Não iniciar antes de concluir a revisão da Fase 3 e confirmar o escopo da próxima etapa. |
| 5 | Validação integrada, regressão e documentação da versão | Pendente. Inclui validação web, regressão integrada, atualização documental e preparação da versão prevista no plano. |

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

**Resultados informados pelo usuário em 31/10/2026:**

| Validação | Resultado |
|---|---:|
| Testes da interface desktop | 21/21 aprovados |
| Suíte completa Python | 92/92 aprovados |
| Validação manual da interface desktop | Confirmada pelo usuário |

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
| `docs/REGISTRO-DIVERGENCIAS.md` | Atualizado em 31/10/2026 com adaptações, evidências e resultados da Fase 3. |
| `docs/ESTADO-ATUAL.md` | Este documento; criado para registrar a continuidade do desafio. |
| `README.md` | Ainda descreve a baseline `v2.0.0` e os 25 testes Python/11 testes web da versão publicada. Atualização da documentação da versão evoluída permanece para a etapa apropriada do plano. |

## 7. Decisões e cuidados

- Preservar os requisitos originais e registrar separadamente as adaptações aceitas.
- Não ampliar o escopo da Fase 3 nem reimplementar funcionalidades já validadas.
- Não repetir testes aprovados sem justificativa técnica.
- Não confundir o commit local de implementação com os commits documentais feitos diretamente na branch remota.
- Antes de novas operações Git, conferir o estado local e remoto. Não executar operações destrutivas.
- A interface web da Fase 4 possui requisitos próprios; as dimensões da janela desktop não determinam o layout web.
- A versão `v2.1.0` é uma previsão do plano, não uma release já criada.

## 8. Pendências e próxima ação

Pendências registradas para concluir a revisão da Fase 3:

- [ ] Sincronizar a branch local com o commit documental `60bc525` e conferir o estado Git.
- [ ] Fazer a revisão documental final da Fase 3, confrontando plano, registro de divergências, estado atual e implementação.
- [ ] Confirmar o encerramento da Fase 3 antes de iniciar outra fase.

Depois da revisão da Fase 3, a próxima etapa prevista no plano é a **Fase 4 — Interface Web (Pyodide, Dark Premium e Responsividade)**. A Fase 5 permanece posterior.

**Próxima ação operacional recomendada:** no ambiente local, conferir primeiro:

```bash
git status --short --branch
git log -1 --oneline
```

Com a saída, confirmar a sincronização antes de qualquer nova alteração. Não iniciar implementação da Fase 4 nesta etapa.
