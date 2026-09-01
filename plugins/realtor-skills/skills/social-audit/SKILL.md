---
department: content
name: social-audit
description: >
  Audit the agent's own Instagram — content mix, posting cadence, and what is actually
  performing versus what is not — from Insights screenshots, a browsed logged-in session,
  or the public grid if neither is available, then hand back a dated report with a
  one-week post plan ready for content-week. Zero setup beyond having an Instagram
  account. Trigger on "audit my instagram", "audit my social", "how's my instagram
  doing", "what's working on my IG", "check my social media", "instagram audit",
  "social audit", or "review my posts". Do NOT trigger to plan next week's content from
  scratch — that is content-week, which reads this skill's output. Do NOT trigger to
  write a single caption — that is social-caption.
---

# Social Audit — ten minutes, one command, real numbers only

This is the skill an agent can run the moment the library is installed, before they have
touched anything else, and still walk away with something true and useful. No listings
file, no market pull, no profile setup required. If `profile/AGENT.md` exists, use it to
sharpen the advice — brokerage, price band, service area. If it does not, run anyway.

---

## The one rule this skill will not break

**Every claim that a post "performed well" or "underperformed" must name the actual
post and the actual number, and say which path below produced that number.**

If the input path available this run cannot surface a number, say "no visible
engagement data for this post" and stop there. Never estimate a like count, never infer
reach from a caption's tone, never carry a number forward from a prior audit into this
one, and never round a fuzzy read into a clean-looking stat. A guessed number is worse
than no number — it is the same failure this whole library refuses everywhere else.

## Step 0 — Work out which path is available, in this order

**Path 1 — Insights screenshots.** Ask first: "Drop in a screenshot of your Instagram
Insights — Accounts Reached, your top posts, and Total Followers / growth. Three
screenshots, from your phone, is plenty." Read the images directly. This is the only
path with real numbers attached to real posts, so prefer it every time it is available.
If the agent has a professional (business or creator) account, these screens live at
profile → menu (top right) → **Insights**. If they are on a personal account, Insights
does not exist — tell them plainly and drop to Path 2 or 3.

**Path 2 — browse their own session.** If this session has a working browser tool and
the agent is already logged into Instagram in it, browse to their own profile and
insights pages directly instead of asking for screenshots. Say so in the report —
"read live from your logged-in session" — and still cite the specific number and screen
it came from. Do not attempt to log in on the agent's behalf and do not ask for a
password; if no logged-in session is available, drop to Path 3.

**Path 3 — public profile only (degraded).** Look at the public grid: post captions,
apparent post type, cadence from visible dates, and like/comment counts where Instagram
still shows them publicly. This path cannot see reach, saves, shares, or follower
growth, and it is often blocked entirely by Instagram's logged-out wall. Try it, and if
it comes back empty or clearly wrong, say that plainly rather than presenting a thin
result as a full audit.

**State the path used at the top of the report, every time**, plus one line on what it
could not see. An agent reading this needs to know whether they are looking at real
Insights numbers or a grid-only guess.

## Step 1 — Content mix breakdown

Sort what you can see (screenshots, browsed feed, or public grid — however many recent
posts the path exposes, note the count) into:

- **Listings** — a property, an open house, a just-sold, a buydown/rate post
- **Personal** — the agent as a person: family, faith, behind-the-scenes, no CTA tied to a deal
- **Market** — stats, trends, "what's happening in [city]"
- **Value** — an answer to a real question, a how-to, a myth-buster, anything a
  non-client would still find useful

Report counts and rough percentages. Do not force a post into a category it does not
fit — say "unclear" rather than guess.

## Step 2 — Posting cadence reality check

From visible post dates, work out the actual average per week over whatever window the
path exposes (Insights screenshots often show 30 or 90 days; the public grid shows
whatever is on screen). Compare it, gently and specifically, to what the agent probably
believes they are doing — most agents overestimate their own cadence. Flag any gap of
two weeks or longer with no post, by date.

## Step 3 — What's performing vs. what's not

Only from Path 1 or Path 2 data with real numbers attached. For each: the post named
(caption snippet or date, whichever identifies it), the actual number, and the source
screen. Group into "performing" and "not performing" only where the gap is real, not
noise between two similar posts. If working from Path 3 only, replace this whole
section with: "No engagement numbers were visible this run — public grids don't show
reach or saves. Send Insights screenshots next time for this section to mean anything."

## Step 4 — Three to do more of, three to stop

Pull straight from Steps 1 through 3, not from general social media advice. Each of the
six lines should point at something specific already visible in this agent's own data —
a format that is over- or under-represented, a category that is quietly winning or
losing, a cadence gap. If the data does not support six distinct findings, give fewer
and say why, rather than padding to six.

## Step 5 — One-week suggested post plan

Build a five-slot week in the same table shape `content-week` uses, so it can be handed
straight over:

| Day | Post | Why (tie back to Step 4) |
|---|---|---|

This is a suggestion, not a build. Tell the agent plainly: "Hand this to content-week
(or just say 'plan my content' and paste this in) to actually produce the posts."

## Write the report

`content/audit-<YYYY-MM-DD>.md`. Never overwrite a prior audit — each run is a dated
snapshot, and comparing this month's cadence or mix to last month's only works if both
files still exist.

```
## Social Audit — <date>

Path used: [Insights screenshots / browsed session / public grid only]
What this path could not see: [...]

## Content mix
[counts + rough %, with "unclear" called out]

## Cadence
[actual posts/week over the visible window, gaps flagged by date]

## Performing / not performing
[named post + number + source, or the Path-3 disclaimer]

## Do more of
1.
2.
3.

## Stop
1.
2.
3.

## Suggested week
[the 5-slot table]
```

## Requires

Nothing but an Instagram handle and ten minutes. `profile/AGENT.md` is optional — read
it if present for a sharper read (brokerage voice, price band, service area), but do not
block or degrade the audit for its absence.

## Chains from / into

Standalone entry point — does not require any other skill to have run first. Feeds its
suggested week into `content-week`. If the agent wants the "what's performing" section
sharper going forward, point them at turning on Insights if they have not, and at
running this again in about a month rather than weekly — engagement data needs more
than a few days to mean anything.

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
