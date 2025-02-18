from fastapi import APIRouter
from typing import List
#from models import Lecturer  # Ensure this points to your `Lecturer` model
import json 

# Create an APIRouter instance
lecturer_router = APIRouter(prefix="/mct/lecturers", tags=["Lecturers"])

# ( database logic)
with open('data/lecturers.json', 'r') as f:
  lecturers = json.load(f)

# Get all lecturers
@lecturer_router.get("/", response_model=List[Lecturer], summary="Return all lecturers")
def get_all_lecturers():
    return lecturers

# Get lecturers by track
@lecturer_router.get("/track/{track}", summary="Return lecturers by track")
def get_all_lecturers_by_track(track: str):
    return [lecturer for lecturer in lecturers if lecturer["track"] == track]

# Get lecturer by name
@lecturer_router.get("/name/{name}", summary="Return lecturer by name")
def get_lecturer_by_name(name: str):
    return next((lecturer for lecturer in lecturers if lecturer["name"] == name), {"error": "Lecturer not found"})

