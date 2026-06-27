from __future__ import annotations

import textwrap
from abc import ABC, abstractmethod
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from frikshun.models import GeneratedImage


class ImageGenerator(ABC):
    generation_model = "abstract"

    @abstractmethod
    def generate(
        self,
        prompt: str,
        negative_prompt: str,
        output_path: Path,
        *,
        asset_id: str,
        session_id: str,
        version: int,
        prompt_audit_path: Path,
    ) -> GeneratedImage:
        ...


class MockImageGenerator(ImageGenerator):
    generation_model = "mock-pillow-placeholder"

    def generate(
        self,
        prompt: str,
        negative_prompt: str,
        output_path: Path,
        *,
        asset_id: str,
        session_id: str,
        version: int,
        prompt_audit_path: Path,
    ) -> GeneratedImage:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image = Image.new("RGB", (1024, 1024), color=(34, 36, 40))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        title = f"{session_id} / {asset_id} / v{version:03d}"
        draw.text((48, 48), title, fill=(255, 255, 255), font=font)
        wrapped = textwrap.wrap(prompt, width=82)[:34]
        draw.text((48, 104), "\n".join(wrapped), fill=(220, 220, 220), font=font)
        if negative_prompt:
            draw.text((48, 900), "Negative: " + negative_prompt[:140], fill=(255, 170, 170), font=font)
        image.save(output_path)
        return GeneratedImage(
            asset_id=asset_id,
            session_id=session_id,
            filename=output_path.name,
            prompt=prompt,
            negative_prompt=negative_prompt,
            generation_model=self.generation_model,
            version=version,
            output_path=output_path,
            metadata_path=output_path.with_suffix(".json"),
            prompt_audit_path=prompt_audit_path,
        )


class OpenAIImageGenerator(ImageGenerator):
    generation_model = "openai-images-todo"

    def generate(
        self,
        prompt: str,
        negative_prompt: str,
        output_path: Path,
        *,
        asset_id: str,
        session_id: str,
        version: int,
        prompt_audit_path: Path,
    ) -> GeneratedImage:
        # TODO: Integrate the OpenAI Images API here.
        # Suggested shape:
        # 1. Send prompt and negative_prompt to the selected model.
        # 2. Decode or download the returned image bytes.
        # 3. Save them to output_path.
        # 4. Return GeneratedImage with the same metadata contract as MockImageGenerator.
        raise NotImplementedError("OpenAI image generation is intentionally left as an integration stub.")
