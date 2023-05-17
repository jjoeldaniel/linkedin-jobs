import sqlite3
import uuid
from job import Job


def does_exist(job: Job) -> bool:
    """Returns True if job exists in database, False otherwise"""

    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()

    c.execute(
        "SELECT * FROM jobs WHERE title = ? AND company = ? AND location = ?",
        (job.title, job.company, job.location),
    )
    result = c.fetchone()

    conn.close()

    return result is not None


def edit_job(
    job: Job,
    field: str,
    value: str,
) -> None:
    """Edits job with specified title"""

    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()

    # Check if job exists in database
    if not does_exist(job):
        return

    c.execute(f"UPDATE jobs SET {field} = ? WHERE title = ?", (value, job.title))

    conn.commit()
    conn.close()


def delete_job(job: Job) -> None:
    """Deletes job with specified title"""

    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()

    # Check if job exists in database
    if not does_exist(job):
        return

    c.execute("DELETE FROM jobs WHERE title = ?", (job.title,))

    conn.commit()
    conn.close()


def get_job(job: Job) -> Job:
    """Returns job with specified title"""

    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()

    c.execute("SELECT * FROM jobs WHERE title = ?", (job.title,))
    result = c.fetchone()

    conn.close()

    return result


def get_jobs() -> list[Job]:
    """Returns all jobs in database"""

    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()

    c.execute("SELECT * FROM jobs")
    jobs = c.fetchall()

    conn.close()

    return jobs


def insert_job(job: Job) -> None:
    """Inserts job into database"""

    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()

    # Check if job already exists in database
    if does_exist(job):
        return

    c.execute(
        "INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?)",
        (str(uuid.uuid4()), job.title, job.company, job.location, job.link, job.date),
    )

    conn.commit()
    conn.close()


def initialize_database():
    """Creates/initializes database"""

    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()

    # Create table if it does not exist
    c.execute(
        """CREATE TABLE IF NOT EXISTS jobs (
                unique_id text primary key,
                title text not null,
                company text not null,
                location text not null,
                link text,
                date text
            )"""
    )

    conn.commit()
    conn.close()
