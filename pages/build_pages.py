#!/usr/bin/env python3
"""Build 4 modular HTML pages for the qiuzhao workbench."""
from pathlib import Path
import json, re

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
  --bg:#f3f5fb; --card:#ffffff; --line:#e6eaf2; --txt:#1a2233; --sub:#69718a;
  --pri:#3b5bfd; --pri2:#7c3aed; --pri-soft:#eef1fe;
  --red:#e5484d; --red-soft:#fdeced; --red-line:#f6c6c8;
  --orange:#e58f0b; --orange-soft:#fdf4e3; --orange-line:#f2ddb5;
  --green:#0a9d6c; --green-soft:#e6f7f0;
  --grad:linear-gradient(135deg,#3b5bfd,#7c3aed);
  --grad-blue:linear-gradient(135deg,#0ea5e9,#3b5bfd);
  --grad-red:linear-gradient(135deg,#e5484d,#f97316);
  --grad-amber:linear-gradient(135deg,#e58f0b,#f59e0b);
  --grad-green:linear-gradient(135deg,#0a9d6c,#10c98a);
  --radius:16px;
  --shadow:0 1px 2px rgba(23,32,64,.04),0 4px 16px rgba(23,32,64,.06);
  --shadow-hi:0 2px 4px rgba(23,32,64,.05),0 12px 32px rgba(23,32,64,.10);
}
*{margin:0;padding:0;box-sizing:border-box}
::-webkit-scrollbar{width:8px;height:8px}
::-webkit-scrollbar-thumb{background:#d3dae6;border-radius:99px}
::-webkit-scrollbar-thumb:hover{background:#bcc5d8}
::selection{background:rgba(59,91,253,.18)}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:var(--txt);font-size:15px;line-height:1.55;padding-bottom:env(safe-area-inset-bottom);
  background:radial-gradient(1100px 480px at 88% -120px,rgba(124,58,237,.09),transparent 62%),
             radial-gradient(900px 420px at -8% -60px,rgba(59,91,253,.09),transparent 58%),
             var(--bg);
  background-attachment:fixed}
.wrap{max-width:1000px;margin:0 auto;padding:0 16px 80px}
/* ---------- 顶栏：毛玻璃 ---------- */
nav.tabbar{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.72);backdrop-filter:saturate(180%) blur(16px);-webkit-backdrop-filter:saturate(180%) blur(16px);border-bottom:1px solid rgba(230,234,242,.9)}
nav.tabbar .inner{max-width:1000px;margin:0 auto;display:flex;align-items:center;gap:6px;padding:10px 16px;overflow-x:auto;-webkit-overflow-scrolling:touch}
nav.tabbar a.logo{font-weight:800;font-size:16px;color:var(--txt);text-decoration:none;display:flex;align-items:center;gap:8px;flex:none;margin-right:6px;letter-spacing:.2px}
nav.tabbar a.logo svg{width:28px;height:28px;background:var(--grad);border-radius:8px;padding:6px;stroke:#fff;box-shadow:0 2px 8px rgba(59,91,253,.35);flex:none}
nav.tabbar .tab{flex:none;padding:8px 15px;border-radius:999px;font-size:13px;color:var(--sub);text-decoration:none;font-weight:600;white-space:nowrap;border:1px solid transparent;background:transparent;transition:background .15s,color .15s}
nav.tabbar .tab[aria-current="page"]{background:var(--grad);color:#fff;border-color:transparent;box-shadow:0 2px 10px rgba(59,91,253,.35)}
nav.tabbar .tab:not([aria-current]):hover{background:rgba(59,91,253,.08);color:var(--pri)}
nav.tabbar .sync{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--sub);margin-left:auto;flex:none;background:rgba(255,255,255,.9);border:1px solid var(--line);border-radius:999px;padding:5px 11px;white-space:nowrap}
nav.tabbar .sync .dot{width:8px;height:8px;border-radius:50%;background:var(--green);box-shadow:0 0 0 3px rgba(10,157,108,.15)}
nav.tabbar .sync.off .dot{background:var(--red);box-shadow:0 0 0 3px rgba(229,72,77,.15)}
nav.tabbar .sync.warn .dot{background:var(--orange);box-shadow:0 0 0 3px rgba(229,143,11,.15)}
/* ---------- Hero 横幅 ---------- */
.hero{max-width:1000px;margin:18px auto 0;padding:0 16px}
.hero .hero-in{border-radius:20px;padding:22px 24px;color:#fff;display:flex;align-items:center;gap:16px;position:relative;overflow:hidden;background:var(--grad);box-shadow:0 10px 28px rgba(59,91,253,.30)}
.hero .hero-in::before{content:'';position:absolute;right:-50px;top:-80px;width:230px;height:230px;border-radius:50%;background:rgba(255,255,255,.14)}
.hero .hero-in::after{content:'';position:absolute;right:70px;bottom:-90px;width:160px;height:160px;border-radius:50%;background:rgba(255,255,255,.09)}
.hero h1{font-size:21px;font-weight:800;letter-spacing:.3px;margin:0 0 3px;position:relative}
.hero p{font-size:13px;opacity:.88;margin:0;position:relative}
.hero .hero-ic{width:48px;height:48px;margin-left:auto;flex:none;opacity:.95;position:relative;filter:drop-shadow(0 2px 6px rgba(0,0,0,.15))}
.hero.blue .hero-in{background:var(--grad-blue);box-shadow:0 10px 28px rgba(14,165,233,.28)}
.hero.red .hero-in{background:var(--grad-red);box-shadow:0 10px 28px rgba(229,72,77,.26)}
.hero.amber .hero-in{background:var(--grad-amber);box-shadow:0 10px 28px rgba(229,143,11,.26)}
.banner{display:none;background:var(--red-soft);color:var(--red);border:1px solid var(--red-line);border-radius:var(--radius);padding:12px 16px;margin:14px 0;font-size:14px}
/* ---------- 区块卡片 ---------- */
section{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:18px;margin:16px 0}
section>h2{font-size:16px;display:flex;align-items:center;gap:10px;margin-bottom:14px;font-weight:700}
section>h2 svg{width:32px;height:32px;flex:none;background:#f0f3fa;border-radius:9px;padding:6px}
section>h2 .cnt{margin-left:auto;font-size:12px;color:var(--sub);font-weight:500;background:#f4f6fb;border-radius:999px;padding:3px 10px}
#todayList{display:flex;flex-direction:column;gap:8px}
.titem{display:flex;align-items:center;gap:10px;padding:12px 14px;border-radius:12px;background:#fafbfe;border:1px solid var(--line);flex-wrap:wrap;transition:border-color .15s,box-shadow .15s}
.titem:hover{box-shadow:var(--shadow)}
.titem.red{background:var(--red-soft);border-color:var(--red-line)}
.titem.orange{background:var(--orange-soft);border-color:var(--orange-line)}
.titem.blue{background:var(--pri-soft);border-color:#ccd8fb}
.titem .badge{font-size:11px;font-weight:700;border-radius:7px;padding:3px 9px;flex:none;color:#fff;letter-spacing:.3px}
.titem.red .badge{background:var(--grad-red)}.titem.orange .badge{background:var(--grad-amber)}.titem.blue .badge{background:var(--grad)}
.titem .tinfo{flex:1;min-width:180px}
.titem .tinfo b{font-size:14px}
.titem .tinfo span{display:block;font-size:12px;color:var(--sub);margin-top:1px}
.titem .btns{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.titem .tdrop{color:var(--sub)}
.titem .tdrop:hover{background:var(--red-soft);color:var(--red);border-color:var(--red-line)}
.empty{color:var(--sub);font-size:14px;text-align:center;padding:30px 0}
/* ---------- 统计卡 ---------- */
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:0}
.stat{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:18px 14px 15px;text-align:center;box-shadow:var(--shadow);position:relative;overflow:hidden;transition:transform .15s,box-shadow .15s}
.stat:hover{transform:translateY(-2px);box-shadow:var(--shadow-hi)}
.stat::before{content:'';position:absolute;top:0;left:0;right:0;height:3px}
.stat:nth-child(1)::before{background:var(--grad)}
.stat:nth-child(2)::before{background:var(--grad-green)}
.stat:nth-child(3)::before{background:var(--grad-red)}
.stat:nth-child(4)::before{background:var(--grad-amber)}
.stat b{font-size:30px;display:block;line-height:1.15;font-weight:800;font-variant-numeric:tabular-nums;letter-spacing:-.5px}
.stat:nth-child(1) b{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.stat:nth-child(2) b{background:var(--grad-green);-webkit-background-clip:text;background-clip:text;color:transparent}
.stat:nth-child(4) b{background:var(--grad-amber);-webkit-background-clip:text;background-clip:text;color:transparent}
.stat span{font-size:12px;color:var(--sub);display:block;margin-top:5px;font-weight:500}
.stat.danger{background:linear-gradient(180deg,#fff5f5,#fff);border-color:var(--red-line)}
.stat.danger b{background:var(--grad-red);-webkit-background-clip:text;background-clip:text;color:transparent}
/* ---------- 网格/筛选 ---------- */
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:start}
.filters{display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap}
.filters input,.filters select{flex:1;min-width:120px;height:40px;border:1px solid var(--line);border-radius:10px;padding:0 12px;background:#fff;font-size:14px;font-family:inherit;transition:border-color .15s,box-shadow .15s}
.cards{display:flex;flex-direction:column;gap:10px}
.jcard,.acard{background:#fff;border:1px solid var(--line);border-radius:14px;padding:13px 15px;display:flex;flex-direction:column;gap:6px;transition:box-shadow .18s,transform .18s,border-color .18s}
.jcard:hover,.acard:hover{box-shadow:var(--shadow-hi);transform:translateY(-2px);border-color:#d5dcea}
.jcard.soe{border-color:var(--red-line);background:linear-gradient(180deg,#fffafa,#fff);box-shadow:inset 3px 0 0 var(--red)}
.jrow{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.jrow b{font-size:15px;flex:none}
.tag{font-size:11px;font-weight:600;padding:2.5px 9px;border-radius:999px;background:var(--pri-soft);color:var(--pri);flex:none}
.tag.ok{background:var(--green-soft);color:var(--green)}
.tag.bad{background:var(--red-soft);color:var(--red)}
.tag.soe{background:var(--red-soft);color:var(--red)}
.tag.gray{background:#eef0f4;color:#6b7280}
.jmeta{font-size:12px;color:var(--sub)}
.jnote{font-size:13px;color:var(--txt);background:#f7f9fd;border:1px solid #eef1f8;border-radius:8px;padding:7px 10px;margin:2px 0 0}
.jacts{display:flex;gap:6px;flex-wrap:wrap;margin-top:4px;align-items:center}
/* ---------- 按钮 ---------- */
.btn{appearance:none;border:0;cursor:pointer;padding:0 14px;height:36px;border-radius:10px;font-size:13px;font-weight:600;background:var(--card);color:var(--txt);font-family:inherit;text-decoration:none;display:inline-flex;align-items:center;justify-content:center;min-height:36px;transition:transform .08s,box-shadow .15s,filter .15s,background .15s}
.btn:active{transform:translateY(1px)}
.btn:disabled{opacity:.5;cursor:not-allowed}
.btn-sm{height:32px;padding:0 11px;font-size:12px;min-height:32px;border-radius:9px}
.btn-pri{background:var(--grad);color:#fff;box-shadow:0 2px 10px rgba(59,91,253,.30)}
.btn-pri:hover{filter:brightness(1.07)}
.btn-ghost{background:#fff;color:var(--pri);border:1px solid #ccd8fb}
.btn-ghost:hover{background:var(--pri-soft)}
.btn-go{background:var(--grad-green);color:#fff;border:1px solid transparent;box-shadow:0 2px 8px rgba(10,157,108,.25)}
.btn-go:hover{filter:brightness(1.06)}
.btn-search{background:#fff;color:var(--sub);border:1px dashed #c3cad6}
.btn-search:hover{color:var(--pri);border-color:#a9b6d8}
.btn-danger{background:#fff;color:var(--red);border:1px solid var(--red-line)}
.btn-gray{background:#f1f3f7;color:var(--sub);border:1px solid var(--line)}
.btn-gray:hover{background:#e8ebf2}
.btn-nav{background:#fff;color:var(--pri);border:1px solid #ccd8fb;height:52px;padding:0 18px;font-size:14px;display:flex;align-items:center;gap:8px;text-decoration:none;border-radius:14px;transition:background .15s,box-shadow .15s,transform .15s}
.btn-nav:hover{background:var(--pri-soft);box-shadow:var(--shadow);transform:translateY(-1px)}
.btn-nav .meta{font-size:11px;color:var(--sub);font-weight:normal;display:block;margin-top:2px}
select{height:36px;border:1px solid var(--line);border-radius:10px;padding:0 8px;background:#fff;font-size:13px;font-family:inherit;transition:border-color .15s,box-shadow .15s}
/* ---------- 模块入口卡 ---------- */
.moduleCards{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:14px 0}
.moduleCard{background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px;text-decoration:none;color:var(--txt);display:flex;flex-direction:column;gap:8px;transition:transform .15s,box-shadow .15s,border-color .15s;position:relative;overflow:hidden}
.moduleCard::after{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:var(--grad);opacity:0;transition:opacity .15s}
.moduleCard:hover{transform:translateY(-3px);box-shadow:var(--shadow-hi);border-color:#d5dcea}
.moduleCard:hover::after{opacity:1}
.moduleCard .mh{display:flex;align-items:center;gap:10px;font-weight:700;font-size:15px}
.moduleCard .mh svg{width:36px;height:36px;border-radius:10px;background:#f0f3fa;padding:8px;flex:none}
.moduleCard svg{width:20px;height:20px}
.moduleCard .mmeta{font-size:12px;color:var(--sub);line-height:1.5}
.moduleCard .mstat{font-size:11px;background:var(--pri-soft);color:var(--pri);border-radius:999px;padding:3px 10px;align-self:flex-start;font-weight:700;margin-left:auto}
.moduleCard.danger .mstat{background:var(--red-soft);color:var(--red)}
.moduleCard.warn .mstat{background:var(--orange-soft);color:var(--orange)}
/* ---------- chips/图例 ---------- */
.batchChips{display:flex;gap:6px;margin-bottom:10px}
.chip{min-height:32px;padding:0 16px;border-radius:999px;border:1px solid var(--line);background:#fff;color:var(--sub);font-size:12px;font-weight:600;cursor:pointer;font-family:inherit;transition:all .15s}
.chip:hover{border-color:#c3cbe0;color:var(--txt)}
.chip.active{background:var(--grad);color:#fff;border-color:transparent;box-shadow:0 2px 8px rgba(59,91,253,.3)}
.legend{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:8px;font-size:12px;color:var(--sub)}
.legend span{display:flex;align-items:center;gap:6px}
.legend .g{width:10px;height:10px;border-radius:3px;background:var(--grad-green);display:inline-block}
.legend .s{width:10px;height:10px;border-radius:3px;border:1px dashed #c3cad6;display:inline-block;background:#fff}
/* ---------- 表单 ---------- */
details.add{margin-bottom:10px;border:1px dashed #cdd5e6;border-radius:12px;padding:0 12px;background:#fafbfe}
details.add summary{cursor:pointer;padding:10px 0;font-weight:600;font-size:13px;color:var(--sub);list-style:none}
details.add[open] summary{padding-top:8px}
details.add form{padding:8px 0}
.formrow{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px}
.formrow>div,.fl{display:flex;flex-direction:column;gap:4px}
.fl{font-size:12px;color:var(--sub);font-weight:600;margin-bottom:6px}
input[type="text"],input[type="search"],input:not([type]){height:40px;border:1px solid var(--line);border-radius:10px;padding:0 12px;background:#fff;font-size:14px;font-family:inherit;transition:border-color .15s,box-shadow .15s}
textarea{width:100%;min-height:64px;border:1px solid var(--line);border-radius:10px;padding:8px 12px;font-size:14px;font-family:inherit;resize:vertical;transition:border-color .15s,box-shadow .15s}
input[type="date"]{height:40px;border:1px solid var(--line);border-radius:10px;padding:0 10px;font-size:14px;font-family:inherit;transition:border-color .15s,box-shadow .15s}
input:focus,select:focus,textarea:focus{outline:none;border-color:var(--pri);box-shadow:0 0 0 3px rgba(59,91,253,.13)}
label.fl{display:block;margin:6px 0 0}
.mtail{font-size:11px;color:var(--sub);text-align:center;margin-top:4px}
.navSpacer{height:8px}
/* ---------- 公司情报面板 ---------- */
.intel-card{background:#fff;border-radius:18px;max-width:560px;width:100%;max-height:82vh;overflow:auto;padding:20px;box-shadow:0 24px 60px rgba(15,23,42,.25);animation:pop .18s ease}
.intel-head{display:flex;align-items:flex-start;gap:10px}
.intel-head b{font-size:17px;display:block}
.intel-head p{font-size:12px;color:var(--sub);margin:2px 0 0}
.intel-head .iclose{margin-left:auto;border:0;background:#f1f3f7;width:30px;height:30px;border-radius:9px;cursor:pointer;font-size:13px;color:var(--sub);flex:none}
.intel-head .iclose:hover{background:#e6e9f0;color:var(--txt)}
.isec{font-size:12px;font-weight:700;color:var(--pri);margin:16px 0 8px;display:flex;align-items:center;gap:8px}
.isec::after{content:'';flex:1;height:1px;background:var(--line)}
.iitem{display:flex;align-items:center;gap:10px;padding:10px 12px;border:1px solid var(--line);border-radius:12px;margin-bottom:6px;background:#fafbfe;transition:box-shadow .15s,border-color .15s}
.iitem:hover{box-shadow:var(--shadow);border-color:#d5dcea}
.iitem .iinfo{flex:1;min-width:0}
.iitem .iinfo b{font-size:14px;display:block}
.iitem .iinfo span{font-size:12px;color:var(--sub)}
/* ---------- 日常实习直通车 ---------- */
.xgrid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.xcard{background:#fff;border:1px solid var(--line);border-radius:14px;padding:13px 15px;display:flex;flex-direction:column;gap:6px;transition:box-shadow .18s,transform .18s,border-color .18s}
.xcard:hover{box-shadow:var(--shadow-hi);transform:translateY(-2px);border-color:#f0d9ae}
.xhead{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.xhead b{font-size:15px;flex:none}
/* ---------- 公司情报快捷搜索 ---------- */
.qintel{display:flex;gap:8px;margin-bottom:10px}
.qintel input{flex:1;height:40px;border:1px solid var(--line);border-radius:8px;padding:0 12px;font-size:14px;font-family:inherit;background:#fff;min-width:0}
.qintel input:focus{outline:none;border-color:var(--pri);box-shadow:0 0 0 3px var(--pri-soft)}
/* ---------- 弹层 ---------- */
#lnkModal .lnk-card{background:#fff;border-radius:18px;max-width:520px;width:100%;padding:20px;box-shadow:0 24px 60px rgba(15,23,42,.25);animation:pop .18s ease}
@keyframes pop{from{transform:scale(.94);opacity:0}to{transform:scale(1);opacity:1}}
@media (max-width:768px){
  .stats,.grid,.moduleCards,.formrow{grid-template-columns:1fr}
  nav.tabbar .inner{padding:8px 12px}
  nav.tabbar .sync{font-size:11px;padding:4px 8px}
  .wrap{padding:0 12px 60px}
  .hero{padding:0 12px}
  .hero .hero-in{padding:16px 18px}
  .hero h1{font-size:18px}
  .hero .hero-ic{width:38px;height:38px}
  .stat b{font-size:24px}
  .xgrid{grid-template-columns:1fr}
}
"""

# shared utility JS that every page needs
SHARED_JS = """
var JOBS_ID='{JOBS_ID}', APPS_ID='{APPS_ID}', INTERN_ID='{INTERN_ID}';
var OPTS={{}};
var state={{jobs:[],apps:[],interns:[],todayMine:true,batchMode:''}};
var STAGES=['已投递','笔试','一面','二面','HR面','Offer','感谢信'];
var DROP_STAGE='已终止';
var db=null,offline=false;
var CAREER_KW={CAREER_KW};
var MY_CITY_KW={MY_CITY_KW};
var SOE_KW={SOE_KW};

function $(id){{return document.getElementById(id)}}
// 不用正则的 trim：本文件是 Python 模板串，JS 正则里的反斜杠转义（空白/Unicode/词边界等）
// 会被 Python 先解析掉，轻则丢字符重则整页脚本失效（见 pages/check_escapes.py）。纯 charCode 判断最稳。
function trimStr(s){{s=String(s==null?'':s);var a=0,b=s.length;while(a<b&&s.charCodeAt(a)<=32)a++;while(b>a&&s.charCodeAt(b-1)<=32)b--;return s.slice(a,b)}}
function esc(s){{return String(s==null?'':s).replace(/[&<>""]/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]}})}}
function dayStr(d){{var p=function(n){{return (n<10?'0':'')+n}};return d.getFullYear()+'-'+p(d.getMonth()+1)+'-'+p(d.getDate())}}
function today(){{return dayStr(new Date())}}
// 日期字段可能是字符串、对象（date/text/value/start 字段）或 Date，统一取出前 10 位
function dOnly(v){{if(v==null)return '';if(typeof v==='object'){{v=v.date||v.text||v.value||v.start||''}}return String(v).slice(0,10)}}
function diffDays(a,b){{if(!a||!b)return null;return Math.round((Date.parse(b)-Date.parse(a))/86400000)}}
function optId(field,text){{var l=OPTS[field]||[];for(var i=0;i<l.length;i++){{if(l[i].text===text)return l[i].id}}return text}}
function optText(field,idOrText){{var l=OPTS[field]||[];for(var i=0;i<l.length;i++){{if(l[i].id===idOrText)return l[i].text}}return idOrText||''}}
function fieldText(j,f){{var v=j[f];if(v==null)return '';if(typeof v==='object')return String(v.text||'');return String(v)}}
// 资料库返回的字段值可能是对象（{{text:'x'}} / {{date:'x'}} / [{{...}}]），
// 直接拼进字符串会渲染成 [object Object]，统一在这里拍平成可读文本
function plain(v){{if(v==null)return '';if(typeof v==='object'){{if(typeof v.length==='number')v=(v&&v[0])||{{}};return String(v.text||v.value||v.name||v.date||v.link||'')}}return String(v)}}
function urlVal(v){{if(!v)return {{text:'',link:''}};if(typeof v==='object'){{if(typeof v.length==='number')v=(v&&v[0])||{{}};return {{text:String(v.text||v.link||''),link:String(v.link||v.text||'')}}}}return {{text:String(v),link:String(v)}}}}
function recId(r){{return (r&&(r._id||r.record_id||r.id))||''}}
function webSearchUrl(q){{return 'https://www.bing.com/search?q='+encodeURIComponent(q+' 校招 网申入口')}}
function searchUrl(q){{return 'https://www.nowcoder.com/search/all?query='+encodeURIComponent(q+' 校招')}}

// 分类结果缓存：列表每次刷新都会对全部岗位重跑关键词扫描（600+ 条 × 56 个关键词），
// 缓存后同一批记录只算一次；loadData 成功时整体失效重建。
var _clsCache={{}};
function recKey(j){{return recId(j)||(fieldText(j,'公司')+'|'+fieldText(j,'岗位方向')+'|'+fieldText(j,'工作地点'))}}
function isSOE(j){{var k='s'+recKey(j);if(k in _clsCache)return _clsCache[k];var c=fieldText(j,'公司'),v=false;for(var i=0;i<SOE_KW.length;i++){{if(c.indexOf(SOE_KW[i])>=0){{v=true;break}}}}_clsCache[k]=v;return v}}
function mineMatch(j){{var k='m'+recKey(j);if(k in _clsCache)return _clsCache[k];var c=fieldText(j,'岗位方向'),v=false;for(var i=0;i<CAREER_KW.length;i++){{if(c.indexOf(CAREER_KW[i])>=0){{v=true;break}}}}if(v){{v=false;var loc=fieldText(j,'工作地点');for(var j2=0;j2<MY_CITY_KW.length;j2++){{if(loc.indexOf(MY_CITY_KW[j2])>=0){{v=true;break}}}}}}_clsCache[k]=v;return v}}
// 牛客公司 ID（用于企业主页/面经/真题深链），非数字一律丢弃避免拼出坏链接
function nkId(rec){{var v=rec&&rec['牛客ID'];if(v==null)return '';if(typeof v==='object')v=v.text||v.value||'';return String(v).replace(/[^0-9]/g,'')}}
function jobStatus(j){{return j['投递状态']?optText('投递状态',typeof j['投递状态']==='object'?j['投递状态'].text||'':String(j['投递状态'])):'待投递'}}
function appStage(a){{return a['当前阶段']?optText('当前阶段',typeof a['当前阶段']==='object'?a['当前阶段'].text||'':String(a['当前阶段'])):'已投递'}}

function showLinkModal(link){{var m=$('lnkModal');if(!m){{alert('投递链接：'+link);return}}$('lnkTxt').textContent=link;m.style.display='flex';$('lnkCopy').onclick=function(){{var done=function(){{$('lnkCopy').textContent='已复制'}};try{{var ta=document.createElement('textarea');ta.value=link;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();var ok=document.execCommand('copy');document.body.removeChild(ta);if(ok){{done();return}}}}catch(e){{}}if(navigator.clipboard&&navigator.clipboard.writeText){{navigator.clipboard.writeText(link).then(done)}}}}}};
// 是否已是完整 http(s) 链接 / 是否长得像域名（都不用正则：本文件是 Python 模板串，
// JS 正则里的反斜杠转义会被 Python 先解析掉，可能悄悄改坏脚本）
function isHttpUrl(u){{u=String(u).toLowerCase();return u.indexOf('http://')===0||u.indexOf('https://')===0}}
function looksDomain(u){{
  u=String(u);
  if(u.indexOf(' ')>-1||u.indexOf(':')>-1||u.indexOf('@')>-1)return false;
  var cut=u.length,k;
  for(k=0;k<u.length;k++){{var c=u.charAt(k);if(c==='/'||c==='?'||c==='#'){{cut=k;break}}}}
  var host=u.slice(0,cut),dot=host.indexOf('.');
  return dot>0&&dot<host.length-2;
}}
// 外链统一出口：只放行 http(s)，挡掉 javascript:/data: 等协议；新窗口一律 noopener+noreferrer，
// 避免被打开页面通过 window.opener 反向拿到本页的 SDK 与全部投递数据。
function openLink(link){{if(!link){{alert('这条记录没有填链接');return}}var safe=trimStr(link);if(!isHttpUrl(safe)){{if(looksDomain(safe))safe='https://'+safe;else{{alert('链接协议不受支持，已阻止打开');return}}}}var w=null;try{{w=window.open(safe,'_blank','noopener,noreferrer')}}catch(e){{}}if(!w)showLinkModal(safe);}}
// 顶部同步状态点：ok / warn（本次拉取失败但可重试）/ err / off（无 SDK）
function setSync(state){{var b=$('syncBox'),t=$('syncTxt');if(!b)return;b.className='sync'+(state==='ok'?'':state==='warn'?' warn':' off');if(t)t.textContent=state==='ok'?'已同步':state==='warn'?'同步异常':state==='err'?'同步失败':'离线模式';}}
function jobLink(j){{return urlVal(j['投递链接']).link}}
function jobJump(j){{var l=jobLink(j);var c=plain(j['公司']);return l||searchUrl(c)||webSearchUrl(c)}}

/* ---------- 公司情报面板 ---------- */
/* nk = 牛客 companyId（表里的「牛客ID」字段）。有 ID 时走牛客企业档案精准深链，
   没有则退化为牛客全网检索，保证任何一条记录都有可用的情报入口。 */
function intelLinks(c,nk){{
  var e=encodeURIComponent,g=[];
  if(nk){{
    var base='https://www.nowcoder.com/enterprise/'+e(nk);
    g.push({{sec:'牛客企业档案 · 精准直达',items:[
      {{t:'牛客 · 企业主页',d:'该公司在牛客的校招职位与招聘动态',u:base}},
      {{t:'牛客 · 面经',d:'同家公司历年面试流程与面试题回忆帖',u:base+'/interview'}},
      {{t:'牛客 · 笔试真题',d:'该公司笔试题库，可在线自测',u:base+'/question/company'}},
      {{t:'牛客 · 薪资爆料',d:'各职级 offer 薪资、涨薪与年终奖信息',u:base+'/salary'}},
      {{t:'牛客 · 讨论区',d:'offer 对比、加班与部门氛围讨论',u:base+'/discussion'}}
    ]}});
  }}
  g.push({{sec:'牛客全网检索',items:[
    {{t:'牛客 · 面经搜索',d:'笔试真题、面试流程、通过率、入职体验帖',u:'https://www.nowcoder.com/search/all?query='+e(c+' 面经')}},
    {{t:'牛客 · 公司讨论区',d:'薪资爆料、offer 对比、加班情况',u:'https://www.nowcoder.com/search/all?query='+e(c+' 公司')}},
    {{t:'牛客 · 面经专区',d:'牛客经验分享频道，按公司/岗位翻帖',u:'https://www.nowcoder.com/experience/0?query='+e(c)}}
  ]}});
  g.push({{sec:'公司背景',items:[
    {{t:'百度百科',d:'主营业务、规模、母公司背景',u:'https://baike.baidu.com/item/'+e(c)}},
    {{t:'爱企查 · 工商信息',d:'股权结构、注册信息、是否国企/经营风险',u:'https://aiqicha.baidu.com/s?q='+e(c)}},
    {{t:'官方网站',d:'找官方招聘频道与业务线介绍',u:'https://www.bing.com/search?q='+e(c+' 官网 招聘')}}
  ]}});
  g.push({{sec:'薪资与评价',items:[
    {{t:'看准网',d:'员工评价、面试题库、薪资爆料',u:'https://www.kanzhun.com/search/?query='+e(c)}},
    {{t:'职友集',d:'薪资统计、招聘趋势、公司排行',u:'https://www.jobui.com/search/?keyword='+e(c)}},
    {{t:'全网经验帖聚合',d:'知乎/博客的面经与校招经验搜索',u:'https://www.bing.com/search?q='+e(c+' 校招 面经 入职体验')}}
  ]}});
  return g;
}}
function showIntel(company,nk){{
  var c=(company||'').trim()||'未命名公司';
  nk=nk==null?'':String(typeof nk==='object'?(nk.text||''):nk).replace(/[^0-9]/g,'');
  var m=$('intelModal');
  if(!m){{openLink(webSearchUrl(c));return}}
  $('intelName').textContent=c+' · 公司情报';
  var html='';
  intelLinks(c,nk).forEach(function(g){{
    html+='<div class="isec">'+g.sec+'</div>';
    g.items.forEach(function(it){{
      html+='<div class="iitem"><div class="iinfo"><b>'+it.t+'</b><span>'+it.d+'</span></div>'
           +'<button class="btn btn-pri btn-sm igoto" data-u="'+it.u.replace(/"/g,'&quot;')+'">打开</button></div>';
    }});
  }});
  $('intelBody').innerHTML=html;
  Array.prototype.forEach.call($('intelBody').querySelectorAll('.igoto'),function(b){{
    b.addEventListener('click',function(){{openLink(b.getAttribute('data-u'))}});
  }});
  m.style.display='flex';
}}
function bindIntelClose(){{
  var m=$('intelModal');if(!m)return;
  $('intelClose').addEventListener('click',function(){{m.style.display='none'}});
  m.addEventListener('click',function(e){{if(e.target===m)m.style.display='none'}});
  document.addEventListener('keydown',function(e){{if(e.key==='Escape')m.style.display='none'}});
}}
function bindExpress(){{
  Array.prototype.forEach.call(document.querySelectorAll('.xgo'),function(b){{
    b.addEventListener('click',function(){{openLink(b.getAttribute('data-u'))}});
  }});
  Array.prototype.forEach.call(document.querySelectorAll('.xintel'),function(b){{
    b.addEventListener('click',function(){{showIntel(b.getAttribute('data-c'),b.getAttribute('data-nk'))}});
  }});
}}

function setFieldText(root,name,val,dbid){{var el=root.querySelector('[data-field="'+name+'"]');if(!el)return;if(name==='投递链接'||name==='相关链接'){{var u=urlVal(val);el.style.display='';if(u.link){{el.className=name==='投递链接'?'btn btn-go btn-sm':'btn btn-ghost btn-sm';el.textContent=name==='投递链接'?'直达官网':'链接';el.setAttribute('href',u.link)}}else{{el.className='btn btn-search btn-sm';el.textContent=name==='投递链接'?'搜索网申入口':'搜索进度';el.removeAttribute('href')}}}}else{{el.textContent=plain(val)}}el.setAttribute('data-sp-bindable','database');el.setAttribute('data-sp-database-id',dbid)}}
function setText(id,v){{var el=$(id);if(el)el.textContent=v}}
function markBindable(el,dbid){{el.setAttribute('data-sp-bindable','database');el.setAttribute('data-sp-database-id',dbid)}}

/* ---------- 表单缓存（DSDK008） ---------- */
/* 只缓存本地草稿用途的表单值，且不上云：password/file/data-no-cache 以及命中
   密码·身份证·token·key 类字段名一律跳过；空值即删除（避免残留旧内容）；单条截断 500 字。 */
var CACHE_KEY='wb_qiuzhao_form_v1';
var CACHE_SKIP=/password|passwd|secret|token|api[-_]?key|身份证|银行卡/i;
var CACHE_MAX=65536;
var cacheTimer=null;
function cacheSaveForm(fid){{try{{var f=$(fid);if(!f)return;var data=JSON.parse(localStorage.getItem(CACHE_KEY)||'{{}}');Array.prototype.forEach.call(f.querySelectorAll('[name]'),function(el){{if(el.type==='password'||el.type==='file')return;if(el.hasAttribute('data-no-cache'))return;if(CACHE_SKIP.test(el.name||'')||CACHE_SKIP.test(el.getAttribute('data-field')||''))return;var k=fid+'.'+el.name,v=String(el.value==null?'':el.value).slice(0,500);if(!v){{delete data[k]}}else{{data[k]=v}}}});var s=JSON.stringify(data);if(s.length>CACHE_MAX)return;localStorage.setItem(CACHE_KEY,s)}}catch(e){{}}}}
function cacheDebounce(fid){{if(cacheTimer)clearTimeout(cacheTimer);cacheTimer=setTimeout(function(){{cacheSaveForm(fid)}},300)}}
function cacheRestoreForm(fid){{try{{var data=JSON.parse(localStorage.getItem(CACHE_KEY)||'{{}}');var f=$(fid);if(!f)return;Array.prototype.forEach.call(f.querySelectorAll('[name]'),function(el){{var k=fid+'.'+el.name;if(data[k]!==undefined&&el.type!=='password'&&el.type!=='file')el.value=data[k]}})}}catch(e){{}}}}
function cacheClearForm(fid){{try{{var data=JSON.parse(localStorage.getItem(CACHE_KEY)||'{{}}');Array.prototype.forEach.call(Object.keys(data),function(k){{if(k.indexOf(fid+'.')===0)delete data[k]}});localStorage.setItem(CACHE_KEY,JSON.stringify(data))}}catch(e){{}}}}
function bindFormCache(fid){{var f=$(fid);if(!f)return;f.addEventListener('input',function(){{cacheDebounce(fid)}});f.addEventListener('change',function(){{cacheDebounce(fid)}});cacheRestoreForm(fid);}}
function cacheWipeAll(){{try{{localStorage.removeItem(CACHE_KEY)}}catch(e){{}}}}

/* ---------- 连接与实时订阅 ---------- */
var DB_READY=null;      /* 由各页 init()/boot() 注入：重跑「取 schema → 渲染下拉 → 拉全量」 */
var _updBound=false,_updTimer=null;
/* 数据变更订阅：他人在表格改 / 其他端提交 / 脚本批量写都会回调（平台只通知「变了」，内容自己查）。
   能力探测后再注册，整页只注册一次（DSDK013）；700ms 去抖；刚拉过数（1200ms 内）直接跳过——
   本页每次写入后自己会调 reloadAll()，订阅事件只是回声，跳过可避免一次操作拉两轮数据。
   旧环境无 onUpdated → 静默降级，页面照常手动刷新。 */
function subscribeUpdates(){{
  if(_updBound||!db)return;
  if(typeof db.onUpdated!=='function')return;
  _updBound=true;
  try{{
    db.onUpdated(function(payload){{
      var ids=(payload&&payload.databaseIds)||[];
      if(!ids.length)return;
      if(Date.now()-_lastLoadAt<1200)return;
      if(_updTimer)clearTimeout(_updTimer);
      _updTimer=setTimeout(function(){{_updTimer=null;reloadAll()}},700);
    }});
  }}catch(e){{_updBound=false}}
}}
/* 取三表 schema → 合并 select 选项 → 触发各模块 setup → 拉全量数据 */
function initSchema(after){{
  return Promise.all([db.getSchema({{databaseId:'GgZ71tywhs4HEZytFSqXTP'}}),db.getSchema({{databaseId:'oBGkMFTv9Xv4Xn5gFOK18S'}}),db.getSchema({{databaseId:'tgH8096uENTaIj8RSY9qm5'}})]).then(function(ss){{
    ss.forEach(function(schema){{(schema.properties||[]).forEach(function(f){{if((f.type==='select'||f.type==='multi_select')&&f.config&&f.config.options){{OPTS[f.name]=f.config.options}}}})}});
    subscribeUpdates();
    if(after)after();
    return reloadAll();
  }});
}}
/* 离线横幅「重试连接」：重新探测 SDK → 重跑就绪链路；无就绪链路时退回整页刷新 */
function retryConnect(){{
  var b=$('offRetry'),o=$('offBanner');
  var done=function(ok){{if(b){{b.disabled=false;b.textContent='重试连接'}}if(ok&&o)o.style.display='none'}};
  if(b){{b.disabled=true;b.textContent='正在重连…'}}
  db=window.__SMART_PAGE__&&window.__SMART_PAGE__.database;
  if(!db){{setSync('off');done(false);return}}
  offline=false;
  if(!DB_READY){{location.reload();return}}
  Promise.resolve(DB_READY()).then(function(){{var ok=!_syncFailed;setSync(ok?'ok':'warn');done(ok)}},function(){{setSync('warn');done(false)}});
}}
document.addEventListener('click',function(e){{var t=e.target;if(t&&t.id==='offRetry')retryConnect()}});
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
<div id="lnkModal" style="display:none;position:fixed;inset:0;background:rgba(15,23,42,.5);backdrop-filter:blur(3px);-webkit-backdrop-filter:blur(3px);z-index:99;align-items:center;justify-content:center;padding:20px">
  <div class="lnk-card" style="background:#fff;border-radius:18px;max-width:520px;width:100%;padding:20px">
    <b style="font-size:15px">浏览器拦截了新窗口，复制链接去打开</b>
    <p id="lnkTxt" style="word-break:break-all;background:#f4f6fb;border:1px solid #e6eaf2;border-radius:10px;padding:11px;margin:12px 0 6px;font-size:13px;color:var(--pri);font-weight:500"></p>
    <p style="font-size:12px;color:var(--sub);margin:0 0 12px">手机端可长按上方链接选择复制，再粘贴到浏览器打开</p>
    <div style="display:flex;gap:8px;justify-content:flex-end">
      <button class="btn btn-gray btn-sm" id="lnkClose">关闭</button>
      <button class="btn btn-pri btn-sm" id="lnkCopy">复制链接</button>
    </div>
  </div>
</div>
"""

INTELMODAL_HTML = """
<div id="intelModal" style="display:none;position:fixed;inset:0;background:rgba(15,23,42,.5);backdrop-filter:blur(3px);-webkit-backdrop-filter:blur(3px);z-index:98;align-items:center;justify-content:center;padding:20px">
  <div class="intel-card">
    <div class="intel-head">
      <div><b id="intelName">公司情报</b><p>投递前先看：面经经验、公司背景、薪资评价</p></div>
      <button class="iclose" id="intelClose">✕</button>
    </div>
    <div id="intelBody"></div>
    <p style="font-size:11px;color:var(--sub);text-align:center;margin-top:14px">各条目在新窗口打开 · 沙箱内被拦截时会出现复制链接弹层</p>
  </div>
</div>
"""

HERO_ICONS = {
    "overview": '<svg class="hero-ic" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/></svg>',
    "autumn":   '<svg class="hero-ic" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>',
    "soe":      '<svg class="hero-ic" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 21V4"/><path d="M5 4c3-2 6 1.5 9 0s5-.5 7 .5V13c-2-1-4-1.5-7 0s-6-2-9 0"/></svg>',
    "intern":   '<svg class="hero-ic" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>',
}

def hero_html(cls, title, sub, icon_key):
    return ('<div class="hero {cls}"><div class="hero-in">'
            '<div class="hero-txt"><h1>{title}</h1><p>{sub}</p></div>'
            '{icon}</div></div>'
            ).format(cls=cls, title=title, sub=sub, icon=HERO_ICONS[icon_key])

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
  <div class="jmeta" style="margin:-2px 0 9px">每条可操作：<b>直达官网</b>／<b>搜网申入口</b> 去投递 ｜ <b>公司情报</b> 先看面经·评价·工商背景 ｜ <b>标记已投 / 节点已完成</b> 推进并记进投递跟踪 ｜ <b>不投了 / 去掉这条</b> 移出今日列表</div>
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
      <div class="mmeta">15 家官方日常实习通道直达 + 牛客实习批次自动同步</div>
    </a>
  </div>
</section>

<section>
  <h2><svg viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4 20-7z"/></svg>投递跟踪<span class="cnt" id="appCnt"></span></h2>
  <div class="qintel">
    <input id="qiInput" placeholder="表里没有的企业？输入任意公司名，直接查面经/薪资/官网">
    <button type="button" class="btn btn-pri" id="qiBtn">查企业情报</button>
  </div>
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
    if(n<0)items.push({kind:'job',level:'red',badge:'已过截止',title:plain(j['公司'])||'未命名公司',meta:'岗位：'+(plain(j['岗位方向'])||'未填')+' ｜ 截止 '+dd+'（已过'+(-n)+'天）',rec:j});
    else if(n<=3)items.push({kind:'job',level:'orange',badge:(n===0?'今天截止':'剩'+n+'天'),title:plain(j['公司'])||'未命名公司',meta:'岗位：'+(plain(j['岗位方向'])||'未填')+' ｜ 截止 '+dd,rec:j});
  });
  state.apps.forEach(function(a){
    var st=appStage(a);if(st==='Offer'||st==='感谢信'||st===DROP_STAGE)return;
    var nd=dOnly(a['下次节点']);if(!nd)return;
    var n=diffDays(t,nd);
    if(n<0)items.push({kind:'app',level:'red',badge:'节点已过',title:plain(a['公司'])+' · '+plain(a['岗位']),meta:st+' ｜ 原定 '+nd+'（'+(plain(a['节点说明'])||'未填说明')+'）',rec:a});
    else if(n<=1)items.push({kind:'app',level:'blue',badge:(n===0?'今天':'明天'),title:plain(a['公司'])+' · '+plain(a['岗位']),meta:st+' ｜ '+nd+'（'+(plain(a['节点说明'])||'未填说明')+'）',rec:a});
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
    if(it.kind==='job'){var jl=jobLink(it.rec);btns='<button class="btn btn-sm tgo '+(jl?'btn-go':'btn-search')+'">'+(jl?'直达官网':'搜网申入口')+'</button>';}
    else{var al=urlVal(it.rec['相关链接']).link;btns='<button class="btn btn-sm tgo '+(al?'btn-ghost':'btn-search')+'">'+(al?'查看链接':'搜公司')+'</button>';}
    btns+='<button class="btn btn-sm btn-ghost tintel">公司情报</button><button class="btn btn-sm btn-go tdone">'+(it.kind==='job'?'标记已投':'节点已完成')+'</button><button class="btn btn-sm btn-gray tdrop">'+(it.kind==='job'?'不投了':'去掉这条')+'</button>';
    d.innerHTML='<span class="badge">'+esc(it.badge)+'</span><div class="tinfo"><b>'+esc(it.title)+'</b><span>'+esc(it.meta)+'</span></div><div class="btns">'+btns+'</div>';
    d.querySelector('.tgo').addEventListener('click',function(){if(it.kind==='job'){var l=jobLink(it.rec);if(l){openLink(l)}else{showIntel(fieldText(it.rec,'公司'),nkId(it.rec))}}else{var al=urlVal(it.rec['相关链接']).link;if(al){openLink(al)}else{showIntel(fieldText(it.rec,'公司'),nkId(it.rec))}}});
    d.querySelector('.tintel').addEventListener('click',function(){showIntel(fieldText(it.rec,'公司'),nkId(it.rec))});
    d.querySelector('.tdone').addEventListener('click',function(){todayDone(it,this)});
    d.querySelector('.tdrop').addEventListener('click',function(){todayDrop(it,this)});
    box.appendChild(d);
  });
}
/* 今日处理 → 标记已完成：岗位=已投递+自动建档；投递跟踪=清空本次节点 */
function todayDone(it,btn){
  if(btn)btn.disabled=true;
  if(it.kind==='job'){
    db.updateRecord({databaseId:'GgZ71tywhs4HEZytFSqXTP',recordId:recId(it.rec),properties:{'投递状态':{select:'已投递'}}})
      .then(function(){return todaySyncTracking(it.rec)})
      .then(reloadAll)
      .catch(function(e){console.error('[database] 标记已投失败:'+((e&&e.message)||String(e)));if(btn)btn.disabled=false;alert('更新失败，请刷新后重试')});
  }else{
    db.updateRecord({databaseId:'oBGkMFTv9Xv4Xn5gFOK18S',recordId:recId(it.rec),properties:{'下次节点':{date:null}}})
      .then(reloadAll)
      .catch(function(e){console.error('[database] 清空节点失败:'+((e&&e.message)||String(e)));if(btn)btn.disabled=false;alert('更新失败，请刷新后重试')});
  }
}
/* 今日处理 → 去掉：岗位=不投了；投递跟踪=已终止（两条都从今日列表消失，可随时改回） */
function todayDrop(it,btn){
  var name=fieldText(it.rec,'公司')||'这条记录';
  var tip=it.kind==='job'
    ?'确定不再考虑「'+name+'」吗？该岗位会标记为「不投了」，之后不会再出现在今日处理里（可去岗位表改回）。'
    :'确定去掉「'+name+'」这条投递跟踪吗？会标记为「已终止」，不再出现在今日处理里（可在投递跟踪里改回阶段）。';
  if(!confirm(tip))return;
  if(btn)btn.disabled=true;
  if(it.kind==='job'){
    db.updateRecord({databaseId:'GgZ71tywhs4HEZytFSqXTP',recordId:recId(it.rec),properties:{'投递状态':{select:'不投了'}}})
      .then(reloadAll)
      .catch(function(e){console.error('[database] 标记失败:'+((e&&e.message)||String(e)));if(btn)btn.disabled=false;alert('更新失败，请刷新后重试')});
  }else{
    db.updateRecord({databaseId:'oBGkMFTv9Xv4Xn5gFOK18S',recordId:recId(it.rec),properties:{'当前阶段':{select:'已终止'},'下次节点':{date:null}}})
      .then(reloadAll)
      .catch(function(e){console.error('[database] 标记失败:'+((e&&e.message)||String(e)));if(btn)btn.disabled=false;alert('更新失败，请刷新后重试')});
  }
}
/* 岗位标记已投后，若跟踪表还没有这家公司就自动建档 */
function todaySyncTracking(rec){
  var company=fieldText(rec,'公司');if(!company)return Promise.resolve();
  var exists=state.apps.some(function(a){return fieldText(a,'公司')===company});
  if(exists)return Promise.resolve();
  var p={'公司':{text:company},'岗位':{text:fieldText(rec,'岗位方向')||'校招岗位'},'当前阶段':{select:'已投递'},'投递日期':{date:today()},'节点说明':{text:'由今日处理一键标记自动生成'}};
  var u=urlVal(rec['投递链接']);if(u.link)p['相关链接']={url:{text:'网申入口',link:u.link}};
  return db.addRecord({databaseId:'oBGkMFTv9Xv4Xn5gFOK18S',properties:p}).catch(function(e){console.error('[database] 建档失败:'+((e&&e.message)||String(e)))});
}
function renderStats(){
  var w=0,done=0,ddl=0,live=0,t=today();
  state.jobs.forEach(function(j){var st=jobStatus(j);if(st==='待投递')w++;if(st==='已投递')done++;var dd=dOnly(j['截止日期']);if(st==='待投递'&&dd){var n=diffDays(t,dd);if(n>=0&&n<=7)ddl++}});
  state.apps.forEach(function(a){var st=appStage(a);if(st!=='Offer'&&st!=='感谢信'&&st!=='已投递'&&st!==DROP_STAGE)live++});
  setText('stWait',w);setText('stDone',done);setText('stDdl',ddl);setText('stLive',live);
  markBindable($('stWait'),JOBS_ID);markBindable($('stDone'),JOBS_ID);markBindable($('stDdl'),JOBS_ID);markBindable($('stLive'),APPS_ID);
}
function renderModuleCounts(){
  var aut=state.jobs.filter(function(j){return !isSOE(j)}).length;
  var soe=state.jobs.filter(function(j){return isSOE(j)}).length;
  setText('cntAutumn',aut);setText('cntSOE',soe);setText('cntIntern',state.interns.length);
  markBindable($('cntAutumn'),JOBS_ID);markBindable($('cntSOE'),JOBS_ID);markBindable($('cntIntern'),INTERN_ID);
}
function bindQuickIntel(){
  var inp=$('qiInput'),btn=$('qiBtn');if(!inp||!btn)return;
  function go(){var v=inp.value.replace(/^\s+|\s+$/g,'');if(v)showIntel(v)}
  btn.addEventListener('click',go);
  inp.addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();go()}});
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
    card.querySelector('[data-field="相关链接"]').addEventListener('click',function(e){e.preventDefault();var l=urlVal(a['相关链接']).link;if(l){openLink(l)}else{showIntel(fieldText(a,'公司'),nkId(a))}});
    var nd=dOnly(a['下次节点']);if(nd){var nEl=card.querySelectorAll('[data-field="下次节点"]')[0];var n=diffDays(today(),nd);if(n<0&&appStage(a)!=='Offer'&&appStage(a)!=='感谢信'){nEl.style.color='var(--red)';nEl.textContent=nd+'（已过期）'}}
    var sel=card.querySelector('.astage');sel.innerHTML='';
    var opt0=document.createElement('option');opt0.value='';opt0.textContent='改阶段';sel.appendChild(opt0);
    STAGES.concat([DROP_STAGE]).forEach(function(s){var o=document.createElement('option');o.value=optId('当前阶段',s);o.textContent=s;sel.appendChild(o)});
    sel.addEventListener('change',function(){if(!sel.value)return;sel.disabled=true;db.updateRecord({databaseId:'oBGkMFTv9Xv4Xn5gFOK18S',recordId:recId(a),properties:{'当前阶段':{select:sel.value}}}).then(reloadAll).catch(function(e){console.error('[database] 更新失败:'+((e&&e.message)||String(e)));sel.disabled=false})});
    card.querySelector('.anote').addEventListener('click',function(){var v=prompt('复盘笔记：',plain(a['复盘笔记']));if(v===null)return;db.updateRecord({databaseId:'oBGkMFTv9Xv4Xn5gFOK18S',recordId:recId(a),properties:{'复盘笔记':{text:v}}}).then(reloadAll).catch(function(e){console.error('[database] 更新失败:'+((e&&e.message)||String(e)))})});
    card.querySelector('.adel').addEventListener('click',function(){if(!confirm('确定删除「'+plain(a['公司'])+'」这条记录吗？'))return;db.deleteRecord({databaseId:'oBGkMFTv9Xv4Xn5gFOK18S',recordId:recId(a)}).then(reloadAll).catch(function(e){console.error('[database] 删除失败:'+((e&&e.message)||String(e)))})});
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
    db.addRecord({databaseId:'oBGkMFTv9Xv4Xn5gFOK18S',properties:p}).then(function(){form.reset();return reloadAll()}).catch(function(err){console.error('[database] 提交失败:'+((err&&err.message)||String(err)));alert('提交失败，请稍后重试')}).finally(function(){if(btn){btn.disabled=false;btn.textContent='保存记录'}});
  });
}

function init(){
  db=window.__SMART_PAGE__&&window.__SMART_PAGE__.database;
  bindIntelClose();
  bindExpress();
  if(!db){goOffline();return}
  setSync('ok');
  bindSubmitApp();
  bindFormCache('appForm');
  bindQuickIntel();
  $('lnkClose').addEventListener('click',function(){$('lnkModal').style.display='none'});
  $('lnkModal').addEventListener('click',function(e){if(e.target===$('lnkModal'))$('lnkModal').style.display='none'});
  $('todayMine').addEventListener('change',function(){state.todayMine=$('todayMine').checked;renderToday()});
  DB_READY=function(){return initSchema(function(){
    function fillStage(){
      var sel=$('fStage');if(!sel)return;sel.innerHTML='';var o0=document.createElement('option');o0.value='';o0.textContent='请选择';sel.appendChild(o0);
      (OPTS['当前阶段']||[]).forEach(function(o){var oo=document.createElement('option');oo.value=o.id;oo.textContent=o.text;sel.appendChild(oo)});
    }
    fillStage();
  })};
  DB_READY().catch(function(e){console.error('[database] 初始化失败:'+((e&&e.message)||String(e)));goOffline()});
}
function goOffline(){offline=true;setSync('off');$('offBanner').style.display='block';refreshAll()}
"""
    hero = hero_html("", "求职总览台", "今天的投递节奏、逾期提醒和全局统计都在这里", "overview")
    return _wrap_page("总览", body, nav, page_js, urls, active="overview", hero=hero)

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
    <div class="jacts"><a class="btn btn-ghost btn-sm" data-field="投递链接" target="_blank" rel="noopener">投递</a><button class="btn btn-search btn-sm jsearch">公司情报</button><button class="btn btn-sm jmark">标已投</button><select class="jstatus"></select><button class="btn btn-gray btn-sm jdel">删除</button></div>
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
    if(state.q){var q=state.q.toLowerCase();var hay=(plain(j['公司'])+' '+plain(j['岗位方向'])+' '+plain(j['备注'])).toLowerCase();if(hay.indexOf(q)<0)return false}
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
  var lnk=card.querySelector('[data-field="投递链接"]');lnk.addEventListener('click',function(e){e.preventDefault();var l=jobLink(j);if(l){openLink(l)}else{showIntel(fieldText(j,'公司'),nkId(j))}});
  card.querySelector('.jsearch').addEventListener('click',function(){showIntel(fieldText(j,'公司'),nkId(j))});
  card.querySelector('.jmark').addEventListener('click',function(){markApplied(j);});
  var jst=card.querySelector('.jstatus');jst.innerHTML='';
  (OPTS['投递状态']||[]).forEach(function(o){var op=document.createElement('option');op.value=o.text;op.textContent=o.text;jst.appendChild(op)});
  jst.value=st;
  jst.addEventListener('change',function(){
    if(!jst.value||jst.value===st){jst.value=st;return}
    jst.disabled=true;
    db.updateRecord({databaseId:'GgZ71tywhs4HEZytFSqXTP',recordId:recId(j),properties:{'投递状态':{select:jst.value}}}).then(function(){return jst.value==='已投递'?syncTracking(j):null}).then(reloadAll).catch(function(e){console.error('[database] 更新失败:'+((e&&e.message)||String(e)));jst.disabled=false});
  });
  card.querySelector('.jdel').addEventListener('click',function(){if(!confirm('确定删除「'+plain(j['公司'])+'」这条岗位吗？'))return;db.deleteRecord({databaseId:'GgZ71tywhs4HEZytFSqXTP',recordId:recId(j)}).then(reloadAll).catch(function(e){console.error('[database] 删除失败:'+((e&&e.message)||String(e)))})});
  return card;
}
function syncTracking(rec){
  var company=fieldText(rec,'公司');if(!company)return Promise.resolve();
  var exists=state.apps.some(function(a){return fieldText(a,'公司')===company});if(exists)return Promise.resolve();
  var p={'公司':{text:company},'岗位':{text:fieldText(rec,'岗位方向')||'校招岗位'},'当前阶段':{select:'已投递'},'投递日期':{date:today()},'节点说明':{text:'由岗位看板一键标记自动生成'}};
  var u=urlVal(rec['投递链接']);if(u.link)p['相关链接']={url:{text:'网申入口',link:u.link}};
  return db.addRecord({databaseId:'oBGkMFTv9Xv4Xn5gFOK18S',properties:p}).catch(function(e){console.error('[database] 投递跟踪写入失败:'+((e&&e.message)||String(e)))});
}
function markApplied(rec){
  db.updateRecord({databaseId:'GgZ71tywhs4HEZytFSqXTP',recordId:recId(rec),properties:{'投递状态':{select:'已投递'}}}).then(function(){return syncTracking(rec)}).then(reloadAll).catch(function(e){console.error('[database] 标已投失败:'+((e&&e.message)||String(e)));alert('更新失败，请刷新页面重试');});
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
    db.addRecord({databaseId:'GgZ71tywhs4HEZytFSqXTP',properties:p}).then(function(){form.reset();return reloadAll()}).catch(function(err){console.error('[database] 提交失败:'+((err&&err.message)||String(err)));alert('提交失败，请稍后重试')}).finally(function(){if(btn){btn.disabled=false;btn.textContent='保存岗位'}});
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
  bindIntelClose();
  bindExpress();
  if(!db){goOffline();return}
  setSync('ok');
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
  DB_READY=function(){return initSchema(function(){renderSelectOptions()})};
  DB_READY().catch(function(e){console.error('[database] 初始化失败:'+((e&&e.message)||String(e)));goOffline()});
}
function goOffline(){offline=true;setSync('off');$('offBanner').style.display='block';refreshAll()}
"""
    hero = hero_html("blue", "秋招岗位 · 其他企业", "互联网 / 科技 / 制造业，按城市·职业·批次快速筛选", "autumn")
    return _wrap_page("秋招岗位", body, nav, page_js, urls, active="autumn", hero=hero)

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
    <div class="jacts"><a class="btn btn-ghost btn-sm" data-field="投递链接" target="_blank" rel="noopener">投递</a><button class="btn btn-search btn-sm jsearch">公司情报</button><button class="btn btn-sm jmark">标已投</button><select class="jstatus"></select><button class="btn btn-gray btn-sm jdel">删除</button></div>
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
    if(state.q){var q=state.q.toLowerCase();var hay=(plain(j['公司'])+' '+plain(j['岗位方向'])+' '+plain(j['备注'])).toLowerCase();if(hay.indexOf(q)<0)return false}
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
  card.querySelector('[data-field="投递链接"]').addEventListener('click',function(e){e.preventDefault();var l=jobLink(j);if(l){openLink(l)}else{showIntel(fieldText(j,'公司'),nkId(j))}});
  card.querySelector('.jsearch').addEventListener('click',function(){showIntel(fieldText(j,'公司'),nkId(j))});
  card.querySelector('.jmark').addEventListener('click',function(){markApplied(j);});
  var jst=card.querySelector('.jstatus');jst.innerHTML='';
  (OPTS['投递状态']||[]).forEach(function(o){var op=document.createElement('option');op.value=o.text;op.textContent=o.text;jst.appendChild(op)});jst.value=st;
  jst.addEventListener('change',function(){if(!jst.value||jst.value===st){jst.value=st;return}jst.disabled=true;db.updateRecord({databaseId:'GgZ71tywhs4HEZytFSqXTP',recordId:recId(j),properties:{'投递状态':{select:jst.value}}}).then(function(){return jst.value==='已投递'?syncTracking(j):null}).then(reloadAll).catch(function(e){console.error('[database] 更新失败:'+((e&&e.message)||String(e)));jst.disabled=false})});
  card.querySelector('.jdel').addEventListener('click',function(){if(!confirm('确定删除「'+plain(j['公司'])+'」这条岗位吗？'))return;db.deleteRecord({databaseId:'GgZ71tywhs4HEZytFSqXTP',recordId:recId(j)}).then(reloadAll).catch(function(e){console.error('[database] 删除失败:'+((e&&e.message)||String(e)))})});
  return card;
}
function syncTracking(rec){var company=fieldText(rec,'公司');if(!company)return Promise.resolve();var exists=state.apps.some(function(a){return fieldText(a,'公司')===company});if(exists)return Promise.resolve();var p={'公司':{text:company},'岗位':{text:fieldText(rec,'岗位方向')||'校招岗位'},'当前阶段':{select:'已投递'},'投递日期':{date:today()},'节点说明':{text:'由岗位看板一键标记自动生成'}};var u=urlVal(rec['投递链接']);if(u.link)p['相关链接']={url:{text:'网申入口',link:u.link}};return db.addRecord({databaseId:'oBGkMFTv9Xv4Xn5gFOK18S',properties:p}).catch(function(e){console.error('[database] 操作失败:'+((e&&e.message)||String(e)))});}
function markApplied(rec){db.updateRecord({databaseId:'GgZ71tywhs4HEZytFSqXTP',recordId:recId(rec),properties:{'投递状态':{select:'已投递'}}}).then(function(){return syncTracking(rec)}).then(reloadAll).catch(function(e){console.error('[database] 标已投失败:'+((e&&e.message)||String(e)));alert('更新失败，请刷新页面重试');});}
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
    db.addRecord({databaseId:'GgZ71tywhs4HEZytFSqXTP',properties:p}).then(function(){form.reset();return reloadAll()}).catch(function(err){console.error('[database] 操作失败:'+((err&&err.message)||String(err)));alert('提交失败')}).finally(function(){if(btn){btn.disabled=false;btn.textContent='保存岗位'}});
  });
}
function fillSelect(selId,field,withAll){var sel=$(selId);if(!sel)return;sel.innerHTML='';if(withAll){var o0=document.createElement('option');o0.value='';o0.textContent=field==='投递状态'?'全部状态':'全部批次';sel.appendChild(o0)}(OPTS[field]||[]).forEach(function(o){var oo=document.createElement('option');oo.value=withAll?o.text:o.id;oo.textContent=o.text;sel.appendChild(oo)});}
function renderSelectOptions(){fillSelect('fBatch','批次',false);fillSelect('fPrio','优先级',false);fillSelect('fSt','投递状态',true);}
function init(){
  db=window.__SMART_PAGE__&&window.__SMART_PAGE__.database;
  bindIntelClose();
  bindExpress();
  if(!db){goOffline();return}
  setSync('ok');bindSubmitJob();
  bindFormCache('jobForm');
  $('lnkClose').addEventListener('click',function(){$('lnkModal').style.display='none'});
  $('lnkModal').addEventListener('click',function(e){if(e.target===$('lnkModal'))$('lnkModal').style.display='none'});
  $('q').addEventListener('input',function(){state.q=$('q').value.trim();renderJobs()});
  $('fSt').addEventListener('change',function(){state.fSt=$('fSt').value;renderJobs()});
  $('fCity').addEventListener('change',function(){state.fCity=$('fCity').value;renderJobs()});
  $('fCareer').addEventListener('change',function(){state.fCareer=$('fCareer').value;renderJobs()});
  DB_READY=function(){return initSchema(function(){renderSelectOptions()})};
  DB_READY().catch(function(e){console.error('[database] 初始化失败:'+((e&&e.message)||String(e)));goOffline()});
}
function goOffline(){offline=true;setSync('off');$('offBanner').style.display='block';refreshAll()}
"""
    hero = hero_html("red", "央国企专栏", "央企 · 银行 · 运营商 · 电网 · 烟草，稳定选择单独看", "soe")
    return _wrap_page("央国企", body, nav, page_js, urls, active="soe", hero=hero)

def page_intern(urls):
    nav = NAV_HTML.format(
        OVERVIEW_URL=urls["overview"], AUTUMN_URL=urls["autumn"], SOE_URL=urls["soe"], INTERN_URL=urls["intern"],
        OVERVIEW_ACTIVE='', AUTUMN_ACTIVE='', SOE_ACTIVE='', INTERN_ACTIVE='aria-current="page"',
    )
    EXPRESS = [
        ("字节跳动", "AI·大模型·后端·算法", "北京、成都", "https://jobs.bytedance.com/campus/position?keywords=&category=&location="),
        ("腾讯", "技术·算法·产品", "北京、成都", "https://careers.tencent.com/zh-CN/campusDiscover"),
        ("阿里巴巴", "技术·算法·数据", "北京、杭州", "https://talent.alibaba.com/campus/position-list"),
        ("百度", "AI·大模型·技术", "北京", "https://talent.baidu.com/jobs/campus-list"),
        ("美团", "算法·后端·数据", "北京", "https://zhaopin.meituan.com/web/campus"),
        ("京东", "技术·算法", "北京、成都", "https://zhaopin.jd.com"),
        ("网易", "技术·游戏·算法", "杭州、北京", "https://campus.163.com"),
        ("华为", "研发·AI·云计算", "成都、北京", "https://career.huawei.com/reccampportal/portal5/campus-recruitment.html"),
        ("小米", "技术·AIoT·算法", "北京", "https://hr.xiaomi.com/campus"),
        ("大疆", "嵌入式·算法·软件", "深圳、北京", "https://we.dji.com/zh-CN/campus"),
        ("科大讯飞", "AI·语音·大模型", "成都、合肥", "https://campus.iflytek.com"),
        ("商汤科技", "CV·大模型·算法", "北京、上海", "https://www.sensetime.com/cn/careers"),
        ("OPPO", "软件·算法", "成都、深圳", "https://campus.oppo.com"),
        ("NVIDIA 英伟达", "GPU·AI·深度学习", "北京、上海", "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite"),
        ("微软", "研发·AI·云", "北京", "https://careers.microsoft.com/v2/global/en/home.html"),
    ]
    xcards = "".join([
        '<div class="xcard"><div class="xhead"><b>' + n + '</b><span class="tag">' + c + '</span></div>'
        '<div class="jmeta">重点城市：' + ct + ' ｜ 进入官网后筛选「实习生 / 日常实习」+ 城市</div>'
        '<div class="jacts"><button class="btn btn-go btn-sm xgo" data-u="' + u + '">直达实习官网</button>'
        '<button class="btn btn-search btn-sm xintel" data-c="' + n + '">公司情报</button></div></div>'
        for n, c, ct, u in EXPRESS
    ])
    body = """<section>
  <h2 style="color:var(--orange)"><svg viewBox="0 0 24 24" fill="none" stroke="#e58f0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/></svg>日常实习直通车 · 27届官方通道<span class="cnt">15 家</span></h2>
  <div class="jmeta" style="margin-bottom:10px">BOSS / 实习僧反爬无法自动抓取，日常实习最靠谱的入口是<b>各家官方实习招聘页</b>：点「直达实习官网」→ 页面内筛选「实习生 / 日常实习」+ 目标城市，一步到位。想了解公司先点「公司情报」看面经和评价。</div>
  <div class="xgrid">""" + xcards + """</div>
</section>

<section>
  <h2 style="color:var(--orange)"><svg viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>实习批次同步 · 专栏<span class="cnt" id="jobCnt" data-sp-bindable="database" data-sp-database-id="tgH8096uENTaIj8RSY9qm5"></span></h2>
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
      <label class="fl">投递链接（官方投递页链接）</label><input name="ilnk" type="url" placeholder="https://">
      <label class="fl">网申开始 / 截止日期（可留空）</label>
      <div style="display:flex;gap:8px"><input name="open" type="date" style="flex:1"><input name="deadline" type="date" style="flex:1"></div>
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
    <div class="jmeta dline">网申：<span data-field="网申开始"></span> ~ <span data-field="截止日期"></span></div>
    <div class="jnote" data-field="备注"></div>
    <div class="jmeta">来源：<span data-field="来源"></span></div>
    <div class="jacts"><a class="btn btn-ghost btn-sm" data-field="投递链接" target="_blank" rel="noopener">投递</a><button class="btn btn-search btn-sm jsearch">公司情报</button><select class="jstatus"></select><button class="btn btn-gray btn-sm jdel">删除</button></div>
  </div>
</div>
"""
    body += tpl
    page_js = r"""
function filteredInterns(){
  return state.interns.filter(function(i){
    var st=jobStatus(i);if(state.fSt&&st!==state.fSt)return false;
    if(state.q){var q=state.q.toLowerCase();var hay=(plain(i['公司'])+' '+plain(i['岗位名称'])+' '+plain(i['备注'])).toLowerCase();if(hay.indexOf(q)<0)return false}
    return true;
  }).sort(function(a,b){var c=plain(a['公司']);var cc=plain(b['公司']);return c<cc?-1:1});
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
  // 网申起止来自牛客同步；两条都为空时整行隐藏，避免出现「网申： ~ 」这种空壳
  var dl=plain(i['截止日期'])||plain(i['网申开始']);
  setFieldText(card,'网申开始',plain(i['网申开始'])||'—',INTERN_ID);setFieldText(card,'截止日期',plain(i['截止日期'])||'—',INTERN_ID);
  var dlRow=card.querySelector('.dline');if(dlRow&&!dl)dlRow.style.display='none';
  var stEl=card.querySelector('[data-field="投递状态"]');if(st==='已投递')stEl.className='tag ok';else if(st==='不投了')stEl.className='tag gray';
  card.querySelector('[data-field="投递链接"]').addEventListener('click',function(e){e.preventDefault();var l=urlVal(i['投递链接']).link;if(l){openLink(l)}else{showIntel(fieldText(i,'公司'),nkId(i))}});
  card.querySelector('.jsearch').addEventListener('click',function(){showIntel(fieldText(i,'公司'),nkId(i))});
  var jst=card.querySelector('.jstatus');jst.innerHTML='';
  (OPTS['投递状态']||[]).forEach(function(o){var op=document.createElement('option');op.value=o.text;op.textContent=o.text;jst.appendChild(op)});jst.value=st;
  jst.addEventListener('change',function(){if(!jst.value||jst.value===st){jst.value=st;return}jst.disabled=true;db.updateRecord({databaseId:'tgH8096uENTaIj8RSY9qm5',recordId:recId(i),properties:{'投递状态':{select:jst.value}}}).then(reloadAll).catch(function(e){console.error('[database] 更新失败:'+((e&&e.message)||String(e)));jst.disabled=false})});
  card.querySelector('.jdel').addEventListener('click',function(){if(!confirm('确定删除「'+plain(i['公司'])+'」这条实习岗位吗？'))return;db.deleteRecord({databaseId:'tgH8096uENTaIj8RSY9qm5',recordId:recId(i)}).then(reloadAll).catch(function(e){console.error('[database] 删除失败:'+((e&&e.message)||String(e)))})});
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
    var od=form.querySelector('[name="open"]').value;if(od)p['网申开始']={date:od};
    var dd=form.querySelector('[name="deadline"]').value;if(dd)p['截止日期']={date:dd};
    var n=form.querySelector('[name="inote"]').value.trim();if(n)p['备注']={text:n};
    db.addRecord({databaseId:'tgH8096uENTaIj8RSY9qm5',properties:p}).then(function(){form.reset();return reloadAll()}).catch(function(err){console.error('[database] 操作失败:'+((err&&err.message)||String(err)));alert('提交失败')}).finally(function(){if(btn){btn.disabled=false;btn.textContent='保存实习岗位'}});
  });
}
function fillSelect(selId,field,withAll){var sel=$(selId);if(!sel)return;sel.innerHTML='';if(withAll){var o0=document.createElement('option');o0.value='';o0.textContent='全部状态';sel.appendChild(o0)}(OPTS[field]||[]).forEach(function(o){var oo=document.createElement('option');oo.value=withAll?o.text:o.id;oo.textContent=o.text;sel.appendChild(oo)});}
function renderSelectOptions(){fillSelect('fSt','投递状态',true);}
function init(){
  db=window.__SMART_PAGE__&&window.__SMART_PAGE__.database;
  bindIntelClose();
  bindExpress();
  if(!db){goOffline();return}
  setSync('ok');bindSubmitIntern();
  bindFormCache('internForm');
  $('lnkClose').addEventListener('click',function(){$('lnkModal').style.display='none'});
  $('lnkModal').addEventListener('click',function(e){if(e.target===$('lnkModal'))$('lnkModal').style.display='none'});
  $('q').addEventListener('input',function(){state.q=$('q').value.trim();renderInterns()});
  $('fSt').addEventListener('change',function(){state.fSt=$('fSt').value;renderInterns()});
  DB_READY=function(){return initSchema(function(){renderSelectOptions()})};
  DB_READY().catch(function(e){console.error('[database] 初始化失败:'+((e&&e.message)||String(e)));goOffline()});
}
function goOffline(){offline=true;setSync('off');$('offBanner').style.display='block';refreshAll()}
"""
    hero = hero_html("amber", "日常实习直通车", "15 家官方实习通道一键直达，牛客实习批次每日自动同步，秋招批次绝不混入", "intern")
    return _wrap_page("成都实习", body, nav, page_js, urls, active="intern", hero=hero)

def _wrap_page(title, body, nav, page_js, urls, active, hero=''):
    # JS fetches all 3 tables + reloadAll is shared
    # pageSize 取 SDK 上限 200（默认 50），600+ 条的岗位表从 7 次请求降到 4 次；
    # 每轮都校验 hasMore/nextCursor/空页/游标不前进，任一异常立即停，避免死循环。
    fetch_jobs = "function fetchJobs(){var out=[],cur=null;function once(){return db.query({databaseId:'GgZ71tywhs4HEZytFSqXTP',pageSize:200,startCursor:cur||undefined}).then(function(res){var rs=res.results||[],nx=res.nextCursor;out=out.concat(rs);if(!res.hasMore||!nx||!rs.length||nx===cur||out.length>=5000)return out;cur=nx;return once()})}return once()}\n"
    fetch_apps = "function fetchApps(){var out=[],cur=null;function once(){return db.query({databaseId:'oBGkMFTv9Xv4Xn5gFOK18S',pageSize:200,startCursor:cur||undefined}).then(function(res){var rs=res.results||[],nx=res.nextCursor;out=out.concat(rs);if(!res.hasMore||!nx||!rs.length||nx===cur||out.length>=3000)return out;cur=nx;return once()})}return once()}\n"
    fetch_ints = "function fetchInterns(){var out=[],cur=null;function once(){return db.query({databaseId:'tgH8096uENTaIj8RSY9qm5',pageSize:200,startCursor:cur||undefined}).then(function(res){var rs=res.results||[],nx=res.nextCursor;out=out.concat(rs);if(!res.hasMore||!nx||!rs.length||nx===cur||out.length>=3000)return out;cur=nx;return once()})}return once()}\n"
    load = ("var _loadP=null,_loadRetry=0,_lastLoadAt=0,_syncFailed=false;\n"
            "function loadOnce(){return Promise.all([fetchJobs(),fetchApps(),fetchInterns()]).then(function(r){"
            "state.jobs=r[0];state.apps=r[1];state.interns=r[2];_clsCache={};_lastLoadAt=Date.now();setSync('ok')})}\n"
            "/* 并发去重：连点/多模块同时刷新只发一轮请求；失败自动重试 1 次（间隔 1.5s）。 */\n"
            "function loadData(){if(offline)return Promise.resolve();if(_loadP)return _loadP;"
            "_loadP=loadOnce().then(function(r){_loadP=null;_loadRetry=0;_syncFailed=false;return r},function(e){"
            "_loadP=null;console.error('[database] 数据加载失败:'+((e&&e.message)||String(e)));"
            "if(_loadRetry<1){_loadRetry++;return new Promise(function(ok){setTimeout(ok,1500)}).then(loadData)}"
            "_loadRetry=0;_syncFailed=true;setSync('warn');return Promise.reject(e)});return _loadP}\n"
            "function reloadAll(){return loadData().then(function(){refreshAll()},function(){refreshAll()});}\n")
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
{hero}
<div class="wrap">
<div class="banner" id="offBanner">离线模式：未连接到在线数据表，数据读写暂不可用。请通过资料库链接打开本页面。<button type="button" class="btn btn-sm" id="offRetry" style="margin-left:10px;cursor:pointer">重试连接</button></div>
{body}
</div>
{LNKMODAL_HTML}
{INTELMODAL_HTML}
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
    "overview": ["公司","批次","岗位方向","工作地点","优先级","投递状态","网申开始","截止日期","投递链接","来源","备注","牛客ID",
                 "岗位","当前阶段","投递日期","下次节点","节点说明","复盘笔记","相关链接"],
    "autumn":   ["公司","批次","岗位方向","工作地点","优先级","投递状态","网申开始","截止日期","投递链接","来源","备注","牛客ID"],
    "soe":      ["公司","批次","岗位方向","工作地点","优先级","投递状态","网申开始","截止日期","投递链接","来源","备注","牛客ID"],
    "intern":   ["公司","岗位名称","薪资","工作地点","岗位要求","投递状态","网申开始","截止日期","投递链接","来源","备注","牛客ID"],
}

# 每页与 canonical 不同的真实选择器：canonical_schema.json 是以合并版单文件为准写的，
# 独立页的表单名/展示位跟它并不一致（例如实习表单用 ilnk/inote、央国企卡片用 .jstatus 而不是
# data-field="投递状态"）。这里按页覆盖，保证 lint_schema 的 R10「选择器必须真实存在」成立。
FIELD_MAPPING_OVERRIDE = {
    "intern": {
        "投递链接": {"form_input": '[name="ilnk"]'},
        "备注": {"form_input": '[name="inote"]'},
    },
    "soe": {
        "投递状态": {"display_selector": ".jstatus"},
    },
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
    # also write to workspace root for import
    (workspace/p_over['filename']).write_text(p_over['content'], encoding='utf-8')
    (workspace/p_aut['filename']).write_text(p_aut['content'], encoding='utf-8')
    (workspace/p_soe['filename']).write_text(p_soe['content'], encoding='utf-8')
    (workspace/p_int['filename']).write_text(p_int['content'], encoding='utf-8')
    # write per-page schema files
    for name, fields in SCHEMAS.items():
        # options_map / field_mapping 同步收窄到该页实际用到的字段，否则 lint R7
        # 会报「options_map 中存在但 properties 不存在」
        fm = {k: dict(v) for k, v in full.get("field_mapping", {}).items() if k in fields}
        for fk, patch in FIELD_MAPPING_OVERRIDE.get(name, {}).items():
            if fk in fm:
                fm[fk].update(patch)
        sub = {"title": full.get("title"), "page_type": full.get("page_type"),
               "properties": {k: v for k, v in full["properties"].items() if k in fields},
               "field_mapping": fm,
               "options_map": {k: v for k, v in full.get("options_map", {}).items()
                               if k in fields and k in full["properties"]}}
        (here/f"canonical_{name}.json").write_text(json.dumps(sub, ensure_ascii=False), encoding='utf-8')
    for f in [p_over, p_aut, p_soe, p_int]:
        print(f"wrote {f['filename']}, {len(f['content'])} bytes")

def _wrap_marker(filename, content):
    return {"filename": filename, "content": content}


if __name__ == "__main__":
    main()
