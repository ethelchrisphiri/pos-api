def test_admin_can_create_list_get_update_delete_supplier(client, admin_header):
    create = client.post(
        "/suppliers/",
        json={"name": "Global Foods", "phone": "555-0100", "email": "contact@globalfoods.example"},
        headers=admin_header,
    )
    assert create.status_code == 201
    supplier_id = create.json()["supplier_id"]

    fetched = client.get(f"/suppliers/{supplier_id}", headers=admin_header)
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Global Foods"

    updated = client.put(f"/suppliers/{supplier_id}", json={"phone": "555-0199"}, headers=admin_header)
    assert updated.status_code == 200
    assert updated.json()["phone"] == "555-0199"

    deleted = client.delete(f"/suppliers/{supplier_id}", headers=admin_header)
    assert deleted.status_code == 204

    gone = client.get(f"/suppliers/{supplier_id}", headers=admin_header)
    assert gone.status_code == 404


def test_supplier_create_rejects_empty_name(client, admin_header):
    response = client.post("/suppliers/", json={"name": ""}, headers=admin_header)
    assert response.status_code == 422


def test_supplier_create_rejects_invalid_email(client, admin_header):
    response = client.post(
        "/suppliers/",
        json={"name": "Bad Email Co", "email": "not-an-email"},
        headers=admin_header,
    )
    assert response.status_code == 422


def test_get_nonexistent_supplier_returns_404(client, admin_header):
    response = client.get("/suppliers/9999", headers=admin_header)
    assert response.status_code == 404


def test_cashier_cannot_create_supplier(client, cashier_header):
    response = client.post("/suppliers/", json={"name": "Global Foods"}, headers=cashier_header)
    assert response.status_code == 403