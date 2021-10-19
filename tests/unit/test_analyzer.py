from unittest import TestCase, mock
from app.analyzer import Analyzer
from tests.helper import mock_api


class TestTorreAPI(TestCase):

    @mock.patch('app.analyzer.analyzer.TorreAPI.search_jobs', return_value=mock_api('torre_jobs'))
    def test_analyze_job(self, mock) -> None: 

        skills = {
            'php': 'novice',
        }
        analyzer = Analyzer()
        analysis = analyzer.analyze_jobs(skills)

        self.assertEqual(analysis['population'], 4247)
        self.assertEqual(analysis['sample_type'], 'jobs')
        self.assertEqual(analysis['sample_size'], 20)
        self.assertDictEqual(analysis['skills'], skills)
        self.assertEqual(type(analysis['related_skills']), dict)

        for skill, value in analysis['related_skills'].items():
            self.assertEqual(type(skill), str)
            self.assertEqual(type(value), float)

        self.assertDictEqual(analysis, mock_api('analyzer_jobs')[1])

    @mock.patch('app.analyzer.analyzer.TorreAPI.search_people', return_value=mock_api('torre_people'))
    def test_analyze_people(self, mock) -> None: 

        skills = {
            'php': 'novice',
        }
        analyzer = Analyzer()
        analysis = analyzer.analyze_people(skills)

        self.assertEqual(analysis['population'], 10635)
        self.assertEqual(analysis['sample_type'], 'people')
        self.assertEqual(analysis['sample_size'], 20)
        self.assertDictEqual(analysis['skills'], skills)
        self.assertEqual(type(analysis['related_skills']), dict)

        for skill, value in analysis['related_skills'].items():
            self.assertEqual(type(skill), str)
            self.assertEqual(type(value), float)

        self.assertDictEqual(analysis, mock_api('analyzer_people')[1])
