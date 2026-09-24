---
name: checkpoint
description: The end-of-activity check. Run it once, when Parts 0 to 3 and Part 5 are done and before submission - or mid-activity if the student asks what is missing. Runs run_all.py, names the blank writeup slots that count, and confirms this session is in TRANSCRIPT.md.
---

Each part of the activity ends with a commit, not a checkpoint. This skill runs **once**, at
the end, before the student submits. Run it earlier only if they ask where they are; then pass
`--part N` for the part being worked on, so a later part's results do not appear before they have
said what they expect from it.

Three steps, in this order. Stop at the first thing missing: that is the current step.

1. Run `uv run python run_all.py` and paste its output in full: every line, copied into your
   reply. A summary, or "see above", fails this step. Mid-activity, run
   `uv run python run_all.py --part N` instead, which also prints an "as written" block showing
   the student their words as they landed. Do not say whether the numbers look right.
2. Name, one line each, every slot the output lists as still `XXXX`, and ask what each needs; do
   not suggest wording. If a slot's text is not what the student typed, say so and fix it to
   their words. A prediction slot that a result has contradicted is not reworded; the "Revisited"
   slot at the end of Part 3 takes the later thought.

   **Part 4's slots, and the follow-up slots at the end of `WRITEUP.md`, never count: they are
   optional.** `run_all.py` prints them as "part 4 slot, optional, not counted" and "follow-up
   slot, not counted". Leave them as `XXXX` unless the student did Part 4 or that follow-up, and
   do not ask them to fill them.
3. Run `uv run python dump_transcript.py` and paste its last line. It says how many sessions are
   in `TRANSCRIPT.md` and whether this session is one of them. If the script fails on their
   machine, say so and go on: it costs them nothing.

Then go on to the submission steps in `CLAUDE.md`. If anything the student has done since their
last commit is uncommitted, ask whether they are ready to commit it, and on a yes:

```
git add -A
git commit -m "Part 5 done"
```

Nothing here is a judgment about the work. Presence and form only.
