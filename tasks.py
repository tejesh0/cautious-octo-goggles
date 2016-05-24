# dependencies
# pydrive
# redis
# celery

import urllib2
import csv
import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from celery import Celery
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from celery.task.schedules import crontab


app = Celery('tasks', broker='redis://localhost')
logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute=0, hour=0)),
    name="fetch_users_from_twitch",
    ignore_result=True
)
def fetch_users_from_twitch():
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

    for r in json_res['streams']:
        if r['channel']['name'] not in prev_users:
            csv_writer.writerow([r['channel']['name']])

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    file1 = drive.CreateFile({'title': filename + '.csv', 'mimeType': 'text/csv'})
    file1.SetContentFile(filename + '.csv')
    file1.Upload()

    logger.info("Saved to google drive")
