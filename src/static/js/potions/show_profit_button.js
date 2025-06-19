document.addEventListener("DOMContentLoaded", function () {
    const showProfitBtn = document.getElementById("show-profit-btn");
    const backBtn = document.getElementById("back-to-inputs-btn");
    const inputsView = document.getElementById("v-potion-tabs-content");
    const profitView = document.getElementById("profit-view");

    if (showProfitBtn) {
        showProfitBtn.addEventListener("click", () => {
            inputsView.style.display = "none";
            profitView.style.display = "block";
            renderProfitTable();  // your existing table logic
        });
    }

    if (backBtn) {
        backBtn.addEventListener("click", () => {
            profitView.style.display = "none";
            inputsView.style.display = "block";
        });
    }
});
