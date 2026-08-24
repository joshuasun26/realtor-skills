---
department: foundation
name: agent-profile
description: >
  Create or refresh the agent profile file that every other skill in this library reads —
  the agent's name, brokerage, license number, service area, price band, brand colors and
  fonts, contact details, lender partner, and the disclosures their state and brokerage
  require on marketing. Trigger on "set up my profile", "agent profile", "update my
  brokerage", "my license changed", "change my service area", "my brand colors", "who am
  I in this system", or on the FIRST run of any listing, market, or sphere skill when
  `profile/AGENT.md` does not exist yet. Do NOT trigger for a client's or a lead's
  details — that is contact-import.
---

# Agent Profile — the file everything else reads

This is the foundation skill. Almost every other skill in this library opens
`profile/AGENT.md` before it does anything. If that file is thin or stale, every flyer,
caption, and brief downstream is thin or stale too.

Run this once at install, then whenever something in it changes.

---

## The file

Path: `profile/AGENT.md`, relative to the working folder the user runs skills from.

If it already exists, **read it first and edit in place.** Never regenerate it from
scratch — it accumulates corrections over time, and a rebuild silently drops them.

## What to collect

Ask for all of it in ONE message. Do not trickle-ask across five turns.

**Identity and licensing**
- Full legal name as it appears on the license, plus the name they go by
- License number and issuing state
- Brokerage legal name, brokerage license number, office address
- Team name, if they market under one

**Reach**
- Direct phone for public-facing marketing (confirm this is the number they want printed;
  many agents do not want their personal cell on a flyer)
- Email, website, Instagram handle, other public profiles

**Market**
- Primary service area: cities, neighborhoods, or ZIP codes, listed explicitly
- Typical price band
- Property types they actually work (SFR, condo, income, land, luxury, new construction)
- Their MLS name and whether they have an agent login — every market number in this
  library comes from that MLS, so record which one

**Brand**
- Two or three brand colors as hex values
- Headline and body fonts, and whether those fonts are installed locally
- Logo and headshot file paths
- Any brokerage brand rules they must follow (some brokerages mandate logo size,
  placement, and a specific disclosure line)

**Partners**
- Lender partner, title, escrow, photographer, stager, inspector — name and contact.
  Skills like `buydown-math` need to know who to ask for a rate sheet.
- **The lender's NMLS ID**, and **the lender's pricing convention** — the exact rule for
  reading a base rate off their sheet (for example: "the zero-cost par rate", or "the
  rebate closest to 1.500 without going over"). `buydown-math` blocks without this, and
  if it is missing every run picks its own rule and the same rate sheet produces
  different payments. Ask the lender for it in one line and record their answer verbatim.
- **The mortgage insurance provider** they quote through. Any payment below 20% down
  needs a dated MI quote from a named provider, so without this `buydown-math` can only
  ever show the 20%-down row.

**Required disclosures**
- The exact disclosure line their brokerage requires on marketing pieces
- Their state's license-display rule (most states require the license number and the
  brokerage name on any advertising)
- Equal Housing Opportunity treatment

If they do not know their brokerage's rules, **do not guess and do not fill in a
plausible-looking line.** Write `TO CONFIRM WITH BROKER` in that field and tell them it
blocks any piece that ships publicly. A wrong disclosure is a license problem.

## The format

Write it as markdown with one `##` section per group above and one fact per line, in
`Key: value` form. Machine-readable enough for other skills to parse, human-readable
enough for the agent to correct by hand.

**The section names and their order are fixed. Do not rename them, do not reorder them,
and do not invent a new one.** Downstream skills look these up by name, so a run that
calls it `## Track record` when the last run called it `## Production & experience`
silently breaks every skill that reads it. The canonical list, in order:

```
## Identity and licensing
## Reach
## Market
## Brand
## Track record
## Partners
## Required disclosures
## Corrections log
```

`## Track record` holds years of experience, specialty, and production numbers. Create it
empty with `TO CONFIRM` values rather than omitting it, so the shape of the file is the
same on every machine. If the agent asks for a field that does not belong to any section
above, put it in the closest existing section and say where you put it — do not open a
new section for it.

End the file with:

```
Last updated: YYYY-MM-DD
```

and a `## Corrections log` section. **Append one dated line for every change you make in
a run, every time, including the run that creates the file** — what changed, from what to
what, and who said so. Also log it when a downstream skill is told something in this file
is wrong. That log is how the profile gets more accurate instead of drifting, and a run
that edits the file without writing the line has broken it. Set `Last updated` to today's
date read from the system, never a date you inferred from the contents of the file.

## Guardrails

- **Never invent a fact about the agent's business.** No production numbers, no years of
  experience, no specialties unless they told you in this session. Blank beats wrong.
- **Never write a market statistic into this file.** Profile holds identity, not data.
  Market numbers live in `market-pull` output with an as-of date attached.
- **Flag stale.** If `Last updated` is more than 180 days old when another skill reads
  this, say so once and offer to run a refresh.

## Downstream

These skills read `profile/AGENT.md` and will stop and route here if it is missing:
`agent-voice`, `birthday-watch`, `buydown-math`, `carousel-render`, `compliance-check`,
`followup-sequence`, `home-anniversary`, `listing-carousel`, `listing-description`,
`listing-flyer`, `listing-package`, `market-brief`, `market-carousel`,
`market-update-package`, `open-house-flyer`, `open-house-followup`,
`open-house-package`, `open-house-signin`, `social-caption`, `sphere-message`.

If you add or remove a reader, update this list in the same edit. It was wrong in both
directions on 2026-08-24 — it named two skills that never read the file and omitted nine
that do, including `buydown-math`, the one with real compliance exposure.

---

<!-- self-improvement-loop v1 -->

## Self-improvement loop

Before ending a run of this skill, review the run:

1. Did any step fail, stall, or need a workaround you had to invent?
2. Did the user correct, reject, or rewrite something meaningful in the output?
3. Did you discover something a future run would want to know (a path that moved, a
   tool that replaced another, a preference they stated out loud)?

If yes to any, propose a specific edit to this SKILL.md in one or two lines and ask
whether to apply it. Propose only changes that would alter a future run's behavior --
skip cosmetic rewording, and never propose more than two edits at once.

Do not edit this file without their go-ahead. If they say no, drop it and do not re-raise
the same suggestion in a later run of the same session.
