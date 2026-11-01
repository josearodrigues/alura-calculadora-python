# Changelog

Todas as alterações relevantes deste projeto serão registradas neste arquivo.

O formato segue, de maneira simplificada, as convenções do [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/), com versões organizadas cronologicamente.

## [Não publicado] — desenvolvimento da v2.1.0

### Adicionado
- Avaliador de expressões matemáticas com parser e árvore sintática própria, sem uso de `eval()`.
- Operações avançadas: potenciação, raiz quadrada, raiz de índice n, valor absoluto, inverso e troca de sinal.
- Percentual isolado e contextual, incluindo percentuais sucessivos em operações aditivas.
- Validação de literais numéricos com limite de 30 dígitos e controle de magnitude de expoente.
- Histórico de sessão em Python, recuperação de entradas anteriores e gestão do resultado anterior por meio de `ANS`.
- Operações de memória na interface desktop (MC, MR, M+, M- e MS), mantidas por decisão aceita durante a revisão.
- Interface desktop Tkinter evoluída, com visor duplo, histórico interativo e atalhos de teclado.
- Interface Web complementar com Pyodide, incluindo histórico, recuperação de resultados, alternância de tema, cópia do resultado e layout responsivo.

### Alterado
- Interface Web: removido o fluxo de compatibilidade legado, preservando a interface atual, a aplicação desktop e o motor Python.
- Suíte Web reescrita para a interface atual; após remoção autorizada do cenário estrutural TW-03, contém 31 cenários.
- Página `testes.html`: cabeçalho reorganizado, tabela ajustada para telas menores e coluna de evidências/detalhes preservada.
- Executor Web: captura os detalhes retornados pelos cenários aprovados, quando disponíveis.
- README atualizado com sintaxe de expressões, exemplos de percentual e raiz de índice n, atalhos por interface e resultados de testes.

### Corrigido
- Inicialização da interface Web após remoção de chamada obsoleta.
- Sintaxe do executor de testes.
- Contagem apresentada na página de testes, atualizada para 31 cenários.

### Validado
- Suíte Python: 92/92 testes aprovados, conforme execução informada pelo usuário em 31/10/2026.
- Suíte Web: 31/31 cenários aprovados, 0 falhas e 0 não executados, conforme resultado informado pelo usuário em 01/11/2026.
- Interface desktop: validação manual confirmada pelo usuário; 21/21 testes direcionados da interface e 92/92 da suíte Python informados como aprovados.
- Interface Web: usuário confirmou funcionamento, exibição de evidências nos cenários que as fornecem e apresentação visual da página de testes em 01/11/2026.
- Auditoria estática da baseline `v2.0.0`: os 25 métodos de teste legados continuam presentes e suas asserções originais foram preservadas. Cinco testes de integração passaram a chamar um método auxiliar renomeado; nenhum teste ou asserção original foi identificado como removido.
- Execução integrada local via `python3 app.py`: confirmada pelo usuário em 01/11/2026. O usuário informou que os testes manuais solicitados (operação básica, expressão com potência ou raiz, histórico e `ANS`) funcionaram. A Fase 5 está concluída no escopo documentado; a `v2.1.0` permanece não publicada.

## [2.0.0] - 2026-10-30

### Adicionado
- Interface web complementar à calculadora desktop utilizando Pyodide v0.27.8 via CDN oficial (sem Vite, sem npm, sem frameworks).
- Reutilização direta do pacote Python da v1.0.0 (`calculadora/__init__.py`, `calculadora/operacoes.py` e `calculadora/validacao.py`) montado no sistema de arquivos virtual do Pyodide (`MEMFS`) via caminhos relativos.
- Função ponte `bridge_calcular` no interpretador Python para despacho seguro e padronizado entre JavaScript e Python.
- Gerenciamento estrito de memória com liberação obrigatória dos proxies `PyProxy` (função ponte e resultado) em blocos `finally`, com suporte a falhas simuladas de conversão.
- Medição de tempo duplo na telemetria: tempo interno de execução da ponte Python (`tempo_interno_ms`) e tempo até atualização do DOM e agendamento do próximo ciclo de renderização (`tempo_ate_atualizacao_dom_ms`).
- Painel de telemetria e logs em caixa de texto recolhida (`<details>` / `<summary>`) na parte inferior da página, com tamanhos dinâmicos de arquivos calculados via `Blob.size`.
- Recursos de acessibilidade visual orientados pelas diretrizes WCAG AA: contraste mínimo de 4.5:1 para texto e 3:1 para controles, agrupamento de radio buttons com `<fieldset>` e `<legend>`, identificação com pares semânticos (ícones + rótulos de texto) e foco visual nítido.
- Suíte automatizada de testes do navegador isolada em `tests_web.js` e executável visualmente em `testes.html`, cobrindo 11 cenários de integração DOM/Pyodide.

### Verificado
- Suíte de 25 testes automatizados `unittest` do Python mantida e aprovada com 100% de sucesso via `python3 -m unittest discover -s tests -v`.
- Disponibilidade da distribuição Pyodide v0.27.8 verificada na CDN jsDelivr (HTTP 200).

### Corrigido
- Ajustado o posicionamento do iframe isolado em `testes.html`, mantendo-o fora da área visível sem impedir o recebimento de foco pelos campos. A alteração corrige a falha do TW-10 na validação da ação de limpeza.

- Adicionado `.nojekyll` à raiz do projeto para evitar que o processamento Jekyll do GitHub Pages exclua arquivos Python cujo nome começa com sublinhado, como `__init__.py`.

### Verificado
- Suíte web reexecutada localmente: 11 testes aprovados.
- Correção do TW-10 validada no GitHub Pages por testes manuais repetidos. Na primeira tentativa foi observado o comportamento anterior, possivelmente devido ao cache; as tentativas seguintes confirmaram a correção.

## v1.0.0

### Adicionado
- Aplicação desktop de calculadora com interface Tkinter.
- Operações de adição, subtração, multiplicação e divisão.
- Validação e conversão dos operandos, com suporte a ponto e vírgula decimal.
- Tratamento específico para entradas inválidas, operações não suportadas e divisão por zero.
- Testes automatizados de operações, validação e integração com `unittest`.
- Documentação da arquitetura, execução, testes e limitações no README.
- Documento de planejamento para uma possível evolução com Pyodide em `docs/`.
- Licença MIT em `LICENSE`, com aviso de copyright usando o nome do projeto, conforme decisão para esta publicação.

### Alterado
- Organização do projeto para manter o escopo da versão inicial exclusivamente em Python/Tkinter.
- Remoção dos arquivos da implementação React/TypeScript e de metadados específicos do Google AI Studio da estrutura destinada ao repositório.

### Verificado
- Suíte automatizada executada em 30/10/2026 com Python 3.13.5: 25 testes aprovados.
- Interface gráfica executada manualmente pelo responsável pelo projeto em ambiente desktop; funcionamento confirmado.
