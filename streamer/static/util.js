function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.getElementById(tabId).classList.add('active');
}

function submitTVShow() {
    const id = document.getElementById('tvId').value;
    const season = document.getElementById('season').value;
    const link = `https://vidsrc.to/embed/tv/${id}/${season}`;
    updateVideo(link);
}

function submitMovie() {
    const id = document.getElementById('movieId').value;
    const link = `https://vidsrc.to/embed/movie/${id}`;
    updateVideo(link);
}
function checkEnter(event, searchId) {
    if (event.key === 'Enter') {
        event.preventDefault();
        const query = document.getElementById(searchId).value;
        if (query) {
            search(query, searchId);
        }
    }
}

function search(query, searchId) {
    console.log("searching");
    const xhr = new XMLHttpRequest();
    xhr.open('GET', `search/?q=${query}&type=${searchId}`, true);
    console.log(xhr.responseText);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            const results = JSON.parse(xhr.responseText).results;
            displayResults(results);
        }
    };
    xhr.send();
}

function displayResults(results) {
    let link;
    console.log("dr");
    const resultsContainer = document.getElementById('searchResults');
    resultsContainer.innerHTML = ''; // Clear previous results
    results.forEach(result => {
        const resultElement = document.createElement('div');
        resultElement.className = 'result';
        if(result.media_type === "movie"){
            link = `https://vidsrc.to/embed/movie/${result.id}`;
        }
        else{
            link = `https://vidsrc.to/embed/tv/${result.id}/${document.getElementById('season').value}`;
        }
        resultElement.innerHTML = `
            <a href="#" onclick="updateVideo('${link}')">
                <img src="${result.poster}" alt="${result.title} poster">
                <h3>${result.title} (${result.year})</h3>
            </a>
        `;
        resultsContainer.appendChild(resultElement);
    });
    const closeButton = document.createElement('button');
    closeButton.textContent = 'Close';
    closeButton.onclick = closeSearchResults;
    resultsContainer.appendChild(closeButton);
    document.getElementById('searchResultsWidget').style.display = 'block';
}

function closeSearchResults() {
    document.getElementById('searchResultsWidget').style.display = 'none';
}

function updateVideo(link) {
    document.getElementById('videoPlayer').src = link;
    document.getElementById('searchResultsWidget').style.display = 'none';
}
function handleClickOutside(event) {
    const widget = document.getElementById('searchResultsWidget');
    if (!widget.contains(event.target)) {
        widget.style.display = 'none';
    }
    console.log(event.target);
}
function loadAccountPage()
{

}
function startMedia(event){

    const csrftoken = '{{ csrf_token }}';
    let player = document.getElementById("videoPlayer");
    const url = player.src;
    const parts = url.split('/');
    let id, season;
    let params = {}
    if(player.src.includes("movie")){
         id = parts.pop();

    } else if(player.src.includes("tv")){
         season = parts.pop();
         id = parts.pop();
         params.season = season;
    }
    params.id = id;
    console.log(id);
    const resp = fetch('/watch_movie/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken  // Include CSRF token in the header
        },
        body: new URLSearchParams(params)
    });
    if(!resp.ok) {
        console.error(`Response status ${resp.status} in  startMedia POST request`)
    }
}


document.addEventListener('click', handleClickOutside);
