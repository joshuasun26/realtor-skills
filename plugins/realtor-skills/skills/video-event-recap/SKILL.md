---
department: content
name: video-event-recap
description: >
  Turns a folder of raw phone clips from an event or a property into a 30-60 second
  vertical recap reel — an open house, a broker caravan, a networking event, a client
  appreciation, or a property walkthrough. Picks the best moments (sharpness, faces,
  motion — skips shaky or dark clips and says which and why), builds a simple arc
  (arrive, people, moments, close), paces cuts to be music-friendly, adds an optional
  title card, and captions only the clips where someone speaks to camera. Uses
  standard tools (ffmpeg, a word-level transcriber for spoken clips) run locally.
  Shares `profile/VIDEO-STYLE.md` with `video-talking-head` — read it first if it
  exists. Trigger on "recap reel", "event reel", "open house video", "make a reel
  from these clips", "I filmed the open house", or when the agent hands over a
  folder of clips with no other instruction. Do NOT trigger for one raw talking-head
  clip — that is `video-talking-head`.
---

# Video: Event Recap — a folder of clips in, one reel out

**The standard: right on the first render.** A folder of raw phone clips goes in. A
postable vertical recap comes out, with an honest note on any clip that got skipped
and why. The only decision left for the agent is whether to post it.

Works for any event with a folder of clips: an open house, a broker caravan, a
networking mixer, a client appreciation event, an association meeting — and for a
single property, where the "event" is a walkthrough and the "close" beat is the
address.

Built on standard tools only — `ffmpeg`/`ffprobe` for everything video and audio, a
word-level transcriber for any clip where someone talks to camera. No private
renderer, no licensed engine.

---

## Set expectations before you start

> The first recap is calibration. You'll tell me what to change — different pacing,
> bigger title text, drop a clip — and that becomes your style, saved once. Every
> recap after this needs no questions. Budget 30 to 60 minutes for this first one.

---

## Step 0 — Check your tools

```bash
ffmpeg -version
ffprobe -version
python3 -c "import faster_whisper" 2>/dev/null || pip show openai-whisper 2>/dev/null
```

You only need the transcriber if any clip has someone speaking to camera and needs
captions. Ask before installing anything missing, with the exact command for the
agent's OS, and wait for a yes.

---

## Step 1 — Ask five things, once, then stop asking

Same five questions every time, one message, no follow-up round unless an answer is
vague:

1. **What is this, and who's the host?** The event name (or the property address, if
   this is a listing/open-house recap) and the cadence line for a closing card, if
   there is one (e.g. "every 3rd Thursday" or the property's price/address).
2. **What's the one thing that happened, or the one thing about this property?**
   Not a list. A recap with no single subject plays like a random montage.
3. **Who's in the footage, and is anyone off-limits?** Faces that must not appear.
   Get this before selecting clips, not after.
4. **What's the ask, if any?** "Come to the next one," "call to schedule a tour,"
   or nothing at all — never a sales pitch if this is someone else's event.
5. **Where are the clips, and is the upload finished?** Confirm the count before
   scanning, so you are not selecting against a folder that is still filling.

Check `profile/VIDEO-STYLE.md` for caption and font defaults before asking anything
about how it should look — if it exists, do not re-ask those questions.

---

## Step 2 — Scan every clip. With your eyes, not just a script.

Pull a few sample frames per clip and actually look at them before scoring anything:

```bash
for f in raw/*.mp4 raw/*.mov; do
  ffmpeg -i "$f" -vf "select='not(mod(n\,60))'" -vsync vfr "scan/$(basename "$f" | sed 's/\..*//')_%02d.jpg"
done
```

Write a one-line inventory per clip: what's in it, is it usable, any names or faces
that need clearance. The beat plan gets built from this inventory, never from memory
of the folder's filenames.

---

## Step 3 — Score and select. Skip clips honestly, and say why.

Score every clip on three things, using tools that ship with ffmpeg:

**Sharpness** — a Laplacian-variance blur check. If OpenCV is available:
```python
import cv2, numpy as np
frame = cv2.imread("scan/clip_01.jpg", cv2.IMREAD_GRAYSCALE)
sharpness = cv2.Laplacian(frame, cv2.CV_64F).var()
```
A low variance (roughly under 50-100, but judge relative to the other clips in the
same folder — phone cameras vary) means the clip is soft or out of focus.

**Motion / shake** — ffmpeg's stabilization detector reports how much correction a
clip would need, which doubles as a shake score:
```bash
ffmpeg -i clip.mp4 -vf vidstabdetect=shakiness=10:result=clip.trf -f null -
```
A `.trf` file full of large transform values means a shaky handheld clip. If
`vidstab` isn't installed, fall back to eyeballing the sample frames from Step 2 for
obvious blur-from-motion — say plainly that the check was visual, not measured.

**Darkness** — ffmpeg's own detector:
```bash
ffmpeg -i clip.mp4 -vf blackdetect=d=0.1:pic_th=0.10 -f null - 2> black.log
```
Or just read mean brightness off `volumedetect`'s video-equivalent: sample a frame
and check its average pixel value. A very dark clip is unusable no matter how good
the moment is.

**Faces**, as a bonus signal, not a requirement — Haar-cascade face detection if
OpenCV is available. A clip with a clear face is worth more than an empty room shot,
but a strong establishing or product shot with no face is still a valid beat.

**Then decide, and say so out loud in the build notes:**

```
SKIPPED: IMG_4410.MOV — shaky (vidstab transform magnitude high), unusable
SKIPPED: IMG_4417.MOV — too dark (mean brightness well below the rest of the folder)
KEPT: IMG_4402.MOV, seconds 1.2-3.0 — sharp, well-lit crowd shot, good for "people" beat
```

Never silently drop a clip. The agent handed over that folder for a reason and
deserves to know what didn't make it and why.

---

## Step 4 — Build the arc

Four beats, in order. Not a highlight reel with no shape — a shape a stranger can
follow with the sound off.

| Beat | Job | Length |
|---|---|---|
| **Arrive** | Establish the place — the room, the sign, the front door, the property exterior. One shot. | ~2-3s |
| **People** | Who showed up, the energy in the room, buyers/agents/guests interacting. | 1-2 shots |
| **Moments** | The best evidence — the thing that actually happened, the standout room, the specific feature, the specific interaction. This is the payoff section; give it the most beats. | 3-5 shots |
| **Close** | A wide or settling shot, plus the title/end card — event name and cadence, or the property address and price/open-house time. | ~2-3s |

Total runtime: **30-60 seconds.** Under 30 rarely fits all four beats with room to
breathe; over 60 loses viewers who came for a quick recap, not a highlight film.

Cut on a steady pulse (each beat landing at a consistent, similar length rather than
wildly varying) so that whatever trending audio the agent picks in-app lands cleanly
on the cuts. **Do not bake a copyrighted music track into the file** — cut clean and
let the poster add audio in the platform's own picker, which also gets the post
better distribution than an uploaded track. If you have royalty-free or the agent's
own audio, that is the one exception; otherwise suggest 2-3 track moods as text
("upbeat, mid-tempo," "warm acoustic") rather than attaching a file.

---

## Step 5 — Captions only where someone speaks to camera

Most beats in an event recap are silent b-roll and need no captions at all — do not
caption a room-wide shot just to fill space.

For any clip where someone is talking to camera (an agent's on-camera line, a guest
testimonial, a quick interview moment):

1. Transcribe that clip specifically with word-level timestamps (same method as
   `video-talking-head` Step 2).
2. Apply the same face-clearance rule: extract frames across that clip's on-screen
   window and confirm the caption band (from `profile/VIDEO-STYLE.md`, default
   lower third) is clear of the face throughout, not just at one frame.
3. Burn the caption for that beat only.

If nobody speaks to camera anywhere in the folder, this step produces nothing, and
that is correct — do not invent captions to narrate silent b-roll.

---

## Step 6 — Optional title card

For an event: the event name and the cadence line, if there is one.
For a property: the address, and the price or the open-house day/time, pulled from
`profile/AGENT.md` for the agent's name/brokerage/license block if it's going on the
card.

Keep it simple — a solid or lightly scrimmed background, one headline, one detail
line. Same rule as any on-screen text: check it against a real rendered frame before
calling it final, not against the numbers in your head.

```bash
ffmpeg -i background.jpg -vf "drawtext=fontfile=/path/to/font.ttf:text='123 Main St':fontsize=72:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" title.png
```

For the property use case, this is the same address-as-title-card the workshop
teaches for open-house recaps — the recap ends with exactly what a viewer needs to
act (the address, the day, the price), not just a warm feeling about the event.

---

## Step 7 — Render

Concatenate the selected, scored, trimmed clips in arc order using the same
trim/setpts/concat pattern as `video-talking-head` Step 4 (a slight scale/zoom
variance per clip reads better than a hard static cut between differently-framed
handheld shots, but it is optional here — event footage already has natural camera
movement that a talking-head static shot does not).

```bash
ffmpeg -i clip1.mp4 -i clip2.mp4 -i clip3.mp4 -filter_complex "
[0:v]trim=1.2:3.0,setpts=PTS-STARTPTS,scale=1080:1920[v0];
[1:v]trim=0.5:2.8,setpts=PTS-STARTPTS,scale=1080:1920[v1];
[2:v]trim=0:2.5,setpts=PTS-STARTPTS,scale=1080:1920[v2];
[v0][v1][v2]concat=n=3:v=1:a=0[outv]
" -map "[outv]" -an recap_silent.mp4
```

Add captions (Step 5's burn-in, per-beat) and the title card (Step 6) as a final
pass, and mux back any beat-specific dialogue audio that needs to survive (a spoken
testimonial beat should keep its own audio; silent b-roll beats stay muted so the
in-app music track carries them cleanly).

---

## Step 8 — Verify by extracting frames and looking

```bash
ffmpeg -i final.mp4 -vf "fps=2" -q:v 2 qa/frame_%04d.jpg
```

Check, out loud, per beat:

- The clip in each beat is actually the clip the plan says — verify from the frame,
  not the filename.
- No caption sits on a face, chin, or hand, checked across its whole on-screen
  window.
- Nothing load-bearing (a sign, a logo, an address on a title card) is clipped at
  a frame edge.
- No word is clipped at a cut, on any beat that has dialogue.
- No dead air at the very start — frame one is already inside the arrive beat.
- Total runtime is inside 30-60 seconds.
- Vertical geometry is correct, no letterboxing.

A clean exit code is not the verdict. The frames are.

---

## Step 9 — Deliver, do not publish

Local files only: the reel, the title card image if one was made, and build notes
listing exactly which clips were kept, which were skipped and why, and what was
verified in Step 8. This skill never posts, schedules, or sends the recap anywhere —
that decision belongs to the agent, made outside this skill.

---

## Guardrails, gathered

- Never invent a name, price, date, or credential on a title card without a source
  the agent gave you this session.
- Skip clips honestly and say why — never silently drop footage.
- No copyrighted music baked into the file. Suggest moods as text, let the poster
  pick audio in-app.
- Never caption silent b-roll to manufacture content.
- Same font-substitution honesty as `video-talking-head`: say what's missing and
  what you used instead.

## Chains from / into

Reads `profile/AGENT.md` for the agent's name/brokerage/license on a property title
card. Reads and writes `profile/VIDEO-STYLE.md`, shared with `video-talking-head` —
check it first so caption and font choices stay consistent across both formats.

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
