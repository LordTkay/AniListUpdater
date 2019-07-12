import urllib

import requests
import Secrets
import json
import os
import webbrowser

# from Anilist_TEST import AniList
# #
# # anilist = AniList(Secrets.API_ID, Secrets.API_SECRET, Secrets.API_REDIRECT_URL)
# # if anilist.token == '':
# #     anilist.code_by_pin()
# #     code = input('Enter the Code: ')
# #     anilist.receive_token(code)
# #
# # mediaId = input('MediaID: ')
# # status = input('Status: ')
# #
# # anilist.update_anime(mediaId, status)

from Anilist import AniList

anilist = AniList()
anilist.authorization.client_id = Secrets.API_ID
anilist.authorization.client_secret = Secrets.API_SECRET
anilist.authorization.redirect_url = Secrets.API_REDIRECT_URI
# # print(anilist.authorization.code_by_pin_url())
# # anilist.authorization.token_by_code('def5020097ee7aeb614cb86ed4e51470491c5282b9fc7bdff19d5bad847a934900c13588a56c7c03217a55d0fc352fb5155ff24f4a000d79679f3dca8dcd80afea3d5c6e8e590bfd4810829c89a2d5e8a45b203877ae9d1d86e9f9170a3a9495db3bb54bb200b373c8a3063dc54fd0903a75270b3b83f3531a79afe4249cd2564b00e73f563a452cf4254c763739d6abc134d26761f701ad3154a3dfd43a2eb9729ed90635846c6877b5c7a22c67eb055f0f60abe4fc7fa77a3e4b93d56c3cf8214b19c46645e6a4ab8b8763b00467c30c6e76237ffd15e872c25fdb32deda8a0c272e1fc35d4f69283b2c124ae4d816e7684140cd32474e8db223fc8f3e97fb2cba101363ef75d8a687cf95a505103524953a37c7fc7c3eb4cc17d2ac96822ffedf5afe3163d3a5ee7ab6b6f035da40acd421c5b34266d76c9ade5e520cca2fe80807383d7ed7037da9a8af6487c5149b2b0619daf0587b2f4080d6774e7adfbafaf65834994e3ccf88c98b8f777a38')
anilist.authorization.token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImZkOWFiZTA5ZDFkOWE1ZTU5OWE3ZTgwZjA5NjRjOTliYTU1NzYyZTQxNmVmYTM3ZGM3YzUzMGY3NTY1ZjBlYTg2NzY4NThiYWNkYWFjOTk4In0.eyJhdWQiOiIyMTc4IiwianRpIjoiZmQ5YWJlMDlkMWQ5YTVlNTk5YTdlODBmMDk2NGM5OWJhNTU3NjJlNDE2ZWZhMzdkYzdjNTMwZjc1NjVmMGVhODY3Njg1OGJhY2RhYWM5OTgiLCJpYXQiOjE1NjA4NTQ2NTcsIm5iZiI6MTU2MDg1NDY1NywiZXhwIjoxNTkyNDc3MDU3LCJzdWIiOiIyNTU2OTYiLCJzY29wZXMiOltdfQ.VSpQOXCENyLECQHSxLCUxyVJWYtf9pNOJOPozbObBIccstcxJsRMdZnoRRyn7i4lfnfzRsECSyyU8g2ngCZYTCIcTFpa00rxJGrYQ3XJ4XDbR_xuFm7qPwku_weawY2JPiwgf9w_0v8Hxxo89vF9pE9lPM1A9KRt3YL-pNHiRWOkDtbEKkeXbq8H4ALupz14ltZWQwbud8TPVLRpVSvQVouhFbKsglEkxlbdYWHm7adDegK0l1rxGz4oA7kEltE_hDMrK5epcpw6NDFvkN9COB4LaQQk7939Ti_iL86Aj9n4b69qE3WhOYjcfaSIqW3oXxpJZa-VCm9JRsXPkf6MZ5Fdu547Jqz1SgMicZftYmAPbCoy4z4J2dYmp6_8NME6Q0NlhSlIUTGEOekntYhL5C-P4YjyP1GPi1aYS5Wv4s1hybuKTszmRSxDVKS8h-vvkhEWUXn25gwpBwPPf3y0nUts5iU0mA00uSF8YyNVMcTUw1fCcAy-cVF8QzTT8lQ-Fv1-__a7QG2s5PeaqLj7m_UTTUGvCgfJac-ETFr-VDtrsp0uLyjujCMHuo6RS5wPX11BRdUOgEgvym7cFDpxGm6s1bgsOiwVvBvG7lzpmuI1ox7AQTPOsMbtN-lo3MVom_InAHelfW_3s8sYCBeJZ6qyY8LPVq0XBYwe4O9RNUw'
anilist.authorization.token_type = 'Bearer'
#
# info, animes = anilist.search(0, 100, 'Mirai Nikki', additional_values=['status', 'description'])
# print(info)
# for media in animes:
#     print(media)

parameters = [
    {
        'name': 'type',
        'value': 'ANIME',
        'type': 'MediaType'
    }
]
# anilist.search_media('One Piece')
anilist.search_media('One Piece', variables=parameters, fields=['type'])