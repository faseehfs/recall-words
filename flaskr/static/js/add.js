document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("wordForm");
    const successMessage = document.getElementById("successMessage");

    form.addEventListener("submit", (event) => {
        event.preventDefault();

        const word = document.getElementById("word").value.trim();
        const comments = document.getElementById("comments").value.trim();

        if (!word) return;

        successMessage.style.display = "block";
        form.reset();
        setTimeout(() => {
            successMessage.style.display = "none";
        }, 3000);
    });
});
