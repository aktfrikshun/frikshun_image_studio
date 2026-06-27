from __future__ import annotations

import os
from pathlib import Path

import streamlit as st

from frikshun.generator import MockImageGenerator
from frikshun.review_store import ReviewStore
from frikshun.session_loader import StudioConfig, resolve_studio_root


def _store() -> ReviewStore:
    root = resolve_studio_root(Path(os.environ["FRIKSHUN_STUDIO_ROOT"]) if os.getenv("FRIKSHUN_STUDIO_ROOT") else None)
    return ReviewStore(StudioConfig(studio_root=root))


def main() -> None:
    st.set_page_config(page_title="FrikShun Image Studio", layout="wide")
    st.title("FrikShun Image Studio")
    store = _store()

    manifests = sorted(store.config.sessions_dir.glob("**/*.y*ml"))
    selected = st.selectbox("Session manifest", manifests, format_func=lambda path: str(path.relative_to(store.config.studio_root)))
    manifest = store.load_manifest(selected) if selected else None

    if manifest and st.button("Generate pending assets"):
        created = store.generate_session(manifest, MockImageGenerator())
        st.success(f"Generated {len(created)} candidate image(s).")

    if not manifest:
        st.info("Create or select a session manifest to begin.")
        return

    st.caption(f"Studio root: {store.config.studio_root}")
    candidates = store.candidates(manifest.session_id)
    if not candidates:
        st.info("No candidate images are waiting for review.")
        return

    cols = st.columns(3)
    for index, image in enumerate(candidates):
        with cols[index % 3]:
            st.image(str(image.output_path), caption=f"{image.asset_id} v{image.version:03d}")
            with st.expander("Metadata and creative brief"):
                st.json(image.model_dump(mode="json"))
                st.code(image.prompt)
            if image.style_packs:
                with st.expander("Style Packs"):
                    st.write(", ".join(image.style_packs))
                    for pack_name in image.style_packs:
                        summary = image.style_pack_summaries.get(pack_name, {})
                        st.markdown(f"### {pack_name}")
                        style_text = summary.get("style_text") or ""
                        if style_text:
                            st.markdown(style_text)
                        wardrobe = summary.get("wardrobe") or {}
                        lighting = summary.get("lighting") or {}
                        negative = summary.get("negative_text") or ""
                        if wardrobe:
                            st.markdown("**Wardrobe**")
                            st.json(wardrobe)
                        if lighting:
                            st.markdown("**Lighting**")
                            st.json(lighting)
                        if negative:
                            st.markdown("**Negative Style Notes**")
                            st.write(negative)
            reason_key = f"reason_{image.metadata_path}"
            rejection_type_key = f"rejection_type_{image.metadata_path}"
            identity_score_key = f"identity_score_{image.metadata_path}"
            canon_confidence_key = f"canon_confidence_{image.metadata_path}"
            appearance_score_key = f"appearance_score_{image.metadata_path}"
            expression_score_key = f"expression_score_{image.metadata_path}"
            technical_score_key = f"technical_score_{image.metadata_path}"
            continuity_score_key = f"continuity_score_{image.metadata_path}"
            model_status_key = f"model_status_{image.metadata_path}"
            notes_key = f"notes_{image.metadata_path}"
            st.selectbox(
                "Rejection type",
                [
                    "technical",
                    "identity_drift",
                    "canon_refinement",
                    "anatomy",
                    "wardrobe",
                    "expression",
                    "lighting",
                    "composition",
                ],
                key=rejection_type_key,
            )
            st.text_area("Rejection reason", key=reason_key)
            st.number_input("Identity score", min_value=0.0, max_value=10.0, value=9.0, step=0.1, key=identity_score_key)
            st.number_input("Canon confidence", min_value=0.0, max_value=10.0, value=9.0, step=0.1, key=canon_confidence_key)
            st.number_input("Appearance score", min_value=0.0, max_value=10.0, value=9.0, step=0.1, key=appearance_score_key)
            st.number_input("Expression score", min_value=0.0, max_value=10.0, value=9.0, step=0.1, key=expression_score_key)
            st.number_input("Technical score", min_value=0.0, max_value=10.0, value=9.0, step=0.1, key=technical_score_key)
            st.number_input("Continuity score", min_value=0.0, max_value=10.0, value=9.0, step=0.1, key=continuity_score_key)
            st.text_input("Model status", value="identity_core", key=model_status_key)
            st.text_area("Approval notes", key=notes_key)
            approve_col, reject_col, regen_col = st.columns(3)
            if approve_col.button("Approve", key=f"approve_{image.metadata_path}"):
                store.approve(
                    image.metadata_path,
                    identity_score=st.session_state.get(identity_score_key),
                    canon_confidence=st.session_state.get(canon_confidence_key),
                    appearance_score=st.session_state.get(appearance_score_key),
                    expression_score=st.session_state.get(expression_score_key),
                    technical_score=st.session_state.get(technical_score_key),
                    continuity_score=st.session_state.get(continuity_score_key),
                    model_status=st.session_state.get(model_status_key, ""),
                    notes=st.session_state.get(notes_key, ""),
                )
                st.rerun()
            if reject_col.button("Reject", key=f"reject_{image.metadata_path}"):
                reason = st.session_state.get(reason_key, "")
                rejection_type = st.session_state.get(rejection_type_key, "")
                try:
                    store.reject(image.metadata_path, reason, rejection_type)
                    st.rerun()
                except ValueError as exc:
                    st.error(str(exc))
            if regen_col.button("Regenerate", key=f"regen_{image.metadata_path}"):
                store.regenerate(manifest, image.asset_id, MockImageGenerator())
                st.rerun()


if __name__ == "__main__":
    main()
