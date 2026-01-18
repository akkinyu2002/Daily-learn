import requests
import urllib.parse
import webbrowser

def get_mood_songs():
    """Returns a dictionary of moods and their corresponding song lists (fallback)."""
    return {
        'happy': [
            {"name": "Pharrell Williams - Happy", "url": "https://www.youtube.com/results?search_query=Pharrell+Williams+Happy"},
            {"name": "Justin Timberlake - Can't Stop the Feeling!", "url": "https://www.youtube.com/results?search_query=Justin+Timberlake+Can%27t+Stop+the+Feeling!"},
            {"name": "Katrina and the Waves - Walking on Sunshine", "url": "https://www.youtube.com/results?search_query=Katrina+and+the+Waves+Walking+on+Sunshine"},
            {"name": "Mark Ronson ft. Bruno Mars - Uptown Funk", "url": "https://www.youtube.com/results?search_query=Mark+Ronson+ft.+Bruno+Mars+Uptown+Funk"}
        ],
        'sad': [
            {"name": "Adele - Someone Like You", "url": "https://www.youtube.com/results?search_query=Adele+Someone+Like+You"},
            {"name": "Coldplay - Fix You", "url": "https://www.youtube.com/results?search_query=Coldplay+Fix+You"},
            {"name": "Sam Smith - Stay With Me", "url": "https://www.youtube.com/results?search_query=Sam+Smith+Stay+With+Me"},
            {"name": "Billie Eilish - when the party's over", "url": "https://www.youtube.com/results?search_query=Billie+Eilish+when+the+party%27s+over"}
        ],
        'focused': [
            {"name": "Lofi Girl - Study Beats", "url": "https://www.youtube.com/live/jfKfPfyJRdk"},
            {"name": "Hans Zimmer - Time", "url": "https://www.youtube.com/results?search_query=Hans+Zimmer+Time"},
            {"name": "Ludovico Einaudi - Nuvole Bianche", "url": "https://www.youtube.com/results?search_query=Ludovico+Einaudi+Nuvole+Bianche"},
            {"name": "Tycho - Awake", "url": "https://www.youtube.com/results?search_query=Tycho+Awake"}
        ],
        'energetic': [
            {"name": "Survivor - Eye of the Tiger", "url": "https://www.youtube.com/results?search_query=Survivor+Eye+of+the+Tiger"},
            {"name": "Eminem - Lose Yourself", "url": "https://www.youtube.com/results?search_query=Eminem+Lose+Yourself"},
            {"name": "Queen - Don't Stop Me Now", "url": "https://www.youtube.com/results?search_query=Queen+Don%27t+Stop+Me+Now"},
            {"name": "The Weeknd - Blinding Lights", "url": "https://www.youtube.com/results?search_query=The+Weeknd+Blinding+Lights"}
        ]
    }

def get_itunes_recommendations(mood):
    """Fetches song recommendations from iTunes Search API based on mood."""
    mood_terms = {
        'happy': 'happy music',
        'sad': 'sad songs',
        'focused': 'study music',
        'energetic': 'workout music'
    }

    if mood not in mood_terms:
        return None

    term = mood_terms[mood]
    encoded_term = urllib.parse.quote(term)
    url = f"https://itunes.apple.com/search?term={encoded_term}&media=music&entity=song&limit=5"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        tracks = []
        if 'results' in data:
            for result in data['results']:
                track_name = result.get('trackName', 'Unknown Track')
                artist_name = result.get('artistName', 'Unknown Artist')
                preview_url = result.get('previewUrl') or result.get('trackViewUrl')
                tracks.append({"name": f"{artist_name} - {track_name}", "url": preview_url})
        
        return tracks if tracks else None
    except Exception as e:
        print(f"Error fetching from iTunes: {e}")
        return None

def recommend_songs(mood):
    """Prints song recommendations based on the given mood and offers playback."""
    mood = mood.lower().strip()
    
    # Try iTunes first
    print(f"Searching online for '{mood}' songs...")
    songs = get_itunes_recommendations(mood)
    source = "iTunes"
    
    if not songs:
        # Fallback to local list
        mood_songs = get_mood_songs()
        if mood in mood_songs:
            songs = mood_songs[mood]
            source = "Offline Fallback"
        else:
            print(f"\nSorry, I don't have a playlist for '{mood}'.")
            print("Try one of these: happy, sad, focused, energetic")
            return

    print(f"\nHere are some recommendations for your '{mood}' mood ({source}):")
    for i, song in enumerate(songs, 1):
        print(f"{i}. {song['name']}")

    choice = input("\nEnter a number to play a song (or press Enter to skip): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(songs):
        song_url = songs[int(choice)-1]['url']
        if song_url:
            print(f"Opening: {songs[int(choice)-1]['name']}...")
            webbrowser.open(song_url)
        else:
            print("Sorry, no playback link available for this song.")

def main():
    print("Welcome to the Mood-Based Music Recommender!")
    print("Available moods: happy, sad, focused, energetic")
    
    while True:
        user_input = input("\nHow are you feeling today? (or type 'exit' to quit): ")
        
        if user_input.lower() == 'exit':
            print("Goodbye! Hope your mood improves!")
            break
            
        recommend_songs(user_input)

if __name__ == "__main__":
    main()
