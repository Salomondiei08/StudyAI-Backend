from googleapiclient.discovery import build
import pprint


# Get youtube results
def get_youtube_videos(query: str, limit: str, key:str):

    print("Getting Videos...")

    # Define the YouTube API client
    youtube = build("youtube", "v3", developerKey=key)

    # Call the search.list method to retrieve video results
    search_response = youtube.search().list(
        q=query,
        type="video",
        part="id,snippet",
        maxResults=limit  # Change the number of results as per your need
    ).execute()

    # Create a new json and return the wanted data
    video_list = []
    for item in search_response['items']:
        if item["id"]["kind"] == "youtube#video":

            video_id = item['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            channelTitle = item['snippet']['channelTitle']
            description = item['snippet']['description']
            publishedAt = item['snippet']['publishedAt']
            high_thumbnail = item['snippet']['thumbnails']['high']['url']
            video_list.append({
                'title': item['snippet']['title'],
                'description': description,
                'videoUrl': video_url,
                'videoId': video_id,
                'publishedAt': publishedAt,
                'channelTitle': channelTitle,
                'thumbnails-high': high_thumbnail,
            })

    # Print the video details
    pprint.pprint(video_list)
    return video_list
