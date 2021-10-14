import http.client
import json
from typing import Any, Optional, Tuple, Union
from enum import Enum


class Proficiency(Enum):
    master = "master"
    expert = "expert"
    proficient = "proficient"
    novice = "novice"
    no_experience_interested = "no-experience-interested"


class TorreAPI:

    def get_person_skills(self, username: str) -> Tuple[int, dict]:
        """Get the details of a person at Torre.co"""

        # Host
        conn = http.client.HTTPSConnection("bio.torre.co")
        
        # Payload, header and URL
        payload: str = ''
        headers: dict[str, str] = {}
        url = f"/api/bios/{username}"

        # Request data
        conn.request("GET", url, payload, headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        strengths = data['strengths']

        return res.status, strengths

    def get_job_skills(self, id: str) -> Tuple[int, dict]:
        """Get the details of a job at Torre.co"""

        # Host
        conn = http.client.HTTPSConnection("torre.co")
        
        # Payload, header and URL
        payload: str = ''
        headers: dict[str, str] = {}
        url = f"/api/suite/opportunities/{id}"

        # Request data
        conn.request("GET", url, payload, headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        result = {
            "name": data["objective"],
            "skills": data["strengths"]
        }

        return res.status, result

    def search_jobs(
        self,
        skills:Optional[dict[str, str]]=None,
        currency:str="USD%24",
        periodicity:str="hourly",
        lang:str="en",
        size:int=20,
        aggregate:bool=False
    ) -> Tuple[int, dict[str, Any]]:
        """Search for jobs at Torre.co"""

        # Host
        conn = http.client.HTTPSConnection("search.torre.co")

        # Payload
        payload: str = self._skills_to_payload(skills)

        # Headers
        headers: dict[str, str] = {
            'Content-Type': 'application/json'
        }

        # URL
        url = f"/opportunities/_search?currency={currency}&periodicity={periodicity}" + \
            f"&lang={lang}&size={str(size)}&aggregate={str(aggregate).lower()}"

        # Request data
        conn.request("POST", url, payload, headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        data['results'] = [
            {'id':job['id'], 'skills':job['skills']} for job in data['results']
        ]

        return res.status, data

    def search_people(
        self,
        skills:Optional[dict[str, str]]=None,
        currency:str="USD%24",
        periodicity:str="hourly",
        lang:str="en",
        size:int=20,
        aggregate:bool=False
    ) -> Tuple[int, dict[str, Any]]:
        """Search for people at Torre.co"""

        # Host
        conn = http.client.HTTPSConnection("search.torre.co")

        # Payload
        payload: str = self._skills_to_payload(skills)

        #Headers
        headers: dict[str, str] = {
            'Content-Type': 'application/json'
        }

        # URL
        url = f"/people/_search?currency={currency}&periodicity={periodicity}" + \
            f"&lang={lang}&size={size}&aggregate={str(aggregate).lower()}"

        # Request data
        conn.request("POST", url, payload, headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        data['results'] = [
            {'username':person['username'], 'skills':person['skills']}
            for person in data['results']
        ]

        return res.status, data

    def _skills_to_payload(self, skills:Optional[dict[str, str]]) -> str:
        """Receive a dictionary of skills where the key is a skill and
        the value is the level of proficiency and return a propertly
        formated payload.
        """

        if skills is None:
            return ''
        else:
            skills_array:list = []
            for skill, proficiency in skills.items():
                
                skills_array.append(
                    {
                        "skill/role": {
                            "text": skill,
                            "proficiency": Proficiency(proficiency).value
                        }
                    }
                )

            return json.dumps({"and": skills_array})
