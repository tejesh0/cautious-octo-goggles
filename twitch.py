from bs4 import BeautifulSoup
import urllib2
import csv
import pickle
import urllib
import json
import requests

# from celery import Celery
# app = Celery('tasks', broker='redis://localhost')
# from .celery import app


# @app.task
def fetch_users_from_twitch():
    game = ''
    # channel = ''
    offset = ''
    limit = ''
    # client_id = ''
    stream_type = ''
    # game channel limit offset client_id stream_type
    filename = 'sync_with_google_sheets'
    csv_file = open(filename + '.csv', 'a+')
    csv_writer = csv.writer(csv_file)


    source = urllib2.urlopen("https://api.twitch.tv/kraken/streams" + "?game=" + game +
                             '&limit=' + limit + '&offset=' + offset + '&stream_type=' + stream_type)

    json_res = json.load(source)

    with open(filename + '.csv', 'rb') as f:
        prev_users = [row.rstrip() for row in f]

    print prev_users
    for r in json_res['streams']:
        if r['channel']['name'] not in prev_users:
            csv_writer.writerow([r['channel']['name']])


    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    file1 = drive.CreateFile({'title': filename + '.csv', 'mimeType': 'text/csv'})
    file1.SetContentFile(filename + '.csv')
    file1.Upload()

fetch_users_from_twitch()
# host = 'https://www.googleapis.com'
# url = '/upload/drive/v3/files?uploadType=media'
# values = {}


# files = {'file': open(filename + '.csv')}
# response = requests.post(host + url, files=files)
# print response.read()

# https://api.twitch.tv/kraken/streams?game=&
# source = urllib2.urlopen("https://api.twitch.tv/kraken/streams" + "?game=" + game + '&limit=' + limit + '&offset=' + offset +'&client_id='+ client_id + '&stream_type=' + stream_type)

# data = urllib.urlencode(values)
# req = urllib2.Request(url, data)
# response = urllib2.urlopen(req)

