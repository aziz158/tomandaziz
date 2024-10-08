


import json
import os
import folium
import pandas as pd
import webbrowser
from folium.plugins import GroupedLayerControl
from branca.colormap import linear
import requests
import SpotifyCredentials
from bs4 import BeautifulSoup
import time



def main():

    #RS_500_Songs()

    Spotify_Search_API()

def Spotify_Search_API():

     # POST
    auth_response = requests.post(SpotifyCredentials.AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': SpotifyCredentials.CLIENT_ID,
        'client_secret': SpotifyCredentials.CLIENT_SECRET,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()


    # save the access token
    access_token = auth_response_data['access_token']


    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    # Read the CSV file
    df = pd.read_csv('RS_500_Songs.csv')

    data = []

    for index, row in df.iterrows():

        print("Song number: " + str(index))
   

        search_params = {
            "q": row['Artist + Song'],
            "type": "track",
            "limit": 1  # Limit to one result
        }


        
        
        r = requests.get(SpotifyCredentials.SEARCH_API, headers=headers, params=search_params)
        search_results = r.json()
        

        if search_results['tracks']['items']:
            track = search_results['tracks']['items'][0]
            track_id = track['id']
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            album_name = track['album']['name']
  

            resp = get_audio_features(track_id, access_token)

            danceability = resp['danceability']
            energy = resp['energy']
            key = resp['key']
            loudness = resp['loudness']
            mode = resp['mode']
            speechiness = resp['speechiness']
            acousticness = resp['acousticness']
            instrumentalness = resp['instrumentalness']
            liveness = resp['liveness']
            valence = resp['valence']
            tempo = resp['tempo']
            duration_ms = resp['duration_ms']
            time_signature = resp['time_signature']

            data.append([row['Rank'], 
                         track_name, 
                         artist_name, 
                         album_name, 
                         danceability, 
                         energy, 
                         key, 
                         loudness, 
                         mode, 
                         speechiness, 
                         acousticness, 
                         instrumentalness,
                         liveness,
                         valence,
                         tempo,
                         duration_ms,
                         time_signature])

            


            # print(f"Track ID: {track_id}")
            # print(f"Track: {track_name}")
            # print(f"Artist: {artist_name}")
            # print(f"Album: {album_name}")
            # print(f"Spotify URL: {spotify_url}")
            # print(f"Danceability: {danceability}")
            # print(f"Energy: {energy}")
            # print(f"Key: {key}")
            # print(f"Loudness: {loudness}")
            # print(f"Mode: {mode}")
            # print(f"Speechiness: {speechiness}")
            # print(f"Acousticness: {acousticness}")
            # print(f"Instrumentalness: {instrumentalness}")
            # print(f"Liveness: {liveness}")
            # print(f"Valence: {valence}")
            # print(f"Tempo: {tempo}")
            # print(f"Duration: {duration_ms}")
            # print(f"Time Signature: {time_signature}")



        else:
            print("Track not found.")
        

        
        time.sleep(0.1)
    
    new_df = pd.DataFrame(data, columns=['rank',
                         'track_name', 
                         'artist_name', 
                         'album_name', 
                         'danceability', 
                         'energy', 
                         'key', 
                         'loudness', 
                         'mode', 
                         'speechiness', 
                         'acousticness', 
                         'instrumentalness',
                         'liveness',
                         'valence',
                         'tempo',
                         'duration_ms',
                         'time_signature'])
    new_df.to_csv('RS_500_Songs_final.csv', index=False)

    
def get_audio_features(track_id, access_token):
    features_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    features_headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(features_url, headers=features_headers)
    if response.status_code == 429:  # Too Many Requests
        retry_after = int(response.headers.get("Retry-After", 1))
        print(f"Rate limited. Retrying after {retry_after} seconds.")
        time.sleep(retry_after)
        return get_audio_features(track_id, access_token)  # Recursive call after waiting
    
    return response.json()


def RS_500_Songs():

    data = []
    rank = 500
    
    link = ['https://www.rollingstone.com/music/music-lists/best-songs-of-all-time-1224767/townes-van-zandt-pancho-and-lefty-1224839/',
            'https://www.rollingstone.com/music/music-lists/best-songs-of-all-time-1224767/neil-young-powderfinger-1224887/',
            'https://www.rollingstone.com/music/music-lists/best-songs-of-all-time-1224767/sylvester-you-make-me-feel-mighty-real-1224939/',
            'https://www.rollingstone.com/music/music-lists/best-songs-of-all-time-1224767/the-zombies-time-of-the-season-1224989/',
            'https://www.rollingstone.com/music/music-lists/best-songs-of-all-time-1224767/the-b-52s-rock-lobster-2-1225038/',
            'https://www.rollingstone.com/music/music-lists/best-songs-of-all-time-1224767/jimi-hendrix-purple-haze-2-1225088/',
            'https://www.rollingstone.com/music/music-lists/best-songs-of-all-time-1224767/david-bowie-changes-2-1225138/',
            'https://www.rollingstone.com/music/music-lists/best-songs-of-all-time-1224767/green-day-basket-case-1225188/',
            'https://www.rollingstone.com/music/music-lists/best-songs-of-all-time-1224767/bob-dylan-blowin-in-the-wind-3-1225238/',
            'https://www.rollingstone.com/music/music-lists/best-songs-of-all-time-1224767/daddy-yankee-feat-glory-gasolina-1225288/'
            ]
    
    for l in link:
        r = requests.get(l)
        s1 = BeautifulSoup(r.content, 'html.parser')
        result = s1.find('div', id = 'pmc-gallery-vertical')
        h2s = result.find_all('h2')
        for h2 in h2s:
            s = h2.get_text()
            s = s.replace("‘", "")
            s = s.replace("’", "")
            s = s.replace(",", " ")
            s = s.replace("\xa0", "")
            data.append([rank, s])
            rank -= 1

   


    df = pd.DataFrame(data, columns=['Rank', 'Artist + Song'])

    df.to_csv('RS_500_Songs.csv', index=False)
   








if __name__ == '__main__':
    main()