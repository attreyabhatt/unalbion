document.addEventListener("DOMContentLoaded", function () {
    const wormInput = document.getElementById("worm_price");
    const t1Input = document.getElementById("t1_price");
    const t3Input = document.getElementById("t3_price");
    const t5Input = document.getElementById("t5_price");

    const outputSection = document.getElementById("profit-output");
    const profitT1 = document.getElementById("profit_t1");
    const profitT3 = document.getElementById("profit_t3");
    const profitT5 = document.getElementById("profit_t5");

    function updateProfits() {
        const worm = parseInt(wormInput.value);

        if (isNaN(worm)) {
            outputSection.style.display = "none";
            return;
        }

        let hasAny = false;

        if (t1Input.value.trim() !== "") {
            const t1 = parseInt(t1Input.value);
            if (!isNaN(t1)) {
                const profit = t1 - (worm * 1);
                profitT1.textContent = profit;
                hasAny = true;
            } else {
                profitT1.textContent = "No data";
            }
        } else {
            profitT1.textContent = "No data";
        }

        if (t3Input.value.trim() !== "") {
            const t3 = parseInt(t3Input.value);
            if (!isNaN(t3)) {
                const profit = t3 - (worm * 3);
                profitT3.textContent = profit;
                hasAny = true;
            } else {
                profitT3.textContent = "No data";
            }
        } else {
            profitT3.textContent = "No data";
        }

        if (t5Input.value.trim() !== "") {
            const t5 = parseInt(t5Input.value);
            if (!isNaN(t5)) {
                const profit = t5 - (worm * 5);
                profitT5.textContent = profit;
                hasAny = true;
            } else {
                profitT5.textContent = "No data";
            }
        } else {
            profitT5.textContent = "No data";
        }

        outputSection.style.display = hasAny ? "block" : "none";
    }

    // Listen for input changes
    [wormInput, t1Input, t3Input, t5Input].forEach(input => {
        input.addEventListener("input", updateProfits);
    });

    // Trigger on load in case fields are pre-filled
    updateProfits();
});
