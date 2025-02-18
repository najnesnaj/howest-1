I installed uvicorn on linux (apt install uvicorn)

but ....
poetry run python http_apis/main.py

ModuleNotFoundError: No module named 'fastapi'

solution
--------
poetry add uvicorn
poetry run python -m uvicorn http_apis.main:app --reload


documenting
-----------
@app.get('/mct/courses', description='Return all the courses of MCT') will not show the docstring !!!


@app.get('/mct/courses') --- this will show the following docstring
You cannot use both the Description parameter into your route, and the Docstring description at the same time. If you do so, it will not take the Docstring description into your API documentation, but it will take the one you filled into a parameter.



destructuring  (**object)
-------------- 


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


project structure: 
--------------------

http-apis/
│-- data/
│   ├── lecturers.json  # JSON file with lecturer data
│-- http_apis/
│   ├── main.py         # FastAPI app entry point
│   ├── schemas/
│   │   ├── lecturer.py # Defines the Lecturer Pydantic model



----------------------
poetry add strawberry-graphql[debug-server,fastapi]

