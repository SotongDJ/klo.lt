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

user_agents = json.load(open("agent.json"))

def trim_url(url_str):
    output_str = ""
    target_dict = {
        ".mp3?timestamp=":".mp3",
        ".mp3?v=":".mp3",
    }
    for target_split, target_ext in target_dict.items():
        if output_str == "":
            url_list = url_str.split(target_split)
            if len(url_list) == 2:
                output_str = "{}{}".format(url_list[0],target_ext)
    if output_str == "":
        return url_str
    else:
        return output_str

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
                url = trim_url(unit.enclosure['url'])
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
        # if configing.apple != "":
        if 0 == 1:
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
