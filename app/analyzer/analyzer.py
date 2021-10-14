from app.api import TorreAPI
from fastapi import HTTPException

class Analyzer:

    def analyze_jobs(self, skills:dict[str, str], sample:int=20):
        return self._analyze(skills, 'jobs', sample)

    def analyze_people(self, skills:dict[str, str], sample:int=20):
        return self._analyze(skills, 'people', sample)

    def _analyze(self, skills:dict[str, str], item_type:str, sample:int = 20):

        # Make sure sample does not exceed 2500
        if sample > 2500:
            raise HTTPException(
                status_code=400,
                detail="The sample can't be greater than 2500"
            )

        # Request data from Torre API
        api: TorreAPI = TorreAPI()

        if item_type=='jobs':
            status, items = api.search_jobs(skills=skills)
        elif item_type == 'people':
            status, items = api.search_people(skills=skills)
        else:
            raise HTTPException(
                status_code=500,
                detail="Unknown itemtype"
            )

        # Validate status code
        if status != 200:
            raise HTTPException(
                status_code=503,
                detail="A 3rd Party Service Unavailable"
            )

        # Count related skills
        related_skills:dict = {}
        base_skills = [skill.lower() for skill in skills.keys()]
        for item in items['results']:
            for skill in item['skills']:
                if skill['name'] in related_skills.keys():
                    related_skills[skill['name']] += 1
                else:
                    if skill['name'].lower() not in base_skills:
                        related_skills[skill['name']] = 1

        # Order related skills from highest to lowest
        # and change the value to and AVG
        related_skills = {
            k: v / sample 
            for k, v in sorted(related_skills.items(), key=lambda item: item[1], reverse=True)
        }

        return {
            'population': items['total'],
            'sample_type': item_type,
            'sample_size': min(items['total'], sample),
            'skills': skills,
            'related_skills': related_skills,
        }
