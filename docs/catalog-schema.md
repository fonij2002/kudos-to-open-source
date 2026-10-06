# Catalog schema

## Mapping: `data/alternatives.yml`

A mapping answers: “What open-source project can I evaluate instead of this proprietary product?”

```json
{
  "id": "capcut-kdenlive",
  "category": "video-editing",
  "proprietary": "CapCut",
  "project_id": "kdenlive",
  "note_key": "capcut-kdenlive"
}
```

## Project: `data/projects.yml`

Project metadata is normalized and reused by every mapping.

```yml
{
  "id": "kdenlive",
  "name": "Kdenlive",
  "url": "https://kdenlive.org/",
  "setup_url": "https://kdenlive.org/download/",
  "platforms": ["windows", "macos", "linux"],
  "limitations": ["desktop-focused", "gpu-recommended"],
}
```

`setup_url` should point to the most useful official install/download/quick-start/usage page available. Platform and limitation values are stable keys translated in locale files.
