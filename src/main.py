from bs4 import BeautifulSoup
import requests
from job import Job
import db as db


# URL containing pre-filtered job search results
# for "software engineer intern/entry level" in the last 7 days
linkedin_url = "https://www.linkedin.com/jobs/search/?currentJobId=3511050778&f_E=1%2C2&f_JT=F%2CI&f_TPR=r604800&geoId=103644278&keywords=software%20engineer%20intern&location=United%20States&refresh=true"


def main():
    # Get the HTML content of the URL
    html = requests.get(linkedin_url).content
    soup = BeautifulSoup(html, "html.parser")

    # Unordered list containing all job postings
    posting_list = soup.find_all(name="div", class_="job-search-card")

    # List of Job objects
    jobs = []

    for post in posting_list:
        title = str(post.find(name="h3", class_="base-search-card__title").text).strip()
        company = str(post.find(name="a", class_="hidden-nested-link").text).strip()
        location = str(
            post.find(name="span", class_="job-search-card__location").text
        ).strip()
        date = str(post.find(name="time").text).strip()
        link = str(
            post.find(name="a", class_="base-card__full-link").get("href")
        ).strip()

        jobs.append(Job(title, company, location, link, date))

    for job in jobs:
        db.insert_job(job)


if __name__ == "__main__":
    db.initialize_database()
    main()
