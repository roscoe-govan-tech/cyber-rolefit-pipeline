from src.collect_adzuna import collect_adzuna_jobs


jobs = collect_adzuna_jobs(
    search_term="SOC Analyst",
    location="Dallas, TX",
    results_per_page=5,
)

for job in jobs:
    print("=" * 80)
    print(f"Title: {job['title']}")
    print(f"Company: {job['company']}")
    print(f"Location: {job['location']}")
    print(f"Source: {job['source']}")
    print(f"Created: {job['created']}")
    print(f"URL: {job['redirect_url']}")