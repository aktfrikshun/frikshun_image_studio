from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

ImageStatus = Literal["pending", "candidate", "approved", "rejected"]
RejectionType = Literal[
    "",
    "technical",
    "identity_drift",
    "canon_refinement",
    "anatomy",
    "wardrobe",
    "expression",
    "lighting",
    "composition",
]


class CreativeBrief(BaseModel):
    asset_id: str = ""
    purpose: str = ""
    success_criteria: str = ""
    generation_guidance: str = ""
    review_focus: str = ""

    def as_generation_text(self) -> str:
        parts = [
            ("Asset ID", self.asset_id),
            ("Purpose", self.purpose),
            ("Success Criteria", self.success_criteria),
            ("Generation Guidance", self.generation_guidance),
            ("Review Focus", self.review_focus),
        ]
        return "\n".join(f"{label}: {value}" for label, value in parts if value.strip())


class ImageTask(BaseModel):
    id: str
    filename: str
    purpose: str = ""
    prompt: str = ""
    performance: Optional[str] = None
    style_pack: Optional[str] = None
    style_packs: List[str] = Field(default_factory=list)
    creative_brief: Optional[CreativeBrief] = None
    status: ImageStatus = "pending"

    @model_validator(mode="after")
    def ensure_creative_brief(self) -> "ImageTask":
        if self.style_pack and self.style_pack not in self.style_packs:
            self.style_packs.insert(0, self.style_pack)
        if self.creative_brief is None:
            self.creative_brief = CreativeBrief(
                asset_id=self.id,
                purpose=self.purpose,
                generation_guidance=self.prompt,
            )
        if not self.creative_brief.asset_id:
            self.creative_brief.asset_id = self.id
        if not self.purpose and self.creative_brief.purpose:
            self.purpose = self.creative_brief.purpose
        if not self.prompt and self.creative_brief.generation_guidance:
            self.prompt = self.creative_brief.generation_guidance
        return self


class SessionManifest(BaseModel):
    session_id: str
    character: str
    description: str = ""
    base_prompt_file: Optional[str] = None
    negative_prompt_file: Optional[str] = None
    visual_canon_file: Optional[str] = None
    image_directives_file: Optional[str] = None
    negative_canon_file: Optional[str] = None
    performance_registry_file: Optional[str] = None
    style_pack: Optional[str] = None
    style_packs: List[str] = Field(default_factory=list)
    body_profile: Dict[str, Dict[str, str]] = Field(default_factory=dict)
    images: list[ImageTask] = Field(default_factory=list)

    @model_validator(mode="after")
    def normalize_style_packs(self) -> "SessionManifest":
        if self.style_pack and self.style_pack not in self.style_packs:
            self.style_packs.insert(0, self.style_pack)
        return self


class StylePack(BaseModel):
    name: str
    path: Path
    style_text: str = ""
    wardrobe: Dict[str, Any] = Field(default_factory=dict)
    palette: Dict[str, Any] = Field(default_factory=dict)
    lighting: Dict[str, Any] = Field(default_factory=dict)
    camera: Dict[str, Any] = Field(default_factory=dict)
    negative_text: str = ""


class GeneratedImage(BaseModel):
    model_config = ConfigDict(extra="allow")

    asset_id: str
    session_id: str
    filename: str
    prompt: str
    negative_prompt: str = ""
    style_packs: List[str] = Field(default_factory=list)
    style_pack_summaries: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    generation_model: str
    status: Literal["candidate", "approved", "rejected"] = "candidate"
    rejection_type: RejectionType = ""
    rejection_reason: str = ""
    identity_score: Optional[float] = None
    canon_confidence: Optional[float] = None
    appearance_score: Optional[float] = None
    expression_score: Optional[float] = None
    technical_score: Optional[float] = None
    continuity_score: Optional[float] = None
    reference_score: Optional[float] = None
    reference_priority: str = ""
    canonical_name: str = ""
    canonical_role: str = ""
    model_status: str = ""
    approved: bool = False
    notes: str = ""
    measurement_notes: Dict[str, str] = Field(default_factory=dict)
    locked_attributes: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    version: int = 1
    output_path: Path
    metadata_path: Path
    prompt_audit_path: Path


class ReviewDecision(BaseModel):
    asset_id: str
    session_id: str
    decision: Literal["approved", "rejected"]
    rejection_type: RejectionType = ""
    rejection_reason: str = ""
    identity_score: Optional[float] = None
    canon_confidence: Optional[float] = None
    appearance_score: Optional[float] = None
    expression_score: Optional[float] = None
    technical_score: Optional[float] = None
    continuity_score: Optional[float] = None
    reference_score: Optional[float] = None
    reference_priority: str = ""
    canonical_name: str = ""
    canonical_role: str = ""
    model_status: str = ""
    approved: bool = False
    notes: str = ""
    measurement_notes: Dict[str, str] = Field(default_factory=dict)
    locked_attributes: List[str] = Field(default_factory=list)
    decided_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
