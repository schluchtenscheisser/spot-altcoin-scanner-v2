from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict

import yaml

CONFIG_PATH = os.getenv("SCANNER_CONFIG_PATH", "config/config.yml")


@dataclass
class ScannerConfig:
  raw: Dict[str, Any]

  @property
  def run_mode(self) -> str:
      return self.raw.get("general", {}).get("run_mode", "standard")


def load_config(path: str | None = None) -> ScannerConfig:
    cfg_path = path or CONFIG_PATH
    with open(cfg_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return ScannerConfig(raw=raw)

