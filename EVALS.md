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

- **buydown-math, listing-flyer, agent-profile** — not touched or re-simulated this
  pass. No known defect, but that's an absence of evidence, not evidence of fitness —
  run them through a live session before trusting them on an actual client, especially
  buydown-math since it touches lender rate sheets and MI quotes (compliance-sensitive).
- **revocation-watch → downstream suppression** — the field-name fix is verified by
  reading the SKILL.md files, not by an actual end-to-end run where a revoked contact
  is fed through birthday-watch/home-anniversary/followup-queue/sphere-message and
  confirmed absent from every output. Run that live once before relying on it for a
  real revoked contact.
- **listing-package overall** — the chain fix (buydown-math can block for 5 different
  reasons) has not been exercised live against each of the 5 block conditions
  individually; only the "missing rate sheet" case is well-trodden.
