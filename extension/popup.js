document.getElementById('analyze-btn').addEventListener('click', async () => {
  const statusDiv = document.getElementById('status');
  const resultsDiv = document.getElementById('results');
  
  statusDiv.innerText = "Extracting comments from page...";
  resultsDiv.style.display = "none";

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  if (!tab.url.includes("youtube.com/watch")) {
    statusDiv.innerText = "⚠️ Please open a YouTube video page!";
    return;
  }

  // Inject content script to scrape comments from DOM
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: scrapeYouTubeComments
  }, async (injectionResults) => {
    const comments = injectionResults[0]?.result || [];
    
    if (comments.length === 0) {
      statusDiv.innerText = "⚠️ No comments found. Scroll down on the video page to load comments, then try again!";
      return;
    }

    statusDiv.innerText = `Analyzing ${comments.length} comments via API...`;

    try {
      const response = await fetch('http://127.0.0.1:8000/predict_batch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comments: comments })
      });

      const data = await response.json();

      document.getElementById('total-count').innerText = data.total_comments;
      document.getElementById('pos-count').innerText = data.summary.Positive || 0;
      document.getElementById('neu-count').innerText = data.summary.Neutral || 0;
      document.getElementById('neg-count').innerText = data.summary.Negative || 0;

      statusDiv.innerText = "✅ Analysis complete!";
      resultsDiv.style.display = "block";
    } catch (err) {
      statusDiv.innerText = "❌ Error connecting to backend API. Is uvicorn running?";
      console.error(err);
    }
  });
});

// Function executed directly inside the YouTube web page
function scrapeYouTubeComments() {
  const commentElements = document.querySelectorAll('#content-text');
  const comments = [];
  commentElements.forEach((el, index) => {
    if (index < 50 && el.innerText.trim()) { // Limit to 50 comments for speed
      comments.push(el.innerText.trim());
    }
  });
  return comments;
}