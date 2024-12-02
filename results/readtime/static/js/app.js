document.getElementById('contentForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const content = document.getElementById('content').value;
    const format = document.getElementById('format').value;
    const wpm = document.getElementById('wpm').value;

    // Simulate a reading time calculation
    const readingTime = calculateReadingTime(content, wpm);
    document.getElementById('result').innerText = `Estimated Reading Time: ${readingTime} minutes`;
});

function calculateReadingTime(content, wpm) {
    const words = content.trim().split(/\s+/).length;
    return Math.ceil(words / wpm);
}