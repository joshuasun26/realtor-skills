# The AI tools and skills page — what is being designed

The page: **joshuasun.co/aitools**, the one hub link. Always write that URL, never the old
joshuasuncapital.com one. The old address 301s to the same page, so it works, but it sends
traffic and link equity to the domain being retired.

Status: **design notes, partly unbuilt.** Sections marked SHIPPED were verified live.
Everything else is a decision recorded, not a thing that exists. Do not describe an
unbuilt section as if it is on the page.

---

## The problem being solved

The hub grew as a link library, and the skills library arrived as a separate thing taught
in a room. So the page tells people about tools and the bootcamp installs tools, and those
are two different experiences with no seam between them.

Week 6 is where that seam has to close. Someone who was never in the room should be able
to land on the page and get to the same place the room got to: installed, one real output,
and the guardrails on.

---

## The design decisions

### 1. Install is a paste block, not a terminal walkthrough

The single biggest source of failure, confirmed twice. Most attendees are in the Claude
Code desktop app, where the `/plugin` slash commands simply do not exist. The page has to
lead with the paste block that works in both surfaces, and demote the terminal path to a
labeled advanced note. Full copy in `INSTALL-PAGE-COPY.md`.

### 2. Filters, not sections

The library is ONE flat list with filter chips. This was the core decision when the hub
was built and it holds. Do not regress it into accordions or into a page per department.
Chips: start-here, realtors, escrow, content, productivity, investors, and the week tags.

### 3. The skills library gets a real home on the page

Right now the 44 skills are a thing that happens in a bootcamp room. They need a zone on
the hub with:

- What the library is, in one paragraph, no jargon
- The install paste block, above the fold of that zone
- The count, generated rather than typed. It has been wrong on the page twice
- A link to the Atlas (`atlas/index.html`), which already renders every skill and how they
  chain. It is self-contained and opens from a file, so it can be hosted as-is

### 4. "The use cases," not "the prompt library"

Joshua's rename and it stays. Use cases is the more powerful frame. A prompt is a thing
you paste. A use case is a problem you have.

### 5. Autonomy is part of the pitch, not a footnote

New for Week 6. The page should say the quiet part: everyone who gets good at this ends up
turning the permission prompts off, and most do it badly, all at once, with no undo layer
and no idea what they just switched off.

The `safe-autonomy` skill is the answer and it belongs on the page as its own card, not
buried in a list of 44. The framing that works is the honest one:

> The permission prompt is not the safety system. By the fortieth one you are clicking
> Allow without reading it. Turn the prompts off for the noise, put real stops on the five
> percent that can cost you money or a client.

Three layers, and the middle one is the whole point:

| Layer | What it is | Why it matters here |
|---|---|---|
| Deny | The machine refuses. Nothing to click | Stops the agent wrecking their own files |
| **Ask** | Still prompts under bypass: sends, posts, deploys, payments | **The layer people leave out. It is the one that catches the real failure** |
| Standing rules | Written into CLAUDE.md, loads every session | Judgment no setting can enforce. It is a promise, and the page should say so |

The real failure mode is not a deleted folder. It is a reasonable-looking message going to
the wrong list at the wrong time, and finding out from a reply. Say that on the page.

### 6. Every claim on the page carries its source

Counts, versions, and dates get read off the repo at build time or checked by hand the day
they ship. The page has shipped a wrong skill count twice. That is small on its own and it
is the exact habit that produces a wrong rate or a wrong market number later.

---

## Open, needs a decision

- **Where the Atlas gets hosted.** It is self-contained and opens from `file://` today.
  Putting it at a real URL makes it linkable from the page, from emails and from the DM
  funnel. Nothing blocks this but a decision.
- **Whether the library is gated.** The bootcamp is now a paid course at $297 with early
  attendees grandfathered. The repo is public and anonymously cloneable, so today the
  skills are effectively free while the teaching is paid. That may be exactly right. It
  should be a decision, not an accident.
- **The hero hack rotation.** Still driven by the `HACK` dict in `cards.py`. Unchanged.

---

## What is NOT changing

- The canonical URL rule. `joshuasun.co/aitools`, every time, everywhere.
- Filters over sections.
- Start Here stays at four items and never grows.
- Compliance rules live once, at `/bootcamp/rules`, linked from the footer. Never mid-page.
