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
function checkEnter(event) {
    const query = document.getElementById("searchBar").value;
    const link = document.getElementById("searchLink");
    link.href = `/search/${query}`;
    // if (event.key === 'Enter') {
    //     event.preventDefault();
    //     if (query) {
    //         search(query);
    //     }
    // }
}

function search(query, searchId) {
    console.log("searching");
    const xhr = new XMLHttpRequest();
    xhr.open('GET', `../search/?q=${query}&type=${searchId}`, true);
    
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
    const closeButton = document.createElement('button');
    closeButton.textContent = 'Close';
    closeButton.onclick = closeSearchResults;
    resultsContainer.appendChild(closeButton);
    results.forEach(result => {
        const resultElement = document.createElement('div');
        resultElement.className = 'result';
        if(result.media_type === "movie"){
            link = `/movie/${result.id}`;
        }
        else{
            link = `/tv/${result.id}`;
        }
        resultElement.innerHTML = `
            <a href="${link}">
                <img src="${result.poster}" alt="${result.title} poster">
                <h3>${result.title} (${result.year})</h3>
            </a>
        `;
        resultsContainer.appendChild(resultElement);
    });

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
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function addToList(event){
    let player = document.getElementById("videoPlayer");
    const url = player.src;
    const parts = url.split('/');
    let id, season;
    let params = {}
    if(player.src.includes("movie")){
         id = parts.pop();
            params.media_type = "movie";

    } else if(player.src.includes("tv")){
        console.log("tv");
         season = parts.pop();
         id = parts.pop();
         params.season = season;
         params.media_type = "tv";
    }
    params.id = id;
    console.log(id);
    const resp = fetch('add_to_list', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie("csrftoken") // Include CSRF token in the header
        },
        body: new URLSearchParams(params)
    });
    if(!resp.ok) {
        console.error(`Response status ${resp.status} in  addToList POST request`)
    }
}

function playFromList(event, media_type, id, season){
    let link;
    if(media_type === "movie"){
        link = `https://vidsrc.to/embed/movie/${id}`;
    }
    else{
        link = `https://vidsrc.to/embed/tv/${id}/${season}`;
    }
    const resp = fetch('/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie("csrftoken") // Include CSRF token in the header
        },
        body: new URLSearchParams({id: id, media_type: media_type, season: season})
    });
    updateVideo(link);
}


