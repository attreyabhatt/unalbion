document.addEventListener("DOMContentLoaded", function () {
    const tierSelect = document.getElementById("tier-select");
    const enchantSelect = document.getElementById("enchant-select");
    const nameSelect = document.getElementById("potion-name-select");
    const rows = document.querySelectorAll("#sale-price-table tbody tr");

    function filterRows() {
        const selectedTier = tierSelect.value;
        const selectedEnchant = enchantSelect.value;
        const selectedName = nameSelect.value;

        rows.forEach(row => {
            const rowTier = row.dataset.tier;
            const rowEnchant = row.dataset.enchant;
            const rowName = row.dataset.name;

            const matchesTier = selectedTier === "all" || selectedTier === rowTier;
            const matchesEnchant = selectedEnchant === "all" || selectedEnchant === rowEnchant;
            const matchesName = selectedName === "all" || rowName === selectedName;

            row.style.display = matchesTier && matchesEnchant && matchesName ? "" : "none";
        });
    }

    tierSelect.addEventListener("change", filterRows);
    enchantSelect.addEventListener("change", filterRows);
    nameSelect.addEventListener("change", filterRows);

    // Trigger filtering on page load
    filterRows();
});
