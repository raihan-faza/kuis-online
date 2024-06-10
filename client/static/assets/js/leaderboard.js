// kuis-online/client/static/js/leaderboard.js

document.addEventListener("DOMContentLoaded", function() {
    const leaderboardContainer = document.getElementById("leaderboard-container");
    const quizId = leaderboardContainer.getAttribute("data-quiz-id");

    fetchLeaderboardData(quizId);

    function fetchLeaderboardData(quizId) {
        fetch(`/api/leaderboard/${quizId}/`)
            .then(response => response.json())
            .then(data => {
                updateLeaderboardTable(data);
            })
            .catch(error => console.error('Error fetching leaderboard data:', error));
    }

    function updateLeaderboardTable(data) {
        const tbody = document.querySelector("#leaderboard-table tbody");
        tbody.innerHTML = "";

        data.forEach((entry, index) => {
            const row = document.createElement("tr");

            const rankCell = document.createElement("td");
            rankCell.textContent = index + 1;
            row.appendChild(rankCell);

            const nameCell = document.createElement("td");
            nameCell.textContent = entry.user_id;  // Adjust to use user's name if available
            row.appendChild(nameCell);

            const gradeCell = document.createElement("td");
            gradeCell.textContent = entry.grade;
            row.appendChild(gradeCell);

            const timestampCell = document.createElement("td");
            timestampCell.textContent = entry.timestamp;
            row.appendChild(timestampCell);

            tbody.appendChild(row);
        });
    }
});
