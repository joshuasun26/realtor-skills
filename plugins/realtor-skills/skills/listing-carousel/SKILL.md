---
department: listings
name: listing-carousel
description: >
  Build a multi-slide Instagram or Facebook carousel for one property — the photo-led
  listing carousel, or the text-and-graphics buydown carousel on the same property.
  Renders slides from HTML to PNG at social dimensions using the agent's brand colors and
  fonts. Trigger on "carousel for [address]", "listing carousel", "build the slides",
  "make the buydown carousel", or as a step inside listing-package or open-house-package.
  Do NOT trigger for a market or city carousel — that is market-carousel.
---

# Listing Carousel — the format that gets shared

Two variants, built from the same listing file. Post them on different days so they do
not compete with each other.

Reads `listings/<slug>/LISTING.md`, `listings/<slug>/BUYDOWN.md` if it exists, and
`profile/AGENT.md`.

---

## Variant A — the listing carousel (photo-led)

**Real photography. The property is the hero on slide one.** Not a logo, not a headshot,
not a "JUST LISTED" bar over a stock image.

- **Slide 1 (cover):** the hero photo, with a restrained overlay — address and city, and
  the price. If it is an open house, the day and time window instead of the price. Keep
  overlay text off faces and off the roof line.
- **Slides 2 to 7:** six photos from the Photos section of `LISTING.md`, in the order a
  buyer walks the house. Slide 2 is always the distinctive-feature photo with its sentence
  from `LISTING.md` — that one slide is why the post gets saved. If the Supporting set has
  more than five photos left after slide 2, take the first five in walk order and drop the
  rest; if it has fewer than five, use what exists and end the carousel early rather than
  repeating a photo or padding with the hero shot again.
- **Slide 8 (close):** the specs in a clean block — beds, baths, interior sqft, lot sqft,
  year built — plus the agent's name, headshot, brokerage, license number, phone, and the
  Equal Housing statement.

## Variant B — the buydown carousel (text and graphics)

**No photography required.** This variant routinely outperforms the photo carousel with
people who do not already follow the agent, because it answers a question rather than
showing a house. Do not over-build it.

- **Cover:** the tension in the reader's own language. "Most buyers negotiate the price.
  Almost nobody negotiates the rate."
- **Slide 2:** the mechanic in plain English — one credit applied once versus the same
  dollars applied to the payment every month.
- **Slides 3 to 5:** the scenario table from `BUYDOWN.md`, one comparison per slide. Big
  numbers, minimal chrome.
- **Slide 6:** the down-payment ladder, if the product supports it, with the product
  named.
- **Slide 7:** pivot to the property and the open house, so the post still serves the
  listing.
- **Final slide:** the full disclaimer block, verbatim from `BUYDOWN.md`. It is small
  type but it is legible type. Never a screenshot, never cropped.

## Build method

1. Write one HTML file per slide, or one HTML file with one `.slide` element per slide,
   at **1080 x 1350** (4:5 portrait, the highest-reach feed ratio). Use 1080 x 1080 only
   if the agent asks for square.
2. Pull colors and fonts from `profile/AGENT.md`. If a brand font is not installed
   locally, say so and fall back to a named system font rather than silently substituting.
3. Design at 2x and downscale — render at 2160 x 2700 and resize. Text renders far
   cleaner.
4. Render with a headless browser to PNG. Name files `slide-01.png` … in post order, in
   `listings/<slug>/carousel-<variant>/`.
5. Open the rendered PNGs and actually look at them before delivering. Check for clipped
   text, overlay text sitting on a face or a busy area, and low-contrast text on photos.
   Rendering is where layouts break, and the only way to catch it is to look.

## Type and layout rules

- One idea per slide. If a slide needs a paragraph, it needs to be two slides.
- Minimum body size ~28px at 1080 wide. Instagram compresses; small type turns to mush.
- High contrast. Text over a photo needs a scrim or a solid block behind it, never raw
  text on a busy image.
- Leave the bottom ~120px of every slide clear of anything important — the app's own UI
  covers it in feed.
- Consistent margins across all slides. Inconsistent gutters is the single most common
  tell of a generated deck.

## Before it ships

- `compliance-check` on all slide copy. Every time. This is public marketing.
- `source-check` on any number on any slide.
- License number and brokerage on the final slide, per `profile/AGENT.md`.
- If the listing belongs to another agent, credit the listing agent and their brokerage
  on the final slide, and confirm photo permission is recorded in `LISTING.md`.

## Distribution note (say this to the agent once)

The design is not what makes this reach people. **The tags are.** Crediting and tagging
the listing agent, the co-lister, the open house host, and the brokerage borrows their
audiences, which are dense with exactly the people the agent wants. A carousel with
nobody tagged is a worse version of a post that already underperforms. Invite every real
account as a collaborator.

## Chains from / into

Called by `listing-package`, `open-house-package`. Reads `listing-intake` and
`buydown-math` output. Feeds `social-caption`.

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
