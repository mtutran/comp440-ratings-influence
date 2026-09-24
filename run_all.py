"""
Run the parts, start to finish, and say what is still missing.

    uv run python run_all.py              every part: before you submit
    uv run python run_all.py --part 3      Parts 1 to 3 only
    uv run python run_all.py --verbose     every script's full output as well

Runs measures.py's self-check, then the core Parts 1 to 3, then Part 4. Part 4, your own
recommender, is optional, like the follow-ups: it runs here, but it is never counted as missing.
Part 5 is the reflection: it has slots and no script. It never runs a follow-up: those are
optional, and they run only when you ask Claude for one. With --part N it stops after Part N, so
that a later part's results never appear before you have said what you expect from it. A part
that stops, because it failed or because what it needs is not done yet (your rule in
my_choice.py, your recommender in my_recommender.py), does not stop the others.

Each part gets one line: "ran" and how long it took; "stopped:" and the last line its script
printed, which says why; or "not run" after --part N. The scripts' own output is kept back, so
that the whole report is short enough to paste. To see a part's output, run its script, or add
--verbose to print every script's output in full above its line.

Then it lists what is missing: the slots in WRITEUP.md still holding XXXX, under each part's
"## Part N" heading, and the figures a part promises that are not in figures/. A core part
counts once it, or any later core part, has run to the end; the name and date and Part 0 always
count, and Part 5 counts once Part 3 has run, unless --part N stops before Part 5. A part that
does not count yet is listed but never held against you, so this is safe to run from the first
day. Part 4's slots and the follow-up slots are listed and never counted as missing: they are
optional. With --part N it ends with every slot under "## Part N" as it now reads, each answer
cut at 120 characters, to check that your words landed as you said them. The exit code is 0 when
nothing that counts is missing, and 1 otherwise. Presence and form only: nothing here says
whether an answer is right.
"""

import os
import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent
WRITEUP = REPO / "WRITEUP.md"
FIGURES = REPO / "figures"
# The parts with a script. part number -> (its script, the figures its docstring promises).
# Parts 1 to 3 are graded for completion. Part 5, the reflection, has slots and no script.
PARTS = {
    1: ("part1_independent.py", ["part1_strip.png"]),
    2: ("part2_recommender.py", ["part2_strip.png"]),
    3: ("part3_influence.py", ["part3_gini.png", "part3_unpredictability.png"]),
    4: ("part4_recommender.py", ["part4_recommenders.png"]),
}
LAST_PART = 5
# Part 4, your own recommender, is optional, like the follow-ups. It runs here, but it is never
# graded and never counted as missing, and Part 5 counts once Part 3 has run.
OPTIONAL_PART = 4

# The key `slots()` gives every WRITEUP.md slot under the "## Follow-ups" heading. The optional
# follow-ups are never run here, never graded and never counted as missing.
FOLLOWUPS_KEY = "followups"

# A slot in WRITEUP.md: a bold label ending in ":" or "?", then the answer: "**Label:** answer".
LABEL = re.compile(r"\*\*(.+?[:?])\s*\*\*(.*)")


def run(script, verbose):
    """Run one script with this Python. Returns its exit code, its last line of output (which
    says why when a part stops) and the seconds it took. With verbose, prints its output too."""
    if verbose:
        print(f"\n== {script} ==", flush=True)
    start, last = time.perf_counter(), ""
    process = subprocess.Popen([sys.executable, script], cwd=REPO, text=True,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               env={**os.environ, "PYTHONUNBUFFERED": "1"})
    for line in process.stdout:
        if verbose:
            print(line, end="", flush=True)
        last = line.strip() or last
    code = process.wait()
    return code, last, time.perf_counter() - start


def slots():
    """Every slot in WRITEUP.md, in order, as [part, label, answer]. Part None is the lines above
    the first heading; part FOLLOWUPS_KEY is the lines under "## Follow-ups". The answer is the
    rest of the label's line and every line under it up to the next slot label or heading, blank
    lines included, so an answer of several paragraphs is read whole; its lines are joined by
    spaces. A label may wrap over lines."""
    found, part, pending, reading = [], None, "", False
    for line in WRITEUP.read_text(encoding="utf-8").splitlines():
        if re.match(r"#+\s", line):   # a heading; "#3 for sure" is an answer, not a heading
            heading = re.match(r"##\s+Part\s+(\d+)", line)
            if heading:
                part = int(heading.group(1))
            elif re.match(r"##\s+Follow-ups", line):
                part = FOLLOWUPS_KEY
            pending, reading = "", False
            continue
        if not line.strip():
            pending = ""   # a blank line ends a wrapped label, never an answer
            continue
        text = f"{pending} {line}" if pending else line
        label = LABEL.match(text)
        if label:
            name = " ".join(label.group(1).replace("**", " ").split()).rstrip(":")
            found.append([part, name, label.group(2).strip()])
            pending, reading = "", True
        elif text.startswith("**") and "**" not in text[2:]:
            pending = text   # a label that goes on past this line
        elif reading:
            found[-1][2] = f"{found[-1][2]} {line.strip()}".strip()
    return found


def blank_slots():
    """Part number -> the labels of the slots still holding XXXX."""
    blank = {}
    for part, label, answer in slots():
        if answer == "XXXX":
            blank.setdefault(part, []).append(label)
    return blank


def print_as_written(part):
    """Every slot under "## Part N" as it now reads: the label, then the answer, cut at 120
    characters."""
    print(f"\n== Part {part}, as written ==")
    if not WRITEUP.exists():
        print("WRITEUP.md is missing.")
        return
    shown = []
    for slot_part, label, answer in slots():
        if slot_part == part:
            cut = answer[:120] + ("..." if len(answer) > 120 else "")
            shown.append(f"{label}\n  {cut or '(empty)'}")
    print("\n\n".join(shown) if shown else f"No slots under ## Part {part}.")


def through_part(argv):
    """The last part to run: LAST_PART, or N from "--part N"."""
    if "--part" in argv:
        return int(argv[argv.index("--part") + 1])
    return LAST_PART


def main():
    verbose, through = "--verbose" in sys.argv, through_part(sys.argv)
    self_check, last, _ = run("measures.py", verbose)
    print(f"measures.py self-check: {'passed' if self_check == 0 else 'failed: ' + last}")
    finished, status = set(), {}   # parts that ran to the end; part -> its one-line status
    for part, (script, _) in PARTS.items():
        if part > through:
            status[part] = f"not run, after --part {through}"
        else:
            code, last, seconds = run(script, verbose)
            if code == 0:
                finished.add(part)
                status[part] = f"ran, {seconds:.1f} s"
            else:
                status[part] = f"stopped: {last.rstrip('.') or f'exit code {code}'}"
        name = f"part {part}" + (" (optional, not counted)" if part == OPTIONAL_PART else "")
        print(f"{name}: {status[part]}", flush=True)

    print("follow-ups: optional, and not run here; ask Claude for one if you want it",
          flush=True)

    counted = {None, *range(max(finished - {OPTIONAL_PART}, default=0) + 1)}
    if through < LAST_PART:
        status[LAST_PART] = f"not reached, after --part {through}"
    elif 3 in finished:   # Part 4 is optional, so Part 5 follows Part 3
        counted.add(LAST_PART)
    else:
        status[LAST_PART] = "it counts once Part 3 has run"
    blank = blank_slots() if WRITEUP.exists() else {}
    missing = 0

    print("\n== what is missing ==")
    if self_check != 0:
        print("  measures.py's self-check failed: the measures are wrong. Tell your instructor.")
        missing += 1
    if not WRITEUP.exists():
        print("  WRITEUP.md is missing, so its slots were not checked.")
        missing += 1
    for part in [None, *range(LAST_PART + 1)]:
        name = "name and date" if part is None else f"part {part}"
        labels = blank.get(part, [])
        if part == OPTIONAL_PART:   # listed like a follow-up slot, never counted
            for label in labels:
                print(f"  part 4 slot, optional, not counted: {label}")
            continue
        if part not in counted:
            why = status.get(part, "not reached").split(":")[0]   # "stopped", "not run", ...
            count = f"{len(labels)} slot{'' if len(labels) == 1 else 's'} still XXXX"
            print(f"  {name}: does not count yet ({why}); {count}.")
            continue
        if part in status and part not in finished and part in PARTS:   # counts, did not finish
            print(f"  {name}: {status[part]}.")
            missing += 1
        for figure in PARTS.get(part, ("", []))[1]:
            if not (FIGURES / figure).exists():
                print(f"  {name}: figures/{figure} is missing.")
                missing += 1
        for label in labels:
            print(f"  {name}: still XXXX: {label}")
            missing += 1
    for label in blank.get(FOLLOWUPS_KEY, []):
        print(f"  follow-up slot, not counted: {label}")
    if not missing:
        print("  nothing, in the parts that count so far.")
    print(f"\n{missing} missing in the parts that count so far.")
    if "--part" in sys.argv:
        print_as_written(through)
    elif not missing and 5 in counted:
        print("\nWhen your work is pushed, submit the form, select \"activity\", and paste your "
              "repo's GitHub URL:\nhttps://forms.gle/mgKcnqzTGxNaGvteA")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
