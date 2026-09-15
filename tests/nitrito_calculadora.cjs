/* Run with: node tests/nitrito_calculadora.cjs <path-to-playwright-module>
   Uses an installed Chrome/Edge and file://; no application server or dependencies in the HTML. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require(process.argv[2] || 'playwright');
const root = path.resolve(__dirname, '..');
const target = process.env.NITRITO_HTML || 'index.html';
const artifacts = path.join(root, 'scratch', target.includes('_v2') ? 'nitrito_v2_qa' : 'nitrito_qa');
const close = (x,y,tol=1e-8)=>assert.ok(Math.abs(x-y)<tol, `${x} != ${y}`);
(async()=>{
  fs.mkdirSync(artifacts,{recursive:true});
  const browser = await chromium.launch({channel:'chrome',headless:true});
  const context = await browser.newContext({viewport:{width:1440,height:1000},offline:true});
  const page = await context.newPage();
  const errors=[],requests=[];
  page.on('pageerror',e=>errors.push(e.message));
  page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url());});
  page.on('dialog',d=>d.accept());
  await page.goto(pathToFileURL(path.join(root,target)).href);
  await page.waitForSelector('#result strong');
  const baseline=await page.evaluate(()=>Nitrito.calculate(Nitrito.example()));
  assert.deepEqual(baseline.errors,[]);
  close(baseline.y,.085); close(baseline.p.mean,.0846); close(baseline.p.s,.0021);
  close(baseline.check.mean,.00995); close(baseline.check.s,.0001125);
  close(baseline.b,-.005); close(baseline.recovery.mean,98.5);
  // Independent fixed-value evaluation; do not reuse the application's combine function.
  const expectedBias=Math.sqrt(.005**2+(.0001125/(Math.sqrt(10)*.010))**2+.003**2);
  const expectedMatrix=Math.sqrt(.015**2+.006**2+.003**2);
  const expectedUc=.085*Math.sqrt((.0021/.0846)**2+expectedBias**2+expectedMatrix**2);
  close(baseline.uc,expectedUc); close(baseline.U,2*expectedUc);
  assert.match(await page.locator('#result').innerText(),/0,0850 ± 0,0052/);
  const standard=baseline.certificates[0],balance=baseline.certificates[1],flask=baseline.certificates[2],pipette=baseline.certificates[3];
  close(standard.u,5);close(balance.u,.0001);close(flask.u,.1);close(pipette.u,.0025);
  close(baseline.budget.reduce((a,x)=>a+x.share,0),100);
  // Balanced random-effects study: within MS = 2; between MS = 4 => sIP = sqrt(3).
  const anova=await page.evaluate(()=>Nitrito.precision([
    {date:'2026-01-01',run:'a',result:'1'},{date:'2026-01-01',run:'a',result:'3'},
    {date:'2026-01-02',run:'b',result:'3'},{date:'2026-01-02',run:'b',result:'5'}]));
  close(anova.sip,Math.sqrt(3));
  const scenarios=await page.evaluate(()=>{
    const run=fn=>{const s=Nitrito.example();fn(s);return Nitrito.calculate(s);};
    return {
      empty:run(s=>s.fields.concentration=''), maxHigh:run(s=>s.fields.rangeMax='.151'),
      zeroK:run(s=>s.fields.coverage='0'),certK:run(s=>s.certs[0].k='0'),
      short:run(s=>s.monthly=s.monthly.slice(0,1)),expired:run(s=>s.certs[0].expiry='2020-01-01'),
      duplicated:run(s=>{s.certs[0].mode='include';s.certs[0].name='Analista';}),
      recovery:run(s=>s.residualRecovery=false),
      unbalanced:run(s=>{s.monthly[1].run=s.monthly[0].run;s.monthly[1].date=s.monthly[0].date;s.monthly[1].rep='2';}),
      independentCert:run(s=>s.certs[0].mode='include'),
      rectangle:run(s=>{s.certs[0].mode='include';s.certs[0].distribution='rect';}),
      resolution:run(s=>{s.certs[0].mode='include';s.certs[0].distribution='resolution';}),
      legacyDilution:run(s=>s.fields.dilution='2'),
      wrongCheck:run(s=>s.fields.checkValue='.011'),
      failedCheck:run(s=>s.fields.checkValues='.008\n.0081'),
      accept:run(s=>{s.fields.decisionMode='upper';s.fields.decisionAgreement='Acordo teste';s.fields.limit='.1';}),
      overlap:run(s=>{s.fields.decisionMode='upper';s.fields.decisionAgreement='Acordo teste';s.fields.limit='.085';}),
      reject:run(s=>{s.fields.decisionMode='upper';s.fields.decisionAgreement='Acordo teste';s.fields.limit='.07';})
    };
  });
  for(const name of ['empty','maxHigh','zeroK','certK','short','duplicated','recovery','unbalanced','wrongCheck','failedCheck'])assert.ok(scenarios[name].errors.length,name);
  assert.ok(scenarios.expired.warnings.some(x=>/vencido/.test(x)));
  close(scenarios.independentCert.uc,Math.sqrt(baseline.uc**2+(.085*.005)**2));
  close(scenarios.rectangle.certificates[0].u,10/Math.sqrt(3));
  close(scenarios.resolution.certificates[0].u,10/Math.sqrt(12));
  close(scenarios.legacyDilution.U,baseline.U);
  assert.match(scenarios.accept.decision,/^Conforme/);
  assert.match(scenarios.overlap.decision,/não demonstrada/);
  assert.match(scenarios.reject.decision,/^Não conforme/);
  await page.locator('#concentration').fill('');
  assert.equal(await page.locator('#print').isDisabled(),true);
  assert.match(await page.locator('#result').innerText(),/pendente/);
  await page.locator('#concentration').fill('0,085');
  assert.equal(await page.locator('#print').isEnabled(),true);
  const tip=page.locator('#identity .term');
  assert.ok(await tip.count()>0);await tip.first().focus();assert.equal(await page.locator('#identity .tip').first().isVisible(),true);
  await page.locator('#study').focus();
  await page.screenshot({path:path.join(artifacts,'desktop.png')});
  const download=async(id)=>{const promise=page.waitForEvent('download');await page.locator(id).click();const d=await promise;const target=path.join(artifacts,d.suggestedFilename());await d.saveAs(target);return target;};
  const jsonPath=await download('#export');const saved=JSON.parse(fs.readFileSync(jsonPath,'utf8'));
  const monthlyPath=await download('#csvMonthly');
  const budgetPath=await download('#csvBudget');
  assert.match(fs.readFileSync(budgetPath,'utf8'),/Precisão intermediária/);
  await page.locator('#concentration').fill('1');
  await page.locator('#import').setInputFiles(jsonPath);
  await page.waitForFunction(()=>document.querySelector('#concentration').value==='0,085');
  assert.equal(await page.locator('#concentration').inputValue(),'0,085');
  await page.locator('#import').setInputFiles({name:'invalid.json',mimeType:'application/json',buffer:Buffer.from('{bad')});
  assert.match(await page.locator('#status').innerText(),/não realizada/);
  assert.equal(await page.locator('#concentration').inputValue(),'0,085');
  await page.locator('#import').setInputFiles({name:'wrong.json',mimeType:'application/json',buffer:Buffer.from('{"schema":"wrong"}')});
  assert.match(await page.locator('#status').innerText(),/incompatível/);
  await page.locator('#importCsv').setInputFiles(monthlyPath);
  assert.equal(await page.locator('#monthlyTable tbody tr:not(.addrow)').count(),24);
  assert.match(await page.locator('#status').innerText(),/CSV importado/);
  await page.locator('#importCsv').setInputFiles({name:'wrong.csv',mimeType:'text/csv',buffer:Buffer.from('bad;header\n1;2')});
  assert.match(await page.locator('#status').innerText(),/Cabeçalhos incompatíveis/);
  // CSV quoting, decimal comma, newline and formula-injection handling.
  const csvRound=await page.evaluate(()=>Nitrito.parseCSV(Nitrito.csv([['a;b','x"y','line\nbreak','0,85','=1+1']])));
  assert.deepEqual(csvRound,[['a;b','x"y','line\nbreak','0,85',"'=1+1"]]);
  // Hostile imported text must remain text in both UI and printable report.
  const injected=structuredClone(saved);injected.fields.study='<img src=x onerror="window.pwned=1">';
  await page.locator('#import').setInputFiles({name:'safe.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(injected))});
  await page.waitForFunction(value=>document.querySelector('#study').value===value,injected.fields.study);
  assert.equal(await page.locator('#study').inputValue(),injected.fields.study);
  assert.equal(await page.evaluate(()=>window.pwned),undefined);
  await page.locator('#import').setInputFiles(jsonPath);
  await page.locator('#output').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(artifacts,'resultado.png')});
  await page.setViewportSize({width:390,height:844});
  await page.evaluate(()=>window.scrollTo(0,0));
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  await page.screenshot({path:path.join(artifacts,'mobile.png')});
  // PDF invokes beforeprint, generating the same full report as the print button.
  await page.emulateMedia({media:'print'});
  await page.pdf({path:path.join(artifacts,'memoria_exemplo.pdf'),format:'A4',printBackground:true});
  const report=await page.locator('#report').innerText();
  for(const text of ['0,0850 ± 0,0052','Certificados','Dados de precisão','Check e recuperação','Orçamento','Glossário','Assinatura'])assert.ok(report.includes(text),text);
  assert.ok(!(await page.locator('#report .tip').count()));
  await page.emulateMedia({media:'screen'});
  await page.locator('#new').click();
  assert.equal(await page.locator('#concentration').inputValue(),'');
  assert.equal(await page.locator('#monthlyTable tbody tr:not(.addrow)').count(),0);
  assert.equal(await page.locator('#print').isDisabled(),true);
  await page.locator('#example').click();
  assert.equal(await page.locator('#print').isEnabled(),true);
  assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);
  console.log(JSON.stringify({status:'PASS',uc:baseline.uc,U:baseline.U,checks:'numeric + ANOVA + invalid fields + certificates + decision + JSON/CSV + injection + offline + mobile + print',consoleErrors:errors,networkRequests:requests,artifacts},null,2));
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});
