def test_create_and_list_product_as_admin(client, admin_header):
    client.post("/categories/", json={"name": "Drinks", "description": "Beverages"}, headers=admin_header)
    client.post("/suppliers/", json={"name": "Acme Co", "phone": "123", "email": "s@example.com"}, headers=admin_header)

    response = client.post(
        "/products/",
        json={"name": "Cola", "price": "2.50", "stock_qty": 100, "category_id": 1, "supplier_id": 1},
        headers=admin_header,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Cola"
    assert body["stock_qty"] == 100

    list_response = client.get("/products/", headers=admin_header)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


def test_product_rejects_negative_price(client, admin_header):
    client.post("/categories/", json={"name": "Drinks"}, headers=admin_header)
    client.post("/suppliers/", json={"name": "Acme Co"}, headers=admin_header)

    response = client.post(
        "/products/",
        json={"name": "Bad Product", "price": "-5.00", "stock_qty": 10, "category_id": 1, "supplier_id": 1},
        headers=admin_header,
    )
    assert response.status_code == 422

def test_cashier_cannot_create_product(client, cashier_header):
    response = client.post(
        "/products/",
        json={"name": "Soda", "price": "1.50", "stock_qty": 10, "category_id": 1, "supplier_id": 1},
        headers=cashier_header,
    )
    assert response.status_code == 403

