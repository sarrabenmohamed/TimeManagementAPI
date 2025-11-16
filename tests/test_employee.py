def test_create_employee(client):
    response = client.post(
        "/employees/",
        json={"name": "John Doe", "role": "Baker"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["role"] == "Baker"


def test_prevent_duplicate_employee(client):
    client.post("/employees/", json={"name": "Alice"})
    response = client.post("/employees/", json={"name": "Alice"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Employee with this name already exists"


def test_get_employee(client):
    create = client.post("/employees/", json={"name": "Henry"})
    emp_id = create.json()["id"]

    response = client.get(f"/employees/{emp_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Henry"


def test_update_employee(client):
    create = client.post("/employees/", json={"name": "Greg"})
    emp_id = create.json()["id"]

    updated = client.put(
        f"/employees/{emp_id}",
        json={"name": "Greg Updated"}
    )

    assert updated.status_code == 200
    assert updated.json()["name"] == "Greg Updated"


def test_delete_employee(client):
    create = client.post("/employees/", json={"name": "Delete Me"})
    emp_id = create.json()["id"]

    response = client.delete(f"/employees/{emp_id}")
    assert response.status_code == 204

    # Verify deleted
    get_after = client.get(f"/employees/{emp_id}")
    assert get_after.json() is None
