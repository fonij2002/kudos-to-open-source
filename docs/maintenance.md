# Maintenance guide

## Monthly

- Review open pull requests and requested additions.
- Review broken links reported by the scheduled link checker, especially `setup_url` installation links.
- Review projects reported as archived, renamed, or relicensed.
- Correct platform tags when upstream support changes.

## Quarterly

- Re-check all `open-core` / mixed-license entries.
- Review fast-moving categories such as AI/LLM tooling, developer tooling, hosting, analytics, and self-hosted apps.
- Re-check limitation tags for projects whose deployment model changed.
- Remove mappings that no longer represent a useful alternative.

## Translation maintenance

`python scripts/validate.py` requires every enabled locale to cover every category, platform key, limitation key, and mapping note. Adding a catalog item without updating translations should fail CI rather than silently ship a half-translated UI.

## Design principle

`data/alternatives.yml` is the source of truth for mappings, `data/projects.yml` is the source of truth for project/runtime metadata, and `data/locales/*.json` is the source of truth for translated text. Generated category READMEs and `dist/` should never be edited directly.
