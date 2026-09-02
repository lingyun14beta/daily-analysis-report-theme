"""生成模板预览图：渲染 image_template.html → 无头浏览器截图 → 白边裁剪 → JPEG。

用法:
    python generate_preview.py

输出: assets/gda_sky_diary-demo.jpg
依赖: 无头浏览器（Chrome/Edge），可选 PIL（环境无 PIL 时保留 PNG）。
"""
import base64
import shutil
import subprocess
import tempfile
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).resolve().parent
TPL = ROOT / "gda_sky_diary"
OUT_DIR = ROOT / "assets"
OUT_JPG = OUT_DIR / "gda_sky_diary-demo.jpg"
OUT_THUMB = OUT_DIR / "gda_sky_diary-demo-thumb.jpg"
OUT_PNG = OUT_DIR / "gda_sky_diary-demo.png"

# ---------- 1) 构造示例数据并渲染 ----------
def svg_avatar(color: str) -> str:
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96">'
        f'<circle cx="48" cy="34" r="16" fill="{color}"/>'
        f'<path d="M16 88c0-18 14-28 32-28s32 10 32 28z" fill="{color}"/>'
        f'</svg>'
    )
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


env = Environment(
    loader=FileSystemLoader(str(TPL)),
    autoescape=True,
    trim_blocks=True,
    lstrip_blocks=True,
    undefined=StrictUndefined,
)
common = {
    "hide_user_names": False,
    "t2i_font_source": "Mainland",
    "t2i_google_fonts_mirror": "https://fonts.googleapis.com",
    "t2i_gstatic_mirror": "https://fonts.gstatic.com",
    "t2i_atri_font_mirror": "",
}
sub_ctx = {
    "topics": [
        {
            "index": 1,
            "topic": {"topic": "今晚吃什么？群里聊了 40 分钟"},
            "contributors": "小明、小红、阿伟",
            "detail": "最终决定去吃火锅，<b>人均 80</b>，周五晚八点老地方集合～",
        },
        {
            "index": 2,
            "topic": {"topic": "新版本功能讨论"},
            "contributors": "阿伟、小美",
            "detail": "建议把聊天记录导出做成 markdown，被采纳了！",
        },
    ],
    "titles": [
        {
            "name": "小明",
            "title": "话题发动机",
            "mbti": "ENFP",
            "reason": "几乎每个话题都由 TA 开启，是群里的气氛担当。",
            "avatar_data": svg_avatar("#4a9fd8"),
            "profile_display": "ENFP",
        },
        {
            "name": "小红",
            "title": "深夜守望者",
            "mbti": "ISTP",
            "reason": "凌晨 1 点的群里，总能看到 TA 的回复。",
            "avatar_data": svg_avatar("#f6a940"),
            "profile_display": "ISTP",
        },
        {
            "name": "阿伟",
            "title": "冷场救星",
            "mbti": "INFJ",
            "reason": "擅长在话题冷却时丢出新的讨论点。",
            "avatar_data": svg_avatar("#5cbf8a"),
            "profile_display": "INFJ",
        },
    ],
    "quotes": [
        {
            "content": "今天真开心，感觉自己又变聪明了一点",
            "sender": "小红",
            "reason": "典型的“学点新东西就膨胀”式自我鼓励，已被群友习惯性点赞。",
            "avatar_url": svg_avatar("#f6a940"),
        },
        {
            "content": "猫又踩我键盘了！！",
            "sender": "阿伟",
            "reason": "猫：这键盘手感不错，以后归我了。",
            "avatar_url": svg_avatar("#5cbf8a"),
        },
    ],
    "chart_data": [{"hour": i, "count": i, "percentage": i * 4} for i in range(24)],
    "title": "今日群聊质量锐评",
    "subtitle": "总体氛围极佳",
    "summary": "全群保持高热度互动，深夜回血、白天封神，只差亿点点正经。",
    "dimensions": [
        {"name": "活跃度", "percentage": 92, "comment": "全天无冷场"},
        {"name": "话题深度", "percentage": 68, "comment": "吃一半聊一半"},
        {"name": "含梗量", "percentage": 88, "comment": "表情包含量超标"},
    ],
}
topics_html = env.get_template("topic_item.html").render(**common, **sub_ctx)
titles_html = env.get_template("user_title_item.html").render(**common, **sub_ctx)
quotes_html = env.get_template("quote_item.html").render(**common, **sub_ctx)
hourly_chart_html = env.get_template("activity_chart.html").render(**common, **sub_ctx)
chat_quality_html = env.get_template("chat_quality_item.html").render(**common, **sub_ctx)
main_ctx = {
    **common,
    "topics_html": topics_html,
    "titles_html": titles_html,
    "quotes_html": quotes_html,
    "hourly_chart_html": hourly_chart_html,
    "chat_quality_html": chat_quality_html,
    "message_count": 233,
    "participant_count": 42,
    "total_characters": 8765,
    "emoji_count": 131,
    "most_active_period": "21:00 - 23:00",
    "current_date": "2026年08月01日",
    "current_datetime": "2026-08-01 23:59:12",
    "total_tokens": 15234,
    "prompt_tokens": 8033,
    "completion_tokens": 7201,
}
preview_html = env.get_template("image_template.html").render(**main_ctx)

with tempfile.TemporaryDirectory(prefix="tpl_preview_") as tmp:
    tmp_dir = Path(tmp)
    html_path = tmp_dir / "preview.html"
    png_path = tmp_dir / "preview.png"
    html_path.write_text(preview_html, encoding="utf-8")

    # ---------- 2) 无头浏览器截图 ----------
    browser = shutil.which("msedge") or shutil.which(
        "chrome"
    ) or shutil.which("chromium") or None
    candidates = [
        browser,
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    ]
    browser = next((c for c in candidates if c and Path(c).exists()), None)
    if not browser:
        raise SystemExit("未找到 Chrome/Edge 浏览器，无法生成预览图。")

    subprocess.run(
        [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            "--window-size=750,3400",
            f"--user-data-dir={tmp_dir / 'profile'}",
            f"--screenshot={png_path}",
            html_path.as_uri(),
        ],
        check=True,
        capture_output=True,
        timeout=120,
    )
    if not png_path.exists():
        raise SystemExit("截图失败：输出文件不存在。")

    # ---------- 3) 白边裁剪 + 转 JPEG ----------
    try:
        from PIL import Image
    except ImportError:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        png_path.replace(OUT_PNG)
        print(f"[ok] 预览图已生成（PNG）: {OUT_PNG}")
        raise SystemExit(0)

    img = Image.open(png_path).convert("RGB")
    w, h = img.size
    pixels = img.load()
    # 从底部向上跳过纯白/近白行
    bottom = h
    for y in range(h - 1, 0, -1):
        row_white = True
        for x in range(0, w, 8):  # 采样步长 8 加速
            r, g, b = pixels[x, y]
            if not (r > 248 and g > 248 and b > 248):
                row_white = False
                break
        if not row_white:
            bottom = y + 1
            break
    cropped = img.crop((0, 0, w, min(bottom + 24, h)))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cropped.save(OUT_JPG, "JPEG", quality=88)
    print(f"[ok] 预览图已生成: {OUT_JPG} ({cropped.size[0]}x{cropped.size[1]})")

    # README 使用的缩略图（宽 420，保持比例）
    thumb = cropped.copy()
    thumb.thumbnail((420, 1200))
    thumb.save(OUT_THUMB, "JPEG", quality=85)
    print(f"[ok] 缩略图已生成: {OUT_THUMB} ({thumb.size[0]}x{thumb.size[1]})")

    # 复制一份到模板目录（随 zip 打包安装后，QQ /查看模板 即可显示该预览图）
    cropped.save(TPL / "preview.jpg", "JPEG", quality=88)
    print(f"[ok] 已同步模板目录预览图: {TPL / 'preview.jpg'}")
