# The Generic Thing
Lion Kimbro
2021-09-13 (amended 2021-09-30)

## <a name="context">Context</a>

While working on [the Entity-Focal Data Package idea](https://github.com/LionKimbro/lions_internet_office/blob/main/2021/users/lion/entries/2021-09-13_entity-focal-data-package.md), I realized that it'd be nice to have a placeholder generic "thing" that could be linked to.

It essentially means:  "Yes, -- it'd be nice if there were a thing at the target address that had a schema and was organized and such, but maybe there isn't such a thing yet.  So here's a generic thing you might be able to use instead."

And it occurred to me -- what kinds of data would you want in "a generic thing" ..?

## <a name="prototype">Prototype</a>

I think I'd include the following pieces of data in a generic "thing."

* **SCHEMA** -- *the schema identifier for The Generic Thing* (`tag:entitypkg.net,2022:entity-schema:generic-v1`)
* **EID** -- *the entity identifier for the thing*
* **LANG** -- *2-character (en) or 5-character (en-US) language code for human readable strings*
* **TYPE** -- *a "just folks" human readable denotation of the type of the thing; NOT a unique ID -- ex: "a Person", "a Feed", "a URL", "a File"*
* **TITLE** -- *human readable title*
* **HOOK**-- *human readable string, something about why this is here; more a phrase than a sentence -- hooks are used in summary presentations or browsing*
* **DESCRIPTION** -- *roughly 3-5 sentences describing the thing, but really no limit*
* **IMAGE** -- *url to an image of the thing, or otherwise associated with the thing*
* **TAGS** -- *various textual tags (just strings, not unique IDs) attached to the thing*
* **URL** -- *url associated with the entity*
* **CREATED** -- *date that the entity was created*
* **DATE** -- *date that the entity notes (particular to the thing)*
* **DATA** -- *additional data, attached beneath, by whatever format desired*
* **CONTENT** -- *a string of "content," whatever that means*
* **BINARY** -- *a set of bytes of binary content, whatever that means*

All of these dimensions are optional -- they could be defined or not defined.

The data kept inside of a "generic thing" is deliberately ambiguous.  This is about about wandering a path in a forest, or chopping wood and making a log cabin, more than it is about a Tokyo railway station.


## Changed 2021-09-30

* specified tag uri for The Generic Thing's schema
* ID -> "EID"
* added "IMAGE"
* changed "locating" to "annotating" on tags, because there are a many reasons you'd want to tag something, not just locating
* minor clarification of intent -- this is deliberately an informal structure

