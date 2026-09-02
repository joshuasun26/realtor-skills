---
department: pipeline
name: ghl-setup
description: >
  Set up GoHighLevel as the agent's CRM, texting number, inbox and automation rail, with
  Claude doing the configuration and verification and the agent's own hands on every
  password, payment, consent screen and code. Trigger on "set up my GoHighLevel", "GHL
  setup", "connect my Instagram to GoHighLevel", "get me a texting number", "connect my
  calendar to GoHighLevel", "let Claude read my GoHighLevel", or when any pipeline skill
  needs a CRM and profile/STACK.md has no GoHighLevel section. Do NOT trigger for building
  a specific automation once setup is done; that is ghl-automations. Do NOT trigger for
  writing the messages themselves; that is sphere-message or followup-sequence.
---

# GoHighLevel setup, with the right hands on the right clicks

GoHighLevel is the system of record this library can run on: one contact record per person,
every text, DM and synced email on that record, a phone number the agent owns, booking
calendars, and workflows. Claude Code is the brain that reads it and drafts from it. This
skill wires the two together in the right order and proves each step before the next.

Reads `profile/AGENT.md` and `profile/STACK.md`. Writes a `## GoHighLevel` section into
`profile/STACK.md` and stores credentials only in `.env`.

## The rule that comes first

**A password, a payment method, an OAuth consent screen, and a 2FA code are the agent's
own click. Always.** Claude opens the page, names the button, and stops. If the agent asks
Claude to type a password or enter a card, Claude declines and says why. This is not a
limitation to work around; it is the reason the agent can trust the setup.

## Levels, so nothing is promised before it is proven

- **Level 1, the app.** GoHighLevel on the phone and the laptop, the number bought, the
  inbox live, Instagram connected. Everything in this level is the agent's own clicks with
  Claude narrating the path.
- **Level 2, Claude reads.** A read-only API token. Claude reads the inbox, drafts replies,
  reports what a workflow actually delivered, and never transmits. Most agents live here
  for weeks and that is correct.
- **Level 3, Claude sends on your go.** A second token that can send and cannot read.
  Claude drafts, the agent says go in that same exchange, Claude sends that one message
  and reads the delivery status back. Set up in a later session, after Level 2 is trusted.

## Who does what

| Step | Claude | The agent (their own hands) | Why |
|---|---|---|---|
| Create the account, choose Starter, enter the card | Opens the pricing page, explains the usage billing | Yes | Payment |
| Buy the phone number | Names the menu path | Yes | Payment, account settings |
| A2P 10DLC registration (US texting will not deliver without it; allow days) | Drafts the business description and the sample messages to paste | Yes: EIN, business address, submit | Regulatory identity |
| Account timezone (Settings > Business Profile) | Says why it matters: texts must land inside the legal 8am to 9pm window | Yes, one time | Settings page |
| Connect Instagram | Drives to the popup; says to use the direct Instagram route, not Instagram through a Facebook Page | Yes: the Meta consent screen and any 2FA | OAuth |
| Connect Google or Outlook calendar (Calendars > Connections) | Clicks "+ Add new" | Yes: the Google consent screen | OAuth |
| Two-way email sync (Settings > My Profile > Email) | Explains what it does and does not sync | Yes: the Google consent screen | OAuth |
| Mint API tokens (Settings > Private Integrations) | Names the exact scopes for each token | Yes: creates each one, copies the token from the one-time toast, pastes it into `.env` | The token is shown once |
| Verify every token | One GET per token; reports pass or fail | Nothing | Read-only |
| Create pipeline stages and one booking calendar | By API, with `calendars.write` | Nothing, or their own clicks if they prefer | Config work |
| Import contacts, tag, dedupe, set DND for opt-outs | By API, after the canary below | Confirms the file and the tags | Config work |
| Build or edit a workflow | Reads the list by API, dictates the exact clicks, verifies `published` after | Yes: every click in the builder | No write API exists |
| Anything that costs money beyond the plan | Prints the price and stops | Yes | Payment |

## The run, in order

1. **Intake.** Do they already have a GoHighLevel account, on which plan, with which of
   the above done? Read `profile/STACK.md`. Ask only what the file does not answer.
2. **No account yet: stop here.** Point them to the playbook's "Before you start" section
   for the plan and the referral disclosure. Never host them under someone else's agency;
   the account is theirs.
3. **Level 1 clicks,** in the table order. After each one, verify by looking, not by asking:
   the number shows in Settings > Phone Numbers, the Instagram thread appears in
   Conversations, the calendar shows under Connections.
4. **Tokens.** Two Private Integrations, deliberately split:
   - `GHL_READ_TOKEN`: `contacts.readonly`, `contacts.write`, `conversations.readonly`,
     `conversations/message.readonly`, `workflows.readonly`, `calendars.readonly`,
     `calendars.write`, `locations/customFields.readonly`, `locations/customFields.write`.
     No message-write scope.
   - `GHL_SEND_TOKEN` (Level 3 only): `conversations/message.write` and nothing else.
   - `GHL_LOCATION_ID`: the sub-account id from the address bar or Settings > Business
     Profile.
   All three go in `.env`, which must be in `.gitignore`. Confirm the ignore before the
   paste, not after.
5. **Verify each token with one read.** `GET https://services.leadconnectorhq.com/workflows/?locationId=...`
   with header `Version: 2021-07-28` for the read token. Contacts and workflows use
   `2021-07-28`; conversations and calendars use `2021-04-15`. Send a normal browser
   `User-Agent` header; without one the edge returns 403 with `error code: 1010`, which is
   not an auth failure. A 401 or 403 with the right headers means the token lacks that
   scope: mint again, do not guess.
6. **Canary before any import.** Create one contact by API using the agent's own email
   with a plus-alias, carrying the exact tags the real import will carry. Confirm no
   workflow's enrolled count moved, the contact has no messages, and it gained no tags it
   was not given. Then delete it. Only then import.
7. **Opt-outs.** A tag never blocks a send; only DND does. Set DND on every opt-out. When
   updating a contact, write only the fields being changed; a `tags` array in a PUT
   replaces the whole set.
8. **Write `profile/STACK.md`**: which steps are done, which tokens exist and their scopes
   (never the values), the number, and what could not be done and why.
9. **Level 3, only when asked, only after Level 2 has run for real.** The send wrapper
   POSTs `{"type": "SMS", "contactId": ..., "message": ...}` to
   `/conversations/messages` with `Version: 2021-04-15` and the send token. A 201 means
   accepted, not delivered: read the message back and report its status. Every send is
   logged with the timestamp, the contact, and the agent's go in that session.

## What this skill will not claim

- It will not say texts are working until a real text has delivered after A2P clears.
- It will not build a workflow by API; there is no such API. It dictates and verifies.
- It will not present two-way email sync as an inbox replacement. Only threads started
  from the CRM, or from contacts already in it, sync; nothing before the connection does.
- It will not turn on Conversation AI to answer people on the agent's behalf without the
  agent reading its pricing and saying yes.

## Chains from / into

Called before `ghl-automations`, `followup-sequence`, `open-house-followup`, and any skill
that wants a texting rail. Reads `agent-profile`. Writes to `profile/STACK.md`, which
`stack-setup` also owns.

If the user asks how this works, what it needs, or how to customize it, read `PLAYBOOK-ghl-setup.md`
in this folder and answer from it.

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
