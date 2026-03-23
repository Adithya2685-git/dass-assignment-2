def test_missing_roll_number_header_returns_401(session, base_url):
    response = session.get(f"{base_url}/api/v1/admin/users")

    assert response.status_code == 401


def test_invalid_roll_number_header_returns_400(session, base_url):
    response = session.get(
        f"{base_url}/api/v1/admin/users",
        headers={"X-Roll-Number": "abc"},
    )

    assert response.status_code == 400


def test_missing_user_id_header_returns_400(session, base_url, admin_headers):
    response = session.get(
        f"{base_url}/api/v1/profile",
        headers=admin_headers,
    )

    assert response.status_code == 400


def test_invalid_user_id_header_returns_400(session, base_url, admin_headers):
    headers = dict(admin_headers)
    headers["X-User-ID"] = "abc"

    response = session.get(
        f"{base_url}/api/v1/profile",
        headers=headers,
    )

    assert response.status_code == 400
