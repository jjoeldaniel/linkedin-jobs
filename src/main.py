import datetime
from bs4 import BeautifulSoup
import requests
from job import Job
import db as db


# URL containing pre-filtered job search results
# for "software engineer intern/entry level" in the last 7 days
LINKEDIN_URL = "https://www.linkedin.com/jobs/search/?currentJobId=3511050778&f_E=1%2C2&f_JT=F%2CI&f_TPR=r604800&geoId=103644278&keywords=software%20engineer%20intern&location=United%20States&refresh=true"


def scrape_postings() -> list[Job]:
    """Scrapes job postings from LinkedIn and returns a list of Job objects"""

    # Get the HTML content of the URL
    html: str = requests.get(LINKEDIN_URL).content
    soup: BeautifulSoup = BeautifulSoup(html, "html.parser")

    # Unordered list containing all job postings
    posting_list: list[BeautifulSoup] = soup.find_all(
        name="div", class_="job-search-card"
    )

    # List of Job objects
    jobs: list[Job] = []

    for post in posting_list:
        title: str = str(
            post.find(name="h3", class_="base-search-card__title").text
        ).strip()
        company: str = str(
            post.find(name="a", class_="hidden-nested-link").text
        ).strip()
        location: str = str(
            post.find(name="span", class_="job-search-card__location").text
        ).strip()
        date: str = str(post.find(name="time").text).strip()
        link: str = str(
            post.find(name="a", class_="base-card__full-link").get("href")
        ).strip()

        # remove query parameters from link
        link = link.split("?")[0]

        # convert relative date to absolute date
        units = date.split(" ")[1]
        length = int(date.split(" ")[0])

        # remove 's' from units if necessary
        if units[-1] == "s":
            units = units[:-1]

        match units:
            case "minute":
                date = datetime.datetime.now() - datetime.timedelta(minutes=length)
            case "hour":
                date = datetime.datetime.now() - datetime.timedelta(hours=length)
            case "day":
                date = datetime.datetime.now() - datetime.timedelta(days=length)
            case "week":
                date = datetime.datetime.now() - datetime.timedelta(weeks=length)
            case _:
                date = datetime.datetime.now()

        # format date %m/%d/%Y %H:%M %p
        tup = date.timetuple()
        date = datetime.datetime(*tup[:6])

        jobs.append(Job(title, company, location, link, date))

    return jobs


def main():
    """Main function"""

    new_postings: list[Job] = scrape_postings()
    for j in new_postings:
        db.insert_job(j)

    # jobs = db.get_jobs()
    # for j in jobs:
    #     print(j)


if __name__ == "__main__":
    db.initialize_database()
    main()
