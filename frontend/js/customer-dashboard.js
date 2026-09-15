document.addEventListener(
    "DOMContentLoaded",
    loadDashboard
);

async function loadDashboard() {

    const user =
        JSON.parse(
            localStorage.getItem("user")
        );

    if (!user) {

        window.location.href =
            "../landingpage.html";

        return;
    }

    try {

        const response =
            await fetch(
                `http://127.0.0.1:8000/requests/user/${user.user_id}`
            );

        if (!response.ok) {
            throw new Error("Failed to load requests.");
        }

        const requests =
            await response.json();

        loadStats(requests);

        loadRecentRequests(requests);

    }
    catch (error) {

        console.error(
            "Dashboard Error:",
            error
        );
    }
}

function loadStats(requests) {

    const pending =
        requests.filter(
            r =>
                r.status &&
                r.status.toLowerCase() ===
                "pending"
        ).length;

    const approved =
        requests.filter(
            r =>
                r.status &&
                r.status.toLowerCase() ===
                "approved"
        ).length;

    const completed =
        requests.filter(
            r =>
                r.status &&
                r.status.toLowerCase() ===
                "completed"
        ).length;

    document.getElementById(
        "pendingCount"
    ).textContent = pending;

    document.getElementById(
        "approvedCount"
    ).textContent = approved;

    document.getElementById(
        "completedCount"
    ).textContent = completed;
}

function loadRecentRequests(requests) {

    const tableBody =
        document.getElementById(
            "recentRequestsBody"
        );

    tableBody.innerHTML = "";

    requests
        .slice(0, 5)
        .forEach(request => {

            let type = "General";

            if (request.category_id == 1) {
                type = "Food";
            }
            else if (request.category_id == 2) {
                type = "Water";
            }
            else if (request.category_id == 3) {
                type = "Shelter";
            }
            else if (request.category_id == 4) {
                type = "Medicine";
            }
            else if (request.category_id == 5) {
                type = "General";
            }

            const status =
                request.status
                    ? request.status.toLowerCase()
                    : "pending";

            const statusText =
                request.status
                    ? request.status
                        .charAt(0)
                        .toUpperCase() +
                    request.status
                        .slice(1)
                    : "Pending";

            const date =
                request.date_requested
                    ? new Date(
                        request.date_requested
                    ).toLocaleDateString(
                        "en-US",
                        {
                            month: "short",
                            day: "numeric",
                            year: "numeric"
                        }
                    )
                    : "";

            tableBody.innerHTML += `
                <tr>
                    <td>${request.request_id}</td>

                    <td>
                        ${type}
                    </td>

                    <td>
                        <span class="status-badge ${status}">
                            ${statusText}
                        </span>
                    </td>

                    <td>
                        ${date}
                    </td>
                </tr>
            `;
        });
}