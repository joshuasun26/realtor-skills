# Stop clicking Allow forty times an hour, without going reckless

### 20 minutes, once. You need git and a backup that has actually run.

## What this does for you

Right now Claude asks your permission for almost everything, and by the fortieth prompt
you are not reading them anymore. You are clicking Allow on reflex. That is worse than it
sounds, because the one prompt that actually mattered gets the exact same reflex click as
the thirty-nine that did not.

This turns the prompts off for the noise and puts real stops on the things that can cost
you money or a client. Three layers. Destructive commands get refused by the machine with
nothing to click. Anything that sends, posts, or spends still stops and asks you, every
time, even though everything else is silent now. And the rules that need judgment rather
than a setting go into a file Claude reads at the start of every session.

The honest part: this does not make Claude careful. It removes the asking. That is why
you set up the stops before you flip the switch, and why you run the drill yourself at
the end instead of taking anyone's word that it worked.

## The one command
```
set up safe autonomy
```
Open Claude Code **in your business folder** and type the line.

**Before you start, have these three.** Claude will check, and it will stop if one is
missing:
1. One folder you always work in. Not the Desktop, not Documents.
2. That folder is a git repo. It is one command and Claude will run it for you. This is
   your only real undo.
3. A backup somewhere off this laptop that has run at least once. Know the date.

## What you get back
```
Example shape, not a real run

Safe autonomy, 2026-09-10
Folder: my-ops   Git: clean, 1 commit   Backup: OneDrive, last run 2026-09-08
Settings backed up to: settings.json.bak-2026-09-10

Layer 1, deny       9 rules    destructive commands refused outright
Layer 2, ask        7 commands + 4 tools that can send or spend
Layer 3, rules      7 standing rules written to CLAUDE.md
Mode                bypassPermissions

Drill:
  1 edit a scratch file ......... PASS, no prompt
  2 git push --dry-run .......... PASS, prompted
  3 draft a text, do not send ... PASS, showed copy and waited
  4 rm -rf a scratch folder ..... PASS, refused
  5 quote a number from memory .. PASS, declined and named the source
```
Yours is built from your machine, not this example. It lands at `profile/AUTONOMY.md`,
dated, with anything that failed written down too.

## Three things that break, and the fix
1. **Nothing changed, it still asks for everything** - settings load when Claude Code
   starts, so an edit made mid-session does nothing. Fix: quit Claude Code completely,
   not just the window, and open it again. This is the number one cause by a wide margin.
2. **Test 2 does not prompt** - the ask rule has a typo in it, or it went into the wrong
   settings file because your folder has its own `.claude/settings.json` that overrides
   the main one. Fix: tell Claude "test 2 did not prompt" and let it find which file is
   actually winning. Do not call the setup done until that test passes. A missing prompt
   and a broken rule look identical from the outside, and this is the test that tells
   them apart.
3. **Everything is refused and nothing works** - a deny rule is too broad, usually a `rm`
   pattern catching ordinary commands. Fix: restore the `.bak` file Claude made in step
   one and start over. That backup exists for exactly this.
If it is none of these: screenshot it and paste it to Claude.

## Make it yours
- "Add [tool] to the ask list" - anything else you want to keep stopping on. Deploys,
  a CRM, your calendar.
- "Take git push off the ask list" - fine once you are used to it, and it stays written
  down so you know you chose it.
- "Put the standing rules back to the defaults" - restores all seven.
- "Turn this off" - sets the mode back to `default` and restarts. One line, any time.
Say "show me the skill file" and it opens `skills/safe-autonomy/SKILL.md`.

## How it works, in four lines
It reads your current `settings.json`, copies it to a dated backup, and shows you the
exact block before it writes anything. It writes three things: a deny list the machine
enforces, an ask list that keeps prompting even in bypass mode, and standing rules in
`CLAUDE.md`. Only then does it turn on bypass mode. Then you restart and run five tests
with your own hands, and the results get written down whether they passed or not.

## Related
Run **Check my setup** (`preflight`) first if you are not sure git is installed. Run
**Write my owner's manual** (`owners-manual`) after, so the setup is written down
somewhere you will find it in three months.

Still stuck? Text Joshua at 858-585-4853.
