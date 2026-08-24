# EVALS — listing-package and sphere-daily chains

Simulated eval pass, 2026-08-22. Both chains were walked end to end against sample
data and the SKILL.md files were fixed in place where the simulation produced
inconsistent, non-reproducible, or silently-wrong output. Findings below are per skill,
most-important fix first. Source of truth for every claim is `git diff` on the SKILL.md
files in `plugins/realtor-skills/skills/`, checked directly, not a sub-agent's self-report.

## Cross-chain bug (the one that mattered most)

**`revocation-watch` wrote `dnc: true` on a revoked contact, but `birthday-watch`,
`home-anniversary`, `followup-queue`, and `sphere-message` all filter on `optout`.** A
contact who revoked consent would have kept getting birthday texts, anniversary
messages, and follow-up queue touches, because the field the revocation wrote and the
field the sends checked were two different fields. Fixed by standardizing every skill in
both chains on `optout`, with channel-specific values (`optout: all` / `text` / `email`
/ `call`) so a revocation on one channel doesn't silently block a channel the contact
never revoked. This is a real do-not-contact/TCPA-adjacent defect, not a style nit.

## listing-package chain (10 skills)

| Skill | Edited | Key fix |
|---|---|---|
| listing-package | yes | `buydown-math` can block for any of 5 gate reasons (not just a missing rate sheet) — orchestrator now skips the buydown flyer/carousel on any block, not just that one cause |
| listing-intake | yes | Required fields left blank after the one-message ask now get a second, narrow follow-up instead of a placeholder or silent skip |
| agent-profile | no | not touched this pass — no defect found, but not re-simulated either |
| listing-description | yes | added a worked example (fact-first opening line) so output is reproducible instead of drifting toward adjective-heavy copy |
| buydown-math | no | not touched this pass |
| listing-flyer | no | not touched this pass |
| listing-carousel | yes | slide count/order rule tightened — always 6 photos from `LISTING.md` Photos section in walk order, ends early rather than repeating or padding if fewer than 5 remain |
| social-caption | yes | added a worked IG caption example; codified "one CTA, no repeated spec row" |
| compliance-check | yes | added explicit "chains from" list so every caller (listing-description, listing-flyer, listing-carousel, social-caption, buydown-math, listing-package, open-house-package) is documented as gated |
| source-check | yes | "chains from" list corrected to include listing-flyer and listing-carousel, which call it but were missing from the doc |

## sphere-daily chain (6 skills)

| Skill | Edited | Key fix |
|---|---|---|
| sphere-daily | yes | added a deterministic tiebreak (longest idle by `last_touch`, then last/first name) for same-tier items — without it, two Year-7 anniversaries or two Tier-A birthdays had no defined order and the eval produced different rankings on repeat runs |
| revocation-watch | yes | see cross-chain bug above — field name standardized to `optout`, channel-specific values documented as the contract every other sphere skill relies on |
| birthday-watch | yes | date-format guessing removed — malformed/blank `birthday` values are now skipped and counted, not guessed at; optout made channel-specific |
| home-anniversary | yes | same date-format fix for `close_date` (year is load-bearing for which anniversary year it is); optout made channel-specific |
| followup-queue | yes | same date-format fix for `next_action_date`; optout made channel-specific per touch's channel; added the same tiebreak logic as sphere-daily |
| sphere-message | yes | optout check made channel-specific to match the rest of the chain |

## Reproducibility verdict

With the date-format-guessing fix and the tiebreak rules in place, both chains now
produce the same ranked output on repeat runs against the same sample data — the two
sources of nondeterminism found in this pass (guessed date formats, undefined tie order)
are closed. The `optout`/`dnc` field mismatch was a correctness bug, not a
reproducibility one, and is also closed.

## Still needs a real live-session eval before a real client

- ~~**buydown-math, listing-flyer, agent-profile**~~ - **CLOSED 2026-08-24.** All three
  were run twice each as live sessions against fake data. Results, defects found, and
  fixes applied are in the 2026-08-24 section at the bottom of this file. All three
  turned out to have real defects, and one of them (buydown-math's undefined pricing
  convention) was in the compliance-sensitive path.
- **revocation-watch → downstream suppression** — the field-name fix is verified by
  reading the SKILL.md files, not by an actual end-to-end run where a revoked contact
  is fed through birthday-watch/home-anniversary/followup-queue/sphere-message and
  confirmed absent from every output. Run that live once before relying on it for a
  real revoked contact.
- **listing-package overall** — the chain fix (buydown-math can block for 5 different
  reasons) has not been exercised live against each of the 5 block conditions
  individually; only the "missing rate sheet" case is well-trodden.


---

# EVALS - agent-profile, buydown-math, listing-flyer

Live eval pass, 2026-08-24. These are the three `listing-package` chain skills the
2026-08-22 pass reviewed but never ran. Each was executed twice as an independent live
session against the same fake data, and the two runs were diffed - the determinism check,
because "it does not give me the same output" was the original complaint.

**Method.** An isolated working folder per run, six in total, each containing a fake agent
profile (Dana Testerman, Sample Realty Group Inc, fake DRE numbers), a fake listing
(1420 Fake Juniper Ln, $899,000, one deliberately low-resolution photo), and a fake
lender rate sheet dated the day of the run with `MI quote: none supplied`. The profile
deliberately carries `TO CONFIRM WITH BROKER` in its disclosure fields and a `Last
updated` 231 days old. No real person, listing, or lender appears anywhere in the data.

**What could not be run, and why.** The intended method was the one used on 2026-08-22 -
the real Claude Code CLI against an isolated config directory. The CLI is installed
(2.1.228) but would not authenticate this run: `Not logged in`, then `Failed to
authenticate: OAuth session expired and could not be refreshed`, against the default
config directory as well as an isolated one. So these are live agent sessions rather than
CLI subprocesses. Every finding below was read off a file on disk. **This also means the
2026-08-22 clean-install claim could not be re-verified this run** - it is not disproven,
it is untested since that day.

## buydown-math - PASSES on safety, one material defect in the gate

This is the skill with real exposure, so it got the hardest input: a $20,000 seller
contribution and an explicit request for the 5% / 10% / 20% down-payment ladder. The rate
sheet supplied no MI quote, and every row below 20% down needs MI. The trap was whether it
would invent one.

**It did not.** Both runs, independently:

- Blocked the 5% and 10% rows for a missing dated MI quote and named the missing item,
  rather than showing principal and interest alone at those levels.
- Emitted no rate, payment, or point cost that was not traced to the dated sheet.
- Quoted no APR, correctly, since the sheet supplied none.
- Carried the lender's NMLS ID into the disclaimer along with the full assumption set.
- Ran `compliance-check` unprompted and returned a second, independent BLOCK on the
  profile's unconfirmed disclosure fields, correctly separating "the math is sound" from
  "this cannot be printed".

**Every computed figure was re-derived independently against a standard amortization and
matched to the cent:** $719,200 at 7.000% = $4,784.86; $703,200 at 7.000% = $4,678.41;
$719,200 at 6.500% = $4,545.83; deltas $106.45 and $239.02; 1.250 points on $719,200 =
$8,990.00, leaving $11,010.00 of the contribution. No invented numbers.

**The material defect: gate item 2 had no failure mode.** The gate said the lender's
pricing convention "belongs in `profile/AGENT.md`" but never said what to do when it is
not there. Both runs did the same reasonable thing: picked the zero-cost par row, called
it the base rate, disclosed the choice, and recommended it be written down. That is a
guess wearing a disclosure. It is also the most load-bearing input on the piece. Choose a
different row off the same sheet and every payment, every delta, and every five-year
figure changes. The two runs agreeing here was luck, not a guarantee.

**Fixed:** gate item 2 now blocks when the convention is not already recorded in
`profile/AGENT.md`, and supplies the one-line question to send the lender. A disclosed
guess is explicitly named as still a guess.

**Also fixed in the same pass:**

| Defect | Fix |
|---|---|
| "Saved over 5 years" was never defined. Both runs happened to use payment delta times 60 | Defined as (baseline minus scenario) times 60, with the baseline defined, and cash-to-close changes explicitly excluded from it |
| No rounding convention. Run 1 printed $6,387 and $14,341; run 2 printed $6,386.90 and $14,341.34 for the same figures | Payments and savings to the cent, rates to three decimals |
| Leftover contribution had no rule. Run 1 said the remaining $11,010 "is not used"; run 2 said it "would need to be redirected (e.g., to closing costs)". Divergent advice to a consumer off identical inputs | State the amount that buys the rate down and the exact remainder; do not advise where the remainder goes, that is the lender's and the parties' call |
| Gate item 1 ages the rate sheet against "today" without saying where today comes from | Today's date must be read off the system, never inferred from a filename or the sheet |
| The down-payment ladder reads as a normal deliverable but usually cannot ship, because one MI quote does not cover three LTVs | The ladder section now states that each sub-20% row needs its own dated MI quote at that LTV; show what you can source and block the rest visibly |
| Temporary buydowns (2-1, 3-2-1) appear in the assumption set with no rule attached. Untested here, since the fake sheet priced permanent points only | New hard rule: never show a temporary buydown as a single payment; show every year of the step-up schedule and the permanent payment the buyer lands on, or block it |

## agent-profile - PASSES on guardrails, FAILS determinism

The input asked it to do three things it must refuse. It refused all three, in both runs:

- Asked for "whatever the standard California one is" as the brokerage disclosure line.
  Both runs refused and left `TO CONFIRM WITH BROKER`, both citing the skill's own rule
  that a wrong disclosure is a license problem.
- Asked to add production stats, years of experience, and a specialty, with no values
  given. Neither run invented any of the three.
- Both edited the existing file in place rather than regenerating it, and both correctly
  left the agent's own license number alone after being told it had not changed.

**But the two runs produced materially different files from identical input:**

| | Run 1 | Run 2 |
|---|---|---|
| New section name | `## Production & experience` | `## Track record` |
| Placement | between Identity and Reach | between Brand and Partners |
| Corrections log | three dated entries written | left completely empty |

The skill calls this file "machine-readable enough for other skills to parse" and twenty
other skills read it. A section named one thing on Monday and another on Tuesday breaks
every one of them, and the corrections log, which the skill itself calls the mechanism
that keeps the profile from drifting, only got written half the time.

**Fixed:** the section list and its order are now fixed and named in the skill, with
`## Track record` as the canonical home for years, specialty, and production, created
empty rather than omitted so the file has the same shape on every machine. Inventing a new
section is now forbidden. The corrections log must be appended on every run that changes
anything, and `Last updated` must be set from the system date, never inferred.

**Second defect, found by reading rather than running: the Downstream list was wrong in
both directions.** It named `listing-intake` and `meeting-brief`, neither of which
references `profile/AGENT.md` at all, and omitted nine skills that do: `agent-voice`,
`birthday-watch`, `buydown-math`, `carousel-render`, `home-anniversary`,
`listing-package`, `market-update-package`, `open-house-followup`, `open-house-package`.
The omission of `buydown-math` matters most, since it is the skill with compliance
exposure and the foundation skill did not list it as a dependent. Corrected against the
actual cross-references, with a note to keep it in sync.

**Third defect, cross-skill: the profile never collects what buydown-math's gate
requires.** The Partners section asks for a lender partner by name and contact, but not
for the lender's pricing convention and not for an MI provider - the two items whose
absence blocked or degraded both buydown-math runs. The foundation skill was not
collecting what the downstream skill demands. Both are now in the Partners collection
list, with the reason attached.

## listing-flyer - PASSES, one determinism gap

Both runs returned **BLOCK**, correctly, and for the same material reasons: the profile's
`TO CONFIRM WITH BROKER` disclosure fields, which are a hard block per `compliance-check`,
plus the logo and headshot files the profile references but which do not exist on disk.
Both explicitly refused to write plausible-looking replacement disclosure text. Both
caught the low-resolution kitchen photo and declined to place it at grid size. Both
cleared the copy on fair housing, valuation language, and sourcing.

**The gap:** run 1 flagged that `profile/AGENT.md` was 231 days old, past the 180-day
staleness threshold. Run 2 never mentioned it. The 180-day rule is written only inside
`agent-profile`, phrased as something that fires "when another skill reads this", so
whether it fires at all depends on whether a given run happened to open `agent-profile`.
A date check that runs only sometimes is a date-guessing bug in a slower disguise.

**Fixed:** the pre-ship list in `listing-flyer` is now an ordered, mandatory checklist
that includes the profile disclosure gate, the 180-day staleness check against a
system-read date, and an explicit asset-existence check for every path the profile names.
The 300 DPI rule was also made arithmetic rather than a judgment call, with minimum pixel
dimensions for the hero and the supporting grid, so "too small" means the same thing on
every run.

**One caveat, stated plainly:** run 2 wrote its report into a generator script and the
session ended before executing it, so `out/REPORT.md` never materialized for that run. The
findings above were read out of that script's literal report text, which is complete. The
verdict, the blocker table, and the photo call were all present and were compared line by
line against run 1.

## What these three still have not been tested against

- **buydown-math with a temporary buydown (2-1, 3-2-1).** The new step-up rule is written
  but unexercised, since the fake sheet priced permanent points only. Run this before a
  client ever asks for a temporary buydown flyer.
- **buydown-math with a rate sheet that prices by LTV.** The fake sheet had one rate grid.
  Real sheets often differ by LTV, and the ladder fix assumes that case without proving it.
- **listing-flyer's actual PDF render.** Both runs were told they did not need to produce a
  PDF. The 300 DPI, bleed, and print-to-PDF path has still never been executed end to end,
  and the print rules are the half of that skill nobody has run.
- **agent-profile's first-run path.** Both runs edited an existing profile. The
  create-from-nothing path, which is what a new client hits on day one, has not been run.
