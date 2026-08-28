# Realtor Skills

This is a set of ready-made abilities that get added to Claude on your own computer.

Once it is installed, you can say things like **"build the full package for 123 Main
Street"** or **"who should I contact today"** and Claude already knows your process,
your brand, your license number, and your rules. You do not have to explain it again
every time.

Everything runs on **your** computer, under **your** accounts. Your contacts and your
client information stay on your machine.

---

## What is in it

| Department | What it handles |
|---|---|
| **Foundation** | Your profile, your writing voice, fact checking, fair housing review, importing your contacts |
| **Listings** | Property intake, MLS remarks, print flyers, social carousels, rate buydown math |
| **Open House** | Digital sign-in page and QR code, event flyer, neighbor invitations, follow-up |
| **Market** | Pulling your MLS numbers, the monthly client brief, the stats carousel |
| **Sphere** | Database audit, birthdays, home anniversaries, your daily contact list |
| **Pipeline** | New leads, follow-up cadences, the daily follow-up queue, meeting prep |
| **Content** | Captions, slide rendering, the weekly content plan |

Small pieces that snap together. If you only want a flyer, ask for a flyer. If you want
everything for a new listing, ask for the full package and it runs all the pieces in
order.

---

## Installing it — the whole thing, step by step

You do **not** need a GitHub account, and you do not need to know what GitHub is. You
will type a few lines and that is the entire job.

### Step 1 — Open the terminal

**On a Mac:** press `Command` and the space bar together, type `Terminal`, press Enter.

**On Windows:** click Start, type `Terminal`, press Enter.

A window opens with a blinking cursor. This is normal. It is not going to break anything.

### Step 2 — Start Claude Code

Type this and press Enter:

```
claude
```

If it says the command is not found, Claude Code is not installed yet. That is a separate
one-time setup and it is the first thing covered in your install session.

### Step 3 — Add the library

Type this exactly as it appears and press Enter:

```
/plugin marketplace add joshuasun26/realtor-skills
```

You should see a confirmation that the marketplace was added. If it says it cannot
find it, check the spelling, there is no www and no .com in that line.

### Step 4 — Install it

```
/plugin install realtor-skills@realtor-skills
```

Answer yes if it asks you to confirm.

### Step 5 — Check that it worked

```
/plugin list
```

You should see **realtor-skills** in the list. That is it. It is installed.

### Step 6 — Tell it who you are (do this once)

Type this, in plain English:

```
set up my agent profile
```

It will ask you for your name, your brokerage, your license number, the cities you work,
your brand colors, and the disclosure line your brokerage requires. Answer what you know.
Anything you are not sure about, say so and it will mark it to confirm with your broker
rather than guessing.

### Step 7 — Load your contacts (do this once)

Export your contacts from your CRM or your phone, then say:

```
import my contacts
```

and tell it where the file is. It will clean them up, remove duplicates, and tell you
what is missing.

### Step 8 — Turn on auto-updates (do this once)

This is the step that makes the "you never have to do anything again" promise true.
Without it, new versions of the library sit there until you go get them yourself.

Type this and press Enter:

```
/plugin
```

Go to the **Marketplaces** tab, find **realtor-skills**, and turn auto-update **on**.
Once it is on, updates arrive on their own — you will never need to touch this again.

**You are done setting up.** Everything after this is just asking for what you want.

---

## Using it

Talk normally. You do not need to remember any commands.

- "I just took a listing at 412 Oak Street, build me the full package"
- "I'm holding it open Saturday 1 to 4, set up the open house"
- "Pull the market numbers for Pasadena and write the monthly update"
- "Who should I contact today?"
- "Whose birthday is it this week?"
- "I have a listing appointment at 2, brief me"
- "Write the caption for this"

If you want to be precise, you can call a skill by name with a slash:

```
/realtor-skills:listing-package
/realtor-skills:sphere-daily
/realtor-skills:market-brief
```

---

## Updates

Once you have turned on auto-update in Step 8, your copy updates itself. You do not
do anything.

Two things worth knowing about how that works:

- **Updates show up on your next launch, not mid-session.** If a change goes out
  while you are already working, you will not see it until you close Claude Code and
  open it again. In practice: a change made one evening is live for you the next
  morning.
- **This only works if Step 8 is done.** Auto-update is off by default for a library
  like this one. If you skipped Step 8, or it somehow got turned off, updates will
  not arrive on their own — go back and turn it on in `/plugin` → Marketplaces.

If you want to force a check instead of waiting:

```
/plugin update realtor-skills@realtor-skills
```

(That is the command that actually pulls a new version onto your machine. A plain
`/plugin marketplace update` only refreshes the catalog listing — it does not by
itself update an already-installed copy.)

---

## The rules it will not break

These are built into the skills, and it will tell you no even when you ask it to do
otherwise. That is on purpose — it protects your license.

**It never sends anything without your explicit approval.** Every text, every email,
every post is written, shown to you, and held. You say go, or it does not go. Saying yes
once does not mean yes tomorrow.

**Market numbers come from the MLS only.** Never Zillow, Redfin, or Realtor.com. Their
"days on market" measures how long a listing sat on *their site*, not how long a *sold*
home took to go under contract, and publishing that as your market data is how you get
publicly corrected by another agent. If it cannot reach your MLS, it tells you it cannot
get the number instead of using a worse one.

**If a number cannot be sourced, it comes out.** It will not round it, hedge it, or make
it "approximately". A hedged wrong number is still wrong and it is still your name on it.

**Fair housing is a hard stop.** It describes the property. It will not write about the
neighborhood's character, the schools' quality, who lives in an area, or whether somewhere
is "safe", "quiet", or "family-friendly" — and it will refuse to, even if you ask.

**Payment and rate figures require a current dated rate sheet from your lender.** No
sheet, no payment numbers. It will build everything else and tell you what is missing.

**Opt-outs are permanent**, on every channel, and nothing can undo them.

**Your data stays yours.** Your contacts live in a file on your computer. Nothing in this
library uploads them anywhere.

---

## Something not working?

Text or email your program contact. Include what you typed and what it said back. That is
usually enough to fix it in one message.

---

## What this is not

It is not a CRM and it does not replace one. It is not a lawyer or a compliance officer —
your broker is. It does not send anything on its own. And it will not write a market
number it cannot point at a source for, which is a feature.
