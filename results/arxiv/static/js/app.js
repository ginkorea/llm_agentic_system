document.getElementById('query-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const category = document.getElementById('category').value;
    const title = document.getElementById('title').value;
    const author = document.getElementById('author').value;
    const abstract = document.getElementById('abstract').value;
    const recentDays = document.getElementById('recent_days').value;

    // Perform query logic here and update the results div
    document.getElementById('results').innerHTML = 'Query results will be displayed here.';
});