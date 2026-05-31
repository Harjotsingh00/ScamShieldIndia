import re

SCAM_PATTERNS = {
    "otp": 15,
    "upi": 10,
    "telegram": 10,
    "registration fee": 25,
    "security deposit": 25,
    "limited seats": 15,
    "urgent": 10,
    "click here": 15,
    "winner": 20,
    "lottery": 20,
    "kyc": 15,
    "pay now": 20,
    "offer expires": 15,
    "processing fee": 20,
    "verify account": 20,
    "bank account blocked": 25,
    "claim reward": 20,
    "guaranteed income": 20
}


def calculate_risk(text):
    """
    Returns:
        score (0-100)
        level
        matches
    """

    score = 0
    matches = []

    text = text.lower()

    for keyword, value in SCAM_PATTERNS.items():

        if keyword in text:
            score += value
            matches.append(keyword)

    # suspicious URLs
    urls = re.findall(
        r'https?://\S+',
        text
    )

    if len(urls) > 0:
        score += 10
        matches.append("external link")

    # suspicious money requests
    if "₹" in text:
        score += 10
        matches.append("money request")

    score = min(score, 100)

    if score < 20:
        level = "LOW"

    elif score < 50:
        level = "MEDIUM"

    elif score < 80:
        level = "HIGH"

    else:
        level = "CRITICAL"

    return score, level, matches