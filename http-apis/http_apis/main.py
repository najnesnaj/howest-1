from .schemas.lecturer import Lecturer
from .schemas.course import Course 
from typing import List
#separate lecturer from courses with router
#from .routers.lecturer_router import lecturer_router

import strawberry
from strawberry.fastapi import GraphQLRouter



# Default fastapi
from typing import Optional
from fastapi import FastAPI
import json
app = FastAPI()

# Example how to read in the courses
with open('data/courses.json', 'r') as f:
  courses = json.load(f)

with open('data/lecturers.json', 'r') as f:
  lecturers = json.load(f)




# Two main examples of the GET routes
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


# Lecturer routes
@app.get('/mct/lecturers', tags=['Lecturer'], response_model=List[Lecturer], summary='Return all lecturers')
def getAllLecturers():
    #return load_lecturers()
    return lecturers
#    pass
@app.get('/mct/lecturers/track/{track}')
def getAllLecturersByTrack():
    pass
@app.get('/mct/lecturers/name/{name}')
def getLecturerByName():
    pass



# Course routes

@app.get('/mct/courses')
def getAllCourses():
    """
    Return all the courses of MCT.
    Using a docstring can be easier to use **markdown** for an extensive markup of your description.
    """
    # pass # Remove the pass part now
    return courses

@app.get('/mct/courses/name/{name}', description='Return one course by name')
def getCourseByName(name: str): # Define that you want to get a parameter 'name' from the url, which will be a string-value

    # Use a Lambda method, which is just a shorthand Python function. This function takes one JSON input and checks it.
    # It returns 'true' if the statement is correct. This filter method only returns the elements for which the result of the statement is 'true'
    return list(filter(lambda course: course['title'] == name, courses)) # Use the Python filter function to filter on only one Course. This will still return a list of items. We will fix that later.

@app.get('/mct/courses/track/{track}', description='Return all the courses by a Track')
def getAllCoursesByTrack(track: str): # Define that you want to get a parameter 'track' from the url, which will be a string-value
    # the track should be in a slug-format (e.g.: ai-engineer instead of AI Engineer)
    return list(filter(lambda course: course['tracks'] == None or ( course['tracks'] != None and track in course['tracks'] ), courses)) # What if this track isn't in the list of Courses? Shouldn't we show something nicer? Let's do that later!



# With this all_fields=True option, we have made sure that all the properties of the Lecturers object are passed through to GraphQL.

@strawberry.experimental.pydantic.type(model=Lecturer, all_fields=True)
class LecturerType:
    pass

# Create a GraphQL Schema
@strawberry.type
class Query:
    @strawberry.field
    def lecturers(self) -> List[LecturerType]:
        return lecturers

schema = strawberry.Schema(query=Query)
# Addint the graphql_ide allows you to easily view and test the GraphQL API using the graphiql IDE
graphql_app = GraphQLRouter(schema, graphql_ide="graphiql")


app.include_router(graphql_app, prefix="/graphql")


"""
lecturer_1_json = {
    'name': 'Nathan Segers',
    'language': 'Dutch',
    'track': 'AI Engineer',
    'programmingLanguage': 'Python',
    'favouriteCourse': 'MLOps'
}
lecturer_1_python = Lecturer(**lecturer_1_json)
# The above line actually executed this:
# lecturer_1_python = Lecturer(name = 'Nathan Segers', language = 'Dutch', track = 'AI Engineer', programmingLanguage = 'Python', favouriteCourse = 'MLOps')



lecturer_1_python.sayHello() # This line will print: `Hello, my name is Nathan Segers and I love MLOps
"""
