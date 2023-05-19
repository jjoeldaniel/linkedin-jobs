import datetime


class Job:
    """Represents a job posting on LinkedIn"""

    def __init__(
        self,
        title: str = "Software Engineer",
        company: str = "Google",
        location: str = "Mountain View, CA",
        link: str = "https://www.google.com/",
        date: str = "Today",
        date_added: str = str(datetime.datetime.now()),
    ) -> None:
        self.title = title
        self.company = company
        self.location = location
        self.link = link
        self.date = date
        self.date_added = date_added

    def __eq__(self, other):
        """Returns true if two Job objects are equal"""

        return (
            self.title == other.title
            and self.company == other.company
            and self.location == other.location
            and self.link == other.link
            and self.date == other.date
        )

    def __repr__(self) -> str:
        """Returns a string representation of the Job object"""

        return f"Job(title={self.title}, company={self.company}, location={self.location}, link={self.link}, date={self.date}, date_added={self.date_added})"

    def __str__(self) -> str:
        """Returns a string representation of the Job object"""

        return f"Title: {self.title}\nCompany: {self.company}\nLocation: {self.location}\nLink: {self.link}\nDate Posted: {self.date}\nDate Added: {self.date_added}\n"
