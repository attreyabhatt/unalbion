document.addEventListener("DOMContentLoaded", function () {
    const outputTable = document.getElementById("profit-table-body");

    fetch("/potions/profit-api/")
        .then((res) => res.json())
        .then((data) => {
            if (!Array.isArray(data)) return;

            outputTable.innerHTML = "";

            const getAnimalRemains = () => {
                const val = document.getElementById("animal_remains")?.value;
                return parseInt(val) || 0;
            };

            data.forEach((entry) => {
                const row = document.createElement("tr");

                const [tier, name, enchant] = entry.potion_code.split("_");
                const potionLabel = `${tier} ${name.toLowerCase()} (${enchant})`;

                if (entry.status === "data_insufficient") {
                    row.innerHTML = `
                        <td>${potionLabel}</td>
                        <td colspan="5" class="text-danger">Data insufficient: ${entry.missing.join(", ")}</td>
                    `;
                    outputTable.appendChild(row);
                    return;
                }

                const cost0 = entry.cost;
                const remains = getAnimalRemains();

                const costs = [
                    cost0,
                    cost0 + 45 * remains,
                    cost0 + 45 * 3 * remains,
                    cost0 + 45 * 9 * remains
                ];

                const salePriceInput = document.getElementById(`price_${entry.potion_code}`);
                const salePrice = parseInt(salePriceInput?.value || "0");

                row.innerHTML = `
                    <td>${tier} ${name.toLowerCase()}</td>
                    ${costs.map((c, i) => {
                        if (salePrice) {
                            const profit = salePrice - c;
                            return `<td>Cost: ${c}<br>Profit: ${profit}</td>`;
                        } else {
                            return `<td>Cost: ${c}<br><i class="text-muted">No sale price</i></td>`;
                        }
                    }).join("")}
                `;
                outputTable.appendChild(row);
            });
        });
});
