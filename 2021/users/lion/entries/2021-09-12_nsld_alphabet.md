
# NLSD Alphabet
Lion Kimbro
started 2021-09-10
published 2021-09-12

## <a name="nlsd">What is NLSD?</a>

nLSD v1 was a data format for serializing graphs that extend across file boundaries.
I wrote nLSD v1 in 2004, [evidenced by the WayBack machine.](https://web.archive.org/web/20041014020231/http://onebigsoup.wiki.taoriver.net/moin.cgi/nLSDgraphs)

Recently, I revisited the concept, renamed it "NLSD" (all caps now,) and have altered it somewhat, for nLSD v2.  (I haven't documented it yet; I'm still working on it.)

## <a name="premise">Basic Premise</a>

The basic premise on NLSD is of a graph expressed through numbered nodes.  For example:

    0 S Key 1
    1 S Value 1
    2 S Key 2
    3 S Value 2
    4 S Key 3
    5 i 400
    6 D 0 1 2 3 4 5
    7 S START
    6 M 7

The line `0 S Key 1` means, "Node #0 is a string, that string is `Key 1`."  The following lines declare that nodes #0, #1, #2, #3, #4, and also #7 are strings.

The line `5 i 400` means "Node #5 is an integer, it's value is `400`.

Then line `6 D 0 1 2 3 4 5` says that Node #6 is a dictionary, and it has keys and values in a certain pairing.  It ends up evaluating to `{"Key 1": "Value 1", "Key 2": "Value 2", "Key 3": 400}`.

The final line `6 M 7` is special, and marks a meta-annotation of the dictionary at node #6.  "Node #6 has a meta annotation by Node #7, which is a string that reads START."  That could be interpreted to mean that node #6 is the "START" node, although the meaning of that interpretation is not specified by NLSD.

## <a name="types">Basic Alphabet</a>

Presently, in NLSDv2, the basic node types that I have supplied are as follows:
* numbers
  * **i** -- integer
  * **f** -- floating point
* lists
  * **L** -- list
* strings
  * **S** -- string
  * **b** -- bytes
* dictionaries
  * **D** -- dictionary
* bool
  * **t** -- true
  * **f** -- false
* null
  * **z** -- null
* meta
  * **M** -- meta (links one node to another)

The "M" link makes it possible to vastly expand the range of operations, because you can attach pretty much any meta-data to any node.


## <a name="expanded">Expanded Concepts</a>

I started discussing it in my internet office [(Lion's Internet Office Discord Server,)](https://discord.gg/V8wDBh8d)

As I discussed with Ciprian Craciun, we came up with various ideas for different primitive elements.

Our exploration was essentially, "If higher level concepts were put into nLSD, what would they be?"

### <a name="additional-basics">Additional Basic Types</a>

One was additional basic types.

* additional basic types
  * **sym** -- symbols -- these are strings that meet tight constraints (such as no spaces), and are used to represent program-native identifiers of one kind or another, such as in LISP

### <a name="expanded">Transclusion Codes</a>

Another was codes about transclusion or inclusion.

* transcluding
  * **!** -- transclusion
  * **a** -- A name aliasing
  * **<** -- immediate include

The "!" node would mean, "Insert another remote graph into this graph, at this point."  Whether that is done progressively, in response to a proxy object being turned, whether that patches the original data or simply operates via a link object, or however -- is largely an implementation specific decision.

This node type existed in [NLSD v1](https://web.archive.org/web/20041014020231/http://onebigsoup.wiki.taoriver.net/moin.cgi/nLSDgraphs), where it was called  "REF".

If you transclude into a another NLSD file's graph, you probably want to target a specific node in it for linking into.  That led me to think, "There should be an A name aliasing for nodes as well.  Numbering for nodes might change, but an A name assignment would be explicit, and make for a good mnemonic to support attachment."

Instead of having "A" name aliases, though, another possibility is to allow nodes to have words for names, not just numbers.

*(note to self: it strikes me that -- if you want targets to be able to link back into the first graph, it's imperative that each graph have a unique identifier; that way, they can address one another independent of where they are sourced from)*

"<" is like "transclude," but means to do it automatically, as part of reading the document, so it could reasonably be called "include," or "immediate include."

### <a name="entities">Entities & Links</a>

Ciprian Cracium has been exploring ideas inspired by a book on "the Associative Model of Data."

<a name="associative-model-of-data">Associative Model of Data:</a>
* [Wikipedia: Associative model of data](https://en.wikipedia.org/wiki/Associative_model_of_data)
* [The Associative Model of Data, 2nd Edition, by Simon Williams](https://www.scribd.com/document/79742797/Associative-Model-of-Data)
* [Associative Data Model and Context Maps, article, by Mingui Han](https://spectrum.library.concordia.ca/1663/1/MQ64083.pdf)

I have not explored this model deeply, and am presently skeptical, but I am also interested.

Regardless, we developed these concepts as they would appear in NLSD:

* entities & links:
  * **E** -- entity -- the node is an entity, and it's unique identifier is specified as an argument
  * **L** -- link -- a link, with a left side and a right side, and possibly also an argument
  * **S** -- schema -- the node meets a schema, and it's schema is identified as an argument -- (we imagined this could be used both for Associative Data Model "Entities" and "Links," and "primitive data" as well)

Note: *"S" for Schema conflicts with "S" for string; so it's likely that strings would be represented with lower-case "s", which would match "b" (binary).*

### <a name="lightweight-location">Lightweight Location</a>

Isolating Entities is interesting to me, none-the-less:  declarations that "Here is this unique thing, and I'm describing it."

I have questions about what happens when entities are declared differently in two different documents, though.

It led me to imagine a general "Global" data declaration node type.

* global declaration
  * **G** -- global declaration -- "This data item is the root of a declaration of an item that is globally identifiable with this string" -- and that string would be a GUID or a [tag URI](https://en.wikipedia.org/wiki/Tag_URI_scheme) or something like that
  * **U** -- (same, but "Universal") -- because maybe our ambition stretches out beyond 地球, planet Earth

With "G" (or "U"), while parsing a document, you could quickly isolate and index the items that are claiming to make authoritative assertions about the global space.  As I envision it, you would NOT use this on a link to a global claim; you would only apply this on the global claim itself.

I would expect that the module of code that retains the data collection of nodes and indexes into the nodes, would also keep track of where a particular claim came from.  So if you asked for data about a particular GUID, you would get back a list of: "This source says X, this other source says Y, and this still other source said Z."
