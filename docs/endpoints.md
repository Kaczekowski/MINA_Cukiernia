# Endpointy API

Aplikacja nasłuchuje domyślnie na `http://127.0.0.1:8000`.

---

## Health check

### `GET /health`

Prosty health-check.

**Odpowiedź:**

```json
{"status": "ok"}
```

**Przykład:**

```bash
curl http://127.0.0.1:8000/health
```

---

## Gra (`/game`)

### `POST /game/click`

Rejestruje jedno kliknięcie. Dodaje `1 + bonusy z ulepszeń` do pieniędzy gracza i zwiększa licznik kliknięć.

**Odpowiedź (`ClickOut`):**

```json
{
  "money": 5.0,
  "total_clicks": 5,
  "cookies_per_second": 0.0
}
```

**Przykład:**

```bash
curl -X POST http://127.0.0.1:8000/game/click
```

---

### `POST /game/tick`

Dolicza automatyczny przychód z ulepszeń (cookies per second) do pieniędzy gracza. Frontend wywołuje co 1 sekundę.

**Odpowiedź (`TickOut`):**

```json
{
  "money": 12.0,
  "cookies_per_second": 6.0
}
```

**Przykład:**

```bash
curl -X POST http://127.0.0.1:8000/game/tick
```

---

### `POST /game/buy/{upgrade_id}`

Kupuje ulepszenie o podanym ID. Jeśli gracz ma za mało pieniędzy, zwraca `success: false` bez modyfikacji stanu.

Koszt rośnie wykładniczo: `base_cost * cost_scaling ^ posiadana_ilość`.

**Parametry ścieżki:**

| Parametr     | Typ  | Opis                 |
|--------------|------|----------------------|
| `upgrade_id` | int  | ID ulepszenia (1-10) |

**Odpowiedź (`BuyUpgradeOut`):**

Sukces:

```json
{
  "success": true,
  "money": 950.0,
  "upgrade_id": 1,
  "new_quantity": 1,
  "next_cost": 57.5,
  "cookies_per_second": 0.0
}
```

Brak pieniędzy:

```json
{
  "success": false,
  "money": 10.0,
  "upgrade_id": 1,
  "new_quantity": 0,
  "next_cost": 50.0,
  "cookies_per_second": 0.0
}
```

Nieistniejące ulepszenie → `404`:

```json
{"detail": "Upgrade 999 nie istnieje"}
```

**Przykład:**

```bash
curl -X POST http://127.0.0.1:8000/game/buy/1
```

---

### `GET /game/upgrades`

Zwraca listę wszystkich dostępnych ulepszeń wraz z aktualnym kosztem i ilością posiadaną przez gracza.

**Odpowiedź (lista `UpgradeOut`):**

```json
[
  {
    "id": 1,
    "name": "Łyżka",
    "description": "Zwykła łyżka do mieszania",
    "icon": "🥄",
    "base_cost": 50.0,
    "cost_scaling": 1.15,
    "income_per_second": 0.0,
    "click_bonus": 1.0,
    "current_cost": 50.0,
    "quantity": 0
  }
]
```

**Przykład:**

```bash
curl http://127.0.0.1:8000/game/upgrades
```

---

## Zapis (`/save`)

### `GET /save/`

Odczytuje aktualny stan zapisu gry.

**Odpowiedź (`SaveOut`):**

```json
{
  "id": 1,
  "money": 123.5,
  "total_clicks": 42,
  "cookies_per_second": 6.0,
  "stats": {
    "total_money_earned": 200.0,
    "total_upgrades_bought": 3,
    "play_time_seconds": 600
  }
}
```

**Przykład:**

```bash
curl http://127.0.0.1:8000/save/
```

---

### `POST /save/`

Zapisuje stan gry wysłany z frontendu.

**Request body (`SaveIn`):**

```json
{
  "money": 500.0,
  "total_clicks": 100,
  "cookies_per_second": 6.0,
  "total_money_earned": 800.0,
  "total_upgrades_bought": 5,
  "play_time_seconds": 1200
}
```

**Odpowiedź (`SaveOut`):** taki sam schemat jak `GET /save/`.

**Przykład:**

```bash
curl -X POST http://127.0.0.1:8000/save/ \
  -H "Content-Type: application/json" \
  -d '{"money":500,"total_clicks":100,"cookies_per_second":6}'
```

---

### `DELETE /save/reset`

Resetuje grę — usuwa gracza, statystyki i ulepszenia, tworzy nowego gracza.

**Odpowiedź (`ResetOut`):**

```json
{"message": "reset"}
```

**Przykład:**

```bash
curl -X DELETE http://127.0.0.1:8000/save/reset
```

---

### `GET /save/stats`

Zwraca statystyki gracza.

**Odpowiedź (`StatsOut`):**

```json
{
  "total_money_earned": 200.0,
  "total_upgrades_bought": 3,
  "play_time_seconds": 600
}
```

**Przykład:**

```bash
curl http://127.0.0.1:8000/save/stats
```

---

## Statyki (frontend)

### `GET /` i `GET /{path}`

Pliki statyczne z katalogu `frontend/` zamontowane jako `StaticFiles(html=True)`.

- `GET /` → `frontend/index.html` (strona główna gry)
- `GET /shop.html` → `frontend/shop.html` (sklep z ulepszeniami)
- `GET /app.js`, `GET /style.css`, ... → odpowiednie pliki JS/CSS
