"""Seeding and run provenance.

Neither reproduced paper reports a seed protocol or error bars, so every number
we publish must carry its own seed and config record. See §9 of AGENT.md.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import platform
import random
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


def set_seed(seed: int, deterministic: bool = True) -> None:
    """Seed every RNG we use. Call once, before anything else touches randomness."""
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)

    try:
        import torch
    except ImportError:
        return

    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    if deterministic:
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def git_commit() -> str | None:
    """Current commit hash, or None if this is not a git repo / git is absent."""
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def git_dirty() -> bool | None:
    """True if the working tree has uncommitted changes."""
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return bool(out.stdout.strip()) if out.returncode == 0 else None


def config_hash(config: dict[str, Any]) -> str:
    """Stable short hash of a config, so runs can be grouped without trusting names."""
    blob = json.dumps(config, sort_keys=True, default=str).encode()
    return hashlib.sha256(blob).hexdigest()[:12]


@dataclasses.dataclass
class RunRecord:
    """Everything AGENT.md §9 requires us to save alongside a result."""

    track: str
    algorithm: str
    seed: int
    config: dict[str, Any]
    paper_doi: str | None = None
    simulator_version: str | None = None
    n_uavs: int | None = None
    training_steps: int | None = None
    checkpoint: str | None = None
    notes: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d = dataclasses.asdict(self)
        d["config_hash"] = config_hash(self.config)
        d["git_commit"] = git_commit()
        d["git_dirty"] = git_dirty()
        d["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
        d["python"] = sys.version.split()[0]
        d["platform"] = platform.platform()
        try:
            import torch
            d["torch"] = torch.__version__
            d["cuda"] = torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
        except ImportError:
            d["torch"] = None
            d["cuda"] = None
        return d

    def save(self, directory: str | Path, filename: str = "run.json") -> Path:
        """Write the record. Refuses to overwrite: raw results are append-only."""
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / filename
        if path.exists():
            raise FileExistsError(
                f"{path} already exists. Raw results are never overwritten "
                f"(AGENT.md §15) — use a new run directory."
            )
        path.write_text(json.dumps(self.to_dict(), indent=2, default=str), encoding="utf-8")
        return path


def run_dir(root: str | Path, track: str, algorithm: str, seed: int) -> Path:
    """results/raw/<track>/<algorithm>/seed<N>_<timestamp>, guaranteed fresh."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return Path(root) / "raw" / track / algorithm / f"seed{seed}_{stamp}"
