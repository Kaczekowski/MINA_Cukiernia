def test_index_returns_html(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Cukiernia" in response.text


def test_shop_page_returns_html(client):
    response = client.get("/shop.html")
    assert response.status_code == 200
    assert "Sklep" in response.text
