/**
 * Suíte de testes do navegador para a Calculadora 2.0.
 * Casos voltados à interface atual e à integração com Pyodide.
 */
const relatorioTestes=[];
let notificarResultadoTeste=null;
function registrarResultadoTeste(id,descricao,status,detalhes=""){
 const resultado={id,descricao,status,passou:status==="APROVADO",detalhes};
 relatorioTestes.push(resultado);
 console.log(`[TESTE WEB ${status}] ${id}: ${descricao}${detalhes?` (${detalhes})`:""}`);
 if(notificarResultadoTeste){
  try{notificarResultadoTeste(resultado);}
  catch(e){console.warn("Falha ao atualizar a tabela de testes:",e);}
 }
}
function exigir(ok,msg){if(!ok)throw new Error(msg);}
function el(doc,sel){const e=doc.querySelector(sel);exigir(!!e,`Elemento ausente: ${sel}`);return e;}
function tecla(doc,acao){const b=el(doc,`#teclado-calculadora [data-action="${acao}"]`);exigir(!b.disabled,`Tecla desabilitada: ${acao}`);b.click();}
function preparar({app}){app.limparVisor();const r=app.limparHistorico();exigir(r.sucesso,"Falha ao limpar histórico.");app.renderizarHistorico();}
async function executarCaso(c,ctx){try{if(c.preparar!==false)preparar(ctx);const detalhes=await c.executar(ctx);registrarResultadoTeste(c.id,c.descricao,"APROVADO",detalhes||"");}catch(e){registrarResultadoTeste(c.id,c.descricao,"FALHOU",e?.message||String(e));}}
function marcarNaoExecutados(cs,inicio,motivo){for(let i=inicio;i<cs.length;i++)registrarResultadoTeste(cs[i].id,cs[i].descricao,"NÃO EXECUTADO",motivo);}
const casosTeste=[
["Inicialização do Pyodide e status visual Pronto",({app,doc,pyodideInst})=>{exigir(app.pyodidePronto()&&pyodideInst,"Pyodide indisponível.");exigir(el(doc,"#status-texto").textContent.includes("Pronto"),"Status não está Pronto.");exigir(el(doc,"#status-indicador").classList.contains("pronto"),"Indicador não está pronto.");return "Runtime disponível; status e indicador visual confirmados como Pronto.";},false],
["Montagem dos cinco módulos Python no MEMFS",({pyodideInst})=>{const modulos=["__init__.py","operacoes.py","validacao.py","expressoes.py","historico.py"].map(n=>{const bytes=new Blob([pyodideInst.FS.readFile(`/calculadora/${n}`,{encoding:"utf8"})]).size;exigir(bytes>0,`Módulo vazio: ${n}`);return `${n}: ${bytes} bytes`;});return modulos.join("; ");}],
["Controles atuais habilitados após inicialização",({doc})=>{exigir([...el(doc,"#teclado-calculadora").querySelectorAll("button")].every(b=>!b.disabled),"Há teclas desabilitadas.");for(const s of ["#btn-tema","#btn-informacoes","#btn-historico"])exigir(!el(doc,s).disabled,`${s} desabilitado.`);}],
["Adição de números inteiros",({app})=>exigir(app.avaliarExpressao("12+8").resultado==="20","12+8 deveria ser 20.")],
["Subtração com resultado negativo",({app})=>exigir(app.avaliarExpressao("10-25").resultado==="-15","10-25 deveria ser -15.")],
["Multiplicação por zero",({app})=>exigir(app.avaliarExpressao("50*0").resultado==="0","50*0 deveria ser 0.")],
["Divisão com resultado fracionário",({app})=>exigir(app.avaliarExpressao("7/2").resultado==="3.5","7/2 deveria ser 3.5.")],
["Entrada decimal com vírgula",({app})=>exigir(app.avaliarExpressao("12,5+2,5").resultado==="15","Decimais com vírgula deveriam somar 15.")],
["Precedência entre multiplicação e adição",({app})=>exigir(app.avaliarExpressao("2+3*4").resultado==="14","Precedência incorreta.")],
["Agrupamento com parênteses",({app})=>exigir(app.avaliarExpressao("(2+3)*4").resultado==="20","Agrupamento incorreto.")],
["Potenciação",({app})=>exigir(app.avaliarExpressao("2^3").resultado==="8","2^3 deveria ser 8.")],
["Associatividade à direita da potenciação",({app})=>exigir(app.avaliarExpressao("2^3^2").resultado==="512","Potenciação deveria associar à direita.")],
["Precedência do sinal unário",({app})=>exigir(app.avaliarExpressao("-2^2").resultado==="-4","-2^2 deveria ser -4.")],
["Percentual contextual em adição",({app})=>exigir(app.avaliarExpressao("200+10%").resultado==="220","200+10% deveria ser 220.")],
["Percentual isolado",({app})=>exigir(app.avaliarExpressao("50%").resultado==="0.5","50% deveria ser 0.5.")],
["Raiz quadrada",({app})=>exigir(app.avaliarExpressao("sqrt(81)").resultado==="9","sqrt(81) deveria ser 9.")],
["Raiz de índice n e separador de argumentos",({app})=>exigir(app.avaliarExpressao("root(27;3)").resultado==="3","root(27;3) deveria ser 3.")],
["Função valor absoluto",({app})=>exigir(app.avaliarExpressao("abs(-8)").resultado==="8","abs(-8) deveria ser 8.")],
["Resolução do identificador ANS",({app})=>{app.avaliarExpressao("10");exigir(app.avaliarExpressao("ANS+5").resultado==="15","ANS não recuperou o resultado anterior.");}],
["Rejeição de identificador desconhecido",({app})=>{const r=app.avaliarExpressao("2+abc");exigir(!r.sucesso&&r.tipo_erro==="ExpressaoInvalidaError","Identificador desconhecido não foi rejeitado.");}],
["Tratamento de divisão por zero",({app})=>{const r=app.avaliarExpressao("10/0");exigir(!r.sucesso&&r.tipo_erro==="DivisaoPorZeroError","Divisão por zero não gerou erro de domínio.");}],
["Registro de cálculo no histórico Python",({app})=>{const r=app.avaliarExpressao("3+4"),h=app.obterHistorico();exigir(r.sucesso&&h.length===1&&h[0].resultado_formatado==="7","Registro do histórico incorreto.");}],
["Recuperação de registro e atualização do ANS",({app})=>{app.avaliarExpressao("3+4");app.avaliarExpressao("8+2");const h=app.obterHistorico(),r=app.recuperarHistorico(h[0].id);exigir(r.sucesso&&r.entrada.resultado_formatado==="7"&&r.ans===7,"Recuperação/ANS incorretos.");}],
["Limpeza do histórico preservando o ANS",({app})=>{app.avaliarExpressao("42");app.limparHistorico();exigir(app.obterHistorico().length===0&&app.obterAns()===42,"Limpeza não preservou ANS.");}],
["Execução de cálculo pelas teclas da interface",({doc})=>{for(const a of ["7","+","2","equals"])tecla(doc,a);exigir(el(doc,"#visor-expressao").textContent==="7+2"&&el(doc,"#visor-resultado").textContent==="9","Teclado não calculou 7+2.");}],
["Limpeza do visor e estado neutro",({doc})=>{for(const a of ["4","*","3","equals","clear"])tecla(doc,a);exigir(el(doc,"#visor-expressao").textContent==="0"&&el(doc,"#visor-resultado").textContent==="0"&&el(doc,"#btn-copiar").disabled,"Limpeza do visor incompleta.");return "Expressão e resultado zerados; botão de cópia desabilitado."; }],
["Apagar último caractere pelo teclado da calculadora",({doc})=>{for(const a of ["1","2","3","backspace"])tecla(doc,a);exigir(el(doc,"#visor-expressao").textContent==="12","Backspace não removeu o último caractere.");}],
["Atalhos físicos de teclado e Enter",({doc})=>{const w=doc.defaultView;for(const key of ["6","+","4","Enter"])doc.body.dispatchEvent(new w.KeyboardEvent("keydown",{key,bubbles:true,cancelable:true}));exigir(el(doc,"#visor-expressao").textContent==="6+4"&&el(doc,"#visor-resultado").textContent==="10","Atalhos físicos não executaram 6+4.");}],
["Alternância de tema e persistência",({doc})=>{const b=el(doc,"#btn-tema"),old=doc.documentElement.dataset.theme;b.click();const next=old==="dark"?"light":"dark";exigir(doc.documentElement.dataset.theme===next&&doc.defaultView.localStorage.getItem("theme_calculadora")===next,"Tema não alternou ou não persistiu.");b.click();}],
["Memória: armazenar e recuperar resultado",({doc})=>{for(const a of ["8","equals","memory-store","clear","memory-recall","equals"])tecla(doc,a);exigir(el(doc,"#visor-resultado").textContent==="8","Memória não recuperou 8.");}],
["Renderização e recuperação pela lista de histórico",({app,doc})=>{app.avaliarExpressao("9*9");app.renderizarHistorico();el(doc,"#lista-historico button.item-historico").click();exigir(el(doc,"#visor-resultado").textContent==="81","Histórico não recuperou 81.");}]
].map(([descricao,executar,prepararCaso=true],i)=>({id:`TW-${String(i+1).padStart(2,"0")}`,descricao,executar,preparar:prepararCaso}));
async function executarTodosOsTestesWeb(onResultado=null){
 notificarResultadoTeste=typeof onResultado==="function"?onResultado:null;
 relatorioTestes.length=0;console.log(`=== SUÍTE WEB: ${casosTeste.length} CENÁRIOS ===`);
 const doc=window.documentContexto||document,app=window.calculadoraApp;let tentativas=0;
 while((!app||!app.pyodidePronto())&&tentativas<80){await new Promise(r=>setTimeout(r,250));tentativas++;}
 const pyodideInst=app&&app.pyodidePronto()?app.obterPyodide():null,ctx={doc,app,pyodideInst};
 if(!app||!pyodideInst){registrarResultadoTeste("TW-01",casosTeste[0].descricao,"FALHOU","Pyodide indisponível.");marcarNaoExecutados(casosTeste,1,"Falha na inicialização.");notificarResultadoTeste=null;return relatorioTestes;}
 for(const c of casosTeste)await executarCaso(c,ctx);
 try{preparar(ctx);}catch(e){console.error("Falha na limpeza final:",e);}
 notificarResultadoTeste=null;
 return relatorioTestes;
}
window.executarTodosOsTestesWeb=executarTodosOsTestesWeb;
