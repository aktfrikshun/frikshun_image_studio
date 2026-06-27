from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from frikshun.models import ImageTask, SessionManifest
from frikshun.session_loader import StudioConfig, resolve_studio_path
from frikshun.style_pack_loader import load_style_pack


@dataclass
class PromptBuildResult:
    final_prompt: str
    final_negative_prompt: str
    audit_markdown: str
    warnings: list[str]
    style_packs: list[dict]


@dataclass
class RejectionFeedback:
    rejection_type: str
    reason: str


class PromptBuilder:
    """Composes generation prompts from canon, directives, creative brief, and feedback."""

    def __init__(self, config: StudioConfig):
        self.config = config

    def build(self, manifest: SessionManifest, task: ImageTask) -> PromptBuildResult:
        warnings: list[str] = []
        visual_canon = self._read_optional(
            manifest.visual_canon_file or manifest.base_prompt_file,
            "Character visual canon",
            warnings,
        )
        directives = self._read_optional(
            manifest.image_directives_file,
            "Global image creation directives",
            warnings,
        )
        negative = self._read_optional(
            manifest.negative_canon_file or manifest.negative_prompt_file,
            "Negative canon",
            warnings,
        )
        feedback = self.feedback_for(manifest.session_id, task.id)
        locked_guidance = self._locked_attribute_guidance()
        performance_guidance = self._performance_guidance(manifest, task, warnings)
        style_packs = self._style_packs(manifest, task, warnings)
        style_guidance = self._style_pack_guidance(style_packs)
        style_negative = self._style_pack_negative(style_packs)

        creative_brief_text = task.creative_brief.as_generation_text() if task.creative_brief else task.prompt
        body_override = self._body_override(manifest.body_profile, feedback)
        prompt_parts = [
            ("Character visual canon", visual_canon),
            ("Global image creation directives", directives),
            ("Locked attributes from approved references", locked_guidance),
            ("Performance reference", performance_guidance),
            ("Style pack art direction", style_guidance),
            ("Session description", manifest.description),
            ("Creative Brief", creative_brief_text),
            ("Body Specification Override", body_override),
            ("Prior rejection feedback", self._feedback_guidance(feedback)),
        ]
        final_prompt = "\n\n".join(
            f"{title}:\n{text.strip()}" for title, text in prompt_parts if text and text.strip()
        )
        if not final_prompt:
            final_prompt = creative_brief_text
        final_negative_prompt = "\n\n".join(
            part.strip() for part in [negative, style_negative] if part and part.strip()
        )

        audit = self._audit_markdown(
            visual_canon=visual_canon,
            directives=directives,
            style_guidance=style_guidance,
            session_description=manifest.description,
            task=task,
            feedback=feedback,
            body_override=body_override,
            locked_guidance=locked_guidance,
            performance_guidance=performance_guidance,
            style_negative=style_negative,
            final_prompt=final_prompt,
            final_negative_prompt=final_negative_prompt,
            warnings=warnings,
        )
        return PromptBuildResult(
            final_prompt=final_prompt,
            final_negative_prompt=final_negative_prompt,
            audit_markdown=audit,
            warnings=warnings,
            style_packs=[
                {
                    "name": pack.name,
                    "style_text": pack.style_text,
                    "wardrobe": pack.wardrobe,
                    "palette": pack.palette,
                    "lighting": pack.lighting,
                    "camera": pack.camera,
                    "negative_text": pack.negative_text,
                }
                for pack in style_packs
            ],
        )

    def feedback_for(self, session_id: str, asset_id: str) -> list[RejectionFeedback]:
        path = self.config.feedback_dir / session_id / f"{asset_id}.md"
        if not path.exists():
            return []
        text = path.read_text()
        structured = "- Reason:" in text
        feedback: list[RejectionFeedback] = []
        pending_type = ""
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("- Type:"):
                pending_type = stripped.removeprefix("- Type:").strip()
            elif stripped.startswith("- Reason:"):
                reason = stripped.removeprefix("- Reason:").strip()
                feedback.append(RejectionFeedback(pending_type, reason))
                pending_type = ""
            elif not structured and stripped.startswith("- "):
                feedback.append(RejectionFeedback("", stripped[2:].strip()))
        return feedback

    def _read_optional(self, value: str | None, label: str, warnings: list[str]) -> str:
        if not value:
            return ""
        path = resolve_studio_path(self.config, value)
        if not path.exists():
            warnings.append(f"{label} missing: {path}")
            return ""
        return path.read_text().strip()

    def _feedback_guidance(self, feedback: list[RejectionFeedback]) -> str:
        if not feedback:
            return ""
        bullets = "\n".join(
            f"- [{item.rejection_type or 'unspecified'}] {item.reason}" for item in feedback
        )
        if any(item.rejection_type == "canon_refinement" for item in feedback):
            return (
                "Previous rejected attempts identified targeted canon refinements. Preserve approved "
                "characteristics that worked, and change only the canon mismatch described below:\n"
                f"{bullets}"
            )
        return (
            "Previous rejected attempts failed for these reasons. Avoid repeating them:\n"
            f"{bullets}"
        )

    def _revision_strength(self, feedback: list[RejectionFeedback]) -> str:
        canon_refinements = sum(item.rejection_type == "canon_refinement" for item in feedback)
        if canon_refinements >= 2:
            return "strong"
        if canon_refinements == 1:
            return "moderate"
        return "subtle"

    def _body_override(
        self,
        body_profile: dict[str, dict[str, str]],
        feedback: list[RejectionFeedback],
    ) -> str:
        if not body_profile:
            return ""
        strength = self._revision_strength(feedback)
        targets = {name: values.get("target", "") for name, values in body_profile.items()}
        lines = [
            f"Revision strength: {strength}.",
            "This Body Specification Override supersedes any weaker or older body-description language in the canon or creative brief for this asset.",
            "Preserve facial identity, expression, posture, realism, lighting, camera framing, clothing, hair, skin texture, freckles, and documentary presentation exactly.",
            "Change body proportions only.",
            f"Femininity target: {targets.get('femininity', '')}.",
            f"Bust target: {targets.get('bust', '')}.",
            f"Waist target: {targets.get('waist', '')}.",
            f"Hips target: {targets.get('hips', '')}.",
            f"Thighs target: {targets.get('thighs', '')}.",
            f"Torso target: {targets.get('torso', '')}.",
            f"Core engagement target: {targets.get('core_engagement', '')}.",
            f"Pelvic alignment target: {targets.get('pelvic_alignment', '')}.",
            f"Shoulders target: {targets.get('shoulders', '')}.",
            f"Muscle definition target: {targets.get('muscle_definition', '')}.",
            f"Body fat distribution target: {targets.get('body_fat_distribution', '')}.",
            "Translate these structured targets as: Chloe has a naturally feminine hourglass silhouette; her bust is moderately fuller while remaining entirely believable; her waist is visibly more defined; her hips are gently wider to balance her shoulders; her thighs are naturally fuller; her abdomen is flat and healthy with subtle core engagement and minimal lower-abdomen projection; her pelvis is neutrally aligned; her shoulders remain natural and not broad or muscular; muscle definition is subtle; body fat distribution reflects natural femininity rather than athletic conditioning.",
            "Avoid cosmetic enhancement, glamour modeling, pin-up styling, exaggerated breasts, unrealistic waist reduction, sexualized presentation, fitness-influencer physique, bodybuilder definition, and fashion-model thinness.",
        ]
        if strength == "strong":
            lines.append(
                "Because repeated canon refinements have not produced enough anatomical change, apply a clearly visible but still realistic correction to bust, waist, hips, thigh fullness, and overall feminine silhouette."
            )
        elif strength == "moderate":
            lines.append(
                "Apply a noticeable realistic correction to the body silhouette while keeping the image documentary and non-glamorous."
            )
        else:
            lines.append(
                "Apply a restrained correction while keeping all approved identity characteristics stable."
            )
        return "\n".join(line for line in lines if line and not line.endswith(": ."))

    def _locked_attribute_guidance(self) -> str:
        if not self.config.approved_dir.exists():
            return ""
        locked: dict[str, list[str]] = {}
        for metadata_path in sorted(self.config.approved_dir.glob("*/*.json")):
            try:
                data = json.loads(metadata_path.read_text())
            except json.JSONDecodeError:
                continue
            if data.get("status") != "approved" and not data.get("approved"):
                continue
            attributes = data.get("locked_attributes") or []
            if not attributes:
                continue
            filename = data.get("filename") or metadata_path.with_suffix(".png").name
            locked[filename] = attributes
        if not locked:
            return ""
        lines = [
            "Approved assets define locked character attributes. Treat these as constraints, not suggestions.",
        ]
        for filename, attributes in locked.items():
            attrs = ", ".join(attributes)
            lines.append(f"- {filename}: lock {attrs}.")
        return "\n".join(lines)

    def _performance_guidance(
        self,
        manifest: SessionManifest,
        task: ImageTask,
        warnings: list[str],
    ) -> str:
        if not task.performance:
            return ""
        registry_path = self._performance_registry_path(manifest)
        if not registry_path.exists():
            warnings.append(f"Performance registry missing: {registry_path}")
            return ""
        try:
            registry = json.loads(registry_path.read_text())
        except json.JSONDecodeError as exc:
            warnings.append(f"Performance registry invalid JSON: {registry_path} ({exc})")
            return ""
        performances = registry.get("performances", {})
        performance = performances.get(task.performance)
        if not performance:
            warnings.append(f"Performance not found in registry: {task.performance}")
            return ""
        return "\n".join(
            line
            for line in [
                f"Requested performance: {task.performance}.",
                f"Canonical role: {performance.get('canonical_role', '')}.",
                f"Approved reference asset: {performance.get('asset_id', '')} {performance.get('filename', '')}.",
                performance.get("guidance", ""),
                "Preserve Chloe's approved identity exactly; change only the requested performance state.",
            ]
            if line.strip()
        )

    def _performance_registry_path(self, manifest: SessionManifest) -> Path:
        if manifest.performance_registry_file:
            return resolve_studio_path(self.config, manifest.performance_registry_file)
        return self.config.studio_root / "performance-registry" / "performance_core_v1.json"

    def _style_packs(self, manifest: SessionManifest, task: ImageTask, warnings: list[str]):
        requested = [*manifest.style_packs, *task.style_packs]
        style_names = list(dict.fromkeys(name.strip() for name in requested if name and name.strip()))
        style_packs = []
        for style_name in style_names:
            try:
                style_packs.append(load_style_pack(style_name, self.config.studio_root))
            except (FileNotFoundError, ValueError) as exc:
                warnings.append(str(exc))
        return style_packs

    def _style_pack_guidance(self, style_packs: list) -> str:
        if not style_packs:
            return ""
        blocks = [
            "Style Packs describe visual interpretation only. They must not override Chloe Archive canon, approved identity, body proportions, or story truth unless a session explicitly allows it.",
        ]
        for pack in style_packs:
            blocks.append(
                "\n\n".join(
                    [
                        f"## Style Pack: {pack.name}",
                        pack.style_text,
                        f"Wardrobe:\n{json.dumps(pack.wardrobe, indent=2)}",
                        f"Palette:\n{json.dumps(pack.palette, indent=2)}",
                        f"Lighting:\n{json.dumps(pack.lighting, indent=2)}",
                        f"Camera:\n{json.dumps(pack.camera, indent=2)}",
                    ]
                )
            )
        return "\n\n".join(blocks)

    def _style_pack_negative(self, style_packs: list) -> str:
        blocks = []
        for pack in style_packs:
            if pack.negative_text:
                blocks.append(f"# Style Pack Negative: {pack.name}\n{pack.negative_text}")
        return "\n\n".join(blocks)

    def _audit_markdown(
        self,
        visual_canon: str,
        directives: str,
        style_guidance: str,
        session_description: str,
        task: ImageTask,
        feedback: list[RejectionFeedback],
        body_override: str,
        locked_guidance: str,
        performance_guidance: str,
        style_negative: str,
        final_prompt: str,
        final_negative_prompt: str,
        warnings: list[str],
    ) -> str:
        feedback_text = (
            "\n".join(f"- [{item.rejection_type or 'unspecified'}] {item.reason}" for item in feedback)
            or "_None yet._"
        )
        warnings_text = "\n".join(f"- {warning}" for warning in warnings) or "_None._"
        return "\n\n".join(
            [
                "# Prompt Audit",
                f"## Warnings\n{warnings_text}",
                f"## Canon Text Used\n{visual_canon or '_Not provided._'}",
                f"## Image Directives Used\n{directives or '_Not provided._'}",
                f"## Style Packs Used\n{style_guidance or '_Not requested._'}",
                f"## Style-Specific Negatives\n{style_negative or '_None._'}",
                f"## Locked Attributes\n{locked_guidance or '_None yet._'}",
                f"## Performance Reference\n{performance_guidance or '_Not requested._'}",
                f"## Session Description\n{session_description or '_Not provided._'}",
                f"## Creative Brief\n{task.creative_brief.as_generation_text() if task.creative_brief else task.prompt}",
                f"## Body Specification Override\n{body_override or '_Not provided._'}",
                f"## Prior Rejection Feedback\n{feedback_text}",
                f"## Final Generated Prompt\n{final_prompt}",
                f"## Final Negative Prompt\n{final_negative_prompt or '_Not provided._'}",
            ]
        )
