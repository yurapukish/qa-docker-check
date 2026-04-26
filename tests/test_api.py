import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"


class TestPosts:
    def test_get_posts_status(self):
        """GET /posts повертає 200"""
        r = requests.get(f"{BASE_URL}/posts")
        assert r.status_code == 200

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
        
    def test_post_title_is_string(self):
        """Title поста — рядок і не порожній"""
        r = requests.get(f"{BASE_URL}/posts/1")
        data = r.json()
        assert isinstance(data["title"], str)
        assert len(data["title"]) > 0

    def test_get_comments_for_post(self):
        """GET /posts/1/comments повертає список коментарів"""
        r = requests.get(f"{BASE_URL}/posts/1/comments")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert "email" in data[0]

    def test_all_posts_have_user_id(self):
        """Кожен пост має userId"""
        r = requests.get(f"{BASE_URL}/posts")
        posts = r.json()
        for post in posts:
            assert "userId" in post, f"post {post['id']} не має userId"


class TestUsers:
    def test_get_user(self):
        r = requests.get(f"{BASE_URL}/users/1")
        assert r.status_code == 200
        assert r.json()["id"] == 1

    def test_response_time(self):
        """Відповідь швидша за 3 секунди"""
        r = requests.get(f"{BASE_URL}/posts")
        assert r.elapsed.total_seconds() < 1.0
