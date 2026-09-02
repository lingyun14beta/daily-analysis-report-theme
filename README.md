# 群聊日常分析 · 报告模板示例仓库（Sky Diary 天空日记）

本仓库是 [astrbot_plugin_qq_group_daily_analysis](https://github.com/SXP-Simon/astrbot_plugin_qq_group_daily_analysis)
的 **报告视觉模板示例仓库**，可以作为你自己的模板仓库的起点。

内置模板：**`gda_sky_diary`（天空日记 Sky Diary）** —— 蓝白渐变现代简约风。

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
| 显示名 | 可选 `template.json`：`{"name": "中文名", "desc": "说明"}` |

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

## 许可

MIT，可自由复制修改。
