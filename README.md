# lions_internet_office
Articles, Records, and Inspirations from and around Lion's Internet Office


## Purpose

We have a lot of interesting conversations in [Lion's Internet Office (on discord)](https://discord.gg/vFS94Sn), and several of us wanted to keep some notes and resources from those conversations.  This git repository is suggested as a resource that people who hang out in the Internet Office can use to keep information and code.


## How It Is Intended to Work (Immediately)

1. Hang out in Lion's Internet Office.
   * preferably "#programming," or a related channel
2. Ask for commit access to this repository.
   * note: _I'm not sure how to give people commit access just yet, so I'll figure it out as we go._
   * Or fork the repository and issue a pull request.
3. Check out the repository, add files to the appropriate locations, commit, and push.
   * Or use github's already-present always-present in-browser "add a file" capabilities.

When you want to talk about an article that's in here, post comments in a sub-thread of the #programming channel (or whatever channel you find appropriate.)

To be clear:  Discussion, commenting, and so on -- are intended for Discord, and not in the published articles.

Conversation participants are strongly encouraged, hereby explicitly invited, to update relevant articles, or to post new articles, during or after those conversations.


## How It'll Work in the Future

I'll have some kind of repository that pulls the code down, and then it'll also execute some kind of generation script periodically, and, reading various files as input, output a static HTML website.  Everybody'll be able to make their own generators and such, as necessary.

This is just a note of intention for the future;  This isn't actually in effect presently.


## Directory Layout

This note, however, is for the present.

I'm setting up the directory tree in a particular way, and want this setup to be respected.

The data organization is time based.  So the directory immediately after the root (`/`) is `time/`.
I'm setting up the directory tree like so:

* `/`  -- the root directory for the project
   * `time/`  -- the root directory of most data, which is laid out by year of origin
       * `2021/` -- the root directory for this year
          * `usr/`  -- user-specific directory -- user folders will go in here
             * `lion/`  -- Lion's personal contributions directory (choosing myself for example)
                * `img/`  -- images, named by any particular method
                   * `2021-09-05_image_name.png`  -- a particular image; note the date in the prefix
                * `entries/`  -- any particular entries, intended for public consumption
                   * `index.md` -- a Markdown file, an index of other files in the directory
                   * `2021-09-05_article-name-here.md` -- a Markdown file; note the date in the prefix
                * _user discretion_`/` -- any folder at the user's discretion
                   * _user discretion_  -- any file at the user's discretion

When you first use the repository, think up a simple name (all lower case, no spaces, no punctuation, basically: [a-z]+) and add a folder for yourself beneath `/time/2021/usr/` -- that will be your own folder.

You can do anything that you like with your own folder, but I hope that you will place images beneath `img/`, and articles (or anything else intended to be represented with a web page) under `entries/`.

My intention is that the paths to images and entries are considered "hard" rather than "soft" -- that we treat them as permanent unchanging immutable addresses.  Of course, they are not, and I think we should think that maybe in the future we might relocate them.  But for the time being at least, please consider them "hard" rather than "soft."


## Sharing Links

Ciprian has proposed keeping snapshots of source and HTML used for various articles, and thus has proposed that when we share a link to something, whether from this git repository or from a personal site or [CommunityWiki](http://communitywiki.org/) or wherever, that we share two links -- the first to a raw version of the file for editing, and the second to a generated HTML file.  He intends to write a tool that will use the two links and make an archive version of those two things.
