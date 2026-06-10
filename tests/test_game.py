def test_click_increments_money_and_clicks(client):
    r1 = client.post("/game/click")
    assert r1.status_code == 200
    data1 = r1.json()
    assert data1["money"] == 1.0
    assert data1["total_clicks"] == 1
    assert data1["cookies_per_second"] == 0.0

    r2 = client.post("/game/click")
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["money"] == 2.0
    assert data2["total_clicks"] == 2


def test_buy_upgrade_fails_when_not_enough_money(client):
    response = client.post("/game/buy/1")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["money"] == 0.0
    assert data["new_quantity"] == 0
    assert data["next_cost"] == 50.0


def test_buy_upgrade_succeeds_when_enough_money(client):
    from pytest import approx

    client.post(
        "/save/",
        json={
            "money": 1000,
            "total_clicks": 0,
            "cookies_per_second": 0,
        },
    )

    response = client.post("/game/buy/1")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["money"] == 950.0
    assert data["new_quantity"] == 1
    assert data["next_cost"] == approx(57.5)


def test_buy_nonexistent_upgrade_returns_404(client):
    response = client.post("/game/buy/9999")
    assert response.status_code == 404


def test_tick_adds_cps_to_money(client):
    client.post(
        "/save/",
        json={"money": 1000, "total_clicks": 0, "cookies_per_second": 0},
    )
    client.post("/game/buy/2")

    response = client.post("/game/tick")
    assert response.status_code == 200
    data = response.json()
    assert data["cookies_per_second"] == 1.0
    assert data["money"] > 875.0


def test_click_bonus_after_upgrade(client):
    client.post(
        "/save/",
        json={"money": 1000, "total_clicks": 0, "cookies_per_second": 0},
    )
    client.post("/game/buy/1")

    response = client.post("/game/click")
    assert response.status_code == 200
    data = response.json()
    assert data["money"] > 950.0
    assert data["total_clicks"] == 1


def test_list_upgrades_returns_all(client):
    response = client.get("/game/upgrades")
    assert response.status_code == 200
    upgrades = response.json()
    assert len(upgrades) == 10
    for u in upgrades:
        assert "id" in u
        assert "name" in u
        assert "current_cost" in u
        assert "quantity" in u
