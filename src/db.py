import sqlite3
import uuid
from job import Job


def does_exist(job: Job) -> bool:
    """Returns True if job exists in database, False otherwise"""

    conn: sqlite3.Connection = sqlite3.connect("jobs.db")
    c: sqlite3.Cursor = conn.cursor()

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

    conn: sqlite3.Connection = sqlite3.connect("jobs.db")
    c: sqlite3.Cursor = conn.cursor()

    # Check if job exists in database
    if not does_exist(job):
        raise ValueError("Job does not exist")

    # Check if field is valid
    if field not in ("title", "company", "link", "location", "date"):
        raise ValueError("Invalid field")

    c.execute(f"UPDATE jobs SET {field} = ? WHERE title = ?", (value, job.title))

    # Modify job object
    match field:
        case "title":
            job.title = value
        case "company":
            job.company = value
        case "link":
            job.link = value
        case "location":
            job.location = value
        case "date":
            job.date = value

    conn.commit()
    conn.close()


def delete_job(job: Job) -> None:
    """Deletes job with specified title"""

    conn: sqlite3.Connection = sqlite3.connect("jobs.db")
    c: sqlite3.Cursor = conn.cursor()

    # Check if job exists in database
    if not does_exist(job):
        raise ValueError("Job does not exist")

    try:
        c.execute("DELETE FROM jobs WHERE title = ?", (job.title,))
    except sqlite3.Error as e:
        raise e

    conn.commit()
    conn.close()


def get_job(title: str) -> Job:
    """Returns job with specified title"""

    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()

    c.execute("SELECT * FROM jobs WHERE title = ?", (title))
    result = c.fetchone()

    conn.close()

    if result is None:
        raise ValueError("No job found with that title")

    return Job(result[1], result[2], result[3], result[4], result[5], result[6])


def get_jobs() -> list[Job]:
    """Returns all jobs in database"""

    conn: sqlite3.Connection = sqlite3.connect("jobs.db")
    c: sqlite3.Cursor = conn.cursor()

    c.execute("SELECT * FROM jobs")
    jobs: list[tuple[int, str, int, str, str, int]] = c.fetchall()

    conn.close()

    return [Job(job[1], job[2], job[3], job[4], job[5], job[6]) for job in jobs]


def insert_job(job: Job) -> None:
    """Inserts job into database"""

    conn: sqlite3.Connection = sqlite3.connect("jobs.db")
    c: sqlite3.Cursor = conn.cursor()

    # Check if job already exists in database
    if does_exist(job):
        return

    try:
        c.execute(
            "INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                (str(uuid.uuid4())),
                job.title,
                job.company,
                job.location,
                job.link,
                job.date,
                job.date_added,
            ),
        )

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")


def initialize_database() -> None:
    """Creates/initializes database"""

    conn: sqlite3.Connection = sqlite3.connect("jobs.db")
    c: sqlite3.Cursor = conn.cursor()

    # Create table if it does not exist
    try:
        c.execute(
            """CREATE TABLE jobs (
                    unique_id text primary key,
                    title text not null,
                    company text not null,
                    location text not null,
                    link text,
                    date text,
                    date_added text default current_timestamp
                )"""
        )
    except sqlite3.OperationalError as e:
        # Table already exists
        pass

    conn.commit()
    conn.close()
