"""generate.py  -- generate other versions of 2021_articles.json"""


import copy
import pprint

import json


src = json.load(open("2021_articles_simple.json", "r", encoding="utf-8"))


people = {
  "lion": "tag:lionkimbro@gmail.com,2021:person:lion",
  "ciprian.cracium": "tag:lionkimbro@gmail.com,2021:person:ciprian.cracium",
  "bouncepaw": "tag:lionkimbro@gmail.com,2021:person:bouncepaw"
}


base_2021_articles_json = {
    "$SCHEMA": "tag:lionkimbro@gmail.com,2021:schema:article-postings-list-v1",
    "$UID": "tag:lionkimbro@gmail.com,2021:lions-internet-office:publications:discussions",
    "SOURCE": "tag:lionkimbro@gmail.com,2021:source:lions-internet-office",
    "ARTICLES": []
}

part_2021_articles_json = {
    "$SCHEMA": "tag:lionkimbro@gmail.com,2021:schema:article-posting-v1",
    "AUTHORS": [],
    "HTML": None,
    "RAW": None,
    "HOOK": None,
    "POSTED": None
}


base_entitypackage_json = {
    "$SCHEMA": "tag:lionkimbro@gmail.com,2021:entity-schema:entity-package-v1",
    "$UID": "tag:lionkimbro@gmail.com,2021:entity-package:lions-internet-office-discussions-v1",
    "ENTITIES": {
        "tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:feed":
        [{"$SCHEMA": "tag:lionkimbro@gmail.com,2021:entity-schema:article-feed-v1",
          "$UID": "tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:feed",
          "TITLE": "Lion's Internet Office -- Discussions Feed",
          "ARTICLES": []}],
        
        "tag:lionkimbro@gmail.com,2021:person:lion":
        [{"$SCHEMA": "tag:lionkimbro@gmail.com,2021:entity-schema:generic-v1",
          "$UID": "tag:lionkimbro@gmail.com,2021:person:lion",
          "TITLE": "Lion Kimbro",
          "TYPE": "a person"}],

        "tag:lionkimbro@gmail.com,2021:person:ciprian.cracium":
        [{"$SCHEMA": "tag:lionkimbro@gmail.com,2021:entity-schema:generic-v1",
          "$UID": "tag:lionkimbro@gmail.com,2021:person:lion",
          "TITLE": "Ciprian Cracium",
          "TYPE": "a person"}],

        "tag:lionkimbro@gmail.com,2021:person:bouncepaw":
        [{"$SCHEMA": "tag:lionkimbro@gmail.com,2021:entity-schema:generic-v1",
          "$UID": "tag:lionkimbro@gmail.com,2021:person:bouncepaw",
          "TITLE": "BouncePaw",
          "TYPE": "a person"}]
    },
    "MOREINFO": [
        {"SOURCE": "https://raw.githubusercontent.com/LionKimbro/lions_internet_office/main/2021/data/entitypackage_basics.json",
         "DESCRIBES": ["tag:lionkimbro@gmail.com,2021:entity-schema:schema-v1", "tag:lionkimbro@gmail.com,2021:entity-schema:entity-package-v1", "tag:lionkimbro@gmail.com,2021:entity-schema:generic-v1"]},
        {"SOURCE": "https://raw.githubusercontent.com/LionKimbro/lions_internet_office/main/2021/data/entitypackage_experimentalfeeds.json",
         "DESCRIBES": ["tag:lionkimbro@gmail.com,2021:entity-schema:article-feed-v1", "tag:lionkimbro@gmail.com,2021:entity-schema:article-v1"]}
    ]
}


post_tag_prefix = "tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:post-"  # attach integer at end

part_entitypackage_json = {
    "$SCHEMA": "tag:lionkimbro@gmail.com,2021:entity-schema:article-v1",
    "$UID": None,
    "AUTHORS": [],
    "HTML": None,
    "RAW": None,
    "HOOK": None,
    "POSTED": None
}


# remember to paste into the article index



def gen_2021_articles():
    masterD = copy.deepcopy(base_2021_articles_json)
    for srcD in src:
        D = copy.deepcopy(part_2021_articles_json)
        D["AUTHORS"].append(people[srcD["AUTHOR"]])
        D["HTML"] = srcD["HTML"]
        D["RAW"] = srcD["RAW"]
        D["HOOK"] = srcD["HOOK"]
        D["POSTED"] = srcD["POSTED"]
        masterD["ARTICLES"].append(D)
    json.dump(masterD, open("2021_articles.json", "w", encoding="utf-8"), indent=2)


def gen_entitypackage1():
    """this variant uses a dictionary to communicate entities"""
    masterD = copy.deepcopy(base_entitypackage_json)
    for (index, srcD) in enumerate(src):
        new_id = post_tag_prefix+str(index)
        D = copy.deepcopy(part_entitypackage_json)
        D["$UID"] = new_id
        D["AUTHORS"].append(people[srcD["AUTHOR"]])
        D["HTML"] = srcD["HTML"]
        D["RAW"] = srcD["RAW"]
        D["HOOK"] = srcD["HOOK"]
        D["POSTED"] = srcD["POSTED"]
        masterD["ENTITIES"][new_id] = [D]
        masterD["ENTITIES"]["tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:feed"][0]["ARTICLES"].append(new_id)
    json.dump(masterD, open("eraseme.json", "w", encoding="utf-8"), indent=2)

def gen_entitypackage2():
    """this variant does not use a dictionary to list entities"""
    masterD = copy.deepcopy(base_entitypackage_json)
    masterD["ENTITIES"] = [v[0] for k,v in masterD["ENTITIES"].items()]
    for (index, srcD) in enumerate(src):
        new_id = post_tag_prefix+str(index)
        D = copy.deepcopy(part_entitypackage_json)
        D["$UID"] = new_id
        D["AUTHORS"].append(people[srcD["AUTHOR"]])
        D["HTML"] = srcD["HTML"]
        D["RAW"] = srcD["RAW"]
        D["HOOK"] = srcD["HOOK"]
        D["POSTED"] = srcD["POSTED"]
        masterD["ENTITIES"].append(D)
        masterD["ENTITIES"][0]["ARTICLES"].append(new_id)
    json.dump(masterD, open("eraseme.json", "w", encoding="utf-8"), indent=2)


def run():
    gen_2021_articles()
    gen_entitypackage1()


if __name__ == "__main__":
    run()
