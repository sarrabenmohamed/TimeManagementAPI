from datetime import datetime, timedelta

def test_create_shift(client):
    # Create employee
    emp = client.post("/employees/", json={"name": "Shifty"}).json()
    emp_id = emp["id"]

    start = "2025-11-17T12:00:00"
    end = "2025-11-17T14:00:00"

    response = client.post(
        "/shifts/",
        json={
            "employee_id": emp_id,
            "start_time": start,
            "end_time": end
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["employee_id"] == emp_id


def test_prevent_overlapping_shift(client):
    emp = client.post("/employees/", json={"name": "Overlap Guy"}).json()
    emp_id = emp["id"]

    client.post("/shifts/", json={
        "employee_id": emp_id,
        "start_time": "2025-11-17T10:00:00",
        "end_time": "2025-11-17T12:00:00"
    })

    # Overlaps
    response = client.post("/shifts/", json={
        "employee_id": emp_id,
        "start_time": "2025-11-17T11:00:00",
        "end_time": "2025-11-17T13:00:00"
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Shift overlaps with existing shift"


def test_list_shifts(client):
    emp = client.post("/employees/", json={"name": "Lister"}).json()
    emp_id = emp["id"]

    client.post("/shifts/", json={
        "employee_id": emp_id,
        "start_time": "2025-11-17T08:00:00",
        "end_time": "2025-11-17T10:00:00"
    })

    response = client.get(f"/shifts/{emp_id}")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_delete_shift(client):
    emp = client.post("/employees/", json={"name": "Delete Shifts"}).json()
    emp_id = emp["id"]

    shift = client.post("/shifts/", json={
        "employee_id": emp_id,
        "start_time": "2025-11-17T12:00:00",
        "end_time": "2025-11-17T14:00:00"
    }).json()

    shift_id = shift["id"]

    response = client.delete(f"/shifts/{shift_id}")
    assert response.status_code == 204

    get_after = client.get(f"/shifts/{emp_id}")
    # ensure deleted
    assert all(s["id"] != shift_id for s in get_after.json())
