---
department: listings
name: listing-description
description: >
  Write the MLS public remarks and the agent-facing private remarks for one listing, plus
  the shorter variants for syndication and social, all inside the MLS character limits and
  clean on fair housing. Trigger on "write the listing description", "MLS remarks",
  "property description", "public remarks", "write the copy for [address]", or as a step
  inside listing-package. Do NOT trigger for a caption on a social post — that is
  social-caption.
---

# Listing Description — the copy that has to survive a compliance review

MLS remarks are the most-scrutinized copy an agent writes. They are archived, they are
public, and they are the exhibit if a fair housing complaint is ever filed. Write them
carefully.

Reads `listings/<slug>/LISTING.md` and `profile/AGENT.md`.

---

## What to produce

1. **Public remarks** — the consumer-facing description. Ask the agent for their MLS's
   character limit; most fall between 750 and 1,500 characters including spaces. **Do not
   assume a limit.** If they do not know, write to 750 and note that it can expand.
2. **Private / agent remarks** — showing instructions, lockbox notes, offer instructions,
   commission terms if the MLS carries them, known conditions. Never consumer-facing.
3. **Short syndication line** — roughly 250 characters for portals that truncate.
4. **One-line hook** — under 100 characters, reusable in texts, emails, and captions.

## How to write the public remarks

**Structure that works:**

- **Open on the distinctive feature**, not on "Welcome to this beautiful home." The first
  eight words are the only ones most readers see in a list view. Use the sentence from
  `LISTING.md`.
- **Then the layout**, concretely: bedroom and bath count and how they are arranged, the
  kitchen, the primary suite, the flow. Specific beats adjectival.
- **Then improvements with dates.** "Roof replaced 2021, HVAC 2023" outperforms "recently
  updated" because it is checkable.
- **Then the lot and the outdoor space**, if it is a selling point.
- **Close on the practical**: parking, HOA, and any showing note that belongs in public.

**Voice:** run `agent-voice`. Most MLS remarks read like they were written by the same
person because they were all written by the same three habits. The agent's own register is
a differentiator.

**Banned across the board:** exclamation-point stacking, ALL CAPS SHOUTING, "must see",
"won't last", "priced to sell", "motivated seller" (unless the seller has explicitly
authorized signaling that — it costs them negotiating position), "TLC", "handyman
special", "as-is" without the agent's confirmation, and any word implying a value opinion.

## Fair housing — the specific ones that show up in MLS remarks

Scan for and remove:

- Anything about schools as a quality claim. Naming the assigned district factually is
  different from "top-rated schools."
- "Safe", "quiet neighborhood", "family neighborhood", "good area", "up-and-coming",
  "exclusive", "desirable"
- "Perfect for a growing family", "great starter home", "ideal for retirees", "empty
  nesters", "bachelor pad", "mother-in-law suite" (use "second unit" or "ADU")
- "Walking distance to…" — say the distance or say "near"
- Proximity to a specific place of worship as an amenity
- Anything describing current or expected occupants
- "Master bedroom" — most brokerages have moved to "primary bedroom"

**Describe the property, never the people.** Then run `compliance-check` on the finished
copy anyway. This is the one piece where a second pass is always worth it.

## Accuracy

- Every number in the remarks comes from the verified section of `LISTING.md`. Square
  footage, lot size, year built, bed and bath count.
- **Do not describe an unpermitted addition as finished square footage.** If permit
  status is unknown, describe the space without claiming it as square footage, and flag
  it to the agent.
- Do not state that solar is owned if `LISTING.md` says the lease status is unconfirmed.
- Do not describe a condition you have not been told about — no "move-in ready", no
  "needs nothing", unless the agent said it.

## Output

Append a `## Copy` section to `listings/<slug>/LISTING.md` holding all four variants
verbatim, with the character count of each. The agent pastes from there.

Worked example (public remarks, opening lines only):

> You can renovate a kitchen, you cannot grow a 40-year-old avocado tree. This three
> bedroom, two bath home offers 1,850 square feet with the primary suite separated from
> the secondary bedrooms. Roof replaced 2021, HVAC 2023...

That is the pattern for all four variants: distinctive feature first, then concrete
specifics, never an adjective doing the work a fact could do.

## Chains from / into

Called by `listing-package`. Reads `listing-intake`, `agent-voice`. Gated by
`compliance-check` and `source-check`. Feeds `social-caption` and `listing-flyer`.

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
