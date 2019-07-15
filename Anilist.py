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

    def __init__(self, client_id, client_secret, redirect_url):
        self.authorization = _Authorization(client_id, client_secret, redirect_url)

    def __graphql_request(self, query, variables):
        headers = self.authorization.get_headers()
        json_data = {
            'query': query,
            'variables': variables
        }

        response = requests.post(self.GRAPHQL_URL, headers=headers, json=json_data)
        if response.status_code != 200:
            raise Exception(response.text)
        return json.loads(response.text)

    @staticmethod
    def __prepare_query_data(variables):
        query_params = ''
        media_params = ''
        values = {}
        for variable in variables:
            query_params += ', ${}: {}'.format(variable['name'], variable['type'])
            media_params += ', {0}: ${0}'.format(variable['name'])
            values[variable['name']] = variable['value']

        return query_params, media_params, values

    def search_media(self, search, page=None, per_page=None, variables={}, fields=[]):
        query_params, media_params, values = AniList.__prepare_query_data(variables)
        values['search'] = search
        values['page'] = page
        values['perPage'] = per_page

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
                    type
                    {}
                }}
            }}
        }}
        '''.format(query_params, media_params, ' '.join(fields))

        json_values = self.__graphql_request(query, values)['data']['Page']
        json_page_info = json_values['pageInfo']
        json_media = json_values['media']

        page_info = PageInfo(json_page_info['total'], json_page_info['perPage'], json_page_info['currentPage'],
                             json_page_info['lastPage'], json_page_info['hasNextPage'])

        return page_info, json_media

    def update_series(self, media_id, variables=[], fields=[]):
        query_params, media_params, values = AniList.__prepare_query_data(variables)
        values['mediaId'] = media_id

        query = '''
        mutation ($mediaId: Int{}) {{
          SaveMediaListEntry(mediaId: $mediaId{}) {{
            id
            {}
          }}
        }}
        '''.format(query_params, media_params, ' '.join(fields))

        json_values = self.__graphql_request(query, values)['data']


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


class PageInfo:
    def __init__(self, total=0, per_page=0, current_page=0, last_page=0, has_next_page=False):
        self.total = total
        self.per_page = per_page
        self.current_page = current_page
        self.last_page = last_page
        self.has_next_page = has_next_page

    def __str__(self):
        return '{}/{}'.format(self.current_page, self.last_page)
