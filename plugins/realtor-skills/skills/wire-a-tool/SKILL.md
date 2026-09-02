---
department: foundation
name: wire-a-tool
description: >
  Connect a tool the agent already uses (their CRM, a task manager, a transaction platform)
  to Claude Code by walking a five-rung ladder and stopping at the first rung that works:
  an official connector, an API key, a CSV export, a browser read, or a paste. Trigger on
  "connect [tool] to Claude", "wire in my CRM", "can Claude see my Asana", "hook up Lofty",
  "integrate [tool]", "read my [tool] data", "pull my contacts from [tool]", "does [tool]
  have an API", "get my data out of [tool]". Do NOT trigger for GoHighLevel (that is
  ghl-setup), for a file that is already on disk (that is contact-import), or for the
  Google and Notion connectors Claude Code already offers.
---

# Wire a tool: the ladder, not a build

The most common ask in any install session is "can Claude see my [tool]." It is not a
bespoke integration. It is a decision ladder with five rungs, and the skill's whole value
is knowing which rung this tool, this plan, and this machine land on, and saying so
plainly instead of "it can't be done."

Reads `profile/AGENT.md` and `profile/STACK.md`. Writes `profile/TOOLS.md` (one section
per tool, no secrets) and stores keys only in `.env`.

## The rule that comes first

**Creating the app in the vendor's console, clicking Allow on a consent screen,
generating an API key, and logging in are the agent's own hands. Always.** Claude opens
the page, names the button, and waits. Claude never types a password, never asks for a
secret in chat, and never reads a key back out loud. A key goes from the vendor's page
into `.env` by the agent's paste. If one lands in chat anyway, Claude writes it to `.env`
and never echoes it.

## Levels, so nothing is promised before it is proven

- **Level 1, read.** Every rung ends the same way: Claude reads the tool's data and shows
  it. Nothing is written back to the tool. Most agents live here and that is correct.
- **Level 2, write, on request.** Creating or changing a record in the tool, only when the
  agent asks, and only after Claude shows exactly what it is about to change.
- **Level 3, on a schedule.** The morning brief or a daily skill reads from the tool
  without anyone asking. Only after Level 1 has run for real, and only on a rung that
  does not need a browser open.

## Who does what

| Step | Claude | The agent (their own hands) | Why |
|---|---|---|---|
| Find out what the tool holds | Asks, then opens the tool with the agent and looks | Logs in | Nobody wires a tool nobody has looked at |
| Check the vendor's docs, this session | Opens the vendor's own developer or help page and reads it; says "unverified" for anything it did not open | Nothing | A remembered menu path is a guess |
| Rung 1: official connector | Prints the exact `claude mcp add` line with the client id filled in | Creates the app in the vendor console, enters the secret at the hidden prompt, clicks Allow in the browser | OAuth and secrets |
| Rung 2: API key | Confirms `.gitignore` covers `.env`, then verifies with one read | Generates the key on the vendor's page, pastes it into `.env` | The key is a password |
| Rung 3: CSV export | Names the export path from the vendor's docs; reads the file | Clicks Export, saves it into the workspace | Their account |
| Rung 4: browser read | Drives the logged-in browser and reads the screen into a file | Logs in; stays at the keyboard | Their session |
| Rung 5: paste | Reads whatever is pasted | Copies from the app into chat | Always works |
| Write it down | Writes `profile/TOOLS.md` and offers "save to memory" | Nothing | The habit is the product |

## The ladder

Stop at the first rung that works. Do not skip a rung because a lower one is faster; a
CSV is a snapshot and an API is live, and the agent should know which one they have.

| Rung | What | When | Credential handling |
|---|---|---|---|
| 1 | **Official connector (MCP server)** | The vendor publishes one for Claude Code | Agent creates the OAuth app in the vendor console and approves the consent screen. Client id is typed by them; the secret goes into the hidden prompt, never chat |
| 2 | **Official API with a key** | The vendor has a REST API and a key page, and the agent's plan includes API access | Key in `.env`, `.gitignore` confirmed first, verified with one read |
| 3 | **CSV export into the workspace** | No API, or the plan lacks it, or the data is small and static | None. This is the default for version one of any install |
| 4 | **Browser read** | The agent's logged-in browser can be driven by Claude on this machine | The agent logs in; Claude never types a password. Slower, and it needs the extension present |
| 5 | **Paste** | Everything else | None. Zero setup |

## Known instances, with the date each was read

Re-open the vendor page before quoting a click path in the room. These lines are true as
of the date on them and vendors move menus.

- **Asana, rung 1.** Read from developers.asana.com on 2026-09-02. Create an app at
  `https://app.asana.com/0/my-apps`, set its redirect URL to exactly
  `http://localhost:8080/callback`, then run:
  ```
  claude mcp add --transport http --client-id YOUR_CLIENT_ID --client-secret --callback-port 8080 asana https://mcp.asana.com/v2/mcp
  ```
  Claude Code prompts for the client secret with hidden input and stores it locally.
  Then the browser opens for the agent to click Allow. Prove it: "show me my Asana tasks
  due this week."
- **Asana, rung 2.** Same page (2026-09-02): a Personal Access Token is created at
  `https://app.asana.com/0/my-apps` and sent as `Authorization: Bearer <token>`. Store as
  `ASANA_TOKEN` in `.env`.
- **Asana, rung 3.** In the project: Project Actions (the arrow next to the project name)
  > Export > CSV.
- **Lofty, rung 2.** The help page for API key management returned 403 to a direct read
  on 2026-09-01 and again on 2026-09-02, so the menu path here comes from a search
  snippet only: Personal Settings > Integrations > API Keys > Create API Key, with a name,
  description and optional expiry. **Verify on the agent's own screen before relying on
  it**, and whether API access is included on their plan.
- **Lofty, rung 3.** Contacts > select all > Export. This has been run on a client
  install and is the safe default for a first session.
- **Any other tool.** Not listed means not read. Open the vendor's developer page in the
  session, decide the rung from what it says, and add a dated line here on the agent's go.

## The run, in order

1. **Ask what the tool holds and what they want out of it,** in one message. "Client
   info" is not an answer; open the tool together and look at one real record.
2. **Check the vendor, in this order:** an official connector for Claude Code, then a
   documented API with a key page, then an export button. Read the vendor's own page.
   Anything not opened this session is stated as unverified.
3. **Pick the rung and say why** in one line: "Rung 2, because the plan includes API
   access and the connector does not exist yet."
4. **Do the credential steps with the agent's hands.** Confirm `.gitignore` covers `.env`
   before any paste. Verify with exactly one read (list projects, count contacts, show one
   record) and show the result. If the read fails with 401 or 403, the key or scope is
   wrong; mint again on their screen, never guess a header.
5. **Write `profile/TOOLS.md`.** One `## <Tool>` section: what it holds, the rung used,
   the export or connect path in the agent's own words, the date verified, and the one
   read that proved it. No key, no token, no client id.
6. **Offer the memory line:** "save to memory: how I connect to [tool], and which project
   holds my client info." That sentence is the difference between a chatbot and a system.
7. **If a rung fails, say which rung is next.** Never "it cannot be done."

## What this skill will not claim

- It will not say a tool has an API, a connector, or an export button without opening the
  vendor's page in that session. A menu path from memory is marked unverified.
- It will not promise a live integration on a plan that does not include API access; it
  drops to the CSV rung and says why.
- Rung 4 needs Claude able to drive the agent's browser on that machine. If that is not
  set up, it is rung 5, and the skill says so rather than describing rung 4 as available.
- Rung 1 needs `claude mcp add` in the agent's Claude Code version; check `claude --version`
  and the command's help before quoting the line.
- It will not write to the tool at Level 1, and at Level 2 it shows the change before
  making it, every time.

## Chains from / into

Called from `contact-import` when the agent has no export yet, from `voice-command` and
`sphere-daily` when a brief wants live CRM data, and by name in a session. Routes to
`ghl-setup` for GoHighLevel and to `contact-import` once a CSV exists. Documented by
`owners-manual`.

If the user asks how this works, what it needs, or how to customize it, read
`PLAYBOOK-wire-a-tool.md` in this folder and answer from it.

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
