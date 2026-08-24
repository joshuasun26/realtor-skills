---
department: listings
name: listing-flyer
description: >
  Build a print-ready single-page property flyer for one listing — hero photo, specs,
  supporting photos, agent block, disclosures — as a PDF sized for letter or A4, in the
  agent's brand. Also builds the buydown variant of the same flyer when payment scenarios
  exist. Trigger on "flyer for [address]", "property flyer", "make the handout", "open
  house flyer", "print piece", or as a step inside listing-package or open-house-package.
  Do NOT trigger for social graphics — that is listing-carousel.
---

# Listing Flyer — the thing people pick up and take home

The flyer is the only piece in this library that gets printed, which means every mistake
is permanent and sits in a stack on a kitchen counter. Slower, more careful pass than
anything digital.

Reads `listings/<slug>/LISTING.md`, `listings/<slug>/BUYDOWN.md` if present, and
`profile/AGENT.md`.

---

## Layouts

**Standard property flyer (default)** — one page, letter (8.5 x 11 in) portrait unless
the agent's market uses A4.

- Top third: hero photo, full bleed to the margins. Address and city over it or directly
  beneath it, whichever keeps text off a busy area.
- Price, prominent, with beds / baths / interior sqft / lot sqft / year built as a clean
  spec row.
- Middle: three to five supporting photos in a grid, sized so nothing is a thumbnail.
- Short body copy: three to five sentences maximum, built around the distinctive feature
  and its sentence from `LISTING.md`. Nobody reads a flyer paragraph.
- Bottom block: agent headshot, name, title, license number, phone, email, brokerage name
  and logo, Equal Housing Opportunity statement.
- Fine print: HOA dues if any, and the "information deemed reliable but not guaranteed"
  line the agent's brokerage uses.

**Open house variant** — same layout, with the open house day, date, and time window as
the most prominent element after the address, plus a QR code linking to the sign-in page
from `open-house-signin`.

**Buydown variant** — a second page or a separate flyer. The scenario table from
`BUYDOWN.md` occupies the top half, the property occupies the bottom half, and the full
disclaimer block sits at the foot at a legible size. Never shrink the disclaimer to make
room.

## Print production rules

These are the ones people get wrong:

- **300 DPI.** Render or export at 300 dots per inch at final size. A 1080px photo is a
  screen asset; it prints soft. Check the source resolution of every image before
  placing it, and say so if a photo is too small rather than placing it anyway.
  The test is arithmetic, not taste: a photo supports `pixels / 300` inches at final
  size. On the default letter layout the hero needs at least **2550 x 1200 px** and each
  supporting-grid photo at least **1050 x 790 px**. Below that, name the photo, give its
  pixel size and the largest size it can print at, and either drop it or ask for a
  higher-resolution replacement. Never upscale it and place it anyway, and never quietly
  shrink the whole grid to accommodate one weak file.
- **0.25 inch bleed** on anything intended for a commercial printer; 0.5 inch safe
  margin inside the trim on all four sides. Nothing important within the safe margin.
- **Export as PDF, not PNG or JPG.** Vector text stays sharp; rasterized text does not.
- Check the file size. Over about 10 MB and email will bounce it; run a compression pass
  and verify the photos still look right afterward.
- If the agent is printing at home, produce a no-bleed version too, because home printers
  cannot print to the edge.

## Build method

Author in HTML and CSS with a `@page { size: letter; margin: 0 }` rule and print-to-PDF
from a headless browser. It gives real text in the PDF, the agent's actual brand fonts,
and a file anyone can re-render later.

Use CSS physical units (`in`, `mm`, `pt`) throughout, not `px`. Mixing pixel units into a
print layout is how flyers come out at 92% scale.

Then open the PDF and look at it. Every time.

## Before it ships

Run this list in order, every time. It is a checklist, not a judgment call — a flyer that
gets a clean pass one day and a blocked pass the next on the same inputs is the bug.

1. **Profile gate.** Open `profile/AGENT.md`. If any field under Required disclosures
   reads `TO CONFIRM WITH BROKER`, the flyer is **BLOCKED** — say which fields, route
   them to the broker, and do not write a plausible-looking line in their place.
2. **Profile staleness.** Compare `Last updated` in `profile/AGENT.md` against today's
   date read off the system. More than 180 days, say so and offer a refresh — every run,
   not just the runs that happen to open `agent-profile`. Never infer today's date.
3. **Asset existence.** Every file path the profile names — logo, headshot — and every
   photo the layout places must actually exist on disk. Check them; a path in a profile
   is not a file. Missing logo or headshot blocks the bottom block, and that blocks the
   flyer.
4. **Photo resolution**, per the 300 DPI rule below.
5. `compliance-check` on all copy. License number and brokerage present and at the size
   the brokerage requires.
6. `source-check` on every number, including the square footage and the HOA dues.
7. If it is another agent's listing, their name and brokerage are credited, and photo
   permission is recorded in `LISTING.md`.
8. Confirm the QR code, if present, actually resolves — scan it, do not assume it.

## Output

`listings/<slug>/flyer-<variant>.pdf`, plus the source HTML alongside it so it can be
regenerated when the price changes. Note it in the listing's Status log.

## Chains from / into

Called by `listing-package`, `open-house-package`. Reads `listing-intake`, `buydown-math`,
`open-house-signin` (for the QR target).

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
