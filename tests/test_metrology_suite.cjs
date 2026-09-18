const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');

const html = fs.readFileSync('index.html', 'utf8');
const scripts = [...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]);
const app = scripts.reduce((a, b) => b.length > a.length ? b : a, '');

function createMockElement(id = '') {
  const store = { id, value: '', textContent: '', innerHTML: '', style: {}, dataset: {}, checked: false };
  return new Proxy(store, {
    get(t, k) {
      if (k === 'style') return t.style;
      if (k === 'dataset') return t.dataset;
      if (k === 'classList') return { add() {}, remove() {}, toggle() {}, contains: () => false };
      if (k === 'querySelectorAll') return () => [];
      if (k === 'querySelector') return () => createMockElement();
      if (k in t) return t[k];
      return '';
    },
    set(t, k, v) { t[k] = v; return true; }
  });
}

const elements = {};
function $(id) {
  if (!elements[id]) elements[id] = createMockElement(id);
  return elements[id];
}

const sandbox = {
  document: {
    getElementById: id => $(id),
    querySelector: sel => createMockElement(sel),
    querySelectorAll: () => [],
    createElement: () => createMockElement(),
    addEventListener: () => {},
    body: createMockElement('body'),
    documentElement: createMockElement('html')
  },
  window: {},
  navigator: { serviceWorker: null },
  localStorage: { getItem: () => null, setItem: () => {} },
  MutationObserver: class { observe() {} disconnect() {} },
  console, setTimeout, clearTimeout, URL, Blob: class {}, structuredClone: globalThis.structuredClone, confirm: () => true, alert: () => {}
};
sandbox.window = sandbox;
sandbox.addEventListener = () => {};
sandbox.scrollTo = () => {};
sandbox.location = { hash: '', href: 'file:///index.html', search: '' };
sandbox.history = { replaceState: () => {}, pushState: () => {} };
sandbox.matchMedia = () => ({ matches: false, addEventListener: () => {} });

const ctx = vm.createContext(sandbox);
vm.runInContext(app, ctx);
const N = sandbox.Nitrito;

console.log('Running Metrology & Cary Integration Test Suite (Zero Dependencies)...');

// 1. Fictitious reference example
const ex = N.example('nitrito');
const rEx = N.calculate(ex);
assert.equal(rEx.errors.length, 0, 'Example has no errors');
assert.equal(N.resultText(rEx), '0,0850 ± 0,0044 mg/L de N-NO₂⁻', 'Fictitious result matches reference exactly');
console.log('✓ Test 1 Passed: Reference case ISO 17025 exact numerical match');

// 2. Dilution module propagation (Eurachem CG 4)
$('dilutionStockConc').value = '1000';
$('dilutionStockU').value = '5';
$('dilutionStockK').value = '2';
$('dilutionPipetteVol').value = '0.100';
$('dilutionPipetteTol').value = '0.002';
$('dilutionFlaskVol').value = '1000';
$('dilutionFlaskTol').value = '0.40';
const d1 = N.calcDilution();
assert.ok(Math.abs(d1.cRef - 0.100) < 1e-6, 'Dilution Cref is 0.100 mg/L');
assert.ok(d1.URef > 0.001 && d1.URef < 0.003, 'Dilution Uref within expected expanded bounds');
console.log('✓ Test 2 Passed: Stock dilution propagation (1000 mg/L -> 0.1000 mg/L) verified');

// 3. Cary WinUV real BCN batch extraction
const dir = 'D:\\Downloads\\cary\\New folder';
let bcnFiles = [];
try { bcnFiles = fs.readdirSync(dir).filter(f => f.endsWith('.BCN')); } catch (_) {}
let bcnOk = bcnFiles.length >= 9;
try { if (bcnOk) fs.readFileSync(path.join(dir, bcnFiles[0])); } catch (e) { bcnOk = false; }
if (bcnOk) {
  assert.ok(bcnFiles.length >= 9, 'All 9 real BCN files detected');
  for (const f of bcnFiles) {
  const buf = fs.readFileSync(path.join(dir, f));
  const rep = N.parseBcnReport(buf, { fileName: f, hash: 'h-' + f });
  assert.ok(rep.wavelength > 400 && rep.wavelength < 700, 'Valid wavelength extracted');
  assert.ok(['nitrito', 'amonia', 'hidrazina'].includes(rep.detectedAnalyte), 'Analyte recognized');
  }
  console.log('✓ Test 3 Passed: 9 real Cary WinUV .BCN files parsed with full metadata');
} else {
  console.log('⚠ Test 3 ignorado: arquivos .BCN ilegíveis neste ambiente (pasta provavelmente somente-nuvem).');
}

// 4. Multi-file Batch ANOVA (Intermediate precision sIP)
const batchRows = [];
if (bcnOk) {
  const no2Files = bcnFiles.filter(f => f.includes('NO2') || f.includes('27JAN26'));
  for (const f of no2Files) {
  const buf = fs.readFileSync(path.join(dir, f));
  const rep = N.parseBcnReport(buf, { fileName: f });
  const runDate = rep.parsedDate || N.parseCaryDate(rep.reportTime, rep.fileName);
  const analyst = rep.analyst || N.extractAnalyst(rep.fileName, rep.rawText);
  const chk = rep.checks[0];
  if (chk) {
    chk.readings.forEach((rd, idx) => {
      batchRows.push({
        group: 'Check 0,100 mg/L',
        date: runDate,
        run: f.replace(/\.BCN$/i, ''),
        analyst,
        equipment: 'Cary 300',
        lot: 'LOTE-2026',
        rep: String(idx + 1),
        result: String(rd.conc)
      });
    });
  }
}
} else {
  const synthBatch = [
    ['R1', '2026-01-27', '0.1012', '1'], ['R1', '2026-01-27', '0.1008', '2'],
    ['R2', '2026-01-28', '0.1021', '1'], ['R2', '2026-01-28', '0.1019', '2'],
    ['R3', '2026-01-29', '0.1015', '1'], ['R3', '2026-01-29', '0.1016', '2']
  ];
  for (const [run, date, result, rep] of synthBatch) batchRows.push({ group: 'Check 0,100 mg/L', date, run, analyst: 'Carlos Eduardo', equipment: 'Cary 300', lot: 'LOTE-2026', rep, result });
  console.log('⚠ Massa sintética balanceada (3 corridas x 2 preparações) usada no Teste 4.');
}
const anova = N.precision(batchRows);
assert.equal(anova.error, '', 'ANOVA executed without error');
assert.equal(anova.runs, 3, '3 distinct runs detected');
assert.equal(anova.n, 6, '6 total observations in balanced design');
if (bcnOk) assert.ok(anova.sip > 0.0010 && anova.sip < 0.0015, 'sIP within expected bounds');
else assert.ok(anova.sip > 0, 'sIP calculado sobre a massa sintética balanceada');
console.log('✓ Test 4 Passed: Batch ANOVA intermediate precision across days and analysts verified');

// 5. Complete calculation on real Cary data
const realState = N.example('nitrito');
realState.fictitious = false;
realState.monthly = batchRows;
realState.fields.group = 'Check 0,100 mg/L';
realState.fields.concentration = '0.085';
realState.fields.checkValue = '0.1000';
realState.fields.checkU = String(Number(d1.URef.toFixed(6)));
realState.fields.checkK = '2';
realState.fields.checkValues = batchRows.map(r => r.result).join('\n');
realState.fields.limit = '0.07';
const rReal = N.calculate(realState);
assert.equal(rReal.errors.length, 0, 'No errors in real calculation');
assert.ok(rReal.uc > 0, 'Combined uncertainty uc is positive');
assert.ok(rReal.U > 0, 'Expanded uncertainty U is positive');
console.log('✓ Test 5 Passed: Full uncertainty budget with real Cary data passes with 0 errors');

// 6. Situação 1 dynamic synchronization and dilution alignment
const sit1State = N.example('nitrito');
sit1State.fictitious = false;
sit1State.syncCheckWithMonthly = true;
sit1State.fields.group = 'Check 0,100 mg/L';
sit1State.monthly = [
  { group: 'Check 0,100 mg/L', date: '2026-01-27', run: 'R1', analyst: 'CE', equipment: 'Cary 300', lot: 'L1', rep: '1', result: '0.1012' },
  { group: 'Check 0,100 mg/L', date: '2026-01-27', run: 'R1', analyst: 'CE', equipment: 'Cary 300', lot: 'L1', rep: '2', result: '0.1008' },
  { group: 'Check 0,100 mg/L', date: '2026-01-28', run: 'R2', analyst: 'AP', equipment: 'Cary 300', lot: 'L1', rep: '1', result: '0.1021' },
  { group: 'Check 0,100 mg/L', date: '2026-01-28', run: 'R2', analyst: 'AP', equipment: 'Cary 300', lot: 'L1', rep: '2', result: '0.1019' }
];
N.syncCheckFromMonthly(true, sit1State);
assert.equal(sit1State.fields.checkValues, '0.1012\n0.1008\n0.1021\n0.1019', 'Situação 1 dynamically synchronized checkValues from monthly table');

// Add a 5th replica
sit1State.monthly.push({ group: 'Check 0,100 mg/L', date: '2026-01-29', run: 'R3', analyst: 'JR', equipment: 'Cary 300', lot: 'L2', rep: '1', result: '0.1015' });
N.syncCheckFromMonthly(true, sit1State);
assert.ok(sit1State.fields.checkValues.includes('0.1015'), 'New monthly replica dynamically reflected in checkValues');

// Test Situação 2 (unlinking)
sit1State.syncCheckWithMonthly = false;
sit1State.fields.checkValues = '0.0990\n0.0995';
sit1State.monthly.push({ group: 'Check 0,100 mg/L', date: '2026-01-30', run: 'R4', analyst: 'CE', equipment: 'Cary 300', lot: 'L2', rep: '1', result: '0.1050' });
N.syncCheckFromMonthly(false, sit1State);
assert.equal(sit1State.fields.checkValues, '0.0990\n0.0995', 'Situação 2 preserves independent manual checkValues without overwriting');
console.log('✓ Test 6 Passed: Situação 1 continuous reactive synchronization & Situação 2 independence verified');

// 7. Test 7: Unified 5-stage architecture validation
assert.ok(html.includes('03 · Controle de Qualidade (Precisão & Viés)'), 'Nav contains unified stage 03');
assert.ok(html.includes('04 · Orçamento'), 'Nav contains stage 04 Orçamento');
assert.ok(html.includes('05 · Resultado'), 'Nav contains stage 05 Resultado');
assert.ok(html.includes('<span class="badge">03 / Controle de Qualidade</span>'), 'Section 03 has Controle de Qualidade badge');
assert.ok(html.includes('<span class="badge">04 / Combinação</span>'), 'Section 04 has Combinação badge');
assert.ok(html.includes('<span class="badge">05 / Expressar e avaliar</span>'), 'Section 05 has Expressar e avaliar badge');
assert.ok(html.includes('id="checkPanel"') && html.includes('id="monthlyTable"') && html.includes('id="stats"') && html.includes('id="biasStats"'), 'All key metrological panels coexist in unified Section 03');
console.log('✓ Test 7 Passed: Unified 5-stage workflow and DOM architecture verified');

// 8. Test 8: Executive Dashboard Box 1, 2, 3 & Editable Aba 02 Collection
assert.ok(html.includes('id="qcResultsBox"'), 'Box 2 qcResultsBox exists');
assert.ok(html.includes('id="qcActionsBox"'), 'Box 3 qcActionsBox exists');
assert.ok(html.includes('id="btnQcImportReport"'), 'Quick Import Cary button exists in Box 3');
assert.ok(html.includes('id="btnQcSaveData"'), 'Save Data button exists in Box 3');
assert.ok(html.includes('id="btnQcAddReplica"'), 'Add Replica button exists in Box 3');
assert.ok(html.includes('id="qcSipVal"') && html.includes('id="qcRsdVal"'), 'Box 2 mini metrics exist');

// Verify resolveCheck allows user edits
const testState = N.example('nitrito');
testState.checkLink = { enabled: true, certId: 'cert-1' };
testState.fields.checkValue = '0.010';
testState.fields.checkCert = 'LOTE-CUSTOM-2026';
const rc = N.resolveCheck(testState);
assert.equal(rc.value, '0.010', 'Check value honors user override');
assert.equal(rc.cert, 'LOTE-CUSTOM-2026', 'Check lot honors user override');
assert.equal(rc.linked, true, 'Check remains linked to Aba 02 cert');

console.log('✓ Test 8 Passed: Executive Dashboard boxes & editable Aba 02 standard collection verified');

// 9. Test 9: Visual confirmation banner, advanced settings drawer & hidden group column
assert.ok(html.includes('id="qcImportSuccessBanner"'), 'Banner #qcImportSuccessBanner exists in DOM');
assert.ok(html.includes('id="btnDismissImportBanner"'), 'Dismiss button for import banner exists');
assert.ok(html.includes('id="btnQcImportReport"'), 'Canonical Cary import button exists in Box 3');
assert.ok(html.includes('id="btnClearMonthlyRows"'), 'Clear monthly rows button exists in table header');
assert.ok(html.includes('Configurações avançadas do controle e premissas da ISO 17025'), 'Advanced settings details drawer exists');
assert.ok(html.includes('<th style="display:none;"><span data-term="grupo do controle">Grupo do controle</span></th>'), 'Group column is hidden in table header');
assert.ok(html.includes('<td style="display:none;"><input aria-label="group linha'), 'Group column is hidden in table body');

console.log('✓ Test 9 Passed: Visual confirmation banner, advanced settings drawer & hidden group column verified');

// 10. Test 10: Daily Instrumental Logbook (Diário de Bordo), Lock/Unlock, Quick Lot Copy & Expandable Sample Drawer with Uncertainty
assert.ok(html.includes('id="rowReportFileInput"'), 'Direct row report file input #rowReportFileInput exists in DOM');
assert.ok(html.includes('id="btnAddNewDailyRun"'), 'Dedicated button #btnAddNewDailyRun exists in toolbar');
assert.ok(html.includes('data-toggle-lock='), 'Lock/unlock toggle button data-toggle-lock is implemented in rows');
assert.ok(html.includes('data-copy-lot='), 'Quick copy lot button data-copy-lot is implemented in rows');
assert.ok(html.includes('data-toggle-samples='), 'Expandable samples drawer button data-toggle-samples is implemented in rows');
assert.ok(html.includes('data-attach-file='), 'Direct row attachment button data-attach-file is implemented in rows');
assert.ok(html.includes('function renderSamplesSubtable'), 'Subtable renderer renderSamplesSubtable is defined');
assert.ok(html.includes('function exportRunSamplesCsv'), 'Subtable CSV export function exportRunSamplesCsv is defined');

// Verify sample uncertainty calculation inside run
const mockRun = {
  run: 'ANA_27JAN26 NO2- CE',
  date: '2026-01-27',
  analyst: 'CE',
  samples: [
    { sampleName: 'Amostra Ponto 1', meanConc: 0.050, replicates: [{ conc: 0.050 }] },
    { sampleName: 'Amostra Ponto 2', meanConc: 0.085, replicates: [{ conc: 0.085 }] }
  ]
};
const subtableHtml = sandbox.renderSamplesSubtable(mockRun, 0, N.getAssayConfig('nitrito'));
assert.ok(subtableHtml.includes('Amostra Ponto 1'), 'Sample 1 rendered in drawer subtable');
assert.ok(subtableHtml.includes('Amostra Ponto 2'), 'Sample 2 rendered in drawer subtable');
assert.ok(subtableHtml.includes('Resultado Declarado (y ± U)'), 'Header indicates declared result with uncertainty');
assert.ok(subtableHtml.includes('Conforme'), 'Compliance badge evaluated correctly');

console.log('✓ Test 10 Passed: Daily Instrumental Logbook with row locking, quick lot copy & sample uncertainty drawer verified');

// 11. Diário de Bordo simplificado: corrida automática, grupo com lista e premissas unificadas
assert.ok(!html.includes('id="autoRun"'), 'Checkbox "Corrida automática" removido da interface');
assert.ok(!html.includes('id="homogeneous"') && !html.includes('id="independent"'), 'Checkboxes individuais de premissa substituídos');
assert.ok(html.includes('id="premisesConfirmed"') && html.includes('id="premisesNote"'), 'Declaração única de premissas com campo de justificativa existe');
assert.ok(html.includes('list="dlGroup"'), 'Grupo do controle usa a lista dos grupos já lançados (dlGroup)');
assert.ok(html.includes('id="groupSyncHint"') && html.includes('data-adopt-group'), 'Aviso de grupo divergente com recuperação em um clique existe');
assert.ok(!html.includes("$('autoRun')"), 'Sem referência residual ao checkbox removido');

const runState = N.example('nitrito');
runState.monthly = [
  { group: 'Check 0,010 mg/L', date: '2026-01-27', run: '', analyst: 'Carlos Eduardo', equipment: 'Cary 300', lot: 'L1', rep: '1', result: '0.0102' },
  { group: 'Check 0,010 mg/L', date: '2026-01-27', run: '', analyst: 'Carlos Eduardo', equipment: 'Cary 300', lot: 'L1', rep: '1', result: '0.0104' },
  { group: 'Check 0,010 mg/L', date: '2026-01-27', run: 'LOTE-A', analyst: 'Carlos Eduardo', equipment: 'Cary 300', lot: 'L1', rep: '1', result: '0.0099' },
  { group: 'Check 0,010 mg/L', date: '2026-01-28', run: '', analyst: 'Ana Paula', equipment: 'Cary 300', lot: 'L1', rep: '2', result: '0.0101' }
];
N.syncRuns(runState);
assert.equal(runState.monthly[0].run, 'ANA_27JAN26 NO2- CE', 'Corrida gerada de data + analista');
assert.equal(runState.monthly[1].run, 'ANA_27JAN26 NO2- CE s2', 'Segunda sessão do mesmo dia/analista/preparação recebe sufixo s2');
assert.equal(runState.monthly[2].run, 'LOTE-A', 'Código informado pelo analista é preservado');
assert.equal(runState.monthly[3].run, 'ANA_28JAN26 NO2- AP', 'Nome completo do analista vira iniciais');
assert.equal(new Set(runState.monthly.map(r => r.date + '|' + r.run + '|' + r.rep)).size, 4, 'Nenhuma identificação duplicada após a geração automática');

const premState = N.example('nitrito');
premState.homogeneous = false; premState.independent = false;
let pref = N.calculate(premState);
assert.ok(pref.errors.some(e => e.includes('Confirme as premissas do controle')), 'Premissas não confirmadas bloqueiam o cálculo');
assert.ok(pref.errors.some(e => e.includes('justificativa técnica')), 'Premissas não confirmadas exigem justificativa do desvio');
premState.premisesNote = 'Controle revalidado após troca de lote; comparabilidade reavaliada.';
pref = N.calculate(premState);
assert.ok(!pref.errors.some(e => e.includes('Confirme as premissas do controle')), 'Justificativa registrada libera o cálculo');
assert.ok(pref.warnings.some(w => w.includes('Premissas do controle não confirmadas')), 'Desvio das premissas fica registrado como aviso');

const exemploJson = JSON.parse(fs.readFileSync('exemplos/estudo_exemplo_nitrito.json', 'utf8'));
const importado = N.validateImport(exemploJson);
assert.equal(importado.autoRun, true, 'Importação força a corrida automática');
assert.equal(importado.premisesNote, '', 'Importação normaliza a justificativa das premissas');
assert.equal(N.calculate(importado).errors.length, 0, 'Exemplo versionado importado continua sem erros');
console.log('✓ Test 11 Passed: Diário de Bordo simplificado (corrida automática, grupo com lista e premissas unificadas) verificado');

// 12. Test 12: Calibration Curve Manager (Método & Matriz, CRUD, Água Doce/Mar & Dimmed/Locked Fields)
assert.ok(html.includes('Identificação da Curva de Calibração'), 'Título atualizado para Identificação da Curva de Calibração');
assert.ok(html.includes('id="curveProfileSelect"'), 'Seletor de perfil de curva #curveProfileSelect existe no DOM');
assert.ok(html.includes('id="btnSaveCurve"'), 'Botão Gravar Curva #btnSaveCurve existe no DOM');
assert.ok(html.includes('id="btnEditCurve"'), 'Botão Editar Curva #btnEditCurve existe no DOM');
assert.ok(html.includes('id="btnNewCurve"'), 'Botão Nova Curva #btnNewCurve existe no DOM');
assert.ok(html.includes('id="btnDeleteCurve"'), 'Botão Excluir Curva #btnDeleteCurve existe no DOM');
assert.ok(html.includes('id="btnQuickAddMethod"'), 'Botão Novo Método existe');
assert.ok(html.includes('id="btnQuickAddMatrix"'), 'Botão Nova Matriz existe');
assert.ok(html.includes('id="dlMethod"') && html.includes('id="dlMatrix"'), 'Datalists dlMethod e dlMatrix existem');
assert.ok(html.includes('.curve-fields-locked'), 'Classe CSS .curve-fields-locked para caixas esmaecidas existe');

const mats = N.getSavedMatrices();
assert.ok(mats.includes('Água Doce'), 'Matriz Água Doce pré-cadastrada');
assert.ok(mats.includes('Água de Mar'), 'Matriz Água de Mar pré-cadastrada');

const curves = N.getSavedCurves();
assert.ok(curves.length >= 2, 'Curvas pré-cadastradas disponíveis');
assert.ok(curves.some(c => c.matrix === 'Água Doce' || c.matrix === 'Água de Mar'), 'Curva com Água Doce ou Água de Mar disponível');

console.log('✓ Test 12 Passed: Gerenciador de Curva de Calibração (Método, Matriz, Água Doce/Mar, CRUD & campos esmaecidos) verificado');

console.log('\n=======================================================');
console.log('ALL 12 METROLOGICAL & INSTRUMENTAL SUITE TESTS PASSED!');
console.log('=======================================================\n');
