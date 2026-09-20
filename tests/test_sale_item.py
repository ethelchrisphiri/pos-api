def _create_sale_item(client, admin_header, cashier_header):
    client.post("/categories/", json={"name": "Drinks"}, headers=admin_header)
    client.post("/suppliers/", json={"name": "Acme Co"}, headers=admin_header)
    product = client.post(
        "/products/",
        json={"name": "Cola", "price": "2.50", "stock_qty": 10, "category_id": 1, "supplier_id": 1},
        headers=admin_header,
    ).json()
    sale = client.post(
        "/sales/",
        json={"items": [{"product_id": product["product_id"], "quantity": 2}]},
        headers=cashier_header,
    ).json()
    return sale["sale_items"][0]["sale_item_id"]


def test_list_and_get_sale_item(client, admin_header, cashier_header):
    sale_item_id = _create_sale_item(client, admin_header, cashier_header)

    listed = client.get("/sale-items/", headers=cashier_header)
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    fetched = client.get(f"/sale-items/{sale_item_id}", headers=cashier_header)
    assert fetched.status_code == 200
    assert fetched.json()["quantity"] == 2


def test_get_nonexistent_sale_item_returns_404(client, cashier_header):
    response = client.get("/sale-items/9999", headers=cashier_header)
    assert response.status_code == 404


def test_cashier_cannot_delete_sale_item(client, admin_header, cashier_header):
    sale_item_id = _create_sale_item(client, admin_header, cashier_header)
    response = client.delete(f"/sale-items/{sale_item_id}", headers=cashier_header)
    assert response.status_code == 403


def test_admin_can_delete_sale_item(client, admin_header, cashier_header):
    sale_item_id = _create_sale_item(client, admin_header, cashier_header)
    response = client.delete(f"/sale-items/{sale_item_id}", headers=admin_header)
    assert response.status_code == 204

    gone = client.get(f"/sale-items/{sale_item_id}", headers=admin_header)
    assert gone.status_code == 404