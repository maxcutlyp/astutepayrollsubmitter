#!/usr/bin/env python3.10

import os
import urllib.parse
import datetime
from datetime import timedelta as td

default_times = ('9:00am', '5:00pm', '30')

def main():
    login_url_raw = input('Paste the URL of your astutepayroll login page: ').strip()
    login_url_parsed = urllib.parse.urlparse(login_url_raw)
    DOMAIN = login_url_parsed.netloc
    LOGIN_PATH = login_url_parsed.path

    USER_ID = input('Enter your astutepayroll username: ').strip()
    PASSWORD_CMD = input('Enter a command that sends your astutepayroll password to stdout, or leave blank to prompt to have the script prompt every time: ')
    submit_url_raw = input('Go to one of your timesheets and paste its URL: ').strip()
    submit_url_parsed = urllib.parse.urlparse(submit_url_raw)
    assert submit_url_parsed.netloc == DOMAIN, 'ERROR: Timesheet URL should have the same domain as login URL.'
    SUBMIT_PATH = submit_url_parsed.path
    submit_url_qs = dict(urllib.parse.parse_qsl(submit_url_parsed.query))
    assert 'MID' in submit_url_qs, 'ERROR: MID not found in timesheet URL.'
    assert 'UID' in submit_url_qs, 'ERROR: UID not found in timesheet URL.'
    MID = submit_url_qs['MID']
    UID = submit_url_qs['UID']

    APPROVER_USER_ID = input('Enter your approver\'s username: ').strip()

    today = datetime.date.today()
    monday = today - td(days=today.weekday())
    TIMES = []

    for day in range(5):
        day_string = (monday + td(day)).strftime('%A')
        prev = TIMES[-1] if len(TIMES) > 0 else default_times

        raw_times = tuple(
            input(f'Enter your {item} on {day_string} (leave blank for {prev[i]}): ') or prev[i]
            for i,item in enumerate(('start time', 'finish time', 'break length in minutes')))
        TIMES.append(raw_times)

    # Saturday and Sunday are not supported currently
    for _ in range(2): TIMES.append((None, None, None))

    _newline = '\n' # because f-strings can't include backslashes

    out = f'''# generated by setup.py

{USER_ID = }
{APPROVER_USER_ID = }
{MID = }
{UID = }
{DOMAIN = }
{LOGIN_PATH = }
{SUBMIT_PATH = }
{PASSWORD_CMD = }

TIMES = [
{_newline.join(f'    {time} # {(monday + td(day)).strftime("%A")}' for day,time in enumerate(TIMES))}
]
'''

    env_py_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'env.py')
    with open(env_py_path, 'w') as f:
        f.write(out)
    print(f'env.py generated at: {env_py_path}')

if __name__ == '__main__':
    main()
