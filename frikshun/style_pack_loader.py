from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from frikshun.models import StylePack


def list_style_packs(studio_root: Path) -> list[str]:
    """Return available style pack names for a studio root."""

    root = studio_root / "style-packs"
    if not root.exists():
        return []
    return sorted(path.name for path in root.iterdir() if path.is_dir())


def load_style_pack(name: str, studio_root: Path) -> StylePack:
    """Load a style pack by folder name."""

    style_dir = studio_root / "style-packs" / name
    if not style_dir.exists():
        raise FileNotFoundError(f"Style pack not found: {style_dir}")
    return StylePack(
        name=name,
        path=style_dir,
        style_text=_read_text(style_dir / "style.md"),
        wardrobe=_read_json(style_dir / "wardrobe.json"),
        palette=_read_json(style_dir / "palette.json"),
        lighting=_read_json(style_dir / "lighting.json"),
        camera=_read_json(style_dir / "camera.json"),
        negative_text=_read_text(style_dir / "negative.md"),
    )


def _read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Style pack file missing: {path}")
    return path.read_text().strip()


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Style pack file missing: {path}")
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError(f"Style pack JSON invalid: {path} ({exc})") from exc
    if not isinstance(data, dict):
        raise ValueError(f"Style pack JSON must be an object: {path}")
    return data
