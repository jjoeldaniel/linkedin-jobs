class Job:
    """Represents a job posting on LinkedIn"""

    def __init__(
        self,
        title: str = "Software Engineer",
        company: str = "Google",
        location: str = "Mountain View, CA",
        link: str = "https://www.google.com/",
        date: str = "Today",
    ) -> None:
        self.title = title
        self.company = company
        self.location = location
        self.link = link
        self.date = date

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

        return f"Job(title={self.title}, company={self.company}, location={self.location}, link={self.link}, date={self.date})"

    def __str__(self) -> str:
        """Returns a string representation of the Job object"""

        return f"Title: {self.title}\nCompany: {self.company}\nLocation: {self.location}\nLink: {self.link}\nDate Posted: {self.date}\n"
