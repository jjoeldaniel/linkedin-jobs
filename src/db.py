import sqlite3
from job import Job


def does_exist(job: Job) -> bool:
    """Returns True if job exists in database, False otherwise"""

    with sqlite3.connect("jobs.db") as conn:
        c: sqlite3.Cursor = conn.cursor()

        c.execute(
            "SELECT * FROM jobs WHERE link = ?",
            (job.link),
        )

        return c.fetchone() is not None


def edit_job(
    job: Job,
    field: str,
    value: str,
) -> None:
    """Edits job with specified title"""

    # Check if job exists in database
    if not does_exist(job):
        raise ValueError("Job does not exist")

    # Check if field is valid
    if field not in ("title", "company", "link", "location", "date"):
        raise ValueError("Invalid field")

    with sqlite3.connect("jobs.db") as conn:
        conn.cursor().execute(
            f"UPDATE jobs SET {field} = ? WHERE title = ?", (value, job.title)
        )

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


def delete_job(job: Job) -> None:
    """Deletes job with specified title"""

    if does_exist(job):
        with sqlite3.connect("jobs.db") as conn:
            c: sqlite3.Cursor = conn.cursor()

            try:
                c.execute("DELETE FROM jobs WHERE title = ?", (job.title,))
            except sqlite3.Error as e:
                raise e


def get_jobs() -> list[Job]:
    """Returns all jobs in database"""

    with sqlite3.connect("jobs.db") as conn:
        c: sqlite3.Cursor = conn.cursor()

        c.execute("SELECT * FROM jobs")
        jobs: list[tuple[str, int, str, str, int]] = c.fetchall()
        print(jobs[0])

        return [Job(*job) for job in jobs]


def insert_job(job: Job) -> None:
    """Inserts job into database"""

    # Check if job already exists in database
    if does_exist(job):
        return

    with sqlite3.connect("jobs.db") as conn:
        try:
            conn.cursor().execute(
                "INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?)",
                (
                    job.title,
                    job.company,
                    job.location,
                    job.link,
                    job.date,
                    job.date_added,
                ),
            )
        except Exception as e:
            print(f"Error: {e}")


def initialize_database() -> None:
    """Creates/initializes database"""

    with sqlite3.connect("jobs.db") as conn:
        # Create table if it does not exist
        try:
            conn.cursor().execute(
                """CREATE TABLE jobs (
                        title text not null,
                        company text not null,
                        location text not null,
                        link text,
                        date text,
                        date_added text default current_timestamp
                    )"""
            )
        except sqlite3.OperationalError:
            # Table already exists
            pass
