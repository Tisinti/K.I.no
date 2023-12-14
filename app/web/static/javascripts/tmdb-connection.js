const API_KEY = key;
const filmInput = document.getElementById('filmInput');
const suggestionsContainer = document.getElementById('suggestions');
const outputArea = document.getElementById('outputArea');

filmInput.addEventListener('click', function() {
    outputArea.style.display = 'none';
});

filmInput.addEventListener('input', async (event) => {
    const searchQuery = event.target.value;

    if (searchQuery.length > 2) {
        const suggestions = await fetchSuggestions(searchQuery);
        showSuggestions(suggestions);
    } else {
        hideSuggestions();
    }
});

async function fetchSuggestions(searchQuery) {
    const response = await fetch(`https://api.themoviedb.org/3/search/movie?api_key=${API_KEY}&query=${searchQuery}`);
    const data = await response.json();
    return data.results.slice(0, 5);
}

function showSuggestions(suggestions) {
    suggestionsContainer.innerHTML = '';
    const displayedSuggestions = suggestions.slice(0, 5);
    displayedSuggestions.forEach((suggestion) => {
        const listItem = document.createElement('li');
        listItem.textContent = suggestion.title;
        listItem.addEventListener('click', () => {
            filmInput.value = suggestion.title;
            const selectedValue = filmInput.value;
            console.log('Ausgewählter Film:', selectedValue); //Ausgabe Film Variable: selectedValue
            hideSuggestions();
        });
        suggestionsContainer.appendChild(listItem);
    });
    suggestionsContainer.style.display = 'block';
}

function hideSuggestions() {
    suggestionsContainer.style.display = 'none';
}

filmInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        const selectedValue = filmInput.value;
        console.log('Ausgewählter Film (Enter):', selectedValue); //Ausgabe Film Variable: selectedValue
    }
});