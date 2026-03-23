def test_get_profile_returns_success_and_json(session, base_url, user_headers):
    response = session.get(
        f"{base_url}/api/v1/profile",
        headers=user_headers,
    )

    assert response.status_code == 200
    assert "application/json" in response.headers.get("Content-Type", "")
    assert isinstance(response.json(), dict)


def test_update_profile_rejects_short_name(session, base_url, user_headers):
    response = session.put(
        f"{base_url}/api/v1/profile",
        headers=user_headers,
        json={"name": "A", "phone": "9876543210"},
    )

    assert response.status_code == 400


def test_update_profile_rejects_invalid_phone(session, base_url, user_headers):
    response = session.put(
        f"{base_url}/api/v1/profile",
        headers=user_headers,
        json={"name": "Valid Name", "phone": "12345"},
    )

    assert response.status_code == 400


def test_products_list_returns_only_active_products(session, base_url, user_headers):
    admin_response = session.get(
        f"{base_url}/api/v1/admin/products",
        headers={"X-Roll-Number": user_headers["X-Roll-Number"]},
    )
    products_response = session.get(
        f"{base_url}/api/v1/products",
        headers=user_headers,
    )

    assert admin_response.status_code == 200
    assert products_response.status_code == 200

    admin_products = admin_response.json()
    listed_products = products_response.json()

    assert isinstance(admin_products, list)
    assert isinstance(listed_products, list)

    active_ids = {
        product["product_id"]
        for product in admin_products
        if product.get("is_active") is True
    }
    listed_ids = {product["product_id"] for product in listed_products}

    assert listed_ids <= active_ids


def test_get_missing_product_returns_404(session, base_url, user_headers):
    response = session.get(
        f"{base_url}/api/v1/products/999999999",
        headers=user_headers,
    )

    assert response.status_code == 404
