from dotenv import load_dotenv
import base64
import os
from requests import post, get
import json 

load_dotenv()

#by mestan

client_id = os.getenv("CLIENT_ID")
client_secret= os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = {"grant_type" : "client_credentials"}
    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token

def get_auth_header(token):
    return {"Authorization" : "Bearer " + token}


def search_for_artist(token,artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"



    query_url = url + query
    result =  get(query_url,headers = headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print('Error')
        return None

    return json_result[0]


def albums_of_artist(token,artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)

    albums = json_result.get('items', [])

    return albums

#artist_get = input("Artist Name \n") Getting artist name as input (remove "#")
token = get_token()
#travis_dayim = "Travis Scott"

result = search_for_artist(token,travis_dayim)

artist_id = result["id"]

albums = albums_of_artist(token, artist_id)

for idx, album in enumerate(albums):
    print(f"{idx + 1}.{album['name'], album['release_date']}")
