# Static website

The GitHub Pages site is a dependency-free static frontend generated from the same catalog as the Markdown pages.

## Architecture

```text
data/alternatives.yml ─┐
data/projects.yml     ──┼── scripts/build_site.py ──→ dist/
data/categories.json  ──┤                              ├── index.html
data/locales/*.json   ──┘                              ├── catalog.v2.json
                                                        ├── catalog.json (v1 compatibility)
                                                        ├── locales/*.json
website/ ───────────────────────────────────────────────└── assets/app.<hash>.js, styles.<hash>.css
```

`dist/` is generated and should not be edited or committed.

## Build locally

```bash
python scripts/validate.py
python scripts/build_site.py
python -m http.server 8000 --directory dist
```

Then open `http://localhost:8000`.

## Features

- English/Persian language switch with persistent preference and shareable `?lang=fa` URLs;
- automatic `dir=ltr` / `dir=rtl`;
- instant client-side search across project/product names, translated notes, categories, platforms, limitation tags, and licenses;
- alphabetically sorted localized category and platform filters;
- category, platform, licensing-model, and fit filters;
- direct install/use links on every project card;
- visible platform and “things to know” tags;
- relevance and alphabetical sorting;
- responsive mobile/desktop layout and light/dark themes;
- keyboard shortcut: `/` focuses search;
- no runtime framework, package manager, analytics, cookies, or backend.

## GitHub Pages

`.github/workflows/pages.yml` validates the catalog, builds `dist/`, uploads it as a Pages artifact, and deploys it.

In **Settings → Pages**, set **Source** to **GitHub Actions**. Pushes to `main` that affect catalog/frontend/build files then publish automatically.

## Cache-safe deployments

The Pages build fingerprints `app.js` and `styles.css` with a content hash and exposes the current data schema as `catalog.v2.json`. The page also includes a build ID on locale/catalog requests. This prevents a browser or the GitHub Pages CDN from combining JavaScript/CSS from one release with catalog data from another.

For backward compatibility, `catalog.json` is still generated in the original v1 shape. Cached copies of the pre-i18n JavaScript can therefore render correctly while they age out instead of showing blank project/category fields. New frontend code must use the explicitly versioned catalog (`catalog.v2.json` or a later schema version) when a breaking data-schema change is introduced.
