"""
Backend tests for PunchListJobs API
Tests: health, auth, settings, jobs, user management
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

CREDENTIALS = {
    "superadmin": ("superadmin@punchlistjobs.com", "SuperAdmin@123"),
    "admin": ("admin@punchlistjobs.com", "Admin@123"),
    "crew1": ("crew1@punchlistjobs.com", "Crew@123"),
    "contractor1": ("contractor1@punchlistjobs.com", "Contractor@123"),
}


@pytest.fixture(scope="module")
def session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


def login(session, email, password):
    resp = session.post(f"{BASE_URL}/api/auth/login", json={"email": email, "password": password})
    return resp


# --- Health & Public ---

class TestHealth:
    def test_api_root(self, session):
        r = session.get(f"{BASE_URL}/api/")
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "operational"

    def test_public_settings(self, session):
        r = session.get(f"{BASE_URL}/api/settings/public")
        assert r.status_code == 200
        data = r.json()
        assert "site_name" in data
        assert data["site_name"] == "PunchListJobs"


# --- Authentication ---

class TestAuth:
    def test_login_crew(self, session):
        r = login(session, *CREDENTIALS["crew1"])
        assert r.status_code == 200
        data = r.json()
        assert "access_token" in data
        assert data["user"]["role"] == "crew"

    def test_login_contractor(self, session):
        r = login(session, *CREDENTIALS["contractor1"])
        assert r.status_code == 200
        data = r.json()
        assert "access_token" in data
        assert data["user"]["role"] == "contractor"

    def test_login_admin(self, session):
        r = login(session, *CREDENTIALS["admin"])
        assert r.status_code == 200
        data = r.json()
        assert "access_token" in data

    def test_login_superadmin(self, session):
        r = login(session, *CREDENTIALS["superadmin"])
        assert r.status_code == 200
        data = r.json()
        assert "access_token" in data

    def test_login_invalid_credentials(self, session):
        r = login(session, "wrong@example.com", "wrongpass")
        assert r.status_code in [401, 400, 422]

    def test_get_me_crew(self, session):
        r = login(session, *CREDENTIALS["crew1"])
        token = r.json()["access_token"]
        me_r = session.get(f"{BASE_URL}/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me_r.status_code == 200
        data = me_r.json()
        assert data["email"] == CREDENTIALS["crew1"][0]

    def test_get_me_no_token(self, session):
        r = session.get(f"{BASE_URL}/api/auth/me")
        assert r.status_code in [401, 403]


# --- Jobs ---

class TestJobs:
    def test_list_jobs_authenticated(self, session):
        r = login(session, *CREDENTIALS["crew1"])
        token = r.json()["access_token"]
        jobs_r = session.get(f"{BASE_URL}/api/jobs", headers={"Authorization": f"Bearer {token}"})
        assert jobs_r.status_code == 200
        data = jobs_r.json()
        assert isinstance(data, list)

    def test_list_jobs_unauthenticated(self, session):
        r = session.get(f"{BASE_URL}/api/jobs")
        assert r.status_code in [401, 403]

    def test_contractor_can_post_job(self, session):
        r = login(session, *CREDENTIALS["contractor1"])
        token = r.json()["access_token"]
        job_data = {
            "title": "TEST_Roofing Helper Needed",
            "description": "Need experienced roofing crew for 3-day job",
            "trade": "Roofing",
            "crew_needed": 2,
            "start_time": "2026-03-01T08:00:00",
            "pay_rate": 25.0,
            "address": "Dallas, TX",
        }
        post_r = session.post(
            f"{BASE_URL}/api/jobs/",
            json=job_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert post_r.status_code in [200, 201]
        created = post_r.json()
        assert "id" in created

    def test_crew_cannot_post_job(self, session):
        r = login(session, *CREDENTIALS["crew1"])
        token = r.json()["access_token"]
        job_data = {
            "title": "TEST_Unauthorized job",
            "description": "Should fail for crew",
            "trade": "Roofing",
            "crew_needed": 1,
            "start_time": "2026-03-01T08:00:00",
            "pay_rate": 20.0,
            "address": "Dallas, TX",
        }
        post_r = session.post(
            f"{BASE_URL}/api/jobs/",
            json=job_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert post_r.status_code in [403, 401, 422]


# --- Admin ---

class TestAdmin:
    def test_admin_list_users(self, session):
        r = login(session, *CREDENTIALS["admin"])
        token = r.json()["access_token"]
        users_r = session.get(
            f"{BASE_URL}/api/admin/users",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert users_r.status_code == 200
        data = users_r.json()
        assert isinstance(data, list) or "users" in data

    def test_crew_cannot_access_admin(self, session):
        r = login(session, *CREDENTIALS["crew1"])
        token = r.json()["access_token"]
        admin_r = session.get(
            f"{BASE_URL}/api/admin/users",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert admin_r.status_code in [403, 401]
