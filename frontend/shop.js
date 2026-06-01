const baseAddress = "http://127.0.0.1:8000";

function openMainPage() {
	window.location.replace(baseAddress);
}const API_URL = "http://localhost:8000/game";

async function loadUpgrades() {
    const container = document.getElementById("upgradesContainer");

    container.innerHTML = "Ładowanie...";

    try {
        const response = await fetch(`${API_URL}/upgrades`);
        const upgrades = await response.json();

        container.innerHTML = "";

        upgrades.forEach(upgrade => {
            const div = document.createElement("div");
            div.className = "upgradeDiv";

            div.innerHTML = `
                <div class="upgradeContent">
                    <h3>${upgrade.icon} ${upgrade.name}</h3>
                    <p>${upgrade.description}</p>
                    <p>Ilość: ${upgrade.quantity}</p>
                    <p>Koszt: ${upgrade.current_cost.toFixed(2)}</p>
                    <p>CPS: +${upgrade.income_per_second}</p>
                    <p>Click bonus: +${upgrade.click_bonus}</p>
                </div>

                <button class="smallbutton">
                    Kup
                </button>
            `;

            const button = div.querySelector("button");

            button.addEventListener("click", async () => {
                await buyUpgrade(upgrade.id);
            });

            container.appendChild(div);
        });

    } catch (err) {
        container.innerHTML = "Błąd ładowania ulepszeń";
        console.error(err);
    }
}

async function buyUpgrade(upgradeId) {
    try {
        const response = await fetch(`${API_URL}/buy/${upgradeId}`, {
            method: "POST"
        });

        const data = await response.json();

        if (!data.success) {
            alert("Za mało pieniędzy");
            return;
        }

        await loadUpgrades();

    } catch (err) {
        console.error(err);
        alert("Błąd kupowania ulepszenia");
    }
}

function openMainPage() {
    window.location.href = "index.html";
}

window.addEventListener("DOMContentLoaded", loadUpgrades);
