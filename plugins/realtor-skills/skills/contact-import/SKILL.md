---
department: foundation
name: contact-import
description: >
  Import an agent's database from a CRM export, phone contacts (.vcf), spreadsheet, or
  email export into one normalized contacts file that every sphere and follow-up skill
  reads. Deduplicates, normalizes phone numbers and names, records source and consent
  tier, and flags what is missing. Trigger on "import my contacts", "load my database",
  "here's my CRM export", "upload my sphere", "my contacts csv", "vcf", or on the first
  run of any sphere skill when `data/contacts.csv` does not exist. Do NOT trigger for
  adding a single new lead — that is lead-intake.
---

# Contact Import — one clean database, one time

Every sphere, birthday, and follow-up skill in this library reads `data/contacts.csv`.
This skill builds it and keeps it clean.

---

## Inputs it handles

- CRM export (CSV) from any platform — column names vary wildly, map them, do not assume
- Phone contacts as `.vcf` / vCard
- A spreadsheet the agent keeps by hand
- Gmail / Outlook contacts export
- A past-client list from their transaction management system

Ask which they have. Take all of them — merging is the point.

## The normalized schema

Write `data/contacts.csv` with exactly these columns, in this order:

```
contact_id,first_name,last_name,phone,email,relationship,source,consent_tier,
city,birthday,close_date,property_address,last_touch,tags,notes
```

- `contact_id` — stable slug, `firstname-lastname-4digits`. Never renumber on re-import.
- `phone` — E.164 where possible (`+15555550123`). Strip formatting. Keep only one
  primary; extras go in `notes`.
- `relationship` — one of `past-client`, `active-client`, `lead`, `sphere`, `agent`,
  `vendor`, `personal`, `unknown`
- `source` — where this contact came from and the export's file date. This matters.
- `consent_tier` — see below
- `birthday` — `MM-DD` or `YYYY-MM-DD`. Blank if unknown, never guessed.
- `close_date` — for past clients, the closing date, for home anniversaries
- `last_touch` — date of last real contact, blank if unknown

## Consent tiers (do this at import, not later)

Texting and emailing rules depend on how the relationship started. Record it now while
the source is in front of you.

- `express-written` — they signed up, opted in, or checked a box. Written record exists.
- `existing-relationship` — a past client or an active client. There is a real prior
  business relationship.
- `personal` — friends and family, someone the agent genuinely knows.
- `unknown` — scraped, purchased, harvested, or origin unclear.

**Anything marked `unknown` is not a marketing list.** Do not include those contacts in
any bulk send this library produces. Downstream skills filter them out automatically. If
the agent wants to reach them, that is a one-to-one, personally written, non-automated
message, and it is their call and their compliance risk.

Also carry an `optout` tag. **An opt-out is permanent and applies across every channel and
every skill in this library.** Once tagged, that contact never appears in a send list
again, and no skill may remove the tag.

## Deduplication

Merge on, in priority order: phone match, then email match, then exact
first+last+city match. On conflict, keep the record with the more recent `last_touch` and
put the discarded values in `notes` rather than deleting them.

Report the dedupe count. Agents are usually surprised by it and it builds trust.

## The gaps report

After import, tell the agent, in plain numbers:

- Total contacts, and how many after dedupe
- How many have a phone, how many have an email, how many have both
- How many have a birthday (usually very few — this is the biggest miss)
- How many past clients have a `close_date` (drives home anniversaries)
- How many are `unknown` consent tier and therefore excluded from sends
- Which fields would unlock the most value if filled in

Then offer one concrete next step, not five. Usually: "your birthdays are the biggest gap
— want me to set up a way to fill them in over time?"

## Privacy

This file is the agent's client database. It lives on the agent's machine, in the agent's
working folder.

- Do not upload it anywhere, do not paste its contents into a third-party tool, and do
  not include real names or numbers in any example, screenshot, or shared output.
- If a working copy was made during import, delete it when the import is done and say so.
- `data/` should be listed in the working folder's `.gitignore`. Check that it is; if the
  folder is a git repo and `data/` is not ignored, fix it before writing the file.

## Chains into

`sphere-audit`, `birthday-watch`, `home-anniversary`, `followup-queue`, `sphere-daily`.

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
