#!/usr/bin/env python3.10

import requests
import subprocess as sp
import os
import shutil
import datetime
from datetime import timedelta as td

USER_ID = 'max.cutlyp'
APPROVER_USER_ID = 'matt.bradbury'
MID = '43555'
UID = '43564'
DOMAIN = 'megt.astutepayroll.com'
LOGIN_PATH = '/megt/auth/login'
SUBMIT_PATH = '/megt/attendance/manage/'

def post_login(session: requests.Session):
    password = sp.run(['pass', 'megt-payroll'], capture_output=True).stdout[:-1].decode()

    headers = {
        'authority': DOMAIN,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': f'https://{DOMAIN}',
        'pragma': 'no-cache',
        'referer': f'https://{DOMAIN}{LOGIN_PATH}',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36',
    }

    data = f'authenticate_userid={USER_ID}&authenticate_password={password}&authenticate=yes&autologin=0&autologin=1&log_in=Log+In'

    # todo: handle failure
    response = session.post(f'https://{DOMAIN}{LOGIN_PATH}', headers=headers, data=data)

def post_timesheet_submit(session: requests.Session, monday: datetime.date):
    monday_formatted = monday.strftime('%Y-%m-%d')

    headers = {
        'authority': DOMAIN,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryfsXTtKjUet8vuqQ9',
        'origin': f'https://{DOMAIN}',
        'pragma': 'no-cache',
        'referer': f'https://{DOMAIN}{SUBMIT_PATH}?MID={MID}&UID={UID}&date={monday_formatted}',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36',
    }

    params = {
        'MID': MID,
        'UID': UID,
        'date': monday_formatted,
    }

    cwd = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(cwd, 'post_body'), 'rb') as f:
        content = f.read()

    for day in range(7):
        date = monday + td(days=day)
        content = content.replace(bytes(date.strftime("<DATE_%A>").upper(), 'utf-8'), bytes(date.strftime('%Y-%m-%d'), 'utf-8'))

    content = content.replace(b'<UID>', bytes(UID, 'utf-8'))
    content = content.replace(b'<APPROVER_USER_ID>', bytes(APPROVER_USER_ID, 'utf-8'))

    response = session.post(f'https://{DOMAIN}{SUBMIT_PATH}', params=params, headers=headers, data=content)

def main():
    session = requests.Session()
    post_login(session)

    today = datetime.date.today()
    monday = today - td(days=today.weekday())

    def monday_plus(days: int) -> str:
        return (monday + td(days=days)).strftime('%d/%m')

    if (input(f'[T]his week ({monday_plus(0)} to {monday_plus(4)}) or [l]ast week ({monday_plus(-7)} to {monday_plus(-3)})? ').lower() == 'l'):
        monday -= td(days=7)

    post_timesheet_submit(session, monday)

if __name__ == '__main__':
    main()
