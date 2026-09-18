/* _checkcalc.js — verificação automatizada da calculadora de incerteza do nitrito.
   Uso:  node guia_calculadora/_checkcalc.js
   Carrega calculadora_incerteza_nitrito_v2.html em um sandbox (DOM mínimo por Proxy),
   executa asserções de regressão e do vínculo do check com a aba 02 e devolve código
   de saída 0 (tudo ok) ou 1 (alguma falha). Não modifica nenhum arquivo. */
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const HTML = path.join(__dirname, '..', 'calculadora_incerteza_nitrito_v2.html');
const src = fs.readFileSync(HTML, 'utf8');
const m = src.match(/<script>([\s\S]*?)<\/script>/);
if (!m) { console.error('FALHA: bloco <script> nao encontrado em ' + HTML); process.exit(1); }

/* --- DOM mínimo: qualquer acesso devolve um proxy inerte (get/set/apply) ---
   Exceção: o tbody da tabela mensal é capturado, para conferir o HTML gerado. --- */
const captured = {};
const monthlyTbody = {
  set innerHTML(v) { captured.monthly = String(v); },
  get innerHTML() { return captured.monthly || ''; },
};
const monthlyTableStub = { tBodies: [monthlyTbody] };
function inert() {
  const target = function () {};
  return new Proxy(target, {
    get(t, k) {
      if (k === 'forEach') return () => {};
      if (k === 'length') return 0;
      if (k === Symbol.toPrimitive || k === 'toString') return () => '';
      if (k === 'then' || k === 'toJSON') return undefined;
      return inert();
    },
    set() { return true; },
    apply() { return inert(); },
    has() { return true; },
  });
}
const sandbox = {
  console,
  setTimeout: () => {},
  innerWidth: 1280,
  innerHeight: 900,
  confirm: () => true,
  document: {
    getElementById: id => (id === 'monthlyTable' ? monthlyTableStub : inert()),
    querySelector: () => inert(),
    querySelectorAll: () => [],
    createElement: () => inert(),
    addEventListener() {},
  },
  URL: { createObjectURL: () => 'blob:test', revokeObjectURL() {} },
  Blob: function () {},
  addEventListener() {},
};
sandbox.window = sandbox;
sandbox.globalThis = sandbox;
vm.createContext(sandbox);
try {
  vm.runInContext(m[1], sandbox, { filename: 'calculadora_incerteza_nitrito_v2.html' });
} catch (err) {
  console.error('FALHA: erro de sintaxe/execucao ao carregar o script da calculadora -> ' + err.message);
  process.exit(1);
}
const A = sandbox.window.Nitrito;
if (!A) { console.error('FALHA: window.Nitrito nao foi exposto.'); process.exit(1); }
console.log('Calculadora carregada: ' + HTML);

/* --- asserções --- */
let passed = 0, failed = 0;
function section(t) { console.log('\n' + t); }
function ok(cond, label, extra) {
  if (cond) { passed++; console.log('  ok    ' + label); }
  else { failed++; console.log('  FALHA ' + label + (extra === undefined ? '' : '  -> ' + extra)); }
}
function near(a, b, tol) { return Number.isFinite(a) && Math.abs(a - b) <= tol; }
const clone = o => JSON.parse(JSON.stringify(o));
const entry = (r, name) => r.budget.find(b => b.name === name);

/* 1. Regressão: o exemplo fictício não pode mudar em modo manual */
section('1. Regressao do exemplo ficticio (vínculo desligado)');
const base = A.example();
const r0 = A.calculate(base);
ok(r0.errors.length === 0, 'exemplo calcula sem erros', JSON.stringify(r0.errors));
ok(near(r0.y, 0.085, 1e-12), 'y = 0,085 mg/L N-NO2-', r0.y);
ok(near(r0.p.sip, 0.0021, 5e-5), 'sIP = 0,0021 mg/L N-NO2-', r0.p.sip);
ok(near(r0.U, 0.005192, 5e-6), 'U = 0,005192 mg/L N-NO2- (k = 2)', r0.U);
ok(near(entry(r0, 'Precisão intermediária').share, 66.1, 0.4), 'participacao da precisao ~ 66,1%', entry(r0, 'Precisão intermediária').share);
ok(near(entry(r0, 'Recuperação residual de matriz').share, 28.9, 0.4), 'participacao da recuperacao ~ 28,9%', entry(r0, 'Recuperação residual de matriz').share);
ok(near(entry(r0, 'Viés global / check').share, 5.0, 0.4), 'participacao do vies ~ 5,0%', entry(r0, 'Viés global / check').share);
ok(r0.resolvedCheck.linked === false, 'modo manual: resolvedCheck.linked = false');

/* 2. Vínculo vivo: derivação dos campos do check a partir da aba 02 */
section('2. Vinculo vivo (aba 04 lendo da aba 02)');
const linkedCheck = s => { s.certs[0] = {...s.certs[0], name:'Padrão de check', certificate:'CHECK-N-NO₂⁻-2026-019', value:'0.010', unit:'mg/L N-NO₂⁻', U:'0.00006', k:'2', mode:'covered'}; s.checkLink = {enabled:true,certId:'cert-1'}; return s; };
const t2 = linkedCheck(clone(base));
const r2 = A.calculate(t2);
ok(r2.resolvedCheck.linked === true && r2.resolvedCheck.certIndex === 0, 'vinculo aponta para a linha 1 da aba 02');
ok(near(r2.resolvedCheck.value, 0.010, 1e-12), 'valor designado herdado = 0,010 mg/L N-NO2-', r2.resolvedCheck.value);
ok(near(r2.resolvedCheck.U, 0.00006, 1e-12) && near(r2.resolvedCheck.K, 2, 1e-9), 'U = 0,00006 e k = 2 (normal: U/k)', r2.resolvedCheck.U + ' / ' + r2.resolvedCheck.K);
ok(/CHECK-N-NO₂⁻-2026-019/.test(r2.resolvedCheck.cert), 'certificado herdado da linha', r2.resolvedCheck.cert);
ok(r2.resolvedCheck.expiry === '2027-03-01', 'validade herdada da linha', r2.resolvedCheck.expiry);
ok(near(r2.b, (r2.check.mean - 0.010) / 0.010, 1e-12), 'vies recalculado contra o check vinculado de 0,010', r2.b);
ok(A.isCheckSource(t2, 0) === true && A.isCheckSource(base, 0) === false, 'isCheckSource reconhece a linha vinculada');

/* 3. Anti-dupla-contagem: a linha vinculada não entra no orçamento tipo B */
section('3. Anti-dupla-contagem da linha vinculada');
const t3 = linkedCheck(clone(base)); t3.certs[0].mode = 'include';
const r3 = A.calculate(t3);
ok(!r3.budget.some(b => b.name === t3.certs[0].name), 'linha vinculada nao entra no orcamento tipo B');
ok(r3.warnings.some(w => /vinculada como fonte do check/.test(w)), 'aviso de dupla contagem emitido', JSON.stringify(r3.warnings));
const t3b = linkedCheck(clone(base)); t3b.checkLink = {enabled:false,certId:''}; t3b.certs[0].mode = 'include';
ok(A.calculate(t3b).budget.some(b => b.name === t3b.certs[0].name), 'sem vinculo, "Independente" continua somando (comportamento antigo)');

/* 4. Conversões: distribuição (normal/retangular/resolução) e unidade */
section('4. Conversoes de distribuicao e unidade');
const t4 = linkedCheck(clone(base)); t4.certs[0].distribution = 'rect'; t4.certs[0].U = '0.0001';
const r4 = A.calculate(t4);
ok(near(r4.resolvedCheck.K, Math.sqrt(3), 1e-12), 'retangular: k = raiz de 3', r4.resolvedCheck.K);
ok(near(r4.resolvedCheck.U, 0.0001, 1e-12), 'retangular: U = a (limite)', r4.resolvedCheck.U);
ok(/retangular/.test(r4.resolvedCheck.notes.join(' ')), 'nota de conversao retangular exibida');
const t5 = clone(t4); t5.certs[0].distribution = 'resolution'; t5.certs[0].U = '0.00002';
ok(near(A.calculate(t5).resolvedCheck.K, Math.sqrt(12), 1e-12), 'resolucao: k = raiz de 12', A.calculate(t5).resolvedCheck.K);
const t6 = linkedCheck(clone(base)); t6.certs[0].value = '0.00001'; t6.certs[0].unit = 'g/L'; t6.certs[0].U = '0.00000006';
const r6 = A.calculate(t6);
ok(near(r6.resolvedCheck.value, 0.010, 1e-12) && near(r6.resolvedCheck.U,0.00006,1e-12), 'g/L convertido para mg/L em valor e U', r6.resolvedCheck.value+' / '+r6.resolvedCheck.U);
ok(/convertido/.test(r6.resolvedCheck.notes.join(' ')), 'previa informa a conversao de unidade');
const t7 = linkedCheck(clone(base)); t7.certs[0].unit = '%';
ok(A.calculate(t7).errors.some(e => /relativa/.test(e)), 'unidade relativa (%) nao vincula e explica o motivo');
const t8 = linkedCheck(clone(base)); t8.certs[0].unit = 'unidade desconhecida';
ok(A.calculate(t8).errors.some(e => /não foi reconhecida/.test(e)), 'unidade desconhecida nao vincula e explica o motivo');
ok(near(A.unitToMgL('mg/L NO₂⁻').factor,14/46,1e-12), 'unitToMgL: NO2- convertido para base N');
ok(A.unitToMgL('mg/mL').factor === 1000, 'unitToMgL: mg/mL = 1000');
ok(A.unitToMgL('mg/L N-NO₂⁻').factor === 1 && A.unitToMgL('mg/L NO₂-N').factor === 1, 'unitToMgL: bases N-NO2- aceitas diretamente');
ok(A.unitToMgL('mg/L').factor === 1 && A.unitToMgL('g/L').factor === 1000, 'unitToMgL: mg/L e g/L');

/* 5. Vínculo vivo reage à edição do certificado */
section('5. Vinculo vivo reage a edicao do certificado');
const t9 = linkedCheck(clone(base));
const ubBefore = A.calculate(t9).ub;
const t10 = clone(t9); t10.certs[0].U = '0.00012';
const r10 = A.calculate(t10);
ok(near(r10.resolvedCheck.U, 0.00012, 1e-12), 'U derivado acompanha a edicao da aba 02', r10.resolvedCheck.U);
ok(r10.ub > ubBefore, 'u do vies muda automaticamente (sem redigitar)', ubBefore + ' -> ' + r10.ub);

/* 6. Vínculo quebrado */
section('6. Vinculo quebrado (linha removida)');
const t11 = clone(base); t11.checkLink = { enabled: true, certId: 'cert-99' };
const r11 = A.calculate(t11);
ok(r11.resolvedCheck.broken === true, 'resolvedCheck.broken = true');
ok(r11.errors.some(e => /não existe mais/.test(e)), 'erro explicito de vinculo quebrado', JSON.stringify(r11.errors));

/* 7. Importação e compatibilidade do JSON */
section('7. Importacao e compatibilidade do JSON');
const oldJson = clone(base);
delete oldJson.checkLink;
oldJson.certs.forEach(c => { delete c.id; });
const imported = A.validateImport(clone(oldJson));
ok(imported.certs.every(c => typeof c.id === 'string' && c.id.length > 0), 'ids atribuidos na importacao de JSON antigo');
ok(imported.checkLink && imported.checkLink.enabled === false && imported.checkLink.certId === '', 'checkLink padrao = manual');
ok(A.calculate(imported).errors.length === 0, 'estudo importado calcula sem erros');
const linkedJson = clone(base); linkedJson.checkLink = { enabled: true, certId: 'cert-1' };
const rt2 = A.validateImport(clone(linkedJson));
ok(rt2.checkLink.enabled === true && rt2.checkLink.certId === 'cert-1', 'round-trip preserva o vinculo ativo');
ok(A.calculate(rt2).resolvedCheck.certIndex === 0, 'vinculo resolve apos import');
const dup = clone(base); dup.certs[1].id = 'cert-1';
const norm = A.validateImport(dup);
ok(new Set(norm.certs.map(c => c.id)).size === norm.certs.length, 'ids duplicados sao corrigidos na importacao');

/* 8. UI e helpers não lançam com DOM inerte */
section('8. Funcoes de interface (smoke test)');
let uiOk = true;
try { A.renderCheckSource(); A.refreshCheckSourceUI(A.calculate(base)); } catch (e) { uiOk = false; console.log('  ' + e.message); }
ok(uiOk, 'renderCheckSource/refreshCheckSourceUI executam sem erro');
ok(typeof A.resolveCheck === 'function' && typeof A.newCertId === 'function' && typeof A.certCheckValues === 'function', 'API de teste exposta em window.Nitrito');

/* 9. Consistência estática: todo $('id') literal do script existe no HTML */
section('9. Consistencia de ids entre script e marcacao');
const declaredIds = new Set();
for (const idm of src.matchAll(/\sid="([^"]+)"/g)) declaredIds.add(idm[1]);
const usedIds = new Set();
for (const um of m[1].matchAll(/\$\('([A-Za-z][\w]*)'\)/g)) usedIds.add(um[1]);
const dynamicIds = new Set([...A.specs.map(s => s[0]), ...A.certSpec.map(s => s[0])]);
const missing = [...usedIds].filter(id => !declaredIds.has(id) && !dynamicIds.has(id));
ok(missing.length === 0, 'todos os ids usados em $() existem na marcacao', missing.join(', '));
const required = ['checkSource', 'checkSourceMsg', 'checkUnlink', 'checkFromMonthly', 'addReplica', 'dlGroup', 'dlRun', 'dlAnalyst', 'dlEquipment', 'dlLot'];
ok(required.every(id => declaredIds.has(id)), 'controles do vinculo e datalists presentes na marcacao', required.filter(id => !declaredIds.has(id)).join(', '));
ok(/data-add-row/.test(src) && /function addMonthlyRow/.test(src) && /addMonthlyRow\(\);return;/.test(src), 'linha "+" e handler de adicao de linha presentes');
ok(!/id="addMonthly"/.test(src) && !/\$\('addMonthly'\)/.test(src), 'botao "Adicionar resultado" removido (substituido pela linha +)');

/* 10. Código da corrida gerado da data + analista */
section('10. Codigo da corrida (ANA_ddMMMyy NO2- iniciais)');
ok(A.sessionCode('2026-01-05', 'Carlos Eduardo') === 'ANA_05JAN26 NO2- CE', 'padrao do enunciado', A.sessionCode('2026-01-05', 'Carlos Eduardo'));
ok(A.sessionCode('2026-01-25', 'Carlos Eduardo') === 'ANA_25JAN26 NO2- CE', 'dia 25 de janeiro', A.sessionCode('2026-01-25', 'Carlos Eduardo'));
ok(A.sessionCode('2026-03-09', 'Eduardo (CE)') === 'ANA_09MAR26 NO2- CE', 'apelido entre parenteses forca a sigla', A.sessionCode('2026-03-09', 'Eduardo (CE)'));
ok(A.sessionCode('2026-12-31', 'Ana Paula Souza') === 'ANA_31DEZ26 NO2- APS', 'dezembro (DEZ) e tres iniciais', A.sessionCode('2026-12-31', 'Ana Paula Souza'));
ok(A.sessionCode('2026-05-07', 'Jose Antonio') === 'ANA_07MAI26 NO2- JA', 'maio (MAI) e duas iniciais', A.sessionCode('2026-05-07', 'Jose Antonio'));
ok(A.sessionCode('', 'Carlos Eduardo') === '', 'sem data valida nao gera codigo', A.sessionCode('', 'Carlos Eduardo'));
ok(A.sessionCode('2026-01-05', '') === 'ANA_05JAN26', 'sem analista sai sem sufixo', A.sessionCode('2026-01-05', ''));
ok(A.analystCode('Carlos Eduardo') === 'CE' && A.analystCode('Eduardo (ce)') === 'CE', 'analystCode');
const t12 = clone(base); t12.autoRun = true;
A.syncRuns(t12);
ok(t12.monthly.every(r => r.run === A.sessionCode(r.date, r.analyst)), 'syncRuns preencheu todas as linhas');
const r12 = A.calculate(t12);
ok(r12.errors.length === 0 && near(r12.p.sip, r0.p.sip, 1e-12) && near(r12.U, r0.U, 1e-12), 'gerar a corrida automaticamente nao muda o resultado', r12.p.sip + ' vs ' + r0.p.sip);
const t13 = clone(base); delete t13.autoRun;
ok(A.validateImport(t13).autoRun === false, 'JSON antigo importa com a geracao automatica desligada');
const t14 = clone(base); t14.autoRun = true;
ok(A.validateImport(t14).autoRun === true, 'round-trip mantem a geracao automatica ligada');


/* 11. Linha "+" renderizada na tabela da precisão */
section('11. Linha "+" renderizada na tabela da precisao');
const tableHtml = captured.monthly || '';
ok(/class="addrow"/.test(tableHtml) && /data-add-row/.test(tableHtml), 'linha "+" presente no HTML renderizado');
const dataRows = (tableHtml.match(/data-remove-row=/g) || []).length;
ok(dataRows === base.monthly.length, 'uma linha de dados por resultado do exemplo', dataRows + ' vs ' + base.monthly.length);
ok(tableHtml.lastIndexOf('class="addrow"') > tableHtml.lastIndexOf('data-remove-row='), 'a linha "+" fica depois das linhas de dados');
ok(/colspan="9"/.test(tableHtml), 'a linha "+" ocupa as 9 colunas');

/* 12. Termos com definicao (hover) */
section('12. Termos com definicao (hover)');
const termKeys = [...new Set([...src.matchAll(/data-term="([^"]*)"/g)].map(m => m[1]))].filter(t => t && !t.includes('${'));
const semDef = termKeys.filter(t => !A.definitions[t]);
ok(A.definitions && typeof A.definitions === 'object', 'glossario exportado pela ferramenta', Object.keys(A.definitions || {}).length);
ok(termKeys.length >= 60, 'termos com definicao ao passar o mouse (' + termKeys.length + ')', termKeys.length);
ok(semDef.length === 0, 'todo termo tem definicao no glossario', semDef.join(', ') || 'ok');
ok(/function termify/.test(src) && /termify\(\);/.test(src) && /termify\(\);}/.test(src), 'termify definido e chamado apos a renderizacao');
ok(/tmap=\{A:'Tipo A/.test(src) && /tkey=\{A:'tipo A/.test(src), 'orcamento rotula Tipo A / Tipo B de forma explicita');
ok(!/CTRL-NIT/.test(src) && !/FORT-NIT/.test(src), 'sem a sigla NIT para nitrito (usar NO₂⁻)');
ok(/CTRL-N-NO₂⁻ 0,085 mg\/L/.test(src), 'grupo do exemplo so com material + concentracao');
const specTerms = [...A.specs, ...A.certSpec].map(s => s[4]).filter(Boolean);
ok(specTerms.length >= 15, 'rotulos de campo com definicao ao passar o mouse (' + specTerms.length + ')', specTerms.length);
ok(specTerms.every(t => A.definitions[t]), 'todo rotulo de campo tem definicao', specTerms.filter(t => !A.definitions[t]).join(', ') || 'ok');
ok(/Tipo A — estatística/.test(src) && /Tipo B — certificado/.test(src), 'tipos do orcamento escritos por extenso na tabela');

/* 13. Aba 04 (veracidade): aviso claro do que e opcional e do que e obrigatorio */
section('13. Aba 04: o que e opcional e o que e obrigatorio');
ok(near(A.calculate(base).b, (0.00995 - 0.010) / 0.010, 1e-12), 'vies do exemplo: check 0,00995 vs C ref 0,010', A.calculate(base).b);
ok(A.calculate(base).ur > 0 && A.calculate(base).budget.some(x => /Recuperação/.test(x.name)), 'com recuperacao a linha de matriz entra no orcamento (e opcional, nao automatica)', A.calculate(base).ur);
const semCheck = clone(base); semCheck.fields.checkValues = '';
const rSemCheck = A.calculate(semCheck);
ok(rSemCheck.errors.some(e => /Resultados do check/.test(e)), 'sem leituras do check: erro explicito', rSemCheck.errors.length);
ok(/informe pelo menos dois valores validos/.test(rSemCheck.errors.join(' ').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')), 'o minimo do check e 2 leituras');
const rc = clone(base); rc.includeRecovery = false; rc.fields.recoveries = '';
ok(A.calculate(rc).errors.length === 0, 'sem fortificacao o estudo continua valido (recuperacao e opcional)');
ok(!A.calculate(rc).budget.some(x => /Recuperação/.test(x.name)), 'desligar a fortificacao tira a linha do orcamento');
ok(/id="checkFromMonthly"/.test(src) && /Copiar valores para edição/.test(src), 'atalhos da aba 04 (preencher leituras do grupo e copiar valores)');

/* 14. Aba 04: separacao visual entre check obrigatorio e fortificacao opcional */
section('14. Aba 04: paineis separados (check x fortificacao)');
ok(/<fieldset class="bias-panel" id="checkPanel">/.test(src), 'bloco do check em painel proprio');
ok(/<fieldset class="bias-panel optional" id="recoveryPanel">/.test(src), 'bloco da fortificacao em painel opcional');
ok(/id="checkPanel"[\s\S]*?obrigatório/.test(src), 'painel do check marcado como obrigatorio');
ok(/id="recoveryPanel"[\s\S]*?opcional/.test(src), 'painel da fortificacao marcado como opcional');
ok(/id="biasStatus"/.test(src) && /function updateBiasStatus/.test(src), 'faixa de status do bloco obrigatorio');
const checkBlock = src.slice(src.indexOf('id="checkPanel"'), src.indexOf('id="recoveryPanel"'));
ok(!/id="recoveries"/.test(checkBlock) && !/id="spikeU"/.test(checkBlock), 'campos de recuperacao ficam fora do painel do check');
const recPanelEnd = src.indexOf('</fieldset>', src.indexOf('id="recoveryPanel"'));
const recBlock = src.slice(src.indexOf('id="recoveryPanel"'), recPanelEnd + 12);
ok(/id="includeRecovery"/.test(recBlock), 'caixa de recuperacao dentro do painel opcional');
ok(recBlock.indexOf('id="recoveryFields"') > 0, 'campos de recuperacao renderizados dentro do painel opcional');
ok(/function updateRecoveryAvailability/.test(src) && /\$\('includeRecovery'\)\.onchange/.test(src), 'caixa opcional controla a disponibilidade dos campos');
ok(/panel\.disabled=!on/.test(src) && /el\.disabled=!on/.test(src), 'campos de recuperacao desabilitados quando desligada');
ok(/bias-status required/.test(src) && /bias-status optional/.test(src), 'estilos de pendencia e de conclusao do bloco obrigatorio');
ok(/\['recoveries','spikeU','spikeOrigin','recoveryJustification'\]/.test(src), 'os quatro campos opcionais entram no controle de disponibilidade');
ok(/updateRecoveryAvailability\(\)/.test(src.slice(src.indexOf('function render()'), src.indexOf('function render()') + 800)), 'render inicial aplica o estado do painel opcional');
ok(typeof A.updateRecoveryAvailability === 'function' && typeof A.updateBiasStatus === 'function', 'funcoes de layout exportadas para teste');
/* Comportamento: campos de recuperacao bloqueados/liberados sem alterar o resultado */
const stRec = clone(base); stRec.includeRecovery = false;
const rOff = A.calculate(stRec);
ok(!rOff.budget.some(x => /Recuperação/.test(x.name)), 'desligada: linha de matriz fora do orcamento');
const stRecOn = clone(base); stRecOn.includeRecovery = true;
ok(A.calculate(stRecOn).budget.some(x => /Recuperação/.test(x.name)), 'ligada: linha de matriz dentro do orcamento');
ok(near(A.calculate(stRecOn).U, 0.005192, 5e-6) && near(rOff.U, 0.004377, 5e-6), 'U com e sem fortificacao do exemplo', rOff.U + ' / ' + A.calculate(stRecOn).U);
ok(/meta prática de 6 a 10/.test(src) && /Bloco 1 \(obrigatório\) pendente/.test(src), 'textos de status do bloco obrigatorio');
const blk = clone(base); blk.includeRecovery = true; blk.residualRecovery = false;
ok(A.calculate(blk).errors.some(e => /dupla contagem/i.test(e)), 'recuperacao ligada sem normalizacao pelo check: bloqueio de dupla contagem');
ok(/u<sub>fortificação,rel<\/sub>|u fortificação/.test(src), 'campo da incerteza da fortificacao ligado ao termo do glossario');

/* 15. Contrato do método real: base N-NO2-, faixa, check e ausência de FD */
section('15. Contrato do metodo de nitrito');
ok(base.schemaVersion === 2, 'JSON usa esquema v2 para impedir mistura silenciosa com a antiga base NO2-');
const legacySchema = clone(base); legacySchema.schemaVersion = 1;
let legacyRejected = false; try { A.validateImport(legacySchema); } catch (e) { legacyRejected = /versão 2/.test(e.message); }
ok(legacyRejected, 'JSON v1 e rejeitado ate conversao e revisao tecnica');
const dilutionIgnored = clone(base); dilutionIgnored.fields.dilution = '10';
ok(near(A.calculate(dilutionIgnored).y, r0.y, 1e-12), 'diluicao dos padroes nao multiplica o resultado da amostra');
const highRange = clone(base); highRange.fields.rangeMax = '0.151';
ok(A.calculate(highRange).errors.some(e => /não pode exceder 0,150/.test(e)), 'faixa configurada acima de 0,150 e bloqueada');
const atMaximum = clone(base); atMaximum.fields.concentration = '0.150';
ok(A.calculate(atMaximum).errors.length === 0, 'resultado em 0,150 e aceito como maximo permitido');
const wrongCheck = clone(base); wrongCheck.fields.checkValue = '0.100';
ok(A.calculate(wrongCheck).errors.some(e => /deve ser 0,010/.test(e)), 'check diferente de 0,010 e bloqueado');
const failedCheck = clone(base); failedCheck.fields.checkValues = '0.008\n0.008';
ok(A.calculate(failedCheck).errors.some(e => /fora do critério de aceitação/.test(e)), 'check fora de mais ou menos 10% bloqueia a liberacao');
ok(/duas leituras instrumentais da mesma alíquota devem ser promediadas/i.test(src), 'duplicatas instrumentais nao sao contadas como preparacoes independentes');

/* 16. Experimento visual reversível da versão 2.4 */
section('16. Tipos, gravacao de fontes e grafico de contribuicoes');
ok(/\['certificates','type-b','Incerteza Tipo B'\]/.test(src) && /\['precision','type-a','Incerteza Tipo A'\]/.test(src) && /\['bias','type-ab','Incerteza Tipo A\/B'\]/.test(src), 'caixas completas identificadas como Tipo A, B e A/B');
ok(/data-confirm-cert/.test(src) && /✓ Gravar/.test(src) && /✎ Editar/.test(src), 'botao compacto grava e permite reabrir a fonte');
ok(/c\.confirmed\?'disabled/.test(src) && /Fonte confirmada; clique em Editar/.test(src), 'campos ficam bloqueados depois da confirmacao');
ok(/filter\(x=>x\.c\.confirmed/.test(src), 'somente fontes gravadas alimentam novos vinculos');
const importedNoConfirmation = A.validateImport(clone(base));
ok(importedNoConfirmation.certs.every(c => c.confirmed === false), 'JSON anterior continua compativel e exige confirmacao explicita');
ok(/function renderBudgetChart/.test(src) && /Magnitude das contribuições/.test(src) && /participação na variância total/.test(src), 'painel lateral mostra magnitude e participacao na variancia');
ok(/\.budget-layout\{display:grid;grid-template-columns/.test(src) && /@media\(max-width:950px\)/.test(src), 'grafico fica a direita e empilha em telas menores');
ok(/Tabela compacta de fontes Tipo B/.test(src) && /uma por linha/.test(src) && !/class="cert-detail"/.test(src), 'cada fonte usa somente uma linha na tabela principal');
ok(/\['certificate','Fonte'\],\['certificate','Cert\.\/lote'\],\['value','Valor'\],\['unit','Unid\.'/ .test(src), 'fonte, certificado, valor e unidade ficam em colunas separadas');
ok(/function openCertDetails/.test(src) && /class="cert-drawer"/.test(src) && /aria-modal="true"/.test(src), 'detalhes abrem em painel lateral acessivel');
ok(/certDrawerClose/.test(src) && /data-close-cert-drawer/.test(src) && /e\.key==='Escape'/.test(src), 'painel fecha por botao, concluir e tecla Esc');
ok(/\.cert-actions\{display:flex/.test(src), 'acoes permanecem lado a lado');

/* 17. Importador auditavel de laudos Cary */
section('17. Importador de laudos PDF Cary');
const caryLines=['Concentration Analysis Report','Report time  26/11/2024 15:15:31','Application  ANA 26NOV24 NH4 CE.BCN','Instrument  Cary 300','Wavelength (nm)  630,00','Concentration units  mg/L','Sample  Concentration','PD 0,1 ppm  0,105  0,0916','Duplicate  0,104  0,0911','Mean Conc  0,104','AM6  0,003  -0,0097','Duplicate  0,004  -0,0096','Mean Conc  0,004','AM7  0,003  -0,0103','Duplicate  0,003  -0,0105','Mean Conc  0,003','AM8  0,005  -0,0086','Duplicate  0,005  -0,0084','Mean Conc  0,005'];
const parsedCary=A.parseCaryReport([{page:1,lines:caryLines,text:caryLines.join('\n')}],{fileName:'ANA 26NOV24 NH4 CE.pdf',hash:'fixture-hash'});
ok(parsedCary.equipment==='Cary 300'&&parsedCary.wavelength==='630.00'&&parsedCary.date==='2024-11-26','metadados da corrida Cary extraidos');
ok(parsedCary.testMode&&near(parsedCary.check.mean,.0104,1e-12)&&parsedCary.check.name==='PD 0,01 ppm','check NH4 adaptado ao nominal de nitrito somente no modo teste');
ok(parsedCary.samples.length===3&&parsedCary.samples.map(x=>x.name).join(',')==='AM6,AM7,AM8','AM6 a AM8 extraidas como amostras individuais');
ok(parsedCary.samples[0].readings.length===2&&near(parsedCary.samples[0].mean,.004,1e-12),'duplicatas preservadas e media reportada usada uma unica vez');
ok(base.monthly.length===24,'parser nao altera a precisao intermediaria');
const oldPdfJson=clone(base);delete oldPdfJson.importedReports;ok(Array.isArray(A.validateImport(oldPdfJson).importedReports),'JSON v2 anterior recebe lista vazia de laudos');
ok(/PDF_IMPORT_LIMITS/.test(src)&&/SHA-256/.test(src)&&/já foi importado/.test(src),'limites, auditoria por hash e bloqueio de duplicata presentes');
ok(/Resultados importados/.test(src)&&/incerteza não reportável/.test(src),'resultados finais e bloqueio de extrapolacao presentes');
let performanceRejected=false;try{A.parseCaryReport([{page:1,lines:['Cary Validation Report'],text:'Cary Validation Report\nSummary of Test Results'}],{fileName:'PERFORMANCE.pdf'});}catch(e){performanceRejected=/sem resultados analíticos importáveis/.test(e.message);}ok(performanceRejected,'relatorio PERFORMANCE nao cria contribuicao numerica');
ok(/pdf\.min\.js/.test(src)&&/pdf\.worker\.min\.js/.test(src),'PDF.js clássico e worker locais configurados para file://');

console.log('\n' + passed + ' verificacoes ok, ' + failed + ' falha(s).');
process.exit(failed ? 1 : 0);


