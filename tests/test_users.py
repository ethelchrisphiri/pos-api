def test_me_returns_current_user(client, cashier_header):
    response = client.get("/users/me", headers=cashier_header)
    assert response.status_code == 200
    assert response.json()["username"] == "cashier_user"
    assert response.json()["role"] == "cashier"


def test_non_admin_cannot_list_users(client, cashier_header):
    response = client.get("/users/", headers=cashier_header)
    assert response.status_code == 403


def test_admin_can_list_and_get_user(client, admin_header, cashier_header):
    # cashier_header fixture registers "cashier_user" first
    listed = client.get("/users/", headers=admin_header)
    assert listed.status_code == 200
    usernames = [u["username"] for u in listed.json()]
    assert "cashier_user" in usernames
    assert "admin_user" in usernames

    cashier = next(u for u in listed.json() if u["username"] == "cashier_user")
    fetched = client.get(f"/users/{cashier['user_id']}", headers=admin_header)
    assert fetched.status_code == 200
    assert fetched.json()["username"] == "cashier_user"


def test_admin_can_promote_user_role(client, admin_header, cashier_header):
    listed = client.get("/users/", headers=admin_header).json()
    cashier = next(u for u in listed if u["username"] == "cashier_user")

    updated = client.put(f"/users/{cashier['user_id']}", json={"role": "manager"}, headers=admin_header)
    assert updated.status_code == 200
    assert updated.json()["role"] == "manager"


def test_admin_can_deactivate_and_delete_user(client, admin_header, cashier_header):
    listed = client.get("/users/", headers=admin_header).json()
    cashier = next(u for u in listed if u["username"] == "cashier_user")

    deactivated = client.put(f"/users/{cashier['user_id']}", json={"is_active": False}, headers=admin_header)
    assert deactivated.status_code == 200
    assert deactivated.json()["is_active"] is False

    deleted = client.delete(f"/users/{cashier['user_id']}", headers=admin_header)
    assert deleted.status_code == 204

    gone = client.get(f"/users/{cashier['user_id']}", headers=admin_header)
    assert gone.status_code == 404


def test_get_nonexistent_user_returns_404(client, admin_header):
    response = client.get("/users/9999", headers=admin_header)
    assert response.status_code == 404


def test_deactivated_user_cannot_authenticate_with_new_token(client, admin_header, cashier_header):
    listed = client.get("/users/", headers=admin_header).json()
    cashier = next(u for u in listed if u["username"] == "cashier_user")
    client.put(f"/users/{cashier['user_id']}", json={"is_active": False}, headers=admin_header)

    response = client.get("/users/me", headers=cashier_header)
    assert response.status_code == 403