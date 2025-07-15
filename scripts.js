const chatbox = document.getElementById('chatbox');
const userMessageInput = document.getElementById('userMessage');

// Send Message Function
function sendMessage() {
    const userMessage = userMessageInput.value;
    if (userMessage.trim()) {
        chatbox.innerHTML += `<div class="user-message">${userMessage}</div>`;
        userMessageInput.value = "";
        
        // Detect emotion from text
        detectEmotion(userMessage);
    }
}

// Detect Emotion Function using Flask API
async function detectEmotion(text) {
    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();
        const emotion = data.emotion;

        // Bot responds based on detected emotion
        let botResponse = `You seem ${emotion}! Here's some music for your mood.`;
        chatbox.innerHTML += `<div class="bot-message">${botResponse}</div>`;

        // Fetch music recommendations
        getMusicRecommendations(emotion);
    } catch (error) {
        console.error('Error detecting emotion:', error);
    }
}

// Fetch Music Recommendations Based on Detected Emotion and Language
async function getMusicRecommendations(emotion) {
    let language = "English"; // Default language is English

    if (emotion === 'sad') {
        language = 'Hindi'; // Example: Choose Hindi for sadness
    } else if (emotion === 'joy') {
        language = 'Telugu'; // Example: Choose Telugu for happiness
    }

    const youtubeLink = await getYouTubeSong(emotion, language);
    const spotifyLink = await getSpotifySong(emotion);

    chatbox.innerHTML += `
        <div class="bot-message">
            Check out this song on YouTube: <a href="${youtubeLink}" target="_blank">YouTube Song</a>
        </div>
        <div class="bot-message">
            Or listen to it on Spotify: <a href="${spotifyLink}" target="_blank">Spotify Song</a>
        </div>
    `;
    chatbox.scrollTop = chatbox.scrollHeight; // Auto scroll to the bottom
}

// Fetch Music from YouTube API
async function getYouTubeSong(emotion, language) {
    let query = `${emotion} song ${language}`;
    const youtubeApiKey = 'YOUR_YOUTUBE_API_KEY'; // Replace with your YouTube API Key

    try {
        const response = await fetch(`https://www.googleapis.com/youtube/v3/search?part=snippet&q=${encodeURIComponent(query)}&type=video&key=${youtubeApiKey}&maxResults=5`);
        const data = await response.json();

        const videoId = data.items[0]?.id?.videoId;
        if (videoId) {
            return `https://www.youtube.com/watch?v=${videoId}`;
        } else {
            return '#'; // If no video found
        }
    } catch (error) {
        console.error('YouTube API Error:', error);
        return '#';
    }
}

// Fetch Music from Spotify API
async function getSpotifySong(emotion) {
    const CLIENT_ID = 'YOUR_SPOTIFY_CLIENT_ID'; // Replace with your Spotify Client ID
    const CLIENT_SECRET = 'YOUR_SPOTIFY_CLIENT_SECRET'; // Replace with your Spotify Client Secret

    const accessToken = await getSpotifyAccessToken(CLIENT_ID, CLIENT_SECRET);
    const query = `${emotion} song`;

    const response = await fetch(`https://api.spotify.com/v1/search?q=${encodeURIComponent(query)}&type=track&limit=1`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${accessToken}`,
        }
    });

    const data = await response.json();
    if (data.tracks && data.tracks.items.length > 0) {
        const track = data.tracks.items[0];
        return track.external_urls.spotify;
    } else {
        return 'https://open.spotify.com/';
    }
}

// Get Spotify Access Token
async function getSpotifyAccessToken(clientId, clientSecret) {
    const auth = 'Basic ' + btoa(clientId + ':' + clientSecret);
    const response = await fetch('https://accounts.spotify.com/api/token', {
        method: 'POST',
        headers: {
            'Authorization': auth,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            grant_type: 'client_credentials',
        }),
    });

    const data = await response.json();
    return data.access_token;
}
