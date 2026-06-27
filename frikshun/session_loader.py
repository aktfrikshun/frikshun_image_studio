from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional

import yaml
from pydantic import BaseModel

from frikshun.models import SessionManifest

CONFIG_FILE = "frikshun_image_studio.yaml"


class StudioConfig(BaseModel):
    studio_root: Path

    @property
    def sessions_dir(self) -> Path:
        return self.studio_root / "sessions"

    @property
    def outputs_dir(self) -> Path:
        return self.studio_root / "outputs"

    @property
    def approved_dir(self) -> Path:
        return self.studio_root / "reference-decks" / "approved"

    @property
    def rejected_dir(self) -> Path:
        return self.studio_root / "reference-decks" / "rejected"

    @property
    def feedback_dir(self) -> Path:
        return self.studio_root / "rejection-feedback"

    @property
    def logs_dir(self) -> Path:
        return self.studio_root / "logs"


def resolve_studio_root(cli_value: Optional[Path] = None, cwd: Optional[Path] = None) -> Path:
    cwd = cwd or Path.cwd()
    if cli_value:
        return cli_value.expanduser().resolve()
    env_value = os.getenv("FRIKSHUN_STUDIO_ROOT")
    if env_value:
        return Path(env_value).expanduser().resolve()
    config_path = cwd / CONFIG_FILE
    if config_path.exists():
        data = yaml.safe_load(config_path.read_text()) or {}
        configured = data.get("studio_root")
        if configured:
            return _resolve_path(Path(configured), cwd)
    return (cwd / "studio").resolve()


def ensure_studio_dirs(config: StudioConfig) -> None:
    for path in [
        config.sessions_dir,
        config.outputs_dir,
        config.approved_dir,
        config.rejected_dir,
        config.feedback_dir,
        config.logs_dir,
        config.studio_root / "reference-decks",
        config.studio_root / "style-packs",
    ]:
        path.mkdir(parents=True, exist_ok=True)


def _resolve_path(path: Path, base: Path) -> Path:
    path = path.expanduser()
    if path.is_absolute():
        return path
    return (base / path).resolve()


def resolve_studio_path(config: StudioConfig, value: str | Path) -> Path:
    return _resolve_path(Path(value), config.studio_root)


def resolve_session_path(config: StudioConfig, value: str | Path) -> Path:
    candidate = Path(value).expanduser()
    if candidate.is_absolute():
        return candidate
    if candidate.suffix in {".yaml", ".yml"}:
        if candidate.exists():
            return candidate.resolve()
        return resolve_studio_path(config, candidate)
    return config.sessions_dir / f"{candidate}.yaml"


def load_manifest(config: StudioConfig, value: str | Path) -> SessionManifest:
    path = resolve_session_path(config, value)
    if not path.exists():
        raise FileNotFoundError(f"Session manifest not found: {path}")
    data: dict[str, Any] = yaml.safe_load(path.read_text()) or {}
    return SessionManifest.model_validate(data)


def create_session_manifest(
    config: StudioConfig,
    name: str,
    character: str = "Unnamed Artist",
    description: str = "",
) -> Path:
    ensure_studio_dirs(config)
    path = config.sessions_dir / f"{name}.yaml"
    if path.exists():
        raise FileExistsError(f"Session already exists: {path}")
    manifest = {
        "session_id": name,
        "character": character,
        "description": description,
        "visual_canon_file": "",
        "image_directives_file": "",
        "negative_canon_file": "",
        "images": [
            {
                "id": "001",
                "filename": "001_example.png",
                "creative_brief": {
                    "asset_id": "001",
                    "purpose": "Describe the goal for this asset",
                    "success_criteria": "What must be true for approval",
                    "generation_guidance": "Portrait generation details",
                    "review_focus": "What reviewers should inspect most closely",
                },
                "status": "pending",
            }
        ],
    }
    path.write_text(yaml.safe_dump(manifest, sort_keys=False))
    return path
