#!/usr/bin/python
# -*- coding: utf-8 -*-

from base64 import b64encode
from time import sleep
import json
import re
import requests

USERNAME = ''
PASSWORD = ''
API_KEY = ''


def crua():
    return {
        'Accept': ('text/html,application/xhtml+xml,application/xml;'
                   'q=0.9,image/webp,*/*;q=0.8'),
        'Accept-Encoding':
        'gzip, deflate, sdch',
        'Accept-Language':
        'zh-CN,en-US;q=0.8,en;q=0.6',
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/56.0.2924.59 Safari/537.36')
    }


def redeem():
    v2ex = requests.session()
    host = 'www.v2ex.com'
    home_url = 'https://%s/' % host
    signin_url = 'https://%s/signin' % host
    mission_url = 'https://%s/mission/daily' % host
    v2ex.headers = crua()
    v2ex.headers['Origin'] = home_url
    try:
        resp = v2ex.get(signin_url)
        user, capt = re.findall(
            '<input type="text" class="sl" name="([0-9a-z]+)"', resp.text)
        pswd = re.search(
            '<input type="password" class="sl" name="([0-9a-z]+)"',
            resp.text).group(1)
        once = re.search(r'value="(\d+)" name="once"', resp.text).group(1)
        resp = v2ex.get('%s_captcha?once=%s' % (home_url, once))
        reqs = {
            'requests': [{
                'image': {
                    'content': b64encode(resp.content).decode()
                },
                'features': [{
                    'type': 'TEXT_DETECTION',
                    'maxResults': 1
                }]
            }]
        }
        payload = json.dumps(reqs).encode()
        response = requests.post(
            'https://vision.googleapis.com/v1/images:annotate',
            data=payload,
            params={'key': API_KEY},
            headers={
                'Content-Type': 'application/json'
            })
        code = response.json()['responses'][0]['fullTextAnnotation'][
            'text'].strip()
        if not code.isalnum():
            return True
        payload = {user: USERNAME, pswd: PASSWORD, capt: code, 'once': once}
        v2ex.headers['Referer'] = signin_url
        resp = v2ex.post(signin_url, data=payload)
        v2ex.headers['Referer'] = home_url
        resp = v2ex.get(mission_url)
        once = re.search(r'once=(\d+)', resp.text).group(1)
        v2ex.headers['Referer'] = mission_url
        redeem_url = '%s/redeem?once=%s' % (mission_url, once)
        resp = v2ex.get(redeem_url)
    except:
        pass
    if 'resp' in locals():
        days = re.search(r'已连续登录 (\d+) 天', resp.text)
        if days:
            print('[通知] V2EX 签到成功,', days.group(0))
            return False
    return True


def main():
    while redeem():
        sleep(180)


if __name__ == "__main__":
    main()
