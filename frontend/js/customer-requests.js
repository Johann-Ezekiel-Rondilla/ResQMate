const API_URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", async () => {
    const storedUser = localStorage.getItem("user");

    if (!storedUser) {
        alert("You are not logged in. Please log in first.");
        window.location.href = "../index.html";
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

    const tbody = document.querySelector(".requests-table tbody");

    if (!tbody) {
        return;
    }

    tbody.innerHTML = `
        <tr>
            <td colspan="5" style="text-align: center; color: #718096; padding: 20px;">
                Loading your requests...
            </td>
        </tr>
    `;

    try {
        const response = await fetch(
            `${API_URL}/requests/user/${user.user_id}`
        );

        if (!response.ok) {
            throw new Error("Failed to fetch requests.");
        }

        const requests = await response.json();

        tbody.innerHTML = "";

        if (requests.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="5" style="text-align: center; color: #718096; padding: 20px;">
                        No assistance requests found.
                    </td>
                </tr>
            `;
            return;
        }

        requests.forEach(req => {
            const row = document.createElement("tr");

            const typeText = req.category_name || "General";

            const status = req.status
                ? req.status.toLowerCase()
                : "pending";

            const statusFormatted = req.status
                ? req.status.charAt(0).toUpperCase() + req.status.slice(1)
                : "Pending";

            const dateFormatted = req.date_requested
                ? new Date(req.date_requested).toLocaleDateString("en-US", {
                    month: "short",
                    day: "numeric",
                    year: "numeric"
                })
                : "";

            let actionHTML = "";

            if (status === "pending") {
                actionHTML = `
                    <button 
                        class="follow-up-button"
                        data-request-id="${req.request_id}">
                        Follow Up
                    </button>
                `;
            } else {
                actionHTML = `
                    <span class="no-action">—</span>
                `;
            }

            row.innerHTML = `
                <td class="req-id">
                    ${req.request_id}
                </td>

                <td>
                    ${typeText}
                </td>

                <td>
                    <span class="status-badge ${status}">
                        ${statusFormatted}
                    </span>
                </td>

                <td>
                    ${dateFormatted}
                </td>

                <td>
                    ${actionHTML}
                </td>
            `;

            tbody.appendChild(row);
        });

        document.querySelectorAll(".follow-up-button").forEach(button => {
            button.addEventListener("click", () => {
                const requestId = button.dataset.requestId;

                alert(
                    `Follow-up request sent for Request #${requestId}.`
                );
            });
        });

    } catch (error) {
        console.error("Error fetching user requests:", error);

        tbody.innerHTML = `
            <tr>
                <td colspan="5" style="text-align: center; color: #ef4444; padding: 20px;">
                    Error loading requests. Please try again later.
                </td>
            </tr>
        `;
    }
});

