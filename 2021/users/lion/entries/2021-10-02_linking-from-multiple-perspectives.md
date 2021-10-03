# Linking from Multiple Perspectives

Lion Kimbro
2021-10-02

## <a name="conflict">The Conflict: Atom-sized Links, or Collective Links?</a>

Ciprian and I have been discussing links, and have hit a difference:

While I would model a feed like so:

```
feed: (ID of feed)
articles:
  - (ID of article #1),
  - (ID of article #2),
  - (ID of article #3),
   ...
  - (ID of last article)
```

...Ciprian is of the mind that each article should be linked like so:

```
feed: (ID of feed)
article: (ID of article #N)
```

...with one link, per article.

Ciprian challenged me.  He said (paraphrasing):  "Lion, you'd do feed-to-articles all as one link, but you would model article-to-author as a one-off link, the way I would do it.  Why wouldn't you do it author-to-all-articles?"

(Ciprians exact text was: "*Looking back at your example (feed, post, author), and in support of my reasoning why I think the feed-article as you've modeled is kind of wrong (at least as an example), why did you decide to use left-right for post-author, but multi-link for feed?  Don't both relations look exactly the same?  Why not multi-link for both?*")


## <a name="pragma">Pragma</a>

I first had the impression that -- it's all about the pragmatics:  When I'm publishing a feed (for example, rendering a web page of articles,) I want to see the list of all of the articles in the feed -- at least, all of the articles that are going to be presented today.  While forming that article, I thought, "Heck, why NOT throw in the author as well --"

```
feed: (ID of feed)
articles:
  - article: (ID of article #1)
    author: (ID of author of article #1)
  - article: (ID of article #2)
    author: (ID of author of article #2)
  - article: (ID of article #3)
    author: (ID of author of article #3)
   ...
  - article: (ID of last article)
    author: (ID of author of last article)
```

That's even more pragmatic.

But I also get that, -- if I was looking at an article, and trying to figure out who the author of the article was, and had only this data structure to work with -- it'd be incredibly annoying:  I'd have to look through the data structure to find the list index that featured the article, and then look at the corresponding author.  That's counter-pragmatic.

The most pragmatic thing for *that* query is a simple link from article to author, and vice versa.

(And similar for the perspective of the author -- if you were trying to find everything an author wrote, and you had in the mix a bunch of these "feed-article-publishing" link structures, then you'd have to search through each item and find the specific article(s) that the author was responsible for writing.  Not pragmatic at all, for that query.)


## <a name="both">Do Both - They're Different</a>

This led me to a particular view:  Both can be included.  Or one.  Or the other.  It's all about the pragmatics.

Then I realized:  If I took an individual like Mark Twain, I can imagine a data structure that says, "This is the list of books that Mark Twain wrote in his entire life."  It would include all of his books.  It might structure that information by category, it might structure that information by time.  But it would not include his personal letters and correspondences.

Now if you had individual identifiers not only for Mark Twain and his books, but also for letters he wrote to people, then for each of those items, there might be a statement: "Mark Twain wrote this letter," or "Mark Twain wrote this book."  They would be individual links, just like Ciprian was talking about.

Those are subtly different meanings.  It's not referring to a collected information: "This is the collection of Mark Twain's written books."  It's referring to the individual links, and commenting on them.

Now the problem could be named: "With the individual links, I can comment on them and annotate them, individually.  I can't do that with the collection of all books Mark Twain ever wrote."  But I could say the same in reverse as well:  "When you comment on and annotate them individually, you can't comment on them as a collective whole."

## <a name="hegel">Data Hegelian</a>

It may feel like a duplication of expression.  Sloppy, even.  To this I say, "It probably is."

I think that data is messy and fundamentally ambiguously.  If you say I was born on August 29th, 1977, there is a question: "Per what time zone?"  If you name the minute I was born, there can be a question of the second, and how "being born" was defined in the place and time, and if there could have been any inaccuracies.  If you say my name is Lion, one can ask, "Well, was that your given name?  Who calls you that, and in what circumstances?"  I apply Hegel's insights about the intrinsic inconsistencies within reason, to data.

I think that data translators will be normal:  "If you see this schema, then look for these other schema and use them if they are there, and if they are not, create them."  Yes, this will create reduplication, and of course, there will be systems to react to refactor reduplications, but such is life:  Everybody has to go to school and learn how to read, it is not the case that one person can learn to read for everybody else, and solve that problem for them.  And it doesn't always work.  There is a certain amount of reduplication and failure implicitly in life processes.

As a "data Hegelian", I am skeptical of [OWL, of semantic reasoners](https://en.wikipedia.org/wiki/Semantic_reasoner) as a whole.  I believe in translators and mistakes.  It is not that semantic reasoners work by machines that I have a problem with -- it is the implied faith that data can be freely transformed and that this will "work," that I have doubts about.

I am not looking for a [first normal form](https://en.wikipedia.org/wiki/First_normal_form) for data representation.  I am looking for pragmatic solutions to expressing and reading data that make programmer's lives easier, and help contribute to the flow of civilization.  The Japanese word for "complexity" is 「複雑」(ふくざつ) "fuku-zatsu," -- and it means: "duplicate randomness."  I'm fine with it.

I think people can, will, and should render out linking structures and data structures in whatever forms work for them, to solve whatever problems they have.  For some, that will mean highly atomised data.  For others, it will mean big and complex aggregate structures.  It matters for the specific task, but I don't think it matters in terms of "will we be able to express thoughts in data, or will we work ourselves into a dead end by persuing one path or the other."