# One number, one inbox, one record per person: setting up GoHighLevel with Claude

### 90 minutes across two sittings. You need a GoHighLevel account, your business email, and your EIN for the texting registration.

## What this does for you

Right now your texts are on your phone, your Instagram DMs are in Instagram, your email is
in Gmail, and your CRM has none of it. Every time you ask Claude about a client, it is
working from whatever you remember to paste. GoHighLevel puts the number, the DMs, the
synced email and the calendar on one contact record, and this playbook connects Claude to
that record so every draft starts from real history.

What comes back: a working account with your own texting number, Instagram landing in the
inbox, your calendar connected, and Claude able to read all of it. Sending comes later, in
a second sitting, after you have watched it read correctly for a while.

The one rule it will not break: Claude never types a password, enters a card, or clicks a
consent screen for you. It opens the page, names the button, and waits. That is on purpose.

## Before you start

Sign up on your own account, on the Starter plan. It is **$97 a month** for unlimited
contacts and users, with a 14-day trial. Texts, calls, emails, the phone number rental and
the premium AI features are billed as usage on top of that, so plan on more than $97 once
you are actually sending.

Here is the link: https://www.gohighlevel.com/?fp_ref=joshua-sun73

Plain disclosure: that is a referral link. If you sign up through it, GoHighLevel pays me a
commission every month you stay, at no extra cost to you. I run my own business on it and I
would recommend it either way. Use the link or do not; the price is the same.

> Plan price and contents checked against GoHighLevel's own pricing and help pages on
> 2026-09-01. Usage billing means $97 is the floor, not the all in number. Check the page
> before quoting the figure to anyone.

## The one command
```
set up my GoHighLevel
```
Open Claude Code **in your business folder** (the one with `profile/` in it). Type the
line. Answer by voice if that is easier.
**First time?** It will ask for two things.
1. Your GoHighLevel login, open in your browser. It never asks for the password.
2. Your EIN and business address, for the texting registration form. You type those into
   GoHighLevel's form yourself; Claude drafts the description and sample messages you paste.

## What you get back
```
GoHighLevel setup, 2026-09-10
  Account ........ Starter, your-business sub-account
  Number ......... (562) xxx-xxxx, A2P registration submitted 9/10, pending
  Instagram ...... connected, direct route, 3 threads visible in Conversations
  Calendar ....... Google connected, "Buyer consult, 30 min" created
  Email sync ..... on; only new threads sync, past email does not
  Tokens ......... read token verified (workflows: 4 found); send token: not yet
  Canary ......... clean, deleted
  Next ........... text a friend after A2P clears; then Level 3 in a second sitting
```
Example shape, not a real run. Yours is built from your data, not this example.
It lands in `profile/STACK.md` under a GoHighLevel heading. Your tokens live only in `.env`.

## Three things that break, and the fix
1. **Claude says the text was accepted, nothing arrives** - the texting registration
   (A2P 10DLC) has not cleared, and US carriers drop unregistered texts. Fix: open Settings
   > Phone Numbers > Trust Center and read the status. Until it says approved, use email
   and Instagram flows. This takes days, not minutes, and no setting speeds it up.
2. **Claude reports 401 or 403 on a token** - the token was created without the scope it
   needs, or a header is wrong. Fix: say "which scope is missing" and it names it. Then in
   GoHighLevel, Settings > Private Integrations, create a new one with that scope, copy it
   the moment it appears (it shows once), and paste it into `.env`.
3. **Instagram will not connect, or connects and shows no messages** - the Facebook Page
   route cached an old permission. Fix: disconnect, then reconnect using the direct
   Instagram option, not "Instagram through Facebook." Then send yourself a DM from
   another account and watch for it in Conversations.
If it is none of these: screenshot it and paste it to Claude. That is the fastest way
through.

## Make it yours
- "Give Claude the send token" - moves you to Level 3: Claude drafts, you say go, it
  sends that one message and reads the delivery back. Saved as a second token in `.env`
  and a line in `profile/STACK.md`.
- "Set my texting hours to 9 to 7" - the window Claude will refuse to send outside of,
  saved in `profile/STACK.md`.
- "Use my brokerage's forms for contracts, not GoHighLevel" - tells every later skill to
  keep transaction documents where your broker wants them; saved in `profile/STACK.md`.
One line on the edit path: "Say 'show me the skill file' and it opens
`skills/ghl-setup/SKILL.md`. Change the words, save, and the next run uses them."

## How it works, in four lines
It reads your profile and your stack file, then asks only for what they do not answer.
It decides, step by step, which clicks are yours (passwords, payments, consent screens,
codes) and which are its own (configuration, verification, imports after a canary test).
It writes the result to `profile/STACK.md` and your tokens to `.env`, nothing anywhere else.
It never builds a workflow by API, because none exists; it dictates the clicks and checks.

## Related
Chains into **Turn on the automations that pay for the account** (`GHL automations`) and
**Follow up without forgetting anyone** (`build my follow up sequence`).

The web version of this playbook, the one to send someone who does not have Claude Code
open yet, lives at
<https://docs.google.com/document/d/1c-UF_-AIs82OXcwz9-H64HEGNcWvWCks6lTDY-rb8cw>

Still stuck? Text Joshua at 858-585-4853.
