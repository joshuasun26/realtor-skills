# Skill Atlas

A single-file viewer for the skills in this repo. Force-directed graph clustered by
department, sidebar index, full-text search, and the rendered SKILL.md in the right panel.

## Rebuild it

```
python atlas/build.py
```

That walks `plugins/realtor-skills/skills/`, parses every `SKILL.md`, works out which
skills reference which, and rewrites `atlas/index.html`.

**Rerun it after adding or editing any skill.** The page is a build artifact — nothing in
it reads the repo at view time.

## Auto-rebuild

Two mechanisms keep this from relying on someone remembering to run the command above.

**1. A pre-commit hook (local, works today).** `.githooks/pre-commit` reruns
`atlas/build.py` before every commit and re-stages `atlas/index.html` if it changed. It
is repo-relative on purpose: this folder currently lives inside the `business-ops` git
repo (not as its own repo), and a hook installed the normal way — into `.git/hooks/` —
would land in `business-ops`'s root `.git`, not travel with this folder when it's later
extracted into its own repo. A `.githooks/` folder checked into the repo itself avoids
that and works correctly once this becomes a standalone repo.

It is **not active by default** — git only looks in `.githooks/` if you tell it to. One
time, inside a real git checkout of this repo, run:

```
git config core.hooksPath .githooks
```

After that, every commit that touches a `SKILL.md` rebuilds the Atlas automatically.

**2. A GitHub Actions workflow (backstop, works once this is on GitHub).**
`.github/workflows/rebuild-atlas.yml` reruns the same build on every push that touches a
`SKILL.md` or `atlas/build.py`, and commits the result if it changed. This is inert until
the repo is actually pushed to GitHub — nothing to configure, it just starts working the
moment it lands there.

## Open it

Double-click `atlas/index.html`. No server, no install.

It is fully self-contained on purpose: everything is inlined, there is no CDN, no external
font, and no network call of any kind. Browsers block `fetch()` against `file://` URLs, so
baking the data in at build time is the only way this works from a double-click. It also
means the Atlas can be handed to someone as a single file.

Light and dark both work; it follows the system setting and the Theme button overrides it.

## Reading the graph

- **One cluster per department**, color-coded, labelled.
- **Node size** grows with how connected a skill is.
- **Ringed nodes** are orchestrators — the skills that chain the others.
- **Click a node** to read it; the graph dims everything except that skill and its direct
  connections, which is the fastest way to see a chain.
- **Chips** at the top of the detail panel jump to what a skill calls and what calls it.
- Drag to pan, scroll to zoom, drag a node to pull it out of the pile.

## How edges are found

An edge is a skill naming another skill **in backticks** in its body. These files
reference siblings in backticks by convention, and matching bare prose instead turned
every common word into a false edge. If a real connection is missing from the graph, the
fix is to backtick the reference in the SKILL.md — which is worth doing anyway, because it
is also how a future session finds it.

The build prints any skill with no connections in either direction. An unconnected skill is
usually either genuinely standalone or missing its "Chains from / into" section.
