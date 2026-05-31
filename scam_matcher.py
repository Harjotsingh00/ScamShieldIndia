import pandas as pd
from difflib import SequenceMatcher


def similarity(a, b):
    """
    Returns similarity score between 0 and 1
    """

    return SequenceMatcher(
        None,
        str(a).lower(),
        str(b).lower()
    ).ratio()


def find_similar_scam(user_text):
    """
    Finds closest scam example
    """

    try:

        df = pd.read_csv(
            "data/scams.csv"
        )

        best_match = "Unknown"

        highest_score = 0

        for _, row in df.iterrows():

            score = similarity(
                user_text,
                row["example"]
            )

            if score > highest_score:

                highest_score = score

                best_match = row["scam_type"]

        return (
            best_match,
            round(
                highest_score * 100,
                2
            )
        )

    except Exception:

        return (
            "Unknown",
            0
        )