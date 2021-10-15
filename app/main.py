from fastapi import FastAPI, Query
from app.analyzer import Analyzer
from pydantic import BaseModel
from app.api.torre import Proficiency
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()


class Skills(BaseModel):
    skills: dict[str, Proficiency]


@app.post("/jobs")
def analyze_jobs(skills: Skills, sample: int = Query(20, le=2500)):

    analyzer = Analyzer()

    skills_dict = dict(skills)['skills']

    return analyzer.analyze_jobs(skills_dict, sample=sample)


@app.post("/people")
def analyze_people(skills: Skills, sample: int = Query(20, le=2500)):

    analyzer = Analyzer()

    skills_dict = dict(skills)['skills']

    return analyzer.analyze_people(skills_dict, sample=sample)


# Allow Frontend
origins = [
    os.environ['CORS'],
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)