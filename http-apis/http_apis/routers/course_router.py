from fastapi import APIRouter

course_router = APIRouter(prefix="/courses", tags=["Courses"])

@course_router.get("/")
async def get_courses():
    return {"message": "List of courses"}

@course_router.post("/")
async def create_course():
    return {"message": "Course created"}

