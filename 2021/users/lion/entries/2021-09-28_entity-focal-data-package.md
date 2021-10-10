
# Entity-Focal Data Package

Lion Kimbro
2021-09-28
Status: Complete, Obsolete (but Still Useful) (marked 2021-10-09; see [addendum](#addendum-2021-10-09))

This document outlines further development of [the idea I explored on Sep 13.](2021-09-13_entity-focal-data-package.md)

I have further developed the concepts, and they are going in a particular direction.  This document outlines the main pieces of what is being developed, the data format as I imagine it today, and some of the major questions I am wrestling with.

<a name="brief">**In brief:**</a>  I am developing a method of packaging data, in the abstract, about the world.  It allows you to make claims about things in the world (called "Entities") through simple JSON, rather than (say) RDF triples, that should be intuitive to programmers.  It also allows you to specify where you can source further information about things in the world, if a client decides that it needs more information about something.  Information about entities are encapsulated into typed bundles called "entity data."  There is no specifically authoritative data associated with an entity, there are only packages of entity data that make claims about entities.  Links are **not** specifically modeled in this system, but can be modelled by way of entity data packages.  A given bundle of entity data can be about multiple entities, and a given bundle of entity data can belong to multiple types, as long as those types do not contradict one another.  The system comes with a collection of common, basic types, that are intended to be applied commonly, and used by a variety of tools intelligently, but their use is not required.  These basic types include:  Links (of various kinds, including "left-right" and "parent-child"), the "Generic Item" view, "attachments," "commentary."

I am doing this in frequent collaboration with a man who I know by the handle `ciprian.craciun` in my Discord which is called `Lion's Internet Office`.  There is not yet a website [(but here's a nondescript wiki page)](https://communitywiki.org/wiki/LionsInternetOffice) for either the Internet Office or for this work.

We are presently looking for interested collaborators -- whether that is implementing, or simply kicking the can around, or whatever form of engagement -- we are looking for interested collaborators.

The remainder of this document describes the core ideas, the format, some reasonings about why I made certain decisions, and some open questions.  Depending on whether I peter out or not, I may write a bit about the ambitions of the project.

## <a name="addendum-2021-10-09">(Addendum 2021-10-09)</a>

It's been a couple of weeks since I wrote this, and the format has changed in a small, but very important way:  Links and facets (what I called "data" before) are now segregated, and handled differently.

I can't remember exactly how it happened, but am now completely pleased with the segregation.  I was talking with Ciprian Cracium, and I think I was trying to figure out how to extend JSON so that links could be identified within the data blocks.  "How do I distinguish a link, from merely naming a link?", I think was a question on my mind.  I think Ciprian mentioned that if links were separate from data, then all terminals in the block could be understood to be links.  That was the bingo moment for me, and it solved the other problem I had, which was wanting to be able to have links, but being able to position and structure them as well.  (You can read a bit about this in [2021-10-02_linking-from-multiple-perspectives.md](https://github.com/LionKimbro/lions_internet_office/blob/main/2021/users/lion/entries/2021-10-02_linking-from-multiple-perspectives.md).)

So, now there is a `$type` field in each record, along with the `$schema` and the `$id`.

I hope to break this down into smaller and more specific documents, and create a github repository for the Entity-Focal Data Package project as a whole.

Most recent activity in interpretation has been through:
* [the EntityLoader project](https://github.com/LionKimbro/entityloader) -- a Python loader for Entity-Focal Data Packages
* [the file epkgemit.py in the Internet Office](https://github.com/LionKimbro/lions_internet_office/blob/main/2021/discussions/epkgemit.py) -- an example generator of content
* [cipriancraciun/linked-entities-model/](https://github.com/cipriancraciun/linked-entities-model/) -- Ciprian's work on a Linked Entities data model

As always, the best place to go is to [the Discord.](https://communitywiki.org/wiki/LionsInternetOffice)


## <a name="toc">Table of Contents</a>

* [Introduction](#intro)
	* [Background & Purpose](#purpose)
	* [Overview](#overview)
* [Core Ideas](#core)
	* [Entities](#entities)
	* [Entity Identifiers](#identifiers)
	* [Packages](#packages)
	* [More Info](#more)
	* [Schema](#schema)
* [The Format (so far)](#format)
* [Bundled Schema](#bundled)
    * [More Info](#moreschema)
	* [the Generic Item](#generic)
	* [Attachments](#attachment)
	* [Commentary](#commentary)
	* [Links](#links)
		* [Left-Right](#leftright)
		* [Many-to-Many](#many)
		* [Parent-Child](#parentchild)
* [Reasons](#reasons)
	* [Why JSON?  What's wrong with Triples?](#whyjson)
* [Open Questions](#questions)
	* [How do I model links?](#modellinks)
	* [Should Identifiers be specially noted?](#noteidentifiers)
* [Ambitions](#ambitions) -- and also, your invitation to engagement

## <a name="intro">Introduction</a>

### <a name="purpose">Background & Purpose</a>

[The brief](#brief) gives an abstract overview, but this is intended to be a little more friendly.

Basically, we (as programmers) are writing lots of programs.  Traditionally, the value of the programmer in the work of programming has been in the capacity of the programmer to write code.

The skills in making that software code have involved things like:
* knowing what algorithm to use, and how to make it work
* optimizing code, so that things run faster
* being able to do "the book-keeping"
	* (structuring data for efficient interaction, and loading and storing data)
* being able to make a working user interface

If a programmer was working on a video game, there'd be a separate person, an artist, who would make the art assets for the game.  A programmer might write a tool, so that artists could design levels and input codes about how the game world works.  But the programmer doesn't make the art.  The programmer just makes the tools that the artist can use, and the loaders and the exporters for the artist.  (Programmers can of course make art, but then it's called "programmer art," and it is its own specific thing.)

However, it seems to me that more and more, I want data that is useful and that is about the world.  For a very silly example, it would be nice to have a dictionary of all words in the English language, casually at hand.  Now, there are resources for getting such things, and they have been around for a very long time, but my point here is that this is a kind of "worldly" knowledge that programs can benefit from.  Another example might be maps data about the globe:  If you want to present information about the world to users, then you need to be able to draw a map of the world.

There's also this entire world of communications from person to person on the Internet.  Whether that's on Facebook, or in Slack, or on Twitter, or wherever -- we live in this digital ecology of communications.

Yet it is kind of difficult to access this data from within a program.  Each company has its own special means of getting at data, and its own special way of structuring that data.

At any rate, the goal is to make it easier for programmers to be able to get at the world of data out there.  We need a kind of "data internet."  Programmers should be able to browse this "data internet," and then just load that data into their programming environment, following the usual tropes of programming environments (things such as: "There are integers, and strings, and bytes, and lists, and dictionaries, and true/false," etc.,.)  It should be easier, not super-hard.

Now presently, perhaps the most convenient way to access most general data, is through JSON.  If a programmer picks up a file that has JSON formatted data, the programmer can often just look at it visually, and think, "Okay, the information I need is in there, and I think I can see how to get it out."  The JSON data format handles the simple parsing -- extracting out the lists, strings, dictionaries, numbers, etc., from the data file.  The programmer just has to do the higher level navigation -- "Look up this item in the dictionary, navigate through the list until you find the item that has this value for this key," which is so much easier than having to first write out, "OK, here is how to read a string, here is how to assemble a number from digits, ..."

The goal of this project is to do something similar, but at a higher level.  Instead of data being captured in one single file (like a single JSON file,) the data can be captured in a web of files, that are distributed all over the Internet, even.  And furthermore, instead of relying on a path and a filename, everything in the world that you might want to know things about, has its own name -- and you just use that name to locate information about the thing named.

For example, you might have this source -- a single file -- that operates like a phone book (I am dating myself here...,) and when the user asks, "I want to know about this thing (maybe a person -- myself say,) that is denoted by this identifier (maybe `lionkimbro@gmail.com,2021:person:lion`,") then the software goes to this phone book file, and the phone book file tells the software various places where there is information about this person, and vacuums up relevant pieces, and then the software presents that information to the user.

All this work is done by the software, so the programmer doesn't have to do it themselves.

The JSON file format saved the programmer from having to write code about how to construct strings from bytes, about how to construct numbers from digits, about how to construct lists and dictionaries from characters.  *This* system intends to save the programmer from the work of tracking down sources, loading files, extracting identified data items, and so on.

This format should also make it easier for a programmer to browse abstract data.  With browsing tools, a programmer should be able to see more sophisticated data structures -- like parent-child relationships, links between things, annotations as annotations, etc., in a data browser, rather than the more primitive elements of just numbers, lists, strings, and dictionaries.

### <a name="overview">Overview</a>

Now we go into more specific detail about how the system works.  It's a little like learning a new board game, though -- it's somewhat complex, and you don't always understand "why" a piece is there, the moment it's introduced.  Please try and hang with the explanation though.

The big pieces are:

* **Entities** -- things in the world, that data is about
* **Entity Identifiers** -- the name of an entity, that is recognizable globally around the world
* **Entity Data** -- the smallest package of information about an Entity
* **Packages** -- the file that contains a bundle of entity data

I'm not describing "Schema" or "More Info" here;  Those ideas become more obvious once you have the basic ideas here.

These ideas require some explanation, because they are different than what a programmer is usually accustomed to.

In contemporary ordinary programming, when a programmer needs to get some data, the programmer gets that data from *a file.*  That file has a *file format,* which we can understand as the file's "schema," or the file's "type."  The programmer reads that file, loads it into memory with some kind of a loader, which populates the internal memory structures of the program.

That's what programmers are accustomed to doing, but this system is necessarily a little different.  Part of the whole goal of this is so that the programmer doesn't have to work so hard on figuring out where a particular piece of information is coming from.

So -- while there *are* files "underneath" (and the programmer will need to specify at least one file, as a starting point,) the file isn't really the fundamental mechanism of address.

Instead, the programmer uses an identifier for an entity, to get at data.  That is, instead of saying, "I know that the data for the user Lion Kimbro is in this file located at `D:/localdata/people/lionkimbro.json.txt`," and reading that file to get at the information, or instead of going to a MySQL database and saying `SELECT blahblah FROM People WHERE name='Lion Kimbro'`, instead you use an identifier -- and it might look something like `tag:lionkimbro@gmail.com,2021:person:lion`.  (You can skip on up ahead and read more about identifiers in the system in [the specific section dedicated to that core idea.](#identifers))

The system takes care of locating data associated with that identifier -- which may include a step of trapezing through files on the local filesystem, or across the Internet, to get it to you.  Note that the methods of this system are *controlled.*  You control where exactly information is coming from, where it can be sourced from, what sources are trusted and what sources are not trusted, and so on.  But, if this idea works, the process of sourcing the information should be much easier.  That's the idea, at least.

Also note that there has to be some kind of a seed, for where to get information from.  There has to be some "first file," right?  And then that file points to other files, and those files point to still other files, etc.,.  But this gets too deep into the woods.  The key idea that you have to understand right now is that you locate data by some kind of an interesting identifier, rather than by a source.

This is perhaps the most important thing to notice -- the difference between a *source* and an *identifier.*
* <a name="source">**Source**</a> -- a "source" is path that you can follow, to get to some kind of data
* <a name="identifier">**Identifier**</a> -- an "identifier" is a name for some kind of data

If my name is "Lion Kimbro," then that is an identifier.

But if I say, "My website is at taoriver.net," then I've given you a source for information about me.  But there could be *lots* of sources of information about me.  For example, maybe my Twitter profile page, or my Facebook page, or wherever.  They all have information about "Lion Kimbro."

In this system, the "Entity" is me.  The "Identifier" is "Lion Kimbro."  And the sources of information about me are multitude.

* **Entity** -- a thing
* **Entity Identifier** -- the name of a thing, that can be used as a key for locating information about the thing
* **Source** -- where information is coming from (a filepath, a URL, anything)

This system is identifier-based, rather than source-based, and that takes a little wrapping-the-head-around.

"I don't get it -- how do I read data?  How do I write data?  How do I find it?"

This is getting a little ahead, but the basic idea is that there is a system of code that is interacted with something like:

`get(identifier) -> [{...}, {...}, ...]`  -- locate information about a specific identifier
`get(identifier, schema) -> [{...}, {...}, ...]` -- locate information about a specific identifier, that obeys a specific schema
`put(identifier, {...})`  -- note down information about a specific identifier (specifying a schema is optional)

The `{...}` blocks above represent **Entity Data** -- little chunks of information (and here, they are JSON data,) that are about that entity, or that have something significant to say referencing that entity.  The programmer has the job of sifting through it, and determining what to do with it.  The systems job is to supply that data to the programmer.

"When I call `put`, where does the data go?  What file is it stored in?"  That depends on the particular API that you are using, the particular system that you are using.  Conceivably, it might all go into a single bucket of edits;  Conceivably, there is some system of specifying specific buckets of edits, etc.,.  It could get stored in a local file, or published to the Internet -- that's up to the configuration.  The main idea here is to give you a basic picture of how this mode of address could work.

Looking up at the list at the start of this section, I see that "Packages" are the only thing left unexplained.

A "**package**" is simply the individual file that collects a bundle of entity data.  Each package is itself an entity, which means that each package has an entity identifier.  How I work with these ideas right now, these are files.  But they don't have to be stored in files on disk -- packages could be stored in a database, or however.  What's important is that you're able to get to them.  There's a mechanism in the system for getting more information about something, to connect *sourcing* information to an *identifier.*  So whatever mechanism you use, it has to be accessible to the people that you want to be able to get at it from -- so that'll usually be some kind of a URL (for Internet accessibility,) or a file-system path (in the case of an installed program.)

I think that's about it, for the overview:
* **Entities** are noteworthy things.
* **Entity Identifiers** are how you talk about entities.
	* You use **identifiers** rather than **sourcing addresses** in this system.
* **Entity Data** is the actual packaged data about the entities.
	* It's structured just like JSON data.  (Because it *is* JSON data.)
* **Packages** store entity data, and are typically stored in files.
* There's a mechanism for linking identifiers to sources that's commonly used within the packages.

Using this scheme or a scheme similar to it, programmers should be able to find, read, and publish data without having to think so hard about where it's coming from and how to get at it -- even across the Internet.

## <a name="core">Core Ideas</a>

Now what follows is a much more in-depth study of the ideas that were outlined in [the overview,](#overview) as well as some ideas that were only mentioned or alluded to or left unexplained entirely.

If you just wanted to know the basic idea, this is probably the place to check out.

But if you want to understand more deeply how this system works, this is perhaps where you should get a piece of paper and maybe take some notes, to help get it more clearly.

### <a name="entities">Entities</a>

An "entity" is anything in existence, corporeal or imaginary, still or in motion, hypothetical or actual, any thing or any idea that one might want to refer to, that somebody has taken time out of their busy lives to notice, and to identify.

I don't know that this is a complete ontological description of everything or not, (probably not,) but the basic rule of thumb is: "If it's something anybody cares about, you might want to consider it as an entity."  I'm not going to get more metaphysical than that, here.

An important thing to understand about Entities in my system, is that they are <a name="nothing">"nothing."</a>  That is, Entities do not "contain data" of any kind.  There is "Entity Data," but that entity data is something that somebody said about the Entity;  It is not the Entity itself.

The only thing that might be said to be most truly the entity itself is its name (its identifier,) but even this is incorrect, because there's no reason that some entity couldn't have 3 or 4 or more identifiers that all refer to the same entity.

There are only claims about entities.

If I say that my name is Lion Kimbro, and my identifier is `tag:lionkimbro@gmail.com,2021:person:lionkimbro`, and then make a claim that I was born on `1977-08-29`, then the breakdown is as follows:
* **Entity** -- the "entity" is me, Lion Kimbro
* **Entity Identifier** -- `tag:lionkimbro@gmail.com,2021:person:lionkimbro` is an identifier that somebody used to refer to the entity that is me,
* **Entity Data** -- a block of data that effectively communicates that `tag:lionkimbro@gmail.com,2021:person:lionkimbro` was born on `1977-08-29` is making a claim about me, Lion Kimbro,
	* ... but there could also be Entity Data elsewhere in the world, that declares that `tag:lionkimbro@gmail.com,2021:person:lionkimbro` was born on `2021-09-27`, which is to say that I was "born yesterday," and that is just still more Entity Data out there in the world.

The maximal concept of "authority" here is to then be understood as *authorship* ("so-and-so said something about a thing,") rather than, say, *having been certified of worthiness of declaration* -- in the sense of "ICANN has authority over what the names and numbers are."  It is for users (it is up to the users, or the software code, or however,) to determine the *worthiness* of particular entity data and sources of entity data.  This system doesn't do anything to determine or assert worthiness.  (Unlike, say, cryptographic schemes for websites that are intended to help guarantee fidelity and authorship and authority, and such.)

There is no capacity in this system to get "the" Entity Data for an Entity, or "the" Entity Data associated with an Entity Identifier.  There is only Entity Data that makes claims about an Entity by reference via Entity Identifier.

Maybe the claim about myself would look like:

```
{"$schema": ["tag:some-authority@example.net:schemas:people-and-birthplaces"],
 "$about": ["tag:lionkimbro@gmail.com,2021:person:lionkimbro"],
 "person": "tag:lionkimbro@gmail.com,2021:person:lionkimbro",
 "birthdate": "1977-08-29"}
```

This is a ridiculously special-cased scheme, but that's not important -- what's important is that you get the distinction between an Entity (in this case, me,) an Entity Identifier (here, `tag:lionkimbro@gmail.com,2021:person:lionkimbro`), and Entity Data (the whole block of information from `{` to `}`.)

It could be understood here that Entity Data is something like "facets" in [Aspect-Oriented Programming](https://en.wikipedia.org/wiki/Aspect-oriented_programming).  If the preceding sentence helps, great, if it does not, just ignore it.  Just understand that you can make claims about different aspects of an entity through this system.

### <a name="identifiers">Entity Identifiers (Tag URIs and v4 UUIDs)</a>

There are two schemes of identification that I accept into this system that I'm creating:
* the "tag" URI, [detailed in RFC-4151,](https://datatracker.ietf.org/doc/html/rfc4151) and in [a Wikipedia article "tag URI scheme"](https://en.wikipedia.org/wiki/Tag_URI_scheme), and looking something like: `tag:entitypkg.net,2021-09-28:example-tag-uri`
* the familiar 128-bit v4 UUID, [described in Wikipedia article "Universally unique identifier,"](https://en.wikipedia.org/wiki/Universally_unique_identifier) familiar to all, and looking something like: `uri:uuid:401b996b-0806-48b4-8e93-b17f62b17aae`

The v4 UUID hardly requires introduction, but the "tag" URI requires a little bit of explanation - I think most people are not familiar with it.

The interesting qualities of the tag URI identifiers, which are why I chose it for my system, are the following:
* it is guaranteed to be unique, if the authority granting use of the URI tag is sensible in their assignment
	* it is guaranteed to be unique because it is based in (A) something that a person can have sole authority over (an email address, or a domain name,) and (B) a date wherein that person had that sole authority
* it is human readable, human meaningful
* it is relatively short, compared to [some other possibilities I have explored (which I called: XUUIDs)](https://github.com/LionKimbro/xuuid).

My designs for these two identifications are as follows:
* Use "tag" URI whenever you want to have an identifier that is human readable.
* Use v4 UUIDs whenever you have some piece of data that -- you just don't care whether it is human readable or not.

### <a name="packages">Packages</a>

**Packages** are things that provide **entity data**.

Packages are themselves given **entity identifiers**, and so, though I question the usefulness of it at this point, could be said to be **entities** themselves.  That is, there is **entity data** about packages themselves, too.

Now a package is an abstract idea, a logical idea.  In the system I am working on, however, packages are typically stored in individual files, on disk.  There will be [a section of this document on the data format itself](#format), that you should be able to skip ahead to, if you want to see what the package files themselves look like.

### <a name="more">More Info</a>

There is a special kind of entity data that is called "More Info."  It has a specific schema, and it identifies the following things:
* an **identifier**, or **multiple identifiers** -- for some entity, or multiple entities
* a **schema**, or **multiple schemas** -- that it is asserted that the identifier (or ALL of the identifiers) conform to
	* What I mean is that if there are three (x3) schemas listed, and a hundred (x100) identifiers, then it means that all one hundred (x100) identifiers conform to all three (x3) of the schemas listed; it's not mix-and-match.
* a **sourcing location**, or **multiple sourcing locations** -- these are sources that are considered to be fruitful for locating further entity data about the identifiers, presumably either on the Internet, or on the local filesystem
	* Each source locates a Package, [as described previously.](#packages)
	* I think it should be possible to provide not only a source, but also a Package identifier.  However, that would just kick the can down the road -- another piece of information would need to describe, eventually, "Where can I download this packages data, given this package identifier?"
		* That said, this would be very important if the package were not conventionally stored.  That is, if its data were stored in a database, or if its data were returned from a function call, or if the package were kept in RAM, or shipped as a program's resource file, or some other kind of unusual oddity.

The "More Info" entity data is kept as entity data within packages.

So you can easily imagine that there would be one big package, operating as a kind of directory service (like a phone book,) that all it does, is contain More Info entries that say "If you want to learn about X, go over there."

### <a name="schema">Schema</a>

The system relies on a concept of "Schema."

A Schema is itself, an entity.

Keep in mind that entities themselves do not have schema.  Remember, [an entity is nothing.](#nothing)  Being nothing, they can't have a schema.

The identifiers themselves to not have schemas.  They are just identifiers.

Instead, what has a schema, is **entity data.** Entity data has a schema.  Correction: *Can* have a schema.  *Should,* generally speaking, have a schema.  Though I'm not going to force this -- I think you should always be able to just attach some random data to a entity identifier, and leave it to the programmer to figure out what to do with it -- ["duck typing" it, so to speak.](https://en.wikipedia.org/wiki/Duck_typing)  ("If it looks like a duck, acts like a duck, maybe I'll just treat it as if it's a duck.")

In a given piece of entity data, say, ...

```
{"$schema": ["tag:some-authority@example.net:schemas:people-and-birthplaces"],
 "$about": ["tag:lionkimbro@gmail.com,2021:person:lionkimbro"],
 "person": "tag:lionkimbro@gmail.com,2021:person:lionkimbro",
 "birthdate": "1977-08-29"}
 ```

Here, the schema is the identifier that is essentially here to communicate, "This entity data is about a person specified by the `person` key, who has a birthdate that is specified in key `birthdate`."

The `$schema` identifies the schemas that this entity data conforms to.  The `$about` lists the identifiers that this entity data is advertised to be about.  And then the `person` and `birthdate` are the particular information of this entity data.

Note that -- no further information is truly required.  There is no idea such that -- "The software system downloads the schema `tag:some-authority@example.net:schemas:people-and-birthplaces`, and then, upon finding a complete computer-interpretable specification of what conforming entity data looks like, and then confirms that the entity data conforms to the specification."  None of that is required.  If this hurts your brain, it might be easier to just think of a schema as a type declaration.

In the future, if this implementation progresses, sure, maybe one day, there will be such a detailed schema.  But for the time being, "no," and it's really not required.

Well, that's not quite right -- I *have* made a schema format.  But it is a very, very simple format, essentially just noting a title for the description, and a human readable description of the schema.  But this is not essential.  What is important about the schema is the entity that the schema represents, and the identifier that the schema is referred to be -- not the entity data that annotates the schema itself.

Further development of the schema concept can be safely left to future development.  It is important to have the concept of a schema here;  It is not important that it has an air-tight definition.  Such things are difficult, regardless, and immediately unnecessary.

## <a name="format">The Format (so far)</a>

This is a little bit of trickery.  See, I wrote a draft version of the "Entity Package" data format, a couple weeks back, and made a bunch of data for it.  Then as I experimented with it, I found some things that I wanted to change, and do differently.  And I realized, "Oh, wait, you could just store the More Info's as Entity Data, ...," and other such things.

I haven't yet actually implemented what I am going to describe here.  But it is based on what I have implemented prior.

Let's start with an example package file:

```
{
  "$schema": ["tag:entitypkg.net,2022:entity-schema:entity-package-v1"],
  "$about": ["tag:lionkimbro@gmail.com,2021:entity-package:lions-internet-office-discussions-v1"],
  "$records": [
    {"$schema": ["tag:lionkimbro@gmail.com,2021:entity-schema:article-feed-v1",
                 "tag:entitypkg.net,2022:entity-schema:link:parent-child"],
     "$about": ["tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:feed"],
     "title": "Lion's Internet Office -- Discussions Feed",
     "parent": "tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:feed",
     "children": ["tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:post-0",
                  "tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:post-1",
                  "tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:post-2",
                  "tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:post-3",
                  "tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:post-4",
                  "tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:post-5",
                  "tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:post-6",
                  "tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:post-7",
                  "tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:post-8",
                  "tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:post-9",
                  "tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:post-10",
                  "tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:post-11",
                  "tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:post-12",
                  "tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:post-13",
                  "tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:post-14",
                  "tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:post-15",
                  "tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:post-16"]},

    {"$schema": ["tag:lionkimbro@gmail.com,2021:entity-schema:generic-v1"],
     "$about": ["tag:lionkimbro@gmail.com,2021:person:lion"],
     "eid": "tag:lionkimbro@gmail.com,2021:person:lion",
     "title": "Lion Kimbro",
     "type": "a Person"},
    {"$schema": ["tag:lionkimbro@gmail.com,2021:entity-schema:generic-v1"],
     "$about": ["tag:lionkimbro@gmail.com,2021:person:ciprian.cracium"],
     "eid": "tag:lionkimbro@gmail.com,2021:person:ciprian.cracium",
     "title": "Ciprian Cracium",
     "type": "a Person"},
    {"$schema": ["tag:lionkimbro@gmail.com,2021:entity-schema:generic-v1"],
     "$about": ["tag:lionkimbro@gmail.com,2021:person:bouncepaw"],
     "eid": "tag:lionkimbro@gmail.com,2021:person:bouncepaw",
     "title": "BouncePaw",
     "type": "a Person"},

    {"$schema": ["tag:lionkimbro@gmail.com,2021:entity-schema:article-v1"],
     "$about": ["tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:post-0"],
     "eid": "tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:post-0",
     "authors": ["tag:lionkimbro@gmail.com,2021:person:lion"],
     "html": "https://github.com/LionKimbro/lions_internet_office/blob/main/2021/users/lion/entries/2021-09-05_about-me.md",
     "raw": "https://raw.githubusercontent.com/LionKimbro/lions_internet_office/main/2021/users/lion/entries/2021-09-05_about-me.md",
     "hook": "about Lion Kimbro",
     "posted": "2021-09-05"},

    {"$schema": ["tag:lionkimbro@gmail.com,2021:entity-schema:article-v1"],
     "$about": ["tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:post-1"],
     "eid": "tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:post-1",
     "authors": ["tag:lionkimbro@gmail.com,2021:person:ciprian.cracium"],
     "html": "https://scratchpad.volution.ro/ciprian/992c7f2944456f18cdde77f683f49aa7/6697ebb3.html",
     "raw": "https://scratchpad.volution.ro/ciprian/992c7f2944456f18cdde77f683f49aa7/6697ebb3.txt",
     "hook": "storing tree structures on file systems",
     "posted": "2021-09-05"},

    {"$schema": ["tag:entitypkg.net,2022:entity-schema:packages:moreinfo-v1"],
     "$about": ["tag:entitypkg.net,2022:entity-schema:schema-v1",
                "tag:entitypkg.net,2022:entity-schema:entity-package-v1",
                "tag:entitypkg.net,2022:entity-schema:link:parent-child",
                "tag:entitypkg.net,2022:entity-schema:generic-v1",
                "tag:entitypkg.net,2022:entity-schema:packages:moreinfo-v1"],
     "schema": ["tag:entitypkg.net,2022:entity-schema:schema-v1"],
     "sources": ["https://raw.githubusercontent.com/LionKimbro/lions_internet_office/main/2021/data/entitypackage_basics.json"]},

    {"$schema": ["tag:entitypkg.net,2022:entity-schema:packages:moreinfo-v1"],
     "$about": ["tag:lionkimbro@gmail.com,2021:entity-schema:article-feed-v1",
                "tag:lionkimbro@gmail.com,2021:entity-schema:article-v1"],
     "schema": ["tag:entitypkg.net,2022:entity-schema:schema-v1"],
     "sources": ["https://raw.githubusercontent.com/LionKimbro/lions_internet_office/main/2021/data/entitypackage_experimentalfeeds.json"]}
  ]
}
```

Here you can see that a package is a very simple thing.
* It is kept in a JSON file.
* It has three keys: `$schema`, `$eid`, and `$records`.
* `$schema` is always `["tag:entitypkg.net,2022:entity-schema:entity-package-v1"]`.
* `$eid` is always a list of identifiers that the package is known by.
	* Almost always just a single identifier.
* `$records` is a list of records.

Entity data universally conforms to the following conventions:
* `$schema` is always a list of entity identifiers, said entity being a schema.
	* This key is not *strictly* required.  But almost always good to have.
* `$about` is always a list of entity identifiers.
	* This is the signal to the system that the named entity data can be found described, or at least mentioned, here.
	* This key is not *strictly* required.  But almost always good to have.
		* You could find the data without a key by doing a search on just the schema, dismissing care for identifiers.
		* You could find the data by manually dumping the packages entities.

["More Info"](#more) is provided via special entity data, listed at the end of the example listing above.

In the entity data for `"tag:lionkimbro@gmail.com,2021:lions-internet-office:feeds:discussions:feed"` in the example above, you can see how a single block of entity data can conform to two schema at the same time.  In this case, there's a parent-child link between the feed and the articles named by the feed, and then there's the title of the feed itself.

## <a name="bundled">Bundled Schema</a>

I'm starting to run out of steam, so I'm going to go more briefly over this part.

Ciprian has been advocating strongly for there to be basic, common elements in a data system with the kind of aims that this system has.  Something he said in Discord:

> *Therefore I think we can apply the same pattern with our system:*
> * *identify a small set of uniquely, highly useful, concepts (entities, links, attachments?, annotations?);*
> * *make sure they are flexible enough to model the real world (i.e. links between multiple entities;)*
> * *make sure the whole system is extensible in the terms of these small set of primitives;*

-- Ciprian Craciun,
  *(in: Lion's Internet Office, #programming > #Entity-Focal Data Package, on: Tue 2021-09-28 12:54 AM, (Seattle time))*

I have pushed back a bit on building these primitives into notation, like I think Ciprian favors, but none-the-less I think it is a good idea to have bundled schema, that are common, and have common tooling.

One of them has already been seen.

I will describe here further elements, which may be elucidated in future documents or schema descriptions:

* <a name="moreschema">More Info</a> -- this has already been illustrated in the example above
* <a name="generic">the Generic Item</a> -- the idea is to denote a "generic item"; it has a title, an informal type (expressed independent of the schema system,) a description, an illustrative image, a hook string, a web page, descriptive tags, and various other knick-knacks of data that can describe an item generically, and that could be viewed or searched for in a browser; [I have written about this more elsewhere](https://github.com/LionKimbro/lions_internet_office/blob/main/2021/users/lion/entries/2021-09-13_the-generic-thing.md)
* <a name="attachment">Attachments</a> -- a way of describing an attachment to some entity -- a gigantic file, generally, that is considered as an "attachment" to something else; Ciprian has especially advocated for this
* <a name="commentary">Commentary</a> -- a human readable comment on an entity, like a comment in code, but specifically a comment on an entity
* <a name="links">Links</a> -- specific link types
	* <a name="leftright">Left-Right</a> -- an entity that has `left` and `right` defined, and that represents some fundamental link between two things; the entity data may have multiple schemas, and the other schemas give greater definition to the type of the link
	* <a name="many">Many-to-Many</a> -- an entity that has `linked` defined, that represents a mutual and symmetrical link between all of the entities identified within the list `linked`
	* <a name="parentchild">Parent-Child</a> -- an entity that has `parent` defined with a single parent, and `children` defined with a list of children of that parent

## <a name="#reasons">Reasons</a>

Hoy!  I am getting tired.  So this is going to be brief.

* [Why JSON? What's wrong with Triples?](#whyjson)
* [Links are Entities](#linksareentities)

### <a name="whyjson">Why JSON?  What's wrong with Triples?</a>

The Semantic Web effort, the Linked Data effort, has normalized itself around RDF triples.

That is, for everything you say, you express it in triples roughly of the form:
* "Lion Kimbro" "has-birthdate" "1977-08-29"
* "Lion Kimbro" "has-eye-color" "blue"
* "Lion Kimbro" "loves" "Kitty"

...and so on, and so forth.

The Semantic Web efforts have made elegant data formats that hide that everything is triples, in the expression of the data.  But underneath, the data is stored in triple stores, and then queried out of the triple stores, with some form of a query language.  The idea is that when you want to pull data out, you can write an elegant query, and then get at the data.

Hm, -- ...

So, I've seen it, but I haven't used it.

It looked fairly complicated.

And I think:  "Is this a case where [Worse is Better?](https://en.wikipedia.org/wiki/Worse_is_better)"

As an ordinary mortal programming computers, -- perhaps this is retrograde of me, but I like simple systems of JSON-like data.  In Python, which is my go-to programming language, I regularly work with lists, numbers, strings, and dictionaries.  I like them, and they are comfortable.

I can write a list comprehension like `[D for D in L if D["prop"] == "value"]` just fine.

Most of the time, I'm not writing some complex, abstract manipulation of a volume of data.  Rather, most of the time, I'm consuming data that was written to purpose.  that means that the organization of the data has been made for my convenience.  And when it's not to my convenience, it is usually easy enough to extract the data I need, without using a sophisticated query language.

If I need the data a particular way, I'd just write another entity data block by a different schema, that was more appropriate for that view of the entity, and then retrieve that entity identifier with the specific schema.

So I think that simple JSON data is just fine, and I think that keeping a triple store and querying a triple store makes the data feel more alien, and more peculiar to program with, vs. just using JSON data straight.

### <a name="linksareentities">Links are Entities</a>

This is one that Ciprian and I are opposite ends of, in our hunches.

I think Ciprian is of the mind that Links and Entities are two fundamentally different things, and that the differences between them should be reflected in the fundamental data model.  I believe that Ciprian takes his inspiration from [the Associative Data Model.](https://github.com/LionKimbro/lions_internet_office/blob/main/2021/users/lion/entries/2021-09-14_related-works.md#associative-data-model-adm)

By contrast, in the system I have outlined here, everything is just entity data, [entities are "nothing,"](#nothing) and links are just entity data that meet a particular schema.

My thinking is that it is best to define a minimal system, and then put a language of basic elements around it, and then allow for a world of complexity to develop beyond that.

The basic elements I have chosen as my kernel are:
* entities -- which are nothing
* entity identifiers -- which are unique names
* entity data -- which declares things about entities via their identifiers
* schema -- which *type* entity data
* packages -- which bundle entity data

Then there are [the bundled schema,](#bundled) that build on top of the entity data and schema:
* More Info -- entity data that tells you how to source more entity data
* Generic Item -- generic entity data to describe something
* Links (of three types) -- generic entity data to describe links between things
* ... (some additional items)

While it is clear that there is work to be done to specify how this all works, both in terms of precision, and in terms of nailing down what is included and what is excluded, it seems to me that this basic strategy is right.  If I pushed the elements in the bundled schema up into the layer of "entities, entity identifiers, entity data, schema, packages," then I think I would make the basic kernel that much harder to successfully implement, and endanger the likelihood that people would write tools to work with this system.  It would make it that much more costly to implement.

For example, if "an email address" is a basic parse-recognizable string type, and an ISO-8601 date is a basic parse recognizable string type, and (so on, and so forth,) then the person who wants to implement a parser for this system has to implement all of these concepts in the code that they write.

I hope that one day, somebody does make something like JSON that is able to recognize the world of things that can exist, and make a nice notation that captures it all somehow.  But I suspect that that will happen *after* the revolution of networked data plays out, rather than before, because the gift of networked data is specifically the capacity to work with very complex and collaboratively developed data sets, and that is what is required in order to make the nice notation.  I think.

My belief is that one day, these sophisticated systems will make work with the more complex subtleties of data that we can clearly imagine* much easier.  Then I think it will be much easier to write sophisticated "low-level" data formats that alternate to JSON, and that are absorbable in pretty much every programming language in common use, as JSON is.

But in the mean-time, we are not there.  We are still pulling bricks by hand, and positioning them one atop the other, by hand.  So I think we still need small kernels today, barring heroic multi-million dollar efforts.

*(*footnote) -- "that we can clearly imagine" -- I mean, we all know some native human language, which is many times more complex than any computer programming language,*


## <a name="questions">Open Questions</a>

A number of questions come to me.
* [How Do I Model Links](#modellinks) -- also, "Does the multiple-schema idea really work?"
* [Should Identifiers be specially noted?](#noteidentifiers)

## <a name="modellinks">How Do I Model Links?</a>

(Post-scripted:  I get there by way of: "Does the multiple-schema idea really work?"  Hang with this for a moment.)

I think I included the idea of multiple-schema with a sort of compromise with Ciprian in mind.  That said, I'm not sure it's really a good idea.

Here's the root of the problem:
* Ciprian wants links to be general and interpretable in a data browser.  If you have general link types, then even if you don't have the specifics of the link worked out (perhaps you can't load the schema, or the schema doesn't exist yet,) you can still make out in the browser that there is a kind of link between two entities.  I agree that that sounds really great, and so yeah -- let's include some basic link types.
* On the other hand, I'm slightly skeptical of "links between entities," in the abstract.  I am more inclined to have a JSON data structure, and a value to some key, or a value in some list, is an identifier that points to another entity.  That gives the links "positioning" within the JSON data structure (as a value of a key, as a value with an index within a list,) which is more natural to conventional programming, and carries meaning by context, which would otherwise have to be specified somehow in the "links between entities" paradigm.

I figured that allowing entity data to have multiple schema would help solve this problem.  But it doesn't.  It fails, because (for example) a piece of entity data can only have a single left-right link relationship, now.

So how do I model links?

Are links embedded in the Entity Data, with that rich positional data, but not abstractly recognizable by a browser?

Or are links their own entity data, annotating entities abstractly?

Is there a way that I can get the best of both worlds -- links positioned within the JSON data, but also abstractly recognizable by a browser or a query system?

Perhaps just manually specify *both*?  Or perhaps a schema annotation can declare how to produce links information from entity data?

I am turned off by the idea of pushing positioning information into purely abstract links.  "This is a link between a feed and an article.  The article has ordinality 34 -- it's the 34th article in the feed."  That seems really ugly to me -- it feels like the most ordinary way of representing articles, is simply to list the article identifiers in a list within the feed.  That's what people would expect, that's what people would use, that's what people would like to read and write.

So this seems like a sort of fundamental problem, and I've already written notes towards an article on specifically this problem, which, if time and luck coincide, I will write up and hope that I remember to link to from here.

## <a name="noteidentifiers">Should Identifiers be specially noted?</a>

What I mean --

In JSON, there are just "strings."  You can't even specifically demark, say, base64 data.

This means that if there's an identifier like `"tag:lionkimbro@gmail.com,2021:person:lion"` as being specifically an identifier, rather than a string that happens to read `tag:lionkimbro@gmail.com,2021:person:lion`.

Where this comes in is --
If I could just scan the entity data for identifiers, then there'd be no need for an `"$about"` key, since you could just scan the entity data for identifiers and take a note that there's a reference to the identifier in this block.

That said: I'm not sure that I really want that behavior.  If I had that behavior, then every mere *mention* of an identifier would cause it to be flagged, and that's not always what you want.  Something might be mentioned 10,000 times, but you only want to pull entity data where it is specifically listed as `$about` that entity.

But you could at least do a `search_for_mentions(identifier, schema)`, and I could easily see that being useful.

I remain on the fence.

### <a name="howtonoteids">How To Note Identifiers in JSON</a>

But let's talk for a moment about, how you could implement identifiers in JSON.

You could make `!` a special character, and if a string begins with `!`, then it is an identifier.

Now you just have to pass all the strings going in and out of your JSON encoder/decoder, and make some substitutions.

If it's an Identifier object, encode it like `"!"` + the identifier, and use that string in JSON.
If it's *not* an Identifier object, and it starts with a `!`, then use some kind of an escaping sequence ( `!!`), and encode it out like that.

On the read, if it starts with `!!`, then it's a normal string that starts with a single bang; If it starts with `!` and something else, it's an identifier, and should be wrapped as such.

Whatever -- some kind of silly escape system.

It's ugly, it's a hack, but if this feature was important, I think I'd be willing to make this compromise.

## <a name="ambitions">Ambitions</a>

That pretty much wraps up how this all works.  But I want to conclude with a note about my ambitions here.

I wrote up in a Discord thread, (not yet in an article,) my picture for the next couple of years: "Networked Data Exploration Ambitions 2021-2023."

In it, I specified these principles:
* Many Data Formats & Possibilities Can Be Explored
* Fun/ADHD > Ambition
* Ambition > Who Cares
* Contact > Rules

And then I wrote the following:

> This is my picture of my efforts on networked data exploration for the next 2 years.
> 
> This is not a commitment; It's not even a statement of intent; Rather, -- it's just what I envision could be in the next 2 years, after an hour of thinking about it.
> 
> I am very ADHD, and tend to move "from thing to thing." I am also a foundational pillar of [the Star Community,](http://star-community.org/) which is the first priority in my life, and then I have a job, which is an important priority, and then there are also relationships that are precious to me.
> 
> So, this is not "my life's effort," -- rather, this is something that I do for fun. But I also take it seriously and hope that it can be a serious contribution.
> 
> So in Principles, I wrote "ADHD/Fun > Ambition,"
> 
> But I also added "Ambition > Who Cares." I'd like to treat this project responsibly.
> 
> If I should be so fortunate that this should should grow to be something bigger, I'll start looking for replacements for myself who take on the responsibility.
> 
> I want to keep this broader than EntityPkg. I am very intrigued by Ciprian's lines of thought, even when I do not agree with them myself, so I would like to have a "Big Tent" approach to data formats and such.
> 
> If I should be so fortunate that a community develops around this exploration of networked data formats, then I would like it to carry several different data concepts in its midst.

I find "semantic web" and "networked data" ideas fun, and worthy of exploration.  This represents my exploration.

I would consider this effort to be a suprising success if somebody, just somebody, who I don't even know, read something here, and it altered how they thought about networked data, and led them to implement something somewhere else, which then somebody else saw, who I don't even know about, and that led them to do something valuable in some big-time data format that everybody uses.  *Wouldn't that be cool?*

And if it's just me and Ciprian experimenting with data formats and we learn something, kick some ideas around, and have fun, that is success enough for me.  I learn a lot from working on this.  `Fun/ADHD > Ambition`

But if there's a possibility that this could be a data format that a lot of people use, I'd like to submit my applications, do the work, and make it happen.  `Ambition > Who Cares`.

If you find these ideas interesting, if you like how I talk, if you would like to explore these ideas with us, I invite you to visit my "Internet Office," [Lion's Internet Office,](https://communitywiki.org/wiki/LionsInternetOffice) introduce yourself, either in #general or in #programming, and share a little about yourself and what you're interested in.  We can talk in a live discussion, or by text, whatever you're comfortable with, and see how we can link our problems and our creativity together.