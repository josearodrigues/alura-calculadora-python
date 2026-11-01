# Registro de Divergências e Evolução do Escopo

**Projeto:** Calculadora Python — Desafio 2  
**Repositório:** `josearodrigues/alura-calculadora-python`  
**Branch de referência:** `desafio-2-revisao-final`  
**Criado em:** 31/10/2026  
**Última atualização:** 01/11/2026

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

## 3. Estado observado no código e nos testes

Base da conferência: arquivos da branch `desafio-2-revisao-final` e resultados de execução informados pelo usuário em 31/10/2026.

| ID | Comportamento | Evidência observada | Situação |
|---|---|---|---|
| C-01 | Dimensões da janela | `calculadora/interface.py`: `geometry("740x580")` e `minsize(700, 540)`. | Adaptação A-01 aceita |
| C-02 | Tema e visor | Tema `#0D1B2A`, expressão em cinza claro e resultado em ciano `#22D3EE`. | Implementado |
| C-03 | Teclado e raiz enésima | Teclado completo; `_aplicar_raiz_n()` insere `root(` ou `root(valor; ` após resultado. | Implementado e coberto por teste direcionado |
| C-04 | Recuperação do histórico | `_recuperar_historico_por_id()` restaura expressão/resultado e o modelo atualiza ANS para o valor recuperado. | Implementado e coberto por teste direcionado |
| C-05 | Continuidade após recuperação | O operador utiliza o resultado recuperado quando o estado de resultado calculado está ativo. | Implementado e coberto por teste direcionado |
| C-06 | Limpeza do histórico | A limpeza remove os registros e preserva o valor de ANS. | Implementado e coberto por teste direcionado |
| C-07 | Memória | Os cinco botões são funcionais e possuem métodos correspondentes. | Adaptação A-02 aceita |
| C-08 | Atalhos físicos | O tratamento de teclado encaminha dígitos, operadores, parênteses, Enter, Backspace, Escape/Delete e Ctrl+C. | Implementado e coberto por teste de encaminhamento dos atalhos |
| C-09 | Testes de interface | `tests/test_interface_desktop.py` contém 21 métodos de teste. | 21 testes de interface aprovados |

## 4. Evoluções além do escopo originalmente previsto

| ID | Evolução | Relação com o plano | Situação |
|---|---|---|---|
| E-01 | Operações de memória MC, MR, M+, M- e MS. | O plano previa os botões desabilitados na Fase 3 e a memória em evolução posterior. | Implementadas e mantidas por decisão do usuário. |
| E-02 | Ampliação dos testes da interface de 16 para 21 métodos. | Amplia a cobertura da Fase 3. | 21/21 testes aprovados. |
| E-03 | Ampliação da suíte completa de 87 para 92 testes. | Amplia a cobertura de regressão. | 92/92 testes aprovados. |
| E-04 | Validação manual da interface desktop pelo usuário. | Validação funcional da GUI. | Confirmada pelo usuário. |

## 5. Validações realizadas e pendências documentais da Fase 3

Testes direcionados acrescentados e executados:

- [x] Teste do template de raiz enésima, com e sem resultado anterior.
- [x] Teste de recuperação do histórico e atualização do ANS.
- [x] Teste de continuidade após recuperação.
- [x] Teste de limpeza do histórico preservando ANS.
- [x] Teste de encaminhamento dos atalhos físicos.
- [x] Execução dos testes da interface: 21/21 aprovados.
- [x] Execução da suíte completa: 92/92 aprovados.
- [x] Atualizar `docs/ESTADO-ATUAL.md` com a situação final da Fase 3.
- [x] Concluir a revisão documental, confrontando o plano original, as adaptações aceitas, a implementação registrada e os resultados dos testes.

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

### 31/10/2026 — Atualização da validação da Fase 3
- Registrados os cinco testes direcionados adicionados à interface desktop.
- Atualizada a cobertura da interface de 16 para 21 métodos, com resultado de 21/21 aprovados.
- Atualizada a suíte completa de 87 para 92 testes, com resultado de 92/92 aprovados.
- Registrada a confirmação do usuário sobre a validação manual da interface desktop.
- Na atualização final de 31/10/2026, foram concluídos `docs/ESTADO-ATUAL.md` e a revisão documental da Fase 3.
- A Fase 3 foi encerrada. As Fases 4 e 5 permanecem pendentes conforme o plano original.

## 8. Fase 4 — Evolução da interface Web e revisão do escopo

A Fase 4 foi implementada na branch `desafio-2-revisao-final`. Durante a revisão da interface, identificou-se que o fluxo de compatibilidade da interface Web da baseline não fazia mais parte da experiência atual e permanecia distribuído entre HTML, JavaScript, CSS e testes.

Por decisão expressa do usuário, foi removido esse fluxo legado, preservando a interface Web atual, a aplicação desktop Tkinter e o motor Python. A baseline publicada `v2.0.0` não foi reescrita nem substituída.

### 8.1 Decisão de escopo

| ID | Decisão | Motivo e limite |
|---|---|---|
| W-01 | Remover a seção de compatibilidade legada de `index.html`, a ponte e eventos exclusivos em `app.js`, e a regra CSS correspondente. | Eliminar o fluxo antigo que não integra a interface Web atual. |
| W-02 | Reescrever `tests_web.js` para cobrir a interface atual e a integração com Pyodide. | Manter a suíte alinhada à aplicação efetivamente apresentada. |
| W-03 | Remover o cenário estrutural TW-03 após avaliação com o usuário. | O teste verificava apenas a ausência de elementos legados; sua remoção foi autorizada. |
| W-04 | Restaurar a captura dos detalhes retornados pelos cenários aprovados. | Preservar evidências úteis na coluna “Evidências / Detalhes”, sem forçar conteúdo em todos os testes. |
| W-05 | Ajustar o cabeçalho e a apresentação responsiva da página `testes.html`. | Recuperar alinhamento visual e legibilidade da tabela de testes. |

O plano original não foi alterado. Estas decisões registram uma adaptação do escopo executado e preservam a rastreabilidade em relação aos requisitos inicialmente planejados.

### 8.2 Arquivos afetados e commits

| Commit | Arquivos | Alteração |
|---|---|---|
| `3711a5e` | `app.js`, `index.html`, `tests_web.js`, `testes.html`, `style.css` | Remoção do fluxo legado e reescrita da suíte Web para 32 cenários. |
| `106bb55` | `app.js`, `testes.html` | Correção da inicialização da interface atual e da sintaxe do executor. |
| `1b896ce` | `tests_web.js` | Remoção autorizada do cenário estrutural TW-03. |
| `dcc96af` | `testes.html` | Atualização da indicação fixa para 31 cenários. |
| `c9f4ee7` | `tests_web.js` | Restauração da captura e apresentação de detalhes de cenários aprovados. |
| `9ca9d1a` | `testes.html` | Ajuste do cabeçalho, largura do cartão e comportamento responsivo da tabela. |

### 8.3 Validação confirmada pelo usuário

Em 01/11/2026, após sincronizar a branch com `git pull`, o usuário confirmou:
- A suíte Web executa e funciona após a remoção do legado.
- A coluna “Evidências / Detalhes” voltou a exibir informações nos cenários que retornam detalhes; os demais podem apresentar `-`.
- O cabeçalho e o layout da página de testes foram aprovados visualmente.
- A tabela e sua última coluna estão visíveis na apresentação testada.

Na execução confirmada em 01/11/2026, a página apresentou **31/31 aprovados, 0 falhas e 0 não executados (100% OK)**. O usuário também confirmou o funcionamento da suíte, a exibição das evidências e a apresentação visual da página.

## 9. Histórico de atualização da Fase 4

### 01/11/2026 — Remoção do legado e revisão da suíte
- Removido o fluxo de compatibilidade legado da interface Web.
- Reescrita a suíte para a interface atual; após a remoção autorizada do TW-03, a suíte passou a conter 31 cenários.
- Corrigidas falhas introduzidas na inicialização e no executor de testes.
- Restaurada a captura de evidências positivas nos cenários que retornam detalhes.
- Ajustado o cabeçalho da página de testes.
- Usuário confirmou funcionamento da suíte, apresentação das evidências e aprovação visual do layout.
- A Fase 4 fica registrada como implementada e validada pelo usuário no escopo executado. A validação integrada e a regressão final permanecem na Fase 5.


## 10. Registro intermediário da Fase 5 — 01/11/2026

> Registro histórico anterior à confirmação final do usuário. A situação vigente está registrada na seção 8.

### Resultados confirmados
- Suíte Python: 92/92 aprovados, conforme execução informada pelo usuário em 31/10/2026.
- Suíte Web: 31/31 aprovados, 0 falhas e 0 não executados, conforme resultado exibido em 01/11/2026.
- Comparação dos testes da baseline `v2.0.0`: os 25 métodos legados foram preservados e nenhuma asserção original foi identificada como removida. A análise distinguiu mudanças de chamada auxiliar e comentários de alterações efetivas nas verificações.
- README e CHANGELOG foram atualizados para descrever a evolução da calculadora e os resultados das suítes.

### Pendência
Naquele momento, a execução integrada local via `python3 app.py` ainda não havia sido confirmada. A confirmação posterior encerrou essa pendência, conforme seção 8. A versão `v2.1.0` permanece não publicada.


## 8. Validação integrada local — Fase 5 (01/11/2026)

O usuário confirmou a execução local da aplicação Web iniciada por `python3 app.py` e informou que todos os testes manuais solicitados funcionaram:

- Operação aritmética básica.
- Expressão envolvendo potência ou raiz.
- Consulta e utilização do histórico.
- Continuidade de cálculo com `ANS`.

Este registro documenta a confirmação do usuário; não afirma que o assistente executou os testes no ambiente local. Em conjunto com os resultados informados das suítes Python (92/92) e Web (31/31) e a comparação da baseline, a validação integrada prevista na Fase 5 está concluída no escopo documentado. A versão `v2.1.0` continua não publicada.


## 11. Coexistência das versões — 01/11/2026

### Decisão de organização

A branch de trabalho mantém duas árvores de aplicação independentes:

- **v2.0.0:** arquivos da aplicação preservados na raiz, correspondentes à baseline publicada.
- **v2.1.0:** aplicação evoluída organizada em `v2.1.0/`, incluindo módulos Python, interfaces e suítes de testes próprias.

A documentação e os recursos comuns permanecem na raiz: `docs/`, `README.md`, `CHANGELOG.md`, `LICENSE`, `.gitignore` e `.nojekyll`. Não foram duplicados dentro de `v2.1.0/`.

### Critérios de separação

- As referências relativas de cada interface Web devem resolver arquivos dentro do diretório da própria versão.
- Os testes Python devem ser executados a partir do diretório da versão correspondente, evitando importar o pacote da outra versão.
- A raiz deve continuar servindo a v2.0.0; a rota `/v2.1.0/` deve servir a evolução.
- A presença dos arquivos na branch não equivale à publicação nem à criação de uma release.

### Verificações documentais realizadas no GitHub

Em 01/11/2026, a branch `desafio-2-revisao-final` foi consultada diretamente. Foram localizados os arquivos de aplicação em `v2.1.0/` e os arquivos da aplicação da baseline na raiz. Os documentos compartilhados foram revisados para refletir essa organização.

A compatibilidade dos caminhos relativos foi inspecionada nos arquivos HTML e JavaScript. Isso é uma verificação estática; não substitui a validação efetiva da publicação no GitHub Pages. A configuração de publicação e a rota pública da v2.1.0 permanecem sujeitas a validação antes do merge na `main`.

### Limites

Esta decisão organiza as duas versões na branch de trabalho sem alterar os requisitos históricos do plano original. O arquivo `docs/calculadora-2.0-plano.md` permanece preservado.
