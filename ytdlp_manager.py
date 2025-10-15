#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility to manage external yt-dlp executable across platforms.

This module downloads and keeps an external yt-dlp binary up to date so the
application does not depend on the embedded Python package version.

It uses only Python standard library.
"""

from __future__ import annotations

import json
import os
import platform
import stat
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional


GITHUB_API_LATEST_RELEASE = (
    "https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest"
)


def _binary_name() -> str:
    """Return platform-specific yt-dlp binary filename."""
    return "yt-dlp.exe" if platform.system() == "Windows" else "yt-dlp"


def _download_url_latest_binary() -> str:
    """Return direct download URL for the latest yt-dlp binary for this OS."""
    # Latest convenience URL maintained by yt-dlp project
    if platform.system() == "Windows":
        return (
            "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
        )
    return "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"


def get_local_version(binary_path: Path) -> Optional[str]:
    """Return local yt-dlp version string or None if unavailable."""
    try:
        completed = subprocess.run(
            [str(binary_path), "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
        version = completed.stdout.strip().splitlines()[0].strip()
        return version or None
    except Exception:
        return None


def get_latest_version_from_api(timeout_sec: int = 5) -> Optional[str]:
    """Query GitHub API for latest release tag. Return tag like '2024.08.06'."""
    try:
        req = urllib.request.Request(GITHUB_API_LATEST_RELEASE, headers={"User-Agent": "yt2d-updater"})
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="ignore"))
            tag = data.get("tag_name") or data.get("name")
            if tag:
                # Normalize v prefix
                return tag.lstrip("v").strip()
    except urllib.error.URLError:
        return None
    except Exception:
        return None
    return None


def _mark_executable(path: Path) -> None:
    """Ensure the binary is executable on POSIX."""
    try:
        if platform.system() != "Windows":
            current_mode = path.stat().st_mode
            path.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    except Exception:
        pass


def download_latest(dest_path: Path, timeout_sec: int = 30) -> bool:
    """Download latest yt-dlp binary to dest_path. Return True on success."""
    url = _download_url_latest_binary()
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(url, timeout=timeout_sec) as resp:
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(resp.read())
                tmp_path = Path(tmp.name)
        tmp_path.replace(dest_path)
        _mark_executable(dest_path)
        return True
    except Exception:
        return False


def ensure_external_ytdlp(base_dir: Path, channel: str = "nightly", auto_update: bool = True, timeout_sec: int = 20) -> Optional[Path]:
    """Ensure an external yt-dlp binary exists and is up to date.

    - The binary is placed in base_dir/_bin/yt-dlp[.exe]
    - If no internet, it will keep existing binary if present
    - Returns the binary path if available after the operation
    """
    bin_dir = base_dir / "_bin"
    binary_path = bin_dir / _binary_name()

    # If binary missing, try download
    if not binary_path.exists():
        if download_latest(binary_path):
            return binary_path
        return binary_path if binary_path.exists() else None

    # Self-update using yt-dlp native updater for selected channel
    if auto_update:
        try:
            update_args = [str(binary_path)]
            if channel:
                update_args += ["--update-to", channel]
            else:
                update_args += ["-U"]
            subprocess.run(update_args, timeout=timeout_sec)
        except Exception:
            # Fallback to remote version check if self-update failed silently
            local_ver = get_local_version(binary_path)
            latest_ver = get_latest_version_from_api()
            if latest_ver and local_ver and local_ver != latest_ver:
                download_latest(binary_path)

    return binary_path if binary_path.exists() else None


def find_or_install_ytdlp(prefer_external_dir: Optional[Path] = None, channel: str = "nightly", auto_update: bool = True) -> Optional[str]:
    """Find yt-dlp executable; install external one if not available.

    Returns a string path to the executable or None if not available.
    """
    # 1) Prefer existing in PATH
    path_in_system = shutil_which("yt-dlp.exe" if platform.system() == "Windows" else "yt-dlp")
    if path_in_system:
        return path_in_system

    # 2) Ensure external
    base_dir = prefer_external_dir or Path.cwd()
    ensured = ensure_external_ytdlp(base_dir, channel=channel, auto_update=auto_update)
    if ensured:
        return str(ensured)
    return None


def shutil_which(cmd: str) -> Optional[str]:
    """Wrapper for shutil.which without importing shutil globally at module import."""
    try:
        import shutil  # local import to keep scope minimal

        return shutil.which(cmd)
    except Exception:
        return None


__all__ = [
    "ensure_external_ytdlp",
    "find_or_install_ytdlp",
    "get_local_version",
    "get_latest_version_from_api",
]


