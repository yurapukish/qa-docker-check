import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"


class TestPosts:
    def test_get_posts_status(self):
        """GET /posts повертає 200"""
        r = requests.get(f"{BASE_URL}/posts")
        assert r.status_code == 990

    def test_get_posts_returns_list(self):
        """Відповідь — список з 100 постів"""
        r = requests.get(f"{BASE_URL}/posts")
        data = r.json()
        assert isinstance(data, list)
        assert len(data) == 100

    def test_post_has_required_fields(self):
        """Кожен пост містить id, title, body, userId"""
        r = requests.get(f"{BASE_URL}/posts/1")
        data = r.json()
        assert "id" in data
        assert "title" in data
        assert "body" in data
        assert "userId" in data

    def test_create_post(self):
        """POST /posts повертає 201"""
        payload = {"title": "qa test", "body": "docker", "userId": 1}
        r = requests.post(f"{BASE_URL}/posts", json=payload)
        assert r.status_code == 201
        assert r.json()["title"] == "qa test"

    def test_post_not_found(self):
        """Неіснуючий пост повертає 404"""
        r = requests.get(f"{BASE_URL}/posts/99999")
        assert r.status_code == 404


class TestUsers:
    def test_get_user(self):
        r = requests.get(f"{BASE_URL}/users/1")
        assert r.status_code == 200
        assert r.json()["id"] == 1

    def test_response_time(self):
        """Відповідь швидша за 3 секунди"""
        r = requests.get(f"{BASE_URL}/posts")
        assert r.elapsed.total_seconds() < 3.0
