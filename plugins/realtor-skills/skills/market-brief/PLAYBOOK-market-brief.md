# Turn this month's MLS numbers into a client-ready market update

### 10 minutes. Prerequisite warning: needs a current market-pull data file for the area (MLS numbers). Do not run this until market-pull has written data/market/<area>-<YYYY-MM>.md.

## What this does for you

The monthly market update is proof you know your farm. Done well, it justifies the email and gives every follow-up a reason that is not "just checking in."

This skill reads one area's market-pull file and writes the client-facing brief in your voice: headline, numbers table, what it means for buyers, what it means for sellers, caveats, and sources with as-of dates.

It will not predict prices, will not say it is a "good time" to buy or sell, and will not write a brief from last month's file when this month's pull is missing.

## The one command

```
write the market update
```

Open Claude Code **in your business folder** (the one with `profile/` in it). Type the line (or "market report for [city]"). Answer by voice if that is easier.

**First time?**

1. Run market-pull for the area and period first (that skill needs your own MLS login; it will not scrape aggregator sites).
2. Confirm `data/market/<area-slug>-<YYYY-MM>.md` exists for the current period.
3. Then run this command. If the file is missing, this skill stops and sends you back to market-pull.

## What you get back

`Example shape, not a real run`

```
1. Headline (one sentence on what changed, or that nothing changed)
2. Numbers table (4-6 metrics, YoY, sample size on each)
3. If you are buying (2-3 concrete sentences, no prediction)
4. If you are selling (same)
5. Caveats (where data is thin)
6. Sources (MLS name, area definition, date range, pull date)

Plus shorter cuts: email length, one-page PDF shape, three-line text version.
```

Yours is built from your data, not this example. Output is drafted in chat and saved where your market-update package expects it for that area and month.

## Three things that break, and the fix

1. **It stops and refuses to write** - the current-period data file is missing. (*"If the data file does not exist for the current period, stop and run `market-pull` first. Do not write a brief from a previous month's numbers and do not write around the absence of data."*) Fix: run market-pull for that area and month, then re-run "write the market update."

2. **The draft forecasts or says now is a good time to buy/sell** - those lines are banned. (*"Never predict. No 'prices will rise', no 'now is the time to buy', no 'we expect'."* And: *"Never say 'it's a good time to buy' or 'a good time to sell.'"*) Fix: say "describe what happened only; strip forecasts and good-time lines" and regenerate.

3. **A percentage looks bold but the sample was tiny** - sample size must travel with the claim. (*"Sample size travels with every percentage. 'Down 12%' on nine sales is noise. Report the nine."*) Fix: require every % to show N, and move thin metrics into the caveat section.

If it is none of these: screenshot it and paste it to Claude. That is the fastest way through.

## Make it yours

- "Always lead with the three-line text version" - useful for sphere texts; set preference in `profile/` or the skill length section.
- "Default area is [city / zip set]" - store in `profile/AGENT.md` so you do not re-specify.
- "Keep the email under 300 words" - already in the 250-400 band; tighten in `skills/market-brief/SKILL.md`.

Say 'show me the skill file' and it opens `skills/market-brief/SKILL.md`. Change the words, save, and the next run uses them.

## How it works, in four lines

It reads the current `data/market/<area>-<YYYY-MM>.md` plus your voice and agent profile. It picks a handful of understandable metrics that moved, with YoY and sample size. It writes buyer and seller meaning as interpretation of the past, never a forecast. Every number is meant to route through source-check; neighborhood wording through compliance-check.

## Related

Upstream: market-pull (bring the MLS numbers). Often wrapped by market-update-package. Downstream pieces can reuse the brief for carousels, sphere messages, and captions.

Still stuck? Text Joshua.
