#!/usr/bin/env python3
from __future__ import annotations

import json
import math
from pathlib import Path
import sys
from typing import Any

from PIL import Image, ImageDraw, ImageFont

try:
    from .project_paths import GENERATED_TALISMANS_DIR
except ImportError:
    ROOT_DIR = Path(__file__).resolve().parents[1]
    if str(ROOT_DIR) not in sys.path:
        sys.path.insert(0, str(ROOT_DIR))
    from core.project_paths import GENERATED_TALISMANS_DIR


BASE_DIR = Path(__file__).resolve().parent
GENERATED_DIR = GENERATED_TALISMANS_DIR
GENERATED_DIR.mkdir(parents=True, exist_ok=True)


def pick_font(*candidates: str) -> str:
    for raw in candidates:
        path = Path(raw)
        if path.exists():
            return str(path)
    raise FileNotFoundError("No usable font found")


FONT_REG = pick_font("C:/Windows/Fonts/arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
FONT_BOLD = pick_font("C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", FONT_REG)


PALETTES = {
    "gold": {"bg": "#fbf7ee", "line1": "#c89b39", "line2": "#6f4ca8", "ink": "#201d29"},
    "emerald": {"bg": "#f3fbf5", "line1": "#1d9079", "line2": "#6f4ca8", "ink": "#203028"},
    "blue": {"bg": "#f4f8fd", "line1": "#3163b2", "line2": "#8f62c8", "ink": "#1a2238"},
    "violet": {"bg": "#f7f3fc", "line1": "#7a4ec4", "line2": "#d2ad41", "ink": "#251e37"},
    "midnight": {"bg": "#edf0f8", "line1": "#2f3f6b", "line2": "#8b5ec6", "ink": "#192133"},
}


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size=size)


def slugify(text: str) -> str:
    import re
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return re.sub(r"_+", "_", text).strip("_") or "talisman"


def draw_centered(draw: ImageDraw.ImageDraw, xy: tuple[float, float], text: str,
                  font: ImageFont.FreeTypeFont, fill: str) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    x = xy[0] - (bbox[2] - bbox[0]) / 2
    y = xy[1] - (bbox[3] - bbox[1]) / 2
    draw.text((x, y), text, font=font, fill=fill)


def render_talisman(result: dict[str, Any], output_path: str | Path | None = None,
                    title: str | None = None) -> Path:
    tal = result["talisman"]
    domain = result.get("domain", {})
    palette = PALETTES.get(domain.get("color", "gold"), PALETTES["gold"])

    img = Image.new("RGB", (1400, 1400), palette["bg"])
    draw = ImageDraw.Draw(img)
    cx, cy = 700, 700

    for radius, width, color in [(450, 7, palette["line1"]), (345, 5, palette["line2"]), (250, 4, palette["line1"]), (140, 4, palette["line2"])]:
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=color, width=width)

    outer_r = 390
    inner_r = 280
    for i in range(8):
        angle = math.radians(45 * i - 90)
        x1 = cx + inner_r * math.cos(angle)
        y1 = cy + inner_r * math.sin(angle)
        x2 = cx + outer_r * math.cos(angle)
        y2 = cy + outer_r * math.sin(angle)
        draw.line((cx, cy, x2, y2), fill=palette["line1"], width=3)
        draw.ellipse((x1 - 48, y1 - 28, x1 + 48, y1 + 28), outline=palette["line2"], width=3, fill="#ffffff")
        draw.ellipse((x2 - 58, y2 - 32, x2 + 58, y2 + 32), outline=palette["line1"], width=3, fill="#fffdf9")

    for offset in [0, 22.5]:
        pts = []
        r = 330 if offset == 0 else 230
        for i in range(4):
            angle = math.radians(offset + 45 + i * 90)
            pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
        for i in range(4):
            draw.line((*pts[i], *pts[(i + 1) % 4]), fill=palette["line2" if offset else "line1"], width=4)

    center_radius = 95
    draw.ellipse((cx - center_radius, cy - center_radius, cx + center_radius, cy + center_radius), outline=palette["line1"], width=5, fill="#ffffff")
    center_text = str(tal["center"])
    draw_centered(draw, (cx, cy - 10), center_text, _font(64, True), palette["line2"])
    ref_text = str(result.get("source", "source"))
    draw_centered(draw, (cx, cy + 52), ref_text, _font(24, False), palette["line1"])

    for i, value in enumerate(tal["inner_ring"][:8]):
        angle = math.radians(45 * i - 90)
        x = cx + inner_r * math.cos(angle)
        y = cy + inner_r * math.sin(angle)
        draw_centered(draw, (x, y), str(value), _font(34, True), palette["ink"])

    for i, value in enumerate(tal["outer_ring"][:8]):
        angle = math.radians(45 * i - 90)
        x = cx + outer_r * math.cos(angle)
        y = cy + outer_r * math.sin(angle)
        draw_centered(draw, (x, y), str(value), _font(30, False), palette["ink"])

    headline = title or result.get("source", "Talisman")
    draw_centered(draw, (700, 70), headline, _font(38, True), palette["line1"])
    scheme_text = domain.get("label") or result.get("scheme_label") or "Sacred Signature"
    draw_centered(draw, (700, 120), scheme_text, _font(24, False), palette["line2"])

    spirit = result.get("spirit", {})
    if spirit:
        footer = spirit.get("reading", "")
    else:
        footer = "Phi • nombre • texte • sceau"
    draw_centered(draw, (700, 1320), footer[:110], _font(22, False), palette["ink"])

    if output_path is None:
        output_path = GENERATED_DIR / f"{slugify(headline)}.png"
    else:
        output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
    return output_path


def render_from_json_file(path: str | Path, output_path: str | Path | None = None) -> Path:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return render_talisman(data, output_path=output_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True)
    parser.add_argument("--out")
    args = parser.parse_args()
    out = render_from_json_file(args.json, args.out)
    print(out)
