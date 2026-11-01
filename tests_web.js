/**
 * Suíte de Testes do Navegador para a Calculadora Web Pyodide
 * Valida a integração completa JavaScript <-> Pyodide <-> DOM
 * Garante idempotência e isolamento a cada execução.
 */

const relatorioTestes = [];

function registrarResultadoTeste(id, descricao, passou, detalhes = "") {
  relatorioTestes.push({ id, descricao, passou, detalhes });
  console.log(`[TESTE WEB ${passou ? 'PASSOU ✓' : 'FALHOU ✖'}] ${id}: ${descricao} ${detalhes ? `(${detalhes})` : ''}`);
}

/**
 * Função utilitária para aguardar condição com timeout.
 */
function aguardar(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Executa todos os 11 testes automatizados no navegador com restauração de ambiente garantida.
 */
async function executarTodosOsTestesWeb() {
  relatorioTestes.length = 0;
  console.log("=== INICIANDO SUÍTE DE TESTES DO NAVEGADOR (11 TESTES) ===");

  // Contexto de documento dinâmico (funciona tanto na janela principal quanto via iframe)
  const doc = window.documentContexto || document;
  const app = window.calculadoraApp;

  try {
    // 0. Aguarda até o Pyodide e os módulos estarem 100% inicializados
    let tentativas = 0;
    while ((!app || !app.pyodidePronto()) && tentativas < 80) {
      await aguardar(250);
      tentativas++;
    }

    // Hook de Setup: limpa qualquer resíduo antes de iniciar
    if (app && typeof app.limparCampos === 'function') {
      app.limparCampos();
    }

    const pyodideInst = app ? app.obterPyodide() : null;
    const statusTextoEl = doc.getElementById('status-texto');
    const statusIndicadorEl = doc.getElementById('status-indicador');
    const tw01Passou = app && app.pyodidePronto() &&
                       pyodideInst !== null &&
                       statusTextoEl && statusTextoEl.textContent.includes('Pronto') &&
                       statusIndicadorEl && statusIndicadorEl.classList.contains('pronto');
    registrarResultadoTeste('TW-01', 'Inicialização do Pyodide v0.27.8 e status "Pronto"', tw01Passou);

    if (!tw01Passou) {
      throw new Error("Pyodide ainda não concluiu a inicialização.");
    }

    // TW-02: Existência dos 3 arquivos no MEMFS com tamanho > 0
    let tw02Passou = false;
    let tw02Detalhes = "";
    try {
      const arquivos = ['__init__.py', 'operacoes.py', 'validacao.py'];
      const stats = arquivos.map(nome => {
        const conteudo = pyodideInst.FS.readFile(`/calculadora/${nome}`, { encoding: 'utf8' });
        const bytes = new Blob([conteudo]).size;
        return { nome, bytes };
      });
      tw02Passou = stats.every(s => s.bytes > 0);
      tw02Detalhes = stats.map(s => `${s.nome}: ${s.bytes}b`).join(', ');
    } catch (e) {
      tw02Detalhes = e.message;
    }
    registrarResultadoTeste('TW-02', 'Presença e integridade de __init__.py, operacoes.py e validacao.py no MEMFS', tw02Passou, tw02Detalhes);

    // TW-03: Adição com vírgula ('12,5' + '2,5' = '15')
    const resTW03 = await app.executarCicloCalculo("12,5", "2,5", "+");
    const elValor = doc.getElementById('resultado-valor');
    const elIcone = doc.getElementById('resultado-icone');
    const tw03Passou = resTW03.sucesso === true && resTW03.resultado === "15" && 
                       elValor.textContent === "15" && elIcone.textContent === "✓";
    registrarResultadoTeste('TW-03', 'Adição com vírgula decimal (12,5 + 2,5 -> "15" com ícone ✓)', tw03Passou);

    // TW-04: Subtração com resultado negativo ('10' - '25' = '-15')
    const resTW04 = await app.executarCicloCalculo("10", "25", "-");
    const tw04Passou = resTW04.sucesso === true && resTW04.resultado === "-15" && elValor.textContent === "-15";
    registrarResultadoTeste('TW-04', 'Subtração com resultado negativo (10 - 25 -> "-15")', tw04Passou);

    // TW-05: Multiplicação com zero ('50' * '0' = '0')
    const resTW05 = await app.executarCicloCalculo("50", "0", "*");
    const tw05Passou = resTW05.sucesso === true && resTW05.resultado === "0" && elValor.textContent === "0";
    registrarResultadoTeste('TW-05', 'Multiplicação por zero (50 * 0 -> "0", zero aceito normalmente)', tw05Passou);

    // TW-06: Divisão com resultado decimal ('7' / '2' = '3.5')
    const resTW06 = await app.executarCicloCalculo("7", "2", "/");
    const tw06Passou = resTW06.sucesso === true && resTW06.resultado === "3.5" && elValor.textContent === "3.5";
    registrarResultadoTeste('TW-06', 'Divisão fracionária decimal (7 / 2 -> "3.5")', tw06Passou);

    // TW-07: Divisão por zero ('10' / '0' -> erro com ícone ✖)
    const resTW07 = await app.executarCicloCalculo("10", "0", "/");
    const elMensagem = doc.getElementById('resultado-mensagem');
    const tw07Passou = resTW07.sucesso === false && resTW07.tipo_erro === "DivisaoPorZeroError" &&
                       elIcone.textContent === "✖" && elMensagem.textContent.includes("divisão por zero");
    registrarResultadoTeste('TW-07', 'Guardrail de Divisão por Zero (captura controlada de DivisaoPorZeroError)', tw07Passou);

    // TW-08: Validação de campo vazio (Operando A em branco -> ícone ⚠)
    const resTW08 = await app.executarCicloCalculo("", "10", "+");
    const tw08Passou = resTW08.sucesso === false && resTW08.tipo_erro === "ErroValidacao" &&
                       elIcone.textContent === "⚠" && elMensagem.textContent.includes("Operando A");
    registrarResultadoTeste('TW-08', 'Validação de campo vazio (bloqueio antes da matemática com ErroValidacao)', tw08Passou);

    // TW-09: Validação de entrada inválida com letras ('abc' -> ícone ⚠)
    const resTW09 = await app.executarCicloCalculo("abc", "10", "+");
    const tw09Passou = resTW09.sucesso === false && resTW09.tipo_erro === "ErroValidacao" &&
                       elIcone.textContent === "⚠" && elMensagem.textContent.includes("não é um número válido");
    registrarResultadoTeste('TW-09', 'Validação de entrada alfanumérica inválida ("abc")', tw09Passou);

    // TW-10: Ação de limpeza restaura campos e foco
    const inputA = doc.getElementById('input-op-a');
    const inputB = doc.getElementById('input-op-b');
    inputA.value = "123";
    inputB.value = "456";
    app.limparCampos();
    const tw10Passou = inputA.value === "" && inputB.value === "" && elIcone.textContent === "ℹ" && doc.activeElement === inputA;
    registrarResultadoTeste('TW-10', 'Ação de limpeza esvazia inputs e restaura estado neutro e foco', tw10Passou);

    // TW-11: Liberação de Proxies em dois cenários (Fluxo normal e Falha forçada em toJs)
    let tw11CenarioAPassou = false;
    let tw11CenarioBPassou = false;

    // Cenário A: Execução normal destrói ambos os proxies (função ponte e objeto resultado)
    let funcProxyDestruidoA = false;
    let resProxyDestruidoA = false;

    const provedorEspiaoNormal = () => {
      const realFunc = pyodideInst.globals.get('bridge_calcular');
      const spyFunc = function(a, b, op) {
        const realRes = realFunc(a, b, op);
        return {
          toJs: (opts) => realRes.toJs(opts),
          destroy: () => {
            resProxyDestruidoA = true;
            if (typeof realRes.destroy === 'function') realRes.destroy();
          }
        };
      };
      spyFunc.destroy = () => {
        funcProxyDestruidoA = true;
        if (typeof realFunc.destroy === 'function') realFunc.destroy();
      };
      return spyFunc;
    };

    const resA = await app.executarCicloCalculo("5", "5", "+", provedorEspiaoNormal);
    tw11CenarioAPassou = funcProxyDestruidoA === true && resProxyDestruidoA === true && resA.sucesso === true;

    // Cenário B: Falha forçada em toJs() comprova que o bloco finally destrói ambos os proxies
    let mockPonteDestruidoB = false;
    let mockResDestruidoB = false;

    const provedorMockFalha = () => {
      const mockFunc = function(a, b, op) {
        return {
          toJs: () => {
            throw new Error("Erro simulado durante toJs() para teste do bloco finally");
          },
          destroy: () => {
            mockResDestruidoB = true;
          }
        };
      };
      mockFunc.destroy = () => {
        mockPonteDestruidoB = true;
      };
      return mockFunc;
    };

    const resB = await app.executarCicloCalculo("1", "1", "+", provedorMockFalha);
    tw11CenarioBPassou = mockPonteDestruidoB === true && mockResDestruidoB === true && resB.sucesso === false;

    const tw11Passou = tw11CenarioAPassou && tw11CenarioBPassou;
    registrarResultadoTeste(
      'TW-11',
      'Gerenciamento de memória: liberação de proxies no fluxo normal e em falha de toJs()',
      tw11Passou,
      `Cenário A (Normal): ${tw11CenarioAPassou ? 'OK' : 'FALHA'}, Cenário B (Mock toJs falhou): ${tw11CenarioBPassou ? 'OK' : 'FALHA'}`
    );

  } catch (erroGeral) {
    console.error("Erro fatal durante a execução dos testes web:", erroGeral);
  } finally {
    // Teardown Global: Garante que o ambiente volte 100% ao estado limpo e original
    if (app && typeof app.limparCampos === 'function') {
      app.limparCampos();
    }
  }

  return relatorioTestes;
}

window.executarTodosOsTestesWeb = executarTodosOsTestesWeb;
