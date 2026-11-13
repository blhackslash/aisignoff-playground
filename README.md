# aisignoff playground

Files and lines ([folder report](https://blhackslash.github.io/aisignoff-playground/)):
[![AI generation (files)](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/blhackslash/aisignoff-playground/badges/aisignoff-generation.json)](https://blhackslash.github.io/aisignoff-playground/)
[![Human review (files)](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/blhackslash/aisignoff-playground/badges/aisignoff-human-review.json)](https://blhackslash.github.io/aisignoff-playground/)
[![AI review (files)](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/blhackslash/aisignoff-playground/badges/aisignoff-ai-review.json)](https://blhackslash.github.io/aisignoff-playground/)

Merged pull requests:
[![AI generation](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/blhackslash/aisignoff-playground/badges/ai-generation.json)](https://github.com/industrial-mathematics-group/.github/blob/main/.github/CONTRIBUTING.md#g-generation)
[![Human review](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/blhackslash/aisignoff-playground/badges/ai-human-review.json)](https://github.com/industrial-mathematics-group/.github/blob/main/.github/CONTRIBUTING.md#h-human-review)
[![AI review](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/blhackslash/aisignoff-playground/badges/ai-review.json)](https://github.com/industrial-mathematics-group/.github/blob/main/.github/CONTRIBUTING.md#a-ai-review)

A throwaway repository for trying [aisignoff](https://github.com/industrial-mathematics-group/aisignoff) on GitHub: a small dummy Python package, results and a script, declared with the setup the aisignoff docs recommend.

## What's in it

| Path | Declared as | How |
|---|---|---|
| everything (`**`) | G0 · H2 · A0, by Pascal Jung | default annotation in `SIGNOFF.toml` |
| `src/playground/fitting.py` | G2 · H1 · A1, Claude Opus | annotation |
| `results/**` | G3 · H1 · A2, Claude Opus | annotation (folder) |
| `scripts/make_results.py` | G1 · H2 · A1, Claude Opus | inline tags in the file |

`SIGNOFF.toml` also turns on line-level declarations (`[history]`, `merge-method = "merge"`) and a policy: every file needs at least H1, G3 needs A2.

| File | What it does |
|---|---|
| `.github/workflows/signoff.yml`, job `lint` | `aisignoff lint` on pushes to main, pull requests and merge queues, plus the pull request description check; folder tree in the job summary, folder report as an artifact. Installs `aisignoff==0.14.0` from PyPI |
| `.github/workflows/pr-signoff.yml` | The organisation's PR-signoff check: validates the ticked template, sets `ai:G*` / `human:H*` / `ai-review:A*` labels |
| `.github/pull_request_template.md` | The organisation's template, with the responsibility, model and review-level boxes |
| `.github/workflows/signoff.yml`, job `badges` | On pushes to main: `aisignoff badge` writes the three file badges (top row above) and commits them to the `badges` branch |
| `.github/workflows/signoff-badges.yml` | The organisation's Signoff-Badges workflow: badges of the declarations of merged pull requests (second row), on the same `badges` branch |
| `.github/workflows/signoff-pages.yml` | On pushes to main: publishes the interactive folder report, with the text of each file, to GitHub Pages |
| `extras/workflows/` | Optional workflows to copy into `.github/workflows/`: the PR diff and PR files summaries, the organisation's File-signoff caller |

## Setup on GitHub

1. Create an empty repository and push: `git remote add origin <url> && git push -u origin main`.
2. *Settings → General → Pull Requests*: allow merge commits (and squash, for scenario 5), and set the default commit message of both to **Pull request title and description**. Without this the declaration never reaches git.
3. *Settings → Rules → Rulesets* (or *Branches*), for `main`: require a pull request, and require the checks **`aisignoff / lint`** and **`pr-signoff / check`**. Leave direct pushes allowed for yourself if you want to try scenario 1 after this.
4. Check the first run under *Actions*: `aisignoff / lint` should be green, and its summary should show the folder tree.
5. *Settings → Pages → Build and deployment → Source*: **GitHub Actions**. The report is then at <https://blhackslash.github.io/aisignoff-playground/> after the next push to main (or *Actions → aisignoff report on Pages → Run workflow*).
6. The badges branch is created by the first push to main after this. The pull request badges show "no declarations yet" until a declared pull request is merged. Don't protect `badges` against pushes by github-actions[bot].

Locally: `pipx install aisignoff==0.14.0`, then `aisignoff lint`, `aisignoff report --files` (with `[history]`, files with mixed lines show the share of each declaration), `aisignoff diff HEAD^1 --files` (the levels of the lines a commit added) and `aisignoff report --json` (every line run with its source).

## Scenarios

Each one says what should happen. In pull requests, fill the template by ticking boxes: generation (exactly one), models, human review, AI review.

### 1. Plain push to main

Edit `docs/notes.md`, commit with a plain message, push to `main`.
**Expect:** lint green. The new lines declare nothing, so they take the file-level declaration (G0 · H2 · A0). `aisignoff report --files` is unchanged.

Variant: commit with "Key: value" lines in the message (`AI-Generation: G2`, `Assisted-by: …`, `Human-Review: H1`, `Reviewed-by: …`, `AI-Review: A1`, `AI-Reviewed-by: …`). **Expect:** `aisignoff report --files` shows `docs/notes.md` partly at G2.

### 2. Pull request into main

Branch, change `src/playground/stats.py`, open a pull request into `main`.

- With the template untouched: **expect** `aisignoff / lint` and `pr-signoff / check` to fail (unfilled template, `TODO`).
- Tick G2, Claude Opus, H1, A1: both turn green after the edit, without a new push (the description check reruns on `edited`).
- Tick only H0: **expect** a policy failure (H1 is required).
- Tick G1 and G2 together: **expect** an error (more than one generation box).

Merge it on GitHub with a merge commit. **Expect:** on `main`, `aisignoff report --files` shows `stats.py` as mostly G0 · H2 · A0 plus a share at the ticked levels, and `aisignoff diff HEAD^1 --files` shows the added lines at G2 · H1 · A1. Their reviewer is the merge commit's author, i.e. whoever clicked *Merge*.

### 3. Stacked pull requests

Branch `a` from `main`, branch `b` from `a`. Open PR A (`a` → `main`) and PR B (`b` → `a`).
**Expect:** PR B's description isn't checked by aisignoff (it doesn't go into the default branch), and PR-signoff only checks PRs into `main`. Merge B into A, then A into `main`: A's description declares all the lines, B's included.

Variant: merge A first, let GitHub retarget B to `main`, then merge B. **Expect:** B's description now counts, for the lines B's merge brings in.

### 4. Something undeclared

Change the `results/**` annotation to `AI-Review = "A1"`. **Expect:** lint fails with a policy error (G3 needs A2). Or add an annotation for a path that doesn't exist: lint passes but warns (`lint --strict` would fail). Or delete the inline tags from `scripts/make_results.py`: it falls back to the `**` default.

### 5. Squash merge

Set `merge-method = "squash"` in `SIGNOFF.toml` (land that first), then open a PR with a few commits, some of them with `AI-Generation: G3` in their messages, and squash-merge it.
**Expect:** the squash commit's description declares all its lines; the branch commits' generation is ignored. With `merge-method = "merge"` and a merge commit instead, a branch commit with `AI-Generation: G3` raises the generation of the lines it wrote.

### 6. Freeze

Once a few PRs have landed, take a snapshot:

```bash
git switch --detach origin/main
aisignoff freeze --prune
git switch -c freeze
git add SIGNOFF.snapshot.json SIGNOFF.toml && git commit -m "Freeze the declarations"
git push -u origin freeze      # and open a PR (tick G0 / H2 / A0, or "Key: value" lines)
```

**Expect:** lint in the PR checks the snapshot by working it out again (green). Then try:

- Edit a level in `SIGNOFF.snapshot.json` by hand and push: **expect** lint to fail.
- After the freeze has landed, change the `**` annotation: frozen lines keep their levels (`aisignoff report --files` unchanged). `aisignoff freeze --reset docs/notes.md` on `main` applies it to that file.
- `aisignoff freeze --check` runs the snapshot check on its own.

### 7. Merge queue (optional)

Turn on the merge queue in the ruleset. **Expect:** the `merge_group` run says it checks `HEAD` as landed, and fails if the description was left unfilled.

## Updating aisignoff

The version is pinned in `AISIGNOFF_VERSION` in `.github/workflows/signoff.yml`. Raise it in `signoff.yml`, `signoff-pages.yml` and `extras/workflows/`, and in your local install together: a snapshot written by another version than CI's can fail the check.
