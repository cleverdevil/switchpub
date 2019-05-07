import conf
import json
import requests



def get_access_token():
    response = requests.post(conf.TOKEN_API_URL, data={
        'session_token': conf.SESSION_TOKEN,
        'client_id': conf.CLIENT_ID,
        'grant_type': conf.GRANT_TYPE
    })
    return response.json()


def get_daily_summary(access):
    response = requests.get(conf.SUMMARY_URL, headers={
        'x-moon-os-language': 'en-US',
        'x-moon-app-language': 'en-US',
        'authorization': access['token_type'] + ' ' + access['access_token'],
        'x-moon-app-internal-version': '271',
        'x-moon-app-display-version': '1.8.0',
        'x-moon-app-id': 'com.nintendo.znma',
        'x-moon-os': 'IOS',
        'x-moon-os-version': '12.1.4',
        'x-moon-model': 'iPhone10,3',
        'accept-encoding': 'gzip;q=1.0, compress;q=0.5',
        'accept-language': 'en-US;q=1.0',
        'user-agent': 'moon_ios/1.8.0 (com.nintendo.znma; build:271; iOS 12.1.4) Alamofire/4.7.3',
        'x-moon-timezone': 'America/Los_Angeles',
        'x-moon-smart-device-id': conf.SMART_DEVICE_ID
    })
    return response.json()


if __name__ == '__main__':
    token = get_access_token()
    summary = get_daily_summary(token)

    with open(conf.PATH + '/summary.json', 'w') as f:
        f.write(json.dumps(summary))
