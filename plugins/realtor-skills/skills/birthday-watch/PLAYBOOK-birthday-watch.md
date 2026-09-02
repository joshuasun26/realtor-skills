# Draft real birthday texts for today and this week

### 5 minutes. Prerequisite: a CRM (or contacts) export with a birthday column in MM-DD or YYYY-MM-DD, imported into data/contacts.csv.

## What this does for you

A birthday text is the one unsolicited note from a realtor people actually welcome. It fails when it sounds like a merge field.

This skill checks who has a birthday today and in the next seven days, then drafts one short message per person in your voice, using whatever real context your contact file holds.

It will not put business, links, or a pitch in a birthday message. Nothing sends to a contact until you approve that specific batch.

## The one command

```
whose birthday is it
```

Open Claude Code **in your business folder** (the one with `profile/` in it). Type the line. Answer by voice if that is easier.

**First time?** You need birthdays in `data/contacts.csv`:

1. Export contacts from your CRM with the birthday field included.
2. Hand that file to contact-import (or say "import these contacts") so birthdays land as `MM-DD` or `YYYY-MM-DD`.
3. Re-run this skill. Rows with blank or odd formats (like March 3 or 3/3) are skipped and counted as "needs fixing."

## What you get back

`Example shape, not a real run`

```
Today
1. [Name] - [relationship note]
   [1-3 sentence draft, no pitch]

Next 7 days
- [Name] - [date] - [call vs text suggestion]

Needs fixing: N rows with bad or blank birthday formats
Coverage: N contacts have birthdays / total
```

Yours is built from your data, not this example. The approval batch is a file you can edit; after you say go, it can update `last_touch` and log sends to `records/sent-log.md`.

## Three things that break, and the fix

1. **The list is empty even though you "know" birthdays** - the file needs a real birthday column in the only two valid formats. (*"Only two formats are valid: `MM-DD` or `YYYY-MM-DD`. If a row's `birthday` value is blank, or is in any other format... do not guess - skip that row."*) Fix: pull a fresh CRM export with the birthday field, run contact-import, then re-run birthday watch. Bring the CRM export; most phone exports have none.

2. **It drafted a pitch or a market line into a birthday text** - business is banned here. (*"No business in a birthday message. No market update, no 'let me know if you're thinking of selling', no link, no listing, no call to action of any kind."*) Fix: say "strip the ask; birthday only" and regenerate that draft.

3. **It sent (or you thought it would send) without you saying go** - outbound to contacts is gated every time. (*"Nothing sends without an explicit approval in this session for this specific batch. Approval today is not approval tomorrow."*) Fix: review the numbered batch file, edit if needed, then say go for this batch only.

If it is none of these: screenshot it and paste it to Claude. That is the fastest way through.

## Make it yours

- "Text me the daily list to myself from my CRM number" - Level 2 notify; store the setup ids in `profile/AGENT.md` under Birthday Watch.
- "For tier A, always suggest a call before a text" - already the escalate path; lock it in `profile/AGENT.md`.
- "Schedule my birthday check every morning at 7:30" - a schedule skill job, not this skill; say that line to Claude.

Say 'show me the skill file' and it opens `skills/birthday-watch/SKILL.md`. Change the words, save, and the next run uses them.

## How it works, in four lines

It reads `data/contacts.csv` for birthdays today and the next seven days, skipping bad formats and opt-outs. It drafts each message individually through your voice file, never a merge-field template. It presents a numbered batch and waits for your explicit go before any contact is messaged. It never invents a birthday from a fuzzy date string.

## Related

Usually called from your daily sphere run (`sphere-daily`). Home purchase anniversaries are a different skill (`home-anniversary`). Growing the birthday column starts with contact-import from a CRM or phone export.

Still stuck? Text Joshua.
