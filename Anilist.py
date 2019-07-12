import requests
import webbrowser
import json
from urllib import parse
from enum import Enum


class MediaFormat(Enum):
    TV = 'TV'
    TV_SHORT = 'TV_SHORT'
    MOVIE = 'MOVIE'
    SPECIAL = 'SPECIAL'
    OVA = 'OVA'
    MUSIC = 'MUSIC'
    MANGA = 'MANGA'
    NOVEL = 'NOVEL'
    ONE_SHOT = 'ONE_SHOT'


class MediaStatus(Enum):
    FINISHED = 'FINISHED'
    RELEASING = 'RELEASING'
    NOT_YET_RELEASED = 'NOT_YET_RELEASED'
    CANCELLED = 'CANCELLED'


class AniList:
    GRAPHQL_URL = 'https://graphql.anilist.co'

    def __init__(self):
        self.authorization = _Authorization()

    def __graphql_request(self, query, variables):
        headers = self.authorization.get_headers()
        json_data = {
            'query': query,
            'variables': variables
        }

        response = requests.post(self.GRAPHQL_URL, headers=headers, json=json_data)
        if response.status_code != 200:
            raise Exception(response.text)
        return response.text

    def search_media(self, search, variables={}, fields=[]):

        query_params = ''
        media_params = ''
        values = {}
        values['search'] = search
        for variable in variables:
            query_params += ', ${}: {}'.format(variable['name'], variable['type'])
            media_params += ', {0}: ${0}'.format(variable['name'])
            values[variable['name']] = variable['value']

        query = '''
        query($search: String, $page: Int, $perPage: Int{}) {{
            Page(page: $page, perPage: $perPage) {{
                pageInfo {{
                    total
                    perPage
                    currentPage
                    lastPage
                    hasNextPage
                }}
            
                media(search: $search{}) {{
                    id
                    title {{
                        romaji
                        english
                        native
                        userPreferred
                    }}
                    {}
                }}
            }}
        }}
        '''.format(query_params, media_params, ' '.join(fields))

        print(values)
        print( self.__graphql_request(query, values))












class _Authorization :
    AUTHORIZE_URL = 'https://anilist.co/api/v2/oauth/authorize?'
    TOKEN_URL = 'https://anilist.co/api/v2/oauth/token'

    def __init__(self, client_id='', client_secret='', redirect_uri=''):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_url = redirect_uri

        self.token = ''
        self.token_type = ''

    def code_by_pin_url(self):
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_url,
            'response_type': 'code'
        }

        params = parse.urlencode(params)
        url = self.AUTHORIZE_URL + params
        return url

    def token_by_code(self, code):
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
        print(self.token)
        self.token_type = json_content['token_type']

    def get_headers(self):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': self.token_type + ' ' + self.token
        }

        return headers


class Media:
    def __init__(self, id):
        self.id = id
        self.id_mal = 0
        self.title = []
        self.type = ''
        self.format = ''
        self.status = ''
        self.description = ''
        self.start_date = None
        self.end_date = None
        self.country_of_origin = ''
        self.is_favourite = False

    def __str__(self):
        return '{}-{}({})'.format(self.id, self.title['romaji'], self.type)


class Anime(Media):
    def __init__(self, id):
        super(Anime, self).__init__(id)
        self.season = ''
        self.episodes = 0
        self.duration = 0


class Manga(Media):
    def __init__(self, id):
        super(Manga, self).__init__(id)
        self.chapter = 0
        self.volumes = 0
