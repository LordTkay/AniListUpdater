import urllib

import requests
import Secrets
import json
import os
import mysql.connector as mariadb
import webbrowser
import datetime
import logging

from Anilist import AniList


class Series:

    def __init__(self, raw_entry):
        self.file_id = raw_entry[0]
        self.play_count = raw_entry[1]
        self.last_played = raw_entry[2]
        self.show_id = raw_entry[3]
        self.show_name = raw_entry[4]
        self.season_id = raw_entry[5]
        self.season = raw_entry[6]
        self.episode_id = raw_entry[7]
        self.episode = raw_entry[8]
        self.episode_name = raw_entry[9]
        self.episode_aired = raw_entry[10]
        self.show_first_aired = raw_entry[11]

    def __str__(self):
        return 'Serie: {} season {} latest episode {}'.format(self.show_name, self.season, self.episode)


DAYS_RANGE = 10
COMPLETED = 'COMPLETED'

logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%d-%m-%Y %H:%M:%S')

anilist = AniList(Secrets.API_ID, Secrets.API_SECRET, Secrets.API_REDIRECT_URI)
anilist.authorization.token = Secrets.API_TOKEN
anilist.authorization.token_type = 'Bearer'

host = 'Tkay-Server'
port = '3307'
user = 'Mediencenter'
password = 'Wabawa1998!Mediencenter'
database = 'mediencenter_video116'
mariadb_connection = mariadb.connect(host=host, port=port, user=user, password=password, database=database)
cursor = mariadb_connection.cursor()

cursor.execute('''
SELECT files.idfile, 
       files.playcount, 
       files.lastplayed, 
       episode.idshow, 
       tvshow.c00                                  AS tvshowName, 
       episode.idseason, 
       seasons.season, 
       episode.idepisode, 
       episode.c13                                 AS episode, 
       episode.c00                                 AS episodeName, 
       episode.c05                                 AS airedDate, 
       (SELECT Min(e1.c05) 
        FROM   episode AS e1 
        WHERE  e1.idshow = episode.idshow 
               AND e1.idseason = episode.idseason) AS firstAired 
FROM   files 
       INNER JOIN episode 
               ON episode.idfile = files.idfile 
       INNER JOIN seasons 
               ON seasons.idseason = episode.idseason 
       INNER JOIN tvshow 
               ON tvshow.idshow = episode.idshow 
WHERE  files.playcount IS NOT NULL 
       AND episode.c13 = (SELECT Max(Cast(e2.c13 AS UNSIGNED)) AS epi 
                          FROM   episode AS e2 
                          WHERE  e2.idshow = episode.idshow 
                                 AND e2.idseason = episode.idseason) 
GROUP  BY episode.idshow, 
          episode.idseason 
ORDER  BY tvshow.c00 ASC 
''')
series_list = cursor.fetchall()

for series_raw in series_list:
    logging.info('-'*20)
    series = Series(series_raw)
    anilist_id = None
    logging.info(series)

    # Prepare search parameters
    search_parameters = [
        {
            'name': 'type',
            'value': 'ANIME',
            'type': 'MediaType'
        }
    ]
    # Search for up to ten series with the name
    page_info, results = anilist.search_media(series.show_name,
                                              per_page=10,
                                              variables=search_parameters,
                                              fields=['status',
                                                      'episodes',
                                                      'startDate { year month day }',
                                                      'mediaListEntry { progress status }'])

    logging.info('{} entries received from AniList'.format(len(results)))

    # AniList may have a different day, which is one/two days off
    # Create a range from the aired date stored in the database
    anime_date = datetime.datetime.strptime(series.show_first_aired, '%Y-%m-%d')
    anime_date_past = anime_date - datetime.timedelta(days=DAYS_RANGE)
    anime_date_future = anime_date + datetime.timedelta(days=DAYS_RANGE)
    # Checking through all entries
    for result in results:
        date_values = result['startDate']
        if date_values['year'] is None or date_values['month'] is None:
            continue

        search_date = datetime.datetime(date_values['year'],
                                        date_values['month'],
                                        date_values['day'] if date_values['day'] is not None and
                                                              date_values['day'] != '' else anime_date.day)
        if anime_date_past <= search_date <= anime_date_future:
            # Save AniList ID of the anime and continue
            anilist_id = result['id']
            logging.info('Anime found {} ({})'.format(result['title']['romaji'], anilist_id))
            break

    # If an anime was found continue
    if anilist_id is not None:
        # Check if the online progress differs from the local one
        list_entry = result.get('mediaListEntry')
        max_episodes = result.get('episodes')
        if list_entry is None:
            online_progress = -1
        else:
            online_progress = list_entry['progress']

        logging.info('Online {} Local {}'.format(online_progress, series.episode))

        if True:
        # if int(online_progress) < int(series.episode):

            update_parameters = [
                {
                    'name': 'progress',
                    'value': series.episode,
                    'type': 'Int'
                }
            ]

            if max_episodes is not None and int(series.episode) >= max_episodes:
                update_parameters.append({
                    'name': 'status',
                    'value': COMPLETED,
                    'type': 'MediaListStatus'
                })

            anilist.update_series(anilist_id, variables=update_parameters, fields=['progress', 'status'])
            logging.info('Series updated!')
        else:
            logging.info('Series already up-to date')
    else:
        logging.warning('No Anime found! {}'.format(series.show_name))
