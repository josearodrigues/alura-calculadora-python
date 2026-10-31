# Changelog

Todas as alterações relevantes deste projeto serão registradas neste arquivo.

O formato segue, de maneira simplificada, as convenções do [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/), com versões organizadas cronologicamente.

## [Não lançado] v2.0.0

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
