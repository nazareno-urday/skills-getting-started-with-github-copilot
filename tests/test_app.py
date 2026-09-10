def test_get_activities_returns_activity_catalog(client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert activities["Chess Club"]["max_participants"] == 12
    assert "participants" in activities["Chess Club"]


def test_signup_adds_participant_to_activity(client):
    # Arrange
    endpoint = "/activities/Chess Club/signup"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(
        endpoint,
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for Chess Club"
    }
    activities = client.get("/activities").json()
    assert "new.student@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_rejects_participant_already_registered(client):
    # Arrange
    endpoint = "/activities/Chess Club/signup"
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        endpoint,
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student already signed up for an activity"
    }


def test_signup_returns_not_found_for_unknown_activity(client):
    # Arrange
    endpoint = "/activities/Unknown Club/signup"

    # Act
    response = client.post(
        endpoint,
        params={"email": "new.student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_delete_removes_participant_from_activity(client):
    # Arrange
    endpoint = "/activities/Chess Club/participants/michael@mergington.edu"

    # Act
    response = client.delete(endpoint)

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered michael@mergington.edu from Chess Club"
    }
    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_delete_returns_not_found_for_unknown_activity(client):
    # Arrange
    endpoint = "/activities/Unknown Club/participants/student@mergington.edu"

    # Act
    response = client.delete(
        endpoint
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_delete_returns_not_found_for_unknown_participant(client):
    # Arrange
    endpoint = "/activities/Chess Club/participants/unknown@mergington.edu"

    # Act
    response = client.delete(
        endpoint
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found"}
