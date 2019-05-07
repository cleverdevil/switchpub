from dateutil.parser import parse
from dateutil.tz import gettz

import conf
import os
import json
import requests


pacific = gettz('America/Los_Angeles')


def publish(date, title, art, duration, uri):
    # generate body
    summary = 'Played on the Nintendo Switch.'

    # generate date time
    game_datetime = parse(date + ' 23:30').replace(tzinfo=pacific).isoformat()

    # fetch artwork
    art_response = requests.get(art)

    # publish
    response = requests.post('https://cleverdevil.io/play/hook/', data={
        'payload': json.dumps(dict(
            title=title,
            summary=summary,
            duration=duration,
            gameURL=uri,
            publishDateTime=game_datetime
        ))
    }, files={
        'photo': (
            art.rsplit('/', 1)[1],
            art_response.content,
            art_response.headers['Content-Type'],
            {'Expires': '0'}
        )
    })

    return response.status_code in (200, 201, 202)


# open the latest summary
summaries = json.loads(open(conf.PATH + '/summary.json').read())


# update our games database
games = json.loads(open(conf.PATH + '/games.json').read())
for summary in summaries.get('items', []):
    for game in summary.get('playedApps', []):
        if game['applicationId'] not in games:
            games[game['applicationId']] = game

with open(conf.PATH + '/games.json', 'w') as f:
    f.write(json.dumps(games))


# process games played
plays = []
for summary in summaries.get('items', []):
    # only process completed days
    if summary['result'] != 'ACHIEVED':
        print('Skipping date ->', summary['date'])
        continue

    print('=' * 80)
    print('Processing date ->', summary['date'])
    print('-' * 80)

    # loop through each player
    for player in summary['devicePlayers']:

        # ignore everyone but myself
        if player['nickname'] != 'Jonathan':
            continue

        # loop through each game I played on this date
        for play in player['playedApps']:
            game = games[play['applicationId']]

            # check for a footprint for this date/game
            footprint = (
                conf.HISTORY_PATH + '/' +
                summary['date'] + '-' +
                play['applicationId']
            )

            if os.path.exists(footprint):
                print('Skipping ->', summary['date'], '->', play['applicationId'])
                continue

            if game['title'].lower() == 'youtube':
                print('Skipping -> YouTube')
                continue

            # publish
            print('Publishing ->', summary['date'], '->', play['applicationId'])

            duration = play['playingTime'] / 60.0
            title = game['title']
            art = game['imageUri']['extraLarge']
            uri = game['shopUri']

            data = dict(
                date=summary['date'],
                title=title,
                art=art,
                duration=duration,
                uri=uri
            )

            success = publish(**data)

            # store a footprint if successful
            if success:
                open(footprint, 'w').write(json.dumps(data))
                print('Successfully published!')
            else:
                print('Failed to publish...')
