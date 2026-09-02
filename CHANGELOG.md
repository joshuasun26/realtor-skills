# Changelog

All notable changes to the Realtor Skills library, in plain English. This file is the
source for the Membership tier's monthly "what shipped" changelog (see
`agreement-DRAFT.md` section 8).

Format: newest entry first, dated, short bullets. No version numbers yet — this library
hasn't shipped to an outside client so there's nothing to version against.

---

## 2026-09-02 (later)

One new skill and the Week 6 page material, moved into the repo so the site copy and the
library cannot drift apart. Skill count 43 -> 44. Plugin version 0.3.0 -> 0.4.0 in both
manifests.

- **`safe-autonomy` (new, Foundation).** "Stop asking me permission." Turns off the
  permission prompts without removing the stops that matter, in three layers: a `deny`
  list the machine refuses outright, an `ask` list that keeps prompting even under bypass
  mode for anything that sends, posts, deploys or spends, and the standing rules in
  `CLAUDE.md` for the judgment no setting can enforce. Three preconditions before the
  switch is flipped (a dedicated working folder, git as the undo layer, an off-machine
  backup that has actually run), and a five-test drill the agent runs with their own
  hands at the end. Honest rails: bypass mode does not make Claude careful, does not undo
  anything, does not sandbox the folder, and is not for a brokerage-managed laptop. The
  middle layer is the one people leave out and the one that catches the real failure,
  which is not a deleted folder but a reasonable-looking message reaching the wrong list.
  Layer 2 is verified with a live `git push --dry-run` before the setup is called done,
  because a missing prompt and a misspelled tool name look identical from the outside.
- **`docs/week-6/` (new).** The Week 6 material that has to stay in sync with the library:
  the verified install-section page copy (Mac git step, the paste block that works in the
  desktop app, the restart, the update path, the bracket-placeholder fix) and the AI tools
  and skills page redesign notes, with unbuilt sections labeled unbuilt rather than
  described as live.
- **README.** The Foundation row names the new skill.

---

## 2026-09-02

Four new skills, all Foundation, built so a Private Install session spends its minutes on
the agent's business instead of on setup and support. Skill count 39 -> 43. Plugin version
0.2.0 -> 0.3.0 in both manifests, so installed copies with auto-update on actually receive
it. First non-prose files in the plugin: five small scripts under
`skills/voice-command/scripts/`.

- **`preflight` (new, Foundation).** "Check my setup." Runs every tool check the library
  quietly depends on (Claude Code and the paid plan, the working folder and profile, git,
  Python, the render browser, ffmpeg, disk, memory, plugin auto-update), reports one
  table, offers each missing install one at a time with a yes required, and sorts the
  library into run it now, run it if you brought the thing, and tonight after an install.
  Installs nothing on a managed laptop that refuses; hands over the IT note instead.
- **`voice-command` (new, Foundation).** The texting wire to the agent's own phone:
  iMessage self-thread on a Mac, a Telegram bot on Windows, and the send scripts have no
  recipient argument so the worst a bug can do is text the agent. Three levels: the
  morning brief, the loop where they text work back, then dispatch on a numbered go. The
  Mac loop-guard check happens live before any poll is scheduled, the awake problem is
  said out loud, and a scheduled run is the only thing that counts as done. Ships the
  five scripts (Telegram send and poll, iMessage send, read, poll) that were previously
  copied by hand from a starter kit. Honest rail: the Telegram poll was checked against a
  recorded payload, not a live bot, so its first live round trip is done in the room.
- **`wire-a-tool` (new, Foundation).** "Connect [tool] to Claude." A five-rung ladder
  (official connector, API key, CSV export, browser read, paste) that stops at the first
  rung that works on the agent's plan and machine, and never says it cannot be done.
  Carries the Asana connector command and token path as read from Asana's developer
  pages on 2026-09-02, and flags the Lofty API key path as unverified because the help
  page refused a direct read two days running. Writes `profile/TOOLS.md`, no secrets.
- **`owners-manual` (new, Foundation).** "Write my owner's manual." The system reads the
  machine (profile, data counts, the wire, scheduled tasks and their last run, the plugin
  version) and writes the manual from what is there, with the six things that break in
  the first three weeks and their fixes, and a five-minute drill the agent does with
  their own hands. Reads only; prints no secret; leaves the support section blank rather
  than invent it.
- **Playbooks.** Each new skill ships with a client-facing playbook in its own folder
  (`PLAYBOOK-<name>.md`), in the Week 6 template, labeled "Example shape, not a real
  run" because none of the four has been run on a client machine yet.
- **README.** The Foundation row names the four new skills.

---

## 2026-09-01 (later)

One new skill for the Week 6 bootcamp session. Skill count 38 -> 39.

- **`ghl-setup` (new, Pipeline).** Wires GoHighLevel up as the CRM, texting number, inbox
  and automation rail the rest of the library runs on, in an order that proves each step
  before starting the next. The agent's own hands stay on every password, payment, consent
  screen and verification code; Claude opens the page, names the button and waits. Three
  levels so nothing is promised before it is proven: the app on day one, Claude reading the
  account, then Claude drafting on the agent's go. Honest rails throughout - US texts do not
  deliver until A2P clears and that takes days, synced email covers only threads that start
  from the CRM or from contacts already in it, and workflows are built by talking to
  GoHighLevel's own builder because there is no write API for them.

---

## 2026-09-01

Five new skills and a three-level upgrade to birthday-watch, built for the Week 6
bootcamp session ("The Most Important Skill of the Future"). Skill count 33 → 38.

- **`computer-revive` (new, Foundation).** For the machine that crawls by 2pm: measures
  RAM and top consumers first, classifies before closing anything (safe / ask-first /
  never-touch), kills only what the agent approves, re-measures and reports the before
  and after, and teaches one prevention habit per run. Windows and Mac paths. Honest
  rail: on 8GB or less it says hardware is the ceiling.

- **`social-scan` (new, Pipeline).** A daily Instagram lead scan: reads new followers,
  story viewers, and post engagers, classifies each (fellow agent, buyer signal, seller
  signal, sphere contact re-engaging), and drafts up to 5 first DMs in the agent's own
  voice. Works from a logged-in browser session or pasted screenshots — no Instagram API,
  no scraping of private accounts, nothing auto-sends.
- **`social-audit` (new, Content).** A one-command audit of the agent's own Instagram:
  content mix, cadence, what performed and what didn't, three do-more, three stop, and a
  one-week plan shaped for `content-week`. Three input paths (Insights screenshots,
  logged-in browse, public grid) and it states which one it used. Hard grounding rail:
  no performance claim without a named post and a visible number.
- **`video-talking-head` (new, Content).** One raw phone clip in, a finished vertical
  reel out: transcript-driven cuts on word boundaries, captions that never cover the
  face, loudness-normalized audio, an on-screen hook. First run calibrates and locks the
  agent's style into `profile/VIDEO-STYLE.md`; every later run reads it silently.
- **`video-event-recap` (new, Content).** A folder of event or open-house clips in, a
  30-60 second recap reel out, with honest clip triage (skipped clips are named, with
  why) and a property variant that closes on the address card from `profile/AGENT.md`.
- **`birthday-watch` upgraded: wider sources and three notification levels.** New
  sources: phone .vcf and CRM refresh (via `contact-import`), a guided Facebook
  birthdays read, and a paste-in path for anything else — discovered birthdays get
  written back into `contacts.csv`. New levels: Level 1 emails the daily brief to the
  agent themselves, Level 2 texts it from the agent's own CRM number (Lofty reference
  included, add-yourself-as-a-lead setup), Level 3 is the full dictate-a-reply loop.
  The hard rail is unchanged at every level: nothing goes to a contact without the
  agent's explicit go for that specific message.

---

## 2026-08-28

Install-path fix. No skill changes, skill count unchanged at 33.

- **Step 3 of the README is now a real command instead of a blank to fill in.** It read
  `/plugin marketplace add [ADDRESS YOUR INSTALL SESSION GIVES YOU]`, which meant nobody
  could install the library without a person on the other end telling them the address.
  The repo has been public since 2026-08-22, so the address is not a secret and the line
  is now `/plugin marketplace add joshuasun26/realtor-skills`, typed as-is. Added the one
  failure people actually hit, which is adding www or .com to it.
- **Atlas rebuilt and confirmed stable at 33 skills, 7 departments, 209 connections.**
  A second run produced a byte-identical file, so the build is deterministic.

---

## 2026-08-24

Eval pass on the three chain skills that had never been run, plus the fixes they turned
up. No new skills. Skill count unchanged at 33.

- **The last three untested chain skills are now tested.** `agent-profile`,
  `buydown-math`, and `listing-flyer` each ran twice as independent live sessions against
  fake listing, contact, and rate-sheet data, and the two runs were diffed. Full results
  in `EVALS.md`.
- **`buydown-math` held on safety.** Asked for a 5% / 10% / 20% down-payment ladder off a
  rate sheet with no mortgage insurance quote, both runs blocked the rows that needed MI
  instead of estimating one, quoted no APR, and carried the lender's NMLS ID and the full
  assumption set into the disclaimer. Every payment figure it produced was re-derived
  independently and matched to the cent.
- **`buydown-math` gate fixed: the pricing convention now blocks.** The gate required the
  lender's pricing convention but never said what to do when it was missing, so both runs
  picked their own base rate off the sheet and disclosed the choice. Which row you call
  the base rate changes every number on the piece, so a disclosed guess is still a guess.
  It now blocks and routes the question to the lender. Same pass also defined "saved over
  5 years", set a rounding convention, added a rule for a contribution larger than the
  cheapest rate on the sheet, required today's date to be read rather than inferred, and
  added a hard rule that a temporary 2-1 or 3-2-1 buydown can never be shown as a single
  payment.
- **`agent-profile` fixed: the file now has a fixed shape.** Two runs on identical input
  produced different section names in different places, and only one of them wrote the
  corrections log. The canonical section list and order are now written into the skill,
  the corrections log is required on every run that changes anything, and `Last updated`
  comes from the system date. Its Downstream list was also wrong in both directions and is
  now correct. Partners now collects the lender's pricing convention and the MI provider,
  which `buydown-math` requires and the profile was never asking for.
- **`listing-flyer` fixed: the pre-ship list is a checklist, not a judgment call.** Both
  runs correctly blocked the flyer on unconfirmed broker disclosures and missing brand
  assets, but only one of them noticed the profile was 231 days stale. The staleness
  check, the disclosure gate, and an asset-existence check are now explicit, ordered
  steps, and the 300 DPI rule is now arithmetic with minimum pixel dimensions instead of
  an eyeball call.
- **Atlas pre-commit hook actually turned on.** The hook and the GitHub Action shipped on
  2026-08-22, but `core.hooksPath` had never been set in this checkout, so the local hook
  was inert. Now set. The Atlas rebuild was also confirmed byte-for-byte reproducible: 33
  skills, 7 departments, 202 connections.

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
