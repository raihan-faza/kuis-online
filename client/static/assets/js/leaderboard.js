document.addEventListener("DOMContentLoaded", function() {
    // Fetch the quiz ID from local storage
    const quizId = localStorage.getItem('quiz_id');

    if (quizId) {
        fetch(`/leaderboard/${quizId}`)
            .then(response => response.json())
            .then(data => {
                const tableBody = document.querySelector("#leaderboard-table tbody");
                tableBody.innerHTML = ""; // Clear existing rows
                data.forEach((entry, index) => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td class="rank">${index + 1}</td>
                        <td class="name">${entry.name}</td>
                        <td class="points">${entry.grade} Points</td>
                        <td class="timestamp">${entry.timestamp}</td>
                    `;
                    tableBody.appendChild(row);
                });
            });
    } else {
        // Handle case where quiz ID is not found
        const tableBody = document.querySelector("#leaderboard-table tbody");
        tableBody.innerHTML = "<tr><td colspan='4'>No quiz ID found. Please attempt a quiz first.</td></tr>";
    }
});
