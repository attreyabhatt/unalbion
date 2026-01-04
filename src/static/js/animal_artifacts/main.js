document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("animal_artifacts_form");
    const profitTableBody = document.querySelector("#profit-table tbody");

    if (!form || !profitTableBody) return;

    const inputs = form.querySelectorAll("input[type='number']");

    // Helper to add profit rows
    function addProfitRow(tbody, breakdown, revenue, cost, profit, isFirstRow = false, name = "") {
        const row = document.createElement("tr");
        row.setAttribute("data-profit", profit);

        let icon = "";
        let badgeClass = "bg-secondary";
        let rowClass = "";

        if (profit > 0) {
            icon = `<i class="bi bi-arrow-up-circle-fill text-success me-1"></i>`;
            badgeClass = "bg-success";
            rowClass = "table-success";
        } else if (profit < 0) {
            icon = `<i class="bi bi-arrow-down-circle-fill text-danger me-1"></i>`;
            badgeClass = "bg-danger";
            rowClass = "table-danger";
        } else {
            icon = `<i class="bi bi-dash-circle-fill text-muted me-1"></i>`;
            badgeClass = "bg-secondary";
        }

        row.className = `${rowClass}`;

        row.innerHTML = `
            <td>${isFirstRow ? `<strong>${name}</strong>` : ""}</td>
            <td class="text-center">${breakdown}</td>
            <td class="text-center">${revenue.toFixed(2)}</td>
            <td class="text-center">${cost.toFixed(2)}</td>
            <td class="text-center">
                <span class="badge ${badgeClass} px-3 py-2 fs-6">
                    ${icon} ${profit >= 0 ? "+" : ""}${profit.toFixed(2)}
                </span>
            </td>
        `;

        tbody.appendChild(row);
    }

    function calculateProfits() {
        const data = {};

        inputs.forEach((input) => {
            const name = input.dataset.name?.trim();
            const tierString = input.dataset.tier?.trim();
            const value = parseInt(input.value);

            if (!name || !tierString || isNaN(value)) return;

            let tier = null;
            if (tierString === "RUGGED") tier = 3;
            else if (tierString === "FINE") tier = 5;
            else if (tierString === "EXCELLENT") tier = 7;

            if (!tier) return;

            if (!data[name]) data[name] = {};
            data[name][`t${tier}`] = value;
        });

        profitTableBody.innerHTML = "";

        for (let name in data) {
            const { t3, t5, t7 } = data[name];
            let isFirstRow = true;

            const spacer = document.createElement("tr");
            spacer.innerHTML = `<td colspan="3" class="table-light"></td>`;
            profitTableBody.appendChild(spacer);

            if (t3 !== undefined && t5 !== undefined) {
                const revenue53 = t3 * 2;
                const cost53 = t5;
                const profit53 = revenue53 - cost53;
                addProfitRow(profitTableBody, "T5 -> 2x T3", revenue53, cost53, profit53, isFirstRow, name);
                isFirstRow = false;
            }

            if (t5 !== undefined && t7 !== undefined) {
                const revenue75 = t5 * 2;
                const cost75 = t7;
                const profit75 = revenue75 - cost75;
                addProfitRow(profitTableBody, "T7 -> 2x T5", revenue75, cost75, profit75, isFirstRow, name);
                isFirstRow = false;
            }

            if (t3 !== undefined && t7 !== undefined) {
                const revenue73 = t3 * 4;
                const cost73 = t7;
                const profit73 = revenue73 - cost73;
                addProfitRow(profitTableBody, "T7 -> 4x T3", revenue73, cost73, profit73, isFirstRow, name);
            }
        }
    }

    // Bootstrap icon link (if not already added)
    if (!document.querySelector("link[href*='bootstrap-icons']")) {
        const iconLink = document.createElement("link");
        iconLink.rel = "stylesheet";
        iconLink.href = "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css";
        document.head.appendChild(iconLink);
    }

    // Events
    calculateProfits();
    inputs.forEach((input) => input.addEventListener("input", calculateProfits));
});
