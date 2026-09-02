# Build a print-ready one-page listing flyer (PDF)

### 15 minutes. Prerequisite warning: needs headless render (Playwright + Chromium), a listing folder with LISTING.md and photos, and brand assets in profile/AGENT.md. FIX-THEN-SHIP until Playwright is installed.

## What this does for you

The flyer is the piece people pick up and take home. Mistakes are permanent and sit in a stack on a kitchen counter.

You point Claude at one listing. It builds a letter or A4 single-page PDF in your brand: hero photo, specs, supporting photos, short body copy, agent block, and disclosures. It can also build the open-house and buydown variants when those inputs exist.

It will not ship a flyer with missing required disclosures, missing logo or headshot, or photos too soft to print. Soft screen images get named and blocked, not quietly upscaled.

## The one command

```
flyer for [address]
```

Open Claude Code **in your business folder** (the one with `profile/` in it). Type the line with the listing address. Answer by voice if that is easier.

**First time?**

1. Confirm Playwright + Chromium are available (headless print-to-PDF). If `python -c "import playwright"` fails, install per your stack preflight before relying on this skill.
2. Have `listings/<slug>/LISTING.md` and the photo files on disk.
3. Confirm `profile/AGENT.md` has logo, headshot, license, brokerage, and disclosure lines filled (nothing left as TO CONFIRM WITH BROKER).

## What you get back

`Example shape, not a real run`

```
listings/<slug>/flyer-standard.pdf
listings/<slug>/flyer-standard.html   (source, re-render when price changes)

Checklist:
- Profile gate: pass / BLOCKED [fields]
- Photo DPI: hero and grid sizes checked
- Compliance + source-check on copy and numbers
```

Yours is built from your data, not this example. PDF plus HTML land under that listing folder; the Status log gets a note.

## Three things that break, and the fix

1. **Render fails or there is no PDF** - this skill authors HTML/CSS and print-to-PDF from a headless browser; Playwright + Chromium must be present. (*"Author in HTML and CSS with a `@page { size: letter; margin: 0 }` rule and print-to-PDF from a headless browser."*) Fix: run your preflight / install Playwright and Chromium, then re-run. Do not improvise a PNG export as the print master.

2. **It says BLOCKED and will not write the flyer** - required disclosure fields are still placeholders. (*"If any field under Required disclosures reads `TO CONFIRM WITH BROKER`, the flyer is **BLOCKED** - say which fields, route them to the broker, and do not write a plausible-looking line in their place."*) Fix: fill those fields in `profile/AGENT.md` with broker-confirmed values, then re-run.

3. **A photo was dropped or the bottom block is missing** - missing assets or soft files stop the ship. (*"Missing logo or headshot blocks the bottom block, and that blocks the flyer."* Also: *"Below that, name the photo, give its pixel size... Never upscale it and place it anyway."*) Fix: add the real logo/headshot paths, or replace undersized photos (hero at least 2550 x 1200 px; supporting at least 1050 x 790 px at 300 DPI).

If it is none of these: screenshot it and paste it to Claude. That is the fastest way through.

## Make it yours

- "Default to A4, not letter" - market paper size; set in the skill layout section or `profile/`.
- "Always produce a no-bleed home-printer PDF too" - already supported for home printers; make it the default in `skills/listing-flyer/SKILL.md`.
- "Use the open house day as the second-loudest element after the address" - open-house variant; say the day/date/time when you trigger.

Say 'show me the skill file' and it opens `skills/listing-flyer/SKILL.md`. Change the words, save, and the next run uses them.

## How it works, in four lines

It reads the listing file, optional buydown file, and your agent profile. It builds HTML/CSS in physical print units and renders PDF through a headless browser (Playwright / Chromium). It runs the ship checklist: profile gate, asset existence, 300 DPI math, compliance and source checks. It never invents disclosure text or upscales a soft photo to fake print quality.

## Related

Often called from a full listing package or open-house package. Listing intake and buydown math feed the inputs. Social graphics are a different skill (listing-carousel), not this flyer.

Still stuck? Text Joshua.
