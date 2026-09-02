"""端到端验证：demo 模板打包安装后，元信息与预览图可被插件识别。"""
import io
import json
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(r"D:\Edge浏览器下载\files (1)\daily-analysis-report-theme")
TPL = ROOT / "gda_sky_diary"

sys.path.insert(0, r"D:\Edge浏览器下载\files (1)\astrbot_plugin_qq_group_daily_analysis_new")
sys.path.insert(0, ROOT)

import logging  # noqa: E402
import types  # noqa: E402

if "astrbot.api" not in sys.modules:
    astrbot_module = types.ModuleType("astrbot")
    astrbot_api_module = types.ModuleType("astrbot.api")
    astrbot_star_module = types.ModuleType("astrbot.api.star")
    astrbot_api_module.logger = logging.getLogger("astrbot-demo")
    astrbot_api_module.AstrBotConfig = dict

    class StarTools:  # noqa: D101
        pass

    comp_module = types.ModuleType("astrbot.api.message_components")

    class BaseMessageComponent:  # noqa: D101
        pass

    class Image:  # noqa: D101
        def __init__(self, *a, **k):
            pass

    class Node:  # noqa: D101
        def __init__(self, *a, **k):
            pass

    class Nodes:  # noqa: D101
        def __init__(self, *a, **k):
            pass

    class Plain:  # noqa: D101
        def __init__(self, *a, **k):
            pass

    comp_module.BaseMessageComponent = BaseMessageComponent
    comp_module.Image = Image
    comp_module.Node = Node
    comp_module.Nodes = Nodes
    comp_module.Plain = Plain
    astrbot_star_module.StarTools = StarTools
    astrbot_module.api = astrbot_api_module
    astrbot_api_module.message_components = comp_module
    sys.modules.setdefault("astrbot", astrbot_module)
    sys.modules.setdefault("astrbot.api", astrbot_api_module)
    sys.modules.setdefault("astrbot.api.star", astrbot_star_module)
    sys.modules.setdefault("astrbot.api.message_components", comp_module)

from src.infrastructure.reporting.template_installer import (  # noqa: E402
    install_template_from_zip,
)
from src.infrastructure.reporting import template_installer  # noqa: E402
from src.infrastructure.reporting.templates import HTMLTemplates  # noqa: E402
from src.application.commands.template_command_service import (  # noqa: E402
    TemplateCommandService,
)
from unittest.mock import MagicMock  # noqa: E402

# 打包（含 template.json 新字段 + preview.jpg）
buf = io.BytesIO()
with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
    for f in sorted(TPL.rglob("*")):
        if f.is_file():
            zf.write(f, f.relative_to(ROOT).as_posix())

with tempfile.TemporaryDirectory() as tmp:
    custom_root = Path(tmp) / "custom"
    custom_root.mkdir()
    result = install_template_from_zip(
        buf.getvalue(), store_dir=custom_root, source="url",
        source_url="https://github.com/lingyun14beta/daily-analysis-report-theme",
    )
    print("install:", result["name"], "| label =", result["label"], "| files =", len(result["files"]))

    # 元信息透出
    mock = MagicMock()
    mock.get_custom_report_template_dir = MagicMock(
        side_effect=lambda n: (custom_root / n) if n else custom_root
    )
    items = {t["id"]: t for t in HTMLTemplates(mock).get_available_templates()}
    meta = items["gda_sky_diary"]
    print("meta:", meta["display_name"], "|", meta["tag"], "|", meta["desc"])
    assert meta["display_name"] == "天空日记 (Sky Diary)"
    assert meta["tag"] == "清新渐变"
    assert meta["tag_color"] == "blue"

    # 预览图优先级：模板目录内 preview.jpg
    import src.infrastructure.reporting.template_installer as ti_mod

    original = ti_mod.default_template_store_dir
    ti_mod.default_template_store_dir = lambda: custom_root
    service = TemplateCommandService(plugin_root=str(ROOT))
    preview = service.resolve_template_preview_path("gda_sky_diary")
    preview = service.resolve_template_preview_path("gda_sky_diary")
    print("preview:", preview)
    assert preview is not None and preview.endswith("preview.jpg")
    assert Path(preview).is_file()

    # 列表包含自定义模板
    names = service.list_available_templates()
    print("list contains custom:", "gda_sky_diary" in names)
    assert "gda_sky_diary" in names
    ti_mod.default_template_store_dir = original

print("ALL OK")
