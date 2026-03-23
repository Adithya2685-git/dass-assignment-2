def _clear_cart(session, base_url, user_headers):
    response = session.delete(
        f"{base_url}/api/v1/cart/clear",
        headers=user_headers,
    )
    assert response.status_code in (200, 204)


def _admin_products(session, base_url, user_headers):
    response = session.get(
        f"{base_url}/api/v1/admin/products",
        headers={"X-Roll-Number": user_headers["X-Roll-Number"]},
    )
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    return products


def _pick_product(session, base_url, user_headers, min_stock=1):
    for product in _admin_products(session, base_url, user_headers):
        if product.get("is_active") is True and product.get("stock", 0) >= min_stock:
            return product
    raise AssertionError("No suitable active product with enough stock was found")


def _cart_items(payload):
    if isinstance(payload, dict):
        for key in ("items", "cart_items"):
            if key in payload and isinstance(payload[key], list):
                return payload[key]
    if isinstance(payload, list):
        return payload
    raise AssertionError("Could not locate cart items in response payload")


def _cart_total(payload):
    if isinstance(payload, dict):
        for key in ("total", "cart_total"):
            if key in payload:
                return payload[key]
    return sum(item["subtotal"] for item in _cart_items(payload))


def _cart_item_by_product_id(payload, product_id):
    for item in _cart_items(payload):
        if item.get("product_id") == product_id:
            return item
    raise AssertionError(f"Product {product_id} not found in cart response")


def test_get_cart_returns_json(session, base_url, user_headers):
    response = session.get(
        f"{base_url}/api/v1/cart",
        headers=user_headers,
    )

    assert response.status_code == 200
    assert "application/json" in response.headers.get("Content-Type", "")


def test_add_to_cart_rejects_zero_quantity(session, base_url, user_headers):
    response = session.post(
        f"{base_url}/api/v1/cart/add",
        headers=user_headers,
        json={"product_id": 1, "quantity": 0},
    )

    assert response.status_code == 400


def test_add_to_cart_rejects_missing_product(session, base_url, user_headers):
    response = session.post(
        f"{base_url}/api/v1/cart/add",
        headers=user_headers,
        json={"product_id": 999999999, "quantity": 1},
    )

    assert response.status_code == 404


def test_adding_same_product_twice_accumulates_quantity(session, base_url, user_headers):
    _clear_cart(session, base_url, user_headers)
    product = _pick_product(session, base_url, user_headers, min_stock=2)

    first = session.post(
        f"{base_url}/api/v1/cart/add",
        headers=user_headers,
        json={"product_id": product["product_id"], "quantity": 1},
    )
    second = session.post(
        f"{base_url}/api/v1/cart/add",
        headers=user_headers,
        json={"product_id": product["product_id"], "quantity": 1},
    )
    listing = session.get(
        f"{base_url}/api/v1/cart",
        headers=user_headers,
    )

    assert first.status_code == 200
    assert second.status_code == 200
    assert listing.status_code == 200

    item = _cart_item_by_product_id(listing.json(), product["product_id"])
    assert item["quantity"] == 2


def test_update_cart_rejects_zero_quantity(session, base_url, user_headers):
    _clear_cart(session, base_url, user_headers)
    product = _pick_product(session, base_url, user_headers, min_stock=1)
    added = session.post(
        f"{base_url}/api/v1/cart/add",
        headers=user_headers,
        json={"product_id": product["product_id"], "quantity": 1},
    )

    assert added.status_code == 200

    updated = session.post(
        f"{base_url}/api/v1/cart/update",
        headers=user_headers,
        json={"product_id": product["product_id"], "quantity": 0},
    )

    assert updated.status_code == 400


def test_remove_missing_cart_item_returns_404(session, base_url, user_headers):
    _clear_cart(session, base_url, user_headers)

    response = session.post(
        f"{base_url}/api/v1/cart/remove",
        headers=user_headers,
        json={"product_id": 999999999},
    )

    assert response.status_code == 404


def test_cart_total_matches_sum_of_item_subtotals(session, base_url, user_headers):
    _clear_cart(session, base_url, user_headers)
    first_product = _pick_product(session, base_url, user_headers, min_stock=1)

    second_product = None
    for product in _admin_products(session, base_url, user_headers):
        if (
            product.get("is_active") is True
            and product.get("stock", 0) >= 1
            and product["product_id"] != first_product["product_id"]
        ):
            second_product = product
            break

    if second_product is None:
        raise AssertionError("Could not find a second active product for cart total test")

    add_first = session.post(
        f"{base_url}/api/v1/cart/add",
        headers=user_headers,
        json={"product_id": first_product["product_id"], "quantity": 1},
    )
    add_second = session.post(
        f"{base_url}/api/v1/cart/add",
        headers=user_headers,
        json={"product_id": second_product["product_id"], "quantity": 1},
    )
    listing = session.get(
        f"{base_url}/api/v1/cart",
        headers=user_headers,
    )

    assert add_first.status_code == 200
    assert add_second.status_code == 200
    assert listing.status_code == 200

    payload = listing.json()
    items = _cart_items(payload)
    subtotal_sum = sum(item["subtotal"] for item in items)

    assert _cart_total(payload) == subtotal_sum


def test_checkout_rejects_empty_cart(session, base_url, user_headers):
    _clear_cart(session, base_url, user_headers)

    response = session.post(
        f"{base_url}/api/v1/checkout",
        headers=user_headers,
        json={"payment_method": "CARD"},
    )

    assert response.status_code == 400


def test_checkout_rejects_invalid_payment_method(session, base_url, user_headers):
    _clear_cart(session, base_url, user_headers)
    product = _pick_product(session, base_url, user_headers, min_stock=1)
    added = session.post(
        f"{base_url}/api/v1/cart/add",
        headers=user_headers,
        json={"product_id": product["product_id"], "quantity": 1},
    )

    assert added.status_code == 200

    response = session.post(
        f"{base_url}/api/v1/checkout",
        headers=user_headers,
        json={"payment_method": "UPI"},
    )

    assert response.status_code == 400
