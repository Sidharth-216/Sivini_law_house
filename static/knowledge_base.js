document.getElementById('backButton').addEventListener('click', () => {
    window.location.href = '/lawyer_dashboard'; // Change to your dashboard route
});

// Sample data for articles
const articles = [
    { title: "What is Legal Aid?", content: "Legal aid is..."},
    { title: "How to File a Complaint", content: "To file a complaint..."},
    { title: "Understanding Court Procedures", content: "Court procedures involve..."},
    // Add more articles as needed
];

function displayArticles(articlesToDisplay) {
    const articlesList = document.getElementById('articlesList');
    articlesList.innerHTML = ''; // Clear existing articles

    articlesToDisplay.forEach(article => {
        const articleDiv = document.createElement('div');
        articleDiv.classList.add('article');
        articleDiv.innerHTML = `<h3>${article.title}</h3>`;
        articleDiv.onclick = () => alert(article.content); // Replace with a modal or detailed view if needed
        articlesList.appendChild(articleDiv);
    });
}

// Search functionality
document.getElementById('searchBar').addEventListener('input', (event) => {
    const searchTerm = event.target.value.toLowerCase();
    const filteredArticles = articles.filter(article => article.title.toLowerCase().includes(searchTerm));
    displayArticles(filteredArticles);
});

// Initial display of articles
displayArticles(articles);
