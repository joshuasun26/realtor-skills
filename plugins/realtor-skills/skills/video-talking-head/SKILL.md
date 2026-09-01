---
department: content
name: video-talking-head
description: >
  Turns one raw phone video of the agent talking to camera into a finished vertical
  reel — silence and stumble cuts on real word boundaries, punch-in jump cuts to hide
  the seams, loudness-normalized audio, burned captions that never sit on the face,
  and an on-screen hook line in the first two seconds. Uses standard tools (ffmpeg,
  a word-level transcriber, drawtext/ASS subtitles) run locally on the agent's own
  machine. First run asks a few style questions and locks the answers into
  `profile/VIDEO-STYLE.md` so every run after that needs no questions at all. Trigger
  on "edit my video", "cut this footage", "caption this clip", "make this into a
  reel", "I recorded a video", or when the agent hands over one raw talking-head
  clip with no other instruction. Do NOT trigger for a folder of clips from an event
  or a property walkthrough — that is `video-event-recap`.
---

# Video: Talking Head — one clip in, one finished reel out

**The standard: right on the first render, not after five rounds of "make it bigger."**
One raw phone video goes in. A vertical reel comes out with the seams hidden, the
audio leveled, and captions burned in the right place. The only thing left for the
agent to do is watch it and decide whether to post it.

This skill runs entirely on standard, publicly available tools — `ffmpeg`, a
word-level speech transcriber, and `ffmpeg`'s own subtitle/drawtext burn-in. Nothing
here depends on a private renderer or a licensed font. If the agent's brand fonts
from `profile/AGENT.md` are installed locally, use them; otherwise fall back to a
named system font and say so.

---

## Set expectations before you start anything

Say this to the agent, plainly, before the first render:

> The first video is calibration, not the final answer. You are going to look at it
> and tell me what to change — bigger captions, different position, plainer hook,
> whatever is off. That feedback becomes your style, saved once. Every video after
> this one uses it automatically and needs zero questions. Budget 30 to 60 minutes
> for this first one. The payoff is every video after it.

Do not apologize for the first cut needing a revision round. That round is the
product working as designed, not a failure of it.

---

## Step 0 — Check your tools before touching the video

Run these checks first. Do not assume any of them are installed.

```bash
ffmpeg -version
ffprobe -version
python3 -c "import faster_whisper" 2>/dev/null || pip show openai-whisper 2>/dev/null
```

If `ffmpeg`/`ffprobe` are missing, they are the whole pipeline — nothing below works
without them. If no transcriber is present, you need one of `faster-whisper` or
`openai-whisper` for word-level timestamps (`faster-whisper` is faster and lighter;
either works).

**Ask before installing anything.** State what is missing and the exact install
command for the agent's OS (`winget install ffmpeg` / `brew install ffmpeg` /
`apt install ffmpeg`, `pip install faster-whisper`), and wait for a yes. Never
silently reach outside the working folder to install software.

---

## Step 1 — First run only: ask style, then lock it

Skip this entire step if `profile/VIDEO-STYLE.md` already exists — read it and go
straight to Step 2 with zero questions.

If it does not exist, ask these in one message:

1. **Caption position.** Default: **lower third**, clear of the face. Some agents
   prefer captions higher, just under a top hook — offer that as the alternative.
2. **Caption size and style.** Default: large, bold, one or two short lines,
   sentence-by-sentence (not one word flashing at a time — that reads as gimmicky
   on a realtor's channel, but say the word-by-word option exists if they want it).
3. **Hook style for the first two seconds.** Default: a short bold line across the
   chest-and-below zone stating the topic or the hook line, matching the caption
   font. Offer a "no on-screen hook, captions start immediately" option for agents
   who find hook cards busy.
4. **Font.** Use the brand font from `profile/AGENT.md` if installed locally.
   Otherwise offer 2-3 named system fonts (a bold grotesk for the hook, a clean
   sans for captions) and let the agent pick.

Build the first render off sensible defaults if the agent says "just make it good" —
do not block on this. Then, after they react to render #1, write their real answers
(including anything they corrected) into `profile/VIDEO-STYLE.md`:

```markdown
# Video Style Profile

Shared by video-talking-head and video-event-recap. Read this before asking style
questions in either skill — if it exists, do not ask again.

## Captions
Position: lower third | dynamic (checked per video for face clearance)
Font: <name>, installed locally: yes/no (fallback: <system font>)
Size: large / medium
Style: sentence-by-sentence | word-by-word
Safe margin from bottom: ~120px equivalent (clear of platform UI)

## Hook
Style: bold line, chest-and-below | pill under captions | no on-screen hook
Duration: first ~2s
Font: <name>

## Audio
Loudness target: -14 LUFS (streaming platform standard) unless the agent asked
for something else

## Corrections log
- YYYY-MM-DD: <what changed, from what to what, agent's own words>
```

**Never regenerate this file from scratch on a later run.** Read it, use it, and
only append to the corrections log when the agent asks for a change. A rebuild
silently drops prior corrections — the whole point of the file is that it
accumulates.

---

## Step 2 — Transcribe first. Never cut off a pad.

Run the transcriber with word-level timestamps before planning a single cut:

```bash
# faster-whisper (recommended — lighter, word_timestamps built in)
python3 -c "
from faster_whisper import WhisperModel
model = WhisperModel('medium.en')
segments, info = model.transcribe('input.mp4', word_timestamps=True)
for seg in segments:
    for w in seg.words:
        print(w.start, w.end, w.word)
" > words.txt

# or openai-whisper
whisper input.mp4 --model medium.en --word_timestamps True --output_format json
```

Save the word list as JSON (`start`, `end`, `word`) — every downstream step reads
this file, never the raw audio waveform, for timing.

**Use at least a `medium` model.** A small model misses names and technical terms
often enough to place a caption or a cut on the wrong word.

---

## Step 3 — Plan the cut. On word boundaries, never on a guessed pad.

Two rules, both non-negotiable:

- **A cut OUT lands in silence or on a word's real start/end timestamp from the
  transcript — never "the word ends around there, add a few frames."** A padded
  guess audibly clips syllables. If you need slack, add it in the actual silence
  gap between words, not inside a word.
- **The video starts when the agent starts talking.** Read the first word's start
  time from the transcript, subtract about 0.08-0.15s of pre-roll so the cut
  doesn't launch mid-consonant, and use that exact number as the IN point. Never
  round to 0.0 or to the nearest half second — that either clips the first
  syllable or leaves dead air that reads as "pressing record on the phone."

Find silence gaps to cut in and stumbles to remove:

```bash
ffmpeg -i input.mp4 -af silencedetect=noise=-30dB:d=0.3 -f null - 2> silence.log
```

Cross-reference silence gaps against the transcript. A stumble, a restart, or a
long pause is a candidate cut; the exact boundary is always the nearest word
start/end from the transcript, never the raw silence timestamp (silence detection
is close but not exact — the transcript is the source of truth for where a word
actually starts).

Write the kept segments as a simple list of `in,out` pairs before touching ffmpeg:

```
KEEP: 0.42,8.10  8.95,19.30  19.30,27.0
```

---

## Step 4 — Punch-in jump cuts, so the seam reads as an edit

A hard cut on a single static camera looks like a mistake. A small scale (zoom)
change exactly at the cut point reads as an intentional edit. Alternate a slight
zoom in/out at each boundary:

```bash
# per kept segment, apply a constant crop+scale (a "punch"), then concat
ffmpeg -i input.mp4 -filter_complex "
[0:v]trim=0.42:8.10,setpts=PTS-STARTPTS,scale=iw*1.00:ih*1.00,crop=iw/1.00:ih/1.00[v0];
[0:v]trim=8.95:19.30,setpts=PTS-STARTPTS,scale=iw*1.06:ih*1.06,crop=iw/1.06:ih/1.06[v1];
[0:a]atrim=0.42:8.10,asetpts=PTS-STARTPTS[a0];
[0:a]atrim=8.95:19.30,asetpts=PTS-STARTPTS[a1];
[v0][a0][v1][a1]concat=n=2:v=1:a=1[outv][outa]
" -map "[outv]" -map "[outa]" cut.mp4
```

Alternate the zoom level each segment (1.00, 1.06, 1.00, 1.10 ...) rather than a
steady climb — a steady climb across many cuts drifts the frame noticeably.
**A zoom change only ever lands exactly on a cut**, never mid-segment, or it reads
as an unstable shot instead of an edit.

---

## Step 5 — Loudness-normalize the audio

```bash
# measure first
ffmpeg -i cut.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -
# then apply using the measured values for a cleaner single pass, or just:
ffmpeg -i cut.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:v copy audio.mp4
```

-14 LUFS integrated loudness is the standard streaming platforms normalize to.
Louder just gets turned back down and loses dynamics on playback, so there is no
upside to going hotter.

**"The audio is broken" is a measurement, not a report.** Before agreeing audio is
too quiet or distorted, run `ffmpeg -af volumedetect -f null -` and quote the mean
and max dB. More than once, "no volume" has turned out to be a muted player, not a
bad render.

---

## Step 6 — Captions: measure before you burn

**A caption or hook must never sit over the face.** This is the rule most likely
to get broken by checking one convenient frame and calling it clear.

1. Extract frames across the video at a fixed interval (every ~0.4s is enough to
   catch a moving hand or chin):
   ```bash
   ffmpeg -i audio.mp4 -vf "fps=2.5" -q:v 2 frames/frame_%04d.jpg
   ```
2. Look at the frames — not one, all of them — and note where the face, chin, and
   gesturing hands actually sit across the whole clip, not just the frame where
   the agent happened to be still.
3. If no face-detection tool is available (OpenCV is the common one — `pip install
   opencv-python` and run a Haar-cascade face detector across the sampled frames
   for an automated check), do the look-and-judge pass by eye. Either way, this
   step happens before burning captions, not after.
4. Place captions in the **lower third by default**, or wherever `VIDEO-STYLE.md`
   says, but only after confirming that band is clear across the whole video. If
   the agent moves enough that no fixed band stays clear, say so and offer a
   dynamic per-shot position instead of guessing one band will work everywhere.

Build the caption track from the transcript, synced to real word timings, as an
ASS subtitle file (gives you font, size, position, and outline control that plain
`drawtext` does not) and burn it in:

```bash
ffmpeg -i audio.mp4 -vf "ass=captions.ass" -c:a copy final.mp4
```

Chunk captions into short phrases (5-8 words, one to two lines) rather than the
whole sentence at once — a caption a viewer can't finish reading before the cut
moves on is worse than no caption.

**Never let a caption's on-screen window end before the last word in it is spoken,
and never start it before the first word in it is spoken.** Re-check every caption
boundary against the word list, the same way cut boundaries were checked in Step 3.

---

## Step 7 — The hook, first two seconds

Per `VIDEO-STYLE.md`, either a bold on-screen line stating the hook (chest-and-below
zone, same face-clearance rule as captions) or straight into captions with no hook
card. If there is a hook line, it needs the same frame-by-frame clearance check as
captions — do not check the position of a static hook card at one frame and assume
it holds if the agent is moving during those two seconds.

---

## Step 8 — Verify by extracting frames and looking

**Render is not done at exit code 0.** Before calling anything finished:

```bash
ffmpeg -i final.mp4 -vf "fps=2" -q:v 2 qa/frame_%04d.jpg
```

Open the frames and check, out loud, one by one:

- No caption or hook text touches a face, chin, or hand, anywhere in its on-screen
  window — not just at one timestamp.
- No word is clipped at a cut (spot-check a few boundaries against the transcript).
- No dead air before the first word — frame one is already the hook or the speech.
- Vertical geometry is correct (1080x1920 or the platform's target), no letterboxing.
- Nothing important sits in the bottom ~120px — the app's own UI covers it in feed.
- Audio is present and its measured level matches Step 5's target.

A script that exits cleanly is not a verdict. The frames are the verdict.

---

## Step 9 — Deliver

Local file only. This skill does not post, schedule, or send anything anywhere —
that is the agent's decision, made outside this skill. Hand back:

- The finished file path
- Runtime
- The measured audio levels
- One line per Step 8 check: what was checked, what it showed

If anything in Step 8 failed, fix it and re-render before calling the job done —
never deliver a file with a known issue and a note about it instead of fixing it.

---

## Guardrails, gathered

- Never burn a claim, name, date, price, or rate onto the screen without a source
  the agent gave you this session.
- Never post or send the finished video. Hand it off and stop.
- Never silently substitute a font — say what's missing and what you used instead.
- Never regenerate `profile/VIDEO-STYLE.md` from scratch once it exists — edit in
  place and log the change.

## Chains from / into

Reads `profile/AGENT.md` for brand fonts if set. Reads and writes
`profile/VIDEO-STYLE.md`, shared with `video-event-recap` — check it there first so
style is consistent across both formats.

---

<!-- self-improvement-loop v1 -->

## Self-improvement loop

Before ending a run of this skill, review the run:

1. Did any step fail, stall, or need a workaround you had to invent?
2. Did the agent correct, reject, or rewrite something meaningful in the output?
3. Did you discover something a future run would want to know (a path that moved, a
   tool that replaced another, a preference they stated out loud)?

If yes to any, propose a specific edit to this SKILL.md in one or two lines and ask
whether to apply it. Propose only changes that would alter a future run's behavior --
skip cosmetic rewording, and never propose more than two edits at once.

Do not edit this file without their go-ahead. If they say no, drop it and do not
re-raise the same suggestion in a later run of the same session.
