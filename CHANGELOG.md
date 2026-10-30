# Changelog

Todas as alterações relevantes deste projeto serão registradas neste arquivo.

O formato segue, de maneira simplificada, as convenções do [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/), com versões organizadas cronologicamente.

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
