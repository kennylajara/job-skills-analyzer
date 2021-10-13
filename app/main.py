from fastapi import FastAPI, Query
from app.analyzer import Analyzer


app = FastAPI()


@app.get("/jobs")
def read_root(sample: int = Query(20, le=2500)):

    skills = {
        'php': 'novice',
    }
    analyzer = Analyzer()

    return analyzer.analyze_jobs(skills, sample=sample)


@app.get("/people")
def read_root(sample: int = Query(20, le=2500)):

    skills = {
        'php': 'novice',
    }
    analyzer = Analyzer()

    return analyzer.analyze_people(skills, sample=sample)
