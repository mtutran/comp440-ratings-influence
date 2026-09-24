"""
Your choice rule, for Part 3.

You design the rule. Claude asks you questions about it, writes it here from your answers, and
shows you the code. Then `uv run python hand_check.py` shows each step of your rule on a
two-artist case, so you can say whether each step does what you meant.
"""

import math

from artists import TRUE_POPULARITY
from choose import normalize, step


def my_choice(shown, counts, social_influence):
    """Return the chance that a user picks each shown artist: a list of numbers, one per artist
    in `shown` and in the same order, summing to 1.

    shown              the artists on the list, top first (positions 0, 1, 2, ...)
    counts             the download counts shown with the artists, artist -> number; an artist
                       shown without a count is missing, so read it as counts.get(artist, 0)
    social_influence   from 0 (users ignore the counts) to 1 (users go by the counts alone)

    The rule may use `normalize`, which scales a list of weights so they sum to 1, and
    TRUE_POPULARITY, which gives each artist its hidden true popularity. `step` labels each
    stage of the rule, so that hand_check.py can show it.
    """
    # Own taste: each shown artist's true popularity as a share of the five.
    taste = step("taste share: true popularity scaled to sum to 1",
                 normalize([TRUE_POPULARITY[artist] for artist in shown]))

    # Counts: twice the downloads gives 1.5 times the weight, so the weight is
    # downloads ** log2(1.5); an artist with no downloads gets half the weight of one download.
    weights = step("counts weight: downloads ** log2(1.5), or 0.5 with no downloads",
                   [counts.get(artist, 0) ** math.log2(1.5) if counts.get(artist, 0) > 0 else 0.5
                    for artist in shown])
    social = step("social share: the counts weights scaled to sum to 1", normalize(weights))

    # The mix: social_influence of the chance comes from the counts, the rest from taste.
    # Position on the list plays no part.
    return step("chance: social_influence * social share + (1 - social_influence) * taste share",
                [social_influence * s + (1 - social_influence) * t
                 for s, t in zip(social, taste)])
