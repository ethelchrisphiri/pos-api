def _create_sale(client, admin_header, cashier_header):
    client.post("/categories/", json={"name": "Drinks"}, headers=admin_header)
    client.post("/suppliers/", json={"name": "Acme Co"}, headers=admin_header)
    product = client.post(
        "/products/",
        json={"name": "Cola", "price": "2.50", "stock_qty": 10, "category_id": 1, "supplier_id": 1},
        headers=admin_header,
    ).json()
    sale = client.post(
        "/sales/",
        json={"items": [{"product_id": product["product_id"], "quantity": 1}]},
        headers=cashier_header,
    ).json()
    return sale["sale_id"]


def test_create_list_and_get_receipt(client, admin_header, cashier_header):
    sale_id = _create_sale(client, admin_header, cashier_header)

    created = client.post("/receipts/", json={"sale_id": sale_id}, headers=cashier_header)
    assert created.status_code == 201
    body = created.json()
    assert body["sale_id"] == sale_id
    assert body["receipt_number"].startswith("RCT-")

    listed = client.get("/receipts/", headers=cashier_header)
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    fetched = client.get(f"/receipts/{body['receipt_id']}", headers=cashier_header)
    assert fetched.status_code == 200
    assert fetched.json()["receipt_number"] == body["receipt_number"]


def test_create_receipt_for_nonexistent_sale_returns_404(client, cashier_header):
    response = client.post("/receipts/", json={"sale_id": 9999}, headers=cashier_header)
    assert response.status_code == 404


def test_get_nonexistent_receipt_returns_404(client, cashier_header):
    response = client.get("/receipts/9999", headers=cashier_header)
    assert response.status_code == 404


def test_receipts_require_authentication(client):
    response = client.get("/receipts/")
    assert response.status_code == 401