const API_URL = "http://127.0.0.1:8000";

const requestForm = document.getElementById("requestForm");
const assistanceTypeInput = document.getElementById("assistanceType");
const locationInput = document.getElementById("location");
const detailsInput = document.getElementById("details");
const priorityInput = document.getElementById("priority");
const characterCount = document.getElementById("characterCount");
const cancelButton = document.getElementById("cancelButton");
const assistanceOptions = document.querySelectorAll(".assistance-option");

assistanceOptions.forEach(option => {
    option.addEventListener("click", function () {
        assistanceOptions.forEach(item => {
            item.classList.remove("active");
        });

        this.classList.add("active");
        assistanceTypeInput.value = this.getAttribute("data-type");
    });
});

if (detailsInput && characterCount) {
    detailsInput.addEventListener("input", function () {
        characterCount.textContent = this.value.length;
    });
}

if (cancelButton) {
    cancelButton.addEventListener("click", function () {
        requestForm.reset();

        assistanceTypeInput.value = "Food";

        assistanceOptions.forEach(option => {
            option.classList.remove("active");

            if (option.getAttribute("data-type") === "Food") {
                option.classList.add("active");
            }
        });

        if (characterCount) {
            characterCount.textContent = "0";
        }
    });
}

if (requestForm) {
    requestForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const storedUser = localStorage.getItem("user");

        if (!storedUser) {
            alert("You are not logged in. Please log in first.");
            return;
        }

        let user;

        try {
            user = JSON.parse(storedUser);
        } catch (error) {
            alert("Invalid user information. Please log in again.");
            return;
        }

        if (!user.user_id) {
            alert("User ID was not found. Please log in again.");
            return;
        }

        const assistanceType = assistanceTypeInput.value.trim();
        const location = locationInput.value.trim();
        const details = detailsInput.value.trim();
        const priority = priorityInput.value;

        if (!assistanceType || !location || !details || !priority) {
            alert("Please complete all required fields.");
            return;
        }

        const submitButton = requestForm.querySelector(".submit-button");

        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = "Submitting...";
        }

        try {
            const response = await fetch(`${API_URL}/requests/create`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    user_id: user.user_id,
                    assistance_type: assistanceType,
                    location: location,
                    request_details: details,
                    priority: priority
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.detail ||
                    data.message ||
                    "Failed to submit request."
                );
            }

            alert("Your assistance request has been submitted successfully.");

            requestForm.reset();

            assistanceTypeInput.value = "Food";

            assistanceOptions.forEach(option => {
                option.classList.remove("active");

                if (option.getAttribute("data-type") === "Food") {
                    option.classList.add("active");
                }
            });

            if (characterCount) {
                characterCount.textContent = "0";
            }

        } catch (error) {
            console.error(error);
            alert(`Failed to submit request.\n\n${error.message}`);
        } finally {
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = "Submit Request";
            }
        }
    });
}