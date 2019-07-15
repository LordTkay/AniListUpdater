import urllib

import requests
import Secrets
import json
import os
import webbrowser

from Anilist import AniList

anilist = AniList(Secrets.API_ID, Secrets.API_SECRET, Secrets.API_REDIRECT_URI)
print('Please enter following website and copy the token.')
print(anilist.authorization.code_by_pin_url())
code = input('Enter Code here:\n')

anilist.authorization.token_by_code(code)
token = anilist.authorization.token

lines = []
with open('Secrets.py', 'r') as file:
    line = file.readline()
    while line:
        if 'API_TOKEN' in line:
            line = 'API_TOKEN = \'{}\''.format(token)

        lines.append(line)
        line = file.readline()

open('Secrets.py', 'w').write(''.join(lines))
print('Token was saved!')
