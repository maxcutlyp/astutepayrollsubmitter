#!/usr/bin/env python3.10

import subprocess as sp
import os
import shutil
import datetime
from datetime import timedelta as td

def main():
    cwd = os.path.dirname(os.path.realpath(__file__))
    if (sp.run([f'{os.path.join(cwd, "login.sh")}']).returncode != 0):
        print("ERROR: couldn't log in.")
        return

    content = ''
    with open(os.path.join(cwd, "post_body"), 'rb') as f:
        content = f.read()

    today = datetime.date.today()
    monday = today - td(days=today.weekday())
    
    if (input(f'[T]his week ({monday.strftime("%d/%m")} to {(monday + td(days=4)).strftime("%d/%m")}) or [l]ast week ({(monday - td(days=7)).strftime("%d/%m")} to {(monday - td(days=3)).strftime("%d/%m")})? ') == 'l'):
        monday -= td(days=7)

    for day in range(7):
        date = monday + td(days=day)
        content = content.replace(bytes(date.strftime("DATE_%A").upper(), 'utf-8'), bytes(date.strftime('%Y-%m-%d'), 'utf-8'))

    with open(os.path.join(cwd, "post_body.current"), 'wb') as f:
        f.write(content)

    curl_content = ''
    with open(os.path.join(cwd, "raw_timesheet_submit.sh")) as f:
        curl_content = f.read()

    curl_content = curl_content.replace(("DATE_MONDAY"), monday.strftime('%Y-%m-%d'))

    with open(os.path.join(cwd, "raw_timesheet_submit.current.sh"), 'w') as f:
        f.write(curl_content)

    if (sp.run([f'{os.path.join(cwd, "raw_timesheet_submit.current.sh")}']).returncode != 0):
        print("ERROR: something went wrong submitting the timesheet.")
        return

if __name__ == '__main__':
    main()
