import requests
import webbrowser
import json
from urllib import parse


class AniList:

    AUTHORIZE_URL = 'https://anilist.co/api/v2/oauth/authorize?'
    TOKEN_URL = 'https://anilist.co/api/v2/oauth/token'
    GRAPHQL_URL = 'https://graphql.anilist.co'

    def __init__(self, client_id, client_secret, redirect_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_url = redirect_url

        self.token = ''
        self.token_type = ''

    def code_by_pin(self):
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_url,
            'response_type': 'code'
        }

        params = parse.urlencode(params)
        url = self.AUTHORIZE_URL + params
        webbrowser.open(url)

    def receive_token(self, code):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_url,
            'code': code
        }

        response = requests.post(self.TOKEN_URL, data=data, json=headers)
        if response.status_code != 200:
            raise Exception(response.text)

        json_content = json.loads(response.text)
        self.token = json_content['access_token']
        self.token_type = json_content['token_type']

    # Anime Functionalities

    def update_anime(self, mediaId : int, status):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': self.token_type + ' ' + self.token
        }

        query = '''
            mutation ($mediaId: Int, $status: MediaListStatus) {
              SaveMediaListEntry(mediaId: $mediaId, status: $status) {
                id
                status
              }
            }
        '''

        variables = {
            'mediaId': mediaId,
            'status': status
        }

        response = requests.post(self.GRAPHQL_URL, headers=headers, json={'query':query, 'variables': variables})
        if response.status_code != 200:
            raise Exception(response.text)
        return response.text
