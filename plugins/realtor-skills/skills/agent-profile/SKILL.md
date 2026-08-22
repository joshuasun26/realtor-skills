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

End the file with:

```
Last updated: YYYY-MM-DD
```

and a `## Corrections log` section — one dated line each time a downstream skill was
told something in this file was wrong. That log is how the profile gets more accurate
instead of drifting.

## Guardrails

- **Never invent a fact about the agent's business.** No production numbers, no years of
  experience, no specialties unless they told you in this session. Blank beats wrong.
- **Never write a market statistic into this file.** Profile holds identity, not data.
  Market numbers live in `market-pull` output with an as-of date attached.
- **Flag stale.** If `Last updated` is more than 180 days old when another skill reads
  this, say so once and offer to run a refresh.

## Downstream

These skills read `profile/AGENT.md` and will stop and route here if it is missing:
`listing-intake`, `listing-flyer`, `listing-carousel`, `listing-description`,
`open-house-flyer`, `open-house-signin`, `market-brief`, `market-carousel`,
`sphere-message`, `followup-sequence`, `social-caption`, `meeting-brief`,
`compliance-check`.

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
