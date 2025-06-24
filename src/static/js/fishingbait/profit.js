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

        function setProfitDisplay(element, value, cost) {
            if (!isNaN(value)) {
                const profit = value - cost;
                element.textContent = profit;

                element.classList.remove("text-success", "text-danger");

                if (profit > 0) {
                    element.classList.add("text-success");
                } else if (profit < 0) {
                    element.classList.add("text-danger");
                }

                hasAny = true;
            } else {
                element.textContent = "No data";
                element.classList.remove("text-success", "text-danger");
            }
        }

        if (t1Input.value.trim() !== "") {
            const t1 = parseInt(t1Input.value);
            setProfitDisplay(profitT1, t1, worm * 1);
        } else {
            profitT1.textContent = "No data";
            profitT1.classList.remove("text-success", "text-danger");
        }

        if (t3Input.value.trim() !== "") {
            const t3 = parseInt(t3Input.value);
            setProfitDisplay(profitT3, t3, worm * 5);
        } else {
            profitT3.textContent = "No data";
            profitT3.classList.remove("text-success", "text-danger");
        }

        if (t5Input.value.trim() !== "") {
            const t5 = parseInt(t5Input.value);
            setProfitDisplay(profitT5, t5, worm * 25);
        } else {
            profitT5.textContent = "No data";
            profitT5.classList.remove("text-success", "text-danger");
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
