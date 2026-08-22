---
department: market
name: market-pull
description: >
  Pull the current month's statistics for one defined geography from the MLS and write
  them to a dated, sourced data file that every market skill reads — median sold price,
  closed sales, sold days on market, months of supply, sale-to-list ratio, active and
  pending counts. Trigger on "pull the numbers for [city]", "market data", "run the stats",
  "what's the market doing in [area]", or as step 1 of any market skill. Do NOT trigger to
  write a client-facing brief — that is market-brief, which reads this file.
---

# Market Pull — get the numbers, from the MLS, with a date on them

Every market number this library ever publishes originates here. Separating the pull from
the presentation is what makes it possible to check a claim months later.

---

## The MLS rule — read this before anything else

**Market statistics come from the MLS. Full stop.**

Consumer aggregators — Zillow, Redfin, Realtor.com, Homes.com and the rest — publish
market statistics on definitions that do not match the MLS, and the mismatch is not
cosmetic. The most damaging case: their "days on market" typically measures how long a
listing has been **active on their site**, not how long a **sold** property took to reach
contract. Publishing that as "average days on market" is a false claim, and it is the
number an agent gets publicly corrected on by another agent.

Aggregator data is acceptable for exactly one thing in this library: confirming a single
property's basic facts when there is no MLS access. Never for a statistic about a market.

**If there is no MLS access this session, this skill does not produce a number.** Report
that, name what you tried, and stop. That is honest and it is completely different from
handing the agent a wrong figure.

## Define the geography precisely

Vague geography is the second-biggest source of wrong market claims. Pin down and record:

- Exactly what area: city, MLS area code, ZIP list, or drawn boundary. Write down the
  literal definition used.
- Property types included: SFR only, or SFR + condo + townhome? These move differently
  and blending them without saying so is misleading.
- Price band, if filtered
- The date range, and whether it is calendar month, trailing 30 days, or trailing 12
  months

**The same definition must be used every month** or the trend line is fiction. Store the
definition in the file and reuse it.

## What to pull

| Metric | Definition to use |
|---|---|
| Closed sales | Count of `Sold` in the period |
| Median sold price | Median of closed sale prices in the period. Median, not average. |
| Sold price per sqft | Median, on interior sqft |
| Days on market | Median DOM of **SOLD** listings. Say which DOM field the MLS reports. |
| Sale-to-list ratio | Median of sold price ÷ final list price |
| Active listings | Count as of the pull date |
| Pending / under contract | Count as of the pull date |
| Months of supply | Active ÷ trailing-12-month average monthly closed sales |
| New listings | Count entered in the period |

Also pull the same period one year prior, for year-over-year. Month-over-month in real
estate is mostly seasonality and it misleads.

**Small samples.** If a metric is built on fewer than about 10 closed sales, the median is
noise. Record the sample size next to every metric and flag anything thin. Never publish a
percentage change built on 4 sales without saying it is built on 4 sales.

## Write the file

`data/market/<area-slug>-<YYYY-MM>.md`:

```
## Definition
Area: ...          Property types: ...      Date range: ...
MLS: ...           Pulled by: ...           Pulled on: YYYY-MM-DD

## Metrics
metric | value | sample size | YoY | notes

## Source
Report name / search ID, exactly as run in the MLS, so it can be re-run.

## Caveats
Anything thin, anything the MLS defines unusually, anything that changed since last month.
```

**Never overwrite a prior month's file.** The archive is what makes trends real.

## Handing it on

Return the file path plus a two-line plain reading: what actually changed, and what did
not. Resist narrative. `market-brief` writes the story; this skill produces the facts.

## Chains into

`market-brief`, `market-carousel`, `market-update-package`, `meeting-brief`,
`open-house-followup` (message 2).

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
