// Fetch and display movies
document.addEventListener("DOMContentLoaded", () => {
    fetch('/api/movies')  // Replace with the actual API endpoint
        .then(response => response.json())
        .then(data => {
            const movieList = document.getElementById("movieList");
            data.forEach(movie => {
                const listItem = document.createElement("li");
                listItem.className = "movie-item";
                listItem.innerHTML = `<strong>${movie[1]}</strong> - ${movie[2]} (${movie[4]}/5)`;
                movieList.appendChild(listItem);
            });
        })
        .catch(error => console.error("Error fetching movies:", error));
});
