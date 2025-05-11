document.addEventListener("DOMContentLoaded", () => {
    const profilePicInput = document.getElementById("profile_picture");
    const currentProfilePic = document.querySelector(".current-profile-pic");

    profilePicInput.addEventListener("change", (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                currentProfilePic.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });
});
