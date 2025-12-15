const API_URL = "http://127.0.0.1:8000";

// -----------------------------
// LOAD ALL MOVIES
// -----------------------------
async function loadMovies() {
    const res = await fetch(`${API_URL}/movies/`);
    const movies = await res.json();
    renderMovies(movies);
}

// -----------------------------
// SEARCH MOVIES
// -----------------------------
async function searchMovies() {
    const query = document.getElementById("searchInput").value;
    const res = await fetch(`${API_URL}/movies/search?title=${query}`);
    const movies = await res.json();
    renderMovies(movies);
}

// -----------------------------
// RENDER MOVIES TO HTML
// -----------------------------
function renderMovies(movies) {
    const container = document.getElementById("moviesList");
    container.innerHTML = "";

    movies.forEach(movie => {
        const card = document.createElement("div");
        card.className = "movie-card";

        card.innerHTML = `
            <h3>${movie.title}</h3>
            <p><b>Genre:</b> ${movie.genre}</p>
            <p><b>Year:</b> ${movie.year}</p>
            <button onclick="openMovie(${movie.id})">Details</button>
        `;

        container.appendChild(card);
    });
}

function openMovie(id) {
    window.location.href = `movie.html?id=${id}`;
}

// Auto-load at page open
loadMovies();
