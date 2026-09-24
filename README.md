# COMP 440: Ratings and Social Influence, a simulated market with Claude

**Fall 2026 · Individual · Counts as one reading reflection or activity · graded for completion**
**Due Tue Oct 6, 8:00am Central**

This is graded for completion of parts 0-3 and part 5. Part 4 and the follow-ups at the end are
optional and are not graded. Questions go to `#comp440-f26`.

**When you are finished, complete the [Work Submission Form](https://forms.gle/mgKcnqzTGxNaGvteA), select "activity" and share the URL to your GitHub repo in the textbox.**

## Goals

* To have you compute numbers behind the paper's two claims: inequality and unpredictability.
* To incorporate social influence into a model yourself and watch what it changes.
* To understand the possibilities and limitations of simulations, and see how they shift by
  changing assumptions.

## Overview

[Salganik, Dodds and Watts](https://www.princeton.edu/~mjs3/salganik_dodds_watts06_full.pdf)
built an artificial music market: 14,341 people downloaded songs in
eight separate worlds where they could see each song's download count and one world where they
could not. A song could be a hit in one world and a flop in another.

You will run a small version of that market hundreds of times.

* Eleven artists have a hidden **true popularity**. If users picked independently (without
  social influence) the distribution of artist downloads would reflect that value.
* Each simulated user is shown five artists by a recommender and then picks one.
* A world is 1,000 users in a row.
* You run hundreds of worlds from the same start and measure how unequal each world ends up and
  how much the worlds differ from each other.

The model ships with users who ignore the download counts (the independent world). You will add
social influence.

## The measures

Every part prints the same five measures for each condition it runs. `measures.py` has the
exact formulas.

* **Gini**: inequality within a world, the paper's Figure 1. 0 means every artist has the same
  share of the downloads; 0.91 means one artist has all of them. The table shows the average
  over worlds.
* **Unpredictability**: how differently identical worlds end, the paper's Figure 2. For each
  artist, the average difference in its share between two worlds, then the average over artists.
  0 means every world ends the same way.
* **Fidelity**: how closely a world ranks the artists in the order of their true popularity. 1
  means the same order; 0 means no relation.
* **True best wins**: the fraction of worlds in which the Beatles (true popularity 100) end with
  the largest share.
* **Accidental hits**: the fraction of worlds in which an artist with true popularity 30 or less
  ends with the largest share.

## How this activity works

1. Claude codes, runs the simulation, computes the measures and draws the figures.
2. You determine approaches and strategies, hypothesize about what will happen, and interpret the results.
3. Claude leads each step by asking you a question. You answer in a word or a sentence, and
   Claude writes your answer into `WRITEUP.md` exactly as you said it. To have anything run,
   shown or changed, ask Claude; you do not need to edit any file yourself.
4. If you are stuck, ask Claude for a hint. It will give as many as you need, starting small,
   without giving you the answer.

Claude records the transcript of your sessions to share with Shilad.

## The task

Parts 0 to 3 and Part 5, about 70 minutes together; Part 4 is optional. Part 3 is the long one. The minutes are a guide (and Claude's prediction).

### Part 0. Predictions · about 5 minutes

Fork this repo, clone your fork, start `claude`, and type `/setup`. Claude asks your name, then
four questions. Answer each in a word or a line. Claude commits your answers before anything
runs; that is what they are for.

### Part 1. Users on their own · about 8 minutes

Claude runs `part1_independent.py`. In this version of the simulation, each user sees five random
artists and picks independently by taste with no social influence. The simulation prints the five
measures and one world's shares, and draws a strip plot: one column per artist, one dot per world.
Claude then asks you two things: what Gini and unpredictability each show, in your own words, and
what the figure shows, in one sentence.

### Part 2. The recommender · about 10 minutes

Claude shows you `recommender.py`, which is short. A recommender returns two things: the five
artists to show, top of the list first, and the download counts shown with them. Claude asks
you about the capabilities and limitations of the `top_five` mechanisms. If you have the code
wrong, Claude corrects you and asks what you want recorded about the correction.

Claude then runs `part2_recommender.py`: the same users, still ignoring the counts, now see the
five most downloaded artists. Claude asks what changed against Part 1, in one sentence.

### Part 3. Social influence · about 40 minutes

The simulation's choice rule decides what song a user picks from the five shown by the
recommender. The one originally in this repo, `independent_choice` in `choose.py`, ignores the
counts. In other words, social influence plays no role in a user's choice. You will design a
choice rule, and Claude will implement it in `my_choice.py`.

There is no single right rule. Some things to consider as you design your rule:

* Whether a user favors artists that have more downloads.
* Whether an artist with no downloads can be selected.
* Whether artists nearer the top of the recommendation list are more likely to be picked.
* How `social_influence`, which ranges from 0 to 1, affects the above.

1. Claude asks you a few questions to pin down your rule: how the counts should change what a
   user picks, how `social_influence`, from 0 to 1, should set the mix between the counts and a
   user's own taste, and whether an artist's place on the list should matter. Claude writes the
   rule into `my_choice.py` from your answers and shows you the code.
2. The hand check. Claude shows you a two-artist case and asks which artist your rule should
   favor, and by a little or a lot. Then it runs `hand_check.py`, which prints each step of your
   rule computed on that case, and asks whether the result matches what you said. If it does not,
   Claude asks what you want to change.
3. Claude asks what shape you expect the curves to have, then runs `part3_influence.py` at
   social-influence levels 0, 0.25, 0.5, 0.75 and 1. You may ask for other levels, but you do
   not have to.
4. Claude points out problems it sees in your rule, as questions: for example, whether an
   artist with no downloads can ever be picked. It does not say what the curves show. If you
   want to change your rule, Claude changes it, shows you the change, and reruns Part 3 once.
5. Claude asks what the two curves show against the paper's Figures 1 and 2, in one or two
   sentences: direction, not size.
6. Claude shows your four Part 0 predictions as you wrote them and asks which you would now
   change, and why.

### Part 4. Your recommender (optional) · about 15 minutes

Optional, and not graded, like the follow-ups. You can skip it and go straight from Part 3 to
Part 5; a skipped Part 4 is never counted as missing. If you have already started it, you may
finish it or stop and go to Part 5. If you want to do it, ask Claude for it.

A recommender sees only the download counts, never true popularity. It decides which five artists
to show, in what order, and what counts to show with them. Claude asks for a rule of your own, in
words, before any code: for example, show no counts at all, show every count divided by ten, or
keep one of the five spots for a random artist. Claude asks what you expect your rule to do to
inequality, unpredictability and fidelity, writes `my_recommender.py` from your description, and
runs `part4_recommender.py`. It compares your rule with `top_five` and `random_five`, all three
with your Part 3 rule at social influence 0.5. Some rules will not move the numbers; that is a
result. Claude asks for one sentence: what your rule buys and what it costs.

### Part 5. Reflection · about 5 minutes

Claude asks two questions and writes your answers into `WRITEUP.md`. First, where does this show
up in data you have already handled, or in an interface you use: HW1's figure of when a movie's
tags and ratings arrived, HW0's three rankings, the "Popular on Netflix" row in the Sep 22
reading? Second, a moment Claude was wrong or overconfident, or a judgment you kept for yourself.

## Follow-ups

Optional, and not graded, like Part 4. Claude offers them once, after Part 5, with Part 4 if you
have not done it. Ask for one if you want it; do none and you have still finished the activity.
Their slots are at the end of `WRITEUP.md`, and `run_all.py` neither runs them nor counts them as
missing.

* **What is shown.** `followup_shown.py`: two markets at the same social influence, both showing
  the five most downloaded artists, one in a random order and one sorted by count — the paper's
  experiments 1 and 2. It draws the paper's Figure 3 for each: an artist's share when nobody saw
  counts (its quality) against its share in each world (its success). Which market moved success
  further from quality?
* **One assumption.** `followup_assumption.py`: pick one thing your rule or the model
  assumes — how your rule treats list position or artists with no downloads, how fast the counts
  pull, that the recommender only ever shows artists that already have a download, or 1,000 users
  per world. Claude makes the change there, so the files Parts 1 to 4
  used stay as they were, and reruns Part 3's levels without and with the change. Did the
  conclusion survive?
* **More recommenders.** Ask Claude for a second and a third rule in Part 4's shape, and compare
  them.
* **More worlds.** Every script runs 300 worlds. Ask Claude to rerun a part with 1,000 and see
  which numbers move and which only get steadier.

## Submitting

When Parts 0 to 3 and Part 5 are done, Claude runs `/checkpoint`, which lists anything still
missing. Then ask Claude to commit and push, and fill in the form:
https://forms.gle/mgKcnqzTGxNaGvteA. Tell Claude when you have. It will say **YOU ARE FINISHED!**

## AI guidelines

**No AI**: every sentence in `WRITEUP.md` that says what you expect, what a figure shows, or why
you chose something; the rule in Part 3 and the recommender in Part 4 as you describe them. Claude
writes down what you said, word for word.

**Never edited by anyone**: `TRANSCRIPT.md`, `run_all.py`, `measures.py`, `recommender.py`,
`sim.py`, `artists.py`, `choose.py` and `hand_check.py`; and `my_choice.py` once Part 3 is
done. Part 4 and the follow-ups write new functions of their own; none of them changes the
Part 3 rule.

**AI encouraged**: all the code, the figures, and any extra experiment you want to run.

## Rubric

Graded for completion. A part is complete when its script has run and its slots in `WRITEUP.md`
hold your own words. I do not grade whether a prediction came true or whether a reading is the
one I would have written. `uv run python run_all.py` lists what is still missing, and never counts
Part 4 or the follow-ups; when it says nothing is missing, the activity is complete.

| Part | Complete when |
|---|---|
| 0. Predictions | Four predictions committed before anything runs |
| 1. Users on their own | `part1_independent.py` has run; what the two measures show and what the figure shows, in your words |
| 2. The recommender | `part2_recommender.py` has run; `top_five` in your words, what Claude corrected, what changed |
| 3. Social influence | Your rule in your words and in `my_choice.py`, your two hand-check answers, the shape you expected, what you changed, `part3_influence.py` has run, what the curves show, and the revisited predictions |
| 5. Reflection | Both sentences |
| 4. Your recommender | Optional. Not graded, and never counted as missing |
| Follow-ups | Optional. Not graded, and never counted as missing |

## Talk to me if...

**You would rather not use Claude.** Talk to me; there is no grade effect.

**Claude, or something else, is down.** A reported problem never costs you points; post in
`#comp440-f26` or email me. An outage of more than about half a day extends the deadline by 48
hours.

**Claude will not make your predictions, pick your rule, or say what a figure shows.** Working as
intended; those are the assignment. It will give you hints toward any of them; ask for one.
