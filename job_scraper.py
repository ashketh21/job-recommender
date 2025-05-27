## This script scrapes job listings from Indeed using BeautifulSoup and requests.
from bs4 import BeautifulSoup
import requests

def scrape_indeed_jobs(query, location="Ottawa"):
    
    #Testing with mock data right now
    return [
        "Software Developer: Develop web applications using Python and JavaScript frameworks.",
        "Full Stack Developer: Build and maintain web applications using React and Node.js.",
        "Python Developer: Develop backend services using Python, Django and Flask.",
        "Software Engineer: Design and implement scalable software solutions.",
        "Web Developer: Create responsive web applications with modern frameworks."
    ]

    #Original code to scrape Indeed jobs
    # Uncomment the following lines to enable actual scraping from Indeed
    """jobs = []
    url = f"https://www.indeed.com/jobs?q={query}&l={location}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    for job_card in soup.select(".job_seen_beacon"):
        title = job_card.select_one("h2.jobTitle span")
        desc = job_card.select_one("div.job-snippet")
        if title and desc:
            jobs.append(f"{title.text}: {desc.text.strip()}")

    return jobs"""
