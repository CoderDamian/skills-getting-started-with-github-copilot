import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

# Fixture to reset activities before each test
@pytest.fixture(autouse=True)
def reset_activities():
    # Reset participants to original state
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
    activities["Programming Class"]["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]
    activities["Gym Class"]["participants"] = ["john@mergington.edu", "olivia@mergington.edu"]
    activities["Soccer Team"]["participants"] = ["liam@mergington.edu", "noah@mergington.edu"]
    activities["Yoga Club"]["participants"] = ["ava@mergington.edu", "isabella@mergington.edu"]
    activities["Art Club"]["participants"] = ["mia@mergington.edu", "charlotte@mergington.edu"]
    activities["Music Ensemble"]["participants"] = ["amelia@mergington.edu", "harper@mergington.edu"]
    activities["Debate Team"]["participants"] = ["evelyn@mergington.edu", "jackson@mergington.edu"]
    activities["Science Club"]["participants"] = ["lucas@mergington.edu", "ella@mergington.edu"]


def test_root_redirect():
    # Arrange
    expected_url = "/static/index.html"

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    assert response.url.path == expected_url


def test_get_activities():
    # Arrange
    expected_keys = ["Chess Club", "Programming Class", "Gym Class", "Soccer Team", "Yoga Club", "Art Club", "Music Ensemble", "Debate Team", "Science Club"]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert set(data.keys()) == set(expected_keys)
    for activity in data.values():
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)


def test_signup_success():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    initial_count = len(activities[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]
    assert len(activities[activity_name]["participants"]) == initial_count + 1
    assert email in activities[activity_name]["participants"]


def test_signup_invalid_activity():
    # Arrange
    invalid_activity = "Nonexistent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{invalid_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_signup_duplicate():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student already signed up for this activity" in data["detail"]