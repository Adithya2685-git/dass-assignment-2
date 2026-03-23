def test_admin_users_returns_success_and_json(session, base_url, admin_headers):
    response = session.get(
        f"{base_url}/api/v1/admin/users",
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert "application/json" in response.headers.get("Content-Type", "")
    assert isinstance(response.json(), list)


def test_admin_products_returns_success_and_json(session, base_url, admin_headers):
    response = session.get(
        f"{base_url}/api/v1/admin/products",
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert "application/json" in response.headers.get("Content-Type", "")
    assert isinstance(response.json(), list)
