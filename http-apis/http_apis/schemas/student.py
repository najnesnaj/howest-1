# lecturer.py
# Make the Student Class inherit from the base-class `object`
class Student(object):

    # Create a method which will be called on initialization of a new Lecturer object: Lecturer('Nathan Segers', ...)
    def __init__(self,
        name: str, # e.g.: Nathan Segers
        language: str, # e.g.: Dutch
        track: str, # e.g.: AI Engineer
        programmingLanguage: str, # e.g.: Python
        favouriteCourse: str, # MLOps
        ):
        # Set all the properties of this class to the arguments given on initialization.
        # These properties can be referred to onto this instance of the Lecturer class.
        self.name = name
        self.language = language
        self.track = track
        self.programmingLanguage = programmingLanguage
        # In the future this can be updated with the whole Course object
        self.favouriteCourse = favouriteCourse

    def sayHello(self):
        print(f"Hello, my name is {self.name} and I love {self.favouriteCourse}")

