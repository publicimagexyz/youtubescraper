import csv
import requests

# set API key and channel ID
api_key = 'YOUR_API_KEY'
channel_id = 'YOUR_CHANNEL_ID'

# set API endpoint and parameters for video search
search_endpoint = 'https://www.googleapis.com/youtube/v3/search'
search_params = {
    'part': 'snippet',
    'channelId': channel_id,
    'maxResults': 50, # adjust as needed
    'key': api_key
}

# send request to video search API
search_response = requests.get(search_endpoint, params=search_params)
search_data = search_response.json()

# open CSV file for writing
with open('videos.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    # write header row
    writer.writerow(['Title', 'Description', 'Thumbnail URL', 'Video URL'])
    
    # iterate through list of videos and extract information
    for item in search_data['items']:
        if item['id']['kind'] == 'youtube#video':
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            thumbnail_url = item['snippet']['thumbnails']['default']['url']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            
            # send request to video API to get full description
            video_endpoint = 'https://www.googleapis.com/youtube/v3/videos'
            video_params = {
                'part': 'snippet',
                'id': video_id,
                'key': api_key
            }
            video_response = requests.get(video_endpoint, params=video_params)
            video_data = video_response.json()
            description = video_data['items'][0]['snippet']['description']
        
            # write row to CSV file
            writer.writerow([title, description, thumbnail_url, video_url])
