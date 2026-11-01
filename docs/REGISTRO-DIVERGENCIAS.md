# Registro de Divergências e Evolução do Escopo

**Projeto:** Calculadora Python — Desafio 2  
**Repositório:** `josearodrigues/alura-calculadora-python`  
**Branch de referência:** `desafio-2-revisao-final`  
**Documento criado em:** 31/10/2026  
**Última conferência remota:** 31/10/2026  
**Finalidade:** manter rastreabilidade entre os critérios publicados, a implementação realizada e as decisões tomadas durante a conclusão das fases.

> Este documento é complementar ao plano original. Não altera seus critérios nem reescreve seu histórico. A execução das próximas atividades seguirá os critérios da fase correspondente publicados no GitHub. Divergências serão registradas e avaliadas, sem serem tratadas automaticamente como erros ou como autorização para ampliar o escopo.

## 1. Referência de execução

A referência para a conclusão da Fase 3 é a seção **“Fase 3 — Interface Desktop Tkinter (Calculadora 2.0 Dark)”** de [docs/calculadora-2.0-plano.md](calculadora-2.0-plano.md), na branch `desafio-2-revisao-final`.

A fase especifica: janela Tkinter Dark, visor duplo, teclado completo, botão de raiz enésima com template `root(` e separador `;`, recuperação do histórico, continuidade com ANS, limpeza do histórico preservando ANS, botões de memória desabilitados com indicação “Em breve” e atalhos físicos.

**Regra de continuidade:** concluir e validar os critérios dessa fase antes de avançar. Nas fases seguintes, consultar os critérios publicados da respectiva fase e atualizar este registro.

## 2. Divergências identificadas na versão remota consultada

Base da análise: código e documentos disponíveis na branch `desafio-2-revisao-final`, commit `53de65a764e1f68f7126a2a4d12723a6bb3efea5`.

| ID | Critério / referência | Evidência encontrada | Situação |
|---|---|---|---|
| D-01 | Janela de 720×560 px | `calculadora/interface.py` configura `740x580` e tamanho mínimo `700x540`. | Divergência confirmada no remoto |
| D-02 | Botões de memória desabilitados com indicação visual “Em breve” | Os cinco botões são criados com `state=tk.DISABLED`. A expressão “Em breve” aparece na docstring do método, mas não no texto ou em outro elemento visual apresentado ao usuário. | Atendimento parcial no remoto |
| D-03 | Identificação da versão | A janela e o cabeçalho exibem “Calculadora 2.0”; a docstring da classe identifica “Calculadora 2.1”. | Inconsistência de identificação no remoto |
| D-04 | Testes da interface | O arquivo remoto `tests/test_interface_desktop.py` contém quatro métodos de teste. O `setUp()` converte qualquer exceção de inicialização em teste ignorado. | Cobertura e tratamento a revisar |
| D-05 | Plano e documentação | O README remoto consultado ainda descreve a estrutura e a contagem de testes de uma versão anterior à evolução da interface. | Documentação desatualizada no remoto |

## 3. Evoluções relatadas além do escopo da Fase 3

Os itens abaixo foram relatados durante as sessões de trabalho, mas precisam ser confrontados com a cópia local e com os commits antes de serem considerados parte do estado confirmado do repositório:

| ID | Evolução relatada | Relação com o plano | Confirmação necessária |
|---|---|---|---|
| E-01 | Implementação das operações de memória MC, MR, M+, M- e MS. | O plano deixa os botões desabilitados na Fase 3 e prevê a ativação da memória em uma evolução posterior, indicada como v2.2.0. | Conferir código local, testes e decisão de escopo/versionamento. |
| E-02 | Ampliação dos testes da interface para 16 casos. | O arquivo remoto consultado contém quatro métodos de teste. | Conferir suíte local, resultado e correspondência entre testes e funcionalidades. |
| E-03 | Suíte geral com 87 testes aprovados. | Resultado informado em sessão anterior. | Não repetir sem necessidade; confirmar histórico/relatório e se o código testado corresponde ao estado atual. |
| E-04 | Validação manual da interface e das operações de memória. | Validação informada pelo usuário. | Preservar como validação manual relatada; detalhar eventuais lacunas sem exigir repetição desnecessária. |

## 4. Divergência de planejamento e versionamento

O plano original estabelece:
- Fase 3: interface desktop, com memória desabilitada;
- Fase 4: interface web;
- Fase 5: validação integrada, regressão e documentação;
- versão final planejada para o conjunto das fases: `v2.1.0`;
- ativação da memória como evolução posterior, indicada como `v2.2.0`.

A implementação de memória relatada durante a Fase 3 ultrapassa esse escopo. Isso deve ser tratado como **desvio de escopo já ocorrido**, não como alteração retroativa do plano. A decisão sobre manter, reclassificar ou adiar essa funcionalidade e seus efeitos sobre a versão será registrada quando confrontarmos o estado local e os critérios aplicáveis. Nenhuma tag ou release é presumida por este documento.

## 5. Pendências de confirmação

- [ ] Confrontar este registro com o estado local da branch de trabalho.
- [ ] Identificar alterações locais, staged, commits e estado remoto separadamente.
- [ ] Verificar os critérios da Fase 3 no código local, incluindo dimensões, indicação “Em breve” e atalhos.
- [ ] Confirmar implementação e testes de memória sem confundir funcionalidade implementada com escopo aprovado.
- [ ] Fechar a revisão funcional, visual e documental da Fase 3.
- [ ] Atualizar este registro com evidências e decisões antes de iniciar a fase seguinte.

## 6. Histórico de atualizações

### 31/10/2026 — Registro inicial
- Consultada a seção da Fase 3 do plano na branch `desafio-2-revisao-final`.
- Registradas divergências observadas no código e na documentação remotos.
- Registradas separadamente as evoluções locais relatadas em sessões anteriores, ainda sujeitas a confronto com o repositório.
- Definido que os critérios publicados da fase serão a referência de execução, mesmo que o plano geral tenha ficado desatualizado.
