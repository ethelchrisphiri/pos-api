def test_cashier_can_create_list_get_update_delete_customer(client, cashier_header):
    create = client.post(
        "/customers/",
        json={"name": "Jane Doe", "phone": "555-0111", "email": "jane@example.com"},
        headers=cashier_header,
    )
    assert create.status_code == 201
    customer_id = create.json()["customer_id"]

    fetched = client.get(f"/customers/{customer_id}", headers=cashier_header)
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Jane Doe"

    updated = client.put(f"/customers/{customer_id}", json={"phone": "555-0122"}, headers=cashier_header)
    assert updated.status_code == 200
    assert updated.json()["phone"] == "555-0122"

    deleted = client.delete(f"/customers/{customer_id}", headers=cashier_header)
    assert deleted.status_code == 204

    gone = client.get(f"/customers/{customer_id}", headers=cashier_header)
    assert gone.status_code == 404


def test_customer_create_rejects_empty_name(client, cashier_header):
    response = client.post("/customers/", json={"name": ""}, headers=cashier_header)
    assert response.status_code == 422


def test_get_nonexistent_customer_returns_404(client, admin_header):
    response = client.get("/customers/9999", headers=admin_header)
    assert response.status_code == 404


def test_customers_require_authentication(client):
    response = client.post("/customers/", json={"name": "Jane Doe"})
    assert response.status_code == 401