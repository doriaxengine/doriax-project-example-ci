# Doriax Project Example CI

Reusable workflow that builds a [Doriax Engine](https://github.com/doriaxengine/doriax)
project for Linux, Windows, macOS and the web, and deploys the web build to
GitHub Pages.

## Usage

`.github/workflows/build-artifacts.yml`:

```yaml
name: Build Artifacts

on:
  push:
  pull_request:
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    uses: doriaxengine/doriax-project-example-ci/.github/workflows/build-project.yml@v3
    with:
      title: Tappy Plane
      subtitle: Tap, click, or press space to keep the plane in the air.
      controls: |
        Flap [Space] [↑] or click / tap
```

Set **Settings > Pages > Source** to **GitHub Actions** in the project repository.

| Input | Description |
| --- | --- |
| `title` | Page title. Required. |
| `subtitle` | Text under the title. |
| `description` | Meta description, defaults to the subtitle. |
| `controls` | One group per line. `[Key]` is shown as a key, the rest as labels. |

Desktop builds are uploaded as `<AppName>-<platform>` artifacts and kept for
90 days. Pages is deployed from the default branch only.

Add the repository to the [nightly.link](https://nightly.link) GitHub App
installation so the page's download links work.

## Web page

`web/shell.html` is the page template. The game stage uses `canvasWidth` and
`canvasHeight` from `project.yaml`, and the page links back to the calling
repository. Project Settings > Web in the editor doesn't apply to this page.

The Download section below the game links to the Windows, Linux and macOS
artifacts of the latest successful run on the default branch, through
nightly.link, since GitHub only serves artifacts to signed-in users. A branch
with no successful run in 90 days has no builds to serve, so run the workflow again.

On narrow screens and touch devices, the bar below the game shows source-code and
fullscreen icons with 44-pixel tap targets. Keyboard hints remain visible on desktop.
The fullscreen action is shown only when the browser supports it.

Preview a page locally:

```sh
TITLE="Tappy Plane" SOURCE_URL=https://github.com/doriaxengine/tappyplane \
  DOWNLOAD_URL=https://nightly.link/doriaxengine/tappyplane/workflows/build-artifacts.yml/main \
  APP_NAME=TappyPlane python3 web/render_shell.py ../tappyplane/project.yaml /tmp/shell.html
```

## Releases

Callers use `@v3`. Move the tag after compatible changes:

```sh
git tag -f v3 && git push -f origin v3
```

Tests: `python3 -m unittest discover`
