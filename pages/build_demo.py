#!/usr/bin/env python3
"""Build demo versions of the 4 pages that work on GitHub Pages / any static server.

Inserts a localStorage-backed mock for the WorkBuddy SDK so the same HTML logic runs
without the parent iframe.
"""
import re, json, os
from pathlib import Path

HERE = Path(__file__).parent
WORKSPACE = HERE.parent

# Adapter injected at the very start of the inline <script>:
# wraps window.__SMART_PAGE__ so the page works on plain hosting (GitHub Pages etc.).
MOCK_ADAPTER = r"""
/* === DEMO MODE ADAPTER (GitHub Pages / 离线 localStorage) ============ */
(function(){
  function hasSDK(){return !!(window.__SMART_PAGE__&&window.__SMART_PAGE__.database);}
  function loadLS(name){
    try { return JSON.parse(localStorage.getItem('qiuzhao_demo_'+name)||'[]'); } catch(e){ return []; }
  }
  function saveLS(name,rows){
    try { localStorage.setItem('qiuzhao_demo_'+name, JSON.stringify(rows)); } catch(e){}
  }
  function loadSchema(){return JSON.parse(localStorage.getItem('qiuzhao_demo_schema')||'null')||{
    'jobs':{name:'jobs',dbid:'JOBS_ID_FAKE',options:{},order:0},
    'apps':{name:'apps',dbid:'APPS_ID_FAKE',options:{},order:1},
    'interns':{name:'interns',dbid:'INTERN_ID_FAKE',options:{},order:2}
  };}
  function dbidOf(name){return loadSchema()[name].dbid;}
  function fakeDb(names){
    // databaseId -> 本地表名 的映射；所有方法按 opts.databaseId 分派，
    // 避免三个表共用同一个闭包变量导致互相覆盖（旧版 bug：三张表都返回 interns）。
    var map={};
    names.forEach(function(n){map[dbidOf(n)]=n;});
    function nameOf(opts){
      var id=(opts&&opts.databaseId)||'';
      return Object.prototype.hasOwnProperty.call(map,id)?map[id]:names[0];
    }
    function nextId(){return 'rec_'+Date.now()+'_'+Math.floor(Math.random()*1e6);}
    return {
      query:function(opts){
        var n=nameOf(opts);
        return Promise.resolve({results:loadLS(n),hasMore:false,nextCursor:null});
      },
      addRecord:function(opts){
        var n=nameOf(opts),rows=loadLS(n),id=nextId();
        var rec={_id:id,record_id:id,id:id};
        Object.keys(opts.properties||{}).forEach(function(k){rec[k]=opts.properties[k];});
        rows.push(rec);saveLS(n,rows);
        return Promise.resolve({_id:id,record_id:id});
      },
      updateRecord:function(opts){
        var n=nameOf(opts),rows=loadLS(n);
        var i=rows.findIndex(function(r){return (r._id||r.record_id)===opts.recordId;});
        if(i>=0){Object.keys(opts.properties||{}).forEach(function(k){rows[i][k]=opts.properties[k];});saveLS(n,rows);}
        return Promise.resolve({ok:true});
      },
      deleteRecord:function(opts){
        var n=nameOf(opts);
        saveLS(n,loadLS(n).filter(function(r){return (r._id||r.record_id)!==opts.recordId;}));
        return Promise.resolve({ok:true});
      },
      // 返回真实的 select 字段，让页面里的下拉框/选项映射（OPTS）在 demo 下也能正常填充
      getSchema:function(opts){
        var s=loadSchema()[nameOf(opts)]||{};
        var props=[];
        Object.keys(s.options||{}).forEach(function(k){
          props.push({name:k,type:'select',config:{options:s.options[k]||[]}});
        });
        return Promise.resolve({properties:props});
      }
    };
  }
  if(!hasSDK()){
    // Demo banner：用普通文档流（不是 fixed），避免盖住顶部 sticky 导航
    document.addEventListener('DOMContentLoaded',function(){
      var b=document.createElement('div');
      b.style.cssText='position:relative;z-index:99;background:#fef3c7;color:#92400e;text-align:center;padding:8px 12px;font-size:13px;border-bottom:1px solid #fbbf24;line-height:1.5';
      b.innerHTML='GitHub Pages 演示模式：数据只存在当前浏览器的 localStorage，不会同步到资料库。<a href="javascript:void(0)" id="demoWipe" style="color:#b45309;text-decoration:underline">清空演示数据</a>';
      document.body.insertBefore(b,document.body.firstChild);
      document.getElementById('demoWipe').onclick=function(){
        if(confirm('清空演示数据？会恢复初始示例岗位。')){localStorage.clear();location.reload();}
      };
    });
    // Mock SDK: only query that returns localStorage; write operations update localStorage.
    window.__SMART_PAGE__={database:fakeDb(['jobs','apps','interns'])};
    // Pre-fill demo data on first visit
    if(!localStorage.getItem('qiuzhao_demo_seeded_v1')){
      // 演示数据用「相对今天」的日期生成，保证任何时候打开 demo 都有逾期/临期/正常三类样本
      function d(off){var t=new Date();t.setDate(t.getDate()+off);function p(n){return (n<10?'0':'')+n}return t.getFullYear()+'-'+p(t.getMonth()+1)+'-'+p(t.getDate());}
      var demoJobs=[
        {公司:{text:'字节跳动'},批次:{text:'27秋招'},岗位方向:{text:'大模型算法、推荐算法'},工作地点:{text:'北京、上海'},优先级:{text:'P0'},投递状态:{text:'待投递'},网申开始:{date:d(-12)},截止日期:{date:d(3)},投递链接:{url:{text:'官网',link:'https://jobs.bytedance.com'}},来源:{text:'牛客校招日程'},备注:{text:'示例数据，演示用'}},
        {公司:{text:'中国电信'},批次:{text:'27秋招'},岗位方向:{text:'云计算、AI'},工作地点:{text:'北京'},优先级:{text:'P1'},投递状态:{text:'待投递'},截止日期:{date:d(20)},投递链接:{url:{text:'网申',link:'https://zhaopin.chinatelecom.com.cn'}},来源:{text:'牛客校招日程'},备注:{text:'央国企示例'}},
        {公司:{text:'中国移动'},批次:{text:'27秋招'},岗位方向:{text:'人工智能、数据'},工作地点:{text:'成都'},优先级:{text:'P1'},投递状态:{text:'待投递'},截止日期:{date:d(30)},投递链接:{url:{text:'网申',link:'https://job.10086.cn'}},来源:{text:'牛客校招日程'},备注:{text:'央国企示例'}},
        {公司:{text:'腾讯'},批次:{text:'27暑期实习'},岗位方向:{text:'机器学习'},工作地点:{text:'深圳、北京'},优先级:{text:'P0'},投递状态:{text:'待投递'},截止日期:{date:d(-2)},投递链接:{url:{text:'官网',link:'https://careers.tencent.com'}},来源:{text:'牛客校招日程'},备注:{text:'已过期示例（今天要处理里的红色项）'}},
        {公司:{text:'美团'},批次:{text:'27秋招'},岗位方向:{text:'后端、算法'},工作地点:{text:'北京'},优先级:{text:'P2'},投递状态:{text:'待投递'},截止日期:{date:d(12)},投递链接:{url:{text:'官网',link:'https://zhaopin.meituan.com'}},来源:{text:'牛客校招日程'},备注:{text:'互联网示例'}},
        {公司:{text:'商汤科技'},批次:{text:'27秋招'},岗位方向:{text:'AGI算法、视觉算法'},工作地点:{text:'北京、上海'},优先级:{text:'P1'},投递状态:{text:'待投递'},截止日期:{date:d(8)},投递链接:{url:{text:'官网',link:'https://www.sensetime.com/cn/careers'}},来源:{text:'牛客校招日程'},备注:{text:'互联网示例'}}
      ];
      var demoApps=[{公司:{text:'字节跳动'},岗位:{text:'大模型算法实习生'},当前阶段:{text:'一面'},投递日期:{date:d(-5)},下次节点:{date:d(2)},节点说明:{text:'技术一面'},复盘笔记:{text:'演示数据'},相关链接:{url:{text:'官网',link:'https://jobs.bytedance.com'}}}];
      var demoInterns=[{公司:{text:'腾讯成都'},岗位名称:{text:'技术类实习'},薪资:{text:'200-300元/天'},工作地点:{text:'成都'},岗位要求:{text:'实习'},投递状态:{text:'待投递'},投递链接:{url:{text:'投递',link:'https://careers.tencent.com'}},来源:{text:'演示数据'},备注:{text:'演示'}}];
      saveLS('jobs',demoJobs.map(function(r){var id='seed_'+Math.random().toString(36).slice(2,10);r._id=id;r.record_id=id;r.id=id;return r;}));
      saveLS('apps',demoApps.map(function(r){var id='seed_'+Math.random().toString(36).slice(2,10);r._id=id;r.record_id=id;r.id=id;return r;}));
      saveLS('interns',demoInterns.map(function(r){var id='seed_'+Math.random().toString(36).slice(2,10);r._id=id;r.record_id=id;r.id=id;return r;}));
      // Pre-fill schema options for selects to work
      var schema={
        jobs:{name:'jobs',dbid:'JOBS_ID_FAKE',options:{'批次':[{text:'27秋招',id:'b_qz'},{text:'27暑期实习',id:'b_sq'},{text:'27日常实习',id:'b_rc'}],'优先级':[{text:'P0',id:'p0'},{text:'P1',id:'p1'},{text:'P2',id:'p2'}],'投递状态':[{text:'待投递',id:'s_w'},{text:'已投递',id:'s_d'},{text:'不投了',id:'s_n'}]}},
        apps:{name:'apps',dbid:'APPS_ID_FAKE',options:{'当前阶段':[{text:'已投递',id:'ph_yd'},{text:'笔试',id:'ph_bs'},{text:'一面',id:'ph_ym'},{text:'二面',id:'ph_em'},{text:'HR面',id:'ph_hr'},{text:'Offer',id:'ph_of'},{text:'感谢信',id:'ph_th'}]}},
        interns:{name:'interns',dbid:'INTERN_ID_FAKE',options:{'投递状态':[{text:'待投递',id:'i_w'},{text:'已投递',id:'i_d'},{text:'不投了',id:'i_n'}]}}
      };
      localStorage.setItem('qiuzhao_demo_schema',JSON.stringify(schema));
      localStorage.setItem('qiuzhao_demo_seeded_v1','1');
    }
  }
})();
/* === END DEMO MODE ADAPTER ============================================= */

"""


# 生产环境（资料库）节点 URL -> demo 站内的相对页面
DEMO_LINK_MAP = {
    "https://www.workbuddy.cn/space/d/szZlSjyPnnpGwDW4OD4y0X": "index.html",
    "https://www.workbuddy.cn/space/d/G9pPkUVWIc6Fk43Mnn1csc": "autumn.html",
    "https://www.workbuddy.cn/space/d/PQ5cLpifIyB1CaQB2OIMrm": "soe.html",
    "https://www.workbuddy.cn/space/d/JgXPaIiaDMGt2xH3vBftAo": "intern.html",
}


def patch(src):
    """Inject demo adapter into the inline script and adapt IDs."""
    s = open(src, encoding='utf-8').read()
    # Replace constants with FAKE ids (will only be used in demo mode)
    s = s.replace("var JOBS_ID='GgZ71tywhs4HEZytFSqXTP'", "var JOBS_ID='JOBS_ID_FAKE'")
    s = s.replace("var APPS_ID='oBGkMFTv9Xv4Xn5gFOK18S'",  "var APPS_ID='APPS_ID_FAKE'")
    s = s.replace("var INTERN_ID='tgH8096uENTaIj8RSY9qm5'","var INTERN_ID='INTERN_ID_FAKE'")
    s = s.replace("'GgZ71tywhs4HEZytFSqXTP'", "'JOBS_ID_FAKE'")
    s = s.replace("'oBGkMFTv9Xv4Xn5gFOK18S'", "'APPS_ID_FAKE'")
    s = s.replace("'tgH8096uENTaIj8RSY9qm5'", "'INTERN_ID_FAKE'")
    # demo 站是纯静态站：站内导航必须指向 demo 自己的页面，否则一点就跳回生产环境
    for prod_url, local in DEMO_LINK_MAP.items():
        s = s.replace('target="_top" href="%s"' % prod_url, 'href="%s"' % local)
        s = s.replace('href="%s"' % prod_url, 'href="%s"' % local)
    # Inject adapter at the very start of inline script
    script_re = re.compile(r'<script>(.*?)</script>', re.S)
    m = script_re.search(s)
    if m:
        original = m.group(1)
        # Adapter goes before the IIFE
        injected = MOCK_ADAPTER + original
        s = s[:m.start()] + '<script>' + injected + '</script>' + s[m.end():]
    return s


def main():
    here = Path(__file__).parent
    demo_dir = here.parent / 'demo'
    demo_dir.mkdir(exist_ok=True)
    mappings = [
        ('00-总览台.html', 'index.html'),
        ('01-秋招岗位台.html', 'autumn.html'),
        ('02-央国企台.html', 'soe.html'),
        ('03-成都实习台.html', 'intern.html'),
    ]
    for src_name, dst_name in mappings:
        src_path = here / src_name
        dst_path = demo_dir / dst_name
        content = patch(src_path)
        dst_path.write_text(content, encoding='utf-8')
        print(f'wrote demo/{dst_name}, {len(content)} bytes')

if __name__ == '__main__':
    main()
