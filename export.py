"""Export playlist"""
import argparse
from datetime import datetime
import json
from pathlib import Path
import rtoml
import configdo

def convert_month(input_str):
    """get month tag"""
    return int(datetime.strptime(input_str,"%b %Y").strftime("%Y%m"))

def convert_date(input_str):
    """get month tag"""
    return int(datetime.strptime(input_str,"%b %d, %Y").strftime("%Y%m%d"))

def do_job(target_str):
    """Main thread"""
    print("----\nStart export")
    print("    ----")
    print("    load data")
    title_fn_str = f"record/{target_str}/mid/annotation.toml"
    title_doc = rtoml.load(open(title_fn_str,encoding="utf8"))
    keyword_fn_str = f"record/{target_str}/mid/keyword.toml"
    keyword_doc = rtoml.load(open(keyword_fn_str,encoding="utf8"))
    date_fn_str = f"record/{target_str}/record/feedPodcast-month.toml"
    date_doc = rtoml.load(open(date_fn_str,encoding="utf8"))
    dt_list = [m for m in date_doc.values()]
    bY2Y_dict = {datetime.strptime(m,"%b %d, %Y").strftime("%b %Y"):datetime.strptime(m,"%b %d, %Y").strftime("%Y") for m in date_doc.values()}
    rvs_m_dict = {} # reverse_date_dict
    for monthyear_str, year_str in bY2Y_dict.items():
        year_list = rvs_m_dict.get(year_str,[])
        year_list.append(monthyear_str)
        rvs_m_dict[year_str] = year_list
    reverse_list = sorted(list(rvs_m_dict.keys()),key=int, reverse=True)
    reverse_dict = {y:sorted(rvs_m_dict[y],key=convert_month) for y in reverse_list}
    # date_list = sorted(list(bY2Y_dict.keys()), key=convert_month, reverse=True)
    header_dict = {
        "name":"",
        "feed":"",
        "image":"",
        "tag":[],
        "description":"",
        "extra":{},
        "apple":"",
        "google":"",
        "spotify":"",
        "youtube":""
    }
    # title_list = []
    # total_int = len(title_doc.keys())
    print("    ----")
    print(f"    export docs/{target_str}-playlist")
    playlist_dict = {}
    for key_str, value_dict in title_doc.items():
        value_inner_dict = {x:value_dict.get(x,y) for x,y in header_dict.items()}
        tag_list = value_dict.get("tag",[])
        category_list = [n for n in value_dict.get("category",[]) if n[0] != "#"]
        tag_list.extend(sorted(list(set(category_list))))
        deduplicate_tag_list = []
        for tag in tag_list:
            if tag not in deduplicate_tag_list and tag not in d2Y_dict.keys():
                deduplicate_tag_list.append(tag)
        value_inner_dict["tag"] = deduplicate_tag_list
        playlist_dict[key_str] = value_inner_dict

    with open(f"docs/{target_str}-playlist.json","w") as target_handler:
        json.dump(playlist_dict,target_handler,indent=0,sort_keys=True,ensure_ascii=True)

    print("    ----")
    print(f"    export docs/{target_str}-tag_class")
    tag_to_class_dict = {x: [str(n) for n in y["category"]] for x, y in keyword_doc.items()}
    tag_to_class_dict.update({m: [F"{y}"] for m,y in bY2Y_dict.items()})

    with open(f"docs/{target_str}-tag_class.json","w") as target_handler:
        json.dump(tag_to_class_dict,target_handler,indent=0,sort_keys=True,ensure_ascii=True)

    print("    ----")
    print(f"    export docs/{target_str}-class_tag")
    class_to_tag_dict = {}
    class_to_tag_dict.update({F"{y}":m for y,m in reverse_dict.items()})
    for tag_name, entry_detail in keyword_doc.items():
        for category_name in entry_detail["category"]:
            category_list = class_to_tag_dict.get(str(category_name),[])
            category_list.append(tag_name)
            class_to_tag_dict[str(category_name)] = category_list

    with open(f"docs/{target_str}-class_tag.json","w") as target_handler:
        json.dump(class_to_tag_dict,target_handler,indent=0,sort_keys=True,ensure_ascii=True)

    print("    ----")
    print(f"    generate docs/{target_str}/index.html")
    configin = configdo.ConfigCla(args.target)
    template_str = open("template/home.html").read()
    index_html = template_str.format(title=configin.title,channel=configin.channel)
    configin.index(index_html)

    print("    ----")
    print(f"    update docs/klt-playlist.json")
    playlist_path = "docs/klt-playlist.json"
    playlist_json = json.load(open(playlist_path)) if Path(playlist_path).exists() else {}
    for key, values in playlist_dict.items():
        dt_str = [n for n in values["tag"] if n in dt_list][0]
        ymd_str = convert_date(dt_str)
        playlist_json[f"klt{ymd_str}_{key}"] = values
    with open(playlist_path,"w") as target_handler:
        json.dump(playlist_json,target_handler,indent=0,sort_keys=True,ensure_ascii=True)
    print(f"    update docs/klt-tag_class")
    tag_to_class_path = "docs/klt-tag_class.json"
    tag_to_class_json = json.load(open(tag_to_class_path)) if Path(tag_to_class_path).exists() else {}
    for key, values in tag_to_class_dict.items():
        tag_to_class_values = tag_to_class_json.get(key,[])
        tag_to_class_values.extend([n for n in values if n not in tag_to_class_values])
        tag_to_class_json[key] = tag_to_class_values
    with open(tag_to_class_path,"w") as target_handler:
        json.dump(tag_to_class_json,target_handler,indent=0,sort_keys=True,ensure_ascii=True)
    print(f"    update docs/klt-class_tag")
    class_to_tag_path = "docs/klt-class_tag.json"
    class_to_tag_json = json.load(open(class_to_tag_path)) if Path(class_to_tag_path).exists() else {}
    for key, values in class_to_tag_dict.items():
        class_to_tag_values = class_to_tag_json.get(key,[])
        class_to_tag_values.extend([n for n in values if n not in class_to_tag_values])
        class_to_tag_json[key] = class_to_tag_values
    with open(class_to_tag_path,"w") as target_handler:
        json.dump(class_to_tag_json,target_handler,indent=0,sort_keys=True,ensure_ascii=True)
    print("    ----")
    print(f"    generate docs/klt/index.html")
    template_str = open("template/home.html").read()
    index_html = template_str.format(title="All 所有",channel="klt")
    with open("docs/klt/index.html","w") as target_handler:
        target_handler.write(index_html)

    print("    ----\nEnd export")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export playlist")
    parser.add_argument("target", help="target path")
    args = parser.parse_args()
    do_job(args.target)
