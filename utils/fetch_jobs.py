from pydantic import BaseModel
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()
import requests
import os
import logging


class JobOutput(BaseModel):
    job_id: str = ""
    title: str = ""
    company: str = ""
    location: str = ""
    url: str = ""
    description: str = ""

def clean_html(html_text: str) -> str:
    soup = BeautifulSoup(html_text, "html.parser")
    return soup.get_text(separator="\n", strip=True)

def fetch_jobs(query:str):
    try:
        job_outputs = []
        # adzuna API helps us to fetch jobs based on the keyworrds 
        response = requests.get(
    f"https://api.adzuna.com/v1/api/jobs/in/search/1",
        params={
        "app_id":os.getenv("JOB_SEARCH_API_ID"),
        "app_key":os.getenv("JOB_SEARCH_API_KEY"),
        "what": query,
        "results_per_page": 20
    })
        data = response.json()
        for job in data["results"]:
            job_outputs.append(JobOutput(
        job_id=job.get("id"),
        title=job.get("title") or "",
        company=(job.get("company") or {}).get("display_name", ""),
        location=(job.get("location") or {}).get("display_name", ""),
        url=job.get("redirect_url") or "",
        description=job.get("description") or ""
    )
)
        return job_outputs

    except Exception as e:
        logging.error("Error fetching jobs from Adzuna", exc_info=True)
        raise Exception(str(e)) from e
