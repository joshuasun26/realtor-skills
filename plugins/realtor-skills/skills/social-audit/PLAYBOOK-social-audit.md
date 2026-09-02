# See what is actually working on your Instagram

### 10 minutes. An Instagram account; Insights screenshots help, but are not required.

## What this does for you

Most agents guess which posts "did well." This skill refuses that guess. It reads Insights screenshots, a logged-in browser session, or your public grid, then writes a dated audit with a one-week post plan you can hand to content planning.

You get real counts where the path can see them, a mix breakdown, cadence truth, and three do-more / three stop lines pulled from your own data.

It will never invent a like count, never carry last month's numbers into this run, and never call a post a winner without naming the post and the number.

## The one command

```
audit my instagram
```

Open Claude Code **in your business folder** (the one with `profile/` in it). Type the line. Answer by voice if that is easier.

**First time?** It will ask for one of these, in order:

1. Screenshots of Instagram Insights (Accounts Reached, top posts, Total Followers / growth). On a business or creator account: profile → menu (top right) → **Insights**.
2. Or permission to browse your already-logged-in Instagram session.
3. Or, if neither is available, a look at the public grid only (degraded).

## What you get back

`Example shape, not a real run`

```
## Social Audit - <date>
Path used: Insights screenshots
What this path could not see: [example]

## Content mix
Listings / Personal / Market / Value - counts and rough %

## Cadence
Actual posts/week over the visible window; gaps flagged by date

## Performing / not performing
Named post + number + source screen

## Do more of / Stop
Three lines each, tied to this run's data

## Suggested week
Five-slot day / post / why table
```

Yours is built from your data, not this example. The file lands at `content/audit-<YYYY-MM-DD>.md`. Prior audits are never overwritten.

## Three things that break, and the fix

1. **You are on a personal Instagram account and Insights is missing** - Insights only exists on business or creator accounts. (*"If they are on a personal account, Insights does not exist - tell them plainly and drop to Path 2 or 3."*) Fix: switch the account type in Instagram settings, or drop screenshots of the grid / use a logged-in browse.

2. **The report has clean-looking stats that feel too round** - guessed engagement is banned. (*"Never estimate a like count, never infer reach from a caption's tone, never carry a number forward from a prior audit into this one."*) Fix: say "only use numbers you can see on the screenshots" and re-run; missing data should say "no visible engagement data for this post."

3. **Public-grid path comes back empty or thin** - Instagram's logged-out wall often blocks it. (*"Try it, and if it comes back empty or clearly wrong, say that plainly rather than presenting a thin result as a full audit."*) Fix: send three Insights screenshots next time, or open Instagram already logged in in the Claude browser session.

If it is none of these: screenshot it and paste it to Claude. That is the fastest way through.

## Make it yours

- "Weight my advice toward [city] and my price band" - sharper when `profile/AGENT.md` exists; create or edit that file.
- "Always prefer screenshots over browsing my session" - locks Path 1; note it in `profile/` or edit `skills/social-audit/SKILL.md` Step 0.
- "Give me fewer than six do-more/stop lines if the data is thin" - already allowed; reinforce in the skill file so it never pads.

Say 'show me the skill file' and it opens `skills/social-audit/SKILL.md`. Change the words, save, and the next run uses them.

## How it works, in four lines

It picks the best available path: Insights screenshots, logged-in browse, or public grid. It sorts recent posts into mix buckets and checks real cadence from visible dates. It only labels performing vs not when real numbers are attached. It writes a dated markdown audit and a five-slot suggested week; it never estimates engagement.

## Related

Hand the suggested week to content planning: say `plan my content` (content-week) and paste the audit in. For captions on a single post, that is a different skill (social-caption), not this one.

Still stuck? Text Joshua.
