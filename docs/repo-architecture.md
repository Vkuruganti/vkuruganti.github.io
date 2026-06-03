# Repo Architecture

Generated: 2026-05-01 13:55:07 PDT

This repository is a small static GitHub Pages portfolio site. The public site is served from the `docs/` directory and does not require a build step, package manager, backend service, or framework.

## Runtime Flow

1. A browser requests `docs/index.html` from GitHub Pages.
2. `index.html` loads the page shell, embedded CSS, and client-side rendering script.
3. The script fetches `./content.json`.
4. `content.json` supplies site metadata, navigation, theme values, hero content, work sections, writing links, contact links, and analytics configuration.
5. The rendering script injects the content into predefined section roots in the page.
6. Static assets such as `docs/assets/image.jpg` and Markdown publication pages are served directly by GitHub Pages.

## Main Components

- `docs/index.html`: Static application shell, CSS, rendering functions, content loader, and optional analytics loader.
- `docs/content.json`: Primary content and configuration source for the portfolio page.
- `docs/assets/image.jpg`: Hero/profile image asset.
- `docs/publications/index.md`: Publications landing page linked from the main navigation.

## Deployment Model

GitHub Pages serves the `docs/` folder as static content. The homepage remains dynamic only in the browser: there is no server-side rendering, database, or API dependency. Updating most site copy only requires editing `docs/content.json`; adding long-form publication content can be done with Markdown files under `docs/publications/`.
