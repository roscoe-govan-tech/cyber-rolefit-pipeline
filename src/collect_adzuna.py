import os
from typing import List, Dict

import requests
from dotenv import load_dotenv


load_dotenv()


ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")


def collect_adzuna_jobs(
    search_term: str,
    location: str = "Dallas, TX",
    country: str = "us",
    page: int = 1,
    results_per_page: int = 10,
) -> List[Dict]:
    """
    Collect job postings from the Adzuna Job Search API.

    Args:
        search_term: Job keyword/search phrase, such as "SOC Analyst".
        location: Search location, such as "Dallas, TX".
        country: Adzuna country code. Use "us" for United States.
        page: Results page number.
        results_per_page: Number of jobs to return.

    Returns:
        A list of normalized job dictionaries.
    """

    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        raise ValueError(
            "Missing Adzuna credentials. Add ADZUNA_APP_ID and ADZUNA_APP_KEY to your .env file."
        )

    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": results_per_page,
        "what": search_term,
        "where": location,
        "content-type": "application/json",
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()
    results = data.get("results", [])

    normalized_jobs = []

    for job in results:
        normalized_jobs.append(
            {
                "title": job.get("title", ""),
                "company": job.get("company", {}).get("display_name", ""),
                "location": job.get("location", {}).get("display_name", ""),
                "description": job.get("description", ""),
                "redirect_url": job.get("redirect_url", ""),
                "source": "Adzuna",
                "created": job.get("created", ""),
                "salary_min": job.get("salary_min"),
                "salary_max": job.get("salary_max"),
            }
        )

    return normalized_jobs