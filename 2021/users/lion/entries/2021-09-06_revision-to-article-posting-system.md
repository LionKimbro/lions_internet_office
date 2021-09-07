# Revision to the Article Posting System
Lion Kimbro, 2021-09-06

## <a name="problem">The Problem</a>

Gratitude!  We now can post things, and people on the Internet can read them.  Huzzah!

But there are a few issues that I immediately face.
* **Horrible URLs**
  * The URLs are horrible.
	* example: [https://github.com/LionKimbro/lions_internet_office/blob/main/2021/users/lion/entries/2021-09-06_programming-philosophy.md](https://github.com/LionKimbro/lions_internet_office/blob/main/2021/users/lion/entries/2021-09-06_programming-philosophy.md) -- that's mosterous
* **References**
  * Image References must be relative & know the environment
    * I'd rather be able to *name* the image, and have it linked, rather than *source* the image, which is dependent on a whole lot of things.
  * Similar for links to other pages.
* **Framing**
  * The pages are stand-alone, and not easily contextualized with respect to other pages, save by manual navigation of the tree by URL manipulation.

## <a name="generator">Solution: A Generator</a>

I think what I want, in order to fix this, is an HTML generator.

The code would be maintained in the project tree.
* `/2021/code/generator/` -- where the code for the generator would live
  * `generator.py` -- the HTML generator

The system might use filetalk (a Python system I have written, but not yet published to github,) or environment variables, to locate the place to position the output generated pages.

I'd need to configure Apache to serve pages from the output directory.

Now there are some big questions:
* How is the content written?
	* Presently, we are using MarkDown.  But I don't assume this.
* How is other content addressed and referenced?
	* Images
	* Pages
	* Sections within pages
	* perhaps even *paragraphs* within pages
		* (and here we can look at the ideas that Ciprian draws attention to -- uniquely addressing paragraphs and other objects via identifier)

These are not questions to the side; These questions touch on some of our fundamental research questions.

Ordinarily, if we were ordinary reasonable people, we would say, "Now let's select a wiki package to use."  But I am not an ordinary and reasonable person, and I am specifically interested in these questions of representation.  (See [my programming philosophy,](https://github.com/LionKimbro/lions_internet_office/blob/main/2021/users/lion/entries/2021-09-06_programming-philosophy.md) for more on this topic.)

We have solved the *immediate* problem of, "how can we put stuff on the Internet?"  After all, that's what this repository is.

But now I am interested in this more particular and specific problem.

Deciding to use a generator, now there are many questions about how to write it.

## <a name="generator-options">Options for a Generator</a>

These are some of the options I am immediately considering.  I'm open to other options, and I am also to the idea that I shouldn't be doing any of this at all.  But this is the current position of my thinking.

### <a name="issue-content">Issue: How is the Content Written?</a>

* Option 1:  **straight MarkDown** -- Use MarkDown (which is then rendered)
* Option 2:  **output MarkDown** -- Write something, that outputs MarkDown (then rendered)
* Option 3:  **output (something)** -- Write something, that outputs something other than MarkDown (then rendered)
* Option 4:  **pmarkup** -- Directly generate HTML, using pmarkup, or pmarkup2020
* Option 5:  **pmarkup + MarkDown** -- Directly generate HTML, using a hybrid of pmarkup and MarkDown (MarkDown embedded within pmarkup)
* Option 6:  **custom renderer** -- Directly generate HTML, using something new or different
* Option 7:  **in-browser custom** -- Don't generate HTML at all; instead, create some kind of in-browser run-time Javascript environment, that reads a source file, and then generates something within the web browser???
* Option 8:  **custom client** -- Don't generate HTML at all; instead, create a special reader program that readers run, in order to read the data

"pmarkup" requires some introduction.  It's a method of generating HTML from text that is, let us say, "programmer friendly," that I wrote in 2014, and haven't really seen anything like.  I'll write more about it further in this document.

My own preference order would be:
1. Option 5 -- **pmarkup + MarkDown** -- pmarkup with integrated MarkDown
  * Note: any other markup scheme should be pluggable as well; pmarkup is pretty much a container format as it is
2. Option 4 -- **straight pmarkup**
  * Note: pmarkup is *designed* and *intended* to be extended based on the needs of the domain, and so that would be easy to do; pmarkup is about 100-200 lines of code, if I recall right.
 3. Option 6 -- **custom renderer**
 4. Option 7 -- **in-browser custom** -- exciting and interesting; would require I learn a lot of new stuff
 5. Option 8 -- **custom client** -- don't generate HTML, write a special reader program
 6. Option 2 -- **output MarkDown** -- this might be the *easiest*, *fastest* solution

### <a name="issue-addressing">Issue: How Is Other Content Addressed?</a>
Regardless of how content makes its way to the viewers eyes, -- MarkDown, or pmarkup, or something different -- the question remains about, -- "How is content -- like images, like other pages -- going to be addressed?"

And here I look at different options.  I won't number them this time; I'm just going to name them.

* **URI Tags** -- [(Wikipedia article)](https://en.wikipedia.org/wiki/Tag_URI_scheme) -- for example, an image might be referenced by just `lionkimbro@gmail.com,2021-09-06:self-portrait`
* **Hash IDs** -- that is, directly use the hash ID as the resource identifier for the target -- related to Ciprian's advocacy
* **Local Names** -- that is, a specifically defined namespace for resources
	* Note that in a way, this just kicks the can down the road, ...
		* **Local Names + Paths** -- Local Names that point to paths relative to the base of the source tree
		* **Local Names + Unique Names** -- if we make sure that filenames are unique system-wide, then you can just name them, and they'll be searched for in the source tree
		* **Local Names + hash IDs** -- that is, the local name specifically names the hash ID of a graphic resource, or of a page, or of a paragraph within a page, per Ciprian's interest
		* **Local Names + constructions** -- for example, if you named a user (such as "lion" or "ciprian", then it would point to a page about the user name

I think I am leaning towards some form of combination of all of these.

#### <a name="hashids">An Aside About hash IDs</a>

I am not as enthusiastic as Ciprian is about hash IDs.  For example, if I change some text in a paragraph, the identifier for that paragraph has now changed -- even though it is still the same paragraph within the page.  If I am using random codes, I want them to be affixed and then remain, so that changes to that I as the user can choose whether the change is significant enough to warrant a new random code, or whether links to the paragraph should still remain intact.  This applies doubly so for document edits:  Making a single edit to a document, to my thinking, should not mean that all pointers to the document now need to be updated.  Practically speaking, I'd like that control to be closer to the editor of the document, about whether everybody must now get a new link to the document, or if the old links should still point to the same thing.  I would like the writer of the document to be able to export specific versions of the document, or not.
