from blackbox.tests.test_cart_and_checkout import _clear_cart, _pick_product


def _wallet_balance(payload):
    if isinstance(payload, dict):
        for key in ("balance", "wallet_balance", "amount"):
            if key in payload:
                return payload[key]
        if "wallet" in payload and isinstance(payload["wallet"], dict):
            return _wallet_balance(payload["wallet"])
    raise AssertionError("Could not locate wallet balance in response payload")


def _loyalty_points(payload):
    if isinstance(payload, dict):
        for key in ("points", "loyalty_points"):
            if key in payload:
                return payload[key]
        if "loyalty" in payload and isinstance(payload["loyalty"], dict):
            return _loyalty_points(payload["loyalty"])
    raise AssertionError("Could not locate loyalty points in response payload")


def _order_id_from_checkout(payload):
    if isinstance(payload, dict):
        if "order_id" in payload:
            return payload["order_id"]
        if "order" in payload and isinstance(payload["order"], dict):
            return payload["order"].get("order_id")
        if "data" in payload and isinstance(payload["data"], dict):
            return payload["data"].get("order_id")
    return None


def _invoice_value(payload, key):
    if isinstance(payload, dict):
        if key in payload:
            return payload[key]
        for nested_key in ("invoice", "data", "order"):
            nested = payload.get(nested_key)
            if isinstance(nested, dict):
                value = _invoice_value(nested, key)
                if value is not None:
                    return value
    return None


def test_apply_expired_coupon_is_rejected(session, base_url, user_headers):
    _clear_cart(session, base_url, user_headers)
    product = _pick_product(session, base_url, user_headers, min_stock=1)
    added = session.post(
        f"{base_url}/api/v1/cart/add",
        headers=user_headers,
        json={"product_id": product["product_id"], "quantity": 1},
    )

    assert added.status_code == 200

    response = session.post(
        f"{base_url}/api/v1/coupon/apply",
        headers=user_headers,
        json={"code": "EXPIRED50"},
    )

    assert response.status_code == 400


def test_remove_coupon_returns_success(session, base_url, user_headers):
    response = session.post(
        f"{base_url}/api/v1/coupon/remove",
        headers=user_headers,
        json={},
    )

    assert response.status_code in (200, 204)


def test_get_wallet_returns_json(session, base_url, user_headers):
    response = session.get(
        f"{base_url}/api/v1/wallet",
        headers=user_headers,
    )

    assert response.status_code == 200
    assert "application/json" in response.headers.get("Content-Type", "")
    assert _wallet_balance(response.json()) >= 0


def test_wallet_add_rejects_zero_amount(session, base_url, user_headers):
    response = session.post(
        f"{base_url}/api/v1/wallet/add",
        headers=user_headers,
        json={"amount": 0},
    )

    assert response.status_code == 400


def test_wallet_add_rejects_amount_above_limit(session, base_url, user_headers):
    response = session.post(
        f"{base_url}/api/v1/wallet/add",
        headers=user_headers,
        json={"amount": 100001},
    )

    assert response.status_code == 400


def test_wallet_pay_rejects_insufficient_balance(session, base_url, user_headers):
    wallet_before = session.get(
        f"{base_url}/api/v1/wallet",
        headers=user_headers,
    )
    assert wallet_before.status_code == 200
    current_balance = _wallet_balance(wallet_before.json())

    response = session.post(
        f"{base_url}/api/v1/wallet/pay",
        headers=user_headers,
        json={"amount": current_balance + 1},
    )

    assert response.status_code == 400


def test_wallet_pay_deducts_exact_amount(session, base_url, user_headers):
    add_response = session.post(
        f"{base_url}/api/v1/wallet/add",
        headers=user_headers,
        json={"amount": 25},
    )
    assert add_response.status_code == 200

    before = session.get(
        f"{base_url}/api/v1/wallet",
        headers=user_headers,
    )
    assert before.status_code == 200
    before_balance = _wallet_balance(before.json())

    pay_response = session.post(
        f"{base_url}/api/v1/wallet/pay",
        headers=user_headers,
        json={"amount": 10},
    )
    assert pay_response.status_code == 200

    after = session.get(
        f"{base_url}/api/v1/wallet",
        headers=user_headers,
    )
    assert after.status_code == 200
    after_balance = _wallet_balance(after.json())

    assert round(before_balance - after_balance, 2) == 10


def test_get_loyalty_returns_json(session, base_url, user_headers):
    response = session.get(
        f"{base_url}/api/v1/loyalty",
        headers=user_headers,
    )

    assert response.status_code == 200
    assert "application/json" in response.headers.get("Content-Type", "")
    assert _loyalty_points(response.json()) >= 0


def test_loyalty_redeem_rejects_zero_amount(session, base_url, user_headers):
    response = session.post(
        f"{base_url}/api/v1/loyalty/redeem",
        headers=user_headers,
        json={"points": 0},
    )

    assert response.status_code == 400


def test_loyalty_redeem_rejects_when_points_are_insufficient(session, base_url, user_headers):
    current = session.get(
        f"{base_url}/api/v1/loyalty",
        headers=user_headers,
    )
    assert current.status_code == 200
    points = _loyalty_points(current.json())

    response = session.post(
        f"{base_url}/api/v1/loyalty/redeem",
        headers=user_headers,
        json={"points": points + 1},
    )

    assert response.status_code == 400


def test_get_orders_returns_json_list(session, base_url, user_headers):
    response = session.get(
        f"{base_url}/api/v1/orders",
        headers=user_headers,
    )

    assert response.status_code == 200
    assert "application/json" in response.headers.get("Content-Type", "")
    assert isinstance(response.json(), list)


def test_cancel_missing_order_returns_404(session, base_url, user_headers):
    response = session.post(
        f"{base_url}/api/v1/orders/999999999/cancel",
        headers=user_headers,
    )

    assert response.status_code == 404


def test_card_checkout_creates_order_with_paid_status(session, base_url, user_headers):
    _clear_cart(session, base_url, user_headers)
    product = _pick_product(session, base_url, user_headers, min_stock=1)
    added = session.post(
        f"{base_url}/api/v1/cart/add",
        headers=user_headers,
        json={"product_id": product["product_id"], "quantity": 1},
    )
    assert added.status_code == 200

    checkout = session.post(
        f"{base_url}/api/v1/checkout",
        headers=user_headers,
        json={"payment_method": "CARD"},
    )

    assert checkout.status_code == 200
    order_id = _order_id_from_checkout(checkout.json())
    assert order_id is not None

    detail = session.get(
        f"{base_url}/api/v1/orders/{order_id}",
        headers=user_headers,
    )

    assert detail.status_code == 200
    payload = detail.json()
    status_text = str(payload).upper()
    assert "PAID" in status_text


def test_invoice_total_is_not_less_than_subtotal(session, base_url, user_headers):
    orders = session.get(
        f"{base_url}/api/v1/orders",
        headers=user_headers,
    )
    assert orders.status_code == 200
    order_list = orders.json()
    assert isinstance(order_list, list)
    assert order_list, "No orders available for invoice test"

    order_id = order_list[0]["order_id"]
    invoice = session.get(
        f"{base_url}/api/v1/orders/{order_id}/invoice",
        headers=user_headers,
    )

    assert invoice.status_code == 200
    payload = invoice.json()

    subtotal = _invoice_value(payload, "subtotal")
    total = _invoice_value(payload, "total")

    assert subtotal is not None
    assert total is not None
    assert total >= subtotal
