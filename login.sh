#!/bin/bash

set -e

pw=$(pass megt-payroll)

curl 'https://megt.astutepayroll.com/megt/auth/login' \
  --cookie-jar "$(dirname $0)/cookies" \
  -H 'authority: megt.astutepayroll.com' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
  -H 'accept-language: en-GB,en-US;q=0.9,en;q=0.8' \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/x-www-form-urlencoded' \
  -H 'origin: https://megt.astutepayroll.com' \
  -H 'pragma: no-cache' \
  -H 'referer: https://megt.astutepayroll.com/megt/auth/login' \
  -H 'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="104"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: document' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-user: ?1' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36' \
  --data-raw "authenticate_userid=max.cutlyp&authenticate_password=$pw&authenticate=yes&autologin=0&autologin=1&log_in=Log+In" \
  --compressed
