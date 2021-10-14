from fastapi.testclient import TestClient
from app.main import app
from unittest import mock
from tests.helper import mock_api
import json

client = TestClient(app)


@mock.patch('app.analyzer.analyzer.TorreAPI.search_jobs', return_value=mock_api('torre_jobs'))
def test_post_jobs(mock):
    response = client.post(
        "/jobs",
        headers={"Content-Type": "application/json"},
        json={
            "skills": {
                "php": "novice"
            }
        }
    )
    assert response.status_code == 200
    assert json.loads(response.content) == mock_api('analyzer_jobs')[1]


@mock.patch('app.analyzer.analyzer.TorreAPI.search_people', return_value=mock_api('torre_people'))
def test_post_people(mock):
    response = client.post(
        "/people",
        headers={"Content-Type": "application/json"},
        json={
            "skills": {
                "php": "novice"
            }
        }
    )
    assert response.status_code == 200
    assert json.loads(response.content) == mock_api('analyzer_people')[1]