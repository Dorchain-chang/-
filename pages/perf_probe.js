/**
 * 性能探针：注入 mock SDK（620 岗位），测量首屏、全量重渲染、筛选与分类缓存收益。
 * 用法: NODE_PATH=... node pages/perf_probe.js
 */
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright-core');

const ROOT = path.resolve(__dirname, '..');
const TARGET = path.join(ROOT, 'pages', '00-总览台.html');
const EXE = process.env.CHROME_EXE || path.join(process.env.LOCALAPPDATA || '', 'ms-playwright', 'chromium-1228', 'chrome-win64', 'chrome.exe');

function buildMock(n) {
  const jobs = [];
  const cities = ['北京', '成都', '天津', '上海', '深圳'];
  const careers = ['人工智能/算法', '后端开发', '前端开发', '数据', '测试'];
  for (let i = 0; i < n; i++) {
    jobs.push({
      record_id: 'job' + i, 公司: '测试公司' + i, 批次: '27秋招', 岗位方向: careers[i % 5],
      工作地点: cities[i % 5], 优先级: 'P2', 投递状态: i % 7 === 0 ? '已投递' : '待投递',
      网申开始: '2026-09-01T00:00:00Z', 截止日期: new Date(2026, 8, 20 + (i % 40)).toISOString(),
      投递链接: [{ text: '网申入口', link: 'https://example.com/' + i }], 来源: '牛客校招日程', 备注: '评价', 牛客ID: String(800 + i),
    });
  }
  const apps = [];
  for (let i = 0; i < 30; i++) apps.push({ record_id: 'app' + i, 公司: '投递公司' + i, 岗位: '算法', 当前阶段: '已投递', 投递日期: new Date(2026, 8, 1 + (i % 14)).toISOString(), 下次节点: new Date(2026, 8, 14 + (i % 10)).toISOString(), 节点说明: 'x', 复盘笔记: '', 相关链接: [{ text: 'l', link: 'https://e.com' }] });
  const interns = [];
  for (let i = 0; i < 60; i++) interns.push({ record_id: 'int' + i, 公司: '实习公司' + i, 岗位名称: '算法实习生', 薪资: '', 工作地点: '成都', 岗位要求: '实习', 投递状态: '待投递', 网申开始: '2026-09-05T00:00:00Z', 截止日期: new Date(2026, 8, 18 + (i % 30)).toISOString(), 投递链接: [{ text: 'l', link: 'https://e.com/i' + i }], 来源: '牛客校招日程', 备注: 'n', 牛客ID: String(900 + i) });
  return { jobs, apps, interns };
}

const DATA = buildMock(620);
const TABLE = { GgZ71tywhs4HEZytFSqXTP: DATA.jobs, oBGkMFTv9Xv4Xn5gFOK18S: DATA.apps, tgH8096uENTaIj8RSY9qm5: DATA.interns };
const SEL = ['待投递', '已投递', '不投了'];
const SCHEMA = {
  GgZ71tywhs4HEZytFSqXTP: { properties: [['公司', 'text'], ['批次', 'select'], ['岗位方向', 'text'], ['工作地点', 'text'], ['优先级', 'select'], ['投递状态', 'select'], ['网申开始', 'date'], ['截止日期', 'date'], ['投递链接', 'url'], ['来源', 'text'], ['备注', 'text'], ['牛客ID', 'text']].map(([n, t]) => t === 'select' ? { name: n, type: 'select', config: { options: (n === '投递状态' ? SEL : ['27秋招', 'P2']).map((x, i) => ({ id: 'o' + i, text: x })) } } : { name: n, type: t }) },
  oBGkMFTv9Xv4Xn5gFOK18S: { properties: [['公司', 'text'], ['岗位', 'text'], ['当前阶段', 'select'], ['投递日期', 'date'], ['下次节点', 'date'], ['节点说明', 'text'], ['复盘笔记', 'text'], ['相关链接', 'url']].map(([n, t]) => t === 'select' ? { name: n, type: 'select', config: { options: ['已投递', '笔试', '一面', 'Offer'].map((x, i) => ({ id: 's' + i, text: x })) } } : { name: n, type: t }) },
  tgH8096uENTaIj8RSY9qm5: { properties: [['公司', 'text'], ['岗位名称', 'text'], ['薪资', 'text'], ['工作地点', 'text'], ['岗位要求', 'text'], ['投递状态', 'select'], ['网申开始', 'date'], ['截止日期', 'date'], ['投递链接', 'url'], ['来源', 'text'], ['备注', 'text'], ['牛客ID', 'text']].map(([n, t]) => t === 'select' ? { name: n, type: 'select', config: { options: SEL.map((x, i) => ({ id: 'i' + i, text: x })) } } : { name: n, type: t }) },
};

(async () => {
  const browser = await chromium.launch({ executablePath: EXE });
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  // 暴露内部刷新入口，便于循环压测
  await page.addInitScript({ content: 'window.__SCHEMA__=' + JSON.stringify(SCHEMA) + ';window.__TABLE__=' + JSON.stringify(TABLE) + ';' });
  await page.addInitScript({ content: `
    window.__MOCK__={queries:0,handlers:[]};
    window.__SMART_PAGE__={database:{
      getSchema:function(o){return Promise.resolve(JSON.parse(JSON.stringify(window.__SCHEMA__[o.databaseId])))},
      query:function(o){window.__MOCK__.queries++;var all=window.__TABLE__[o.databaseId]||[],size=o.pageSize||50,start=0;
        if(o.startCursor){var i=all.findIndex(function(r){return r.record_id===o.startCursor});start=i<0?0:i+1}
        var pg=all.slice(start,start+size),last=pg.length?pg[pg.length-1].record_id:null;
        return Promise.resolve({results:JSON.parse(JSON.stringify(pg)),nextCursor:last,hasMore:start+size<all.length})},
      addRecord:function(){return Promise.resolve({})},updateRecord:function(){return Promise.resolve({})},deleteRecord:function(){return Promise.resolve({})},
      onUpdated:function(h){window.__MOCK__.handlers.push(h)}
    }};
    // 把四个模块的 refresh 挂出来做压测
    window.__bench=function(){var t=performance.now();window.__REFRESH_ALL__&&window.__REFRESH_ALL__();return performance.now()-t};
  ` });
  const t0 = Date.now();
  await page.goto('file:///' + TARGET.replace(/\\/g, '/'));
  await page.waitForFunction(() => {
    const el = document.getElementById('at_jobCards');
    return el && el.querySelectorAll('.jcard').length > 0 && !/加载中/.test(el.textContent);
  }, { timeout: 25000 }).catch(async (e) => {
    const dump = await page.evaluate(() => ({
      hint: (document.getElementById('at_jobCnt') || {}).textContent,
      cards: (document.getElementById('at_jobCards') || {}).innerHTML.slice(0, 200),
      queries: window.__MOCK__ ? window.__MOCK__.queries : 'no mock',
      schemaLoaded: !!(window.__SCHEMA__),
      tableLoaded: !!(window.__TABLE__),
      jobRows: window.__TABLE__ ? window.__TABLE__.GgZ71tywhs4HEZytFSqXTP.length : -1,
      appRows: window.__TABLE__ ? window.__TABLE__.oBGkMFTv9Xv4Xn5gFOK18S.length : -1,
    }));
    console.error('等待渲染超时:', JSON.stringify(dump));
    console.error('页面错误:', errors);
    throw e;
  });
  const firstPaint = Date.now() - t0;

  // 暴露 refreshAll：它在 IIFE 里，通过点击「全部批次」chip 触发一次 renderJobs 来测量
  const bench = await page.evaluate(async () => {
    const chip = document.querySelector('#at_batchChips .chip[data-mode=""]');
    const times = [];
    for (let k = 0; k < 12; k++) {
      const t = performance.now();
      chip.click();                       // 触发 renderJobs()（走分类缓存 + 全卡片重建）
      times.push(performance.now() - t);
    }
    // 再测一次热力图 + 今日处理（overview.refresh）
    const tabs = document.querySelectorAll('nav.tabbar .tab');
    const t2 = performance.now();
    for (let k = 0; k < 12; k++) { tabs[0].click(); tabs[1].click(); }
    const viewSwitch = (performance.now() - t2) / 12;
    times.sort((a, b) => a - b);
    return { median: times[6], max: times[times.length - 1], viewSwitch: viewSwitch };
  });

  const mem = await page.evaluate(() => performance.memory ? { used: Math.round(performance.memory.usedJSHeapSize / 1048576) } : null);
  const scale = await page.evaluate(() => ({
    queries: window.__MOCK__.queries,
    domNodes: document.getElementsByTagName('*').length,
    jobCards: document.querySelectorAll('#at_jobCards .jcard').length,
  }));

  console.log('=== 性能探针（620 岗位 / 30 跟踪 / 60 实习）===');
  console.log('首屏可交互(ms):', firstPaint);
  console.log('query 请求次数:', scale.queries, '（pageSize=200）');
  console.log('renderJobs 中位数(ms):', bench.median.toFixed(2), '| 最差(ms):', bench.max.toFixed(2));
  console.log('视图切换平均(ms):', bench.viewSwitch.toFixed(2));
  console.log('渲染出的岗位卡片:', scale.jobCards, '| DOM 节点:', scale.domNodes);
  console.log('JS 堆(used MB):', mem ? mem.used : 'n/a');
  console.log('页面错误:', errors.length ? errors : '无');
  await browser.close();
})().catch((e) => { console.error('PERF FAILED:', e.message); process.exit(2); });
