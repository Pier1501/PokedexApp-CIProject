import requests
from bs4 import BeautifulSoup
import urllib.parse

def get_youtube_link(song_title):
    query = urllib.parse.quote(song_title)
    url = f"https://www.youtube.com/results?search_query={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Look for video results
    video_results = soup.find_all('div', {'id': 'dismissible', 'class': 'ytd-video-renderer'})
    
    for result in video_results:
        # Get the title
        title_element = result.find('yt-formatted-string', {'id': 'video-title'})
        if not title_element:
            continue
        title = title_element.text.strip()
        
        # Get the channel name
        channel_element = result.find('yt-formatted-string', {'id': 'text', 'class': 'ytd-channel-name'})
        channel = channel_element.text.strip() if channel_element else "Unknown"
        
        # Get the video link
        link_element = result.find('a', {'id': 'video-title'})
        if link_element and 'href' in link_element.attrs:
            video_link = f"https://www.youtube.com{link_element['href']}"
            
            # Print debug information
            print(f"Found: {title} by {channel}")
            
            # You can add more conditions here to filter results
            if song_title.lower() in title.lower():
                return video_link
    
    return None

def get_musicbrainz_info(song_title):
    search_url = f"https://musicbrainz.org/ws/2/recording/?query={song_title}&fmt=json"
    response = requests.get(search_url)
    data = response.json()
    
    if data['recordings']:
        recording = data['recordings'][0]
        recording_id = recording['id']
        detail_url = f"https://musicbrainz.org/ws/2/recording/{recording_id}?inc=artists+releases&fmt=json"
        detail_response = requests.get(detail_url)
        detail_data = detail_response.json()

        info = {
            'name': detail_data['title'],
            'artist': detail_data['artist-credit'][0]['name'],
            'album': detail_data['releases'][0]['title'] if 'releases' in detail_data else 'Unknown',
            'release_date': detail_data['releases'][0]['date'] if 'releases' in detail_data else 'Unknown',
        }

        release_id = detail_data['releases'][0]['id'] if 'releases' in detail_data else None
        if release_id:
            cover_art_url = f"https://coverartarchive.org/release/{release_id}/front"
            cover_response = requests.get(cover_art_url)
            if cover_response.status_code == 200:
                info['cover_image'] = cover_art_url
            else:
                info['cover_image'] = None
        else:
            info['cover_image'] = None
        
        return info
    return None
def main():
    song_title = input("Enter the title of the song: ")
    
    youtube_link = get_youtube_link(song_title)
    musicbrainz_info = get_musicbrainz_info(song_title)
    
    if youtube_link:
        print(f"\nYouTube link: {youtube_link}")
    else:
        print("\nYouTube link not found.")
    
    if musicbrainz_info:
        print("\nSong Information:")
        for key, value in musicbrainz_info.items():
            print(f"{key.capitalize()}: {value}")
    else:
        print("\nSong information not found on MusicBrainz.")

if __name__ == "__main__":
    main()