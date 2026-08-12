# Photo Beshno — Lightroom→Instagram photo pipeline

Drives one photo from the Lightroom `instagram` album through
fetch → GPT quality-enhance → Telegram title pick → Telegram story pick →
Telegram schedule confirm → auto-advance to the next photo. Always exactly
one photo "in flight" (`pipeline_state` outside `{scheduled, posted,
rejected}`) at a time. Invoked two ways:

- **Automatically**, by the sibling automation repo's `handle_photo_pipeline_trigger.py`
  (see `scripts/telegram_send.py`'s docstring for how this bridge works — its
  repo/path is never named here, this repo is public), whenever Bahman
  replies in Telegram to a message this pipeline sent — it writes a handoff
  file to `images/ig-queue/_inbox/<message_id>.json` before launching this
  skill.
- **Manually**, `claude -p "/photo-beshno"` with no handoff pending — used to
  bootstrap the very first cycle, or to nudge the pipeline if nothing is in
  flight for some reason.

Sending is always via `scripts/telegram_send.py` (which shells out to that
sibling repo's own `notify_telegram.py` — never talk to the Telegram API
directly from this repo, and never run a `getUpdates` consumer here; see
that script's docstring for why). Receiving is always via the handoff file
in `images/ig-queue/_inbox/` — this skill never calls Telegram itself to
check for replies.

## Steps

### 0. Sync

`git remote get-url origin 2>/dev/null` — if a remote exists, `git pull --ff-only`.
Report what changed or "already up to date"; continue either way on failure.

### 1. Read the queue state

- List `images/ig-queue/_inbox/*.json` (Telegram-reply handoff files, if any).
- List `images/ig-queue/*.json` records; find the one **in flight**
  (`pipeline_state` present and not in `{"scheduled", "posted", "rejected"}`).
  There should never be more than one — if there is, stop and report it as a
  bug rather than guessing which to act on.

Branch:
- **A handoff file exists, matching an in-flight record's `asset_id`** → go
  to the step below for that record's current `pipeline_state`. Delete the
  handoff file once fully processed (success or handled failure).
- **A handoff file exists but there's no matching in-flight record** (stale —
  e.g. a reply arrived after the pipeline already moved on, most often
  because the record it was replying to already reached `scheduled`) →
  delete it, but **do not just silently drop it if `reply_text` reads like a
  real question or comment**, not a redundant confirmation/no-op. Confirmed
  real 2026-08-12: Bahman asked (as a reply on an already-`scheduled` «شادی»
  message) whether the tagline-in-scene style was actually applied to that
  photo's story graphic — the run correctly identified the handoff as stale,
  investigated, found the real answer (yes, it was applied correctly), then
  just reported that internally and stopped without ever telling him,
  because this run is unattended `claude -p` with no one to ask "should I
  send this?" If `reply_text` is a redundant no-op (an already-superseded
  "تایید می‌کنم" on a schedule that's already confirmed, etc.), silently
  dropping it is still fine. If it reads as a genuine question/comment, send
  a short `telegram_send.py --reply-to <message_id>` answering it directly
  (using whatever you can determine from the record/files) before deleting
  the handoff — don't leave Bahman's question unanswered just because the
  pipeline itself has moved on.
- **No handoff file, no in-flight record** → this is a bootstrap/manual run.
  Go to step 2.
- **No handoff file, but an in-flight record exists** → nothing to do yet;
  report the current `pipeline_state` and stop. Do not fabricate a reply.

### 2. No active record → start the next photo

1. `scripts/.venv/bin/python scripts/lr_fetch_photo.py` — picks one random
   unprocessed asset from the album, downloads it at the largest available
   rendition (2048px) to `images/ig-queue/_source/<asset_id>.jpg`, writes the
   initial record with `pipeline_state: "enhancing"`.
   - If it reports no unprocessed photos left, tell Bahman via
     `telegram_send.py` that the album queue is empty and stop — don't loop.
2. **Read** `images/ig-queue/_source/<asset_id>.jpg` (the Read tool) — actually
   look at the photo before writing a prompt.
3. Write a **photo-specific** quality-enhance prompt (not a fixed template):
   describe what "ready to publish on Instagram" means for *this* photo —
   e.g. sharpening/denoise appropriate to the actual visible softness or
   grain, exposure/contrast/color balance issues actually present, cleaning
   up genuine sensor dust/artifacts if visible. Never invent new content,
   never change composition/cropping, never alter what's actually in the
   frame (people, objects, setting) — this is a quality pass, not a redraw.
4. `scripts/.venv/bin/python scripts/gpt_enhance_photo.py <asset_id> --prompt "<prompt>"`
   — writes the final, already-optimized `images/ig-queue/<asset_id>.jpg`
   (auto-retries once on an OpenAI `moderation_blocked` response — confirmed
   2026-08-12 this can happen on photos of children even for a plain quality
   pass — then falls back to an optimize-only copy of the source with no AI
   enhancement if it's rejected twice; **never** reword the prompt to try to
   route around a moderation block). Its stdout says which path was taken —
   read it.
5. **Read** the result and sanity-check it actually still looks like the same
   photo (gpt-image-2 edits can occasionally drift) — if it looks wrong,
   note that in the Telegram message so Bahman knows to watch for it, rather
   than silently sending a bad result. If the fallback path was used (GPT
   rejected it), mention that plainly in the Telegram message too — it's not
   a failure to hide, just means this one has no AI quality pass.
6. Write **6-7 title suggestions**. Per `feedback_photo_naming_style.md`
   (two confirmed calibration points so far: «یارو» over 9 poetic options;
   deadpan story over mystical one) — lead with a few short, blunt,
   colloquial/slang options, and include 1-2 more poetic ones for real
   contrast, not as filler.
7. `scripts/.venv/bin/python scripts/telegram_send.py "<message with the numbered title options>" --asset-id <asset_id> --stage awaiting_title --file images/ig-queue/<asset_id>.jpg`
8. Update the record: `pipeline_state: "awaiting_title"`.
9. Report in chat what was sent, then stop — waiting for Bahman's reply.

### 3. `pipeline_state: "awaiting_title"` + handoff → title picked

1. Read `context.text` from the handoff (Bahman's reply) — it may be one of
   the numbered options verbatim, a paraphrase, or something else entirely
   (he's picked something not offered before — «یارو» itself was not one of
   the 9 options offered). Use judgment, not strict matching.
2. Save `record["title"]`.
3. **Update `feedback_photo_naming_style.md`** with this new data point
   (what was offered vs. what was picked) — keep sharpening the calibration
   note every time, per the standing rule.
4. Read `images/ig-queue/_story_universe.md` for continuity.
5. **Draft the 2 story options via the Agent tool, model `opus`** (standing
   rule, 2026-08-12 — Bahman wants the actual creative writing at a higher
   tier than the rest of this skill's mechanical steps; mirrors the same
   Sonnet-for-mechanical/Opus-for-Persian-prose split already used in other
   sessions — see memory `feedback_model_switching_workflow.md`). Give the
   subagent: the photo itself (path), the chosen title, the full contents of
   `_story_universe.md`, and the relevant calibration notes from
   `feedback_photo_naming_style.md` (deadpan-over-lyrical axis; indirection
   axis — don't restate the title's word or literally describe the pictured
   subjects, route through an indirect symbol/object/fragment instead,
   judged fresh per photo, not a fixed formula). Ask for exactly **2**
   distinct options, connected to the shared universe where it fits
   naturally (never forced), **Persian only** (standing rule, 2026-08-12 —
   do not draft an English translation until Bahman has actually approved a
   specific Persian story; translation happens in step 4 below, after a
   pick). Relay the subagent's two options as-is.
6. `telegram_send.py "<both Persian-only story options, clearly labeled>" --asset-id <asset_id> --stage awaiting_story` (no `--file` — text only).
7. Update the record: `pipeline_state: "awaiting_story"`.
8. Delete the handoff file. Report and stop.

### 4. `pipeline_state: "awaiting_story"` + handoff → story picked, or feedback

If the reply doesn't actually pick one of the offered options (rejects both,
asks for changes, gives new instructions) — do **not** advance
`pipeline_state`. Instead: take the feedback into account (pass it to the
Opus subagent verbatim, alongside everything from step 3.5 above), draft a
**fresh** pair of Persian-only options the same way, send them via
`telegram_send.py` with the same `--stage awaiting_story`, delete the
handoff file, and stop — waiting for the next reply. Only proceed with the
numbered steps below once a specific story is actually picked.

1. Save the chosen story text to `record["story"]`.
2. **Update `feedback_photo_naming_style.md`** with this data point too.
3. Build the final caption in the already-locked format (see CLAUDE.md's
   "Caption workflow (per photo)" under Personal Photo Series): title in «»
   quotes on its own line, the chosen story in Persian then its English
   translation, the fixed bilingual closing line, then ~28-30 hashtags
   (Persian+English mixed, high-volume/trending over niche invented ones,
   plus the series tags and always `#هوش‌واره`). Save to `record["caption"]`.
4. Append a short entry to `images/ig-queue/_story_universe.md` (photo title,
   one-line story summary, any named recurring motif introduced).
4.5. Generate this photo's Instagram Story typography graphic:
   `scripts/.venv/bin/python scripts/gpt_story_typography.py <asset_id> --prompt "<bespoke prompt>"`
   — **write a fresh, story-themed prompt every time** (same principle as the
   GPT-enhance prompt in step 2 — never call this without `--prompt`, the
   generic default was explicitly rejected as "not creative enough," 2026-08-12).
   Ground the prompt in the actual chosen story's imagery/mood (see یارو's
   dusty-golden-hour/faint-footprints treatment and مذهب's
   worn-pilgrimage-path treatment as the two references so far) — atmospheric
   photo treatment + the tagline woven into the scene (etched/weathered/set
   into the environment), not a flat gradient box with centered text. Falls
   back automatically to a Playwright/Vazirmatn overlay if gpt-image-2
   moderation-blocks the photo twice (confirmed to recur on photos with
   children) — that fallback can't be made thematic, note it plainly if it
   was used. Result lands at `images/ig-queue/stories/<asset_id>.jpg`.
   Then `scripts/.venv/bin/python scripts/make_story_video.py <asset_id>` —
   turns the static graphic into a ~12s vertical MP4 with a **random**
   segment of `assets/audio/dunya-bozorgtar-theme.mp3` (never always the
   start of the track — standing rule, 2026-08-12) faded in/out underneath.
   Instagram only shows a static photo Story for ~5s; the video keeps it on
   screen the full clip length. Result: `images/ig-queue/stories/<asset_id>.mp4`.
   **Send the video (not the static jpg) to Telegram right away** (standing
   rule, 2026-08-12 — Bahman wants to see every story as it's made, not just
   the feed photo): `telegram_send.py "<short note on which version — AI or
   fallback>" --asset-id <asset_id> --stage story_preview --file
   images/ig-queue/stories/<asset_id>.mp4`. This is FYI, not a gate — do not
   wait for a reply before continuing to the caption/schedule step below.
5. Propose a `scheduled_for` slot (corrected 2026-08-12 — the original "~7
   days out" default was wrong, Bahman explicitly wants posting to start
   **tomorrow**, not next week): take the latest `scheduled_for` across all
   existing records; if none, or if it's already in the past, propose
   **tomorrow**; otherwise propose the day after the latest one — i.e.
   roughly one photo per day, sequential, no artificial gap. Pick a specific
   time using general Instagram-engagement best-practice info (e.g. evening
   hours) until real post-performance stats exist for this account — once
   there's a real posting history, look at it and refine the time choice
   from actual data instead of general advice. This is still just a
   starting proposal, not a fixed rule — Bahman may ask for a different
   date/time, same as the title/story calibration. Use the machine's local
   time (`date`, Europe/Madrid) — `scheduled_for` is stored as a naive local
   ISO datetime (`YYYY-MM-DDTHH:MM:SS`), matching `lr_check_schedule.py`'s
   comparison.
6. `telegram_send.py` the full caption + proposed date/time, asking for
   confirmation or a different time.
7. Update the record: `pipeline_state: "awaiting_schedule"`.
8. Delete the handoff file. Report and stop.

### 5. `pipeline_state: "awaiting_schedule"` + handoff → schedule confirmed or adjusted

- **Confirmed** (explicit yes, or a restated time that matches what was
  proposed): set `record["scheduled_for"]` (final ISO datetime),
  `pipeline_state: "scheduled"`, `status: "approved"`.
  - **Commit and push** `images/ig-queue/<asset_id>.jpg`,
    `images/ig-queue/<asset_id>.json`, `images/ig-queue/_story_universe.md`,
    and any touched memory files. This is the one point in the flow where a
    commit/push happens without a separate explicit ask — Bahman's schedule
    confirmation in Telegram *is* the explicit go-ahead for this specific
    photo (same reasoning as kavosh's own scheduler: "the approval on the
    rendered asset is the authorization, given earlier rather than
    skipped"), and this run is unattended (no one to ask further). The image
    must be public before `lr_check_schedule.py` can ever publish it.
  - Reply in Telegram confirming the scheduled date/time.
  - Delete the handoff file.
  - **Same run, immediately**: go back to step 2 and start the next photo —
    this is what keeps exactly one photo in the queue at all times without a
    separate manual re-trigger. **Do this unconditionally, every time, no
    exceptions** — confirmed 2026-08-12 that skipping this "just this once"
    (deferring it with "I'll send the next one whenever you're ready" mid a
    busy moment) actually broke the queue-of-one guarantee: nothing else
    would have ever restarted it, since nothing calls `/photo-beshno` except
    a reply to a message this pipeline itself sent. Bahman had to notice
    and ask. There is no such thing as "start it later" — either continue
    to step 2 right now, in this same run, or the pipeline silently stops.
- **Wants a different time**: re-propose based on what Bahman asked for,
  stay in `pipeline_state: "awaiting_schedule"`, reply in Telegram, delete
  the handoff file, stop (waiting for the next confirmation).

### 6. Report

Short chat summary: what stage ran, what was sent to Telegram, what's next
(waiting for a reply, or a new cycle already started).

## Never do

- **Never run any step of this skill as a background task and wait for a
  harness notification** (e.g. Bash tool's `run_in_background`, or any
  "I'll wait for the async job to finish" pattern) — this includes
  `gpt_story_typography.py` and `make_story_video.py` in step 4.5, which can
  each take a while and may look like good background candidates. This
  skill is always invoked via a one-shot `claude -p` (see the automatic
  trigger above) — there is no later turn for a notification to land in.
  Confirmed real 2026-08-12: a run backgrounded `gpt_story_typography.py`
  and ended its turn "waiting" for the notification; since `claude -p` has
  no such later turn, the process just exited (success, exit 0) with the
  step never finished, the handoff file never deleted, and no error
  anywhere — the pipeline silently stalled at `awaiting_story` with the
  story/caption already saved but nothing past it. Always run every step of
  this skill synchronously in the foreground, however long it takes.
- Never run a Telegram `getUpdates` consumer from this repo — always go
  through `telegram_send.py` (send) and the `_inbox/` handoff (receive).
- Never publish anything directly from this skill — publishing only happens
  via `lr_check_schedule.py` once `scheduled_for` has actually passed, or via
  a manual `lr_publish_photo.py --confirm-publish` Bahman runs himself.
- Never commit/push before a schedule is actually confirmed — a photo whose
  title/story is still being picked has no reason to be public yet.
- Never invent a title or story pick that wasn't actually in `context.text`
  — if a reply is ambiguous, ask for clarification via `telegram_send.py`
  instead of guessing which option was meant.
- Never skip updating `feedback_photo_naming_style.md` on a title or story
  pick — this calibration is the whole point of offering choices each time.
