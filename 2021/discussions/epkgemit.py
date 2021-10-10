"""epkgemit.py  -- entity package emitter

Emit Entity Packages, and read from a simplified form.

This uses the Entity Package system developed around 2021-09-28,
the characteristics of which include:

* all-lower case keys
* links & facets separate
* moreinfo is a facet

This module creates entity packages.
"""

import datetime
import uuid
import pprint
import json


# Read a JSON file

def read_json(p):
    return json.load(open(p, "r", encoding="utf-8"))

def write_json(obj, p):
    json.dump(obj, open(p, "w", encoding="utf-8"), indent=2)


# Basic Info

basic_info = read_json("basic_info.json")

def findpath(alias):
    return basic_info["paths"][alias]

def longname(s):
    return basic_info["short-names"].get(s, s)

# (patch sources entry)
basic_info["sources"] = {longname(k): longname(v)
                         for k,v in basic_info["sources"].items()}


# Globals

LISTINGORDER = "LISTINGORDER"  # currently selected listing order list

g = {LISTINGORDER: None}


# Constants -- Package Files

K_FILETYPE = "$filetype"
K_PKGID = "$pkgid"
K_RECORDS = "$records"


# Constants -- Records

K_SCHEMA = "$schema"
K_TYPE = "$type"
K_ID = "$id"

TYPE_LINK = "link"
TYPE_FACET = "facet"


# Constants -- Tag Authorities

AUTH_EPKG = "entitypkg.net"
AUTH_EPKG_DATE = "2022"
AUTH_LION = "lionkimbro@gmail.com"

TODAY = datetime.datetime.utcnow().date().isoformat()


# Constants -- Schema (SCH_)

SCH_SOURCE = longname("sch_source")
SCH_GENERIC = longname("sch_generic")
SCH_ARTICLE = longname("sch_article")
SCH_ARTICLES_LIST = longname("sch_articles_list")
SCH_ARTICLE_AUTHOR = longname("sch_article_author")


# Shadow Binding  -- used in packing routines

S = [{}]

python_set = set

def set(k, v):
    """NOTE!!  PERFORMS LONG NAME SUBSTITUTION ON ENTRY!"""
    S[-1][k] = longname(v)

def get(k):
    for D in reversed(S):
        if k in D:
            return D[k]
    raise KeyError(k)

def bind(D):
    """NOTE!! PERFORMS LONG NAME SUBSTITUTION ON ENTRY!"""
    for k in D:
        S[-1][k] = longname(D[k])

def push(D={}):
    S.append({})
    bind(D)

def pop(): return S.pop()


# Functions -- Identifier Construction

def new_uuid():
    return uuid.uuid4().urn

def tag(authority, datestr, content):
    return "tag:"+authority+","+datestr+":"+content

def spectag(content):
    return tag(AUTH_EPKG, AUTH_EPKG_DATE, content)

def liontag(datestr, content):
    return tag(AUTH_LION, datestr, content)


# Functions -- Packing the Package

pkg = {}  # The package being assembled.

def package():  # req: PACKAGE_ID
    pkg.clear()
    pkg.update({K_FILETYPE: longname("filetype_pkg"),
                K_PKGID: get("PKGID"),
                K_RECORDS: []})

def show():
    pprint.pprint(pkg)


content = {}  # the content of a new record

def cue_listing_order():  # req: $SCHEMA
    for D in basic_info["listing-order"]:
        if longname(D["schema"]) == content[K_SCHEMA]:
            g[LISTINGORDER] = D["order"]
            return
    raise KeyError("cannot cue listing order:", content["$schema"])

def add():  # add the listing record to the package, then clear it
    D = {}
    cue_listing_order()  # order the keys, referencing the schema
    for k in g[LISTINGORDER]:
        D[k] = content[k]
    pkg[K_RECORDS].append(D)
    content.clear()


# (these are position-based dictionary constructors)
D_id = lambda ID: locals()  # use with bind()
D_schema = lambda SCHEMA: locals()
D_schema_id = lambda SCHEMA, ID: locals()

def schema_and_id():  # req: ID, SCHEMA
    content[K_ID] = get("ID")
    content[K_SCHEMA] = get("SCHEMA")
    add()

def facet():  # req: ID, SCHEMA
    content[K_TYPE] = TYPE_FACET
    schema_and_id()

def link():  # req: ID, SCHEMA
    content[K_TYPE] = TYPE_LINK
    schema_and_id()


def generic():  # req: ID, TITLE, TYPE
    set("SCHEMA", SCH_GENERIC)
    content["title"] = get("TITLE")
    content["type"] = get("TYPE")
    facet()

def person():  # req: ID, TITLE
    set("TYPE", "a person")
    generic()

def feed():  # req: ID, TITLE
    set("TYPE", "a feed")
    generic()

def feedlinks(articles):  # req: ID (for the link!!!), SCHEMA (link!), FEED id
    content["feed"] = get("FEED")
    content["articles"] = articles  # a list of ids of articles
    link()

def article():  # req: ID, AUTHOR, HTML, RAW, HOOK, POSTED
    set("SCHEMA", SCH_ARTICLE)
    # Remember, the author is noted via link, not a facet
    content["html"] = get("HTML")
    content["raw"] = get("RAW")
    content["hook"] = get("HOOK")
    content["posted"] = get("POSTED")
    facet()

def article_author():  # req: ID (generally a UUID), an ARTICLE, and an AUTHOR
    set("SCHEMA", SCH_ARTICLE_AUTHOR)
    content["article"] = get("ARTICLE")
    content["author"] = get("AUTHOR")
    link()

def source():  # req: ID (the thing), SOURCE (where to find it)
    set("SCHEMA", SCH_SOURCE)
    content["source"] = get("SOURCE")
    facet()


# Functions -- Tracking Schema & Entity Identifiers

def all_schema():
    seen = []
    for rec in pkg[K_RECORDS]:
        if K_SCHEMA in rec:
            s = rec[K_SCHEMA]
            if s not in seen:
                seen.append(s)
    return seen

def all_id():
    """Return all Entity Identifiers seen.
    
    That includes:
    * the package ID
    * the ID of each facet record
    * the ID of each link record
    * all non-terminals in link records
    
    This is part of locating candidates for moreinfo.
    """
    seen = {pkg[K_ID]}
    for rec in pkg[K_RECORDS]:
        if K_ID in rec:
            seen.add(rec[K_ID])
        if rec[K_TYPE] == TYPE_LINK:
            for terminal in all_linkrecord_terminals(rec):
                seen.add(terminal)


def _helper_00(obj):
    seen = python_set()
    is_dict = isinstance(obj, dict)
    for x in obj:
        val = obj[x] if is_dict else x
        if isinstance(val, str):
            seen.append(obj)
        else:
            seen.update(__helper_00(val))  # recurse in
    return seen

def all_linkrecord_terminals(rec):
    """Return all ID terminals for a link record.
    
    The special thing about link records, is that their terminals are
    ALL entity identifiers.
    
    This function is a subroutine of all_id, which needs to collect
    the terminals from all link records, in order to inventory all
    entity identifiers referenced.
    
    Note the following special keys:
    * K_SCHEMA ($schema)  -- INCLUDED (Entity Identifier)
    * K_TYPE ($type)  -- EXCLUDED (*not* an Entity Identifier)
    * K_ID ($id)  -- INCLUDED (Entity Identifier; namely: self)
    """
    D = dict(rec)
    del D[K_TYPE]
    return _helper_00(D)


# Assembly Line Processing

article_src = read_json(findpath("in_articles"))

uuids = read_json(findpath("inout_uuids"))


def stored_uuid(key, for_identifier):
    D = uuids[key]
    if for_identifier not in D:
        D[for_identifier] = new_uuid()  # it'll be saved later
    return D[for_identifier]


def create_lions_internet_office_articles_entitypkg():
    # Create Package
    breakpoint()
    push(basic_info["package"]); package(); pop()

    # 1. feed
    
    # 1.A. generate the feed
    push(basic_info["feed"])
    feedid = get("ID")  # save for when creating the feed-article link
    feed()
    pop()
    
    # 1.B. Create sequential identifiers for the articles
    for (i, D) in enumerate(article_src):
        D["ID"] = longname("article-prefix")+str(i)
    
    # 1.C. generate feed links
    articles = [D["ID"] for D in article_src]
    push({"ID": "link_feed_to_articles",
          "SCHEMA": "sch_feed_to_articles",
          "FEED": feedid})
    feedlinks(articles)
    pop()

    # 2. people

    for person_info in basic_info["people"]:
        push(person_info); person(); pop()

    # 3. articles

    for article_info in article_src:
        push(article_info)
        article()
        set("ARTICLE", get("ID"))  # keep the ID in ARTICLE when rendering the author link
        set("ID", stored_uuid("article-to-author-uuids", get("ARTICLE")))
        article_author()
        pop()

    # 4. sources

    L = all_schema()
    L.append(SCH_SOURCE)
    for schema in L:
        push()
        set("ID", schema)
        set("SOURCE", basic_info["sources"][get("ID")])
        source()
        pop()
    
    # Done -- Write Out
    write_json(pkg, findpath("out_articles"))
    
    # Save UUID records, too:
    write_json(uuids, findpath("inout_uuids"))


def run():
    create_lions_internet_office_articles_entitypkg()


if __name__ == "__main__":
    run()

