# 部署到腾讯文档·资料库

这个工作台是为 [腾讯文档·资料库](https://www.workbuddy.cn) 设计的——它的「在线 page」+「数据表」能力，可以让单个 HTML 在沙箱里跑、并直接读写云端数据。

## 步骤

### 1. 创建 3 张数据表

在资料库里建 3 张空表（用任何字段类型都行，新建时全空也行）：

| 表名 | 用途 |
|------|------|
| `qiuzhao_jobs` | 秋招岗位清单 |
| `qiuzhao_apps` | 简历投递跟踪 |
| `qiuzhao_interns` | 成都实习岗位 |

每张表建好后，把页面里 `JOBS_ID / APPS_ID / INTERN_ID` 常量改成你的真实表 ID。

### 2. 上传页面

每个 HTML 单独上传为一个资料库节点。建议层级：

```
资料库
└── 秋招求职台
    ├── 00-总览台.html         (id: szZlSjyPnnpGwDW4OD4y0X)
    ├── 01-秋招岗位台.html     (id: G9pPkUVWIc6Fk43Mnn1csc)
    ├── 02-央国企台.html       (id: PQ5cLpifIyB1CaQB2OIMrm)
    └── 03-成都实习台.html     (id: JgXPaIiaDMGt2xH3vBftAo)
```

### 3. 绑定数据表到页面

上传时，每个页面都要勾选「关联数据表」并选上对应的 3 张表（这样页面内的 `db.query/getSchema/addRecord/updateRecord/deleteRecord` 才能工作）。

### 4. 跨页跳转

页面之间的导航用 `<a target="_top">` 直接跳，因为 iframe 内不能用常规 `window.open`。

```html
<a class="tab" target="_top" href="https://www.workbuddy.cn/space/d/...">秋招岗位</a>
```

### 5. 设置每天自动同步

在 WorkBuddy 里创建一个「automation」每天 9:00 触发：
- 工具：`ToolSearch` → `connect_open_platform`
- 抓牛客校招日程（无需登录）：
  ```
  POST https://www.nowcoder.com/np-api/u/school-schedule/list-card
  body: query=&propertyId=&page=1&pageSize=20&tab=3
  ```
- 筛选还在有效期 + batchName 含「秋招」/「实习」
- 去重后写入 `qiuzhao_jobs`
- 同样规则在 9:30 触发一次，但写入 `qiuzhao_interns`（成都公司）

## 已知坑

- **沙箱内 `window.open` 被拦截**：所有跳外链的操作都用了兜底弹层（`openLink` 函数）保证可访问
- **服务端返回的链接格式是数组 `[{text,link}]`，不是契约里写的对象**：`urlVal()` 函数已经兼容
- **记录主键叫 `record_id`，不是 `_id`**：`recId()` 函数已经兼容
- **BOSS 直聘有反爬**：实习生数据靠用户手动从 BOSS 复制链接 + 一键收录
