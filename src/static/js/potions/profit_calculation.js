document.addEventListener("DOMContentLoaded", function () {
    const showProfitBtn = document.getElementById("show-profit-btn");
    const backBtn = document.getElementById("back-to-inputs-btn");
    const inputsView = document.getElementById("v-potion-tabs-content");
    const profitView = document.getElementById("profit-view");

    if (showProfitBtn) {
        showProfitBtn.addEventListener("click", () => {
            inputsView.style.display = "none";
            profitView.style.display = "block";
            renderProfitTable();
            if (profitView) {
                requestAnimationFrame(() => {
                    profitView.scrollIntoView({ behavior: "smooth", block: "start" });
                });
            }
        });
    }

    if (backBtn) {
        backBtn.addEventListener("click", () => {
            profitView.style.display = "none";
            inputsView.style.display = "block";
        });
    }

    document.querySelectorAll(".nav-link").forEach(pill => {
        pill.addEventListener("click", () => {
            profitView.style.display = "none";
            inputsView.style.display = "block";
        });
    });
});

window.renderProfitTable = function () {
    const tbody = document.getElementById("profit-table-body-js");
    if (!tbody) return;

    tbody.innerHTML = "";

    const recipes = calculation_data.recipes;
    const prices = calculation_data.ingredient_prices;
    const animalRemainsPrice = prices.animal_remains || 0;
    console.log(prices)

    function formatName(code) {
        const parts = code.split("_");
        const tier = parts[0];
        const name = parts[1].charAt(0).toUpperCase() + parts[1].slice(1).toLowerCase();
        const enchant = parts[2];
        return { tier, name, enchant };
    }

    function getSalePrice(code) {
        const input = document.querySelector(`[data-potion-code="${code}"]`);
        if (input && input.value) {
            const val = parseInt(input.value);
            return isNaN(val) ? null : val;
        }
        return null;
    }

    function createCell(text, className = "", label = "") {
        const td = document.createElement("td");
        td.innerText = text;
        if (className) td.className = className;
        if (label) td.setAttribute("data-label", label);
        return td;
    }

    Object.entries(recipes).forEach(([baseCode, recipeData]) => {
        const ingredients = recipeData.ingredients;
        const yieldQty = recipeData.yield || 1;

        let missing = [];
        let baseTotal = 0;

        for (const [ingredient, qty] of ingredients) {
            const price = prices[ingredient];
            if (price === undefined || price === null || price === 0) {
                missing.push(ingredient);
            } else {
                baseTotal += price * qty;
            }
        }

        if (missing.length > 0) {
            const { tier, name } = formatName(baseCode);
            const row = document.createElement("tr");
            row.setAttribute("data-tier", tier);
            row.setAttribute("data-enchant", "0");
            row.setAttribute("data-name", name.toLowerCase());
            row.append(
                createCell(name, "", "Potion"),
                createCell(tier, "", "Tier"),
                createCell("+0", "", "Enchantment"),
                createCell("N/A", "", "Production Cost"),
                createCell("N/A", "", "Sale Price"),
                createCell("Data Insufficient", "text-muted", "Profit")
            );
            tbody.appendChild(row);
            return;
        }

        for (let enchant = 0; enchant <= 3; enchant++) {
            const enchantCode = baseCode.replace(/_\d$/, `_${enchant}`);
            const { tier, name } = formatName(enchantCode);
            const row = document.createElement("tr");

            row.setAttribute("data-tier", tier);
            row.setAttribute("data-enchant", enchant.toString());
            row.setAttribute("data-name", name.toLowerCase());

            // Lookup extract count from base recipe (_0)
            const baseKey = `${tier}_${name.toUpperCase()}_0`;
            const extractCount = recipes[baseKey]?.extracts || 0;

            // Enchant cost per extract
            const extractCostMultiplier = [0, 1, 3, 9][enchant];
            const enchantCost = extractCount * extractCostMultiplier * animalRemainsPrice;

            // Total per-potion cost
            const totalCost = Math.round((baseTotal + enchantCost) / yieldQty);
            const salePrice = getSalePrice(enchantCode);
            const profit = salePrice !== null ? salePrice - totalCost : null;

            row.appendChild(createCell(name, "", "Potion"));
            row.appendChild(createCell(tier, "", "Tier"));
            row.appendChild(createCell("+" + enchant, "", "Enchantment"));
            row.appendChild(createCell(totalCost, "", "Production Cost"));

            if (salePrice !== null) {
                row.appendChild(createCell(salePrice, "", "Sale Price"));
                const profitCell = createCell(Math.round(profit));
                profitCell.className =
                    profit > 0 ? "text-success" :
                        profit < 0 ? "text-danger" :
                            "text-secondary";
                profitCell.setAttribute("data-label", "Profit");
                row.appendChild(profitCell);
            } else {
                row.appendChild(createCell("N/A", "", "Sale Price"));
                row.appendChild(createCell("N/A", "text-muted", "Profit"));
            }

            tbody.appendChild(row);
        }

    });

    filterProfitRows(); // Apply filters on load
};

function filterProfitRows() {
    const tier = document.getElementById("profit-tier-select").value;
    const enchant = document.getElementById("profit-enchant-select").value;
    const name = document.getElementById("profit-name-select").value;

    document.querySelectorAll("#profit-table-body-js tr").forEach(row => {
        const rowTier = row.getAttribute("data-tier");
        const rowEnchant = row.getAttribute("data-enchant");
        const rowName = row.getAttribute("data-name");

        const matchTier = tier === "all" || rowTier === tier;
        const matchEnchant = enchant === "all" || rowEnchant === enchant;
        const matchName = name === "all" || rowName === name;

        row.style.display = (matchTier && matchEnchant && matchName) ? "" : "none";
    });
}

["profit-tier-select", "profit-enchant-select", "profit-name-select"].forEach(id => {
    document.getElementById(id).addEventListener("change", filterProfitRows);
});
