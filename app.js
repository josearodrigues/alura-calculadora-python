/**
 * Calculadora Python Web (Pyodide WebAssembly)
 * Orquestração JavaScript, montagem do MEMFS e ponte de comunicação
 */

let pyodide = null;
let inicializacaoConcluida = false;

// Elementos do DOM
const dom = {
  statusIndicador: document.getElementById('status-indicador'),
  statusTexto: document.getElementById('status-texto'),
  inputOpA: document.getElementById('input-op-a'),
  inputOpB: document.getElementById('input-op-b'),
  btnCalcular: document.getElementById('btn-calcular'),
  btnLimpar: document.getElementById('btn-limpar'),
  painelResultado: document.getElementById('painel-resultado'),
  resultadoIcone: document.getElementById('resultado-icone'),
  resultadoRotulo: document.getElementById('resultado-rotulo'),
  resultadoValor: document.getElementById('resultado-valor'),
  resultadoMensagem: document.getElementById('resultado-mensagem'),
  telemetriaLog: document.getElementById('telemetria-log'),
};

/**
 * Registra um evento na caixa de telemetria da página (sem tracebacks).
 */
function logTelemetria(categoria, mensagem) {
  const agora = new Date().toISOString();
  const linha = `[${agora}] [${categoria}] ${mensagem}\n`;
  if (dom.telemetriaLog) {
    dom.telemetriaLog.value += linha;
    dom.telemetriaLog.scrollTop = dom.telemetriaLog.scrollHeight;
  }
}

/**
 * Atualiza o painel de status do carregamento.
 */
function atualizarStatus(texto, pronto = false) {
  if (dom.statusTexto) dom.statusTexto.textContent = texto;
  if (dom.statusIndicador) {
    if (pronto) {
      dom.statusIndicador.classList.add('pronto');
    } else {
      dom.statusIndicador.classList.remove('pronto');
    }
  }
}

/**
 * Habilita ou desabilita os controles da interface.
 */
function definirControlesHabilitados(habilitado) {
  if (dom.inputOpA) dom.inputOpA.disabled = !habilitado;
  if (dom.inputOpB) dom.inputOpB.disabled = !habilitado;
  if (dom.btnCalcular) dom.btnCalcular.disabled = !habilitado;
  if (dom.btnLimpar) dom.btnLimpar.disabled = !habilitado;
  document.querySelectorAll('input[name="operacao"]').forEach(r => {
    r.disabled = !habilitado;
  });
}

/**
 * Fase 1 & 2: Carrega o Pyodide e monta os módulos Python no MEMFS.
 */
async function inicializarPyodideEModulos() {
  try {
    logTelemetria('SISTEMA:INIT', 'Iniciando carregamento do Pyodide v0.27.8 via CDN...');
    atualizarStatus('Baixando runtime WebAssembly...');

    pyodide = await loadPyodide({
      indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.27.8/full/'
    });

    logTelemetria('SISTEMA:PRONTO', 'Runtime Pyodide WebAssembly inicializado com sucesso.');
    atualizarStatus('Montando módulos Python...');

    // Cria o diretório do pacote no sistema de arquivos virtual do Pyodide
    if (!pyodide.FS.analyzePath('/calculadora').exists) {
      pyodide.FS.mkdirTree('/calculadora');
    }

    // Carrega os 3 arquivos do pacote via caminhos relativos
    const arquivosParaCarregar = [
      { nome: '__init__.py', caminho: './calculadora/__init__.py' },
      { nome: 'operacoes.py', caminho: './calculadora/operacoes.py' },
      { nome: 'validacao.py', caminho: './calculadora/validacao.py' },
    ];

    for (const arq of arquivosParaCarregar) {
      const resp = await fetch(arq.caminho);
      if (!resp.ok) {
        throw new Error(`Falha ao obter ${arq.caminho}: HTTP ${resp.status}`);
      }
      const conteudo = await resp.text();
      // Mede o tamanho real em bytes com Blob.size (evitando divergências de multibyte)
      const tamanhoBytes = new Blob([conteudo]).size;

      pyodide.FS.writeFile(`/calculadora/${arq.nome}`, conteudo);
      logTelemetria('FS:MONTADO', `Arquivo ./calculadora/${arq.nome} carregado (${tamanhoBytes} bytes).`);
    }

    // Registra o caminho no sys.path do Python e testa a importação canônica
    pyodide.runPython(`
import sys
if '/' not in sys.path:
    sys.path.insert(0, '/')

import calculadora
from calculadora import operacoes, validacao
`);
    logTelemetria('PYTHON:IMPORT', "Pacote 'calculadora' importado e verificado com sucesso.");

    // Fase 3: Registra a função ponte Python com tratamento de erros e logs
    registrarPontePython();

    atualizarStatus('Pronto (Pyodide v0.27.8)', true);
    inicializacaoConcluida = true;
    definirControlesHabilitados(true);
    if (dom.inputOpA) dom.inputOpA.focus();

  } catch (erro) {
    console.error('[Diagnóstico Inicialização]', erro);
    logTelemetria('ERRO:INIT', `Falha na inicialização: ${erro.message}`);
    atualizarStatus('Erro ao carregar Pyodide.');
  }
}

/**
 * Fase 3: Implementação da função ponte dentro do interpretador Python.
 */
function registrarPontePython() {
  const codigoPontePython = `
import time
import traceback
from typing import Optional, Dict, Any, List
from calculadora.operacoes import calcular, formatar_resultado, DivisaoPorZeroError, OperacaoInvalidaError
from calculadora.validacao import converter_operando, ErroValidacao

def bridge_calcular(a_str: str, b_str: str, op_str: str) -> dict:
    t_inicio = time.perf_counter()
    logs: List[str] = []
    
    try:
        logs.append(f"converter_operando('{a_str}', nome_campo='Operando A')")
        a_num = converter_operando(a_str, nome_campo="Operando A")
        logs.append(f"-> Operando A convertido para {a_num}")
        
        logs.append(f"converter_operando('{b_str}', nome_campo='Operando B')")
        b_num = converter_operando(b_str, nome_campo="Operando B")
        logs.append(f"-> Operando B convertido para {b_num}")
        
        logs.append(f"calcular({a_num}, {b_num}, '{op_str}')")
        res_bruto = calcular(a_num, b_num, op_str)
        logs.append(f"-> resultado bruto = {res_bruto}")
        
        logs.append(f"formatar_resultado({res_bruto})")
        res_formatado = formatar_resultado(res_bruto)
        logs.append(f"-> resultado formatado = '{res_formatado}'")
        
        t_fim = time.perf_counter()
        tempo_interno_ms = round((t_fim - t_inicio) * 1000, 3)
        
        return {
            "sucesso": True,
            "resultado": res_formatado,
            "tipo_erro": None,
            "mensagem": None,
            "detalhes": None,
            "tempo_interno_ms": tempo_interno_ms,
            "logs": logs
        }
        
    except ErroValidacao as e:
        t_fim = time.perf_counter()
        logs.append(f"ErroValidacao capturado: {e}")
        return {
            "sucesso": False,
            "resultado": None,
            "tipo_erro": "ErroValidacao",
            "mensagem": str(e),
            "detalhes": None,
            "tempo_interno_ms": round((t_fim - t_inicio) * 1000, 3),
            "logs": logs
        }
        
    except DivisaoPorZeroError as e:
        t_fim = time.perf_counter()
        logs.append(f"DivisaoPorZeroError capturado: {e}")
        return {
            "sucesso": False,
            "resultado": None,
            "tipo_erro": "DivisaoPorZeroError",
            "mensagem": str(e),
            "detalhes": None,
            "tempo_interno_ms": round((t_fim - t_inicio) * 1000, 3),
            "logs": logs
        }
        
    except OperacaoInvalidaError as e:
        t_fim = time.perf_counter()
        logs.append(f"OperacaoInvalidaError capturado: {e}")
        return {
            "sucesso": False,
            "resultado": None,
            "tipo_erro": "OperacaoInvalidaError",
            "mensagem": str(e),
            "detalhes": None,
            "tempo_interno_ms": round((t_fim - t_inicio) * 1000, 3),
            "logs": logs
        }
        
    except Exception as e:
        t_fim = time.perf_counter()
        tb = traceback.format_exc()
        logs.append(f"Exceção não esperada: {type(e).__name__}")
        return {
            "sucesso": False,
            "resultado": None,
            "tipo_erro": f"ErroInesperado ({type(e).__name__})",
            "mensagem": "Ocorreu um erro interno inesperado no processamento.",
            "detalhes": tb,
            "tempo_interno_ms": round((t_fim - t_inicio) * 1000, 3),
            "logs": logs
        }
`;

  pyodide.runPython(codigoPontePython);
  logTelemetria('PONTE:REGISTRADA', "Função 'bridge_calcular' registrada com sucesso no namespace global.");
}

/**
 * Fase 4: Executa a ponte Python com liberação estrita de proxies
 * e sincronização de Promise via requestAnimationFrame.
 */
function executarCicloCalculo(operandoA, operandoB, operacao, provedorPonteOpcional = null) {
  return new Promise((resolve) => {
    const tInicio = performance.now();
    let ponteFuncProxy = null;
    let resultadoProxy = null;
    let resposta = null;

    try {
      if (!pyodide || !inicializacaoConcluida) {
        throw new Error("Pyodide ainda não concluiu a inicialização.");
      }

      // 1. Obtém o proxy da função ponte (permite injeção limpa sem mutação de globals)
      ponteFuncProxy = (typeof provedorPonteOpcional === 'function')
        ? provedorPonteOpcional()
        : pyodide.globals.get('bridge_calcular');

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
      if (resultadoProxy && typeof resultadoProxy.destroy === 'function') {
        try { resultadoProxy.destroy(); } catch (e) { /* silencia limpeza */ }
      }
      if (ponteFuncProxy && typeof ponteFuncProxy.destroy === 'function') {
        try { ponteFuncProxy.destroy(); } catch (e) { /* silencia limpeza */ }
      }
    }

    // 6. Sincronização via requestAnimationFrame: a Promise só resolve após o callback
    requestAnimationFrame(() => {
      try {
        const tAposAtualizacao = performance.now();
        resposta.tempo_ate_atualizacao_dom_ms = Number((tAposAtualizacao - tInicio).toFixed(2));

        // Atualiza a telemetria na página (sem expor tracebacks)
        registrarTelemetriaCalculo(resposta, operandoA, operandoB, operacao);

        // Se houver traceback de erro inesperado, emite exclusivamente no console
        if (resposta.detalhes) {
          console.error("[Diagnóstico Pyodide] Traceback de erro inesperado:\n" + resposta.detalhes);
        }
      } catch (erroRaf) {
        console.error("Erro interno ao processar telemetria no requestAnimationFrame:", erroRaf);
      } finally {
        resolve(resposta);
      }
    });
  });
}

/**
 * Trata erros que ocorram na camada JavaScript antes ou durante a ponte.
 */
function tratarErroInesperadoJs(erroJs, tInicio) {
  console.error("[Diagnóstico JS] Exceção na camada JavaScript:", erroJs);
  const respostaErro = {
    sucesso: false,
    resultado: null,
    tipo_erro: "ErroInesperadoJS",
    mensagem: "Ocorreu um erro interno inesperado no processamento.",
    detalhes: erroJs && erroJs.stack ? erroJs.stack : String(erroJs),
    tempo_interno_ms: 0.0,
    logs: ["Falha na camada de integração JavaScript: " + erroJs.message]
  };
  atualizarInterfaceResultado(respostaErro);
  return respostaErro;
}

/**
 * Atualiza o DOM com acessibilidade visual WCAG AA e pares semânticos.
 */
function atualizarInterfaceResultado(resposta) {
  if (!dom.painelResultado) return;

  // Limpa classes de estado
  dom.painelResultado.classList.remove('sucesso', 'aviso', 'erro');

  if (resposta.sucesso) {
    dom.painelResultado.classList.add('sucesso');
    dom.painelResultado.setAttribute('role', 'status');
    dom.painelResultado.setAttribute('aria-live', 'polite');

    dom.resultadoIcone.textContent = '✓';
    dom.resultadoRotulo.textContent = 'Sucesso:';
    dom.resultadoValor.textContent = resposta.resultado;
    dom.resultadoMensagem.textContent = 'Cálculo concluído com sucesso.';
  } else {
    dom.painelResultado.setAttribute('role', 'alert');
    dom.resultadoValor.textContent = '';

    if (resposta.tipo_erro === 'ErroValidacao') {
      dom.painelResultado.classList.add('aviso');
      dom.resultadoIcone.textContent = '⚠';
      dom.resultadoRotulo.textContent = 'Aviso de Validação:';
      dom.resultadoMensagem.textContent = resposta.mensagem || 'Entrada inválida.';
    } else if (resposta.tipo_erro === 'DivisaoPorZeroError') {
      dom.painelResultado.classList.add('erro');
      dom.resultadoIcone.textContent = '✖';
      dom.resultadoRotulo.textContent = 'Erro Aritmético:';
      dom.resultadoMensagem.textContent = resposta.mensagem || 'Divisão por zero.';
    } else {
      dom.painelResultado.classList.add('erro');
      dom.resultadoIcone.textContent = '✖';
      dom.resultadoRotulo.textContent = 'Erro do Sistema:';
      dom.resultadoMensagem.textContent = resposta.mensagem || 'Erro inesperado.';
    }
  }
}

/**
 * Registra o cálculo na caixa de telemetria sem expor tracebacks.
 */
function registrarTelemetriaCalculo(resposta, opA, opB, op) {
  const statusTexto = resposta.sucesso ? `SUCESSO [${resposta.resultado}]` : `FALHA [${resposta.tipo_erro}]`;
  const metricas = `tempo_interno_ms=${resposta.tempo_interno_ms}ms | tempo_ate_atualizacao_dom_ms=${resposta.tempo_ate_atualizacao_dom_ms}ms`;
  
  let msg = `Entradas: A="${opA}", B="${opB}", Op="${op}" -> ${statusTexto} (${metricas})\n`;
  if (resposta.logs && resposta.logs.length > 0) {
    msg += "  Etapas Python:\n    " + resposta.logs.join("\n    ");
  }
  
  logTelemetria('CALCULO:EXECUCAO', msg);
}

/**
 * Ação de limpeza esvazia inputs e restaura estado neutro e foco.
 */
function limparCampos() {
  if (dom.inputOpA) dom.inputOpA.value = '';
  if (dom.inputOpB) dom.inputOpB.value = '';
  
  const radioSoma = document.getElementById('op-soma');
  if (radioSoma) radioSoma.checked = true;

  if (dom.painelResultado) {
    dom.painelResultado.classList.remove('sucesso', 'aviso', 'erro');
    dom.painelResultado.setAttribute('role', 'status');
    dom.resultadoIcone.textContent = 'ℹ';
    dom.resultadoRotulo.textContent = 'Aguardando Operação:';
    dom.resultadoValor.textContent = '';
    dom.resultadoMensagem.textContent = 'Preencha os campos e selecione uma operação.';
  }

  logTelemetria('ACAO:LIMPAR', 'Campos de entrada e resultado restaurados.');
  if (dom.inputOpA) dom.inputOpA.focus();
}

/**
 * Obtém a operação selecionada nos radio buttons.
 */
function obterOperacaoSelecionada() {
  const radioSelecionado = document.querySelector('input[name="operacao"]:checked');
  return radioSelecionado ? radioSelecionado.value : '+';
}

/**
 * Dispara o ciclo de cálculo a partir dos inputs.
 */
async function dispararCalculo() {
  const valA = dom.inputOpA ? dom.inputOpA.value : '';
  const valB = dom.inputOpB ? dom.inputOpB.value : '';
  const op = obterOperacaoSelecionada();

  await executarCicloCalculo(valA, valB, op);
}

// Configuração de Event Listeners
function configurarEventos() {
  if (dom.btnCalcular) {
    dom.btnCalcular.addEventListener('click', dispararCalculo);
  }

  if (dom.btnLimpar) {
    dom.btnLimpar.addEventListener('click', limparCampos);
  }

  // Atalhos de teclado: Enter para calcular, Esc para limpar
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const activeEl = document.activeElement;
      if (activeEl === dom.inputOpA || activeEl === dom.inputOpB) {
        e.preventDefault();
        dispararCalculo();
      }
    } else if (e.key === 'Escape') {
      limparCampos();
    }
  });

}

// Inicialização da aplicação
document.addEventListener('DOMContentLoaded', () => {
  configurarEventos();
  inicializarPyodideEModulos();
});

// Expõe métodos essenciais no escopo global para a suíte de testes web
window.calculadoraApp = {
  executarCicloCalculo,
  limparCampos,
  pyodidePronto: () => inicializacaoConcluida && pyodide !== null,
  obterPyodide: () => pyodide,
};
