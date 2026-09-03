# 群聊日常分析 · 报告模板示例仓库（Sky Diary 天空日记）

本仓库是 [astrbot_plugin_qq_group_daily_analysis](https://github.com/SXP-Simon/astrbot_plugin_qq_group_daily_analysis)
的 **报告视觉模板示例仓库**，可以作为你自己的模板仓库的起点。

内置模板：**`gda_sky_diary`（天空日记 Sky Diary）** —— 蓝白渐变现代简约风。

> 预览：
> ![天空日记预览图](assets/gda_sky_diary-demo-thumb.jpg)
>
> 完整长图见 [assets/gda_sky_diary-demo.jpg](assets/gda_sky_diary-demo.jpg)。

> 📌 **图片文件说明**（三张图用途不同，别混淆）：
> - `assets/gda_sky_diary-demo-thumb.jpg` —— **本 README 展示用的缩略图**（宽 420，仅约 47KB），
>   用于仓库首页快速预览效果；不参与模板运行，也不打包进 zip 之外的任何插件逻辑。
> - `assets/gda_sky_diary-demo.jpg` —— **完整长图**（750×2311），README 以链接附上，供点开看全部细节。
> - `gda_sky_diary/preview.jpg` —— **随模板打包的预览图**：用户安装本模板后，
>   QQ `/查看模板` 与 WebUI 画廊显示的就是这张图（区别于上面两张仅作仓库展示）。
>
> 三者均由 `generate_preview.py` 一次生成。

## 一键安装（推荐）

在插件 Web 控制台 → 配置页 → 模板选择器旁「安装模板」→ GitHub 链接页签：

```
https://github.com/<你的用户名>/daily-analysis-report-theme
```

插件会自动下载源码、识别 `gda_sky_diary/` 模板目录并安装，**无需重启机器人**。
也可以在本仓库页面点 `Code ▾ → Download ZIP`，然后在「安装模板 → 上传 zip」直接上传。

> 安装成功后模板会出现在「断点续跑」「免 Token 切换主题重绘」下拉中；
> 卸载请用同一入口旁的「卸载模板」（内置模板不可卸载）。

## 目录结构

```
daily-analysis-report-theme/
├── README.md                # 本说明
└── gda_sky_diary/           # 模板根目录（zip 打包时打包这一层）
    ├── image_template.html  # 长图海报主骨架
    ├── html_template.html   # 独立网页主骨架
    ├── topic_item.html      # 话题列表模块
    ├── user_title_item.html # 群友称号与画像模块
    ├── quote_item.html      # 金句与锐评模块
    ├── activity_chart.html  # 24h 活跃轨迹模块
    ├── chat_quality_item.html # 群聊质量锐评模块
    └── template.json        # 模板显示名 {"name": "天空日记 (Sky Diary)"}
```

## 快速自定义

所有视觉都由 `gda_sky_diary/image_template.html` 头部 `:root { ... }` 的 CSS 变量控制：

```css
:root {
    --sky-top: #e3f4fd;      /* 页面顶部渐变 */
    --sky-bottom: #ffffff;   /* 页面底部渐变 */
    --accent: #4a9fd8;       /* 主色（进度条/装饰） */
    --accent-deep: #2b6d9e;  /* 深主色（标题/数字） */
    --warn: #f6a940;         /* 强调色（锐评标签） */
    --ink: #1f3a52;          /* 正文色 */
    --ink-soft: #5c7a93;     /* 次要文字 */
    --line: #d7e9f5;         /* 分隔线 */
    --radius: 14px;          /* 卡片圆角 */
}
```

改完颜色即可得到自己的风格；改版式请直接修改对应 HTML 文件。

## 打包规范速查（安装器强制校验）

| 项 | 要求 |
| --- | --- |
| 单一模板 | 一个 zip 只含一个模板，多个模板目录会被拒绝 |
| 主文件 | 目录内必须有 `image_template.html` 或 `html_template.html` |
| 根目录 | 允许外层套一层目录（`repo-main` 形式自动剥离） |
| 大小 | 解压后 ≤ 64MB、单文件 ≤ 20MB、成员 ≤ 300 |
| 命名 | 建议小写英文蛇形（如 `gda_xxx`）、≤ 50 字符、无空格与特殊字符；与内置模板重名会被拒绝 |
| 显示名 | 可选 `template.json`：`{"name": "中文名", "desc": "说明", "tag": "水蓝色", "tag_color": "blue"}`（desc 显示在 WebUI 下拉/卸载弹窗，tag/tag_color 为下拉中的风格标签） |
| 预览图 | 可选 `preview.jpg/png` 或 `demo.jpg/png` 放在模板目录内：随 zip 一起打包安装后，QQ `/查看模板` 即可显示该预览图 |
| 模板内引用图片 | 只能用**绝对 URL（公开图库链接）**或**内联 data URI / `<svg>`**——报告 HTML 是字符串交给远端 T2I 渲染服务，**相对路径（如 `assets/bg.png`）渲染时必然 404**；预览图（preview.jpg）除外。小图标建议 base64/内联 SVG，大装饰图建议放本仓库 `assets/<模板名>/` 后用 jsDelivr 绝对链接（参考内置 HatsuneMiku 模板的做法） |
| 多余的脚本/文件 | 模板目录内可放置任意文件（安装器原样保留、运行时会忽略），但脚本类文件请留在仓库根，避免徒增 zip 体积 |

## 渲染变量契约

主骨架接收 `topics_html / titles_html / quotes_html / hourly_chart_html /
chat_quality_html` 五个 HTML 片段，以及 `message_count / participant_count /
total_characters / emoji_count / most_active_period / current_date / total_tokens`
等统计字段；子模块分别接收 `topics / titles / quotes / chart_data /
title+subtitle+dimensions+summary`。

完整变量表与子模块结构详见插件仓库
[`docs/REPORT_TEMPLATE_GUIDE.md`](https://github.com/SXP-Simon/astrbot_plugin_qq_group_daily_analysis/blob/main/docs/REPORT_TEMPLATE_GUIDE.md#3-渲染变量契约)。

## 自检脚本

仓库根提供 `verify_demo.py`，在修改模板后运行：

```bash
# 仅校验模板自身（语法 + StrictUndefined 渲染）
python verify_demo.py

# 完整检查：额外模拟打包 zip 走一遍插件的安装/卸载流程
python verify_demo.py <插件仓库路径>   # 或 export PLUGIN_ROOT=<插件仓库路径>
```

它会依次：校验全部 HTML 的 Jinja2 语法 → 用 StrictUndefined 实际渲染 7 个模板
（任何变量缺失/结构错误立即报错）→ 模拟打包 zip 走一遍插件的安装/卸载流程。

> 安装/卸载检查依赖插件仓库 `src/` 中的安装器（脚本内置 astrbot mock，可离线运行）。

## 预览图生成

仓库根提供 `generate_preview.py`，用无头浏览器（Chrome/Edge）渲染模板并生成：

- `assets/gda_sky_diary-demo.jpg`（完整长图）
- `assets/gda_sky_diary-demo-thumb.jpg`（README 展示缩略图）
- `gda_sky_diary/preview.jpg`（随模板打包，供 `/查看模板` 显示）

```bash
python generate_preview.py
```

`verify_demo.py` 的 mock 数据在生成脚本中扩展成了更完整的示例内容
（3 位群友、2 条金句、质量锐评等），修改模板后重跑即可刷新预览图。

## 许可

MIT，可自由复制修改。
