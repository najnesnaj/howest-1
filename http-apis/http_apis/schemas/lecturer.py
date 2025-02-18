# lecturer.py
# Make the Lecturer Class inherit from the base-class `object`
#class Lecturer(object):
#
#    # Create a method which will be called on initialization of a new Lecturer object: Lecturer('Nathan Segers', ...)
#    def __init__(self,
#        name: str, # e.g.: Nathan Segers
#        language: str, # e.g.: Dutch
#        track: str, # e.g.: AI Engineer
#        programmingLanguage: str, # e.g.: Python
#        favouriteCourse: str, # MLOps
#        ):
#        # Set all the properties of this class to the arguments given on initialization.
#        # These properties can be referred to onto this instance of the Lecturer class.
#        self.name = name
#        self.language = language
#        self.track = track
#        self.programmingLanguage = programmingLanguage
#        # In the future this can be updated with the whole Course object
#        self.favouriteCourse = favouriteCourse
#
#    def sayHello(self):
#        print(f"Hello, my name is {self.name} and I love {self.favouriteCourse}")
#
"""
Pydantic Response Models
FastAPI is a big fan of working with Pydantic. Pydantic is a Python package that allows us to quickly create Python objects, with data validation and parsing.
As FastAPI is tightly coupled with Pydantic, we need to embrace it and work with Pydantic for our API documentation.
"""



from pydantic import BaseModel

# Make the Lecturer Class inherit from the pydantic-class `BaseModel`
class Lecturer(BaseModel):
    name: str
    language: str
    track: str
    programmingLanguage: str
    favouriteCourse: str

    def sayHello(self):
        print(f"Hello, my name is {self.name} and I love {self.favouriteCourse}")

