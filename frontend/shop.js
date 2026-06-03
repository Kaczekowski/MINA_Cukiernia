const API_URL = "/game";

function openMainPage() {
    window.location.href = "/";
}

async function loadUpgrades() {
    const container = document.getElementById("upgradesContainer");
    container.innerHTML = "Ładowanie...";

    try {
        const response = await fetch(`${API_URL}/upgrades`);

        if (!response.ok) {
            throw new Error("Nie udało się pobrać ulepszeń.");
        }

        const upgrades = await response.json();
        container.innerHTML = "";

        if (upgrades.length === 0) {
            container.innerHTML = "Brak ulepszeń w bazie.";
            return;
        }

        upgrades.forEach((upgrade) => {
            const div = document.createElement("div");
            div.className = "upgradeDiv";

            div.innerHTML = `
                <div class="upgradeContent">
                    <h3>
                        <span class="upgradeIcon">${upgrade.icon}</span>
                        ${upgrade.name}
                    </h3>
                    <p>${upgrade.description}</p>
                    <p>Ilość: ${upgrade.quantity}</p>
                    <p>Koszt: ${upgrade.current_cost.toFixed(2)}</p>
                    <p>CPS: +${upgrade.income_per_second}</p>
                    <p>Click bonus: +${upgrade.click_bonus}</p>
                </div>

                <button class="smallbutton" type="button">
                    Kup
                </button>
            `;

            const button = div.querySelector("button");

            button.addEventListener("click", async () => {
                await buyUpgrade(upgrade.id);
            });

            container.appendChild(div);
        });
    } catch (error) {
        container.innerHTML = "Błąd ładowania ulepszeń";
        console.error(error);
    }
}

async function buyUpgrade(upgradeId) {
    try {
        const response = await fetch(`${API_URL}/buy/${upgradeId}`, {
            method: "POST",
        });

        if (!response.ok) {
            throw new Error("Nie udało się kupić ulepszenia.");
        }

        const data = await response.json();

        if (!data.success) {
            alert("Za mało pieniędzy");
            return;
        }

        await loadUpgrades();
    } catch (error) {
        console.error(error);
        alert("Błąd kupowania ulepszenia");
    }
}

window.addEventListener("DOMContentLoaded", loadUpgrades);
