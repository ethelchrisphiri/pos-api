def _create_product(client, admin_header, stock_qty=10, price="2.50"):
    client.post("/categories/", json={"name": "Drinks"}, headers=admin_header)
    client.post("/suppliers/", json={"name": "Acme Co"}, headers=admin_header)
    response = client.post(
        "/products/",
        json={"name": "Cola", "price": price, "stock_qty": stock_qty, "category_id": 1, "supplier_id": 1},
        headers=admin_header,
    )
    return response.json()["product_id"]


def test_full_sale_and_payment_flow(client, admin_header, cashier_header):
    product_id = _create_product(client, admin_header, stock_qty=10)

    sale_response = client.post(
        "/sales/",
        json={"items": [{"product_id": product_id, "quantity": 3}]},
        headers=cashier_header,
    )
    assert sale_response.status_code == 201
    sale = sale_response.json()
    assert float(sale["total_amount"]) == 7.5

    product_response = client.get(f"/products/{product_id}", headers=cashier_header)
    assert product_response.json()["stock_qty"] == 7

    payment_response = client.post(
        "/payments/",
        json={"sale_id": sale["sale_id"], "method": "cash", "amount": "7.50"},
        headers=cashier_header,
    )
    assert payment_response.status_code == 201
    assert payment_response.json()["status"] == "COMPLETED"


def test_sale_rejects_insufficient_stock(client, admin_header, cashier_header):
    product_id = _create_product(client, admin_header, stock_qty=1)

    response = client.post(
        "/sales/",
        json={"items": [{"product_id": product_id, "quantity": 5}]},
        headers=cashier_header,
    )
    assert response.status_code == 400


def test_payment_rejects_amount_over_remaining_balance(client, admin_header, cashier_header):
    product_id = _create_product(client, admin_header, stock_qty=10)
    sale_response = client.post(
        "/sales/",
        json={"items": [{"product_id": product_id, "quantity": 2}]},
        headers=cashier_header,
    )
    sale_id = sale_response.json()["sale_id"]

    response = client.post(
        "/payments/",
        json={"sale_id": sale_id, "method": "cash", "amount": "999.00"},
        headers=cashier_header,
    )
    assert response.status_code == 400


def test_only_manager_can_update_payment_status(client, admin_header, cashier_header):
    product_id = _create_product(client, admin_header, stock_qty=10)
    sale_response = client.post(
        "/sales/",
        json={"items": [{"product_id": product_id, "quantity": 1}]},
        headers=cashier_header,
    )
    sale_id = sale_response.json()["sale_id"]
    payment_response = client.post(
        "/payments/",
        json={"sale_id": sale_id, "method": "cash", "amount": "2.50"},
        headers=cashier_header,
    )
    payment_id = payment_response.json()["payment_id"]

    denied = client.patch(f"/payments/{payment_id}/status", json={"status": "REFUNDED"}, headers=cashier_header)
    assert denied.status_code == 403

    allowed = client.patch(f"/payments/{payment_id}/status", json={"status": "REFUNDED"}, headers=admin_header)
    assert allowed.status_code == 200
    assert allowed.json()["status"] == "REFUNDED"


def test_get_nonexistent_sale_returns_404(client, cashier_header):
    response = client.get("/sales/9999", headers=cashier_header)
    assert response.status_code == 404


def test_sale_rejects_empty_items_list(client, cashier_header):
    response = client.post("/sales/", json={"items": []}, headers=cashier_header)
    assert response.status_code == 422


def test_sale_rejects_nonexistent_product(client, cashier_header):
    response = client.post(
        "/sales/",
        json={"items": [{"product_id": 9999, "quantity": 1}]},
        headers=cashier_header,
    )
    assert response.status_code == 404


def test_get_nonexistent_payment_returns_404(client, cashier_header):
    response = client.get("/payments/9999", headers=cashier_header)
    assert response.status_code == 404


def test_payment_rejects_zero_amount(client, admin_header, cashier_header):
    product_id = _create_product(client, admin_header, stock_qty=10)
    sale_id = client.post(
        "/sales/",
        json={"items": [{"product_id": product_id, "quantity": 1}]},
        headers=cashier_header,
    ).json()["sale_id"]

    response = client.post(
        "/payments/",
        json={"sale_id": sale_id, "method": "cash", "amount": "0"},
        headers=cashier_header,
    )
    assert response.status_code == 422


def test_payment_rejects_invalid_method(client, admin_header, cashier_header):
    product_id = _create_product(client, admin_header, stock_qty=10)
    sale_id = client.post(
        "/sales/",
        json={"items": [{"product_id": product_id, "quantity": 1}]},
        headers=cashier_header,
    ).json()["sale_id"]

    response = client.post(
        "/payments/",
        json={"sale_id": sale_id, "method": "crypto", "amount": "2.50"},
        headers=cashier_header,
    )
    assert response.status_code == 422