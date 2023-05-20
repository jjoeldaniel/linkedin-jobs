import sqlite3
from job import Job


def does_exist(job: Job) -> bool:
    """Returns True if job exists in database, False otherwise"""

    with sqlite3.connect("jobs.db") as conn:
        c: sqlite3.Cursor = conn.cursor()

        c.execute(
            "SELECT * FROM jobs WHERE link = ?",
            ([job.link]),
        )

        return c.fetchone() is not None


def delete_job(job: Job) -> None:
    """Deletes job with specified title"""

    if does_exist(job):
        with sqlite3.connect("jobs.db") as conn:
            c: sqlite3.Cursor = conn.cursor()

            try:
                c.execute("DELETE FROM jobs WHERE link = ?", (job.link,))
                conn.commit()
            except sqlite3.Error as e:
                raise e


def get_jobs() -> list[Job]:
    """Returns all jobs in database"""

    with sqlite3.connect("jobs.db") as conn:
        c: sqlite3.Cursor = conn.cursor()

        c.execute("SELECT * FROM jobs")
        jobs: list[tuple[str, str, str, str, str]] = c.fetchall()

        return [Job(*job) for job in jobs]


def insert_job(job: Job) -> None:
    """Inserts job into database"""

    # Check if job already exists in database
    if does_exist(job):
        return

    with sqlite3.connect("jobs.db") as conn:
        try:
            conn.cursor().execute(
                "INSERT INTO jobs VALUES (?, ?, ?, ?, ?)",
                (job.title, job.company, job.location, job.link, job.date),
            )
            conn.commit()
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
                        date text
                    )"""
            )
            conn.commit()
        except sqlite3.OperationalError:
            # Table already exists
            pass
