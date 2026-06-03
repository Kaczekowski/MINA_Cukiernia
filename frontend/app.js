function openShop() {
    window.location.href = "/shop.html";
}

const initialGameState = {
    money: 0,
    total_clicks: 0,
    cookies_per_second: 0,
};

let gameState = { ...initialGameState };

function formatNumber(value, maximumFractionDigits = 2) {
    return new Intl.NumberFormat("pl-PL", {
        minimumFractionDigits: 0,
        maximumFractionDigits,
    }).format(Number(value) || 0);
}

function setStatus(message = "") {
    document.getElementById("statusText").textContent = message;
}

function renderGameState() {
    document.getElementById("moneyValue").textContent = formatNumber(gameState.money);
    document.getElementById("totalClicksValue").textContent = formatNumber(
        gameState.total_clicks,
        0,
    );
    document.getElementById("cookiesPerSecondValue").textContent = formatNumber(
        gameState.cookies_per_second,
    );
}

async function loadSave() {
    try {
        const response = await fetch("/save/");

        if (!response.ok) {
            throw new Error("Nie udało się wczytać zapisu gry.");
        }

        const save = await response.json();
        gameState = {
            money: save.money,
            total_clicks: save.total_clicks,
            cookies_per_second: save.cookies_per_second,
        };
        renderGameState();
        setStatus();
    } catch (error) {
        setStatus(error.message);
    }
}

async function handleCookieClick() {
    const button = document.getElementById("cookieButton");
    button.disabled = true;

    try {
        const response = await fetch("/game/click", {
            method: "POST",
        });

        if (!response.ok) {
            throw new Error("Nie udało się zapisać kliknięcia.");
        }

        const result = await response.json();
        gameState.money = result.money;
        gameState.total_clicks = result.total_clicks;
        renderGameState();
        setStatus();
    } catch (error) {
        setStatus(error.message);
    } finally {
        button.disabled = false;
    }
}

window.addEventListener("DOMContentLoaded", () => {
    document
        .getElementById("cookieButton")
        .addEventListener("click", handleCookieClick);
    renderGameState();
    loadSave();
});
