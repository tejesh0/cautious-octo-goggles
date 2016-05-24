from django.http import HttpResponse
from django.shortcuts import render

import urllib2
import csv
import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def fetch_results_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sync_with_google_sheets.csv"'

    game = ''
    offset = ''
    limit = ''
    stream_type = ''
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

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    file1 = drive.CreateFile({'title': filename + '.csv', 'mimeType': 'text/csv'})
    file1.SetContentFile(filename + '.csv')
    file1.Upload()

    writer = csv.writer(response)
    for r in json_res['streams']:
        if r['channel']['name'] not in prev_users:
            writer.writerow([r['channel']['name']])

    return response


def fetch_results(request):
    game = ''
    offset = ''
    limit = ''
    stream_type = ''
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

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    file1 = drive.CreateFile({'title': filename + '.csv', 'mimeType': 'text/csv'})
    file1.SetContentFile(filename + '.csv')
    file1.Upload()

    return render(request, 'index.html', )
