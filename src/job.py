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

    def __str__(self):
        """Returns a string representation of the Job object"""

        return f"Title: {self.title}\nCompany: {self.company}\nLocation: {self.location}\nLink: {self.link}\nDate Posted: {self.date}\n"
