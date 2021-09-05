from googleapiclient.discovery import build

api_key = 'AIzaSyC0qvJDC0eOFTL7j368bmU2KaoUBaV1saY'

youtube = build('youtube', 'v3', developerKey=api_key)

def search(topic):
    ##searching for playlists
    request_playlists = youtube.search().list(
            part="snippet",
            maxResults=25,
            q=topic,
            type="playlist",
    )
    response_playlists = request_playlists.execute()

    playlist_ids = []

    items_playlists = response_playlists['items']
    for i in items_playlists:
        playlist_ids.append(i['id']['playlistId'])


    #getting 1st video of playlist:
    video_ids = []
    for pid in playlist_ids:

        request_video = youtube.playlistItems().list(
                part="contentDetails",
                playlistId=pid
        )

        respone_video = request_video.execute()

        items_videos = respone_video['items']

        request_sp_video = youtube.videos().list(
            part="snippet",
            id=items_videos[0]['contentDetails']['videoId']
        )

        response_sp_video = request_sp_video.execute()

        video_ids.append((items_videos[0]['contentDetails']['videoId'], response_sp_video['items'][0]['snippet']['title']))
    print(video_ids)
    return(video_ids)