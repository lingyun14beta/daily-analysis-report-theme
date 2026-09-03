# AGENTS.md — AstrBot 报告视觉模板开发守则

本仓库是 AstrBot「群聊日常分析」插件的**报告视觉模板**仓库（可作为 template 起点）。
以下规则适用于本仓库内的模板开发，以及 AI 辅助修改（AI 参与时必须以本文件为准）。

## 仓库结构约定

- **模板目录**：`<模板名>/`——示例：以 `gda_` 开头的小写英文蛇形
  （如 `gda_sky_diary/`），内含插件契约的 7 件套 HTML
  （`image_template.html` / `html_template.html` / `topic_item.html` /
  `user_title_item.html` / `quote_item.html` / `activity_chart.html` /
  `chat_quality_item.html`），以及可选 `template.json`（展示元信息）与
  `preview.*`（随包预览图）。
- **配套脚本**（自检、预览图生成）一律放**仓库根**，禁止放入模板目录。
- 仓库根 README 是使用说明；本文件是开发守则，两者冲突时以本文件为准。

## 修改工作流（模板的任何改动之后）

1. **校验**：运行仓库根的自检脚本（若存在 `verify_*.py` 等，用法见 README；
   脚本会校验全部 HTML 的 Jinja2 语法并以严格 undefined 实际渲染，
   任何变量错误/缺失即失败）。没有脚本时，逐项自查「变量契约」与「资源引用」。
2. **更新产物**：改动视觉样式后，若存在预览图生成脚本，运行它并
   **提交新生成的预览图**（含随模板打包的那一份）。
3. **提交**：一次提交包含「模板改动 + 自检通过」；产物图与源码一并提交。

## 渲染变量契约（插件固定，不可修改）

主骨架（`image_template.html` / `html_template.html`）接收：
`topics_html`、`titles_html`、`quotes_html`、`hourly_chart_html`、
`chat_quality_html`（可能为空串）、`message_count`、`participant_count`、
`total_characters`、`emoji_count`、`most_active_period`、`current_date`、
`current_datetime`、`total_tokens` / `prompt_tokens` / `completion_tokens`、
`hide_user_names`、`t2i_font_source` / `t2i_google_fonts_mirror` /
`t2i_gstatic_mirror` / `t2i_atri_font_mirror`。

子模块：

| 文件 | 变量 |
| --- | --- |
| `topic_item.html` | `topics` |
| `user_title_item.html` | `titles` |
| `quote_item.html` | `quotes` |
| `activity_chart.html` | `chart_data` |
| `chat_quality_item.html` | 直接展开 `title`/`subtitle`/`summary`/`dimensions` |

注意：`topic.detail`、`quote.reason` 是系统预渲染 HTML（含头像），输出必须加
`| safe`；其余字段由插件负责转义，模板不要二次转义；所有模板还共同获得
`hide_user_names` 与 `t2i_*` 字体配置。

## 资源引用（渲染链路约束，极易踩坑）

- 报告 HTML 以字符串交给远端 T2I 渲染服务，**没有本地文件上下文**：
  - ✅ 绝对 URL（长期稳定的公开图库链接）或 ✅ 内联 `data:` URI / `<svg>`
  - ❌ 相对路径（`src="assets/bg.png"`）渲染时必然 404
- 例外：`preview.*`（模板目录内预览图）用于 `/查看模板` 展示，不走渲染管线，可用。
- 小图标/装饰优先内联 SVG 或 data URI；大图走仓库图库绝对链接。

## 命名与元信息

- 模板名建议小写英文蛇形并带命名空间前缀（如 `gda_sky_diary`）；
  ≤50 字符；禁空格、路径分隔符与文件系统危险字符；与内置模板重名会被拒绝。
- `template.json` **仅支持 JSON**，全部字段可选、字符串 ≤100 字符：
  `{"name": 显示名, "desc": 描述, "tag": 风格标签, "tag_color": 标签配色}`。

## 打包与安装器校验（强制）

- 一个 zip 只装一个模板；模板根目录至少含 `image_template.html` 或
  `html_template.html` 其一；允许外层 `repo-main` 式根目录（自动剥离）。
- 限额：解压后 ≤64MB、单文件 ≤20MB、成员 ≤300；路径穿越（`../`、绝对路径）
  与控制字符文件名会被拒绝；加密 zip 无法解压。
- 同时提供 `image_template.html` 与 `html_template.html` 时两者各司其职
  （image→长图，html→网页，html 渲染失败自动回退 image），互不冲突。

## 禁止事项

- 修改/复制插件功能代码（本仓库不含插件实现；模板只能消费上述变量契约）。
- 硬编码本机或他人的绝对路径。
- 引入新运行时依赖（模板是纯 HTML/Jinja，无 Python 依赖）。
- 改动 7 件套的文件名与变量契约（这是与插件渲染器的契约面）。
