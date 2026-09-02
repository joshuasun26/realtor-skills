---
department: market
name: market-carousel
description: >
  Build the social carousel that presents one area's market statistics as readable
  graphics — cover, three to five stat slides, what it means for buyers and sellers, and a
  sources slide with the MLS name and as-of date. Trigger on "market carousel", "make the
  stats slides", "post the market update", "city carousel", or as a step inside
  market-update-package. Do NOT trigger for a single property — that is listing-carousel.
---

# Market Carousel — the recurring post that proves the agent knows their market

The most repeatable content an agent has, because the data refreshes every month on its
own. Build the template once, and every month after is a data swap.

Reads `data/market/<area-slug>-<YYYY-MM>.md`, the brief from `market-brief` if it exists,
and `profile/AGENT.md`.

**Do not build this without a current `market-pull` file.** No exceptions, no
last-month's-numbers, no aggregator fill-ins.

---

## Slide plan (7 slides)

1. **Cover** — the area name, the month and year, and the one-sentence headline from the
   brief. The month must be on the cover; these posts get found months later and an
   undated stat graphic is a liability.
2. **The headline metric** — usually median sold price. One enormous number, the
   year-over-year change beneath it, and the sample size in small type. The sample size
   goes on the slide, not only in the caption.
3. **Speed** — median days on market for **sold** listings, with YoY. Label it "days to
   sell (sold listings)" so nobody reads it as active inventory age.
4. **Supply** — active listings, pendings, and months of supply.
5. **What this means if you're buying** — two or three lines, no prediction.
6. **What this means if you're selling** — same.
7. **Sources** — MLS name, the area definition verbatim, the date range, the pull date,
   plus the agent's name, license number, brokerage, and Equal Housing Opportunity.

Slide 7 is not optional and does not get dropped for aesthetics. It is what separates this
from the thousands of unsourced stat graphics agents post every month, and it is the slide
another agent will screenshot if the numbers are wrong.

## Design

- **1080 x 1350** (4:5). Design at 2x (2160 x 2700) and downscale.
- Brand colors and fonts from `profile/AGENT.md`.
- **One number per slide.** A slide with six statistics on it communicates none of them.
- Numbers set very large; labels small but legible; the caveat line smaller still but
  never below ~22px at 1080 wide.
- Keep the bottom ~120px clear of anything important — the feed UI covers it.
- If a metric moved less than its own noise floor, say "roughly flat" on the slide rather
  than printing a meaningless 0.4% change.

## Honesty rules on the graphics themselves

- **Never truncate a chart's y-axis** to make a small change look dramatic. This is the
  single most common lie in real estate stat graphics.
- Never show a percentage change without its sample size somewhere on the same slide.
- Never blend property types without labeling it.
- Never put a projection or a trend arrow extending past the last real data point.
- Never describe the area's character, its residents, or its schools. Numbers and property
  facts only. `compliance-check` before it ships.

## Render

One HTML file per slide, headless-browser render to PNG, output to
`content/market/<area-slug>-<YYYY-MM>/slide-01.png` and so on.

**Open the rendered PNGs and look at them.** Numbers with more digits than the template
expected are the most common overflow, and a clipped median price is worse than no post.

**Then judge the photography, not just the layout.** Every automated check asks whether a slide
is broken. None asks whether it is any good, and a dull image passes all of them. For each slide:

- **Is the subject identifiable as this city?** A pleasant photograph that could be any suburb has
  failed. Name the landmark it reads as, or say none.
- **Is there a subject at all?** A blank wall, a hedge, a patch of sky or an empty sidewalk is
  texture, not a place.
- **Does it survive as a thumbnail?** Interest that lives in fine detail disappears at phone size.
- **Is there usable negative space** where the text block lands, so the good part is not buried
  under it.
- **Do the slides vary?** Eight golden-hour facades is one photograph shown eight times.

Verdict per slide is KEEP or REPLATE with the subject to shoot instead. "Looks fine" is not a
verdict.

**Imagery rules, all hard.** Text-free, because models garble lettering and the data is composited
by the render anyway. **No identifiable people** - real estate imagery showing people can signal
demographic preference, which is a fair-housing problem. No schools and no places of worship, even
when one is the city's most famous building; substitute a civic landmark and write the exclusion
down so it is not quietly re-added on a later pass.

## Reuse

Save the template HTML with the data separated out, so next month is a data swap and a
re-render rather than a rebuild. Note the template path in the output folder's README so
a future run finds it.

## Chains from / into

Reads `market-pull` and `market-brief`. Called by `market-update-package`. Feeds
`social-caption`.

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
