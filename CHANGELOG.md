# Changelog

All notable changes to the Realtor Skills library, in plain English. This file is the
source for the Membership tier's monthly "what shipped" changelog (see
`agreement-DRAFT.md` section 8).

Format: newest entry first, dated, short bullets. No version numbers yet — this library
hasn't shipped to an outside client so there's nothing to version against.

---

## 2026-08-22

MVP shipping pass: install-flow hardening, flagship chain eval pass, Atlas auto-rebuild,
usage-recap skill, changelog established.

- **Atlas auto-rebuild** — `atlas/index.html` now regenerates automatically instead of
  requiring a manual `python atlas/build.py` run. A repo-relative pre-commit hook
  (`.githooks/pre-commit`, activated via `git config core.hooksPath .githooks`) rebuilds
  and re-stages it on commit; a GitHub Actions workflow
  (`.github/workflows/rebuild-atlas.yml`) does the same on push once this repo is hosted
  on GitHub.
- **New skill: `usage-recap`** — reads the local (opt-in, off-by-default) usage log and
  turns it into a plain-English monthly recap, for the office-hour Zoom promised in the
  Membership tier. Runs entirely offline, on the agent's own machine.
- **Flagship chain eval pass** — the `listing-package` and `sphere-daily` chains went
  through an evaluation pass against fake listing and fake contact data. Fixed a real
  do-not-contact defect (`revocation-watch` wrote `dnc`, downstream sphere skills read
  `optout` — standardized on `optout`), plus nondeterministic tiebreaks and date-format
  guessing that caused reruns to produce different output. Logged in `EVALS.md`.
- **Install-flow hardening** — ran a real clean-install simulation and found the usage
  hook's "off by default" switch didn't actually work (`hooks/hooks.json` auto-loads
  regardless of the `plugin.json` flag). Renamed to `hooks.json.disabled` and confirmed
  `Hooks (0)` on a fresh install. Also fixed the README's incorrect manual-update
  command and added the missing auto-update-toggle step.
- **This changelog established** — going forward, ship notes land here so the Membership
  tier's monthly changelog has a real source to pull from.
