#!/usr/bin/env python3.10

import requests
import subprocess as sp
import os
import shutil
import datetime
from datetime import timedelta as td

def post_login(session: requests.Session):
    password = sp.run(['pass', 'megt-payroll'], capture_output=True).stdout[:-1].decode()

    headers = {
        'authority': 'megt.astutepayroll.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://megt.astutepayroll.com',
        'pragma': 'no-cache',
        'referer': 'https://megt.astutepayroll.com/megt/auth/login',
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

    data = f'authenticate_userid=max.cutlyp&authenticate_password={password}&authenticate=yes&autologin=0&autologin=1&log_in=Log+In'

    # todo: handle failure
    response = session.post('https://megt.astutepayroll.com/megt/auth/login', headers=headers, data=data)

def post_timesheet_submit(session: requests.Session, monday: datetime.date):
    monday_formatted = monday.strftime('%Y-%m-%d')

    headers = {
        'authority': 'megt.astutepayroll.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryfsXTtKjUet8vuqQ9',
        'origin': 'https://megt.astutepayroll.com',
        'pragma': 'no-cache',
        'referer': f'https://megt.astutepayroll.com/megt/attendance/manage/?MID=43555&UID=43564&date={monday_formatted}',
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
        'MID': '43555',
        'UID': '43564',
        'date': monday_formatted,
    }

    cwd = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(cwd, 'post_body'), 'rb') as f:
        content = f.read()

    for day in range(7):
        date = monday + td(days=day)
        content = content.replace(bytes(date.strftime("DATE_%A").upper(), 'utf-8'), bytes(date.strftime('%Y-%m-%d'), 'utf-8'))

    response = session.post('https://megt.astutepayroll.com/megt/attendance/manage/', params=params, headers=headers, data=content)

def main():
    session = requests.Session()
    post_login(session)

    today = datetime.date.today()
    monday = today - td(days=today.weekday())

    if (input(f'[T]his week ({monday.strftime("%d/%m")} to {(monday + td(days=4)).strftime("%d/%m")}) or [l]ast week ({(monday - td(days=7)).strftime("%d/%m")} to {(monday - td(days=3)).strftime("%d/%m")})? ') == 'l'):
        monday -= td(days=7)

    post_timesheet_submit(session, monday)

if __name__ == '__main__':
    main()
