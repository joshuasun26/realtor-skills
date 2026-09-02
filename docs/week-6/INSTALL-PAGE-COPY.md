# Install section — page copy

Verified 2026-09-02 against Claude Code 2.1.228 by running the install on a real machine.
Skill count verified the same day by counting `plugins/realtor-skills/skills/*/SKILL.md`.

---

## What was wrong with the old section

1. It showed `/plugin marketplace add ...` and `/plugin install ...`. Those are
   interactive terminal-only commands. They do not exist in the Claude Code desktop app,
   which is where most attendees are. This is exactly what Cassie hit.
2. Nothing said git is required. Confirmed: `marketplace add` clones the repo, so git has
   to be on the machine. The PC instructions install it already. **The Mac instructions
   do not.**
3. `build the flyer and carousel for [your address]` was getting pasted with the brackets
   still in it.
4. The page said 39 skills. It is **44** as of v0.4.0.

No GitHub account, login, or SSH key is needed. The repo is public, so it is an anonymous
clone. Only the `git` program has to exist.

---

## Section 1 — Mac only, one time

> **Mac users, do this first.** Macs do not come with git, and the skills library needs it
> to download. Open Terminal one time and paste this:
>
> ```
> git --version
> ```
>
> If it prints a version number you are done. Close it and move on. If a box pops up
> asking to install developer tools, click Install, wait for it to finish, then move on.
>
> PC users already installed git when you set up Claude Code. Skip this step.

---

## Section 2 — Install the skills, no terminal needed

> **Open Claude Code, paste this in, and hit enter.** That is the whole install.
>
> ```
> Set up my realtor skills. Please run these two commands for me:
>
> claude plugin marketplace add https://github.com/joshuasun26/realtor-skills.git
> claude plugin install realtor-skills@realtor-skills
>
> If git is not installed, walk me through installing it first. When both
> commands finish, tell me to quit and reopen Claude Code.
> ```
>
> Claude will ask permission to run them. Say yes. It takes about 20 seconds.
>
> **Then quit Claude Code and open it again.** The skills do not turn on until you
> restart. This step gets skipped a lot and it is usually why someone thinks it did not
> work.
>
> To confirm it worked, ask Claude: `what realtor skills do I have?`
> You should see 44 of them.

---

## Section 3 — Updating later

> When new skills get added, paste this into Claude Code:
>
> ```
> Run this for me: claude plugin marketplace update realtor-skills
> ```
>
> Then quit and reopen.

---

## Section 4 — New in Week 6: turn the prompts off safely

> By now Claude has asked your permission a few hundred times, and you have stopped
> reading the prompts. Everyone does. That is the problem: the one prompt that mattered
> gets the same reflex click as the forty that did not.
>
> There is a skill for fixing that properly. It turns the prompts off for the noise and
> puts real stops on the things that can cost you money or a client: destructive commands
> get refused outright, and anything that sends, posts, or spends still stops and asks you
> every single time.
>
> Paste this into Claude Code:
>
> ```
> set up safe autonomy
> ```
>
> Have these ready first, because it will stop and ask for them: one folder you always
> work in, that folder turned into a git repo (Claude does it for you, one command), and a
> backup somewhere off your laptop that has actually run at least once.
>
> It ends with a five-test drill you run with your own hands. Do not skip the drill. A
> guardrail nobody tested is a guardrail nobody has.

---

## Fix — the six example prompts

Replace the bracket placeholder with a real address so it works pasted as-is.

| Current | Change to |
|---|---|
| `build the flyer and carousel for [your address]` | `build the flyer and carousel for 1234 Main St, Arcadia CA` |

Add underneath: *"Swap in one of your own listings."*

Check the other five for the same bracket pattern. `audit my instagram`, `run my social
scan`, `import my contacts`, `revive my computer` and `edit my video` looked clean, but
verify against the live page before shipping.

---

## Also update

- "39 installed tools" becomes **"44 installed tools"**
- Remove or demote the `/plugin` lines. If they stay, label them clearly:
  *"Advanced, terminal only. Most people should use the paste block above."*
