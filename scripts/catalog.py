from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

MAPPINGS_FILE = DATA / "alternatives.yml"
PROJECTS_FILE = DATA / "projects.yml"
CATEGORIES_FILE = DATA / "categories.yml"
LOCALES_FILE = DATA / "locales.yml"
LOCALES_DIR = DATA / "locales"


def load_yaml(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if data is None:
        raise ValueError(f"YAML file is empty: {path}")

    return data


def load_mappings() -> list[dict]:
    data = load_yaml(MAPPINGS_FILE)

    if not isinstance(data, list):
        raise TypeError("alternatives.yml must contain a YAML list")

    return data


def load_projects() -> list[dict]:
    data = load_yaml(PROJECTS_FILE)

    if not isinstance(data, list):
        raise TypeError("projects.yml must contain a YAML list")

    return data


def load_categories() -> list[str]:
    data = load_yaml(CATEGORIES_FILE)

    if not isinstance(data, list):
        raise TypeError("categories.yml must contain a YAML list")

    return data


def load_locale_codes() -> list[str]:
    data = load_yaml(LOCALES_FILE)

    if not isinstance(data, list):
        raise TypeError("locales.yml must contain a YAML list")

    return data


def load_locale(code: str) -> dict:
    path = LOCALES_DIR / f"{code}.yml"
    data = load_yaml(path)

    if not isinstance(data, dict):
        raise TypeError(f"Locale {code}.yml must contain a YAML mapping")

    return data


def load_locales() -> dict[str, dict]:
    return {code: load_locale(code) for code in load_locale_codes()}


def project_map() -> dict[str, dict]:
    return {project["id"]: project for project in load_projects()}


def enriched_records() -> list[dict]:
    projects = project_map()

    return [
        {
            **mapping,
            **projects[mapping["project_id"]],
        }
        for mapping in load_mappings()
    ]
