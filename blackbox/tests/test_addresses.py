import time


def _address_from_payload(payload):
    if isinstance(payload, dict):
        if "address" in payload and isinstance(payload["address"], dict):
            return payload["address"]
        if "data" in payload and isinstance(payload["data"], dict):
            return payload["data"]
    return payload


def _new_address_payload(label="HOME", is_default=False):
    suffix = str(int(time.time() * 1000))[-6:]
    return {
        "label": label,
        "street": f"Maple Street {suffix}",
        "city": "Bangalore",
        "pincode": "560001",
        "is_default": is_default,
    }


def test_get_addresses_returns_json_list(session, base_url, user_headers):
    response = session.get(
        f"{base_url}/api/v1/addresses",
        headers=user_headers,
    )

    assert response.status_code == 200
    assert "application/json" in response.headers.get("Content-Type", "")
    assert isinstance(response.json(), list)


def test_add_address_rejects_invalid_label(session, base_url, user_headers):
    payload = _new_address_payload(label="HOSTEL")

    response = session.post(
        f"{base_url}/api/v1/addresses",
        headers=user_headers,
        json=payload,
    )

    assert response.status_code == 400


def test_add_address_rejects_invalid_pincode(session, base_url, user_headers):
    payload = _new_address_payload()
    payload["pincode"] = "12345"

    response = session.post(
        f"{base_url}/api/v1/addresses",
        headers=user_headers,
        json=payload,
    )

    assert response.status_code == 400


def test_add_address_returns_created_address_object(session, base_url, user_headers):
    payload = _new_address_payload(label="OTHER")

    response = session.post(
        f"{base_url}/api/v1/addresses",
        headers=user_headers,
        json=payload,
    )

    assert response.status_code in (200, 201)

    created = _address_from_payload(response.json())

    assert created["label"] == payload["label"]
    assert created["street"] == payload["street"]
    assert created["city"] == payload["city"]
    assert created["pincode"] == payload["pincode"]
    assert "address_id" in created
    assert "is_default" in created


def test_new_default_address_replaces_old_default(session, base_url, user_headers):
    first_response = session.post(
        f"{base_url}/api/v1/addresses",
        headers=user_headers,
        json=_new_address_payload(label="HOME", is_default=True),
    )
    second_response = session.post(
        f"{base_url}/api/v1/addresses",
        headers=user_headers,
        json=_new_address_payload(label="OFFICE", is_default=True),
    )

    assert first_response.status_code in (200, 201)
    assert second_response.status_code in (200, 201)

    second_address = _address_from_payload(second_response.json())

    listing = session.get(
        f"{base_url}/api/v1/addresses",
        headers=user_headers,
    )

    assert listing.status_code == 200
    addresses = listing.json()
    default_addresses = [address for address in addresses if address["is_default"]]

    assert len(default_addresses) == 1
    assert default_addresses[0]["address_id"] == second_address["address_id"]


def test_update_address_returns_new_street_not_old_data(session, base_url, user_headers):
    create_response = session.post(
        f"{base_url}/api/v1/addresses",
        headers=user_headers,
        json=_new_address_payload(label="HOME"),
    )

    assert create_response.status_code in (200, 201)
    created = _address_from_payload(create_response.json())
    address_id = created["address_id"]
    new_street = f"Updated Street {address_id}"

    update_response = session.put(
        f"{base_url}/api/v1/addresses/{address_id}",
        headers=user_headers,
        json={"street": new_street, "is_default": False},
    )

    assert update_response.status_code == 200
    updated = _address_from_payload(update_response.json())
    assert updated["street"] == new_street


def test_delete_missing_address_returns_404(session, base_url, user_headers):
    response = session.delete(
        f"{base_url}/api/v1/addresses/999999999",
        headers=user_headers,
    )

    assert response.status_code == 404
