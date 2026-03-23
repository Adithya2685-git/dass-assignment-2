import time


def _review_payload(rating=5, comment=None):
    if comment is None:
        comment = f"Review comment {int(time.time() * 1000) % 100000}"
    return {"rating": rating, "comment": comment}


def _ticket_payload(subject=None, message=None):
    suffix = str(int(time.time() * 1000))[-6:]
    if subject is None:
        subject = f"Order issue {suffix}"
    if message is None:
        message = f"Need help with order flow {suffix}"
    return {"subject": subject, "message": message}


def _ticket_id_from_payload(payload):
    if isinstance(payload, dict):
        if "ticket_id" in payload:
            return payload["ticket_id"]
        if "ticket" in payload and isinstance(payload["ticket"], dict):
            return payload["ticket"].get("ticket_id")
        if "data" in payload and isinstance(payload["data"], dict):
            return payload["data"].get("ticket_id")
    return None


def test_get_reviews_returns_json(session, base_url, user_headers):
    response = session.get(
        f"{base_url}/api/v1/products/1/reviews",
        headers=user_headers,
    )

    assert response.status_code == 200
    assert "application/json" in response.headers.get("Content-Type", "")


def test_add_review_rejects_rating_below_range(session, base_url, user_headers):
    response = session.post(
        f"{base_url}/api/v1/products/1/reviews",
        headers=user_headers,
        json=_review_payload(rating=0),
    )

    assert response.status_code == 400


def test_add_review_rejects_rating_above_range(session, base_url, user_headers):
    response = session.post(
        f"{base_url}/api/v1/products/1/reviews",
        headers=user_headers,
        json=_review_payload(rating=6),
    )

    assert response.status_code == 400


def test_add_review_rejects_empty_comment(session, base_url, user_headers):
    response = session.post(
        f"{base_url}/api/v1/products/1/reviews",
        headers=user_headers,
        json=_review_payload(rating=5, comment=""),
    )

    assert response.status_code == 400


def test_add_review_rejects_comment_longer_than_200(session, base_url, user_headers):
    response = session.post(
        f"{base_url}/api/v1/products/1/reviews",
        headers=user_headers,
        json=_review_payload(rating=5, comment="a" * 201),
    )

    assert response.status_code == 400


def test_get_support_tickets_returns_json_list(session, base_url, user_headers):
    response = session.get(
        f"{base_url}/api/v1/support/tickets",
        headers=user_headers,
    )

    assert response.status_code == 200
    assert "application/json" in response.headers.get("Content-Type", "")
    assert isinstance(response.json(), list)


def test_create_ticket_rejects_short_subject(session, base_url, user_headers):
    response = session.post(
        f"{base_url}/api/v1/support/ticket",
        headers=user_headers,
        json=_ticket_payload(subject="Help", message="Need help now"),
    )

    assert response.status_code == 400


def test_create_ticket_rejects_empty_message(session, base_url, user_headers):
    response = session.post(
        f"{base_url}/api/v1/support/ticket",
        headers=user_headers,
        json=_ticket_payload(message=""),
    )

    assert response.status_code == 400


def test_create_ticket_starts_with_open_status(session, base_url, user_headers):
    response = session.post(
        f"{base_url}/api/v1/support/ticket",
        headers=user_headers,
        json=_ticket_payload(),
    )

    assert response.status_code in (200, 201)
    payload = response.json()
    status_text = str(payload).upper()
    assert "OPEN" in status_text


def test_ticket_status_cannot_jump_from_open_to_closed(session, base_url, user_headers):
    create_response = session.post(
        f"{base_url}/api/v1/support/ticket",
        headers=user_headers,
        json=_ticket_payload(),
    )

    assert create_response.status_code in (200, 201)
    ticket_id = _ticket_id_from_payload(create_response.json())
    assert ticket_id is not None

    update_response = session.put(
        f"{base_url}/api/v1/support/tickets/{ticket_id}",
        headers=user_headers,
        json={"status": "CLOSED"},
    )

    assert update_response.status_code == 400


def test_ticket_status_can_move_open_to_in_progress(session, base_url, user_headers):
    create_response = session.post(
        f"{base_url}/api/v1/support/ticket",
        headers=user_headers,
        json=_ticket_payload(),
    )

    assert create_response.status_code in (200, 201)
    ticket_id = _ticket_id_from_payload(create_response.json())
    assert ticket_id is not None

    update_response = session.put(
        f"{base_url}/api/v1/support/tickets/{ticket_id}",
        headers=user_headers,
        json={"status": "IN_PROGRESS"},
    )

    assert update_response.status_code == 200
