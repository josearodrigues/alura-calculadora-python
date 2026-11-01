# Registro de Divergências e Evolução do Escopo

**Projeto:** Calculadora Python — Desafio 2  
**Repositório:** `josearodrigues/alura-calculadora-python`  
**Branch de referência:** `desafio-2-revisao-final`  
**Criado em:** 31/10/2026  
**Última atualização:** 31/10/2026

> Documento complementar ao plano original. Os critérios publicados permanecem preservados como referência histórica e de rastreabilidade. As adaptações aceitas são registradas separadamente, sem reescrever os requisitos originais.

## 1. Referência da Fase 3

A referência é a seção **“Fase 3 — Interface Desktop Tkinter (Calculadora 2.0 Dark)”** de [docs/calculadora-2.0-plano.md](calculadora-2.0-plano.md), na branch `desafio-2-revisao-final`.

Os critérios incluem: janela de 720×560 px, tema Dark, visor duplo, teclado completo, template de raiz enésima `root(` com separador `;`, recuperação de histórico com atualização do ANS, continuidade após recuperação, limpeza do histórico preservando ANS, botões de memória desabilitados com indicação “Em breve” e atalhos físicos.

## 2. Adaptações aceitas para a implementação desktop

Em 31/10/2026, o usuário aceitou manter as seguintes escolhas já implementadas:

| ID | Critério publicado | Implementação mantida | Decisão |
|---|---|---|---|
| A-01 | Janela de 720×560 px | Janela configurada em 740×580 px, com mínimo de 700×540 px. | Aceita. Não alterar a dimensão desktop nesta revisão. |
| A-02 | Botões MC/MR/M+/M-/MS desabilitados, com indicação “Em breve”. | Botões de memória funcionais, com operações de armazenar, recuperar, somar, subtrair e limpar. | Aceita como evolução antecipada. Manter funcionalidade. |

**Importante:** essas adaptações dizem respeito exclusivamente à interface desktop Tkinter. Não definem dimensões nem requisitos da futura interface web, que será implementada e validada separadamente na Fase 4.

O plano original não será alterado para fazer os requisitos parecerem iguais à implementação. A diferença entre requisito publicado e decisão aceita permanece explícita.

## 3. Estado observado no código remoto

Base da conferência: arquivos da branch `desafio-2-revisao-final` consultados em 31/10/2026.

| ID | Comportamento | Evidência observada | Situação |
|---|---|---|---|
| C-01 | Dimensões da janela | `calculadora/interface.py`: `geometry("740x580")` e `minsize(700, 540)`. | Adaptação A-01 aceita |
| C-02 | Tema e visor | Tema `#0D1B2A`, expressão em cinza claro e resultado em ciano `#22D3EE`. | Implementado |
| C-03 | Teclado e raiz enésima | Teclado completo; `_aplicar_raiz_n()` insere `root(` ou `root(valor; ` após resultado. | Implementado; teste direcionado pendente |
| C-04 | Recuperação do histórico | `_recuperar_historico_por_id()` chama `historico.recuperar_entrada()`, restaura expressão/resultado e ativa o estado de resultado calculado. O modelo atualiza ANS para o valor recuperado. | Implementado; teste direcionado pendente |
| C-05 | Continuidade após recuperação | `_adicionar_operador()` utiliza o resultado exibido quando `_resultado_calculado` está ativo. | Implementado; teste direcionado pendente |
| C-06 | Limpeza do histórico | `limpar_historico()` remove registros visuais e do modelo; `HistoricoSessao.limpar_historico()` preserva ANS. | Implementado; teste direcionado pendente |
| C-07 | Memória | Os cinco botões são funcionais e possuem métodos correspondentes. | Adaptação A-02 aceita |
| C-08 | Atalhos físicos | Tratamento de dígitos, operadores, parênteses, Enter, Backspace, Escape/Delete e Ctrl+C em `_ao_pressionar_tecla()`. | Implementado; cobertura direcionada pendente |
| C-09 | Testes de interface | `tests/test_interface_desktop.py` contém 16 métodos de teste na versão consultada. | Cobertura existente; ampliar nos comportamentos listados acima |

## 4. Evoluções além do escopo originalmente previsto

| ID | Evolução | Relação com o plano | Situação |
|---|---|---|---|
| E-01 | Operações de memória MC, MR, M+, M- e MS. | O plano previa os botões desabilitados na Fase 3 e a memória em evolução posterior. | Implementadas e mantidas por decisão do usuário. |
| E-02 | Ampliação dos testes da interface para 16 métodos. | Amplia a cobertura da Fase 3. | Código remoto conferido; resultado de execução atual ainda não revalidado nesta auditoria. |
| E-03 | Suíte geral com 87 testes aprovados. | Resultado informado em sessão anterior. | Registro histórico; não reexecutado nesta conferência. |
| E-04 | Validação manual da interface desktop pelo usuário. | Validação funcional da GUI. | Considerada realizada conforme confirmação anterior do usuário; não repetir sem justificativa. |

## 5. Pendências da auditoria da Fase 3

- [ ] Acrescentar testes direcionados para template `root(` e sua variante após resultado.
- [ ] Acrescentar teste de recuperação de um registro do histórico, incluindo atualização do ANS.
- [ ] Acrescentar teste da continuidade do cálculo após recuperar um registro.
- [ ] Acrescentar teste de limpeza do histórico preservando ANS.
- [ ] Acrescentar teste direcionado aos atalhos físicos essenciais.
- [ ] Executar os testes novos e a suíte de regressão pertinente no ambiente local.
- [ ] Atualizar o documento `docs/ESTADO-ATUAL.md` no repositório, após conferir o estado local e remoto.
- [ ] Fechar a revisão documental e confirmar os critérios restantes da Fase 3 antes de iniciar a Fase 4.

As adaptações A-01 e A-02 não são pendências de correção: foram aceitas e devem permanecer como decisões registradas.

## 6. Versionamento e sequência

O plano original organiza a Fase 3 como interface desktop, a Fase 4 como interface web e a Fase 5 como validação integrada, regressão e documentação. A memória foi implementada antecipadamente; sua manutenção não altera a separação entre desktop e web.

Nenhuma tag, release ou versão nova é presumida por este registro. A identificação da versão deve ser conferida em conjunto com o estado Git e a documentação antes de qualquer publicação.

## 7. Histórico de atualizações

### 31/10/2026 — Registro inicial
- Foram documentadas divergências observadas na consulta inicial dos arquivos remotos.
- Foram separadas as evoluções relatadas que ainda precisavam de confronto com o código.

### 31/10/2026 — Auditoria e decisões do usuário
- Conferidos novamente `calculadora/interface.py`, `calculadora/historico.py` e `tests/test_interface_desktop.py`.
- Confirmados no código remoto: janela 740×580, memória funcional, recuperação do histórico com atualização do ANS e 16 métodos de teste da interface.
- O usuário aceitou manter a dimensão desktop 740×580 e a memória funcional.
- Preservados os critérios originais no plano e registradas as duas adaptações como decisões aceitas.
- Identificadas lacunas de testes direcionados; sua inclusão e execução permanecem pendentes.
