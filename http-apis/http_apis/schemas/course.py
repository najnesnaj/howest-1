# course.py
from typing import List, Optional
# Make the Course Class inherit from the base-class `object`
class Course(object):

    # Create a method which will be called on initialization of a new Course object: Course('MLOps', ...)
    def __init__(self,
            title: str, # e.g.: MLOps
            content: str, # e.g.: A course where you will learn how to deploy AI models
            semester: int, # e.g.: 5 --> Year 3, semester 1
            pillar: str, # e.g.: "code"
            tags: List[str], # e.g.: ["Kubernetes", "CI/CD", "AutomatedAI", "CloudAI"],
            tracks: Optional[List[str]] = None, # e.g.: ['AI Engineer', 'Next Web Developer']
            lecturers: Optional[List[str]] = None, # e.g.: ['Nathan Segers', 'Wouter Gevaert']
            students: Optional[List[str]] = None # e.g.: ['Nathan Segers', 'Wouter Gevaert']
        ):
        # Set all the properties of this class to the arguments given on initialization.
        # These properties can be referred to onto this instance of the Course class.
        self.title = title
        self.content = content
        self.semester = semester
        self.pillar = pillar
        self.tags = tags
        self.tracks = tracks # None means all tracks
        self.lecturers = lecturers # Fill in later
        self.students = students # Fill in later

    def showLecturers(self):
        print(f"The Lecturers for the {self.title} course are {self.lecturers}")

