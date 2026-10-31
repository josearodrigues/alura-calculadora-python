# Implementação de Interface Web Complementar via Pyodide (HTML + CSS + JS Vanilla)

Implementação de uma **interface web complementar à calculadora desktop**, reutilizando a lógica Python existente da versão `v1.0.0` por meio do **Pyodide (WebAssembly CPython)** carregado via CDN oficial, **sem Vite, sem npm e sem empacotadores**.

A aplicação desktop original com Tkinter permanece **intacta e plenamente funcional**, enquanto os módulos **`calculadora/__init__.py`**, **`calculadora/operacoes.py`** e **`calculadora/validacao.py`** são reaproveitados de maneira idêntica no navegador, comprovando a eficácia do desacoplamento arquitetural.

---

## 1. Escolha e Fixação da Versão do Pyodide

> [!NOTE]
> **Versão Fixada:** `v0.27.8`
> - Script: `https://cdn.jsdelivr.net/pyodide/v0.27.8/full/pyodide.js`
> - `indexURL`: `https://cdn.jsdelivr.net/pyodide/v0.27.8/full/`
>
> **Justificativa Técnica:**
> - A versão `v0.27.8` foi a fixada da linha `0.27` para esta implementação, trazendo todas as correções acumuladas.
> - Baseia-se no CPython 3.12 com suporte maduro a chamadas FFI bidirecionais e ao sistema de arquivos virtual Emscripten (`MEMFS`).
> - Mantém determinismo na destruição explícita de objetos `PyProxy` e ampla compatibilidade entre navegadores sem depender de recursos experimentais.

---

## 2. Princípios e Diretrizes de Engenharia

1. **Reutilização Estrita e Não Duplicação:** Toda a validação e toda a aritmética residem exclusivamente nos arquivos Python da pasta `calculadora/`. O JavaScript atua estritamente como adaptador de interface (I/O, manipulação do DOM e despacho de eventos).
2. **Conferência Rigorosa das Assinaturas Existentes:**
   - `converter_operando(valor_bruto: str, nome_campo: str = "Operando") -> float` em `validacao.py`.
   - `calcular(a: float, b: float, operacao: str) -> float` em `operacoes.py`.
   - `formatar_resultado(valor: float, precisao_maxima: int = 8) -> str` em `operacoes.py`.
   - Exceções de Domínio: `ErroValidacao` (`validacao.py`), `DivisaoPorZeroError` e `OperacaoInvalidaError` (`operacoes.py`).
3. **Gerenciamento Estrito de Memória (`PyProxy`):**
   - Tanto o proxy da função ponte (`ponteFuncProxy`) quanto o proxy do resultado retornado (`resultadoProxy`) devem ser **obrigatoriamente liberados com `.destroy()`** dentro de blocos `finally`.
   - A liberação deve ocorrer tanto na execução normal quanto em cenários onde a conversão via `toJs()` falhar ou lançar exceção.
4. **Sincronização de Execução e Ciclo de Renderização:**
   - A função `executarCicloCalculo()` retornará uma `Promise` que **só será resolvida após a execução do callback de `requestAnimationFrame`**, garantindo que testes automatizados que aguardam a Promise encontrem a interface e a telemetria 100% atualizadas.
   - Conceituação precisa da métrica: `tempo_ate_atualizacao_dom_ms` mede o tempo transcorrido até a atualização do DOM e o agendamento do próximo ciclo de renderização do navegador (execução do callback antes da pintura), sem afirmar medição de pintura de pixels na tela.
5. **Isolamento Estrito de Diagnósticos de Erros:**
   - **Interface do Usuário:** Exibe mensagens amigáveis em erros de domínio ou mensagem neutra e segura em falhas não mapeadas (*"Ocorreu um erro interno inesperado no processamento."*).
   - **Telemetria (`<textarea>` na tela):** Registra que um erro ocorreu com o identificador da exceção, **sem expor o traceback**.
   - **Console de Desenvolvimento (`console.error`):** Local exclusivo onde *tracebacks* Python e detalhes de exceções do JavaScript (`tratarErroInesperadoJs`) são emitidos para diagnóstico técnico.
6. **Acessibilidade Holística e Semântica (WCAG AA):**
   - Contraste de texto $\ge 4.5:1$ (texto normal sobre fundo).
   - Contraste de componentes gráficos e controles de interface $\ge 3:1$ (bordas de inputs, botões, indicadores de foco).
   - Radio buttons agrupados semanticamente com `<fieldset>` e `<legend>`, além de `<label for="...">` individual para cada opção.
   - Identificação com múltiplos recursos: ícones (`✓`, `⚠`, `✖`, `ℹ`) acompanhados de rótulos textuais visíveis.
   - Navegação por teclado (`Tab`, `Shift+Tab`), tecla `Enter` para calcular e `Esc` para limpar.
   - Foco visual nítido (`:focus-visible: 2px solid #2563EB`) e anúncios para leitores de tela com `aria-live="polite"` e `role="alert"`.
7. **Medição Exata de Bytes:**
   - A medição de tamanho dos arquivos Python carregados utilizará `new TextEncoder().encode(conteudoTexto).length` ou `new Blob([conteudoTexto]).size`, garantindo o cálculo real de bytes e evitando imprecisões de `String.length` com caracteres multibyte.
8. **Governança do `CHANGELOG.md`:**
   - Preservar a seção `## v1.0.0`.
   - Manter a seção `## [Não lançado] v2.0.0` registrando exclusivamente funcionalidades **efetivamente implementadas e verificadas por testes**, e não etapas previstas.
   - A promoção para `## v2.0.0` ocorre apenas após a validação completa de todas as fases.

---

## 3. Contrato Padronizado da Ponte Python $\leftrightarrow$ JavaScript

A ponte será implementada em Python e registrada no escopo global do Pyodide como `bridge_calcular(a_str: str, b_str: str, op_str: str) -> dict`.

### A. Assinatura do Dicionário de Retorno

```python
{
    "sucesso": bool,               # True para cálculo bem-sucedido; False para erro
    "resultado": Optional[str],    # String formatada (ex.: "15") se sucesso; None se erro
    "tipo_erro": Optional[str],    # Nome da classe do erro ("ErroValidacao", "DivisaoPorZeroError", "ErroInesperado") ou None
    "mensagem": Optional[str],     # Mensagem amigável para a interface visual ou None
    "detalhes": Optional[str],     # Traceback completo para console.error em caso de erro inesperado; SEMPRE None em erros de domínio
    "tempo_interno_ms": float,     # Duração interna da execução da ponte Python em milissegundos
    "logs": list[str]              # Rastreamento detalhado das etapas efetivamente executadas pela ponte
}
```

---

## 4. Gerenciamento Seguro de Proxies e Sincronização com `requestAnimationFrame`

Padrão corrigido em `app.js` assegurando resolução síncrona com os testes e destruição de proxies:

```javascript
function executarCicloCalculo(operandoA, operandoB, operacao) {
  return new Promise((resolve) => {
    const tInicio = performance.now();
    let ponteFuncProxy = null;
    let resultadoProxy = null;
    let resposta = null;

    try {
      // 1. Obtém o proxy da função ponte
      ponteFuncProxy = pyodide.globals.get('bridge_calcular');
      if (!ponteFuncProxy) {
        throw new Error("Ponte Python 'bridge_calcular' não encontrada.");
      }

      // 2. Invoca a função Python no WebAssembly
      resultadoProxy = ponteFuncProxy(operandoA, operandoB, operacao);

      // 3. Converte o dicionário Python para objeto JavaScript puro
      resposta = resultadoProxy.toJs({ dict_converter: Object.fromEntries });

      // 4. Atualiza o DOM (Interface e Acessibilidade)
      atualizarInterfaceResultado(resposta);

    } catch (erroJs) {
      resposta = tratarErroInesperadoJs(erroJs, tInicio);
    } finally {
      // 5. LIBERAÇÃO OBRIGATÓRIA DE AMBOS OS PROXIES EM QUALQUER CENÁRIO
      // Ocorre mesmo se toJs() lançar exceção
      if (resultadoProxy && typeof resultadoProxy.destroy === 'function') {
        try { resultadoProxy.destroy(); } catch (e) { /* silencia limpeza */ }
      }
      if (ponteFuncProxy && typeof ponteFuncProxy.destroy === 'function') {
        try { ponteFuncProxy.destroy(); } catch (e) { /* silencia limpeza */ }
      }
    }

    // 6. Sincronização via requestAnimationFrame: a Promise resolve após o callback
    requestAnimationFrame(() => {
      try {
        const tAposAtualizacao = performance.now();
        resposta.tempo_ate_atualizacao_dom_ms = Number((tAposAtualizacao - tInicio).toFixed(2));

        // Atualiza a telemetria na página (sem expor tracebacks)
        registrarTelemetriaCalculo(resposta);

        // Se houver traceback de erro inesperado, emite exclusivamente no console
        if (resposta.detalhes) {
          console.error("[Diagnóstico Pyodide] Traceback de erro inesperado:\n" + resposta.detalhes);
        }
      } catch (erroRaf) {
        console.error("Erro interno ao processar telemetria no requestAnimationFrame:", erroRaf);
      } finally {
        // Resolve a Promise garantindo que a interface e a telemetria já foram processadas
        resolve(resposta);
      }
    });
  });
}

function tratarErroInesperadoJs(erroJs, tInicio) {
  console.error("[Diagnóstico JS] Exceção inesperada na camada JavaScript:", erroJs);
  const respostaErro = {
    sucesso: false,
    resultado: null,
    tipo_erro: "ErroInesperadoJS",
    mensagem: "Ocorreu um erro interno inesperado no processamento.",
    detalhes: erroJs && erroJs.stack ? erroJs.stack : String(erroJs),
    tempo_interno_ms: 0.0,
    logs: ["Falha na camada de integração JavaScript"]
  };
  atualizarInterfaceResultado(respostaErro);
  return respostaErro;
}
```

---

## 5. Estrutura Acessível do Formulário (HTML Semântico)

A marcação HTML do formulário estruturará os controles de operação utilizando `<fieldset>` e `<legend>`:

```html
<fieldset class="campo-operacao-grupo">
  <legend class="campo-legenda">Operação Desejada</legend>
  <div class="opcoes-operacao">
    <label for="op-soma" class="opcao-radio">
      <input type="radio" id="op-soma" name="operacao" value="+" checked>
      <span>Adição (+)</span>
    </label>
    <label for="op-subtracao" class="opcao-radio">
      <input type="radio" id="op-subtracao" name="operacao" value="-">
      <span>Subtração (-)</span>
    </label>
    <label for="op-multiplicacao" class="opcao-radio">
      <input type="radio" id="op-multiplicacao" name="operacao" value="*">
      <span>Multiplicação (×)</span>
    </label>
    <label for="op-divisao" class="opcao-radio">
      <input type="radio" id="op-divisao" name="operacao" value="/">
      <span>Divisão (÷)</span>
    </label>
  </div>
</fieldset>
```

---

## 6. Arquitetura da Suíte de Testes do Navegador (`tests_web.js`)

A suíte de testes do navegador é implementada em arquivo independente (`tests_web.js`) e pode ser executada por meio de uma página dedicada (`testes.html`):

### Casos de Teste Web (11 Testes):
- **TW-01:** Runtime Pyodide v0.27.8 carregado e status igual a "Pronto".
- **TW-02:** Existência e integridade dos 3 arquivos no MEMFS (`__init__.py`, `operacoes.py`, `validacao.py`) com medição correta de bytes via `Blob.size`.
- **TW-03:** Adição com vírgula (`"12,5"` $+$ `"2,5"` $\to$ `"15"` com ícone `✓`).
- **TW-04:** Subtração com resultado negativo (`"10"` $-$ `"25"` $\to$ `"-15"` com ícone `✓`).
- **TW-05:** Multiplicação com zero (`"50"` $\times$ `"0"` $\to$ `"0"` sem confundir com vazio).
- **TW-06:** Divisão com resultado decimal (`"7"` $\div$ `"2"` $\to$ `"3.5"`).
- **TW-07:** Divisão por zero (`"10"` $\div$ `"0"` $\to$ erro com ícone `✖` e mensagem esperada).
- **TW-08:** Validação de campo vazio (Operando A em branco $\to$ ícone `⚠` e mensagem específica).
- **TW-09:** Validação de entrada inválida (`"abc"` $\to$ ícone `⚠`).
- **TW-10:** Ação de limpeza: verifica se os campos são esvaziados, o estado visual retorna à condição neutra e o foco retorna ao campo Operando A.
  - **Observação de implementação:** o iframe utilizado pelo executor dos testes deve permanecer fora da área visível, mas conservar dimensões não nulas e capacidade de receber foco. O uso de `visibility: hidden` ou dimensões zero impediu a validação confiável do foco no TW-10.
- **TW-11:** **Liberação de Proxies em Dois Cenários:**
  - *Cenário A (Execução normal):* Verifica que tanto o proxy da função quanto o proxy do resultado chamam `.destroy()` e não permanecem ativos na memória.
  - *Cenário B (Falha provocada em `toJs` via mock):* Utiliza um proxy mock cujo método `toJs()` lança um erro simulado e comprova que o bloco `finally` continua chamando `.destroy()` em ambos os proxies, prevenindo vazamentos de memória.

---

## 7. Roteiro Incremental de Implementação

Seguiremos rigorosamente a execução incremental:

### Fase 1: Carregamento do Runtime Pyodide v0.27.8
- Implementar `index.html`, `style.css` e carregamento de Pyodide v0.27.8 via CDN.
- *Evidência de Funcionamento:* Indicador visual passa para "Pronto" e console confirma inicialização sem erros.

### Fase 2: Montagem dos Módulos Python com Caminhos Relativos
- Ler `./calculadora/__init__.py`, `./calculadora/operacoes.py` e `./calculadora/validacao.py`.
- Medir os bytes reais com `new Blob([conteudoTexto]).size`, gravar no `MEMFS` e testar `import calculadora`.
- *Evidência de Funcionamento:* Importação e asserção de sanidade executada no WebAssembly com sucesso.

### Fase 3: Implementação da Ponte Python $\leftrightarrow$ JavaScript
- Registrar `bridge_calcular` no interpretador.
- Implementar `executarCicloCalculo()` com retorno de `Promise`, `requestAnimationFrame`, conversão `toJs()` e liberação segura de proxies no `finally`.
- *Evidência de Funcionamento:* Chamada direta da ponte via console com retorno do dicionário padronizado.

### Fase 4: Interface Acessível e Telemetria Recolhida
- Construir a interface com formulário semântico (`<fieldset>`, `<legend>`, `<label>`), pares semânticos (ícone + texto) e caixa de telemetria colapsável.
- Ligar eventos de cálculo e atalhos (`Enter`/`Esc`).
- *Evidência de Funcionamento:* Cálculos interativos funcionando com telemetria preenchida sem exibir tracebacks na tela.

### Fase 5: Implementação e Execução da Suíte Web (`tests_web.js`)
- Criar `tests_web.js` e página `testes.html`.
- Executar os 11 testes web automatizados, incluindo o teste de dois cenários do TW-11.
- *Evidência de Funcionamento:* 11 testes web aprovados com 100% de sucesso.

### Fase 6: Validação Independente dos Testes Desktop
- Executar a suíte de testes Python no terminal: `python3 -m unittest discover -s tests -v`.
- *Evidência de Funcionamento:* 25 testes unitários e de integração Python aprovados com 100% de sucesso.

### Fase 7: Governança do `CHANGELOG.md` e Documentação
- Atualizar `CHANGELOG.md` adicionando a seção `## [Não lançado] v2.0.0` com as entregas efetivamente implementadas e validadas.
- Atualizar o `README.md` documentando a interface web complementar e a execução via `python3 -m http.server 3000 --bind 127.0.0.1`.
- Salvar cópia do plano aprovado em `docs/implementation_plan.md`.

### Fase 8: Consolidação e Promoção para `v2.0.0`
- Confirmar o funcionamento conjunto das duas interfaces (Desktop Tkinter e Web Pyodide).
- Converter a seção `## [Não lançado] v2.0.0` para `## v2.0.0` no `CHANGELOG.md` com data e escopo formalizados.
