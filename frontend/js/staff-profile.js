document.addEventListener("DOMContentLoaded", () => {

const defaultUser = {
    user_id: "—",
    full_name: "Mark Santos",
    email: "staff@resqmate.com",
    role: "staff"
};

let user = defaultUser;

try {
    const storedUser = localStorage.getItem("user");

    if (storedUser) {
        const parsedUser = JSON.parse(storedUser);

        user = {
            ...defaultUser,
            ...parsedUser
        };
    }
} catch (error) {
    console.error("Unable to read stored user information:", error);
}

const profileName = document.getElementById("profileName");
const topbarName = document.getElementById("topbarName");
const fullName = document.getElementById("fullName");
const email = document.getElementById("email");
const userId = document.getElementById("userId");
const profileRole = document.getElementById("profileRole");
const accountRole = document.getElementById("accountRole");


if (profileName) {
    profileName.textContent = user.full_name;
}

if (topbarName) {
    topbarName.textContent = user.full_name;
}

if (fullName) {
    fullName.textContent = user.full_name;
}

if (email) {
    email.textContent = user.email;
}

if (userId) {
    userId.textContent = user.user_id;
}

if (profileRole) {
    profileRole.textContent = formatRole(user.role);
}

if (accountRole) {
    accountRole.textContent = formatRole(user.role);
}

});

function formatRole(role) {

if (!role) {
    return "Staff";
}

switch (role.toLowerCase()) {

    case "staff":
        return "Relief Staff";

    case "admin":
        return "Administrator";

    case "community_user":
    case "community":
        return "Community User";

    default:
        return role;
}

}