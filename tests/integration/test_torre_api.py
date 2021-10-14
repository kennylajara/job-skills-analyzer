from unittest import TestCase
from app.api import TorreAPI


class TestTorreAPI(TestCase):

    def test_get_people_skills(self) -> None:

        api = TorreAPI()
        status, skills = api.get_person_skills('kennylajara')

        self.assertEqual(status, 200)
        self.assertEqual(type(skills), list)
        if len(skills) > 0:
            self.assertEqual(type(skills[0]), dict)
            self.assertEqual(type(skills[0]['name']), str)
            self.assertEqual(type(skills[0]['proficiency']), str)
            self.assertEqual(type(skills[0]['weight']), int)

    def test_get_job_skills(self) -> None:

        api = TorreAPI()
        status, skills = api.get_job_skills('Odv2Dbdj')

        self.assertEqual(status, 200)
        self.assertEqual(type(skills), dict)
        self.assertEqual(type(skills['name']), str)
        self.assertEqual(type(skills['skills']), list)
        if len(skills['skills']) > 0:
            self.assertEqual(type(skills['skills'][0]), dict)
            self.assertEqual(type(skills['skills'][0]['id']), str)
            self.assertEqual(type(skills['skills'][0]['code']), int)
            self.assertEqual(type(skills['skills'][0]['name']), str)
            if 'proficiency' in skills['skills'][0]:
                self.assertEqual(type(skills['skills'][0]['proficiency']), str)
            if 'experience' in skills['skills'][0]:
                self.assertEqual(type(skills['skills'][0]['experience']), str)

    def test_search_jobs(self) -> None:
        api = TorreAPI()
        status, jobs = api.search_jobs({'php': 'expert'})

        self.assertEqual(status, 200)
        self.assertEqual(type(jobs), dict)
        self.assertEqual(type(jobs['results']), list)
        if len(jobs['results']) > 0:
            self.assertEqual(type(jobs['results'][0]['id']), str)
            self.assertEqual(type(jobs['results'][0]['skills'][0]['name']), str)
            self.assertEqual(type(jobs['results'][0]['skills'][0]['experience']), str)
            self.assertEqual(type(jobs['results'][0]['skills'][0]['proficiency']), str)

    def test_search_person(self) -> None:
        api = TorreAPI()
        status, people = api.search_people({'php': 'expert'})

        self.assertEqual(status, 200)
        self.assertEqual(type(people), dict)
        self.assertEqual(type(people['results']), list)
        if len(people['results']) > 0:
            self.assertEqual(type(people['results'][0]['username']), str)
            if len(people['results'][0]['skills']) > 0:
                self.assertEqual(type(people['results'][0]['skills'][0]['name']), str)
                self.assertEqual(type(people['results'][0]['skills'][0]['weight']), float)

