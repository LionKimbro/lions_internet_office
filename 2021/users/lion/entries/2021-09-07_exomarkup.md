# exo-Markup HTML Generation
Lion Kimbro
2021-09-07

Introducing "exo-Markup", which can be understood as a simple container format for markup languages.  `pmarkup` is introduced as a particular implementation.

## <a name="2014">The Situation: 2014</a>

Back in 2014, I wanted to generate a bunch of web pages.

I wanted to do it from a text file, because I love editing text files, and I was accustomed to working with wiki formats.

And I wanted to do some custom code generations for some specific purposes, so I wanted whatever I used to generate the code, to be easily "switchable," let's say.

And then there was the issue that I felt like rendering wiki pages is hard.  I had tried a few times, but failed.  I couldn't figure out how to handle problems of overlapping bolded vs. italicized text, and dealing with links that span across paragraphs, and various other kinds of weird situations that can arise.  This is not a good reason, because I could have read how, say, MoinMoin implemented its wiki-text system, or tried to decypher the perl of OddMuse, or what not, -- but for whatever reason, I didn't do it, and moved on to other things in my efforts to make a full-blown wiki processor.

For whatever reason, however it developed, I found a new solution.  I call it "Exo-Markup", because it identifies features of the text "from the outside."  And my particular implementation, I named "pmarkup", because it's a markup system, and it is very odd-looking according to our conventional systems, because the way that it handles paragraphs is very unusual.

## <a name="appearance">What It Looks Like</a>

Here is an example pmarkup file:


    p
      This is a test.
    
      This is only a test.
    
    p
      I wonder if it works?
      I hope so!

This entry generates the following:

    <p>
    This is a test.
    This is only a test.
    </p>
    <p>
    I wonder if it works?
    I hope so!
    </p>

Here you can see one of the defining features of the format -- there are two types of lines.
* column 0 lines, which define a shift in the structure of the document
* column 2 lines, which are content

The "p" instruction says, "Start a new paragraph."
The content lines provide the content of the paragraph.

In pmarkup, if you want to insert raw html, you do it like so:

    html
      <p>Here is some raw html, manually inserted.</p>
      <p>More such lines.</p>
    p
      Now this is a new paragraph, inserted via pmarkup.

## Made for Programmers

This approach was taken substantially because it makes it easy for programmers to work with the format.

The outer loop of the interpreter can look something like this:

* for each line of the file
	* strip the line
	* if it's blank, skip this line
	* if the first character is something other than a space:
		* handle the mode-switch, if any
		* render any output, as necessary
	* if the first two characters are (space space):
		* handle the content

So for example, in pmarkup.py, it looks like:

    for fullline in f.readlines():
        fullline = fullline.decode("utf-8")
        line = fullline.rstrip()
        if line.strip() == "": continue
        if chew() == 0: continue
        if fullline[0] != " ":
            if word == "p":
                closetop()
                out(0, "<p>", 3)
                if line.startswith("#"):
                    chew()
                    out(0, """<a name="{}"></a>""".format(word[1:]), 0)
                nl()
                p = True

Don't worry about the particulars here;  But you can note some features:
* The "p" command causes it to close out any prior commitments (for example, an opened table, or a previously opened paragraph marker.)  That's what the call to `closetop()` is about.
* The "p" command outputs the `<p>` block.
* If you give an argument to the "p" command, such as in a line like `p #foo`, then it also creates an anchor.
* It notes that a paragraph block has been opened.

I'm not trying to train you up on pmarkup, so don't worry about remembering all of that.  I'm just trying to communicate the idea of an "exo-markup" system.

## Container Format for Markup

I did not do it in pmarkup, but it is simple to see in this paradigm how one could make commands like:
* markdown -- the following lines will be markdown formatted, and should be run through a markdown processor, and output as html
* asciidoc -- the following lines will be asciidoc formatted, and should be run through an asciidoc processor, and output as asciidoc
* ...  -- (what have you, any system)

As such, exo-markups could be understood as a "container" format, specifically for containing sections of a page to be generated.

## Meta-Data in pMarkup

One thing I did was make it easy to define annotation data, meta-data, in `pmarkup`.

So for example, there is this one line of code:

        elif word.endswith(":"): D[word[:-1].upper()] = line

...which simply says, "If the command ends with a colon, interpret it as a key and store the remainder of the line in the dictionary with that key."

And so I have a file that begins with:

    title: Sun, Moon, and Stars
    template: wiki
    wiki: SunMoonAndStars
    slug: sun-moon-and-stars
    filename: sun_moon_and_stars.html

...which means, "The title of this document is `Sun, Moon, and Stars`, render it with the `wiki` template,  identify it by the wiki-name `SunMoonAndStars`, use the slug `sun-moon-and-stars` in the URL, and store it on disk with filename `sun_moon_and_stars.html`. 

The particular information collected isn't important here;  What's important is that arbitrary meta-data is easily collected and parsed from the content of the file.  This is an important consideration for a container format, and one easily met in an exo-markup system.
