/* _domcheck.js — abre a calculadora em um DOM real (jsdom opcional) ou avisa.
   Uso:  node guia_calculadora/_domcheck.js
   Verifica estrutura final do HTML: todos os ids existem, nenhum <div> orfao,
   paineis da aba 04 presentes e balanceados. Nao altera arquivos. */
'use strict';
const fs = require('fs');
const path = require('path');

const HTML = path.join(__dirname, '..', 'calculadora_incerteza_nitrito_v2.html');
const src = fs.readFileSync(HTML, 'utf8');
let fails = 0;
const ok = (cond, label, extra = '') => {
  console.log((cond ? '  ok    ' : '  FALHA ') + label + (cond ? '' : '   [' + extra + ']'));
  if (!cond) fails++;
};

console.log('=== estrutura do HTML ===');
const body = src.slice(src.indexOf('<body>'), src.indexOf('</body>'));
const opens = (body.match(/<div\b/g) || []).length;
const closes = (body.match(/<\/div>/g) || []).length;
ok(opens === closes, 'divs balanceados', opens + ' aberturas / ' + closes + ' fechamentos');
const fs1 = (body.match(/<fieldset\b/g) || []).length;
const fs2 = (body.match(/<\/fieldset>/g) || []).length;
ok(fs1 === 2 && fs2 === 2, 'dois fieldsets (check + recuperacao)', fs1 + '/' + fs2);

for (const id of ['biasStatus', 'checkPanel', 'recoveryPanel', 'biasFields', 'recoveryFields',
                  'checkSource', 'checkSourceMsg', 'independent', 'includeRecovery',
                  'residualRecovery', 'recoveryOffHint', 'biasStats', 'stats', 'budgetTable']) {
  ok(new RegExp('id="' + id + '"').test(body), 'id presente: ' + id);
}
ok(/id="outputFields"/.test(body), 'id presente: outputFields (aba 06)');
for (const id of ['biasStats', 'stats', 'budgetTable', 'result', 'issues']) {
  ok(new RegExp('id="' + id + '"').test(body), 'id presente: ' + id);
}
ok(!/\.\.\.<\/div>/.test(body), 'nenhum placeholder esquecido no HTML');

console.log('\n=== ordem dos paineis ===');
const iCheck = body.indexOf('id="checkPanel"');
const iRec = body.indexOf('id="recoveryPanel"');
const iForm = body.indexOf('id="biasStats"');
ok(iCheck > 0 && iRec > iCheck, 'painel do check vem antes do opcional');
ok(iForm > iRec, 'metricas ficam depois dos dois paineis');
const iSrc = body.indexOf('id="checkSource"');
ok(iSrc > iCheck && iSrc < iRec, 'fonte do check dentro do painel obrigatorio');

console.log('\n' + (fails ? fails + ' falha(s).' : 'estrutura ok, 0 falha(s).'));
process.exit(fails ? 1 : 0);
