/** A/B：对比「分类结果缓存」开启 / 关闭时的 renderJobs 耗时（同一份 620 岗位数据）。 */
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright-core');
const ROOT = path.resolve(__dirname, '..');
const EXE = path.join(process.env.LOCALAPPDATA || '', 'ms-playwright', 'chromium-1228', 'chrome-win64', 'chrome.exe');

function mock(n) {
  const jobs = [];
  const cities = ['北京', '成都', '天津', '上海', '深圳'];
  const careers = ['人工智能/算法', '后端开发', '前端开发', '数据', '测试'];
  for (let i = 0; i < n; i++) jobs.push({
    record_id: 'j' + i, 公司: '测试公司' + i, 批次: '27秋招', 岗位方向: careers[i % 5], 工作地点: cities[i % 5],
    优先级: 'P2', 投递状态: '待投递', 网申开始: '2026-09-01T00:00:00Z',
    截止日期: new Date(2026, 8, 20 + (i % 40)).toISOString(),
    投递链接: [{ text: 'l', link: 'https://e.com/' + i }], 来源: '牛客', 备注: 'x', 牛客ID: '800',
  });
  return jobs;
}
const JOBS = mock(620);
const SELO = ['待投递', '已投递', '不投了'];
const SCHEMA = {
  GgZ71tywhs4HEZytFSqXTP: { properties: [['公司', 'text'], ['批次', 'select'], ['岗位方向', 'text'], ['工作地点', 'text'], ['优先级', 'select'], ['投递状态', 'select'], ['截止日期', 'date'], ['投递链接', 'url'], ['来源', 'text'], ['备注', 'text'], ['牛客ID', 'text']].map(([n, t]) => t === 'select' ? { name: n, type: 'select', config: { options: (n === '投递状态' ? SELO : ['27秋招', 'P2']).map((x, i) => ({ id: 'o' + i, text: x })) } } : { name: n, type: t }) },
  oBGkMFTv9Xv4Xn5gFOK18S: { properties: [{ name: '公司', type: 'text' }, { name: '岗位', type: 'text' }, { name: '当前阶段', type: 'select', config: { options: [{ id: 'a', text: '已投递' }] } }] },
  tgH8096uENTaIj8RSY9qm5: { properties: [{ name: '公司', type: 'text' }, { name: '岗位名称', type: 'text' }, { name: '投递状态', type: 'select', config: { options: SELO.map((x, i) => ({ id: 'i' + i, text: x })) } }] },
};
const TABLE = { GgZ71tywhs4HEZytFSqXTP: JOBS, oBGkMFTv9Xv4Xn5gFOK18S: [], tgH8096uENTaIj8RsY9qm5: [] };

async function measure(htmlPath, label) {
  const browser = await chromium.launch({ executablePath: EXE });
  const page = await browser.newPage();
  await page.addInitScript({ content: 'window.__SCHEMA__=' + JSON.stringify(SCHEMA) + ';window.__TABLE__=' + JSON.stringify(TABLE) + ';' });
  await page.addInitScript({ content: `window.__SMART_PAGE__={database:{
    getSchema:function(o){return Promise.resolve(JSON.parse(JSON.stringify(window.__SCHEMA__[o.databaseId])))},
    query:function(o){var all=window.__TABLE__[o.databaseId]||[];return Promise.resolve({results:JSON.parse(JSON.stringify(all)),nextCursor:null,hasMore:false})},
    addRecord:function(){return Promise.resolve({})},updateRecord:function(){return Promise.resolve({})},deleteRecord:function(){return Promise.resolve({})},onUpdated:function(){}}};` });
  await page.goto('file:///' + htmlPath.replace(/\\/g, '/'));
  await page.waitForFunction(() => { const e = document.getElementById('at_jobCards'); return e && e.querySelectorAll('.jcard').length > 0; }, { timeout: 20000 });
  const r = await page.evaluate(() => {
    const chip = document.querySelector('#at_batchChips .chip[data-mode=""]');
    const t = [];
    for (let k = 0; k < 15; k++) { const a = performance.now(); chip.click(); t.push(performance.now() - a); }
    t.sort((x, y) => x - y);
    return { median: t[7], p90: t[13] };
  });
  await browser.close();
  console.log(`${label}: renderJobs 中位数 ${r.median.toFixed(2)} ms · P90 ${r.p90.toFixed(2)} ms`);
  return r.median;
}

(async () => {
  const src = fs.readFileSync(path.join(ROOT, 'pages', '00-总览台.html'), 'utf8');
  const onPath = path.join(ROOT, 'pages', '_ab_cache_on.html');
  const offPath = path.join(ROOT, 'pages', '_ab_cache_off.html');
  fs.writeFileSync(onPath, src, 'utf8');
  // 关掉缓存：让 isSOE / mineMatch 每次都重算
  const off = src.replace(/if\(k in _clsCache\)return _clsCache\[k\];/g, '');
  if (off === src) { console.error('未找到缓存开关，A/B 无效'); process.exit(2); }
  fs.writeFileSync(offPath, off, 'utf8');
  const a = await measure(onPath, '开启分类缓存');
  const b = await measure(offPath, '关闭分类缓存');
  console.log(`→ 收益: 单次重渲染 ${(b - a).toFixed(2)} ms（${((b / a - 1) * 100).toFixed(0)}% 提升）`);
  fs.unlinkSync(onPath); fs.unlinkSync(offPath);
})().catch((e) => { console.error('AB FAILED:', e.message); process.exit(2); });
