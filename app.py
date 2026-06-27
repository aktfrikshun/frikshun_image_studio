from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional

import typer

from frikshun.generator import MockImageGenerator
from frikshun.review_store import ReviewStore
from frikshun.session_loader import StudioConfig, create_session_manifest, resolve_studio_root

app = typer.Typer(help="FrikShun Image Studio local image pipeline.")


def _config(studio_root: Optional[Path]) -> StudioConfig:
    return StudioConfig(studio_root=resolve_studio_root(studio_root))


@app.callback()
def main(
    ctx: typer.Context,
    studio_root: Optional[Path] = typer.Option(
        None,
        "--studio-root",
        help="Studio root. Overrides FRIKSHUN_STUDIO_ROOT and frikshun_image_studio.yaml.",
    ),
) -> None:
    ctx.obj = _config(studio_root)


@app.command("create-session")
def create_session(
    ctx: typer.Context,
    name: str = typer.Option(..., "--name", help="Session id/name, e.g. 001_identity_lock."),
    character: str = typer.Option("Unnamed Artist", "--character"),
    description: str = typer.Option("", "--description"),
) -> None:
    """Create a starter YAML session manifest."""
    config: StudioConfig = ctx.obj
    path = create_session_manifest(config, name, character, description)
    typer.echo(f"Created session manifest: {path}")


@app.command()
def generate(
    ctx: typer.Context,
    session: Path = typer.Option(..., "--session", "-s", help="Path or studio-root-relative session YAML."),
) -> None:
    """Generate mock candidates for all pending/candidate tasks in a session."""
    config: StudioConfig = ctx.obj
    store = ReviewStore(config)
    manifest = store.load_manifest(session)
    generator = MockImageGenerator()
    created = store.generate_session(manifest, generator)
    for image in created:
        typer.echo(f"Generated {image.output_path}")
    if not created:
        typer.echo("No pending tasks found.")


@app.command()
def regenerate(
    ctx: typer.Context,
    session: str = typer.Option(..., "--session", "-s", help="Session id or manifest path."),
    asset: str = typer.Option(..., "--asset", "-a", help="Asset id to regenerate."),
) -> None:
    """Regenerate one asset using accumulated rejection feedback."""
    config: StudioConfig = ctx.obj
    store = ReviewStore(config)
    manifest = store.load_manifest(session)
    generated = store.regenerate(manifest, asset, MockImageGenerator())
    typer.echo(f"Generated {generated.output_path}")


@app.command()
def review(ctx: typer.Context) -> None:
    """Launch the Streamlit review UI."""
    from streamlit.web import cli as stcli

    config: StudioConfig = ctx.obj
    os.environ["FRIKSHUN_STUDIO_ROOT"] = str(config.studio_root)
    sys.argv = [
        "streamlit",
        "run",
        str(Path(__file__).parent / "frikshun" / "ui.py"),
        "--server.headless=true",
    ]
    stcli.main()


if __name__ == "__main__":
    app()
