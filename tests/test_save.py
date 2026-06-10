def test_read_save_creates_default_player(client):
    response = client.get("/save/")
    assert response.status_code == 200
    data = response.json()
    assert data["money"] == 0.0
    assert data["total_clicks"] == 0
    assert data["cookies_per_second"] == 0.0


def test_save_and_read_back(client):
    client.post(
        "/save/",
        json={
            "money": 250.5,
            "total_clicks": 42,
            "cookies_per_second": 6.0,
        },
    )

    response = client.get("/save/")
    assert response.status_code == 200
    data = response.json()
    assert data["money"] == 250.5
    assert data["total_clicks"] == 42
    assert data["cookies_per_second"] == 6.0


def test_reset_clears_progress(client):
    client.post(
        "/save/",
        json={
            "money": 999,
            "total_clicks": 100,
            "cookies_per_second": 10.0,
        },
    )

    reset = client.delete("/save/reset")
    assert reset.status_code == 200
    assert reset.json() == {"message": "reset"}

    response = client.get("/save/")
    data = response.json()
    assert data["money"] == 0.0
    assert data["total_clicks"] == 0
    assert data["cookies_per_second"] == 0.0


def test_stats_after_save(client):
    client.post(
        "/save/",
        json={
            "money": 100,
            "total_clicks": 10,
            "cookies_per_second": 0,
            "total_money_earned": 500.0,
            "total_upgrades_bought": 3,
            "play_time_seconds": 120,
        },
    )

    response = client.get("/save/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_money_earned"] == 500.0
    assert data["total_upgrades_bought"] == 3
    assert data["play_time_seconds"] == 120
