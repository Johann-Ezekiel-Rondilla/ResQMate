function initLogoutModal() {

    document.addEventListener("click", function (e) {

        const modal = document.getElementById("logoutModal");

        // Open Modal
        if (e.target.closest(".logout button")) {
            e.preventDefault();

            if (modal) {
                modal.classList.add("show");
            }

            return;
        }

        // Close using X button
        if (e.target.closest("#closeModalBtn")) {
            modal.classList.remove("show");
            return;
        }

        // Close using Cancel button
        if (e.target.closest("#cancelLogoutBtn")) {
            modal.classList.remove("show");
            return;
        }

        // Close when clicking outside modal content
        if (e.target === modal) {
            modal.classList.remove("show");
        }
    });

}