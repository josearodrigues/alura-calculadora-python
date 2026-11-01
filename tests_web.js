/**
 * Suíte de testes do navegador para a Calculadora 2.0.
 * Mantém os casos legados como testes explícitos de compatibilidade
 * e valida os pontos de integração da interface atual.
 */

const relatorioTestes = [];

function registrarResultadoTeste(id, descricao, status, detalhes = "") {
  relatorioTestes.push({
    id,
    descricao,
    status,
    passou: status === "APROVADO",
    detalhes
  });
  console.log(
    \`[TESTE WEB \${status}] \${id}: \${descricao}\${detalhes ? \` (\${detalhes})\` : ""}\`
  );
}

function aguardar(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function exigir(condicao, mensagem) {
  if (!condicao) throw new Error(mensagem);
}

function obterElemento(doc, seletor) {
  const elemento = doc.querySelector(seletor);
  exigir(Boolean(elemento), \`Elemento não encontrado: \${seletor}\`);
  return elemento;
}

/**
 * Cada caso começa com visor/controles neutros e histórico visível vazio.
 * limpar_historico preserva ANS por contrato; nenhum caso desta suíte
 * depende de um valor específico de ANS.
 */
function prepararCaso(app) {
  app.limparCampos();
  const resposta = app.limparHistorico();
  exigir(resposta && resposta.sucesso === true, "Não foi possível preparar o histórico isolado.");
}

async function executarCaso(caso, contexto) {
  try {
    if (caso.preparar !== false) prepararCaso(contexto.app);
    const detalhes = await caso.executar(contexto);
    registrarResultadoTeste(caso.id, caso.descricao, "APROVADO", detalhes || "");
  } catch (erro) {
    registrarResultadoTeste(
      caso.id,
      caso.descricao,
      "FALHOU",
      erro && erro.message ? erro.message : String(erro)
    );
  }
}

function marcarNaoExecutados(casos, inicio, motivo) {
  for (let i = inicio; i < casos.length; i++) {
    registrarResultadoTeste(casos[i].id, casos[i].descricao, "NÃO EXECUTADO", motivo);
  }
}

const casosTeste = [
  {
    id: "TW-01",
    descricao: "Inicialização assíncrona do Pyodide v0.27.8 e status Pronto",
    preparar: false,
    executar: ({ app, doc, pyodideInst }) => {
      const status = obterElemento(doc, "#status-texto");
      const indicador = obterElemento(doc, "#status-indicador");
      exigir(app.pyodidePronto(), "A aplicação não informou que o Pyodide está pronto.");
      exigir(pyodideInst !== null, "Instância do Pyodide não encontrada.");
      exigir(status.textContent.includes("Pronto"), "O status visual não contém Pronto.");
      exigir(indicador.classList.contains("pronto"), "O indicador visual não está pronto.");
      return "Runtime disponível e indicador visual pronto.";
    }
  },
  {
    id: "TW-02",
    descricao: "Presença dos cinco módulos Python no MEMFS",
    executar: ({ pyodideInst }) => {
      const arquivos = [
        "__init__.py",
        "operacoes.py",
        "validacao.py",
        "expressoes.py",
        "historico.py"
      ];
      const stats = arquivos.map(nome => {
        const conteudo = pyodideInst.FS.readFile(
          \`/calculadora/\${nome}\`,
          { encoding: "utf8" }
        );
        const bytes = new Blob([conteudo]).size;
        exigir(bytes > 0, \`O módulo \${nome} está vazio.\`);
        return \`\${nome}: \${bytes} bytes\`;
      });
      return stats.join("; ");
    }
  },
  {
    id: "TW-03",
    descricao: "Compatibilidade legada: adição com vírgula decimal",
    executar: async ({ app, doc }) => {
      const resposta = await app.executarCicloCalculo("12,5", "2,5", "+");
      const valor = obterElemento(doc, "#resultado-valor");
      const icone = obterElemento(doc, "#resultado-icone");
      exigir(resposta.sucesso === true && resposta.resultado === "15", "Resultado legado inesperado.");
      exigir(valor.textContent === "15" && icone.textContent === "✓", "Painel legado não refletiu o resultado.");
    }
  },
  {
    id: "TW-04",
    descricao: "Compatibilidade legada: subtração com resultado negativo",
    executar: async ({ app, doc }) => {
      const resposta = await app.executarCicloCalculo("10", "25", "-");
      exigir(resposta.sucesso === true && resposta.resultado === "-15", "Resultado legado inesperado.");
      exigir(obterElemento(doc, "#resultado-valor").textContent === "-15", "Painel legado não refletiu -15.");
    }
  },
  {
    id: "TW-05",
    descricao: "Compatibilidade legada: multiplicação por zero",
    executar: async ({ app, doc }) => {
      const resposta = await app.executarCicloCalculo("50", "0", "*");
      exigir(resposta.sucesso === true && resposta.resultado === "0", "Resultado legado inesperado.");
      exigir(obterElemento(doc, "#resultado-valor").textContent === "0", "Painel legado não refletiu zero.");
    }
  },
  {
    id: "TW-06",
    descricao: "Compatibilidade legada: divisão com resultado fracionário",
    executar: async ({ app, doc }) => {
      const resposta = await app.executarCicloCalculo("7", "2", "/");
      exigir(resposta.sucesso === true && resposta.resultado === "3.5", "Resultado legado inesperado.");
      exigir(obterElemento(doc, "#resultado-valor").textContent === "3.5", "Painel legado não refletiu 3.5.");
    }
  },
  {
    id: "TW-07",
    descricao: "Compatibilidade legada: tratamento de divisão por zero",
    executar: async ({ app, doc }) => {
      const resposta = await app.executarCicloCalculo("10", "0", "/");
      exigir(resposta.sucesso === false && resposta.tipo_erro === "DivisaoPorZeroError", "Tipo de erro inesperado.");
      exigir(obterElemento(doc, "#resultado-icone").textContent === "✖", "Ícone de erro não exibido.");
      exigir(
        obterElemento(doc, "#resultado-mensagem").textContent.toLowerCase().includes("divisão por zero"),
        "Mensagem de divisão por zero não exibida."
      );
    }
  },
  {
    id: "TW-08",
    descricao: "Compatibilidade legada: rejeição de operando vazio",
    executar: async ({ app, doc }) => {
      const resposta = await app.executarCicloCalculo("", "10", "+");
      exigir(resposta.sucesso === false && resposta.tipo_erro === "ErroValidacao", "Validação do campo vazio não ocorreu.");
      exigir(obterElemento(doc, "#resultado-icone").textContent === "⚠", "Ícone de validação não exibido.");
      exigir(
        obterElemento(doc, "#resultado-mensagem").textContent.includes("Operando A"),
        "Mensagem não identificou o Operando A."
      );
    }
  },
  {
    id: "TW-09",
    descricao: "Compatibilidade legada: rejeição de entrada alfanumérica",
    executar: async ({ app, doc }) => {
      const resposta = await app.executarCicloCalculo("abc", "10", "+");
      exigir(resposta.sucesso === false && resposta.tipo_erro === "ErroValidacao", "Entrada inválida não foi rejeitada.");
      exigir(obterElemento(doc, "#resultado-icone").textContent === "⚠", "Ícone de validação não exibido.");
      exigir(
        obterElemento(doc, "#resultado-mensagem").textContent.includes("não é um número válido"),
        "Mensagem de entrada inválida não exibida."
      );
    }
  },
  {
    id: "TW-10",
    descricao: "Interface atual: limpeza do visor e restauração do estado neutro",
    executar: ({ doc }) => {
      const clicarAcao = acao => {
        const botao = obterElemento(
          doc,
          \`#teclado-calculadora button[data-action="\${acao}"]\`
        );
        exigir(!botao.disabled, \`Ação \${acao} está desabilitada.\`);
        botao.click();
      };

      clicarAcao("7");
      clicarAcao("+");
      clicarAcao("2");
      clicarAcao("equals");

      exigir(obterElemento(doc, "#visor-expressao").textContent === "7+2", "Expressão de teste não foi exibida.");
      exigir(obterElemento(doc, "#visor-resultado").textContent === "9", "Resultado de teste não foi exibido.");

      clicarAcao("clear");

      exigir(obterElemento(doc, "#visor-expressao").textContent === "0", "Visor de expressão não foi limpo.");
      exigir(obterElemento(doc, "#visor-resultado").textContent === "0", "Visor de resultado não voltou a zero.");
      exigir(obterElemento(doc, "#feedback-copiar").textContent === "", "Feedback de cópia não foi limpo.");
      exigir(obterElemento(doc, "#btn-copiar").disabled, "Botão de cópia deveria ficar desabilitado.");
      return "Ação C limpou os dois visores e restaurou os controles.";
    }
  },
  {
    id: "TW-11",
    descricao: "Liberação de proxies: ponte atual e compatibilidade legada, em sucesso e falha",
    executar: async ({ app, pyodideInst }) => {
      // Compatibilidade: mantém a cobertura da ponte legada com provedor injetável.
      let legadoFuncDestruida = false;
      let legadoResultadoDestruido = false;
      const provedorLegado = () => {
        const real = pyodideInst.globals.get("bridge_calcular");
        const funcao = function(a, b, op) {
          const resultado = real(a, b, op);
          return {
            toJs: opcoes => resultado.toJs(opcoes),
            destroy: () => {
              legadoResultadoDestruido = true;
              if (typeof resultado.destroy === "function") resultado.destroy();
            }
          };
        };
        funcao.destroy = () => {
          legadoFuncDestruida = true;
          if (typeof real.destroy === "function") real.destroy();
        };
        return funcao;
      };
      const legadoOk = await app.executarCicloCalculo("5", "5", "+", provedorLegado);
      exigir(
        legadoOk.sucesso && legadoFuncDestruida && legadoResultadoDestruido,
        "A ponte legada não liberou ambos os proxies no fluxo normal."
      );

      let legadoFuncFalhouDestruida = false;
      let legadoResultadoFalhouDestruido = false;
      const provedorLegadoFalha = () => {
        const funcao = () => ({
          toJs: () => { throw new Error("Falha simulada em toJs legado."); },
          destroy: () => { legadoResultadoFalhouDestruido = true; }
        });
        funcao.destroy = () => { legadoFuncFalhouDestruida = true; };
        return funcao;
      };
      const legadoFalha = await app.executarCicloCalculo("1", "1", "+", provedorLegadoFalha);
      exigir(
        !legadoFalha.sucesso && legadoFuncFalhouDestruida && legadoResultadoFalhouDestruido,
        "A ponte legada não liberou ambos os proxies após falha."
      );

      // Ponte atual: valida execução real e inspeciona o bloco finally da função
      // publicada. A inspeção evita monkeypatch frágil do objeto Pyodide.globals.
      const fontePonteAtual = app.executarPontePython.toString();
      exigir(
        fontePonteAtual.includes("finally") &&
        fontePonteAtual.includes("resultadoProxy.destroy") &&
        fontePonteAtual.includes("ponteFuncProxy.destroy"),
        "A implementação atual não apresenta finally com destroy() dos dois proxies."
      );

      const historicoAtual = app.executarPontePython("bridge_obter_historico");
      exigir(Array.isArray(historicoAtual), "A ponte atual não converteu o histórico para array JavaScript.");

      let erroPonteAusenteCapturado = false;
      try {
        app.executarPontePython("ponte_inexistente_para_teste");
      } catch (erro) {
        erroPonteAusenteCapturado = erro.message.includes("não encontrada");
      }
      exigir(
        erroPonteAusenteCapturado,
        "A ponte atual não propagou corretamente a ausência de uma função registrada."
      );
      return "Ponte legada: destroy() observado em sucesso e falha. Ponte atual: finally/destroy inspecionados e sucesso/erro de ausência exercitados."
    }
  }
];

/**
 * Executa os 11 casos isoladamente. Falha de inicialização marca os casos
 * dependentes como NÃO EXECUTADO; exceções individuais não interrompem a suíte.
 */
async function executarTodosOsTestesWeb() {
  relatorioTestes.length = 0;
  console.log("=== INICIANDO SUÍTE WEB (11 CASOS) ===");

  const doc = window.documentContexto || document;
  const app = window.calculadoraApp;
  let tentativas = 0;

  while ((!app || !app.pyodidePronto()) && tentativas < 80) {
    await aguardar(250);
    tentativas++;
  }

  const pyodideInst = app && app.pyodidePronto() ? app.obterPyodide() : null;
  const contexto = { doc, app, pyodideInst };

  if (!app || !pyodideInst) {
    registrarResultadoTeste(
      "TW-01",
      casosTeste[0].descricao,
      "FALHOU",
      "Timeout ou indisponibilidade da aplicação/Pyodide."
    );
    marcarNaoExecutados(casosTeste, 1, "Dependência indisponível após falha de inicialização.");
    return relatorioTestes;
  }

  for (let i = 0; i < casosTeste.length; i++) {
    await executarCaso(casosTeste[i], contexto);
  }

  try {
    app.limparCampos();
    app.limparHistorico();
  } catch (erro) {
    console.error("Falha durante a limpeza final da suíte:", erro);
  }

  return relatorioTestes;
}

window.executarTodosOsTestesWeb = executarTodosOsTestesWeb;
