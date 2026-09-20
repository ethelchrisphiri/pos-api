def test_admin_can_create_list_get_update_delete_category(client, admin_header):
    create = client.post(
        "/categories/",
        json={"name": "Snacks", "description": "Chips and such"},
        headers=admin_header,
    )
    assert create.status_code == 201
    category_id = create.json()["category_id"]

    listed = client.get("/categories/", headers=admin_header)
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    fetched = client.get(f"/categories/{category_id}", headers=admin_header)
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Snacks"

    updated = client.put(
        f"/categories/{category_id}",
        json={"description": "Updated description"},
        headers=admin_header,
    )
    assert updated.status_code == 200
    assert updated.json()["description"] == "Updated description"
    assert updated.json()["name"] == "Snacks"  # untouched field stays as-is

    deleted = client.delete(f"/categories/{category_id}", headers=admin_header)
    assert deleted.status_code == 204

    gone = client.get(f"/categories/{category_id}", headers=admin_header)
    assert gone.status_code == 404


def test_category_create_rejects_empty_name(client, admin_header):
    response = client.post("/categories/", json={"name": ""}, headers=admin_header)
    assert response.status_code == 422


def test_get_nonexistent_category_returns_404(client, admin_header):
    response = client.get("/categories/9999", headers=admin_header)
    assert response.status_code == 404


def test_cashier_cannot_create_category(client, cashier_header):
    response = client.post("/categories/", json={"name": "Snacks"}, headers=cashier_header)
    assert response.status_code == 403


def test_categories_require_authentication(client):
    response = client.get("/categories/")
    assert response.status_code == 401