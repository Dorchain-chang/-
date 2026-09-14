/**
 * 生产单文件的浏览器冒烟测试：注入 mock SDK，跑通完整初始化链路。
 * 用法: node pages/smoke_browser.js
 */
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright-core');

const ROOT = path.resolve(__dirname, '..');
const TARGET = path.join(ROOT, 'pages', process.env.PAGE || '00-总览台.html');

// 造数据：秋招 620 条（跨多页）、投递跟踪 6 条、实习 40 条
function buildMock() {
  const jobs = [];
  const cities = ['北京', '成都', '天津', '上海', '深圳'];
  const careers = ['人工智能/算法', '后端开发', '前端开发', '数据', '测试'];
  const batches = ['27秋招', '27暑期实习', '其他'];
  for (let i = 0; i < 620; i++) {
    const d = new Date(2026, 8, 20 + (i % 40));
    jobs.push({
      record_id: 'job' + i,
      公司: '测试公司' + i,
      批次: batches[i % 3],
      岗位方向: careers[i % 5],
      工作地点: cities[i % 5],
      优先级: i % 3 === 0 ? 'P1' : 'P2',
      投递状态: i % 7 === 0 ? '已投递' : '待投递',
      网申开始: '2026-09-01T00:00:00Z',
      截止日期: d.toISOString(),
      投递链接: [{ text: '网申入口', link: 'https://example.com/' + i }],
      来源: '牛客校招日程',
      备注: '测试评价',
      牛客ID: String(800 + i),
    });
  }
  const apps = [];
  for (let i = 0; i < 6; i++) {
    apps.push({
      record_id: 'app' + i,
      公司: '投递公司' + i,
      岗位: '大模型算法',
      当前阶段: ['已投递', '笔试', '一面', 'Offer', '感谢信', '已终止'][i],
      投递日期: new Date(2026, 8, 1 + i).toISOString(),
      下次节点: new Date(2026, 8, 14 + i).toISOString(),
      节点说明: '节点说明' + i,
      复盘笔记: '',
      相关链接: [{ text: '链接', link: 'https://example.com/app' + i }],
    });
  }
  const interns = [];
  for (let i = 0; i < 40; i++) {
    interns.push({
      record_id: 'int' + i,
      公司: '实习公司' + i,
      岗位名称: '算法实习生',
      薪资: '',
      工作地点: '成都',
      岗位要求: '27届日常实习',
      投递状态: '待投递',
      网申开始: '2026-09-05T00:00:00Z',
      截止日期: new Date(2026, 8, 18 + (i % 30)).toISOString(),
      投递链接: [{ text: '投递入口', link: 'https://example.com/intern' + i }],
      来源: '牛客校招日程',
      备注: '牛客同步',
      牛客ID: String(900 + i),
    });
  }
  const inbox = [
    { record_id: 'ibx0', 公司: '字节跳动', 类型: '笔试', 事项时间: new Date(2026, 8, 20).toISOString(), 原文摘要: '笔试邀请：9月20日 14:00 在线测评', 发件人: 'noreply@bytedance.com', 来源: '邮件', 状态: '待确认', 置信度: '高' },
    { record_id: 'ibx1', 公司: '美团', 类型: '面试', 事项时间: new Date(2026, 8, 22).toISOString(), 原文摘要: '面试邀请：9月22日 10:00 视频面试', 发件人: 'careers@meituan.com', 来源: '邮件', 状态: '待确认', 置信度: '高' },
    { record_id: 'ibx2', 公司: '百度', 类型: 'Offer', 事项时间: new Date(2026, 8, 10).toISOString(), 原文摘要: '录用意向通知', 发件人: 'offer@baidu.com', 来源: '邮件', 状态: '已确认', 置信度: '高' },
  ];
  return { jobs, apps, interns, inbox };
}

const DATA = buildMock();
const SCHEMA = {
  GgZ71tywhs4HEZytFSqXTP: { properties: [
    '公司', '批次', '岗位方向', '工作地点', '优先级', '投递状态', '网申开始', '截止日期',
    '投递链接', '来源', '备注', '牛客ID',
  ].map((n) => ({ name: n, type: n === '投递状态' || n === '优先级' || n === '批次' ? 'select' : 'text' })) },
  oBGkMFTv9Xv4Xn5gFOK18S: { properties: ['公司', '岗位', '当前阶段', '投递日期', '下次节点', '节点说明', '复盘笔记', '相关链接'].map((n) => ({ name: n, type: 'text' })) },
  tgH8096uENTaIj8RSY9qm5: { properties: ['公司', '岗位名称', '薪资', '工作地点', '岗位要求', '投递状态', '网申开始', '截止日期', '投递链接', '来源', '备注', '牛客ID'].map((n) => ({ name: n, type: 'text' })) },
};
// 给 select 字段补 options
SCHEMA.GgZ71tywhs4HEZytFSqXTP.properties.forEach((p) => {
  if (p.name === '投递状态') p.config = { options: [{ id: 's1', text: '待投递' }, { id: 's2', text: '已投递' }, { id: 's3', text: '不投了' }] };
  if (p.name === '优先级') p.config = { options: [{ id: 'p1', text: 'P1' }, { id: 'p2', text: 'P2' }] };
  if (p.name === '批次') p.config = { options: [{ id: 'b1', text: '27秋招' }, { id: 'b2', text: '27暑期实习' }, { id: 'b3', text: '其他' }] };
});
SCHEMA.oBGkMFTv9Xv4Xn5gFOK18S.properties.forEach((p) => {
  if (p.name === '当前阶段') { p.type = 'select'; p.config = { options: ['已投递', '笔试', '一面', '二面', 'HR面', 'Offer', '感谢信', '已终止'].map((t, i) => ({ id: 'st' + i, text: t })) }; }
});
SCHEMA.tgH8096uENTaIj8RSY9qm5.properties.forEach((p) => {
  if (p.name === '投递状态') { p.type = 'select'; p.config = { options: [{ id: 's1', text: '待投递' }, { id: 's2', text: '已投递' }, { id: 's3', text: '不投了' }] }; }
});
SCHEMA.EdCHnKtjZIXEw37tUmvhqL = { properties: ['公司', '类型', '事项时间', '原文摘要', '发件人', '来源', '状态', '置信度', '消息ID', '收件时间'].map((n) => ({ name: n, type: 'text' })) };
SCHEMA.EdCHnKtjZIXEw37tUmvhqL.properties.forEach((p) => {
  if (p.name === '类型') { p.type = 'select'; p.config = { options: [{ id: 't1', text: '笔试' }, { id: 't2', text: '面试' }, { id: 't3', text: 'Offer' }, { id: 't4', text: '感谢信' }, { id: 't5', text: '其他' }] }; }
  if (p.name === '来源') { p.type = 'select'; p.config = { options: [{ id: 'm1', text: '邮件' }, { id: 'm2', text: '短信' }, { id: 'm3', text: '浏览器扩展' }] }; }
  if (p.name === '状态') { p.type = 'select'; p.config = { options: [{ id: 'w1', text: '待确认' }, { id: 'w2', text: '已确认' }, { id: 'w3', text: '已忽略' }] }; }
  if (p.name === '置信度') { p.type = 'select'; p.config = { options: [{ id: 'c1', text: '高' }, { id: 'c2', text: '中' }, { id: 'c3', text: '低' }] }; }
});

const TABLE = { GgZ71tywhs4HEZytFSqXTP: DATA.jobs, oBGkMFTv9Xv4Xn5gFOK18S: DATA.apps, tgH8096uENTaIj8RSY9qm5: DATA.interns, EdCHnKtjZIXEw37tUmvhqL: DATA.inbox };

const MOCK = `
(function(){
  window.__MOCK__={queries:0,onUpdatedCalls:0,writes:0,handlers:[],fired:0,uncaught:[]};
  window.addEventListener('error',function(e){window.__MOCK__.uncaught.push(String(e.message))});
  window.__SMART_PAGE__={database:{
    getSchema:function(o){return Promise.resolve(JSON.parse(JSON.stringify(window.__SCHEMA__[o.databaseId])))},
    query:function(o){window.__MOCK__.queries++;
      var all=window.__TABLE__[o.databaseId]||[],size=o.pageSize||50;
      var start=0;
      if(o.startCursor){var i=all.findIndex(function(r){return r.record_id===o.startCursor});start=i<0?0:i+1}
      var page=all.slice(start,start+size);
      var last=page.length?page[page.length-1].record_id:null;
      return Promise.resolve({results:JSON.parse(JSON.stringify(page)),nextCursor:last,hasMore:start+size<all.length});
    },
    addRecord:function(){window.__MOCK__.writes++;return Promise.resolve({record_id:'new'})},
    updateRecord:function(){window.__MOCK__.writes++;return Promise.resolve({})},
    deleteRecord:function(){window.__MOCK__.writes++;return Promise.resolve({})},
    onUpdated:function(h){window.__MOCK__.onUpdatedCalls++;window.__MOCK__.handlers.push(function(p){window.__MOCK__.fired++;return h(p)})}
  }};
})();
`;

(async () => {
  const EXE = process.env.CHROME_EXE || path.join(process.env.LOCALAPPDATA || '', 'ms-playwright', 'chromium-1228', 'chrome-win64', 'chrome.exe');
  const browser = await chromium.launch(fs.existsSync(EXE) ? { executablePath: EXE } : { channel: 'chromium' });
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
  page.on('console', (m) => {
    if (m.type() === 'error') errors.push('console.error: ' + m.text());
    else if (process.env.DEBUG) console.log('PAGE>', m.text());
  });

  await page.addInitScript({ content: 'window.__SCHEMA__=' + JSON.stringify(SCHEMA) + ';window.__TABLE__=' + JSON.stringify(TABLE) + ';' });
  await page.addInitScript({ content: MOCK });
  const t0 = Date.now();
  await page.goto('file:///' + TARGET.replace(/\\/g, '/'));
  await page.waitForFunction(() => {
    const el = document.getElementById('ov_todayCnt');
    const cards = document.getElementById('at_jobCards');
    return el && cards && !/加载中/.test(cards.textContent);
  }, { timeout: 15000 });
  const tInit = Date.now() - t0;

  const r = await page.evaluate(() => {
    const q = (id) => document.getElementById(id);
    const mock = window.__MOCK__;
    const cards = document.querySelectorAll('#at_jobCards .jcard');
    return {
      queries: mock.queries, onUpdatedCalls: mock.onUpdatedCalls, writes: mock.writes,
      syncTxt: (q('syncTxt') || {}).textContent,
      today: (q('ov_todayList') || {}).innerHTML.length,
      todayCnt: (q('ov_todayCnt') || {}).textContent,
      autumnCards: cards.length,
      autumnCnt: (q('at_jobCnt') || {}).textContent,
      soeCards: document.querySelectorAll('#so_jobCards .jcard').length,
      internCards: document.querySelectorAll('#ir_jobCards .jcard').length,
      heatCells: document.querySelectorAll('#hmGrid .hm-cell').length,
      heatSum: (q('hmSum') || {}).textContent,
      cityOptions: (q('at_fCity') || { options: [] }).options.length,
      careerOptions: (q('at_fCareer') || { options: [] }).options.length,
      batchChips: document.querySelectorAll('#at_batchChips .chip').length,
      domNodes: document.getElementsByTagName('*').length,
      uncaught: mock.uncaught,
      views: document.querySelectorAll('.view').length,
    };
  });

  // 交互：切 Tab → 筛选城市 → 打开公司情报（带牛客ID 深链）→ 热力图弹层
  await page.click('nav.tabbar .tab[data-view="autumn"]');
  await page.click('#at_batchChips .chip[data-mode="autumn"]');
  const afterChip = await page.textContent('#at_jobCnt');
  await page.selectOption('#at_fCity', { index: 2 });
  const afterCity = await page.textContent('#at_jobCnt');
  await page.click('#at_jobCards .jsearch');
  const intel = await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('#intelBody .igoto')).map((b) => b.getAttribute('data-u'));
    return { secs: document.querySelectorAll('#intelBody .isec').length, items: btns.length, hasEnterprise: btns.some((u) => /enterprise\/\d+/.test(u)), sample: btns.slice(0, 3) };
  });
  const intelOpen = await page.evaluate(() => getComputedStyle(document.getElementById('intelModal')).display !== 'none');
  await page.click('#intelClose');
  await page.click('nav.tabbar .tab[data-view="overview"]');
  await page.click('#hmGrid .hm-cell:nth-child(80)');
  const hmOpen = await page.evaluate(() => getComputedStyle(document.getElementById('hmModal')).display !== 'none');
  const hmDetail = await page.textContent('#hmDetail');
  await page.click('#hmClose');

  // 阶段快捷 UI：卡片有 已投/不投 快键；点阶段标签展开全部阶段选项（不点选项，避免触发写库）
  const stageUi = await page.evaluate(() => {
    const card = document.querySelector('#appCards .acard, #ov_appCards .acard');
    if (!card) return null;
    const qy = card.querySelector('.aquick');
    const qn = card.querySelector('.aquick2');
    const tag = card.querySelector('[data-field="当前阶段"]');
    const box = card.querySelector('.astagebox');
    if (!tag || !box) return null;
    const hiddenBefore = box.hidden;
    tag.click();
    const chips = Array.from(box.querySelectorAll('.schip')).map((b) => b.textContent);
    const visibleAfter = !box.hidden;
    const curMarked = !!box.querySelector('.schip.cur');
    tag.click();
    const hiddenAfterToggle = box.hidden;
    return { hasQuick: !!qy && !!qn, quickTxt: [qy && qy.textContent, qn && qn.textContent], hiddenBefore, visibleAfter, chips, curMarked, hiddenAfterToggle };
  });

  // 情报收件箱：待确认渲染 / 确认展开写入条 / 默认阶段映射 / 写库
  const inboxUi = await page.evaluate(() => {
    const cnt = document.getElementById('ibCnt') || document.getElementById('ov_ibCnt');
    const box = document.getElementById('ibCards') || document.getElementById('ov_ibCards');
    const cards = box ? Array.from(box.querySelectorAll('.acard')) : [];
    return { cnt: cnt ? cnt.textContent : '', n: cards.length, companies: cards.map((c) => { const b = c.querySelector('[data-field="公司"]'); return b ? b.textContent : ''; }) };
  });
  await page.click('#ibCards .acard .ibok, #ov_ibCards .acard .ibok');
  const pickVisible = await page.evaluate(() => { const p = document.querySelector('#ibCards .acard .ibpick, #ov_ibCards .acard .ibpick'); return !!p && p.style.display !== 'none'; });
  const defStage = await page.evaluate(() => { const p = document.querySelector('#ibCards .acard .ibpick select, #ov_ibCards .acard .ibpick select'); return p ? p.value : ''; });
  const writesBefore = await page.evaluate(() => window.__MOCK__.writes);
  await page.click('#ibCards .acard .ibpick button.btn-pri, #ov_ibCards .acard .ibpick button.btn-pri');
  await page.waitForTimeout(600);
  const writesAfter = await page.evaluate(() => window.__MOCK__.writes);

  await page.click('nav.tabbar .tab[data-view="autumn"]');

  // 外部数据变更订阅：模拟他人在表格改数据 → 页面应自动重拉
  // 先静置 1.5s 以上，避开「刚拉过数就跳过」的回声抑制窗口
  await page.waitForTimeout(1600);
  const beforeQueries = await page.evaluate(() => window.__MOCK__.queries);
  await page.evaluate(() => { window.__MOCK__.handlers.forEach((h) => h({ databaseIds: ['GgZ71tywhs4HEZytFSqXTP'] })); });
  await page.waitForTimeout(1600);
  const afterQueries = await page.evaluate(() => window.__MOCK__.queries);
  const fired = await page.evaluate(() => window.__MOCK__.fired);

  // 内存/规模指标
  const mem = await page.evaluate(() => (performance.memory ? {
    usedMB: Math.round(performance.memory.usedJSHeapSize / 1048576),
    totalMB: Math.round(performance.memory.totalJSHeapSize / 1048576),
  } : null));

  console.log('--- 初始化 ---');
  console.log('初始化耗时(ms):', tInit);
  console.log('同步状态:', r.syncTxt, '| query 次数:', r.queries, '| onUpdated 注册:', r.onUpdatedCalls);
  console.log('--- 渲染 ---');
  console.log('今日处理条目数:', r.todayCnt, '| 区块 HTML 长度:', r.today);
  console.log('秋招卡片:', r.autumnCards, '计数文案:', r.autumnCnt, '| 央国企卡片:', r.soeCards, '| 实习卡片:', r.internCards);
  console.log('热力图格子:', r.heatCells, '| 摘要:', r.heatSum);
  console.log('城市选项:', r.cityOptions, '| 职业选项:', r.careerOptions, '| 批次 chips:', r.batchChips, '| 视图数:', r.views);
  console.log('DOM 节点总数:', r.domNodes);
  console.log('--- 交互 ---');
  console.log('切Tab+我的批次 后:', afterChip, '| 选城市后:', afterCity);
  console.log('情报面板: 分区', intel.secs, '条目', intel.items, '含牛客企业深链:', intel.hasEnterprise, '| 打开:', intelOpen);
  console.log('  样例链接:', intel.sample.join(' , '));
  console.log('热力图弹层打开:', hmOpen, '| 明细:', String(hmDetail).slice(0, 70));
  if (!stageUi) { console.error('阶段快捷UI: 未找到卡片/标签'); errors.push('stage UI missing'); }
  else {
    console.log('阶段快捷UI: 快键', stageUi.quickTxt.join('/'), '| 展开前隐藏:', stageUi.hiddenBefore, '| 点击后展开:', stageUi.visibleAfter, '| 当前阶段高亮:', stageUi.curMarked, '| 再点收起:', stageUi.hiddenAfterToggle);
    console.log('  阶段选项:', stageUi.chips.join(' · '));
    if (!stageUi.hasQuick || !stageUi.visibleAfter || !stageUi.curMarked || !stageUi.hiddenAfterToggle) errors.push('stage UI broken');
  }
  console.log('情报收件箱: 待确认', inboxUi ? inboxUi.n : '无', '条 计数', inboxUi && inboxUi.cnt, '| 公司:', inboxUi ? inboxUi.companies.join('/') : '-');
  console.log('  确认→展开写入条:', pickVisible, '| 默认阶段:', defStage, '| 写库次数', writesBefore, '→', writesAfter);
  if (!inboxUi || inboxUi.n !== 2 || !pickVisible || defStage !== '笔试' || writesAfter - writesBefore < 2) errors.push('inbox UI broken');

  // 主题色面板
  const theme = await page.evaluate(() => {
    const b = document.getElementById('themebtn');
    if (!b) return { ok: false };
    b.click();
    const pop = document.getElementById('themepop');
    const open = !!pop && pop.classList.contains('open');
    const sws = pop ? Array.from(pop.querySelectorAll('.sw')) : [];
    if (sws[2]) sws[2].click();
    const pri = getComputedStyle(document.documentElement).getPropertyValue('--pri').trim();
    const grad = getComputedStyle(document.documentElement).getPropertyValue('--grad');
    const saved = localStorage.getItem('wb_theme');
    const rgbVar = getComputedStyle(document.documentElement).getPropertyValue('--pri-rgb').trim();
    localStorage.removeItem('wb_theme');
    return { ok: true, open, n: sws.length, pri, gradHas: grad.indexOf('linear-gradient') === 0, saved, rgbVar };
  });
  console.log('主题面板: 打开=', theme.open, '| 预设数=', theme.n, '| 切预设后 --pri=', theme.pri, '| 渐变生效=', theme.gradHas, '| 持久化=', theme.saved, '| --pri-rgb=', theme.rgbVar);
  if (!theme.ok || !theme.open || theme.n < 7 || !theme.gradHas) errors.push('theme picker broken');
  console.log('--- 实时订阅 ---');
  console.log('外部变更前 query:', beforeQueries, '→ 后:', afterQueries, '| 触发重拉:', afterQueries > beforeQueries, '| handler 实际执行次数:', fired);
  if (mem) console.log('JS 堆: 已用', mem.usedMB, 'MB / 总量', mem.totalMB, 'MB');
  console.log('--- 错误 ---');
  console.log('未捕获错误:', r.uncaught.length ? r.uncaught : '无');
  console.log('控制台/页面错误:', errors.length ? errors : '无');

  await browser.close();
  process.exit(errors.length || r.uncaught.length ? 1 : 0);
})().catch((e) => { console.error('SMOKE FAILED:', e); process.exit(2); });
