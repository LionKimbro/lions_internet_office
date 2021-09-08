

# Programming Philosophy
Lion's particular philosophy of programming.
2021-09-06

## <a name="preface">Preface</a>

This is a highly situated philosophy.  It's not intended for "all time"; rather, it reflects my immediate, situated, deeply personal position.

Also, the intended audience for this document is people who have spent at 20 years programming, 10 years minimum, and ideally at least 30 years old.  For example, when I say that "abstraction-focused programmers recognize only three numbers: [0, 1, or infinity,](https://en.wikipedia.org/wiki/Zero_one_infinity_rule)" -- I'm not going explaining what that is for readers.

## <a name="principles">Principles</a>
* ["Big Picture" Principles](#principles-big)
  * [Motorcycles, not Tanks](#motorcycles)
  * [Locate Power Density](#power-density)
  * [Write The Right Foundation](foundation)
  * [Relentlessly Delete Preconceptions](#delete-preconceptions)
  * [Make Machines, not Abstractions](#machines)
  * [Keep Strictures in the Mind, not the Code](#discipline-in-the-mind)
  * [Clear Ideas > "Code Reuse"](#ideas)
  * [Notation > Feature](#notation)

* ["Small Picture" Principles](#principles-small)
  * [Global Variables > Parameters](#global-variables)
  * [Probes > Tests](#probes)
  * [Integration > Interface](#integration)
  * [Let Promises Do Their Work](#promises)
  * [Write It Yourself](#write-it-yourself)

"Big Picture" principles are about the software architecture, the big picture about how you write code, are about the design of software and "what is programming, really?" type stuff.

"Small Picture" principles are principles that have to do with, "OK, how do you write this specific bit of code?"

## <a name="principles-big">Big Picture Principles</a>
### <a name="motorcycles">Motorcycles, Not Tanks</a>
*"Also, it's a kayak, not a Titanic. The priority is user developers, not 3rd party developers."* -- [Terry A. Davis](https://en.wikipedia.org/wiki/Terry_A._Davis), [the TempleOS charter](https://web.archive.org/web/20170110084834/http://www.templeos.org/Wb/Doc/Charter.html#l1)

Most software systems we use day to day, are written like tanks.  They are gigantic, hefty, slow, full of myriad redundant systems, focused on **security** and **safety** foremost, **rigor** and **completeness**.

What I am interested in, however, are qualities such as **speed**, **adaptability**, and **agility**.  The software systems I write, are more like motorcycles.  Or [Crazy Karts](https://www.youtube.com/watch?v=eQSICMN4tM4).

[Chuck Moore](https://en.wikipedia.org/wiki/Charles_H._Moore) once said, (paraphrasing, from memory:) "Most people's programming languages do *everything*.  What's great about my system, is that it lets you do *anything*."  That is my emphasis, as well.

There are trade-offs, to be sure.  But this is where my emphasis lies.

### <a name="power-density">Locate Power Density</a>
As such, I am deeply interested in what I call "power density."  Or it could be called the fulcrum.

What is the small thing that can create a big change?

[Terry Davis](https://en.wikipedia.org/wiki/Terry_A._Davis) (whom I revere) wrote about this as a guiding principle.  I can't find where immediately.  He referred to the apocryphal story of Nasa spending millions to design a pen that would work in space, -- whereas the Russians just used a pencil.  That story isn't true I've heard, but regardless -- the principle behind it is sound, and it's at the center of my efforts.

### <a name="foundation">Write The Right Foundation</a>
Every solution is written on a foundation.  I think we spend too little time thinking about the right foundation.  Then we write something.  Then we write more something.  The foundation wasn't right, so we have to write even more something.  Now we're so invested in what we wrote, -- well, we couldn't go back to the foundation, right?  And so rubbish heaps on top of rubbish, to make up for a poor foundation.  And then when it's time for new software to be written -- what do we do?  We recreate the same thing, all over again, -- because existing systems were all made to work with the previous one.

Instead, what I want to do is either (A) think about the right foundation, and build on that, or (B) experiment with an arbitrary foundation, any foundation, build something, and then tear it down, and use the lessons learned to create the right foundation.

You know you've found the right foundation when you can write whatever you want to write on top of it, and it comes out elegant, easy, builds up fast, and you can experiment and play around with the design aplenty.

You know you have the wrong foundation when you find that you are writing the same code over and over and over again, when development is a slog, when it's not fun, when it takes days or weeks or months to make simple things work -- that's all indications of a faulty foundation.

We have **a lot** of faulty foundations in the software world.

It's amazing that many of these fault foundations live not primarily in our software code, but in our very thinking, to start with.

#### Case Example: from XML to JSON

I remember when XML was spreading around, in the early 2000's.  Everything was being built on top of XML.  It was difficult, cumbersome, ugly.  There were these big libraries going around.  And then there was SOAP, for RPC.  It was built on top of XML -- as if, that were a selling point.

Eventually, though, JSON was located.  JSON hit a sweet spot.  We started writing things on top of JSON.  Life got so much easier.

I think XML is a simply fantastic tool for text markup.  But it's not what we needed.  We didn't need to markup text.  What we mostly needed to do, was to shuffle around structured data.  It's not that there's something fundamentally wrong about the foundation of XML.  It's just the wrong foundation for the task.  So thinking about foundations and developing foundations is critical to programming.

I think most all of the software we write today, is written with little attention to foundations.  Expedience becomes the name of the game.  But I think that we need to pay far more attention to foundations.   

### <a name="delete-preconceptions">Relentlessly Delete Preconceptions</a>
[Chuck Moore](https://en.wikipedia.org/wiki/Charles_H._Moore) was the master of this one.

I'm not just talking about layers of code -- library Z calls library Y calls library X.  I am talking about that.  But it's not the only thing I'm talking about.

I mean, Chuck Moore would delete concepts like files, and filesystems.  Do you really need them?

Chuck Moore deleted the concept of function parameters.  Do you really need them?

Do you really need local variables?

Conventional reasoning would say yes to all three of the above.  But Chuck Moore proved that you can definitely side-step all of these.

* Files and filesystems can be replaced with "blocks", which are just one-page sections of memory, and with an integrated editing system for working with them.
* Function parameters can be replaced by global communications systems, and 0-2 stack parameters.
* Local variables are similarly unnecessary.

"That could only work for small-scale systems!"  And yet Chuck Moore wrote enormous systems without these elements.

I'm not saying that all forms of parameterization are wrong, I'm not saying that filesystems are wrong, I'm not saying that local variables are wrong.  I make absolutely no such commitments.

I'm saying:  We should be open to questioning our assumptions, and we should look for opportunities for efficiencies wherever they can be found, and we should recognize that there are costs implicit in the decisions that we have made, that I see people routinely ignore and take for granted.

On my iPhone, photos taken from the camera just go into one big list of images.  You can view them by location, you can view them by date, you can view them all kinds of ways.  But there's nothing automatic or necessary about the concept of a "file system."

### <a name="machines">Make Machines, not Abstractions</a>

When most people program today, they usually think about what "abstractions" they are programming in.

They think about the classes, and the objects, and the methods.  They think about what data is kept in what class.  They think about how to "abstract" this, and how to "abstract" that, dividing or grouping these data collections and functions into what "abstractions."  What is being hidden?  What is being exposed?  This kind of analysis.

And these "abstractions" lead people into a world of mathematics.  There are three numbers:  0, 1, and Infinity.  There is no such thing as "four" of something -- four is merely a special-case instance of "infinity."  This kind of mathematical way of reasoning about things lead into entire worlds and castles made entirely of abstraction.

Instead of air and clouds, I am interested here in earth and steel.
Instead of infinite memory space and linked lists, I am interested in memory dimensions and assembly code instructions.

When I first think about a task, I ask: "What are the material needs for this?  How much memory is required?  How big are these things?  What kind of throughput do I want to support?  What can the machinery handle?"

I know about the existence of numbers such as 2, 3, and 4, and 50 ms.  1,000 and 1,000,000 mean something very different to me.

Furthermore, I think:  "What is the real problem here?"  I think about the problem.  I think about what needs to be moved where.  I think about what needs to be linked to what -- in essence.

Only after I have thought about all of this, do I then look at the materials on the ground.  And then I write a foundation, and that foundation looks like a collection of machines.

I don't care at all about classes, about objections, about files.  I don't care at all about widget libraries.  I don't care at all about tools and factories and APIs.

I care about the problem.

And then I focus on a foundation, using the various things that are lying around, in order to make a world that is fit for the solution to the problem.

That can look like a DSL, but it does not have to.  That can look like a data structure that correctly holds the dimensions of the problem, but it does not have to.  That can look like an assemblage of UNIX tools, but it does not have to.

The key is to start from the problem, and then assemble and design the tools that would make the resolution of the problem easy, rather than starting from the tools and the environment, and hoping to reach the problem.

I always see the solution to the problems in terms of diagrams, and then I assemble or write the machines that solve the problem.

And as my understanding of the problem develops and changes, and as I work on what the problem really is, I change the tools and the environment -- rather than adapting things to the tools and to the environment.

It turns out that I really don't care if I can have an infinite number of list items.  I will never have an infinite number of list items.  I might have 1,000,000.  I might have 100,000,000.  I might have 2,000,000,000,000.  But I will never have an infinite number of list items, and I am not going to work to make sure that I can support an infinite number of list items.

I want to be focusing on constrained problems that I have, and design the machines that will make that work.  I do not want to spend a single hour lost in software metaphysics about inheritance, and trying to rustle out the true inner "essence" of things.

As another example of this, I do not believe in the existence of metadata.  There is only data.  All data is about the world, and the world includes data as well.  There are concrete machines that index data and produce indexing data, or there is not.  I take all of this for granted.

I appreciate mathematics and the power of mathematics.  When I think about the problem, I use diagrams, and write equations.  This is not an attack on mathematics and conceptual schema.  It's not an attack on big ideas and grand thinking.

But it is a leeriness towards someday-maybe in-principle type thinking, and a focus towards the material, the concrete.  Don't write hooks.  Don't hold the design open indefinitely.  Don't write for the unexpected, and limit your expectations.

And then an opening towards machinery:  Recognize that everything is a machine, and write the right machines for the foundation that you need.  It may look nothing at all like what your programming language offers.

If you don't need classes to implement what you are writing -- if it would be implemented just as well just using raw functions -- then why in the world are you using classes?  Are you doing it because the programming language provided it and everybody's doing it?  Or was it truly demanded by the problem?

### <a name="discipline-in-the-mind">Keep Strictures in the Mind, not in the Code</a>

Often times, our programming languages introduce various mechanisms for enforcing strictures.

Some of these I am fine with.  For example, in Python, there are tuples (cannot be edited) vs. lists (the same thing, but editable.)  In Python too, there is automatic memory management.  In C, you cannot redefine a function at run-time.

But I find that, outside of a small set of strictures, very often, strictures create more problems than they solve.

"How then do we keep discipline in the code?"

My approach is to keep documents about the code, and to use them, whenever I program.

Importantly, I do not rely on comments in the code to keep this information.  There is too much information to note, and the ratio of comments to code would obscure the code itself.

One of the most important of documents is [a data dictionary, described further in the section on global variables further on in this document.](#data-dictionary)


### <a name="ideas">Clear Ideas > "Code Reuse"</a>

"Code Reuse" is a sham.

There are libraries that we rely on, and libraries that we don't.  There are frameworks that we build things in.  There are programming languages and these languages provide for loops and data structures.  OK, these things are "code reuse."

But the idea that you can write a class once, and then reuse it anywhere, -- has never existed, and never will exist.  Code is situated and particular and always will be situated and particular.

Even plug-in systems are questionable.  Because the system changes, or the plug-in changes, and then you get a new adaptor.  Or you want something from the other end of the interface, and it isn't there, and so you have to start changing things if you want to get what you want, -- etc.,.

Furthermore, to make the plug-in system work, you start having to keep a number of promises that you didn't even realize that you had made, ...

Overall, I think that code reuse is not really a thing.  All code is "throw-away" code.

I think that my favorite "blog engine" would be a website that said, "Here's how to write a blog engine."  It would say, "Make a thing of code that does this, and then does that."  "Make another thing of code that does this, and then does that."  Maybe there'd be some pseudo-code.  But there wouldn't be an implementation.

It'd be like watching a Bob Ross video on how to paint a particular kind of landscape.  You don't try and create an exact replica of what Bob Ross painted, and you don't *rely* on making an exact copy of what Bob Ross painted.  Instead, you try and get the general flow, and how the tools work, and what things are important and what things are not important, and the general spirit of doing the thing.  And if you need a "happy little tree" where there wasn't one before, you can put it in, because you're familiar with the brushes and the painting.

It's not "off the shelf."  And when you try to write a system that works adaptably "off the shelf," -- you quickly discover that it's far harder than writing a particular thing.  And it can be maddening, because you need something that it wasn't written to support.  Now we are back on Chuck Moore's point about "My system lets you do anything, rather than doing everything."

In my life I have only seen a few instances of "here's how to write an X."  Instead, I see repository after repository of code, and promises of pluggability and extensibility.  I wish that as a culture, we shifted more to:  "Here is how to write a wiki engine.  Here is how to write a blog engine.  Here is how these algorithms work."

I am fine with an implementation as a reference, but trying to infer the conceptual from the implementation I often find difficult.  On a few occasions in my life, I have done a "deep dive" into a system.  But I much prefer the book, like the Usborne books, that explain conceptually what's going on, and how to write your own adventure game, and occasionally referencing the specifics of a working implementation.

There is nothing nearly as reusable as a clearly expressed idea.

We shouldn't look for "code reuse," anywhere else.

### <a name="notation">Notation > Feature</a>

This is a very particular point, but it is very special.

I focus far more on *notations* than I focus on, say, "language features."

The star example of this is regular expressions.

A single regular expression would be, if you expanded it out, very often easily hundreds of lines of code, if not thousands of lines of code.  And yet the whole thing can be 40-60 characters long.

This is an extraordinary power!  What an incredible point of leverage!

Now -- why do we always write our programs in ASCII?

Why do we not use icons?

Why do we not use spatial arrangement?

I have another entire essay to write on this subject.  And I have written other essays on this subject.

[The last time I wrote about this, was on CommunityWiki:SchematicMedium.](https://communitywiki.org/wiki/SchematicMedium)

I won't write about it more here.

But I ask that programmers please, please, please reconsider the notational system by which we express our programs.

If mathematicians wrote everything out in text files and in ASCII, I think mathematics would be centuries back from where it is today.

There is no reason that mathematical summation notation would not be valuable to programmers.  And yet we hear endlessly that "text files are the final form of computer programming."

It is madness.  We need to construct new mediums for expressing programs.

I did not say new programming *languages.*  Which we do, regardless.  But rather, at a layer deeper, it is essential that we construct and focus on *new generic mediums* for the expression of new programming languages within.

One of the sad things is that -- whenever somebody creates a new programming language that stretches out beyond the limits of text files -- let's just pick SmallTalk out of a hat for instance -- that medium that the programs are expressed in, -- is totally and completely married to the programming language that it was made for.

I think instead that what we need to do is create new mediums to express programs in, and then allow for a wealth of programming languages to be expressed from within that medium.

And so this is what I mean when I say that I am focused on *notation* -- the system and conventions by which we express programs.

## <a name="principles-small">Small Picture Principles</a>
"Small Picture" principles are principles that have to do with, "OK, how do you write this specific bit of code?"

### <a name="global-variables">Global Variables > Parameters</a>

When I call a function, I call it with one of of the following:

* 0 arguments -- aka a "nullary" function
* 1 argument
* 2 arguments

The essential thing to understand here is that I reserve function parameters for things that *vary rapidly.*

Function arguments should not be used to communicate *context.*

How should context be communicated?

Context should be communicated by means of **globals**.

Those globals can include (but do not need to include) an explicitly managed **stack**.  That means *thinking about the flow of information at an architectural level.*  Remember the big-picture principle -- think in terms of *machines,* not in terms of "abstractions."  There is a flow of information through your system.  You have to think about that flow.  It is a burden that you must pay.  But once you've paid it, now you discover that you can use parameters *as parameters*, and not as context transfer.

#### <a name="turtle">An Example: Turtle Graphics</a>

Typically, people are following a model of abstractions, and they create a Point class, a Rectangle class, a Circle class, and whatever on and on.

But Turtle graphics are also a valid way of working with graphics, and often far more expressive and powerful.

I once saw an amazing talk -- it seems to be lost to the Internet, but [the notes from it are still with us](https://www.academia.edu/4903069/Seven_Ways_To_Use_Turtle-Py_Con2009) -- about how to use the Python Turtle module to create live interactive systems and drag-and-drop interfaces.  It turns out that the turtle can tell when it is clicked, can be made to shape like a button, and that you can have multiple turtles on the screen at once.

The arguments to turtle instructions are typically just one or two arguments:
* FD 10
* RT 90
* PEN UP

The context is kept in global state.

For all the prohibitions and warnings of madness and chaos and incalculability that arise from "state," I have found that (A) my programs work just fine, and (B) "state" is just a different level of management, one to be thought and handled just like any other domain.

I deeply appreciate the crispness that appears in thinking about the program, when I have zero, one, or two parameters to a function call.

#### <a name="nullarity">Nullarity Functions</a>

And a zero-parameter function is like a gift from heaven.  All manner of interesting things can be done with zero-parameter functions.  They are infinitely transposable and remixable.  They are the ultimate "event" class instance.

#### Exception: Syntactic Sugar

The only time I call a function with more than 2 arguments, is when the purpose of the function is to create a re-representation of something using some language syntactic features.  For example, something in Python like:

    def foo(a, b, c, d="bar", e="baz", f=100, g=50):
        return {"A": a, "B": b, "C": c, "D": d, "E": e, "F": f, "G", g, "X": 1000, "Y": 50, "Z": 1000}

The purpose of this function is specifically to be a kind of "syntactic sugar."

That's the only kind of place where I call a function with more than 2 parameters.

#### Learning to Use 0, 1, or 2 Parameters

It takes some getting used to.

And you have to think about "looping over a list of things" (and doing something with each item of the list) in a new way.  My explorations are not yet complete.  This is a field of active exploration for me.

But I encourage you to play with these ideas.


#### <a name="data-dictionary">The Importance of a Data Dictionary</a>

It's critical that -- when you use global variables, that you keep a **data dictionary.**

A data dictionary is a document that describes your global variables.

For each global variable, I keep track of:
* the name of the global variable, as it shows up in the program
* a human readable title for the global variable
* a single phrase that briefly states something notable about the global variable -- I call it a "hook" phrase
* a description of the global variable -- what it is for, what it is about; roughly 1-2 paragraphs long
* the global variable's type -- for example, "integer"
* the global variable's "sub-type" -- what kinds of valid values are in it, what it's limits are, etc; -- for example, "a numerical year, such as: 2021"
* what rules must be followed when reading the global variable, and what rules must be followed when writing to the global variable -- this can be very simple ("write once, read anywhere",) or very, very, very complex

The data dictionary is, very importantly, not a comment within the code-base.  It can be referenced from a comment in the code base, but it is not a comment within the code-base.  There is too much information that needs to be communicated about a variable, to neatly fit within the code as written.

Essentially, the strategy is <a href="#discipline-in-the-mind">to take the security rules out of the programming language, and into the mind of the programmer.</a>


### <a name="probes">Probes > Tests</a>

We live in an era of tanks, and all tanks must function according to specification.

But I work on motorcycles, unicycles, Crazy Carts, and the like.

I'm not so interested in a 100% pass test rate.  That 100% pass test rate means that the machine is completely in conformity with a complex and detailed spec.  If I change how I want something to work, I need to not only think about what that is, and I need to not only change the code, but I also furthermore now need to delete some old tests, fix some of the old tests, and now add a bunch of new tests.  That's quite a lot of work.

What I'm more interested in, is being able to see the innards of what my machines are doing.  I'm interested in, in real-time, probing the interior operations of my motorcycle.  I want to see pressures, counts, stress levels, buffer entries, all kinds of things.

In short, I'm far more interested in probing tools, than I am in tests and "completeness."  My project will never be complete.  It is something that is perpetually changing -- that is intended.

So probes -- not tests.

And I write my system in such a way that the probes can easily be written and easily monitor what is going on in it.  It's essential that the system make itself clear from the inside.

### <a name="integration">Integration > Interface</a>

I don't implement "plug-in" systems.

Instead, I write notes like:  "If you want to attach an X, Y, and Z, these are the places where you hook into it."  And by "hook," here, I mean, "This is the function that you attach a function call to," and "This is the table that you need to add entries too."

If something goes wrong, well, the system has probes, so you can see what's happening, and what the interaction is like, with your modifications.

### <a name="promises">Let Promises Do Their Work</a>

This one could also have been called, "Let systems fail."

Promises are extraordinarily powerful.  They don't require a simple line of code;  You just have to keep them.

And then when you break a promise, some kind of an error is generated, and the program breaks.

You know -- when you are motorcycling, and you do something wrong, -- you get immediate feedback.  Then you don't do the wrong thing any longer.

I don't inoculate Syntax Errors, in try: except: blocks.  I let them come straight to the surface, unfiltered.  It tells me that I put something somewhere wrong.

Now, this is not to say that it's wrong to write input-verification routines.  They are certainly valuable!  But those can be absolutely separated from the machine itself.  Have a piece of code that verifies the input, if you must, but then in the central part of the engine, *let the promise that the data is well-formed do its work.*

But if the input has already been verified, and if by whatever means, you have been told that the data coming in is of a certain type and should be correct, do not verify the input data any longer.  Let the promises do their work.  And allow the system to crash on a bad input.

### <a name="write-it-yourself">Write It Yourself</a>

There is such a thing as NIH syndrome -- "Not Invented Here" syndrome: The automatic rejection of anything that was not written in-house.  This can be extremely costly, and kill entire projects.

However, I have seen another extreme, which is "Invented-Anywhere-But-Here."  And that means that your problem must have been already thought about, and there must already be tools and trainings that neatly match to your problem, and somebody else has already anticipated it and made a solution that will work just great for your problem.

I've seen incredible wastes of opportunity performed -- months of project time lost, and subsequent crashes and problems and failures, -- all because we couldn't be bothered to write and manage 200 lines of code.  I have seen *configurations* of large systems that easily consume 10,000 lines of code, for problems that could have been solved with 500 lines of original code.  And it's not that these systems then require no maintenance.  They have huge security exposures, and they need to be updated and maintained and considered, just like anything else.  So I don't buy the argument that the 500 line of code local solution, "requiring maintenance," is much different.

Regardless of industrial efficiencies, my code is focused on speed, adaptation, and research.  So I skew towards: Write It Yourself.
