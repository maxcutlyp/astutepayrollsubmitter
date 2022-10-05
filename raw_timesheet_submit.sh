#!/bin/bash

curl 'https://megt.astutepayroll.com/megt/attendance/manage/?MID=43555&UID=43564&date=DATE_MONDAY' \
  --cookie "$(dirname $0)/cookies" \
  -H 'authority: megt.astutepayroll.com' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
  -H 'accept-language: en-GB,en-US;q=0.9,en;q=0.8' \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundaryfsXTtKjUet8vuqQ9' \
  -H 'origin: https://megt.astutepayroll.com' \
  -H 'pragma: no-cache' \
  -H 'referer: https://megt.astutepayroll.com/megt/attendance/manage/?MID=43555&UID=43564&date=DATE_MONDAY' \
  -H 'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="104"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: document' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-user: ?1' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36' \
  --data-binary "@$(dirname $0)/post_body.current" \
  --compressed \
