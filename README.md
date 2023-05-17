# SWE Opportuniy Scraper

## Description

This is a web scraper that scrapes LinkedIn for internship and new grad opportunities. It is written in Python and uses requests/BeautifulSoup4. It is currently configured to scrape for Software Engineering opportunities, but can be easily modified to scrape for other roles.

It ships with a simple SQLite database to store the scraped opportunities. The database is not required, but is recommended.

## Documentation

- [job.py](https://jjoeldaniel.github.io/linkedin-jobs/job.html) - Contains the Job class, which represents a job opportunity.

- [main.py](https://jjoeldaniel.github.io/linkedin-jobs/main.html) - Contains the main function, which is the entry point of the program.

- [db.py](https://jjoeldaniel.github.io/linkedin-jobs/db.html) Contains the Database class, which represents a SQLite database.
