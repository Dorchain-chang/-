#!/usr/bin/env python3
"""Build ONE single-file app that merges all 4 workbench pages.

Reuses build_pages.py generators, extracts each page's <body> sections + <script>,
namespaces element IDs and state fields per module, then merges into a single HTML
where the top nav switches views in-page (no navigation, data fetched once).

Deploy target: same single file is pushed to all 4 nodes so every existing link
opens the full app.
"""
import os, re, sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import build_pages as bp

MODULES = ["overview", "autumn", "soe", "intern"]

# ---- per-module ID lists (from body templates) + prefix ----
IDS = {
    "overview": ["todayCnt","todayMine","todayList","stWait","stDone","stDdl","stLive",
                 "cntAutumn","cntSOE","cntIntern","appCnt","appForm","fStage","funnelSvg",
                 "appCards","tplBox","tplApp"],
    "autumn":   ["jobCnt","jobForm","fBatch","fPrio","batchChips","q","fCity","fCareer",
                 "fSt","fBatchF","filterHint","jobCards","tplBox","tplJob"],
    "soe":      ["jobCnt","jobForm","fBatch","fPrio","q","fCity","fCareer","fSt",
                 "filterHint","jobCards","tplBox","tplJob"],
    "intern":   ["jobCnt","internForm","q","fSt","filterHint","jobCards","tplBox","tplJob"],
}
PREFIX = {"overview": "ov", "autumn": "at", "soe": "so", "intern": "ir"}

# shared `state.<field>` fields that must be namespaced (used by multiple modules)
STATE_FIELDS = ["fBatchF", "fSt", "fCity", "fCareer", "q"]

REFRESH_LINE = {
    "overview": "function refreshAll(){renderToday();renderStats();renderModuleCounts();renderFunnel();renderApps();}",
    "autumn":   "function refreshAll(){renderFilterFacets();renderJobs();}",
    "soe":      "function refreshAll(){renderFilterFacets();renderJobs();}",
    "intern":   "function refreshAll(){renderInterns();}",
}

# hand-written per-module registration (bind/setup) replacing the old init()
TAIL = {
"overview": """
MODS.push({refresh:function(){renderToday();renderStats();renderModuleCounts();renderFunnel();renderApps();},setup:function(){fillStageOv();},bind:function(){
  bindSubmitApp();
  bindFormCache('ov_appForm');
  $('ov_todayMine').addEventListener('change',function(){state.todayMine=$('ov_todayMine').checked;renderToday()});
}});
function fillStageOv(){
  var sel=$('ov_fStage');if(!sel)return;sel.innerHTML='';var o0=document.createElement('option');o0.value='';o0.textContent='请选择';sel.appendChild(o0);
  (OPTS['当前阶段']||[]).forEach(function(o){var oo=document.createElement('option');oo.value=o.id;oo.textContent=o.text;sel.appendChild(oo)});
}
""",
"autumn": """
MODS.push({refresh:function(){renderFilterFacets();renderJobs();},setup:function(){renderSelectOptions();},bind:function(){
  bindSubmitJob();
  $('at_q').addEventListener('input',function(){state.at_q=$('at_q').value.trim();renderJobs()});
  $('at_fSt').addEventListener('change',function(){state.at_fSt=$('at_fSt').value;renderJobs()});
  $('at_fBatchF').addEventListener('change',function(){state.at_fBatchF=$('at_fBatchF').value;renderJobs()});
  $('at_fCity').addEventListener('change',function(){state.at_fCity=$('at_fCity').value;renderJobs()});
  $('at_fCareer').addEventListener('change',function(){state.at_fCareer=$('at_fCareer').value;renderJobs()});
  Array.prototype.forEach.call(document.querySelectorAll('#at_batchChips .chip'),function(ch){
    ch.addEventListener('click',function(){state.batchMode=ch.getAttribute('data-mode');Array.prototype.forEach.call(document.querySelectorAll('#at_batchChips .chip'),function(x){x.className='chip'+(x===ch?' active':'')});renderJobs();});
  });
}});
""",
"soe": """
MODS.push({refresh:function(){renderFilterFacets();renderJobs();},setup:function(){renderSelectOptions();},bind:function(){
  bindSubmitJob();
  $('so_q').addEventListener('input',function(){state.so_q=$('so_q').value.trim();renderJobs()});
  $('so_fSt').addEventListener('change',function(){state.so_fSt=$('so_fSt').value;renderJobs()});
  $('so_fCity').addEventListener('change',function(){state.so_fCity=$('so_fCity').value;renderJobs()});
  $('so_fCareer').addEventListener('change',function(){state.so_fCareer=$('so_fCareer').value;renderJobs()});
}});
""",
"intern": """
MODS.push({refresh:function(){renderInterns();},setup:function(){renderSelectOptions();},bind:function(){
  bindSubmitIntern();
  bindFormCache('ir_internForm');
  $('ir_q').addEventListener('input',function(){state.ir_q=$('ir_q').value.trim();renderInterns()});
  $('ir_fSt').addEventListener('change',function(){state.ir_fSt=$('ir_fSt').value;renderInterns()});
}});
""",
}

NAV_SINGLE = """
<nav class="tabbar">
  <div class="inner">
    <a class="logo" data-goto="overview"><svg viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>秋招求职台</a>
    <button type="button" class="tab" data-view="overview">总览</button>
    <button type="button" class="tab" data-view="autumn">秋招岗位</button>
    <button type="button" class="tab" data-view="soe">央国企</button>
    <button type="button" class="tab" data-view="intern">实习直通</button>
    <div class="sync" id="syncBox"><span class="dot"></span><span id="syncTxt">连接中…</span></div>
  </div>
</nav>
"""

CSS_EXTRA = """
nav.tabbar .tab{cursor:pointer;font-family:inherit}
.view{display:none}
.view.active{display:block}
"""

BOOT_JS = r"""
function showView(name){
  Array.prototype.forEach.call(document.querySelectorAll('.view'),function(v){v.className='view'+(v.id==='view_'+name?' active':'')});
  Array.prototype.forEach.call(document.querySelectorAll('nav.tabbar .tab'),function(t){if(t.getAttribute('data-view')===name){t.setAttribute('aria-current','page')}else{t.removeAttribute('aria-current')}});
  try{history.replaceState(null,'','#'+name)}catch(e){}
  window.scrollTo(0,0);
}
function bindTabs(){
  Array.prototype.forEach.call(document.querySelectorAll('nav.tabbar .tab'),function(t){t.addEventListener('click',function(){showView(t.getAttribute('data-view'))})});
  Array.prototype.forEach.call(document.querySelectorAll('[data-goto]'),function(a){a.addEventListener('click',function(e){e.preventDefault();showView(a.getAttribute('data-goto'))})});
  var h=(location.hash||'').replace('#','');
  showView(['overview','autumn','soe','intern'].indexOf(h)>=0?h:'overview');
}
function boot(){
  db=window.__SMART_PAGE__&&window.__SMART_PAGE__.database;
  bindIntelClose();
  bindExpress();
  $('lnkClose').addEventListener('click',function(){$('lnkModal').style.display='none'});
  $('lnkModal').addEventListener('click',function(e){if(e.target===$('lnkModal'))$('lnkModal').style.display='none'});
  bindTabs();
  if(!db){goOffline();return}
  setText('syncTxt','已同步');
  MODS.forEach(function(m){m.bind&&m.bind()});
  Promise.all([db.getSchema({databaseId:'GgZ71tywhs4HEZytFSqXTP'}),db.getSchema({databaseId:'oBGkMFTv9Xv4Xn5gFOK18S'}),db.getSchema({databaseId:'tgH8096uENTaIj8RSY9qm5'})]).then(function(ss){
    ss.forEach(function(schema){(schema.properties||[]).forEach(function(f){if((f.type==='select'||f.type==='multi_select')&&f.config&&f.config.options){OPTS[f.name]=f.config.options}})});
    MODS.forEach(function(m){m.setup&&m.setup()});
    return reloadAll();
  }).catch(function(e){console.error('[database] 初始化失败:',e);goOffline()});
}
if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',boot)}else{boot()}
"""


def extract(html):
    """Return (hero, wrap_body, script_js) from a built page."""
    i_nav_end = html.index("</nav>") + len("</nav>")
    i_wrap = html.index('<div class="wrap">')
    hero = html[i_nav_end:i_wrap].strip()
    i_lnk = html.index('<div id="lnkModal"')
    seg = html[i_wrap + len('<div class="wrap">'):i_lnk]
    seg = seg.strip()
    # drop leading offBanner (re-added once globally) and trailing wrap close
    seg = re.sub(r'^<div class="banner" id="offBanner">.*?</div>\s*', '', seg, flags=re.S)
    assert seg.endswith('</div>'), 'body should end with wrap close'
    seg = seg[: seg.rindex('</div>')]
    m = re.search(r'<script>(.*?)</script>', html, re.S)
    return hero, seg, m.group(1)


def prefix_ids(text, mod, is_js):
    p = PREFIX[mod]
    for x in IDS[mod]:
        if is_js:
            text = text.replace("$('%s')" % x, "$('%s_%s')" % (p, x))
            text = text.replace("setText('%s'" % x, "setText('%s_%s'" % (p, x))
            text = text.replace("fillSelect('%s'" % x, "fillSelect('%s_%s'" % (p, x))
            text = text.replace("bindFormCache('%s'" % x, "bindFormCache('%s_%s'" % (p, x))
            text = text.replace("'#%s" % x, "'#%s_%s" % (p, x))
            # indirect reference via pairs array: ['fCity',cities,'全部城市']
            text = text.replace("['%s'," % x, "['%s_%s'," % (p, x))
        else:
            text = text.replace('id="%s"' % x, 'id="%s_%s"' % (p, x))
    return text


def build_module_js(mod, page_js):
    p = PREFIX[mod]
    # namespace shared state fields
    for f in STATE_FIELDS:
        page_js = page_js.replace("state.%s" % f, "state.%s_%s" % (p, f))
    # dynamic funnel ids (overview)
    page_js = page_js.replace("$('fbar'", "$('ov_fbar'").replace("$('fcnt'", "$('ov_fcnt'")
    page_js = page_js.replace("'fbar'+i", "'ov_fbar'+i").replace("'fcnt'+i", "'ov_fcnt'+i")
    page_js = prefix_ids(page_js, mod, is_js=True)
    # drop old refreshAll definition
    page_js = page_js.replace(REFRESH_LINE[mod] + "\n", "")
    # drop trailing init() + goOffline()
    i = page_js.index("function init(){")
    page_js = page_js[:i].rstrip() + "\n"
    return "(function(){\n" + page_js + TAIL[mod] + "\n})();\n"


def build():
    pages = {k: getattr(bp, "page_%s" % k)(bp.URLS) for k in MODULES}
    shared_done = False
    module_blocks = []
    views = []
    for mod in MODULES:
        hero, body, js = extract(pages[mod])
        # shared js = everything up to end of reloadAll definition
        marker = "function reloadAll(){return loadData().then(function(){refreshAll()});}"
        idx = js.index(marker) + len(marker)
        if not shared_done:
            shared = js[:idx]
            shared_done = True
        module_js = js[idx:]
        # strip old boot tail
        cut = module_js.index("\nif(document.readyState==='loading')")
        module_js = module_js[:cut]
        # overview: module cards -> in-page goto
        if mod == "overview":
            for key in MODULES:
                body = re.sub(r'<a class="moduleCard[^"]*" target="_top" href="%s"' % re.escape(bp.URLS[key]),
                              '<a class="moduleCard" data-goto="%s"' % key, body)
        body = prefix_ids(body, mod, is_js=False)
        module_blocks.append("/* ====== module: %s ====== */\n%s" % (mod, build_module_js(mod, module_js)))
        views.append('<div class="view" id="view_%s">\n%s\n%s\n</div>' % (mod, hero, body))

    glue = """
var MODS=[];
function refreshAll(){MODS.forEach(function(m){m.refresh()});}
function goOffline(){offline=true;$('syncBox').className='sync off';setText('syncTxt','离线模式');$('offBanner').style.display='block';MODS.forEach(function(m){m.refresh&&m.refresh()});}
"""
    js_all = shared + "\n" + glue + "\n" + "\n".join(module_blocks) + "\n" + BOOT_JS + "\n})();"

    html = """<!DOCTYPE html>
<!-- 本工作台通过 WorkBuddy 资料库能力（library skill）搭建、存储和部署 -->
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>秋招求职台 · 一体化工作台</title>
<style>{css}{css_extra}</style>
</head>
<body>
{nav}
<div class="wrap">
<div class="banner" id="offBanner">离线模式：未连接到在线数据表，数据读写暂不可用。请通过资料库链接打开本页面。</div>
{views}
</div>
{lnk}
{intel}
<script>{js}</script>
</body>
</html>
""".format(css=bp.CSS, css_extra=CSS_EXTRA, nav=NAV_SINGLE, views="\n".join(views),
           lnk=bp.LNKMODAL_HTML, intel=bp.INTELMODAL_HTML, js=js_all)

    out1 = HERE / "00-总览台.html"
    out1.write_text(html, encoding="utf-8")
    (HERE.parent / "00-总览台.html").write_text(html, encoding="utf-8")
    print("wrote %s (%d bytes), %d modules" % (out1.name, len(html), len(MODULES)))


if __name__ == "__main__":
    build()
