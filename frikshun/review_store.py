from __future__ import annotations

import json
import shutil
from pathlib import Path

from frikshun.generator import ImageGenerator
from frikshun.models import GeneratedImage, ImageTask, SessionManifest
from frikshun.prompt_builder import PromptBuilder
from frikshun.session_loader import StudioConfig, ensure_studio_dirs, load_manifest


class ReviewStore:
    def __init__(self, config: StudioConfig):
        self.config = config
        ensure_studio_dirs(config)
        self.prompt_builder = PromptBuilder(config)

    def load_manifest(self, value: str | Path) -> SessionManifest:
        return load_manifest(self.config, value)

    def generate_session(
        self, manifest: SessionManifest, generator: ImageGenerator
    ) -> list[GeneratedImage]:
        created: list[GeneratedImage] = []
        for task in manifest.images:
            if task.status in {"pending", "candidate"}:
                created.append(self.regenerate(manifest, task.id, generator))
        return created

    def regenerate(
        self, manifest: SessionManifest, asset_id: str, generator: ImageGenerator
    ) -> GeneratedImage:
        task = self._task(manifest, asset_id)
        version = self.next_version(manifest.session_id, task.id)
        version_dir = self.config.outputs_dir / manifest.session_id / task.id / f"v{version:03d}"
        output_path = version_dir / task.filename
        prompt_audit_path = version_dir / "prompt_audit.md"
        built = self.prompt_builder.build(manifest, task)
        generated = generator.generate(
            built.final_prompt,
            built.final_negative_prompt,
            output_path,
            asset_id=task.id,
            session_id=manifest.session_id,
            version=version,
            prompt_audit_path=prompt_audit_path,
        )
        generated.style_packs = [pack["name"] for pack in built.style_packs]
        generated.style_pack_summaries = {
            pack["name"]: {
                "style_text": pack["style_text"],
                "wardrobe": pack["wardrobe"],
                "palette": pack["palette"],
                "lighting": pack["lighting"],
                "camera": pack["camera"],
                "negative_text": pack["negative_text"],
            }
            for pack in built.style_packs
        }
        self.save_generated(generated)
        prompt_audit_path.write_text(built.audit_markdown)
        return generated

    def candidates(self, session_id: str | None = None) -> list[GeneratedImage]:
        roots = [self.config.outputs_dir / session_id] if session_id else list(self.config.outputs_dir.glob("*"))
        images: list[GeneratedImage] = []
        for root in roots:
            if not root.exists():
                continue
            for metadata_path in sorted(root.glob("*/*/*.json")):
                image = self.read_metadata(metadata_path)
                if image.status == "candidate":
                    images.append(image)
        return images

    def approved_references(
        self,
        session_id: str,
        *,
        model_status: str | None = None,
        limit: int | None = None,
    ) -> list[GeneratedImage]:
        root = self.config.approved_dir / session_id
        if not root.exists():
            return []
        images = []
        for metadata_path in sorted(root.glob("*.json")):
            image = self.read_metadata(metadata_path)
            if image.status != "approved" and not image.approved:
                continue
            if model_status and image.model_status != model_status:
                continue
            images.append(image)
        images.sort(key=self._reference_rank, reverse=True)
        return images[:limit] if limit else images

    def approved_references_by_role(self, *canonical_roles: str) -> list[GeneratedImage]:
        wanted = {role for role in canonical_roles if role}
        if not wanted or not self.config.approved_dir.exists():
            return []
        images: list[GeneratedImage] = []
        for metadata_path in sorted(self.config.approved_dir.glob("*/*.json")):
            image = self.read_metadata(metadata_path)
            if image.status != "approved" and not image.approved:
                continue
            if image.canonical_role in wanted:
                images.append(image)
        images.sort(key=self._reference_rank, reverse=True)
        return images

    def approve(
        self,
        metadata_path: Path,
        *,
        identity_score: float | None = None,
        canon_confidence: float | None = None,
        appearance_score: float | None = None,
        expression_score: float | None = None,
        technical_score: float | None = None,
        continuity_score: float | None = None,
        reference_priority: str = "",
        canonical_name: str = "",
        canonical_role: str = "",
        model_status: str = "",
        notes: str = "",
        measurement_notes: dict[str, str] | None = None,
        locked_attributes: list[str] | None = None,
    ) -> GeneratedImage:
        image = self.read_metadata(metadata_path)
        target_dir = self.config.approved_dir / image.session_id
        moved = self._move_pair(image, target_dir)
        moved.status = "approved"
        moved.rejection_type = ""
        moved.rejection_reason = ""
        moved.identity_score = identity_score
        moved.canon_confidence = canon_confidence
        moved.appearance_score = appearance_score
        moved.expression_score = expression_score
        moved.technical_score = technical_score
        moved.continuity_score = continuity_score
        moved.reference_score = self.reference_score(moved)
        moved.reference_priority = reference_priority.strip()
        moved.canonical_name = canonical_name.strip()
        moved.canonical_role = canonical_role.strip()
        moved.model_status = model_status.strip()
        moved.approved = True
        moved.notes = notes.strip()
        if measurement_notes is not None:
            moved.measurement_notes = measurement_notes
        if locked_attributes is not None:
            moved.locked_attributes = locked_attributes
        self.save_generated(moved)
        return moved

    def reject(self, metadata_path: Path, reason: str, rejection_type: str = "") -> GeneratedImage:
        if not reason.strip():
            raise ValueError("Rejection reason is required.")
        image = self.read_metadata(metadata_path)
        target_dir = self.config.rejected_dir / image.session_id
        moved = self._move_pair(image, target_dir)
        moved.status = "rejected"
        moved.rejection_type = rejection_type.strip()
        moved.rejection_reason = reason.strip()
        moved.approved = False
        self.save_generated(moved)
        self.append_feedback(moved.session_id, moved.asset_id, reason.strip(), rejection_type.strip())
        return moved

    def append_feedback(self, session_id: str, asset_id: str, reason: str, rejection_type: str = "") -> Path:
        path = self.config.feedback_dir / session_id / f"{asset_id}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = path.read_text() if path.exists() else f"# Rejection Feedback: {session_id}/{asset_id}\n\n"
        type_text = rejection_type or "unspecified"
        path.write_text(
            existing.rstrip()
            + "\n\n"
            + "## Rejected Attempt\n\n"
            + f"- Type: {type_text}\n"
            + f"- Reason: {reason}\n"
        )
        return path

    def next_version(self, session_id: str, asset_id: str) -> int:
        asset_root = self.config.outputs_dir / session_id / asset_id
        versions = []
        if asset_root.exists():
            for child in asset_root.iterdir():
                if child.is_dir() and child.name.startswith("v") and child.name[1:].isdigit():
                    versions.append(int(child.name[1:]))
        return max(versions, default=0) + 1

    def save_generated(self, image: GeneratedImage) -> None:
        image.metadata_path.parent.mkdir(parents=True, exist_ok=True)
        data = image.model_dump(mode="json")
        data.pop("output_path", None)
        data.pop("metadata_path", None)
        data.pop("prompt_audit_path", None)
        image.metadata_path.write_text(json.dumps(data, indent=2))

    def read_metadata(self, metadata_path: Path) -> GeneratedImage:
        data = json.loads(metadata_path.read_text())
        output_path = metadata_path.with_suffix(".png")
        prompt_audit_path = metadata_path.parent / "prompt_audit.md"
        filename = data.get("filename") or output_path.name
        output_path = metadata_path.with_name(filename)
        return GeneratedImage(
            **data,
            output_path=output_path,
            metadata_path=metadata_path,
            prompt_audit_path=prompt_audit_path,
        )

    def reference_score(self, image: GeneratedImage) -> float | None:
        required_scores = [
            image.identity_score,
            image.continuity_score,
            image.canon_confidence,
            image.technical_score,
        ]
        if any(score is None for score in required_scores):
            return None
        return round(
            image.identity_score * 0.4
            + image.continuity_score * 0.3
            + image.canon_confidence * 0.2
            + image.technical_score * 0.1,
            2,
        )

    def _reference_rank(self, image: GeneratedImage) -> tuple[float, float, float]:
        score = image.reference_score
        if score is None:
            score = self.reference_score(image)
        if score is None:
            score = 0.0
        priority = 1.0 if image.reference_priority == "primary" else 0.0
        return (score, priority, image.identity_score or 0.0)

    def _task(self, manifest: SessionManifest, asset_id: str) -> ImageTask:
        for task in manifest.images:
            if task.id == asset_id:
                return task
        raise ValueError(f"Asset not found in session {manifest.session_id}: {asset_id}")

    def _move_pair(self, image: GeneratedImage, target_dir: Path) -> GeneratedImage:
        target_dir.mkdir(parents=True, exist_ok=True)
        version_tag = f"v{image.version:03d}"
        image_target = target_dir / f"{image.asset_id}_{version_tag}_{image.output_path.name}"
        metadata_target = image_target.with_suffix(".json")
        audit_target = target_dir / f"{image.asset_id}_{version_tag}_prompt_audit.md"
        shutil.move(str(image.output_path), image_target)
        shutil.move(str(image.metadata_path), metadata_target)
        if image.prompt_audit_path.exists():
            shutil.copy2(image.prompt_audit_path, audit_target)
        image.output_path = image_target
        image.metadata_path = metadata_target
        image.prompt_audit_path = audit_target
        image.filename = image_target.name
        return image
