def test_unregister_success_removes_participant(client):
    email = "daniel@mergington.edu"
    response = client.post("/activities/Chess%20Club/unregister", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Chess Club"}

    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_fails_if_activity_not_found(client):
    response = client.post("/activities/Unknown%20Club/unregister", params={"email": "a@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_fails_if_student_not_registered(client):
    response = client.post(
        "/activities/Chess%20Club/unregister",
        params={"email": "not-registered@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up"


def test_unregister_requires_email_query_param(client):
    response = client.post("/activities/Chess%20Club/unregister")

    assert response.status_code == 422
