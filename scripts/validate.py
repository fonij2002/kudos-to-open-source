from __future__ import annotations

import sys
from urllib.parse import urlparse

from catalog import (
    load_categories,
    load_locale_codes,
    load_locales,
    load_mappings,
    load_projects,
)

mappings = load_mappings()
projects = load_projects()
categories = load_categories()
locale_codes = load_locale_codes()
locales = load_locales()

errors: list[str] = []


def valid_https(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


if not locale_codes or "en" not in locale_codes:
    errors.append("locales.json must include the English fallback locale 'en'")
if len(categories) != len(set(categories)):
    errors.append("categories.json contains duplicate category IDs")

# Locale structure must be consistent, which makes adding a language predictable.
en = locales.get("en", {})
required_sections = {"meta", "ui", "categories", "platforms", "limitations", "notes"}
for code, locale in locales.items():
    missing = required_sections - set(locale)
    if missing:
        errors.append(f"locale {code}: missing sections {sorted(missing)}")
        continue
    if locale["meta"].get("code") != code:
        errors.append(f"locale {code}: meta.code must equal {code!r}")
    if locale["meta"].get("direction") not in {"ltr", "rtl"}:
        errors.append(f"locale {code}: direction must be ltr or rtl")
    if en:
        if set(locale["ui"]) != set(en["ui"]):
            errors.append(f"locale {code}: UI translation keys differ from English")
        if set(locale["categories"]) != set(categories):
            errors.append(
                f"locale {code}: category translations must exactly match categories.json"
            )

project_ids: set[str] = set()
project_names: set[str] = set()
used_platforms: set[str] = set()
used_limits: set[str] = set()
project_by_id: dict[str, dict] = {}
project_required = {
    "id",
    "name",
    "url",
    "setup_url",
    "platforms",
    "limitations",
}

for i, project in enumerate(projects, 1):
    missing = project_required - set(project)
    if missing:
        errors.append(f"project {i}: missing {sorted(missing)}")
        continue
    pid = str(project["id"]).strip()
    name = str(project["name"]).strip()
    if not pid or pid in project_ids:
        errors.append(f"project {i}: duplicate/empty id {pid!r}")
    if not name or name.casefold() in project_names:
        errors.append(f"project {i}: duplicate/empty name {name!r}")
    project_ids.add(pid)
    project_names.add(name.casefold())
    project_by_id[pid] = project

    if not valid_https(project["url"]):
        errors.append(f"project {pid}: invalid project URL {project['url']}")
    if not valid_https(project["setup_url"]):
        errors.append(f"project {pid}: invalid setup URL {project['setup_url']}")
    if not isinstance(project["platforms"], list) or not project["platforms"]:
        errors.append(f"project {pid}: at least one platform is required")
    if not isinstance(project["limitations"], list) or not project["limitations"]:
        errors.append(
            f"project {pid}: at least one limitation/constraint tag is required"
        )
    used_platforms.update(project["platforms"])
    used_limits.update(project["limitations"])

mapping_required = {"id", "category", "proprietary", "project_id", "note_key"}
seen_ids: set[str] = set()
seen_pairs: set[tuple[str, str]] = set()
used_categories: set[str] = set()
note_keys: set[str] = set()

for i, mapping in enumerate(mappings, 1):
    missing = mapping_required - set(mapping)
    if missing:
        errors.append(f"mapping {i}: missing {sorted(missing)}")
        continue
    mid = mapping["id"]
    if mid in seen_ids:
        errors.append(f"mapping {i}: duplicate id {mid}")
    seen_ids.add(mid)
    if mapping["note_key"] != mid:
        errors.append(f"mapping {mid}: note_key should equal mapping id")
    note_keys.add(mapping["note_key"])

    if mapping["category"] not in categories:
        errors.append(f"mapping {mid}: unknown category {mapping['category']}")
    used_categories.add(mapping["category"])
    if mapping["project_id"] not in project_by_id:
        errors.append(f"mapping {mid}: unknown project_id {mapping['project_id']}")
        continue
    if not str(mapping["proprietary"]).strip():
        errors.append(f"mapping {mid}: empty proprietary product")
    pair = (mapping["proprietary"].strip().casefold(), mapping["project_id"])
    if pair in seen_pairs:
        errors.append(f"mapping {mid}: duplicate proprietary/project mapping")
    seen_pairs.add(pair)

unused_categories = set(categories) - used_categories
if unused_categories:
    errors.append(f"unused categories: {sorted(unused_categories)}")

for code, locale in locales.items():
    missing_platforms = used_platforms - set(locale.get("platforms", {}))
    missing_limits = used_limits - set(locale.get("limitations", {}))
    missing_notes = note_keys - set(locale.get("notes", {}))
    extra_notes = set(locale.get("notes", {})) - note_keys
    if missing_platforms:
        errors.append(
            f"locale {code}: missing platform labels {sorted(missing_platforms)}"
        )
    if missing_limits:
        errors.append(
            f"locale {code}: missing limitation labels {sorted(missing_limits)}"
        )
    if missing_notes:
        errors.append(
            f"locale {code}: missing notes {sorted(missing_notes)[:5]}{'…' if len(missing_notes)>5 else ''}"
        )
    if extra_notes:
        errors.append(
            f"locale {code}: stale/extra notes {sorted(extra_notes)[:5]}{'…' if len(extra_notes)>5 else ''}"
        )

if errors:
    print("\n".join(errors))
    sys.exit(1)

print(
    f"OK: {len(mappings)} mappings, {len(projects)} projects, "
    f"{len(categories)} categories, {len(locales)} locales validated."
)
