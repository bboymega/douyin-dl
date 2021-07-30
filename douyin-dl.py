#!/usr/local/bin/python3
import requests
import json
import argparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument("url", help="URL of Video Page", type=str, dest="url_vid")
parser.add_argument("-o", "--output", default='./',dest="output", help="Set Output Location", action="store")
args=parser.parse_args()
output_lo=args.output
url=args.url_vid

if(output_lo[len(output_lo)-1] != '/'):
    output_lo=output_lo+'/'


downloader=requests.session()
header={
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'utf8',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'dnt': '1',
    'pragma': 'no-cache',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
}
downloader.headers.update(header)
print("Loading video page...")
page=downloader.get(url, verify=False, allow_redirects=True)

soup = BeautifulSoup(page.text,features="html.parser")

script=soup.find(id="RENDER_DATA")
title=soup.find("title").string[:-6]

for jsons in script:
    prettified_json=json.loads(urllib.parse.unquote(jsons))
    addr0 = "https:"+prettified_json["C_12"]["aweme"]["detail"]["video"]["playAddr"][0]["src"]
    addr1 ="https"+prettified_json["C_12"]["aweme"]["detail"]["video"]["playAddr"][1]["src"]
    print("Saving video to '"+output_lo+title+'.mp4'+"'")
    vid=requests.get(addr0)
    with open(output_lo+title+'.mp4','wb') as f:
        f.write(vid.content)
    print("Video downloaded.")
