#!/usr/bin/env python3
"""Build 4 modular HTML pages for the qiuzhao workbench."""
from pathlib import Path
import json, os, re

OUT = Path(__file__).parent

# ----------------- common head/css/js shell -----------------
JOBS_ID = "GgZ71tywhs4HEZytFSqXTP"
APPS_ID = "oBGkMFTv9Xv4Xn5gFOK18S"
INTERN_ID = "tgH8096uENTaIj8RSY9qm5"

CAREER_KW = "['算法','人工智能','AI','大模型','机器学习','深度学习','数据','软件','开发','计算机','信息技术','网络安全','信息安全','测试','前端','后端','运维','嵌入式']"
MY_CITY_KW = "['北京','成都','天津']"
SOE_KW = "['中国','国家','国电','中航','航空','航天','中船','船舶','兵器','中核','核工业','中石油','中石化','中海油','国家电网','南方电网','中国移动','中国联通','中国电信','中国铁塔','邮政','中储粮','中粮','华润','招商局','中车','一汽','东风','中远','海运','中金','中信','光大','中建','中铁','中交','中冶','电建','能建','华能','大唐','华电','三峡','国投','国机','国药','保利','烟草','黄金','宝武','鞍钢','有研','钢研','诚通','国新','电科','电子科技','兵装','中轻','中盐','建材','矿冶','中咨','银行','证券','保险']"


CSS = r"""
:root{
  --bg:#f5f7fa; --card:#ffffff; --line:#e5e9f0; --txt:#1f2937; --sub:#6b7280;
  --pri:#2563eb; --pri-soft:#eaf1fe; --red:#dc2626; --red-soft:#fdecec;
  --orange:#d97706; --orange-soft:#fdf3e3; --green:#059669; --green-soft:#e6f6f0;
  --radius:14px; --shadow:0 1px 3px rgba(16,24,40,.08);
}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--txt);font-size:15px;line-height:1.55;padding-bottom:env(safe-area-inset-bottom)}
.wrap{max-width:1000px;margin:0 auto;padding:0 16px 80px}
nav.tabbar{position:sticky;top:0;z-index:50;background:rgba(245,247,250,.92);backdrop-filter:saturate(180%) blur(8px);-webkit-backdrop-filter:saturate(180%) blur(8px);border-bottom:1px solid var(--line)}
nav.tabbar .inner{max-width:1000px;margin:0 auto;display:flex;align-items:center;gap:6px;padding:10px 16px;overflow-x:auto;-webkit-overflow-scrolling:touch}
nav.tabbar a.logo{font-weight:700;font-size:16px;color:var(--txt);text-decoration:none;display:flex;align-items:center;gap:6px;flex:none;margin-right:6px}
nav.tabbar a.logo svg{width:22px;height:22px}
nav.tabbar .tab{flex:none;padding:8px 14px;border-radius:999px;font-size:13px;color:var(--sub);text-decoration:none;font-weight:600;white-space:nowrap;border:1px solid transparent;background:transparent}
nav.tabbar .tab[aria-current="page"]{background:var(--pri);color:#fff;border-color:var(--pri)}
nav.tabbar .tab:not([aria-current]):hover{background:var(--card);color:var(--txt)}
nav.tabbar .sync{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--sub);margin-left:auto;flex:none;background:var(--card);border:1px solid var(--line);border-radius:999px;padding:5px 10px;white-space:nowrap}
nav.tabbar .sync .dot{width:8px;height:8px;border-radius:50%;background:var(--green)}
nav.tabbar .sync.off .dot{background:var(--red)}
.banner{display:none;background:var(--red-soft);color:var(--red);border:1px solid #f5c2c2;border-radius:var(--radius);padding:12px 16px;margin:14px 0;font-size:14px}
section{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:16px;margin:14px 0}
section>h2{font-size:16px;display:flex;align-items:center;gap:8px;margin-bottom:12px}
section>h2 svg{width:18px;height:18px;flex:none}
section>h2 .cnt{margin-left:auto;font-size:12px;color:var(--sub);font-weight:normal}
#todayList{display:flex;flex-direction:column;gap:8px}
.titem{display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:10px;background:#fafbfc;border:1px solid var(--line);flex-wrap:wrap}
.titem.red{background:var(--red-soft);border-color:#f3c1c1}
.titem.orange{background:var(--orange-soft);border-color:#f0d9b5}
.titem.blue{background:var(--pri-soft);border-color:#c9dbfa}
.titem .badge{font-size:11px;font-weight:600;border-radius:6px;padding:2px 8px;flex:none;color:#fff}
.titem.red .badge{background:var(--red)}.titem.orange .badge{background:var(--orange)}.titem.blue .badge{background:var(--pri)}
.titem .tinfo{flex:1;min-width:180px}
.titem .tinfo b{font-size:14px}
.titem .tinfo span{display:block;font-size:12px;color:var(--sub)}
.titem .btns{display:flex;gap:6px}
.empty{color:var(--sub);font-size:14px;text-align:center;padding:18px 0}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:0}
.stat{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:14px;text-align:center;box-shadow:var(--shadow)}
.stat b{font-size:24px;display:block;line-height:1.2}
.stat span{font-size:12px;color:var(--sub);display:block;margin-top:4px}
.stat.danger b{color:var(--red)}
.stat.danger{background:var(--red-soft);border-color:#f3c1c1}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:start}
.filters{display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap}
.filters input,.filters select{flex:1;min-width:120px;height:40px;border:1px solid var(--line);border-radius:8px;padding:0 10px;background:#fff;font-size:14px;font-family:inherit}
.cards{display:flex;flex-direction:column;gap:10px}
.jcard,.acard{background:#fff;border:1px solid var(--line);border-radius:12px;padding:12px 14px;display:flex;flex-direction:column;gap:6px}
.jcard.soe{border-color:#f3c1c1;background:#fffbfb;box-shadow:inset 3px 0 0 var(--red)}
.jrow{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.jrow b{font-size:15px;flex:none}
.tag{font-size:11px;font-weight:600;padding:2px 8px;border-radius:6px;background:var(--pri-soft);color:var(--pri);flex:none}
.tag.ok{background:var(--green-soft);color:var(--green)}
.tag.bad{background:var(--red-soft);color:var(--red)}
.tag.soe{background:var(--red-soft);color:var(--red)}
.tag.gray{background:#eef0f4;color:#6b7280}
.jmeta{font-size:12px;color:var(--sub)}
.jnote{font-size:13px;color:var(--txt);background:#fafbfc;border-radius:6px;padding:6px 8px;margin:2px 0 0}
.jacts{display:flex;gap:6px;flex-wrap:wrap;margin-top:4px;align-items:center}
.btn{appearance:none;border:0;cursor:pointer;padding:0 14px;height:36px;border-radius:8px;font-size:13px;font-weight:600;background:var(--card);color:var(--txt);font-family:inherit;text-decoration:none;display:inline-flex;align-items:center;justify-content:center;min-height:36px;transition:transform .05s,opacity .12s}
.btn:active{transform:translateY(1px)}
.btn:disabled{opacity:.5;cursor:not-allowed}
.btn-sm{height:32px;padding:0 10px;font-size:12px;min-height:32px}
.btn-pri{background:var(--pri);color:#fff}
.btn-ghost{background:#fff;color:var(--pri);border:1px solid #c9dbfa}
.btn-go{background:var(--green);color:#fff;border:1px solid var(--green)}
.btn-search{background:#fff;color:var(--sub);border:1px dashed #c3cad6}
.btn-danger{background:#fff;color:var(--red);border:1px solid #f3c1c1}
.btn-gray{background:#f1f3f7;color:var(--sub);border:1px solid var(--line)}
.btn-nav{background:#fff;color:var(--pri);border:1px solid #c9dbfa;height:48px;padding:0 18px;font-size:14px;display:flex;align-items:center;gap:8px;text-decoration:none;border-radius:12px}
.btn-nav:hover{background:var(--pri-soft)}
.btn-nav .meta{font-size:11px;color:var(--sub);font-weight:normal;display:block;margin-top:2px}
select{height:36px;border:1px solid var(--line);border-radius:8px;padding:0 8px;background:#fff;font-size:13px;font-family:inherit}
.moduleCards{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:14px 0}
.moduleCard{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px;text-decoration:none;color:var(--txt);display:flex;flex-direction:column;gap:6px;transition:transform .05s,box-shadow .12s}
.moduleCard:hover{box-shadow:0 4px 12px rgba(16,24,40,.1)}
.moduleCard .mh{display:flex;align-items:center;gap:8px;font-weight:700;font-size:15px}
.moduleCard svg{width:20px;height:20px}
.moduleCard .mmeta{font-size:12px;color:var(--sub)}
.moduleCard .mstat{font-size:11px;background:var(--pri-soft);color:var(--pri);border-radius:6px;padding:3px 8px;align-self:flex-start;font-weight:600}
.moduleCard.danger .mstat{background:var(--red-soft);color:var(--red)}
.moduleCard.warn .mstat{background:var(--orange-soft);color:var(--orange)}
.batchChips{display:flex;gap:6px;margin-bottom:8px}
.chip{min-height:32px;padding:0 14px;border-radius:999px;border:1px solid var(--line);background:#fff;color:var(--sub);font-size:12px;font-weight:600;cursor:pointer;font-family:inherit}
.chip.active{background:var(--pri);color:#fff;border-color:var(--pri)}
.legend{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:8px;font-size:12px;color:var(--sub)}
.legend span{display:flex;align-items:center;gap:6px}
.legend .g{width:10px;height:10px;border-radius:3px;background:var(--green);display:inline-block}
.legend .s{width:10px;height:10px;border-radius:3px;border:1px dashed #c3cad6;display:inline-block;background:#fff}
details.add{margin-bottom:10px;border:1px dashed var(--line);border-radius:10px;padding:0 12px;background:#fafbfc}
details.add summary{cursor:pointer;padding:10px 0;font-weight:600;font-size:13px;color:var(--sub);list-style:none}
details.add[open] summary{padding-top:8px}
details.add form{padding:8px 0}
.formrow{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px}
.formrow>div,.fl{display:flex;flex-direction:column;gap:4px}
.fl{font-size:12px;color:var(--sub);font-weight:600;margin-bottom:6px}
input[type="text"],input[type="search"],input:not([type]){height:40px;border:1px solid var(--line);border-radius:8px;padding:0 10px;background:#fff;font-size:14px;font-family:inherit}
textarea{width:100%;min-height:64px;border:1px solid var(--line);border-radius:8px;padding:8px 10px;font-size:14px;font-family:inherit;resize:vertical}
input[type="date"]{height:40px;border:1px solid var(--line);border-radius:8px;padding:0 10px;font-size:14px}
label.fl{display:block;margin:6px 0 0}
.mtail{font-size:11px;color:var(--sub);text-align:center;margin-top:4px}
.navSpacer{height:8px}
@media (max-width:768px){
  .stats,.grid,.moduleCards,.formrow{grid-template-columns:1fr}
  nav.tabbar .inner{padding:8px 12px}
  nav.tabbar .sync{font-size:11px;padding:4px 8px}
  .wrap{padding:0 12px 60px}
}
"""

# shared utility JS that every page needs
SHARED_JS = """
var JOBS_ID='{JOBS_ID}', APPS_ID='{APPS_ID}', INTERN_ID='{INTERN_ID}';
var OPTS={{}};
var state={{jobs:[],apps:[],interns:[],todayMine:true,batchMode:''}};
var STAGES=['已投递','笔试','一面','二面','HR面','Offer','感谢信'];
var db=null,offline=false;
var CAREER_KW={CAREER_KW};
var MY_CITY_KW={MY_CITY_KW};
var SOE_KW={SOE_KW};

function $(id){{return document.getElementById(id)}}
function esc(s){{return String(s==null?'':s).replace(/[&<>""]/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]}})}}
function dayStr(d){{var p=function(n){{return (n<10?'0':'')+n}};return d.getFullYear()+'-'+p(d.getMonth()+1)+'-'+p(d.getDate())}}
function today(){{return dayStr(new Date())}}
// 日期字段可能以字符串 'YYYY-MM-DD'、对象 date/text/value 字段、或 Date 形式出现，全部兼容
function dOnly(v){{if(v==null)return '';if(typeof v==='object'){{v=v.date||v.text||v.value||v.start||''}}return String(v).slice(0,10)}}
function diffDays(a,b){{if(!a||!b)return null;return Math.round((Date.parse(b)-Date.parse(a))/86400000)}}
function optId(field,text){{var l=OPTS[field]||[];for(var i=0;i<l.length;i++){{if(l[i].text===text)return l[i].id}}return text}}
function optText(field,idOrText){{var l=OPTS[field]||[];for(var i=0;i<l.length;i++){{if(l[i].id===idOrText)return l[i].text}}return idOrText||''}}
function fieldText(j,f){{var v=j[f];if(v==null)return '';if(typeof v==='object')return String(v.text||'');return String(v)}}
function urlVal(v){{if(!v)return {{text:'',link:''}};if(typeof v==='object'){{if(typeof v.length==='number')v=(v&&v[0])||{{}};return {{text:String(v.text||v.link||''),link:String(v.link||v.text||'')}}}}return {{text:String(v),link:String(v)}}}}
function recId(r){{return (r&&(r._id||r.record_id||r.id))||''}}
function webSearchUrl(q){{return 'https://www.bing.com/search?q='+encodeURIComponent(q+' 校招 网申入口')}}
function searchUrl(q){{return 'https://www.nowcoder.com/search/all?query='+encodeURIComponent(q+' 校招')}}

function isSOE(j){{var c=fieldText(j,'公司');for(var i=0;i<SOE_KW.length;i++){{if(c.indexOf(SOE_KW[i])>=0)return true}}return false}}
function mineMatch(j){{var c=fieldText(j,'岗位方向'),hit=false;for(var i=0;i<CAREER_KW.length;i++){{if(c.indexOf(CAREER_KW[i])>=0){{hit=true;break}}}}if(!hit)return false;var loc=fieldText(j,'工作地点');for(var j2=0;j2<MY_CITY_KW.length;j2++){{if(loc.indexOf(MY_CITY_KW[j2])>=0)return true}}return false}}
function jobStatus(j){{return j['投递状态']?optText('投递状态',typeof j['投递状态']==='object'?j['投递状态'].text||'':String(j['投递状态'])):'待投递'}}
function appStage(a){{return a['当前阶段']?optText('当前阶段',typeof a['当前阶段']==='object'?a['当前阶段'].text||'':String(a['当前阶段'])):'已投递'}}

function showLinkModal(link){{var m=$('lnkModal');if(!m){{alert('投递链接：'+link);return}}$('lnkTxt').textContent=link;m.style.display='flex';$('lnkCopy').onclick=function(){{var done=function(){{$('lnkCopy').textContent='已复制'}};try{{var ta=document.createElement('textarea');ta.value=link;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();var ok=document.execCommand('copy');document.body.removeChild(ta);if(ok){{done();return}}}}catch(e){{}}if(navigator.clipboard&&navigator.clipboard.writeText){{navigator.clipboard.writeText(link).then(done)}}}}}};
function openLink(link){{if(!link){{alert('这条记录没有填链接');return}}var w=null;try{{w=window.open(link,'_blank')}}catch(e){{}}if(!w)showLinkModal(link);}}
function jobLink(j){{return urlVal(j['投递链接']).link}}
function jobJump(j){{var l=jobLink(j);var c=j['公司']||'';return l||searchUrl(c)||webSearchUrl(c)}}

function setFieldText(root,name,val,dbid){{var el=root.querySelector('[data-field="'+name+'"]');if(!el)return;if(name==='投递链接'||name==='相关链接'){{var u=urlVal(val);el.style.display='';if(u.link){{el.className=name==='投递链接'?'btn btn-go btn-sm':'btn btn-ghost btn-sm';el.textContent=name==='投递链接'?'直达官网':'链接';el.setAttribute('href',u.link)}}else{{el.className='btn btn-search btn-sm';el.textContent=name==='投递链接'?'搜索网申入口':'搜索进度';el.removeAttribute('href')}}}}else{{el.textContent=val==null?'':String(val)}}el.setAttribute('data-sp-bindable','database');el.setAttribute('data-sp-database-id',dbid)}}
function setText(id,v){{var el=$(id);if(el)el.textContent=v}}
function markBindable(el,dbid){{el.setAttribute('data-sp-bindable','database');el.setAttribute('data-sp-database-id',dbid)}}

/* ---------- 表单缓存（DSDK008） ---------- */
var CACHE_KEY='wb_qiuzhao_form_v1';
var cacheTimer=null;
function cacheSaveForm(fid){{try{{var f=$(fid);if(!f)return;var data=JSON.parse(localStorage.getItem(CACHE_KEY)||'{{}}');Array.prototype.forEach.call(f.querySelectorAll('[name]'),function(el){{if(el.type==='password'||el.type==='file')return;data[fid+'.'+el.name]=el.value}});localStorage.setItem(CACHE_KEY,JSON.stringify(data))}}catch(e){{}}}}
function cacheDebounce(fid){{if(cacheTimer)clearTimeout(cacheTimer);cacheTimer=setTimeout(function(){{cacheSaveForm(fid)}},300)}}
function cacheRestoreForm(fid){{try{{var data=JSON.parse(localStorage.getItem(CACHE_KEY)||'{{}}');var f=$(fid);if(!f)return;Array.prototype.forEach.call(f.querySelectorAll('[name]'),function(el){{var k=fid+'.'+el.name;if(data[k]!==undefined&&el.type!=='password'&&el.type!=='file')el.value=data[k]}})}}catch(e){{}}}}
function cacheClearForm(fid){{try{{var data=JSON.parse(localStorage.getItem(CACHE_KEY)||'{{}}');Array.prototype.forEach.call(Object.keys(data),function(k){{if(k.indexOf(fid+'.')===0)delete data[k]}});localStorage.setItem(CACHE_KEY,JSON.stringify(data))}}catch(e){{}}}}
function bindFormCache(fid){{var f=$(fid);if(!f)return;f.addEventListener('input',function(){{cacheDebounce(fid)}});f.addEventListener('change',function(){{cacheDebounce(fid)}});cacheRestoreForm(fid);}}
function cacheWipeAll(){{try{{localStorage.removeItem(CACHE_KEY)}}catch(e){{}}}}
""".format(JOBS_ID=JOBS_ID, APPS_ID=APPS_ID, INTERN_ID=INTERN_ID, CAREER_KW=CAREER_KW, MY_CITY_KW=MY_CITY_KW, SOE_KW=SOE_KW)


NAV_HTML = """
<nav class="tabbar">
  <div class="inner">
    <a class="logo" target="_top" href="{OVERVIEW_URL}"><svg viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>秋招求职台</a>
    <a class="tab" target="_top" href="{OVERVIEW_URL}" {OVERVIEW_ACTIVE}>总览</a>
    <a class="tab" target="_top" href="{AUTUMN_URL}" {AUTUMN_ACTIVE}>秋招岗位</a>
    <a class="tab" target="_top" href="{SOE_URL}" {SOE_ACTIVE}>央国企</a>
    <a class="tab" target="_top" href="{INTERN_URL}" {INTERN_ACTIVE}>成都实习</a>
    <div class="sync" id="syncBox"><span class="dot"></span><span id="syncTxt">连接中…</span></div>
  </div>
</nav>
"""

LNKMODAL_HTML = """
<div id="lnkModal" style="display:none;position:fixed;inset:0;background:rgba(15,23,42,.45);z-index:99;align-items:center;justify-content:center;padding:20px">
  <div style="background:#fff;border-radius:14px;max-width:520px;width:100%;padding:18px;box-shadow:0 10px 30px rgba(15,23,42,.2)">
    <b style="font-size:15px">浏览器拦截了新窗口，复制链接去打开</b>
    <p id="lnkTxt" style="word-break:break-all;background:#f7f9fc;border-radius:8px;padding:10px;margin:10px 0;font-size:13px;color:var(--pri)"></p>
    <p style="font-size:12px;color:var(--sub);margin:-4px 0 10px">手机端可长按上方链接选择复制，再粘贴到浏览器打开</p>
    <div style="display:flex;gap:8px;justify-content:flex-end">
      <button class="btn btn-gray btn-sm" id="lnkClose">关闭</button>
      <button class="btn btn-pri btn-sm" id="lnkCopy">复制链接</button>
    </div>
  </div>
</div>
"""

# --------- page-specific bodies ---------

def page_overview(urls):
    nav = NAV_HTML.format(
        OVERVIEW_URL=urls["overview"], AUTUMN_URL=urls["autumn"], SOE_URL=urls["soe"], INTERN_URL=urls["intern"],
        OVERVIEW_ACTIVE='aria-current="page"', AUTUMN_ACTIVE='', SOE_ACTIVE='', INTERN_ACTIVE='',
    )
    body = """
<section>
  <h2><svg viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>今天要处理<span class="cnt" id="todayCnt"></span></h2>
  <label class="legend"><input type="checkbox" id="todayMine" checked style="min-height:0;margin:0">只看 AI/计算机相关 · 北京/成都/天津（关掉看全部）</label>
  <div id="todayList"><div class="empty">加载中…</div></div>
</section>

<div class="stats">
  <div class="stat" style="border-color:#f3c1c1"><b id="stWait" data-sp-bindable="database" data-sp-database-id="GgZ71tywhs4HEZytFSqXTP">0</b><span>待投递岗位</span></div>
  <div class="stat"><b id="stDone" data-sp-bindable="database" data-sp-database-id="GgZ71tywhs4HEZytFSqXTP">0</b><span>已投递</span></div>
  <div class="stat danger"><b id="stDdl" data-sp-bindable="database" data-sp-database-id="GgZ71tywhs4HEZytFSqXTP">0</b><span>7天内截止</span></div>
  <div class="stat"><b id="stLive" data-sp-bindable="database" data-sp-database-id="oBGkMFTv9Xv4Xn5gFOK18S">0</b><span>面试进行中</span></div>
</div>

<section>
  <h2><svg viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>跳转模块</h2>
  <div class="moduleCards">
    <a class="moduleCard" target="_top" href="{AUTUMN}">
      <div class="mh"><svg viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>秋招岗位 · 其他企业<span class="mstat" id="cntAutumn">-</span></div>
      <div class="mmeta">互联网/科技/制造业等非央国企岗位，按城市/职业/批次筛选查看</div>
    </a>
    <a class="moduleCard" target="_top" href="{SOE}">
      <div class="mh" style="color:var(--red)"><svg viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2"><path d="M5 21V4"/><path d="M5 4c3-2 6 1.5 9 0s5-.5 7 .5V13c-2-1-4-1.5-7 0s-6-2-9 0"/></svg>央国企专栏<span class="mstat" id="cntSOE">-</span></div>
      <div class="mmeta">自动识别央企/银行/运营商/烟草/电网等，红色卡片独立视图</div>
    </a>
    <a class="moduleCard warn" target="_top" href="{INTERN}">
      <div class="mh" style="color:var(--orange)"><svg viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>成都实习<span class="mstat" id="cntIntern">-</span></div>
      <div class="mmeta">BOSS 直聘手动收录+牛客每日同步，独立的实习岗位专区</div>
    </a>
  </div>
</section>

<section>
  <h2><svg viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4 20-7z"/></svg>投递跟踪<span class="cnt" id="appCnt"></span></h2>
  <details class="add"><summary>添加投递记录</summary>
    <form id="appForm">
      <div class="formrow">
        <div><label class="fl">公司 *</label><input name="company" required placeholder="如：腾讯"></div>
        <div><label class="fl">岗位 *</label><input name="position" required placeholder="如：算法实习生"></div>
      </div>
      <div class="formrow">
        <div><label class="fl">当前阶段</label><select name="stage" id="fStage"><option value="">请选择</option></select></div>
        <div><label class="fl">投递日期</label><input type="date" name="applydate"></div>
      </div>
      <div class="formrow">
        <div><label class="fl">下次节点</label><input type="date" name="nextdate"></div>
        <div><label class="fl">相关链接</label><input name="alnk" type="url" placeholder="https://"></div>
      </div>
      <label class="fl">节点说明</label><textarea name="nodedesc" placeholder="如：一面 14:00 腾讯会议"></textarea>
      <div style="margin-top:10px"><button type="submit" class="btn btn-pri" style="width:100%">保存记录</button></div>
    </form>
  </details>
  <svg id="funnelSvg" viewBox="0 0 600 200" role="img" aria-label="投递漏斗"></svg>
  <div class="mtail">投递漏斗（各阶段当前数量）</div>
  <div class="cards" id="appCards" style="margin-top:10px"><div class="empty">加载中…</div></div>
</section>
""".format(AUTUMN=urls["autumn"], SOE=urls["soe"], INTERN=urls["intern"])
    tpl_app = """
<div hidden id="tplBox">
  <div class="acard" id="tplApp">
    <div class="jrow"><b data-field="公司"></b><span style="color:var(--sub);font-size:13px" data-field="岗位"></span><span class="tag" data-field="当前阶段" style="margin-left:auto"></span></div>
    <div class="jmeta">投递：<span data-field="投递日期"></span> ｜ 下次：<span data-field="下次节点"></span></div>
    <div class="jmeta" data-field="节点说明"></div>
    <div class="jnote" data-field="复盘笔记"></div>
    <div class="jacts"><a class="btn btn-ghost btn-sm" data-field="相关链接" target="_blank" rel="noopener">链接</a><select class="astage"></select><button class="btn btn-gray btn-sm anote">记笔记</button><button class="btn btn-gray btn-sm adel">删除</button></div>
  </div>
</div>
"""
    body += tpl_app
    page_js = r"""
function todayItems(){
  var t=today(),items=[];
  state.jobs.forEach(function(j){
    if(jobStatus(j)!=='待投递')return;
    if(state.todayMine&&!mineMatch(j))return;
    var dd=dOnly(j['截止日期']);if(!dd)return;
    var n=diffDays(t,dd);
    if(n<0)items.push({kind:'job',level:'red',badge:'已过截止',title:j['公司']||'未命名公司',meta:'岗位：'+(j['岗位方向']||'未填')+' ｜ 截止 '+dd+'（已过'+(-n)+'天）',rec:j});
    else if(n<=3)items.push({kind:'job',level:'orange',badge:(n===0?'今天截止':'剩'+n+'天'),title:j['公司']||'未命名公司',meta:'岗位：'+(j['岗位方向']||'未填')+' ｜ 截止 '+dd,rec:j});
  });
  state.apps.forEach(function(a){
    var st=appStage(a);if(st==='Offer'||st==='感谢信')return;
    var nd=dOnly(a['下次节点']);if(!nd)return;
    var n=diffDays(t,nd);
    if(n<0)items.push({kind:'app',level:'red',badge:'节点已过',title:(a['公司']||'')+' · '+(a['岗位']||''),meta:st+' ｜ 原定 '+nd+'（'+(a['节点说明']||'未填说明')+'）',rec:a});
    else if(n<=1)items.push({kind:'app',level:'blue',badge:(n===0?'今天':'明天'),title:(a['公司']||'')+' · '+(a['岗位']||''),meta:st+' ｜ '+nd+'（'+(a['节点说明']||'未填说明')+'）',rec:a});
  });
  items.sort(function(x,y){var o={red:0,orange:1,blue:2};return o[x.level]-o[y.level]});
  return items;
}
function renderToday(){
  var box=$('todayList'),items=todayItems();
  setText('todayCnt',items.length?items.length+' 项':'');
  if(!items.length){box.innerHTML='<div class="empty">今天没有要处理的，按节奏推进就好</div>';return}
  box.innerHTML='';
  items.forEach(function(it){
    var d=document.createElement('div');d.className='titem '+it.level;
    var btns='';
    if(it.kind==='job'){var jl=jobLink(it.rec);btns='<button class="btn btn-sm tgo '+(jl?'btn-go':'btn-search')+'">'+(jl?'直达官网':'搜索网申入口')+'</button>';}
    else{var al=urlVal(it.rec['相关链接']).link;btns='<button class="btn btn-sm tgo '+(al?'btn-ghost':'btn-search')+'">'+(al?'查看链接':'搜索进度')+'</button>';}
    d.innerHTML='<span class="badge">'+esc(it.badge)+'</span><div class="tinfo"><b>'+esc(it.title)+'</b><span>'+esc(it.meta)+'</span></div><div class="btns">'+btns+'</div>';
    d.querySelector('.tgo').addEventListener('click',function(){openLink(it.kind==='job'?jobJump(it.rec):urlVal(it.rec['相关链接']).link||searchUrl(it.rec['公司']||''))});
    box.appendChild(d);
  });
}
function renderStats(){
  var w=0,done=0,ddl=0,live=0,t=today();
  state.jobs.forEach(function(j){var st=jobStatus(j);if(st==='待投递')w++;if(st==='已投递')done++;var dd=dOnly(j['截止日期']);if(st==='待投递'&&dd){var n=diffDays(t,dd);if(n>=0&&n<=7)ddl++}});
  state.apps.forEach(function(a){var st=appStage(a);if(st!=='Offer'&&st!=='感谢信'&&st!=='已投递')live++});
  setText('stWait',w);setText('stDone',done);setText('stDdl',ddl);setText('stLive',live);
  markBindable($('stWait'),JOBS_ID);markBindable($('stDone'),JOBS_ID);markBindable($('stDdl'),JOBS_ID);markBindable($('stLive'),APPS_ID);
}
function renderModuleCounts(){
  var aut=state.jobs.filter(function(j){return !isSOE(j)}).length;
  var soe=state.jobs.filter(function(j){return isSOE(j)}).length;
  setText('cntAutumn',aut);setText('cntSOE',soe);setText('cntIntern',state.interns.length);
  markBindable($('cntAutumn'),JOBS_ID);markBindable($('cntSOE'),JOBS_ID);markBindable($('cntIntern'),INTERN_ID);
}
function renderFunnel(){
  var svg=$('funnelSvg');
  if(!svg.childNodes.length){
    var NS='http://www.w3.org/2000/svg';
    for(var i=0;i<STAGES.length;i++){
      var g=document.createElementNS(NS,'g');
      var t1=document.createElementNS(NS,'text');t1.setAttribute('x',2);t1.setAttribute('y',18+i*28);t1.setAttribute('font-size','12');t1.setAttribute('fill','#6b7280');t1.textContent=STAGES[i];
      var bg=document.createElementNS(NS,'rect');bg.setAttribute('x',92);bg.setAttribute('y',6+i*28);bg.setAttribute('height',18);bg.setAttribute('width',440);bg.setAttribute('rx',9);bg.setAttribute('fill','#f1f3f7');
      var bar=document.createElementNS(NS,'rect');bar.setAttribute('x',92);bar.setAttribute('y',6+i*28);bar.setAttribute('height',18);bar.setAttribute('width',0);bar.setAttribute('rx',9);bar.setAttribute('fill',i===5?'#059669':(i===6?'#c3cad6':'#2563eb'));bar.setAttribute('id','fbar'+i);
      var cnt=document.createElementNS(NS,'text');cnt.setAttribute('x',544);cnt.setAttribute('y',20+i*28);cnt.setAttribute('font-size','12');cnt.setAttribute('fill','#1f2937');cnt.setAttribute('font-weight','600');cnt.setAttribute('id','fcnt'+i);cnt.textContent='0';
      g.appendChild(t1);g.appendChild(bg);g.appendChild(bar);g.appendChild(cnt);svg.appendChild(g);
    }
  }
  var counts={},max=1;
  state.apps.forEach(function(a){var st=appStage(a);counts[st]=(counts[st]||0)+1});
  STAGES.forEach(function(s){if((counts[s]||0)>max)max=counts[s]});
  STAGES.forEach(function(s,i){var c=counts[s]||0;$('fbar'+i).setAttribute('width',Math.round(440*c/max));$('fcnt'+i).textContent=c;});
}
function renderApps(){
  var box=$('appCards'),rows=state.apps.slice().sort(function(a,b){var x=dOnly(a['下次节点'])||'9999',y=dOnly(b['下次节点'])||'9999';return x<y?-1:1});
  setText('appCnt',rows.length+' 条记录');
  if(!rows.length){box.innerHTML='<div class="empty">暂无投递记录，点上方「添加投递记录」开始跟踪</div>';return}
  box.innerHTML='';
  rows.forEach(function(a){
    var card=$('tplApp').cloneNode(true);card.removeAttribute('id');
    setFieldText(card,'公司',a['公司'],APPS_ID);setFieldText(card,'岗位',a['岗位'],APPS_ID);setFieldText(card,'当前阶段',appStage(a),APPS_ID);
    setFieldText(card,'投递日期',dOnly(a['投递日期']),APPS_ID);setFieldText(card,'下次节点',dOnly(a['下次节点']),APPS_ID);setFieldText(card,'节点说明',a['节点说明'],APPS_ID);setFieldText(card,'复盘笔记',a['复盘笔记'],APPS_ID);setFieldText(card,'相关链接',a['相关链接'],APPS_ID);
    card.querySelector('[data-field="相关链接"]').addEventListener('click',function(e){e.preventDefault();openLink(urlVal(a['相关链接']).link||searchUrl(a['公司']||''))});
    var nd=dOnly(a['下次节点']);if(nd){var nEl=card.querySelectorAll('[data-field="下次节点"]')[0];var n=diffDays(today(),nd);if(n<0&&appStage(a)!=='Offer'&&appStage(a)!=='感谢信'){nEl.style.color='var(--red)';nEl.textContent=nd+'（已过期）'}}
    var sel=card.querySelector('.astage');sel.innerHTML='';
    var opt0=document.createElement('option');opt0.value='';opt0.textContent='改阶段';sel.appendChild(opt0);
    STAGES.forEach(function(s){var o=document.createElement('option');o.value=optId('当前阶段',s);o.textContent=s;sel.appendChild(o)});
    sel.addEventListener('change',function(){if(!sel.value)return;sel.disabled=true;db.updateRecord({databaseId:'oBGkMFTv9Xv4Xn5gFOK18S',recordId:recId(a),properties:{'当前阶段':{select:sel.value}}}).then(reloadAll).catch(function(e){console.error('[database] 更新失败:',e);sel.disabled=false})});
    card.querySelector('.anote').addEventListener('click',function(){var v=prompt('复盘笔记：',a['复盘笔记']||'');if(v===null)return;db.updateRecord({databaseId:'oBGkMFTv9Xv4Xn5gFOK18S',recordId:recId(a),properties:{'复盘笔记':{text:v}}}).then(reloadAll).catch(function(e){console.error('[database] 更新失败:',e)})});
    card.querySelector('.adel').addEventListener('click',function(){if(!confirm('确定删除「'+(a['公司']||'')+'」这条记录吗？'))return;db.deleteRecord({databaseId:'oBGkMFTv9Xv4Xn5gFOK18S',recordId:recId(a)}).then(reloadAll).catch(function(e){console.error('[database] 删除失败:',e)})});
    box.appendChild(card);
  });
}
function refreshAll(){renderToday();renderStats();renderModuleCounts();renderFunnel();renderApps();}

function bindSubmitApp(){
  var form=$('appForm');if(!form)return;
  form.addEventListener('submit',function(e){
    e.preventDefault();
    var btn=form.querySelector('[type="submit"]');if(btn){btn.disabled=true;btn.textContent='提交中…'}
    var c=form.querySelector('[name="company"]').value.trim();
    var p_=form.querySelector('[name="position"]').value.trim();
    if(!c||!p_){alert('公司和岗位必填');if(btn){btn.disabled=false;btn.textContent='保存记录'}return}
    var p={'公司':{text:c},'岗位':{text:p_}};
    var s=form.querySelector('[name="stage"]').value;if(s)p['当前阶段']={select:s};
    var ad=form.querySelector('[name="applydate"]').value;if(ad)p['投递日期']={date:ad};
    var nd=form.querySelector('[name="nextdate"]').value;if(nd)p['下次节点']={date:nd};
    var dd=form.querySelector('[name="nodedesc"]').value.trim();if(dd)p['节点说明']={text:dd};
    var al=form.querySelector('[name="alnk"]').value.trim();if(al)p['相关链接']={url:{text:al,link:al}};
    db.addRecord({databaseId:'oBGkMFTv9Xv4Xn5gFOK18S',properties:p}).then(function(){form.reset();return reloadAll()}).catch(function(err){console.error('[database] 提交失败:',err);alert('提交失败，请稍后重试')}).finally(function(){if(btn){btn.disabled=false;btn.textContent='保存记录'}});
  });
}

function init(){
  db=window.__SMART_PAGE__&&window.__SMART_PAGE__.database;
  if(!db){goOffline();return}
  setText('syncTxt','已同步');
  bindSubmitApp();
  bindFormCache('appForm');
  $('lnkClose').addEventListener('click',function(){$('lnkModal').style.display='none'});
  $('lnkModal').addEventListener('click',function(e){if(e.target===$('lnkModal'))$('lnkModal').style.display='none'});
  $('todayMine').addEventListener('change',function(){state.todayMine=$('todayMine').checked;renderToday()});
  Promise.all([
    db.getSchema({databaseId:'GgZ71tywhs4HEZytFSqXTP'}),
    db.getSchema({databaseId:'oBGkMFTv9Xv4Xn5gFOK18S'}),
    db.getSchema({databaseId:'tgH8096uENTaIj8RSY9qm5'})
  ]).then(function(ss){
    ss.forEach(function(schema){(schema.properties||[]).forEach(function(f){if((f.type==='select'||f.type==='multi_select')&&f.config&&f.config.options){OPTS[f.name]=f.config.options}})});
    function fillStage(){
      var sel=$('fStage');if(!sel)return;sel.innerHTML='';var o0=document.createElement('option');o0.value='';o0.textContent='请选择';sel.appendChild(o0);
      (OPTS['当前阶段']||[]).forEach(function(o){var oo=document.createElement('option');oo.value=o.id;oo.textContent=o.text;sel.appendChild(oo)});
    }
    fillStage();
    return reloadAll();
  }).catch(function(e){console.error('[database] 初始化失败:',e);goOffline()});
}
function goOffline(){offline=true;$('syncBox').className='sync off';setText('syncTxt','离线模式');$('offBanner').style.display='block';refreshAll()}
"""
    return _wrap_page("总览", body, nav, page_js, urls, active="overview")

def page_autumn(urls):
    nav = NAV_HTML.format(
        OVERVIEW_URL=urls["overview"], AUTUMN_URL=urls["autumn"], SOE_URL=urls["soe"], INTERN_URL=urls["intern"],
        OVERVIEW_ACTIVE='', AUTUMN_ACTIVE='aria-current="page"', SOE_ACTIVE='', INTERN_ACTIVE='',
    )
    body = """
<section>
  <h2><svg viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>秋招岗位 · 其他企业<span class="cnt" id="jobCnt" data-sp-bindable="database" data-sp-database-id="GgZ71tywhs4HEZytFSqXTP"></span></h2>
  <details class="add"><summary>添加岗位</summary>
    <form id="jobForm">
      <div class="formrow">
        <div><label class="fl">公司 *</label><input name="company" required placeholder="如：字节跳动"></div>
        <div><label class="fl">批次</label><select name="batch" id="fBatch"><option value="">请选择</option></select></div>
      </div>
      <div class="formrow">
        <div><label class="fl">岗位方向</label><input name="direction" placeholder="如：大模型算法"></div>
        <div><label class="fl">工作地点</label><input name="location" placeholder="如：北京"></div>
      </div>
      <div class="formrow">
        <div><label class="fl">优先级</label><select name="priority" id="fPrio"><option value="">请选择</option></select></div>
        <div><label class="fl">截止日期</label><input type="date" name="deadline"></div>
      </div>
      <label class="fl">投递链接</label><input name="jlink" type="url" placeholder="https://">
      <label class="fl">备注</label><textarea name="jnote" placeholder="岗位要求、内推人等"></textarea>
      <div style="margin-top:10px"><button type="submit" class="btn btn-pri" style="width:100%">保存岗位</button></div>
    </form>
  </details>
  <div class="legend"><span><span class="g"></span>绿色 = 有网申链接（直达官网）</span><span><span class="s"></span>虚线 = 无链接（搜索网申入口）</span></div>
  <div class="batchChips" id="batchChips"><button type="button" class="chip active" data-mode="">全部</button><button type="button" class="chip" data-mode="autumn">只要秋招</button><button type="button" class="chip" data-mode="intern">只要实习</button></div>
  <div class="filters">
    <input id="q" type="search" placeholder="搜公司 / 方向">
    <select id="fCity"><option value="">全部城市</option></select>
    <select id="fCareer"><option value="">全部职业</option></select>
    <select id="fSt"><option value="">全部状态</option></select>
    <select id="fBatchF"><option value="">全部批次</option></select>
  </div>
  <div class="jmeta" id="filterHint" style="margin-bottom:8px"></div>
  <div class="cards" id="jobCards"><div class="empty">加载中…</div></div>
</section>
"""
    tpl = """
<div hidden id="tplBox">
  <div class="jcard" id="tplJob">
    <div class="jrow"><b data-field="公司"></b><span class="tag" data-field="批次"></span><span class="tag gray" data-field="优先级"></span><span class="tag" data-field="投递状态" style="margin-left:auto"></span></div>
    <div class="jmeta">方向：<span data-field="岗位方向"></span> ｜ 地点：<span data-field="工作地点"></span> ｜ <span data-field="截止日期"></span></div>
    <div class="jmeta">网申开始：<span data-field="网申开始"></span> ｜ 来源：<span data-field="来源"></span></div>
    <div class="jnote" data-field="备注"></div>
    <div class="jacts"><a class="btn btn-ghost btn-sm" data-field="投递链接" target="_blank" rel="noopener">投递</a><button class="btn btn-search btn-sm jsearch">搜公司</button><button class="btn btn-sm jmark">标已投</button><select class="jstatus"></select><button class="btn btn-gray btn-sm jdel">删除</button></div>
  </div>
</div>
"""
    body += tpl
    page_js = r"""
function filteredJobs(){
  return state.jobs.filter(function(j){
    if(isSOE(j))return false;
    var st=jobStatus(j);if(state.fSt&&st!==state.fSt)return false;
    var bt=optText('批次',typeof j['批次']==='object'?j['批次'].text||'':String(j['批次']));
    if(state.batchMode==='autumn'&&bt.indexOf('秋招')<0)return false;
    if(state.batchMode==='intern'&&bt.indexOf('实习')<0)return false;
    if(state.fBatchF&&bt!==state.fBatchF)return false;
    if(state.fCity&&fieldText(j,'工作地点').indexOf(state.fCity)<0)return false;
    if(state.fCareer&&fieldText(j,'岗位方向').indexOf(state.fCareer)<0)return false;
    if(state.q){var q=state.q.toLowerCase();var hay=((j['公司']||'')+' '+(j['岗位方向']||'')+' '+(j['备注']||'')).toLowerCase();if(hay.indexOf(q)<0)return false}
    return true;
  }).sort(function(a,b){var x=dOnly(a['截止日期'])||'9999',y=dOnly(b['截止日期'])||'9999';return x<y?-1:1});
}
function facet(field,splitRe,cap){
  var m={},order=[];
  state.jobs.forEach(function(j){
    fieldText(j,field).split(splitRe).forEach(function(p){p=p.trim();if(!p)return;if(!m[p]){m[p]=0;order.push(p)}m[p]++});
  });
  order.sort(function(a,b){return m[b]-m[a]});return order.slice(0,cap);
}
function renderFilterFacets(){
  var cities=facet('工作地点',/[、,，\/\s]+/,20);var careers=facet('岗位方向',/[、,，\/]+/,15);
  [['fCity',cities,'全部城市'],['fCareer',careers,'全部职业']].forEach(function(pair){
    var sel=$(pair[0]);if(!sel)return;var cur=sel.value;sel.innerHTML='';
    var o0=document.createElement('option');o0.value='';o0.textContent=pair[2];sel.appendChild(o0);
    pair[1].forEach(function(t){var o=document.createElement('option');o.value=t;o.textContent=t;sel.appendChild(o)});
    if(cur&&pair[1].indexOf(cur)>=0)sel.value=cur;
  });
}
function buildJobCard(j){
  var card=$('tplJob').cloneNode(true);card.removeAttribute('id');
  var st=jobStatus(j);
  setFieldText(card,'公司',j['公司'],JOBS_ID);
  setFieldText(card,'批次',optText('批次',typeof j['批次']==='object'?j['批次'].text||'':String(j['批次'])),JOBS_ID);
  setFieldText(card,'优先级',optText('优先级',typeof j['优先级']==='object'?j['优先级'].text||'':String(j['优先级'])),JOBS_ID);
  setFieldText(card,'投递状态',st,JOBS_ID);
  setFieldText(card,'岗位方向',j['岗位方向'],JOBS_ID);setFieldText(card,'工作地点',j['工作地点'],JOBS_ID);setFieldText(card,'备注',j['备注'],JOBS_ID);setFieldText(card,'来源',j['来源'],JOBS_ID);setFieldText(card,'网申开始',dOnly(j['网申开始']),JOBS_ID);
  var stEl=card.querySelector('[data-field="投递状态"]');
  if(st==='已投递')stEl.className='tag ok';else if(st==='不投了')stEl.className='tag gray';
  var dEl=card.querySelector('[data-field="截止日期"]');
  var dd=dOnly(j['截止日期']);
  if(dd){var n=diffDays(today(),dd);dEl.textContent=(n<0?'已截止(' + dd + ')':(n===0?'今天截止':n+'天后截止(' + dd + ')'));if(n<0)dEl.style.color='var(--red)';else if(n<=3)dEl.style.color='var(--orange)';}else{dEl.textContent='截止时间待定';}
  var lnk=card.querySelector('[data-field="投递链接"]');lnk.addEventListener('click',function(e){e.preventDefault();openLink(jobJump(j))});
  card.querySelector('.jsearch').addEventListener('click',function(){openLink(webSearchUrl(fieldText(j,'公司')+' 公司 招聘'))});
  card.querySelector('.jmark').addEventListener('click',function(){markApplied(j);});
  var jst=card.querySelector('.jstatus');jst.innerHTML='';
  (OPTS['投递状态']||[]).forEach(function(o){var op=document.createElement('option');op.value=o.text;op.textContent=o.text;jst.appendChild(op)});
  jst.value=st;
  jst.addEventListener('change',function(){
    if(!jst.value||jst.value===st){jst.value=st;return}
    jst.disabled=true;
    db.updateRecord({databaseId:'GgZ71tywhs4HEZytFSqXTP',recordId:recId(j),properties:{'投递状态':{select:jst.value}}}).then(function(){return jst.value==='已投递'?syncTracking(j):null}).then(reloadAll).catch(function(e){console.error('[database] 更新失败:',e);jst.disabled=false});
  });
  card.querySelector('.jdel').addEventListener('click',function(){if(!confirm('确定删除「'+(j['公司']||'')+'」这条岗位吗？'))return;db.deleteRecord({databaseId:'GgZ71tywhs4HEZytFSqXTP',recordId:recId(j)}).then(reloadAll).catch(function(e){console.error('[database] 删除失败:',e)})});
  return card;
}
function syncTracking(rec){
  var company=fieldText(rec,'公司');if(!company)return Promise.resolve();
  var exists=state.apps.some(function(a){return fieldText(a,'公司')===company});if(exists)return Promise.resolve();
  var p={'公司':{text:company},'岗位':{text:fieldText(rec,'岗位方向')||'校招岗位'},'当前阶段':{select:'已投递'},'投递日期':{date:today()},'节点说明':{text:'由岗位看板一键标记自动生成'}};
  var u=urlVal(rec['投递链接']);if(u.link)p['相关链接']={url:{text:'网申入口',link:u.link}};
  return db.addRecord({databaseId:'oBGkMFTv9Xv4Xn5gFOK18S',properties:p}).catch(function(e){console.error('[database] 投递跟踪写入失败:',e)});
}
function markApplied(rec){
  db.updateRecord({databaseId:'GgZ71tywhs4HEZytFSqXTP',recordId:recId(rec),properties:{'投递状态':{select:'已投递'}}}).then(function(){return syncTracking(rec)}).then(reloadAll).catch(function(e){console.error('[database] 标已投失败:',e);alert('更新失败，请刷新页面重试');});
}
function renderJobs(){
  var box=$('jobCards'),rows=filteredJobs();
  setText('jobCnt',rows.length+' 个岗位');
  var CAP=300,shown=rows;
  if(rows.length>CAP){shown=rows.slice(0,CAP);setText('filterHint','共 '+rows.length+' 个岗位，已显示前 '+CAP+' 个，请用筛选/搜索缩小范围')}
  else{setText('filterHint','')}
  if(!shown.length){box.innerHTML='<div class="empty">没有符合条件的岗位，试试放宽筛选</div>';return}
  box.innerHTML='';
  shown.forEach(function(j){box.appendChild(buildJobCard(j))});
}
function refreshAll(){renderFilterFacets();renderJobs();}
function bindSubmitJob(){
  var form=$('jobForm');if(!form)return;
  form.addEventListener('submit',function(e){
    e.preventDefault();
    var btn=form.querySelector('[type="submit"]');if(btn){btn.disabled=true;btn.textContent='提交中…'}
    var c=form.querySelector('[name="company"]').value.trim();
    if(!c){alert('公司名必填');if(btn){btn.disabled=false;btn.textContent='保存岗位'}return}
    var p={'公司':{text:c},'投递状态':{select:optId('投递状态','待投递')},'来源':{text:'手动添加'}};
    var b=form.querySelector('[name="batch"]').value;if(b)p['批次']={select:b};
    var pr=form.querySelector('[name="priority"]').value;if(pr)p['优先级']={select:pr};
    var d=form.querySelector('[name="direction"]').value.trim();if(d)p['岗位方向']={text:d};
    var l=form.querySelector('[name="location"]').value.trim();if(l)p['工作地点']={text:l};
    var dl=form.querySelector('[name="deadline"]').value;if(dl)p['截止日期']={date:dl};
    var jl=form.querySelector('[name="jlink"]').value.trim();if(jl)p['投递链接']={url:{text:jl,link:jl}};
    var jn=form.querySelector('[name="jnote"]').value.trim();if(jn)p['备注']={text:jn};
    db.addRecord({databaseId:'GgZ71tywhs4HEZytFSqXTP',properties:p}).then(function(){form.reset();return reloadAll()}).catch(function(err){console.error('[database] 提交失败:',err);alert('提交失败，请稍后重试')}).finally(function(){if(btn){btn.disabled=false;btn.textContent='保存岗位'}});
  });
}
function fillSelect(selId,field,withAll){
  var sel=$(selId);if(!sel)return;sel.innerHTML='';
  if(withAll){var o0=document.createElement('option');o0.value='';o0.textContent=field==='投递状态'?'全部状态':'全部批次';sel.appendChild(o0)}
  (OPTS[field]||[]).forEach(function(o){var oo=document.createElement('option');oo.value=withAll?o.text:o.id;oo.textContent=o.text;sel.appendChild(oo)});
}
function renderSelectOptions(){fillSelect('fBatch','批次',false);fillSelect('fPrio','优先级',false);fillSelect('fSt','投递状态',true);fillSelect('fBatchF','批次',true);}

function init(){
  db=window.__SMART_PAGE__&&window.__SMART_PAGE__.database;
  if(!db){goOffline();return}
  setText('syncTxt','已同步');
  bindSubmitJob();
  $('lnkClose').addEventListener('click',function(){$('lnkModal').style.display='none'});
  $('lnkModal').addEventListener('click',function(e){if(e.target===$('lnkModal'))$('lnkModal').style.display='none'});
  $('q').addEventListener('input',function(){state.q=$('q').value.trim();renderJobs()});
  $('fSt').addEventListener('change',function(){state.fSt=$('fSt').value;renderJobs()});
  $('fBatchF').addEventListener('change',function(){state.fBatchF=$('fBatchF').value;renderJobs()});
  $('fCity').addEventListener('change',function(){state.fCity=$('fCity').value;renderJobs()});
  $('fCareer').addEventListener('change',function(){state.fCareer=$('fCareer').value;renderJobs()});
  Array.prototype.forEach.call(document.querySelectorAll('#batchChips .chip'),function(ch){
    ch.addEventListener('click',function(){state.batchMode=ch.getAttribute('data-mode');Array.prototype.forEach.call(document.querySelectorAll('#batchChips .chip'),function(x){x.className='chip'+(x===ch?' active':'')});renderJobs();});
  });
  Promise.all([db.getSchema({databaseId:'GgZ71tywhs4HEZytFSqXTP'}),db.getSchema({databaseId:'oBGkMFTv9Xv4Xn5gFOK18S'}),db.getSchema({databaseId:'tgH8096uENTaIj8RSY9qm5'})]).then(function(ss){
    ss.forEach(function(schema){(schema.properties||[]).forEach(function(f){if((f.type==='select'||f.type==='multi_select')&&f.config&&f.config.options){OPTS[f.name]=f.config.options}})});
    renderSelectOptions();
    return reloadAll();
  }).catch(function(e){console.error('[database] 初始化失败:',e);goOffline()});
}
function goOffline(){offline=true;$('syncBox').className='sync off';setText('syncTxt','离线模式');$('offBanner').style.display='block';refreshAll()}
"""
    return _wrap_page("秋招岗位", body, nav, page_js, urls, active="autumn")

def page_soe(urls):
    nav = NAV_HTML.format(
        OVERVIEW_URL=urls["overview"], AUTUMN_URL=urls["autumn"], SOE_URL=urls["soe"], INTERN_URL=urls["intern"],
        OVERVIEW_ACTIVE='', AUTUMN_ACTIVE='', SOE_ACTIVE='aria-current="page"', INTERN_ACTIVE='',
    )
    body = """
<section>
  <h2 style="color:var(--red)"><svg viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2" stroke-linecap="round"><path d="M5 21V4"/><path d="M5 4c3-2 6 1.5 9 0s5-.5 7 .5V13c-2-1-4-1.5-7 0s-6-2-9 0"/></svg>央国企专栏<span class="cnt" id="jobCnt" data-sp-bindable="database" data-sp-database-id="GgZ71tywhs4HEZytFSqXTP"></span></h2>
  <div class="jmeta" style="margin-bottom:10px">按公司名关键词自动识别（央企/银行/电网/运营商/烟草等），红色卡片标示；有遗漏的公司名告诉我随时补充</div>
  <details class="add"><summary>添加央国企岗位</summary>
    <form id="jobForm">
      <div class="formrow">
        <div><label class="fl">公司 *</label><input name="company" required placeholder="如：国家电网"></div>
        <div><label class="fl">批次</label><select name="batch" id="fBatch"><option value="">请选择</option></select></div>
      </div>
      <div class="formrow">
        <div><label class="fl">岗位方向</label><input name="direction" placeholder="如：电力调度"></div>
        <div><label class="fl">工作地点</label><input name="location" placeholder="如：北京"></div>
      </div>
      <div class="formrow">
        <div><label class="fl">优先级</label><select name="priority" id="fPrio"><option value="">请选择</option></select></div>
        <div><label class="fl">截止日期</label><input type="date" name="deadline"></div>
      </div>
      <label class="fl">投递链接</label><input name="jlink" type="url" placeholder="https://">
      <label class="fl">备注</label><textarea name="jnote" placeholder="岗位要求、内推人等"></textarea>
      <div style="margin-top:10px"><button type="submit" class="btn btn-pri" style="width:100%">保存岗位</button></div>
    </form>
  </details>
  <div class="legend"><span><span class="g"></span>绿色 = 有网申链接</span><span><span class="s"></span>虚线 = 无链接（搜索）</span></div>
  <div class="filters">
    <input id="q" type="search" placeholder="搜公司 / 方向">
    <select id="fCity"><option value="">全部城市</option></select>
    <select id="fCareer"><option value="">全部职业</option></select>
    <select id="fSt"><option value="">全部状态</option></select>
  </div>
  <div class="jmeta" id="filterHint" style="margin-bottom:8px"></div>
  <div class="cards" id="jobCards"><div class="empty">加载中…</div></div>
</section>
"""
    tpl = """
<div hidden id="tplBox">
  <div class="jcard soe" id="tplJob">
    <div class="jrow"><b data-field="公司"></b><span class="tag" data-field="批次"></span><span class="tag gray" data-field="优先级"></span><span class="tag soe" style="margin-left:auto">央国企</span></div>
    <div class="jmeta">方向：<span data-field="岗位方向"></span> ｜ 地点：<span data-field="工作地点"></span> ｜ <span data-field="截止日期"></span></div>
    <div class="jmeta">网申开始：<span data-field="网申开始"></span> ｜ 来源：<span data-field="来源"></span></div>
    <div class="jnote" data-field="备注"></div>
    <div class="jacts"><a class="btn btn-ghost btn-sm" data-field="投递链接" target="_blank" rel="noopener">投递</a><button class="btn btn-search btn-sm jsearch">搜公司</button><button class="btn btn-sm jmark">标已投</button><select class="jstatus"></select><button class="btn btn-gray btn-sm jdel">删除</button></div>
  </div>
</div>
"""
    body += tpl
    page_js = r"""
function filteredSOE(){
  return state.jobs.filter(function(j){
    if(!isSOE(j))return false;
    var st=jobStatus(j);if(state.fSt&&st!==state.fSt)return false;
    if(state.fCity&&fieldText(j,'工作地点').indexOf(state.fCity)<0)return false;
    if(state.fCareer&&fieldText(j,'岗位方向').indexOf(state.fCareer)<0)return false;
    if(state.q){var q=state.q.toLowerCase();var hay=((j['公司']||'')+' '+(j['岗位方向']||'')+' '+(j['备注']||'')).toLowerCase();if(hay.indexOf(q)<0)return false}
    return true;
  }).sort(function(a,b){var x=dOnly(a['截止日期'])||'9999',y=dOnly(b['截止日期'])||'9999';return x<y?-1:1});
}
function facet(field,splitRe,cap){
  var m={},order=[];
  state.jobs.filter(isSOE).forEach(function(j){fieldText(j,field).split(splitRe).forEach(function(p){p=p.trim();if(!p)return;if(!m[p]){m[p]=0;order.push(p)}m[p]++})});
  order.sort(function(a,b){return m[b]-m[a]});return order.slice(0,cap);
}
function renderFilterFacets(){
  var cities=facet('工作地点',/[、,，\/\s]+/,20);var careers=facet('岗位方向',/[、,，\/]+/,15);
  [['fCity',cities,'全部城市'],['fCareer',careers,'全部职业']].forEach(function(pair){
    var sel=$(pair[0]);if(!sel)return;var cur=sel.value;sel.innerHTML='';
    var o0=document.createElement('option');o0.value='';o0.textContent=pair[2];sel.appendChild(o0);
    pair[1].forEach(function(t){var o=document.createElement('option');o.value=t;o.textContent=t;sel.appendChild(o)});
    if(cur&&pair[1].indexOf(cur)>=0)sel.value=cur;
  });
}
function buildJobCard(j){
  var card=$('tplJob').cloneNode(true);card.removeAttribute('id');
  var st=jobStatus(j);
  setFieldText(card,'公司',j['公司'],JOBS_ID);
  setFieldText(card,'批次',optText('批次',typeof j['批次']==='object'?j['批次'].text||'':String(j['批次'])),JOBS_ID);
  setFieldText(card,'优先级',optText('优先级',typeof j['优先级']==='object'?j['优先级'].text||'':String(j['优先级'])),JOBS_ID);
  setFieldText(card,'岗位方向',j['岗位方向'],JOBS_ID);setFieldText(card,'工作地点',j['工作地点'],JOBS_ID);setFieldText(card,'备注',j['备注'],JOBS_ID);setFieldText(card,'来源',j['来源'],JOBS_ID);setFieldText(card,'网申开始',dOnly(j['网申开始']),JOBS_ID);
  var dEl=card.querySelector('[data-field="截止日期"]');
  var dd=dOnly(j['截止日期']);
  if(dd){var n=diffDays(today(),dd);dEl.textContent=(n<0?'已截止(' + dd + ')':(n===0?'今天截止':n+'天后截止(' + dd + ')'));if(n<0)dEl.style.color='var(--red)';else if(n<=3)dEl.style.color='var(--orange)';}else{dEl.textContent='截止时间待定';}
  card.querySelector('[data-field="投递链接"]').addEventListener('click',function(e){e.preventDefault();openLink(jobJump(j))});
  card.querySelector('.jsearch').addEventListener('click',function(){openLink(webSearchUrl(fieldText(j,'公司')+' 公司 招聘'))});
  card.querySelector('.jmark').addEventListener('click',function(){markApplied(j);});
  var jst=card.querySelector('.jstatus');jst.innerHTML='';
  (OPTS['投递状态']||[]).forEach(function(o){var op=document.createElement('option');op.value=o.text;op.textContent=o.text;jst.appendChild(op)});jst.value=st;
  jst.addEventListener('change',function(){if(!jst.value||jst.value===st){jst.value=st;return}jst.disabled=true;db.updateRecord({databaseId:'GgZ71tywhs4HEZytFSqXTP',recordId:recId(j),properties:{'投递状态':{select:jst.value}}}).then(function(){return jst.value==='已投递'?syncTracking(j):null}).then(reloadAll).catch(function(e){console.error('[database] 更新失败:',e);jst.disabled=false})});
  card.querySelector('.jdel').addEventListener('click',function(){if(!confirm('确定删除「'+(j['公司']||'')+'」这条岗位吗？'))return;db.deleteRecord({databaseId:'GgZ71tywhs4HEZytFSqXTP',recordId:recId(j)}).then(reloadAll).catch(function(e){console.error('[database] 删除失败:',e)})});
  return card;
}
function syncTracking(rec){var company=fieldText(rec,'公司');if(!company)return Promise.resolve();var exists=state.apps.some(function(a){return fieldText(a,'公司')===company});if(exists)return Promise.resolve();var p={'公司':{text:company},'岗位':{text:fieldText(rec,'岗位方向')||'校招岗位'},'当前阶段':{select:'已投递'},'投递日期':{date:today()},'节点说明':{text:'由岗位看板一键标记自动生成'}};var u=urlVal(rec['投递链接']);if(u.link)p['相关链接']={url:{text:'网申入口',link:u.link}};return db.addRecord({databaseId:'oBGkMFTv9Xv4Xn5gFOK18S',properties:p}).catch(function(e){console.error(e)});}
function markApplied(rec){db.updateRecord({databaseId:'GgZ71tywhs4HEZytFSqXTP',recordId:recId(rec),properties:{'投递状态':{select:'已投递'}}}).then(function(){return syncTracking(rec)}).then(reloadAll).catch(function(e){console.error('[database] 标已投失败:',e);alert('更新失败，请刷新页面重试');});}
function renderJobs(){
  var box=$('jobCards'),rows=filteredSOE();
  setText('jobCnt',rows.length+' 家');
  var CAP=300,shown=rows;
  if(rows.length>CAP){shown=rows.slice(0,CAP);setText('filterHint','共 '+rows.length+' 家央国企，已显示前 '+CAP+' 家')}else{setText('filterHint','')}
  if(!shown.length){box.innerHTML='<div class="empty">暂未识别到央国企岗位</div>';return}
  box.innerHTML='';
  shown.forEach(function(j){box.appendChild(buildJobCard(j))});
}
function refreshAll(){renderFilterFacets();renderJobs();}
function bindSubmitJob(){
  var form=$('jobForm');if(!form)return;
  form.addEventListener('submit',function(e){
    e.preventDefault();var btn=form.querySelector('[type="submit"]');if(btn){btn.disabled=true;btn.textContent='提交中…'}
    var c=form.querySelector('[name="company"]').value.trim();if(!c){alert('公司名必填');if(btn){btn.disabled=false;btn.textContent='保存岗位'}return}
    var p={'公司':{text:c},'投递状态':{select:optId('投递状态','待投递')},'来源':{text:'手动添加'}};
    var b=form.querySelector('[name="batch"]').value;if(b)p['批次']={select:b};
    var pr=form.querySelector('[name="priority"]').value;if(pr)p['优先级']={select:pr};
    var d=form.querySelector('[name="direction"]').value.trim();if(d)p['岗位方向']={text:d};
    var l=form.querySelector('[name="location"]').value.trim();if(l)p['工作地点']={text:l};
    var dl=form.querySelector('[name="deadline"]').value;if(dl)p['截止日期']={date:dl};
    var jl=form.querySelector('[name="jlink"]').value.trim();if(jl)p['投递链接']={url:{text:jl,link:jl}};
    var jn=form.querySelector('[name="jnote"]').value.trim();if(jn)p['备注']={text:jn};
    db.addRecord({databaseId:'GgZ71tywhs4HEZytFSqXTP',properties:p}).then(function(){form.reset();return reloadAll()}).catch(function(err){console.error(err);alert('提交失败')}).finally(function(){if(btn){btn.disabled=false;btn.textContent='保存岗位'}});
  });
}
function fillSelect(selId,field,withAll){var sel=$(selId);if(!sel)return;sel.innerHTML='';if(withAll){var o0=document.createElement('option');o0.value='';o0.textContent=field==='投递状态'?'全部状态':'全部批次';sel.appendChild(o0)}(OPTS[field]||[]).forEach(function(o){var oo=document.createElement('option');oo.value=withAll?o.text:o.id;oo.textContent=o.text;sel.appendChild(oo)});}
function renderSelectOptions(){fillSelect('fBatch','批次',false);fillSelect('fPrio','优先级',false);fillSelect('fSt','投递状态',true);}
function init(){
  db=window.__SMART_PAGE__&&window.__SMART_PAGE__.database;
  if(!db){goOffline();return}
  setText('syncTxt','已同步');bindSubmitJob();
  bindFormCache('jobForm');
  $('lnkClose').addEventListener('click',function(){$('lnkModal').style.display='none'});
  $('lnkModal').addEventListener('click',function(e){if(e.target===$('lnkModal'))$('lnkModal').style.display='none'});
  $('q').addEventListener('input',function(){state.q=$('q').value.trim();renderJobs()});
  $('fSt').addEventListener('change',function(){state.fSt=$('fSt').value;renderJobs()});
  $('fCity').addEventListener('change',function(){state.fCity=$('fCity').value;renderJobs()});
  $('fCareer').addEventListener('change',function(){state.fCareer=$('fCareer').value;renderJobs()});
  Promise.all([db.getSchema({databaseId:'GgZ71tywhs4HEZytFSqXTP'}),db.getSchema({databaseId:'oBGkMFTv9Xv4Xn5gFOK18S'}),db.getSchema({databaseId:'tgH8096uENTaIj8RSY9qm5'})]).then(function(ss){
    ss.forEach(function(schema){(schema.properties||[]).forEach(function(f){if((f.type==='select'||f.type==='multi_select')&&f.config&&f.config.options){OPTS[f.name]=f.config.options}})});
    renderSelectOptions();
    return reloadAll();
  }).catch(function(e){console.error('[database] 初始化失败:',e);goOffline()});
}
function goOffline(){offline=true;$('syncBox').className='sync off';setText('syncTxt','离线模式');$('offBanner').style.display='block';refreshAll()}
"""
    return _wrap_page("央国企", body, nav, page_js, urls, active="soe")

def page_intern(urls):
    nav = NAV_HTML.format(
        OVERVIEW_URL=urls["overview"], AUTUMN_URL=urls["autumn"], SOE_URL=urls["soe"], INTERN_URL=urls["intern"],
        OVERVIEW_ACTIVE='', AUTUMN_ACTIVE='', SOE_ACTIVE='', INTERN_ACTIVE='aria-current="page"',
    )
    body = """
<section>
  <h2 style="color:var(--orange)"><svg viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>成都实习 · 专栏<span class="cnt" id="jobCnt" data-sp-bindable="database" data-sp-database-id="tgH8096uENTaIj8RSY9qm5"></span></h2>
  <div class="jmeta" style="margin-bottom:10px">BOSS 直聘有反爬无法自动抓取：在 BOSS 上看到合适的岗位，<b>复制岗位链接</b>点下方「添加实习岗位」一键收录；牛客的成都实习批次由每日自动化同步进本表</div>
  <details class="add" open><summary>添加实习岗位（从 BOSS 直聘复制）</summary>
    <form id="internForm">
      <div class="formrow">
        <div><label class="fl">公司 *</label><input name="company" required placeholder="如：腾讯成都"></div>
        <div><label class="fl">岗位名称</label><input name="position" placeholder="如：后端开发实习"></div>
      </div>
      <div class="formrow">
        <div><label class="fl">薪资</label><input name="salary" placeholder="如：200元/天"></div>
        <div><label class="fl">工作地点</label><input name="location" value="成都"></div>
      </div>
      <label class="fl">投递链接（BOSS 岗位页链接）</label><input name="ilnk" type="url" placeholder="https://">
      <label class="fl">岗位要求</label><textarea name="req" placeholder="方向 / 要求 / 到岗时间"></textarea>
      <label class="fl">备注</label><textarea name="inote" placeholder="HR、内推人等"></textarea>
      <div style="margin-top:10px"><button type="submit" class="btn btn-pri" style="width:100%">保存实习岗位</button></div>
    </form>
  </details>
  <div class="legend"><span><span class="g"></span>绿色 = 有投递链接</span><span><span class="s"></span>虚线 = 无链接（搜索）</span></div>
  <div class="filters">
    <input id="q" type="search" placeholder="搜公司 / 岗位">
    <select id="fSt"><option value="">全部状态</option></select>
  </div>
  <div class="jmeta" id="filterHint" style="margin-bottom:8px"></div>
  <div class="cards" id="jobCards"><div class="empty">加载中…</div></div>
</section>
"""
    tpl = """
<div hidden id="tplBox">
  <div class="jcard" id="tplJob" style="border-left:3px solid var(--orange)">
    <div class="jrow"><b data-field="公司"></b><span style="color:var(--sub);font-size:13px" data-field="岗位名称"></span><span class="tag" data-field="投递状态" style="margin-left:auto"></span></div>
    <div class="jmeta">薪资：<span data-field="薪资"></span> ｜ 地点：<span data-field="工作地点"></span> ｜ <span data-field="岗位要求"></span></div>
    <div class="jnote" data-field="备注"></div>
    <div class="jmeta">来源：<span data-field="来源"></span></div>
    <div class="jacts"><a class="btn btn-ghost btn-sm" data-field="投递链接" target="_blank" rel="noopener">投递</a><button class="btn btn-search btn-sm jsearch">搜公司</button><select class="jstatus"></select><button class="btn btn-gray btn-sm jdel">删除</button></div>
  </div>
</div>
"""
    body += tpl
    page_js = r"""
function filteredInterns(){
  return state.interns.filter(function(i){
    var st=jobStatus(i);if(state.fSt&&st!==state.fSt)return false;
    if(state.q){var q=state.q.toLowerCase();var hay=((i['公司']||'')+' '+(i['岗位名称']||'')+' '+(i['备注']||'')).toLowerCase();if(hay.indexOf(q)<0)return false}
    return true;
  }).sort(function(a,b){var c=(a['公司']||'');var cc=(b['公司']||'');return c<cc?-1:1});
}
function renderInterns(){
  var box=$('jobCards'),rows=filteredInterns();
  setText('jobCnt',rows.length+' 条');
  if(!rows.length){box.innerHTML='<div class="empty">还没有实习岗位：在 BOSS 上看到合适的，复制链接点上方「添加实习岗位」收录</div>';return}
  box.innerHTML='';
  rows.forEach(function(i){box.appendChild(buildInternCard(i))});
}
function buildInternCard(i){
  var card=$('tplJob').cloneNode(true);card.removeAttribute('id');
  var st=jobStatus(i);
  setFieldText(card,'公司',i['公司'],INTERN_ID);setFieldText(card,'岗位名称',i['岗位名称'],INTERN_ID);setFieldText(card,'薪资',i['薪资'],INTERN_ID);setFieldText(card,'工作地点',i['工作地点'],INTERN_ID);setFieldText(card,'岗位要求',i['岗位要求'],INTERN_ID);setFieldText(card,'备注',i['备注'],INTERN_ID);setFieldText(card,'来源',i['来源'],INTERN_ID);
  var stEl=card.querySelector('[data-field="投递状态"]');if(st==='已投递')stEl.className='tag ok';else if(st==='不投了')stEl.className='tag gray';
  card.querySelector('[data-field="投递链接"]').addEventListener('click',function(e){e.preventDefault();openLink(urlVal(i['投递链接']).link||webSearchUrl(fieldText(i,'公司')+' 成都 实习 招聘'))});
  card.querySelector('.jsearch').addEventListener('click',function(){openLink(webSearchUrl(fieldText(i,'公司')+' 成都 实习 招聘'))});
  var jst=card.querySelector('.jstatus');jst.innerHTML='';
  (OPTS['投递状态']||[]).forEach(function(o){var op=document.createElement('option');op.value=o.text;op.textContent=o.text;jst.appendChild(op)});jst.value=st;
  jst.addEventListener('change',function(){if(!jst.value||jst.value===st){jst.value=st;return}jst.disabled=true;db.updateRecord({databaseId:'tgH8096uENTaIj8RSY9qm5',recordId:recId(i),properties:{'投递状态':{select:jst.value}}}).then(reloadAll).catch(function(e){console.error('[database] 更新失败:',e);jst.disabled=false})});
  card.querySelector('.jdel').addEventListener('click',function(){if(!confirm('确定删除「'+(i['公司']||'')+'」这条实习岗位吗？'))return;db.deleteRecord({databaseId:'tgH8096uENTaIj8RSY9qm5',recordId:recId(i)}).then(reloadAll).catch(function(e){console.error('[database] 删除失败:',e)})});
  return card;
}
function refreshAll(){renderInterns();}
function bindSubmitIntern(){
  var form=$('internForm');if(!form)return;
  form.addEventListener('submit',function(e){
    e.preventDefault();var btn=form.querySelector('[type="submit"]');if(btn){btn.disabled=true;btn.textContent='提交中…'}
    var c=form.querySelector('[name="company"]').value.trim();if(!c){alert('公司名必填');if(btn){btn.disabled=false;btn.textContent='保存实习岗位'}return}
    var p={'公司':{text:c},'岗位名称':{text:form.querySelector('[name="position"]').value.trim()||'实习'},'投递状态':{select:optId('投递状态','待投递')},'来源':{text:'BOSS直聘（手动添加）'}};
    var s=form.querySelector('[name="salary"]').value.trim();if(s)p['薪资']={text:s};
    var l=form.querySelector('[name="location"]').value.trim();if(l)p['工作地点']={text:l};
    var r=form.querySelector('[name="req"]').value.trim();if(r)p['岗位要求']={text:r};
    var il=form.querySelector('[name="ilnk"]').value.trim();if(il)p['投递链接']={url:{text:'岗位链接',link:il}};
    var n=form.querySelector('[name="inote"]').value.trim();if(n)p['备注']={text:n};
    db.addRecord({databaseId:'tgH8096uENTaIj8RSY9qm5',properties:p}).then(function(){form.reset();return reloadAll()}).catch(function(err){console.error(err);alert('提交失败')}).finally(function(){if(btn){btn.disabled=false;btn.textContent='保存实习岗位'}});
  });
}
function fillSelect(selId,field,withAll){var sel=$(selId);if(!sel)return;sel.innerHTML='';if(withAll){var o0=document.createElement('option');o0.value='';o0.textContent='全部状态';sel.appendChild(o0)}(OPTS[field]||[]).forEach(function(o){var oo=document.createElement('option');oo.value=withAll?o.text:o.id;oo.textContent=o.text;sel.appendChild(oo)});}
function renderSelectOptions(){fillSelect('fSt','投递状态',true);}
function init(){
  db=window.__SMART_PAGE__&&window.__SMART_PAGE__.database;
  if(!db){goOffline();return}
  setText('syncTxt','已同步');bindSubmitIntern();
  bindFormCache('internForm');
  $('lnkClose').addEventListener('click',function(){$('lnkModal').style.display='none'});
  $('lnkModal').addEventListener('click',function(e){if(e.target===$('lnkModal'))$('lnkModal').style.display='none'});
  $('q').addEventListener('input',function(){state.q=$('q').value.trim();renderInterns()});
  $('fSt').addEventListener('change',function(){state.fSt=$('fSt').value;renderInterns()});
  Promise.all([db.getSchema({databaseId:'GgZ71tywhs4HEZytFSqXTP'}),db.getSchema({databaseId:'oBGkMFTv9Xv4Xn5gFOK18S'}),db.getSchema({databaseId:'tgH8096uENTaIj8RSY9qm5'})]).then(function(ss){
    ss.forEach(function(schema){(schema.properties||[]).forEach(function(f){if((f.type==='select'||f.type==='multi_select')&&f.config&&f.config.options){OPTS[f.name]=f.config.options}})});
    renderSelectOptions();
    return reloadAll();
  }).catch(function(e){console.error('[database] 初始化失败:',e);goOffline()});
}
function goOffline(){offline=true;$('syncBox').className='sync off';setText('syncTxt','离线模式');$('offBanner').style.display='block';refreshAll()}
"""
    return _wrap_page("成都实习", body, nav, page_js, urls, active="intern")

def _wrap_page(title, body, nav, page_js, urls, active):
    # JS fetches all 3 tables + reloadAll is shared
    fetch_jobs = "function fetchJobs(){var out=[],cur=null;function once(){return db.query({databaseId:'GgZ71tywhs4HEZytFSqXTP',pageSize:100,startCursor:cur||undefined}).then(function(res){out=out.concat(res.results||[]);cur=res.nextCursor;return res.hasMore&&out.length<3000?once():out})}return once()}\n"
    fetch_apps = "function fetchApps(){var out=[],cur=null;function once(){return db.query({databaseId:'oBGkMFTv9Xv4Xn5gFOK18S',pageSize:100,startCursor:cur||undefined}).then(function(res){out=out.concat(res.results||[]);cur=res.nextCursor;return res.hasMore&&out.length<2000?once():out})}return once()}\n"
    fetch_ints = "function fetchInterns(){var out=[],cur=null;function once(){return db.query({databaseId:'tgH8096uENTaIj8RSY9qm5',pageSize:100,startCursor:cur||undefined}).then(function(res){out=out.concat(res.results||[]);cur=res.nextCursor;return res.hasMore&&out.length<1000?once():out})}return once()}\n"
    load = "function loadData(){if(offline)return Promise.resolve();return Promise.all([fetchJobs(),fetchApps(),fetchInterns()]).then(function(r){state.jobs=r[0];state.apps=r[1];state.interns=r[2]}).catch(function(e){console.error('[database] 数据加载失败:',e)});}\nfunction reloadAll(){return loadData().then(function(){refreshAll()});}\n"
    js = "(function(){\n'use strict';\n" + SHARED_JS + "\n" + fetch_jobs + fetch_apps + fetch_ints + load + page_js + "\nif(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',init)}else{init()}\n})();"

    return f"""<!DOCTYPE html>
<!-- 本工作台通过 WorkBuddy 资料库能力（library skill）搭建、存储和部署 -->
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{title} · 秋招求职台</title>
<style>{CSS}</style>
</head>
<body>
{nav}
<div class="wrap">
<div class="banner" id="offBanner">离线模式：未连接到在线数据表，数据读写暂不可用。请通过资料库链接打开本页面。</div>
{body}
</div>
{LNKMODAL_HTML}
<script>{js}</script>
</body>
</html>
"""


# ----------- build ----------
URLS = {
    "overview": "https://www.workbuddy.cn/space/d/szZlSjyPnnpGwDW4OD4y0X",
    "autumn":   "https://www.workbuddy.cn/space/d/G9pPkUVWIc6Fk43Mnn1csc",
    "soe":      "https://www.workbuddy.cn/space/d/PQ5cLpifIyB1CaQB2OIMrm",
    "intern":   "https://www.workbuddy.cn/space/d/JgXPaIiaDMGt2xH3vBftAo",
}
URLS_PLACEHOLDER = URLS  # final real URLs now

# Per-page canonical schemas (subset of fields actually rendered)
SCHEMAS = {
    "overview": ["公司","批次","岗位方向","工作地点","优先级","投递状态","网申开始","截止日期","投递链接","来源","备注",
                 "岗位","当前阶段","投递日期","下次节点","节点说明","复盘笔记","相关链接"],
    "autumn":   ["公司","批次","岗位方向","工作地点","优先级","投递状态","网申开始","截止日期","投递链接","来源","备注"],
    "soe":      ["公司","批次","岗位方向","工作地点","优先级","投递状态","网申开始","截止日期","投递链接","来源","备注"],
    "intern":   ["公司","岗位名称","薪资","工作地点","岗位要求","投递状态","投递链接","来源","备注"],
}

def main():
    here = Path(__file__).parent
    workspace = here.parent
    # read original canonical schema if exists
    canon_path = workspace / "canonical_schema.json"
    if canon_path.exists():
        full = json.loads(canon_path.read_text(encoding="utf-8"))
    else:
        full = {"properties": {}, "field_mapping": {}, "options_map": {}}

    p_over = _wrap_marker("00-总览台.html", page_overview(URLS))
    p_aut = _wrap_marker("01-秋招岗位台.html", page_autumn(URLS))
    p_soe = _wrap_marker("02-央国企台.html", page_soe(URLS))
    p_int = _wrap_marker("03-成都实习台.html", page_intern(URLS))
    (here/p_over['filename']).write_text(p_over['content'], encoding='utf-8')
    (here/p_aut['filename']).write_text(p_aut['content'], encoding='utf-8')
    (here/p_soe['filename']).write_text(p_soe['content'], encoding='utf-8')
    (here/p_int['filename']).write_text(p_int['content'], encoding='utf-8')
    # 只有显式 QIUZHAO_EXPORT_ROOT=1 时才另外导出一份到上级目录（给资料库导入用），
    # 默认不导出，保证 CI 里 `git diff --exit-code` 干净。
    if os.environ.get("QIUZHAO_EXPORT_ROOT") == "1":
        (workspace/p_over['filename']).write_text(p_over['content'], encoding='utf-8')
        (workspace/p_aut['filename']).write_text(p_aut['content'], encoding='utf-8')
        (workspace/p_soe['filename']).write_text(p_soe['content'], encoding='utf-8')
        (workspace/p_int['filename']).write_text(p_int['content'], encoding='utf-8')
        print("exported 4 pages to", workspace)
    # write per-page schema files
    for name, fields in SCHEMAS.items():
        sub = {"properties": {k: v for k, v in full["properties"].items() if k in fields},
               "field_mapping": {k: v for k, v in full.get("field_mapping", {}).items() if k in fields},
               "options_map": full.get("options_map", {})}
        (here/f"canonical_{name}.json").write_text(json.dumps(sub, ensure_ascii=False), encoding='utf-8')
    for f in [p_over, p_aut, p_soe, p_int]:
        print(f"wrote {f['filename']}, {len(f['content'])} bytes")

def _wrap_marker(filename, content):
    return {"filename": filename, "content": content}


if __name__ == "__main__":
    main()
