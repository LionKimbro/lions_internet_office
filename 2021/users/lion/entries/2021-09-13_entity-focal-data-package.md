# Entity-Focal Data Package

Lion Kimbro
2021-09-12

I'm kicking around a data package format that looks something like this:

* **self-declaration**: "This document has UUID such-and-such."  Tag URIs are my favorite.
* **entities**: a list of entities, and the data associated with them; all data is essentially keyed by its UUID
* **more info**: a list of further sources of information, each source is associated with the UUIDs that the reader of this document might be interested in learning more about

"**Entity**" here means a unit of data that a formalized universally unique identifier has been chosen for.  That identifier could be (say) a UUID such as "`93a059af-01f9-4d2c-af61-76e9a75c2ebd`", it could be a tag URI such as "`tag:lionkimbro@gmail.com,2021-09-12:example:i-just-made-up-off-the-top-of-my-head`".  (I'm using this definition as an after-shock of my conversations with Ciprian Craciun.)

We can imagine something like:

    {"SELF": "tag:lionkimbro@gmail.com,2021-09-12:example:data-bundle",
     "ENTITIES":
       {"tag:lionkimbro@gmail.com,2021-09-12:example:data-bundle": {...},
        "tag:lionkimbro@gmail.com,2021-09-12:example:item-1": {...},
        "tag:lionkimbro@gmail.com,2021-09-12:example:item-2": {...},
        ...
        "tag:lionkimbro@gmail.com,2021-09-12:example:item-n": {...}},
     "MOREINFO":
      [{"SOURCE": "http://example.net/foo/...",
        "DESCRIBES": ["tag:lionkimbro@gmail.com,2021-09-12:example:item-13",
                      "tag:lionkimbro@gmail.com,2021-09-12:example:item-14"]},
       {"SOURCE": "http://example.net/bar/...",
        "DESCRIBES": [tag:lionkimbro@gmail.com,2021-09-12:example:item-2",
                      ...]},
       ...]
    }

The library that consumes this information would not only gather information about "entities," but further would be able to spider for further information from elsewhere on the Internet.  And it would return this information not just as "Here's the data about the entity," but morever, "Here's the data about the entity from this specific source, here's the data about the entity from this other specific source, and here's the data about this entity from still another specific source."

It is incumbent on the programmer to figure out how to handle the differing accounts.  Perhaps the programmer will decide to unify the data, perhaps the programmer will offer it to the user to decide, perhaps the programmer will decide to pick one of the data sources.  But that is not determined by the protocol; It is decided by the programmer.  The protocol only offers the varying accounts of the entity to the programmer.

## <a name="questions">Some Questions</a>

A number of questions come to me.
* [How is data published?](#q1)
* [Should the MOREINFO block go from source to UUIDs, or from UUIDs to sources?](#q2)
* [Does this actually benefit us in any way?](#q3)
* [Should trust levels be recorded?](#q4)
* [Should there be a short-cuts block?](#q5)
* [Are identifiers keys, or unique identifiers of unique blocks of data?](#q6)

## <a name="q1">Q1. How is Data Published?</a>

I'm assuming that a program goes through the following cycle:
1. The program retrieves data from a file, and from the Internet, and then assembles it.
2. The user browses the data, and then, on finding some interesting things, makes some changes to the data.
3. The user tells the program to save the data.

What happens here?
* Does the program save all of the data it has accumulated, and include the manipulations from the user?
* Does the program only save the data for the entities that the user manipulated?
* Does the program save only the manipulations that the user introduced to the data?
* How does the program issue the question to the user, about how to save the data?  How does the program explain to the user the distinction, so that the user can make a responsible decision?
* How about the "More Info" blocks -- does every "More Info" that the program learned about go in there?  Or does the program rely on other sources providing their parts of "More Info" ..?
* If only the manipulations that the user introduced to the data are stored, how do other programs know to layer it "on top" of other data, rather than "underneath" other data?
* (Or should data be distributed as changesets?)

The answers to these questions are not immediately apparent to me.

It seems even more important to me, though, that correct attribution needs to be maintained by the library.  Not just for the entities information, but for the More Info blocks as well.

On the conservative side, the approach would be:  that the manipulations that are introduced by the user need to be kept separate from the source data, and that the minimum number of "More Info" blocks should be given.  If the user started with a single source bundle, (which then led to spidering to further information,) then just that single source bundle's location should be shared in the saved file as the sole "More Info" segment.

The most liberal approach would be to simply save everything assembled  I would fear making a machine for inducing copyright violation on a massive scale, however.  (see also: [Wikipedia: Database Rights.](https://en.wikipedia.org/wiki/Database_right))

## <a name="q2">Q2. Should the MOREINFO block go from source to UUIDs, or from UUIDs to sources?</a>

This is not a hugely consequential question, but I hold it.  Given that a single source describes multiple UUIDs, it would seem that it should go from source to UUID.  However, given that the most common use case is that the program wants to know more about a given UUID, it would seem it should go the other way around.

It doesn't matter because the software can index in any direction.

## <a name="q3">Q3. Does this actually benefit us in any way?</a>

I mean, "Sure, of course," -- but, -- when I look at an RSS feed, or something like that, I don't see an immediate or obvious benefit.

The consumer of an RSS feed gets a data structure that is tailor made bespoke to the re-presentation of a feed.

But imagine if that RSS feeds entries were bundled up in this data structure.  What benefit is actually coming to the consumer of the feed?

It's hard to justify the switch, if there's no visible benefit.

For RSS, the benefit has got to be some additional information that was not there before.

Here are some RSS feed elements, and how they can be expanded:
* **email address** of author, managing editor, webmaster, ... -- reference not only the email address, but the person themself (at least in their particular role) as well
* **category** -- name a specific unique identifier for the category, not just a string -- upon retrieval of information about the category, super-categories and sub-categories may be discovered and browsable as well, as well as information about other articles on that category, and from multiple sources

It also occurs to me that several elements can be taken *out*.  For example, information about the "channel" can be located in a separate document.  The data store can be fragmented, and given more detail elsewhere.


## <a name="q4">Q4. Should trust levels be recorded?</a>

I've internally debated whether the "more info" section should depict a degree of trust or mistrust in the further entities, and whether the internal data model should keep track of that trust or distrust.

I like the idea of modeling trust vs. distrust, so that provisional data, data under review, data that the user itself may decide "Trust this source," -- can be included fairly easily, rather than just accepted or rejected.

That said, it is an additional complexity, and it is unlikely to be immediately useful.

## <a name="q5">Q5. Should there be a shortcuts block?</a>

Let's face it -- identifiers are long, and liable to be oft-repeated.
It makes sense to me that there would be short-cutting methods for identifiers.

Before, I was working on [a concept called XUUIDs,](https://github.com/LionKimbro/xuuid) which are something like "UUIDs with a lot of information about them."  One of those pieces of information associated with an identifier, was preferred short-hand notations for that identifier.

I don't see any reason why there can't be records for identifiers themselves.

Are those records normal records, stored in (following with the opening example) `ENTRIES`..?

Or do they have their own section, perhaps: `SHORTCUTS` ..?
Is there an escaping mechanism for shortcuts?  Or do they apply globally throughout the document wherever there is a standalone string that exactly matches the shortcut?  That seems like trouble.

The best option it seems to me would to be to declare shortcuts only where they are unambiguously replacements for full URIs.  That would be in the keys for `ENTRIES`, and in the `MOREINFO` block, where they are liable to occur repeatedly.

I don't want to neglect, however, that the containing program may find utility in shortcuts as well, or the programmer debugging the containing program.

## <a name="q6">Q6. Are identifiers keys, or unique identifiers of unique blocks of data?</a>

There are conceivably several things we might want to share about `tag:lionkimbro@gmail.com,2021-09-12:example:item-1`.

What if the data point can be interacted with from multiple points of view?
* Conflicting ideas about the entity.
* Different views or dimensions of the entity.

I think I welcome this approach of multiple annotation.

It does suggest to me, however, that when data is packaged, then, it cannot simply be done like so:

     "ENTITIES":
       {"tag:lionkimbro@gmail.com,2021-09-12:example:data-bundle": {...},
        "tag:lionkimbro@gmail.com,2021-09-12:example:item-1": {...},
        "tag:lionkimbro@gmail.com,2021-09-12:example:item-2": {...},
        ...
        "tag:lionkimbro@gmail.com,2021-09-12:example:item-n": {...}},

...because the ENTITIES dictionary only allows a UUID to be associated with a single value.

Instead, it would need to be associable with multiple values -- multiple comments about the single UUID.  Each key links to a list of definitions, rather than always only a single definition.
