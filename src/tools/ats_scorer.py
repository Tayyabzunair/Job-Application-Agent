"""
ATS Scorer.
Calculates how well a piece of text covers the JD's important keywords.
Used to measure improvement: original resume vs tailored content.
No LLM needed — pure keyword matching.
"""
from src.schemas import JDAnalysis, TailoredContent


def _normalize(text: str) -> str:
    """Lowercases text for case-insensitive matching."""
    return text.lower()


def keyword_coverage(text: str, keywords: list[str]) -> tuple[float, list[str], list[str]]:
    """
    Returns (score_percent, matched_keywords, missing_keywords).
    Matches a keyword if all its significant words appear in the text
    (handles plurals and word-order differences better than exact match).
    """
    text_norm = _normalize(text)
    matched = []
    missing = []

    for kw in keywords:
        kw_words = [w for w in _normalize(kw).split() if len(w) > 2]

        # A keyword counts as matched if every significant word (or its
        # singular form) is present in the text.
        found = all(
            (w in text_norm) or (w.rstrip("s") in text_norm)
            for w in kw_words
        ) if kw_words else False

        if found:
            matched.append(kw)
        else:
            missing.append(kw)

    score = (len(matched) / len(keywords) * 100) if keywords else 0.0
    return round(score, 1), matched, missing
    """
    Returns (score_percent, matched_keywords, missing_keywords).
    Score = % of JD keywords found in the text.
    """
    text_norm = _normalize(text)
    matched = []
    missing = []

    for kw in keywords:
        if _normalize(kw) in text_norm:
            matched.append(kw)
        else:
            missing.append(kw)

    score = (len(matched) / len(keywords) * 100) if keywords else 0.0
    return round(score, 1), matched, missing


def compare_ats(jd: JDAnalysis, original_resume: str, tailored: TailoredContent) -> dict:
    """
    Compares ATS keyword coverage of the original resume vs the tailored content.
    Returns a dict with before/after scores and details.
    """
    # All important keywords the ATS would scan for
    keywords = list(set(jd.key_ats_keywords + jd.must_have_skills))

    # Combine tailored content into one text block
    tailored_text = " ".join(tailored.tailored_bullets) + " " \
        + tailored.professional_summary + " " + tailored.cover_letter

    before_score, before_matched, _ = keyword_coverage(original_resume, keywords)
    after_score, after_matched, still_missing = keyword_coverage(tailored_text, keywords)

    return {
        "before_score": before_score,
        "after_score": after_score,
        "improvement": round(after_score - before_score, 1),
        "matched_after": after_matched,
        "still_missing": still_missing,
        "total_keywords": len(keywords),
    }
