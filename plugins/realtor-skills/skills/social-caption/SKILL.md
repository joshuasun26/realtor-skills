---
department: content
name: social-caption
description: >
  Write the caption for one social post — Instagram, Facebook, or LinkedIn — in the
  agent's voice, with the right hook, the right length for the platform, a real call to
  action, and the tag and credit block that actually drives the reach. Trigger on "write
  the caption", "caption for this post", "what do I write with this", "social copy", or as
  a step inside any package orchestrator. Do NOT trigger for MLS remarks — that is
  listing-description.
---

# Social Caption — the part that decides whether the graphic gets seen

Reads the asset it is captioning, `profile/AGENT.md`, `profile/VOICE.md`, and whatever
source file the asset came from (`LISTING.md`, the market data file, `BUYDOWN.md`).

---

## The rule that governs everything here

**The caption ADDS. It does not repeat the slides.**

If the carousel already says the median price, the caption should not say the median
price. The reader has both in front of them, and a caption that recaps the graphic is
wasted space. Say the thing that did not fit on the slides — the reason it matters, the
story behind it, the honest caveat, the question.

## Structure

**Line 1 is the hook, and it is most of the job.** Feeds truncate after roughly the first
125 characters, so the first line has to earn the tap. What works:

- A specific number with the tension attached
- A statement the reader half-disagrees with
- A concrete detail: "The back yard has a 40-year-old avocado tree."

What does not work: "Check out this beautiful home!", "New listing alert", "Happy Monday
everyone", or any sentence that could sit under any post.

**Then a blank line.** The caption preview cuts at the first line break, so line 1 alone
has to stand up.

**Body: two to five short paragraphs**, one idea each, blank line between them. Not a
wall. People read captions on a phone in a hallway.

**Then one call to action.** One. "Comment X for the flyer" or "send me a message" or
"save this for when you're ready" — but not three of them. Multiple CTAs produce zero
actions.

**Then the credit and tag block.** On a listing or open house post this is not a
courtesy — **it is the distribution.** Tagging and crediting the listing agent, the
co-lister, the host, and the brokerage borrows their audiences. A post with nobody tagged
reaches only the agent's own followers, which for most agents is a fraction of the people
they actually want.

**Then hashtags**, last, after the tag block.

## Platform

| | Length | Hashtags | Notes |
|---|---|---|---|
| **Instagram** | 125 chars before the cut; 300–800 total works | 5–15, mixed local and topical, at the end | Links are not clickable — never say "link below" |
| **Facebook** | Shorter. 1–3 sentences outperforms. | 0–3 | Links work and get clicked |
| **LinkedIn** | 1–3 paragraphs, professional register | 3–5 | Links suppress reach; consider first comment |

Ask the platform. Do not write one caption and hope.

## Worked example (Instagram, listing post)

```
The back yard has a 40-year-old avocado tree the sellers have never let anyone touch.

Three bed, two bath, 1,850 sqft in [City]. The kitchen was redone in 2022, but the tree
is the reason people stop scrolling when this one comes up.

New listing, open house this weekend — details in the caption below.

Comment TREE and I'll send you the flyer.

Listed by [Agent Name], [Brokerage] — DRE #[license]. Co-hosted with [Co-lister],
[Brokerage]. Equal Housing Opportunity.

#[city]realestate #[city]homes #justlisted #openhouse #[neighborhood]
```

Notice what it does NOT do: it does not repeat the price or the spec row that is already
on the carousel slides, it has exactly one CTA, and the hook is a concrete detail, not an
adjective.

## Compliance — every caption, no exceptions

A caption is public advertising. `compliance-check` runs on it before it ships.

- License number and brokerage where the agent's state requires it on advertising
- Equal Housing Opportunity where required
- **Nothing about the neighborhood's character, its residents, its schools, or whether an
  area is "safe", "quiet", "family-friendly", or "desirable"**
- No valuation claim, no prediction, no guarantee
- Any number routes through `source-check` — MLS-sourced with an as-of date
- Any payment or rate figure carries the full disclaimer from `buydown-math`, and the
  disclaimer does not get trimmed to fit the caption. If it does not fit, it goes on the
  final slide and the caption points to it.
- If it is another agent's listing, credit them and their brokerage

## Voice

Run `agent-voice`. Scan the finished draft against the banned words list before
delivering — do not just try to avoid them while writing.

No manufactured urgency the agent has not earned. No claim about their experience or
results that is not in `profile/AGENT.md`.

## Output

Deliver the caption as **plain text, ready to paste, with nothing around it** — no
preamble, no "here's your caption", no metadata, no notes interleaved. Blank line between
paragraphs so it pastes into the app looking the way it will read.

If there are notes, put them after the caption block, clearly separated.

## Chains from / into

Called by `listing-package`, `open-house-package`, `market-update-package`,
`listing-carousel`, `market-carousel`. Uses `agent-voice`, `compliance-check`,
`source-check`.

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
