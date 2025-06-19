document.addEventListener("DOMContentLoaded", function () {
    const saveBtn = document.getElementById("save-data-btn");

    if (!saveBtn) return;

    saveBtn.addEventListener("click", async function () {
        const formData = new FormData();
        document.querySelectorAll(".ingredient-input, .sale-price-input").forEach(input => {
            if (input.name) {
                formData.append(input.name, input.value);
            }
        });

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        if (csrfToken) {
            formData.append("csrfmiddlewaretoken", csrfToken);
        }

        const url = saveBtn.dataset.url;
        if (!url) {
            console.error("Save URL not defined.");
            return;
        }

        // Save original button content and disable it
        const originalText = saveBtn.innerHTML;
        saveBtn.disabled = true;
        saveBtn.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            Saving...
        `;

        try {
            const response = await fetch(url, {
                method: "POST",
                body: formData
            });

            if (response.redirected) {
                const toastEl = document.getElementById("saveToast");
                if (toastEl) {
                    const toast = new bootstrap.Toast(toastEl, {
                        delay: 5000,
                        autohide: true
                    });
                    toast.show();
                }
            } else {
                console.warn("Save did not redirect.");
            }
        } catch (err) {
            console.error("Error while saving data:", err);
        } finally {
            // Restore the button
            saveBtn.disabled = false;
            saveBtn.innerHTML = originalText;
        }
    });
});
