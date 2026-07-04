"""
Job Fetcher.
Fetches live job listings from the RemoteOK public API (free, no key).
This is API-based, not scraping — safe and ToS-friendly.
"""
import requests

REMOTEOK_API = "https://remoteok.com/api"

# RemoteOK requires a User-Agent header, otherwise it may block the request
HEADERS = {"User-Agent": "Mozilla/5.0 (JobAgent/1.0)"}


def fetch_jobs(search: str = "", limit: int = 10) -> list[dict]:
    """
    Fetches recent remote jobs from RemoteOK.
    Optionally filters by a search term (matches title/description/tags).
    Returns a clean list of job summaries.
    """
    try:
        resp = requests.get(REMOTEOK_API, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        return [{"error": f"Failed to fetch jobs: {e}"}]

    # The first item in RemoteOK's response is metadata, skip it
    jobs_raw = data[1:] if data else []

    search_lower = search.lower()
    jobs = []

    for job in jobs_raw:
        title = job.get("position", "") or job.get("title", "")
        company = job.get("company", "")
        description = job.get("description", "")
        tags = job.get("tags", [])

        # Filter by search term if provided
        if search:
            haystack = (title + " " + description + " " + " ".join(tags)).lower()
            if search_lower not in haystack:
                continue

        jobs.append({
            "id": str(job.get("id", "")),
            "title": title,
            "company": company,
            "location": job.get("location", "Remote"),
            "tags": tags[:8],  # keep it short
            "url": job.get("url", ""),
            # description used later as the JD text for /analyze
            "description": _clean_html(description),
        })

        if len(jobs) >= limit:
            break

    return jobs


def _clean_html(text: str) -> str:
    """Removes basic HTML tags from the job description."""
    import re
    if not text:
        return ""
    clean = re.sub(r"<[^>]+>", " ", text)      # remove tags
    clean = re.sub(r"\s+", " ", clean).strip()  # collapse whitespace
    return clean
