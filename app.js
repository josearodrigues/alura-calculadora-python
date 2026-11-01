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
  telemetriaLog: document.getElementById('telemetria-log'),
  visorExpressao: document.getElementById('visor-expressao'),
  visorResultado: document.getElementById('visor-resultado'),
  teclado: document.getElementById('teclado-calculadora'),
  listaHistorico: document.getElementById('lista-historico'),
  btnTema: document.getElementById('btn-tema'),
  btnCopiar: document.getElementById('btn-copiar'),
  feedbackCopiar: document.getElementById('feedback-copiar'),
  btnLimparHistorico: document.getElementById('btn-limpar-historico'),
  btnHistoricoRodape: document.getElementById('btn-historico-limpar-rodape'),
  btnHistorico: document.getElementById('btn-historico'),
  btnInformacoes: document.getElementById('btn-informacoes'),
};

let expressaoAtual = '';
let resultadoAtual = null;
let memoriaCalculadora = 0;
let calculoConcluido = false;

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
  // Os controles da interface atual dependem da inicialização do Pyodide.
  if (dom.teclado) {
    dom.teclado.querySelectorAll('button').forEach(botao => {
      botao.disabled = !habilitado;
    });
  }
  [dom.btnTema, dom.btnHistorico, dom.btnInformacoes].forEach(botao => {
    if (botao) botao.disabled = !habilitado;
  });
  if (dom.btnLimparHistorico) dom.btnLimparHistorico.disabled = !habilitado;
  if (dom.btnHistoricoRodape) dom.btnHistoricoRodape.disabled = !habilitado;
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

    // Carrega os cinco módulos do pacote. __init__.py importa expressoes.py
    // e historico.py, portanto todos precisam existir antes da importação.
    const arquivosParaCarregar = [
      { nome: '__init__.py', caminho: './calculadora/__init__.py' },
      { nome: 'operacoes.py', caminho: './calculadora/operacoes.py' },
      { nome: 'validacao.py', caminho: './calculadora/validacao.py' },
      { nome: 'expressoes.py', caminho: './calculadora/expressoes.py' },
      { nome: 'historico.py', caminho: './calculadora/historico.py' },
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
from calculadora import operacoes, validacao, expressoes, historico
from calculadora import avaliar_expressao, HistoricoSessao
`);
    logTelemetria('PYTHON:IMPORT', "Pacote 'calculadora' importado e verificado com sucesso.");

    // Fase 3: Registra a função ponte Python com tratamento de erros e logs
    registrarPontePython();

    atualizarStatus('Pronto (Pyodide v0.27.8)', true);
    inicializacaoConcluida = true;
    definirControlesHabilitados(true);
    renderizarHistorico();
    atualizarVisor();

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
from typing import Optional
from calculadora.operacoes import ErroAritmetico, OperacaoInvalidaError
from calculadora.validacao import ErroValidacao, sanitizar_texto
from calculadora.expressoes import avaliar_expressao, ExpressaoInvalidaError
from calculadora.historico import HistoricoSessao, RegistroNaoEncontradoError

# Uma única sessão Python mantém histórico e ANS durante a vida da página.
historico_sessao = HistoricoSessao()

def _entrada_para_dict(entrada):
    return {
        "id": entrada.id,
        "expressao": entrada.expressao,
        "expressao_formatada": entrada.expressao_formatada,
        "resultado": entrada.resultado,
        "resultado_formatado": entrada.resultado_formatado,
        "timestamp": entrada.timestamp,
    }

def bridge_avaliar_expressao(expressao_bruta: str, expressao_formatada: Optional[str] = None) -> dict:
    """Avalia uma expressão, registra o cálculo e atualiza o ANS da sessão."""
    t_inicio = time.perf_counter()
    try:
        expressao_limpa = sanitizar_texto(expressao_bruta)
        resultado = avaliar_expressao(expressao_limpa, ans=historico_sessao.obter_ans())
        entrada = historico_sessao.registrar(
            expressao_limpa,
            sanitizar_texto(expressao_formatada) or expressao_limpa,
            resultado,
        )
        return {
            "sucesso": True,
            "entrada": _entrada_para_dict(entrada),
            "resultado": entrada.resultado_formatado,
            "ans": historico_sessao.obter_ans(),
            "tipo_erro": None,
            "mensagem": None,
            "tempo_interno_ms": round((time.perf_counter() - t_inicio) * 1000, 3),
        }
    except (ErroValidacao, ExpressaoInvalidaError, ErroAritmetico, OperacaoInvalidaError) as e:
        return {
            "sucesso": False,
            "entrada": None,
            "resultado": None,
            "ans": historico_sessao.obter_ans(),
            "tipo_erro": type(e).__name__,
            "mensagem": str(e),
            "tempo_interno_ms": round((time.perf_counter() - t_inicio) * 1000, 3),
        }
    except Exception as e:
        return {
            "sucesso": False,
            "entrada": None,
            "resultado": None,
            "ans": historico_sessao.obter_ans(),
            "tipo_erro": f"ErroInesperado ({type(e).__name__})",
            "mensagem": "Ocorreu um erro interno inesperado no processamento.",
            "tempo_interno_ms": round((time.perf_counter() - t_inicio) * 1000, 3),
        }

def bridge_obter_historico() -> list:
    """Retorna os registros da sessão em ordem cronológica."""
    return [_entrada_para_dict(item) for item in historico_sessao.obter_todos()]

def bridge_recuperar_historico(id_entrada: int) -> dict:
    """Recupera uma entrada e atualiza o ANS no próprio motor Python."""
    try:
        entrada = historico_sessao.recuperar_entrada(int(id_entrada))
        return {
            "sucesso": True,
            "entrada": _entrada_para_dict(entrada),
            "ans": historico_sessao.obter_ans(),
            "tipo_erro": None,
            "mensagem": None,
        }
    except (ValueError, TypeError, RegistroNaoEncontradoError) as e:
        return {
            "sucesso": False,
            "entrada": None,
            "ans": historico_sessao.obter_ans(),
            "tipo_erro": type(e).__name__,
            "mensagem": str(e),
        }

def bridge_limpar_historico() -> dict:
    """Limpa os registros visíveis sem apagar o ANS, conforme regra do motor."""
    historico_sessao.limpar_historico()
    return {"sucesso": True, "ans": historico_sessao.obter_ans(), "total": 0}

def bridge_obter_ans():
    return historico_sessao.obter_ans()


`;

  pyodide.runPython(codigoPontePython);
  logTelemetria('PONTE:REGISTRADA', 'Pontes da interface atual registradas com sucesso.');
}

/**
 * Executa uma ponte Python nomeada e converte seu retorno para JavaScript.
 * Os proxies da função e do resultado são sempre liberados, inclusive em falhas.
 */
function executarPontePython(nomePonte, ...argumentos) {
  let ponteFuncProxy = null;
  let resultadoProxy = null;

  try {
    if (!pyodide || !inicializacaoConcluida) {
      throw new Error("Pyodide ainda não concluiu a inicialização.");
    }

    ponteFuncProxy = pyodide.globals.get(nomePonte);
    if (!ponteFuncProxy) {
      throw new Error(`Ponte Python '${nomePonte}' não encontrada.`);
    }

    resultadoProxy = ponteFuncProxy(...argumentos);
    if (resultadoProxy && typeof resultadoProxy.toJs === 'function') {
      return resultadoProxy.toJs({ dict_converter: Object.fromEntries });
    }
    return resultadoProxy;
  } finally {
    if (resultadoProxy && typeof resultadoProxy.destroy === 'function') {
      try { resultadoProxy.destroy(); } catch (e) { /* silencia limpeza */ }
    }
    if (ponteFuncProxy && typeof ponteFuncProxy.destroy === 'function') {
      try { ponteFuncProxy.destroy(); } catch (e) { /* silencia limpeza */ }
    }
  }
}

function avaliarExpressao(expressao, expressaoFormatada = null) {
  return executarPontePython('bridge_avaliar_expressao', expressao, expressaoFormatada);
}

function obterHistorico() {
  return executarPontePython('bridge_obter_historico');
}

function recuperarHistorico(id) {
  return executarPontePython('bridge_recuperar_historico', id);
}

function limparHistorico() {
  return executarPontePython('bridge_limpar_historico');
}

function obterAns() {
  return executarPontePython('bridge_obter_ans');
}

// Fase 4: estado e interações da nova interface.
function atualizarVisor() {
  if (dom.visorExpressao) dom.visorExpressao.textContent = expressaoAtual || '0';
  if (dom.visorResultado) dom.visorResultado.textContent = resultadoAtual === null ? '0' : String(resultadoAtual);
  if (dom.btnCopiar) dom.btnCopiar.disabled = !inicializacaoConcluida || resultadoAtual === null;
}

function inserirNaExpressao(valor) {
  if (calculoConcluido) {
    // Após "=", operadores continuam a partir do resultado exibido (ANS).
    if (['+', '-', '*', '/', '^'].includes(valor)) {
      expressaoAtual = String(resultadoAtual);
    } else if (/[0-9.(]/.test(valor)) {
      // Um número ou parêntese inicia uma nova expressão.
      expressaoAtual = '';
    }
  }

  calculoConcluido = false;
  expressaoAtual += valor;
  resultadoAtual = null;
  atualizarVisor();
}

function limparVisor() {
  expressaoAtual = '';
  resultadoAtual = null;
  calculoConcluido = false;
  atualizarVisor();
  if (dom.feedbackCopiar) dom.feedbackCopiar.textContent = '';
}

function formatarExpressaoVisivel(expressao) {
  return String(expressao).replaceAll('*', '×').replaceAll('/', '÷');
}

function renderizarHistorico() {
  if (!dom.listaHistorico) return;
  const registros = obterHistorico();
  dom.listaHistorico.replaceChildren();
  if (!registros.length) {
    const vazio = document.createElement('li');
    vazio.className = 'historico-vazio';
    vazio.textContent = 'Nenhum cálculo realizado.';
    dom.listaHistorico.appendChild(vazio);
  } else {
    [...registros].reverse().forEach(registro => {
      const item = document.createElement('li');
      const botao = document.createElement('button');
      botao.type = 'button';
      botao.className = 'item-historico';
      botao.dataset.id = String(registro.id);
      const expressao = document.createElement('span');
      expressao.className = 'historico-expressao';
      expressao.textContent = formatarExpressaoVisivel(registro.expressao);
      const resultado = document.createElement('span');
      resultado.className = 'historico-resultado';
      resultado.textContent = registro.resultado_formatado;
      botao.append(expressao, resultado);
      botao.addEventListener('click', () => {
        const resposta = recuperarHistorico(registro.id);
        if (!resposta.sucesso) {
          mostrarErroExpressao(resposta.mensagem);
          return;
        }
        expressaoAtual = resposta.entrada.expressao;
        resultadoAtual = resposta.entrada.resultado_formatado;
        calculoConcluido = true;
        atualizarVisor();
        logTelemetria('HISTORICO:RECUPERADO', `Registro #${registro.id} recuperado.`);
      });
      item.appendChild(botao);
      dom.listaHistorico.appendChild(item);
    });
  }
  const desabilitado = registros.length === 0;
  [dom.btnLimparHistorico, dom.btnHistoricoRodape].forEach(b => { if (b) b.disabled = desabilitado; });
}

function mostrarErroExpressao(mensagem) {
  if (dom.visorResultado) dom.visorResultado.textContent = 'Erro';
  if (dom.feedbackCopiar) dom.feedbackCopiar.textContent = mensagem || 'Não foi possível calcular.';
  logTelemetria('CALCULO:ERRO', mensagem || 'Falha ao avaliar expressão.');
}

function executarExpressaoAtual() {
  if (!expressaoAtual.trim()) return;
  try {
    const resposta = avaliarExpressao(expressaoAtual, formatarExpressaoVisivel(expressaoAtual));
    if (!resposta.sucesso) {
      mostrarErroExpressao(resposta.mensagem);
      return;
    }
    resultadoAtual = resposta.resultado;
    calculoConcluido = true;
    atualizarVisor();
    renderizarHistorico();
    logTelemetria('CALCULO:EXPRESSAO', `${expressaoAtual} = ${resultadoAtual}`);
  } catch (erro) {
    mostrarErroExpressao(erro.message);
  }
}

function aplicarAcaoTecla(acao) {
  const numeroOuOperador = /^[0-9.]$/.test(acao) || ['+', '-', '*', '/', '^', '(', ')'].includes(acao);
  if (numeroOuOperador) { inserirNaExpressao(acao); return; }
  switch (acao) {
    case 'equals': executarExpressaoAtual(); break;
    case 'clear': limparVisor(); break;
    case 'backspace':
      expressaoAtual = expressaoAtual.slice(0, -1);
      resultadoAtual = null; calculoConcluido = false; atualizarVisor(); break;
    case 'sign':
      if (resultadoAtual !== null) expressaoAtual = String(Number(resultadoAtual) * -1);
      else if (expressaoAtual) expressaoAtual = `-(${expressaoAtual})`;
      resultadoAtual = null; calculoConcluido = false; atualizarVisor(); break;
    case 'percent': inserirNaExpressao('%'); break;
    case 'sqrt': inserirNaExpressao('sqrt('); break;
    case 'nth-root':
      if (calculoConcluido && resultadoAtual !== null) {
        expressaoAtual = `root(${resultadoAtual}; `;
        calculoConcluido = false;
        resultadoAtual = null;
        atualizarVisor();
      } else {
        inserirNaExpressao('root(');
      }
      break;
    case 'square': inserirNaExpressao('^2'); break;
    case 'reciprocal': inserirNaExpressao('1/('); break;
    case 'absolute': inserirNaExpressao('abs('); break;
    case ';': inserirNaExpressao(';'); break;
    case 'memory-clear': memoriaCalculadora = 0; break;
    case 'memory-store':
      if (resultadoAtual !== null) memoriaCalculadora = Number(resultadoAtual);
      break;
    case 'memory-recall': inserirNaExpressao(String(memoriaCalculadora)); break;
    case 'memory-add':
      if (resultadoAtual !== null) memoriaCalculadora += Number(resultadoAtual);
      break;
    case 'memory-subtract':
      if (resultadoAtual !== null) memoriaCalculadora -= Number(resultadoAtual);
      break;
  }
}

function configurarTema() {
  const chave = 'theme_calculadora';
  const salvo = localStorage.getItem(chave);
  const temaInicial = salvo === 'light' || salvo === 'dark' ? salvo : 'dark';
  document.documentElement.dataset.theme = temaInicial;
  atualizarIconeTema(temaInicial);
  if (dom.btnTema) {
    dom.btnTema.addEventListener('click', () => {
      const proximo = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      document.documentElement.dataset.theme = proximo;
      localStorage.setItem(chave, proximo);
      atualizarIconeTema(proximo);
    });
  }
}

function atualizarIconeTema(tema) {
  if (!dom.btnTema) return;
  dom.btnTema.textContent = tema === 'dark' ? '☀' : '☾';
  dom.btnTema.setAttribute('aria-label', tema === 'dark' ? 'Ativar tema claro' : 'Ativar tema escuro');
}

async function copiarResultado() {
  if (resultadoAtual === null || !navigator.clipboard || !navigator.clipboard.writeText) {
    if (dom.feedbackCopiar) dom.feedbackCopiar.textContent = 'Área de transferência indisponível.';
    return;
  }
  try {
    await navigator.clipboard.writeText(String(resultadoAtual));
    if (dom.feedbackCopiar) dom.feedbackCopiar.textContent = 'Resultado copiado!';
  } catch (erro) {
    if (dom.feedbackCopiar) dom.feedbackCopiar.textContent = 'Não foi possível copiar.';
    logTelemetria('CLIPBOARD:ERRO', erro.message);
  }
}

function configurarNovaInterface() {
  configurarTema();
  if (dom.teclado) dom.teclado.addEventListener('click', e => {
    const botao = e.target.closest('button[data-action]');
    if (botao && !botao.disabled) aplicarAcaoTecla(botao.dataset.action);
  });
  if (dom.btnCopiar) dom.btnCopiar.addEventListener('click', copiarResultado);
  const limpar = () => {
    try {
      const resposta = limparHistorico();
      if (resposta.sucesso) renderizarHistorico();
    } catch (erro) { mostrarErroExpressao(erro.message); }
  };
  if (dom.btnLimparHistorico) dom.btnLimparHistorico.addEventListener('click', limpar);
  if (dom.btnHistoricoRodape) dom.btnHistoricoRodape.addEventListener('click', limpar);
  if (dom.btnHistorico) dom.btnHistorico.addEventListener('click', () => dom.listaHistorico?.scrollIntoView({behavior:'smooth'}));
  if (dom.btnInformacoes) dom.btnInformacoes.addEventListener('click', () => {
    if (dom.feedbackCopiar) dom.feedbackCopiar.textContent = 'Calculadora 2.0 — motor Python executado via Pyodide.';
  });
  window.addEventListener('keydown', e => {
    if (e.ctrlKey || e.metaKey || e.altKey || e.target.matches('input, textarea, select')) return;
    if (/^[0-9.]$/.test(e.key) || ['+', '-', '*', '/', '(', ')'].includes(e.key)) {
      e.preventDefault(); inserirNaExpressao(e.key);
    } else if (e.key === 'Enter' || e.key === '=') {
      e.preventDefault(); executarExpressaoAtual();
    } else if (e.key === 'Backspace') {
      e.preventDefault(); aplicarAcaoTecla('backspace');
    } else if (e.key === 'Escape') {
      e.preventDefault(); limparVisor();
    }
  });
  atualizarVisor();
}

// Inicialização da aplicação
document.addEventListener('DOMContentLoaded', () => {
  configurarEventos();
  configurarNovaInterface();
  inicializarPyodideEModulos();
});

// Expõe métodos essenciais no escopo global para a suíte de testes web
window.calculadoraApp = {
  executarPontePython, avaliarExpressao, obterHistorico, recuperarHistorico,
  limparHistorico, obterAns, limparVisor, renderizarHistorico,
  pyodidePronto: () => inicializacaoConcluida && pyodide !== null,
  obterPyodide: () => pyodide,
};
