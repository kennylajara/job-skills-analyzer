from fastapi import FastAPI, Query, Response
from app.analyzer import Analyzer
from pydantic import BaseModel
from app.api.torre import Proficiency, TorreAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

@app.get('/people/{username}/skills')
def get_skill_of_the_specified_user(username: str, response: Response):

    api = TorreAPI()
    status, skills = api.get_person_skills(username)

    # Validate status code
    if status != 200:
        response.status_code = status
        return skills

    return [ skill['name'] for skill in skills ]
