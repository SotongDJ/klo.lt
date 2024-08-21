#!/bin/env python
"""Update RSS feed."""
from datetime import datetime
import argparse
import hashlib
import json
import pathlib
import time
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup as bs
import random
import requests
import rtoml
import configdo

user_agents = [
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",

"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",

"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",

"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",

"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",

"Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",

"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",

"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",

"Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 Mobile/14G60 Safari/602.1",

"Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",

"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",

"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0",

"Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36",

"Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.96 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",

"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)",

"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",

"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",

"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36 Edge/13.10586",

"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",

"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36", 

"Mozilla/5.0 (Linux; U; Android 4.3.1; SGH-N075S Build/JSS15J) AppleWebKit/601.27 (KHTML, like Gecko) Chrome/52.0.2308.137 Mobile Safari/603.4", 

"Mozilla/5.0 (Windows; Windows NT 10.0; x64) AppleWebKit/603.40 (KHTML, like Gecko) Chrome/47.0.3384.333 Safari/603.5 Edge/9.26866", 

"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) Gecko/20100101 Firefox/45.8", 

"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 10.3; WOW64 Trident/4.0)", 

"Mozilla/5.0 (Windows; U; Windows NT 6.1; WOW64; en-US) AppleWebKit/603.25 (KHTML, like Gecko) Chrome/52.0.3570.145 Safari/535", 

"Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_7; like Mac OS X) AppleWebKit/537.46 (KHTML, like Gecko) Chrome/51.0.3412.395 Mobile Safari/602.6", 

"Mozilla/5.0 (Windows; Windows NT 10.5; WOW64) AppleWebKit/535.28 (KHTML, like Gecko) Chrome/50.0.1179.375 Safari/537.1 Edge/13.77379", 

" Mozilla/5.0 (U; Linux i681 x86_64) AppleWebKit/602.36 (KHTML, like Gecko) Chrome/54.0.2158.147 Safari/537", 

"Mozilla/5.0 (Windows NT 10.2;; en-US) AppleWebKit/603.13 (KHTML, like Gecko) Chrome/55.0.2735.226 Safari/534.3 Edge/13.35455", 

"Mozilla/5.0 (Windows; Windows NT 10.0; x64; en-US) AppleWebKit/534.28 (KHTML, like Gecko) Chrome/50.0.3818.273 Safari/603.1 Edge/10.30122", 

"Mozilla/5.0 (Linux; Linux x86_64; en-US) Gecko/20100101 Firefox/56.4", 

"Mozilla/5.0 (Windows; U; Windows NT 10.3; Win64; x64; en-US) Gecko/20100101 Firefox/48.5", 

"Mozilla/5.0 (Linux i574 ) AppleWebKit/533.12 (KHTML, like Gecko) Chrome/50.0.2242.140 Safari/603", 

"Mozilla/5.0 (Android; Android 6.0.1; HTC One_M9 Build/MRA58K) AppleWebKit/601.7 (KHTML, like Gecko) Chrome/50.0.3579.306 Mobile Safari/601.7",

"Mozilla/5.0 (Linux x86_64; en-US) Gecko/20100101 Firefox/51.5", 

"Mozilla/5.0 (Linux x86_64; en-US) AppleWebKit/537.32 (KHTML, like Gecko) Chrome/52.0.1580.167 Safari/601", 

"Mozilla/5.0 (compatible; MSIE 11.0; Windows; U; Windows NT 6.0;; en-US Trident/7.0)", 

"Mozilla/5.0 (Windows; U; Windows NT 10.2; WOW64; en-US) AppleWebKit/600.38 (KHTML, like Gecko) Chrome/54.0.1198.281 Safari/601.2 Edge/10.31479", 

"Mozilla/5.0 (Windows NT 10.4; Win64; x64) AppleWebKit/600.5 (KHTML, like Gecko) Chrome/51.0.3831.339 Safari/533.3 Edge/9.22682",

"Mozilla/5.0 (Linux; U; Linux x86_64) Gecko/20100101 Firefox/52.6", 

"Mozilla/5.0 (iPhone; CPU iPhone OS 9_1_5; like Mac OS X) AppleWebKit/602.34 (KHTML, like Gecko) Chrome/55.0.3815.251 Mobile Safari/600.6",

"Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_8; like Mac OS X) AppleWebKit/536.29 (KHTML, like Gecko) Chrome/55.0.2159.286 Mobile Safari/602.5", 

"Mozilla/5.0 (Windows; Windows NT 10.1; WOW64; en-US) AppleWebKit/535.44 (KHTML, like Gecko) Chrome/55.0.2930.353 Safari/600.1 Edge/10.70900", 

"Mozilla/5.0 (Linux i676 ; en-US) Gecko/20100101 Firefox/73.5", 

"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 8_0_9) AppleWebKit/537.41 (KHTML, like Gecko) Chrome/55.0.1341.279 Safari/537", 

"Mozilla/5.0 (Windows; U; Windows NT 10.3; Win64; x64; en-US) AppleWebKit/601.18 (KHTML, like Gecko) Chrome/49.0.1302.348 Safari/600.6 Edge/15.66121", 

"Mozilla/5.0 (Linux; Android 5.0.1; SAMSUNG-SM-N915F Build/LRX22C) AppleWebKit/533.25 (KHTML, like Gecko) Chrome/50.0.1187.169 Mobile Safari/602.9", 

"Mozilla/5.0 (Macintosh; Intel Mac OS X 9_8_5) AppleWebKit/601.14 (KHTML, like Gecko) Chrome/52.0.1558.279 Safari/600", 

"Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; en-US Trident/4.0)", 

"Mozilla/5.0 (Windows; U; Windows NT 6.3;) AppleWebKit/537.10 (KHTML, like Gecko) Chrome/47.0.2984.378 Safari/601", 

"Mozilla/5.0 (Windows; Windows NT 6.1; Win64; x64; en-US) Gecko/20100101 Firefox/54.6",

"Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.1; Win64; x64; en-US Trident/4.0)", 

"Mozilla/5.0 (Windows; U; Windows NT 10.1; x64) AppleWebKit/534.21 (KHTML, like Gecko) Chrome/51.0.3288.157 Safari/602.1 Edge/11.59703", 

"Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/600.1 (KHTML, like Gecko) Chrome/53.0.3684.269 Safari/534", 

"Mozilla/5.0 (iPhone; CPU iPhone OS 9_4_8; like Mac OS X) AppleWebKit/537.3 (KHTML, like Gecko) Chrome/47.0.2512.112 Mobile Safari/602.2",

"Mozilla/5.0 (Linux i680 x86_64; en-US) AppleWebKit/603.40 (KHTML, like Gecko) Chrome/50.0.1121.210 Safari/533", 

"Mozilla/5.0 (Linux; U; Android 5.1; MOTOROLA MOTO XT1562 Build/LMY47Z) AppleWebKit/601.36 (KHTML, like Gecko) Chrome/52.0.3113.396 Mobile Safari/533.6", 

"Mozilla/5.0 (Linux; Android 7.1.1; Pixel XL Build/NME91E) AppleWebKit/600.16 (KHTML, like Gecko) Chrome/54.0.2297.195 Mobile Safari/600.4",

"Mozilla/5.0 (Linux; Linux x86_64) AppleWebKit/533.30 (KHTML, like Gecko) Chrome/52.0.3768.289 Safari/533",

"Mozilla/5.0 (Linux; U; Linux i642 ; en-US) Gecko/20130401 Firefox/59.9", 

"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 9_7_7) AppleWebKit/534.4 (KHTML, like Gecko) Chrome/48.0.1426.252 Safari/536", 

"Mozilla/5.0 (Linux; Android 5.0.2; Lenovo A7000-a Build/LRX21M;) AppleWebKit/534.44 (KHTML, like Gecko) Chrome/53.0.2561.206 Mobile Safari/602.1",

"Mozilla/5.0 (iPod; CPU iPod OS 7_0_7; like Mac OS X) AppleWebKit/535.44 (KHTML, like Gecko) Chrome/54.0.1077.258 Mobile Safari/535.7",

"Mozilla/5.0 (Android; Android 4.4.1; XT1050 Build/SU6-7.3) AppleWebKit/600.7 (KHTML, like Gecko) Chrome/51.0.2717.154 Mobile Safari/534.2", 

"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_1_2) Gecko/20130401 Firefox/63.8", 

"Mozilla/5.0 (iPhone; CPU iPhone OS 7_8_0; like Mac OS X) AppleWebKit/536.13 (KHTML, like Gecko) Chrome/48.0.1562.267 Mobile Safari/600.3",

"Mozilla/5.0 (Macintosh; Intel Mac OS X 8_6_5) AppleWebKit/533.1 (KHTML, like Gecko) Chrome/54.0.3298.105 Safari/533",

"Mozilla/5.0 (Linux; U; Linux x86_64) AppleWebKit/603.7 (KHTML, like Gecko) Chrome/48.0.3606.148 Safari/536", 

"Mozilla/5.0 (iPod; CPU iPod OS 10_3_5; like Mac OS X) AppleWebKit/603.40 (KHTML, like Gecko) Chrome/48.0.3632.383 Mobile Safari/602.2",

"Mozilla/5.0 (Windows NT 10.5; x64; en-US) AppleWebKit/603.35 (KHTML, like Gecko) Chrome/52.0.1514.285 Safari/534.9 Edge/15.24694",

"Mozilla/5.0 (Linux; U; Android 7.1; Xperia Build/NDE63X) AppleWebKit/537.24 (KHTML, like Gecko) Chrome/47.0.1148.130 Mobile Safari/603.3",

"Mozilla/5.0 (Windows; Windows NT 10.0; x64; en-US) AppleWebKit/600.17 (KHTML, like Gecko) Chrome/55.0.1690.300 Safari/603.0 Edge/8.28305",

"Mozilla/5.0 (compatible; MSIE 8.0; Windows; U; Windows NT 6.1; Win64; x64 Trident/4.0)",

"Mozilla/5.0 (Android; Android 5.0; LG-D335 Build/LRX22G) AppleWebKit/600.42 (KHTML, like Gecko) Chrome/49.0.1390.138 Mobile Safari/533.8",

"Mozilla/5.0 (compatible; MSIE 8.0; Windows; Windows NT 6.0; WOW64 Trident/4.0)",

"Mozilla/5.0 (Windows NT 10.0; WOW64; en-US) Gecko/20100101 Firefox/50.0", 

"Mozilla/5.0 (Android; Android 7.1.1; Pixel C Build/NRD90M) AppleWebKit/535.35 (KHTML, like Gecko) Chrome/51.0.1185.164 Mobile Safari/537.1",

"Mozilla/5.0 (iPhone; CPU iPhone OS 10_6_2; like Mac OS X) AppleWebKit/537.40 (KHTML, like Gecko) Chrome/49.0.2804.177 Mobile Safari/534.8",

"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_11_8; en-US) AppleWebKit/535.9 (KHTML, like Gecko) Chrome/55.0.3371.211 Safari/535", 

"Mozilla/5.0 (U; Linux i582 x86_64) Gecko/20100101 Firefox/53.0",

"Mozilla/5.0 (Windows; U; Windows NT 6.1; WOW64; en-US) Gecko/20130401 Firefox/50.4",

"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_3_7; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/51.0.3576.209 Safari/536", 

"Mozilla/5.0 (compatible; MSIE 7.0; Windows; Windows NT 6.2;; en-US Trident/4.0)", 

"Mozilla/5.0 (compatible; MSIE 7.0; Windows; Windows NT 10.2; x64 Trident/4.0)",

"Mozilla/5.0 (Linux; Android 4.3.1; SAMSUNG SGH-N095V Build/JSS15J) AppleWebKit/535.48 (KHTML, like Gecko) Chrome/47.0.3733.118 Mobile Safari/603.5",

"Mozilla/5.0 (Linux i643 ) AppleWebKit/600.9 (KHTML, like Gecko) Chrome/53.0.3687.375 Safari/533", 

"Mozilla/5.0 (Windows; Windows NT 10.3; x64) AppleWebKit/533.37 (KHTML, like Gecko) Chrome/55.0.1082.221 Safari/535",

"Mozilla/5.0 (Linux; Linux x86_64; en-US) AppleWebKit/536.25 (KHTML, like Gecko) Chrome/54.0.1316.386 Safari/535", 

"Mozilla/5.0 (Windows; Windows NT 10.3;) AppleWebKit/600.28 (KHTML, like Gecko) Chrome/49.0.3547.134 Safari/601.3 Edge/15.55517", 

"Mozilla/5.0 (U; Linux x86_64; en-US) Gecko/20100101 Firefox/65.0", 

"Mozilla/5.0 (compatible; MSIE 8.0; Windows; U; Windows NT 6.3; Win64; x64 Trident/4.0)",

"Mozilla/5.0 (Windows; U; Windows NT 6.2; WOW64; en-US) AppleWebKit/536.21 (KHTML, like Gecko) Chrome/51.0.1829.390 Safari/600",

"Mozilla/5.0 (Linux; Android 4.4.1; HTC One0P6B Build/KTU84L) AppleWebKit/537.50 (KHTML, like Gecko) Chrome/53.0.2808.378 Mobile Safari/603.8",

"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; en-US Trident/6.0)",

"Mozilla/5.0 (Linux; U; Linux x86_64; en-US) AppleWebKit/534.18 (KHTML, like Gecko) Chrome/52.0.2295.177 Safari/602",

"Mozilla/5.0 (Windows; Windows NT 10.0; WOW64) Gecko/20100101 Firefox/60.7",

"Mozilla/5.0 (Linux; U; Linux x86_64; en-US) AppleWebKit/533.48 (KHTML, like Gecko) Chrome/52.0.2654.239 Safari/537",

"Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_2; like Mac OS X) AppleWebKit/600.45 (KHTML, like Gecko) Chrome/51.0.1577.134 Mobile Safari/601.4",

"Mozilla/5.0 (compatible; MSIE 10.0; Windows; U; Windows NT 6.3; x64; en-US Trident/6.0)",

"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; WOW64 Trident/5.0)", 

"Mozilla/5.0 (compatible; MSIE 9.0; Windows; U; Windows NT 6.2; x64 Trident/5.0)",

"Mozilla/5.0 (Windows; Windows NT 10.1; x64) AppleWebKit/533.5 (KHTML, like Gecko) Chrome/49.0.2339.235 Safari/535", 

"Mozilla/5.0 (iPhone; CPU iPhone OS 8_7_8; like Mac OS X) AppleWebKit/603.30 (KHTML, like Gecko) Chrome/53.0.1266.264 Mobile Safari/537.3",

"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_2_5) Gecko/20100101 Firefox/74.4",

"Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_9; like Mac OS X) AppleWebKit/533.36 (KHTML, like Gecko) Chrome/52.0.1924.202 Mobile Safari/534.2",

"Mozilla/5.0 (iPhone; CPU iPhone OS 9_6_5; like Mac OS X) AppleWebKit/601.32 (KHTML, like Gecko) Chrome/47.0.1396.160 Mobile Safari/603.6",

"Mozilla/5.0 (Windows; Windows NT 10.3;) AppleWebKit/535.12 (KHTML, like Gecko) Chrome/53.0.2326.180 Safari/535", 

"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_12_8; en-US) AppleWebKit/601.36 (KHTML, like Gecko) Chrome/52.0.3570.201 Safari/533",

"Mozilla/5.0 (Android; Android 4.4; SAMSUNG SM-N8000 Build/JZO54K) AppleWebKit/535.45 (KHTML, like Gecko) Chrome/49.0.1536.175 Mobile Safari/602.1", 

"Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_8; like Mac OS X) AppleWebKit/535.37 (KHTML, like Gecko) Chrome/53.0.2432.291 Mobile Safari/600.4",

"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 8_3_8; en-US) AppleWebKit/602.41 (KHTML, like Gecko) Chrome/48.0.3137.273 Safari/600", 

"Mozilla/5.0 (Linux; U; Android 5.0.1; LG-D330 Build/LRX22G) AppleWebKit/603.30 (KHTML, like Gecko) Chrome/47.0.1785.169 Mobile Safari/602.2", 

"Mozilla/5.0 (compatible; MSIE 9.0; Windows; U; Windows NT 10.3; Trident/5.0)", 

"Mozilla/5.0 (iPhone; CPU iPhone OS 9_4_3; like Mac OS X) AppleWebKit/601.45 (KHTML, like Gecko) Chrome/52.0.1469.262 Mobile Safari/534.6",

"Mozilla/5.0 (Macintosh; Intel Mac OS X 8_8_2; en-US) Gecko/20100101 Firefox/56.7", 

"Mozilla/5.0 (U; Linux x86_64; en-US) AppleWebKit/537.19 (KHTML, like Gecko) Chrome/48.0.2082.121 Safari/601", 

"Mozilla/5.0 (Linux i564 x86_64; en-US) AppleWebKit/536.49 (KHTML, like Gecko) Chrome/52.0.2250.196 Safari/601",

"Mozilla/5.0 (iPod; CPU iPod OS 8_4_5; like Mac OS X) AppleWebKit/536.16 (KHTML, like Gecko) Chrome/54.0.1684.395 Mobile Safari/603.6",

"Mozilla/5.0 (Windows; U; Windows NT 10.1; WOW64; en-US) AppleWebKit/603.14 (KHTML, like Gecko) Chrome/49.0.3085.215 Safari/535.2 Edge/12.31999", 

"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_5; en-US) AppleWebKit/600.43 (KHTML, like Gecko) Chrome/47.0.2844.290 Safari/600",
]

def do_job(target_str,configing):
    """Main thread"""
    result_dict = {}
    print("Start collection")
    print("    ----")
    print("    Start collection: Feed")
    print("        Feed: grab rss feed")
    headers = {'User-Agent': random.choice(user_agents)} 
    print("            Header: {}".format(headers['User-Agent']))
    rss_req = requests.get(configing.rss,timeout=60,headers=headers)
    rss_req.encoding = 'utf-8'
    print("        Feed: convert XML and update dictionary")
    rss_feed = bs(rss_req.content,"xml")
    rss_dict = {}
    description_dict = {}
    date_dict = {}
    name2url_dict = {}
    url_to_file_dict = {}
    if pathlib.Path(f"record/{target_str}/record/image.toml").exists():
        img_doc = rtoml.load(open(f"record/{target_str}/record/image.toml",encoding="utf8"))
        name2url_dict.update(img_doc["name2url"])
        url_to_file_dict.update(img_doc["url2file"])
    img_size_list = [96,128,192,256,384,512]
    if pathlib.Path(f"record/{target_str}/record/description.toml").exists():
        description_path = f"record/{target_str}/record/description.toml"
        description_dict.update(rtoml.load(open(description_path,encoding="utf8")))
    try:
        channel_cover_str = rss_feed.find("image").url.contents[0]  # type: ignore
    except:
        channel_cover_str = ""
    if channel_cover_str == "":
        print("        Access Denied to the server")
        print("    Terminated collection: Feed")
    else:
        for unit in rss_feed.find_all('item'):
            try:
                name = unit.title.contents[0]
            except:
                name = ""
            if name == "":
                unit_title = unit.get('title')
                if unit_title:
                    print(f"        invalid items: {unit_title}")
                else:
                    print("        invalid items")
            else:
                name = unit.title.contents[0]
                url = unit.enclosure['url']
                unit_description = unit.description
                contents = unit_description.contents
                description = str(contents[0]) if len(contents) > 0 else ""
                rss_dict[name] = url
                if name not in description_dict:
                    description_dict[name] = description
                original_time_str = unit.pubDate.contents[0].replace('GMT', '+0000')
                mthfmt_str = "%a, %d %b %Y %H:%M:%S %z"
                date_str = datetime.strptime(original_time_str,mthfmt_str).strftime("%b %d, %Y")
                date_dict[name] = date_str
                img_list = [ufa["href"] for ufa in unit.find_all('itunes:image')] + [channel_cover_str]
                img_url = str(img_list[0])
                name2url_dict[name] = img_url
                path_name_str = pathlib.Path(img_url).parent.name
                file_name_str = pathlib.Path(img_url).name
                safe_img_url = F"{path_name_str}-{file_name_str}"
                if safe_img_url not in url_to_file_dict:
                    print(F"request: {img_url} for '{name}'")
                    cover_img_r = requests.get(img_url,stream=True,timeout=60,headers=headers)
                    # content_type = cover_img_r.headers.get('Content-Type')
                    sleep_time = random.uniform(1, 2)
                    print(f"        sleep: {sleep_time}")
                    time.sleep(sleep_time)
                    try:
                        cover_img_r.raw.decode_content = True
                        img_file = BytesIO(cover_img_r.content)
                        cover_img = Image.open(img_file)
                        h_name = hashlib.new('sha256')
                        h_name.update(cover_img.tobytes())
                        img_name = h_name.hexdigest()
                    except:
                        print("            Access Denied to the file")
                        print("            Use default img instead")
                        img_name = "bbd140bc8bd041b0f1a6a2fc204e6d1024efe2f0e99bf9d5ad052d540df0272b"
                    url_to_file_dict[safe_img_url] = img_name
                    if not pathlib.Path(F"docs/p/{img_name}/512.png").exists():
                        print(F"resize: docs/p/{img_name}")
                        for img_size in img_size_list:
                            pathlib.Path(F"docs/p/{img_name}/").mkdir(parents=True,exist_ok=True)
                            wpercent = img_size / float(cover_img.size[0])
                            hsize = int((float(cover_img.size[1]) * float(wpercent)))
                            cover_img_res = cover_img.resize((img_size, hsize), Image.Resampling.LANCZOS)
                            cover_img_res.save(F"docs/p/{img_name}/{img_size}.png")
        result_dict["feed"] = rss_dict
        configing.xmlw(rss_req.text,"/record/feedPodcastRequests.xml")
        configing.toml(rss_dict,"/record/feedPodcast.toml")
        configing.toml(date_dict,"/record/feedPodcast-month.toml")
        configing.toml(description_dict,"/record/description.toml")
        configing.toml({"name2url":name2url_dict,"url2file":url_to_file_dict},"/record/image.toml")
        print("    Finish collection: Feed")
    #
    if configing.apple != "":
        print("    ----")
        print("    Start collection: Apple")
        print("        Feed: grab rss feed")
        apple_req = requests.get(configing.apple,timeout=60)
        apple_req.encoding = 'utf-8'
        print("        Feed: convert HTML and update dictionary")
        apple_track = bs(apple_req.content,"lxml").find('ol',{'class':'tracks tracks--linear-show'})
        if pathlib.Path(f"record/{target_str}/record/ApplePodcast.toml").exists():
            apple_doc = rtoml.load(open(f"record/{target_str}/record/ApplePodcast.toml",encoding="utf8"))
            apple_record = {str(x):str(y) for x,y in apple_doc.items()}
        else:
            apple_record = {}
        apple_dict = {}
        apple_tag = {"class":"link tracks__track__link--block"}
        for unit in apple_track.find_all('a',apple_tag):  # type: ignore
            name_wt_hidden = unit.contents[0].replace(" &ZeroWidthSpace;","")
            name_single = name_wt_hidden.replace("\n","")
            name = " ".join([n for n in name_single.split(" ") if n != ""])
            url = unit['href']
            if name in apple_record.keys():
                if apple_record[name] != url:
                    print("ERROR: Duplicate entry no consistent, value:", url, apple_record[name])
            else:
                apple_dict[name] = url
        apple_dict.update(apple_record)
        result_dict["apple"] = apple_dict
        configing.xmlw(apple_req.text,"/record/ApplePodcastRequests.html")
        configing.toml(apple_dict,"/record/ApplePodcast.toml")
        print("    Finish collection: Apple")
    #
    if configing.google != "":
        print("    ----")
        print("    Start collection: Google")
        print("        Feed: grab rss feed")
        google_req = requests.get(configing.google,timeout=60)
        google_req.encoding = 'utf-8'
        google_track = bs(google_req.content,"lxml").find('div',{'jsname':'quCAxd'})
        print("        Feed: convert HTML and update dictionary")
        if pathlib.Path(f"record/{target_str}/record/GooglePodcast.toml").exists():
            google_doc = rtoml.load(open(f"record/{target_str}/record/GooglePodcast.toml",encoding="utf8"))
            google_record = {str(x):str(y) for x,y in google_doc.items()}
        else:
            google_record = {}
        google_dict = {}
        for unit in google_track.find_all('a'):  # type: ignore
            url = unit['href'].split("?sa=")[0].replace("./","https://podcasts.google.com/")
            name = unit.findChildren("div", {'class': 'e3ZUqe'})[0].contents[0]
            if name in google_record.keys():
                if google_record[name] != url:
                    print("ERROR: Duplicate entry no consistent, value:", url, google_record[name])
            else:
                google_dict[name] = url
        google_dict.update(google_record)
        result_dict["google"] = google_dict
        configing.xmlw(google_req.text,"/record/GooglePodcastRequests.html")
        configing.toml(google_dict,"/record/GooglePodcast.toml")
        print("    Finish collection: Google")
    #
    if configing.spotify != "":
        print("    ----")
        print("    Start collection: Spotify")
        spotify_toml_name = f"record/{target_str}/record/SpotifyPodcast.toml"
        if pathlib.Path("secret.toml").exists():
            print("        Feed: grab rss feed")
            secret_docs = rtoml.load(open("secret.toml",encoding="utf8"))
            spotify_auth_url = 'https://accounts.spotify.com/api/token'
            spotify_config = {
                'grant_type': 'client_credentials',
                'client_id': secret_docs['spotify_id'],
                'client_secret': secret_docs['spotify_secret'],
            }
            spotify_auth_response = requests.post(spotify_auth_url,spotify_config,timeout=60)
            spotify_auth_response_dict = spotify_auth_response.json()
            spotify_access_token = spotify_auth_response_dict['access_token']
            spotify_url = configing.spotify
            spotify_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": F"Bearer {spotify_access_token}",
            }
            spotify_req = requests.get(spotify_url,headers=spotify_headers,timeout=60)
            spotify_req.encoding = 'utf-8'
            configing.xmlw(spotify_req.text,"/record/SpotifyPodcastRequests.json")
            print("        Feed: convert JSON and update dictionary")
            spotify_req_dict = json.loads(spotify_req.content)
            if pathlib.Path(spotify_toml_name).exists():
                spotify_doc = rtoml.load(open(spotify_toml_name,encoding="utf8"))
                spotify_record = {str(x):str(y) for x,y in spotify_doc.items()}
            else:
                spotify_record = {}
            spotify_dict = {}
            for unit_dict in spotify_req_dict["items"]:
                sp_dict = {}
                sp_dict[0] = "https://api.spotify.com/v1/episodes/"
                sp_dict[1] = "https://open.spotify.com/episode/"
                url = unit_dict['href'].replace(sp_dict[0],sp_dict[1])
                name_wt_hidden = unit_dict['name'].replace(" &ZeroWidthSpace;","")
                name_single = name_wt_hidden.replace("\n","")
                name_str = " ".join([n for n in name_single.split(" ") if n != ""])
                if name_str in spotify_record.keys():
                    record_name = spotify_record[name_str]
                    if record_name != url:
                        print(F"ERROR: Duplicate entry no consistent, value: {url} {record_name}")
                else:
                    spotify_dict[name_str] = url
            spotify_dict.update(spotify_record)
            result_dict["spotify"] = spotify_dict
            configing.toml(spotify_dict,"/record/SpotifyPodcast.toml")
        else:
            print("        Skip: secret not found")
            print("        Feed: use old records")
            if pathlib.Path(spotify_toml_name).exists():
                spotify_doc = rtoml.load(open(spotify_toml_name,encoding="utf8"))
                spotify_record = {str(x):str(y) for x,y in spotify_doc.items()}
            else:
                spotify_record = {}
            spotify_dict = {}
            spotify_dict.update(spotify_record)
            result_dict["spotify"] = spotify_dict
        print("    Finish collection: Spotify")
    #
    if configing.youtube != "":
        print("    ----")
        print("    Start collection: YouTube")
        print("        Feed: grab rss feed")
        youtube_req = requests.get(configing.youtube,timeout=60)
        youtube_req.encoding = 'utf-8'
        youtube_track = bs(youtube_req.content,"xml")
        print("        Feed: convert XML and update dictionary")
        if pathlib.Path(f"record/{target_str}/record/YouTube.toml").exists():
            youtube_doc = rtoml.load(open(f"record/{target_str}/record/YouTube.toml",encoding="utf8"))
            youtube_record = {str(x):str(y) for x,y in youtube_doc.items()}
        else:
            youtube_record = {}
        youtube_dict = {}
        for unit in youtube_track.find_all('entry'):
            name = unit.title.contents[0]
            url = unit.link['href']
            if name in youtube_record.keys():
                if youtube_record[name] != url:
                    print("ERROR: Duplicate entry no consistent, value:", url, youtube_record[name])
            else:
                youtube_dict[name] = url
        youtube_dict.update(youtube_record)
        result_dict["youtube"] = youtube_dict
        configing.xmlw(youtube_req.text,"/record/YouTubeRequests.xml")
        configing.toml(youtube_dict,"/record/YouTube.toml")
        print("    Finish collection: YouTube")
    #
    configing.toml(result_dict,"/mid/history.toml")
    print("    ----\nFinish collection")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update data")
    parser.add_argument("target", help="target path")
    args = parser.parse_args()
    configin = configdo.ConfigCla(args.target)  # type: ignore
    do_job(args.target,configin)
