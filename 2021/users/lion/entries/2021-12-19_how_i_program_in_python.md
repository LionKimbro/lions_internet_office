# How I Program in Python

Lion Kimbro
2021-12-19
status: 1st draft, incomplete

These are some notes on how I write programs in Python.  It accords with [what I wrote about my philosophy of programming,](2021-09-06_programming-philosophy.md) but is much more practically focused, and specifically rooted in Python.

Here are the things I'm writing about today:
* **global-variables** -- how I use global variables in Python
* **modules > classes** -- how I use stateful modules, rather than classes and objects
* **stateful modules** -- how I use stateful modules to simplify APIs
* **making a theory** -- how I make "theories" of the code, to make incisive cuts that work amazingly well
* **notations & micro-interpreters** -- how I write small micro-interpreters in Python
* **not so tight!** -- sometimes specific names, but also sometimes reusable names
* **controlling sequence** -- how I control sequence of initialization and teardown in Python
* **avoiding gobbledygook** -- how I avoid gobbledygook in Python

I'm sure there's more to say, but I'm not focusing on completeness immediately.  I'm just focusing on some of the major features of my code and of my thinking.

(interrupting myself, from the future:) I want to note another thing very quickly here:  I wanted to put the section on "avoiding gobbledygook" *first*.  Because it's actually ***the most important principle,*** and so much so that the principles behind the practices *fall out* of ***that one principle***.

But I thought, "People aren't going to like that.  They will feel like they are being lectured at.  They won't get it.  And they want something tangible."  So, I want to present a choice to you.  You could read this just straight through, from start to finish.  That's how I've written it to be read, after all.  But I want to present an option to you:  Please consider skipping ahead, and reading the "avoiding gobbledygook" part first, and then reading through, and then perhaps rereading the avoiding gobbledygook part.  Because I think that -- regardless of whatever programming language you are programming in, that is *most important*.  And because there's such a fetish in software engineering for gobbledygook.  I believe very strongly it needs to be actively avoided.  OK.  And now on to something tangible.

## Global Variables

Let's start with the basics:  Variable access.

[*I love global variables.*](https://github.com/LionKimbro/lions_internet_office/blob/main/2021/users/lion/entries/2021-09-06_programming-philosophy.md#global-variables)  I know that this statement provokes ire, but my 5-second defense is: "*I've been programming for 40 years, and I haven't encountered the much-predicted doom.  To the contrary, I have seen the avoidance of globals wreck carnage on code-bases.*"  But I will argue this no further here.

Instead, I'm going to write about how I use globals in Python.

Now, Python does feature the idea of global variables.  But it makes them hard to use.

    x = 32  # a module-scoped variable
    
    def foo():
        global x  # use the module-scoped variable
        x = 10  # writes to the module-scoped variable

That is, every time you want to write to the global space, you have to declare that that is what you are doing.

Fair enough!  But notationally, if you are writing to global variables regularly, if this is a normal mode of interaction for you, you're going to have problems.

So in my programs, what I do is make a global dictionary `g`, that lives in the global space, and then I write into and out of that global dictionary, `g`.

    g = {"x": 32}  # a module-scoped variable "g", defining a value for "x", that is globally reachable
    
    def foo():
        g["x"] = 10  # writes to the module-scoped global variable "x"

Here I am taking advantage of the fact that on look-up, Python is happy to reach into the global space, and that from the look-up, I can perform an assignment.  Voila, easy-to-use global variables in Python -- provided you can put up with the `g["..."]`.

However, I feel that there's two problems with this:
1. There's too many characters involved.  (5 characters: g, [, ", ", and ])
2. It'd be easy to mis-spell something within the quotes.

I solve those problems with an invented system for Python *symbols*, a la Lisp.

(UPDATE, 2022-09-02: I invite you to read my essay on [Symbols in Python](https://github.com/LionKimbro/lions_internet_office/blob/main/2021/users/lion/wiki/symbols.md).)

For the program above, it would look like so:

    X = "X"  # symbol declaration: X
    
    g = {X: 32}  # global variables: X (init'ed to 32)
    
    def foo():
        g[X] = 10  # assigning 10 to global variable X

Symbols:
* are always expressed in capital letters
* always point to an interned string that matches its name

Now, a sensible complaint is: "Ok, while I get your picture here, it seems cumbersome to have to make a symbol for every variable in your program."

I'd be inclined to agree, ... *except*, ... that I believe that *I derive so much benefit* from the use of globals (and symbols generally) in programming, that I am willing to pay the cost of writing symbols into Python programs.

I don't consider the cost of initializing the g-var to be a cost.

"*g-var*" is my name, specifically, for a global variable that is stored in the global dictionary named `g`.

I think it is neat and tidy and right to list all g-vars together, and to give them initial values.  If a g-var needs to be programmatically set up, (for example, a function call is required to resolve the value of a g-var,) then I might initialize the value to `None`, and then in a setup function (perhaps: `setup`), assign it to something other than None.

The g-vars declaration is also a good place for a short comment about what the variables are for.

    FOO = "FOO"
    BAR = "BAR"
    
    g = {
      FOO: None,  # str -- name of widgets in cyberia
      BAR: None  # int -- number of quantz last detected
    }
    
    def setup():
        g[FOO] = other_module.foo("blahblah", 10)
        g[BAR] = other_module.run_query()

Now if there is a list or dictionary that is always going to be around, there's often no reason not to simply establish it in a global variable:

    foo = []  # accumulated list of numbers
    
    def add(n):
        foo.append(n)

If that list is not going to be re-assigned (-- and: I use permanent standing lists, far more this most other Python programmers it seems to me, -- I'm not entirely sure why this is,) then this is perfectly workable.

Remember thought that this is a global list.

Don't do this:

    def reset():
        foo = []  # NO!  This creates a local list, and doesn't even touch the global list.

You do this instead:

    def reset():
        foo[:] = []  # empty out the global list

When I am using lists that are defined in a module, my default assumption is that this list is a permanent list, with its own persisting id (`id(foo)`), and I think carefully before reassigning a name that is pointed at a list.

The same goes for dictionaries.

    bar = {}
    
    def add(k, v):
        bar[k] = v
    
    def reset():
        bar.clear()

Using permanent objects (like global lists and dictionaries that won't be re-assigned) can be enormously helpful: You can keep pointers to them, and they remain valid even as the list is transformed.

And that's basically how I do global variables in Python.

## Modules > Classes

I think I could write a whole book on this, and it might be worthwhile.  There's a lot of interesting details and possibilities and methods.

But I'm going to try and focus on the basic idea here which is that:  Modules are much better at grouping functionality, than a Class.

I'm not going to articulate *why*.  That's a long argument with lots of twists and turns.  I'm just going to describe: *How.*

### Questions People Have

I think it's actually fairly obvious on how to group functionality with modules:  You just put functions and global data into a module.  That's it.

But I anticipate some questions, like:
* How do you handle the situation of multiple things?
* How do you handle inheritance?
* How do you handle poly-morphic relationships?

Now these questions evidence to me the mind of someone who is programming in an Object-Oriented way.  I'm okay with that, -- that is natural, given the contemporary environment for programming.  And these questions have an origin in a real place -- there are definitely reasons to run simulations of lots of things interacting that all look alike, for example:  I encounter that a lot in my programming actually.

But the first thing I want to note is that there's a lot more to programming than handling simulations of lots of things interacting that all look alike.  I'd guess that that might represent 10-30% of programming, and not 90-70% of it.

There is a kind of "de-colonization of the mind," that I think has to happen, with respect to OOP.  Honestly, I think most people would be well served by spending a few months just programming with only using function calls and dictionaries, to see the world outside of the grasp of OOP.



Now the obvious and most straightforward replacement of a Class with a module, is a Singleton.

### Method #1: the Singleton Replacement

The most obvious application is the "singleton."  In Object Oriented world, that means a class for which there should only ever be a single instance.  Well, that's obviously just a module.

### Method #2: "Multiple Instances"

For me, what is commonly called an "object," is instead, a bundle of data.

    D = {FOO: 13,
         BAR: 16}

Now, that would be an "object" in object oriented programming.  But for me, it's just a dictionary.

What are the advantages of using a dictionary, over an object?

* You can use all of the methods of dictionary iteration and manipulation.
* You never have to touch hasattr, getattr, setattr.
* You can use anything at all that works with dictionaries, to work with the data.

The artificial distinction between an "object" and a dictionary, I find very little use for.

The only real advantage I find with objects, is that you get a nice namespace for calling functions based on a lookup of the type of the object. When you type `foo.method()`, it's looking at the Class of `foo`, and then looking for a function named `method` indexed under that class, and then calling that specific function, with `foo` as the argument to it.  Being able to access a function with a shorter name, rather than a longer name, is, I am not going to lie, a very nice thing.

And I think that's about it.  I think that that is the one real advantage, that I think is an unambiguous good, with object oriented programming.

Everything else is pretty much a pain in the ass:  Whether that's inheritance, and trying to figure out and maintain the lines of causality of an inheritance tree, -- or whether it is polymorphism, -- "let's see what this code will do, ..."

The thing is, pretty much anything you would want to do: You can do.  If you want polymorphism, with my "instances," it's very simple:

    D = {FOO: 13,
         BAR: 16,
         BARK: bark_fn}

So when you want to BARK with D, it's:

    D[BARK](D)
    
Maybe it doesn't need an argument.  Maybe it's just:

    D[BARK]()

When does that happen?  When it's something like an event.  I use nullary functions all the time.

How about inheritance?  I very, very, very rarely, need inheritance-like features.  But there are a few ways to implement inheritance, if your problem is best served with inheritance:
1. You can clone an existing dictionary, and then customize on top of it.
2. You can keep a pointer to a parent, (perhaps: `D[PARENT]`), and then default to it, when you are trying to resolve a value.
3. You can keep a pointer to a list of functions, (perhaps `D[VTABLE]`), and then use that, when getting a function to call.

An example:

    NAME="NAME"
    URL="URL"
    TAGS="TAGS"
    
    data = []  # list of all objects
    
    def entry(name=None, url=None, tags=None):
        return {NAME: name, URL: url, TAGS: tags or []}
    
    def add(D):
        data.add(D)
        notify_something()
    
    def print_one(D):
        print(f"NAME: {D[NAME]}  - URL: {D[URL]}  - has {len(D[TAGS])} tags")
    
    def list():
        for D in data:
            print_one(D)

This is kind of a silly example, but it demonstrates keeping track of multiple objects, and working with them through a module.

    module.add(module.entry("Slashdot", "http://slashdot.org/"))
    module.add(module.entry("Github", "http://github.com/", ["programming", "github"]))
    module.list()

Here are some things you could do with it:
* Make an access function `get(i)` that returns an entry from data.
	* You could make it return a copy of the entry, so that it can't affect the one in the list.
	* You could make it return the actual entry, and leave it to the programmer to be able to modify it.
	* You could *not* write `get(i)`, and encourage the user to directly index into `module.data`.
	* You could make it so that `get(i)` keeps a log note somewhere, when the item is indexed.

Notice also that writing the code this way, makes it easier to work with the entire collection of all of the data items.  If you had `class Entry`, then there's the question: Where do you put the code for listing *all* of the items?  Usually, that question is discouraged even -- because, "Well, all of *which* items..?"  The implication is that you shouldn't look at the objects as a set.  But I find that most of the time, I actually do want to be able to consider all of the objects as a set.  Why then are we typically conditioned to not looking at it that way?

Another note.  People often say, "Well, the code isn't *flexible*.  For example, how do I attach an observer to this?"

But the code is plenty flexible.

If you want to make something notice that something has happened, there's this thing called "a line of code" that can be inserted.  If you want to know every time `add(D)` is called, you just attach this "line of code" concept to the `add` function, and there you have the notification vehicle.  Heck, you're going to have to write a line of code anyways, if you create an interest registration system.

Indeed, if you do need an interest registration system, it is easy enough to write:

    add_observers = [notify_something]
    
    def add(D):
        data.add(D)
        for fn in add_observers:
            fn()

That wasn't hard.

If the two lines of code were too much of an expense, it could be expressed as just:  `[fn() for fn in add_observers]`, though I frown a little to read that.

But I'd rather not do that.

I'd rather just call `notify_something()` directly.


When I program something fairly complex, I might use *all* of the above in a single collection of data.  What's interesting to me is that for some reason, C++ (say) chose a very specific system of relating classes and objects to one another.  But what I find in my own programming, is that I like to use one system for some things, and another system for other things, and it is not unusual that I use several different systems all together with the same data, and it all works out.

I don't understand why we try and bake a specific set of relationships right into the programming language, and then require that everybody use those baked in forms.

C++ style inheritance works for, ...  I'm sure it works for some class of problems, but I find that other forms of relating code to other code work more commonly in general.

When you use simple dictionaries, to assemble your data together, you're not constricted to one way of working with data.  Suddenly, you can work with every form of working with data.

Heck, you can use lists very effectively as well.  Programming with tables can be incredibly convenient.  Each row in the table is a different "object," if you will, and the columns of the table represent the different attributes of the table.  Functions can also be pegged as attributes, and then you can look at the table and see a total inventory of objects and what they will do.


## Avoiding Gobbledygook

Python has features.

It has a *lot* of features.

Let's talk about one of them, so you have a sense of what I'm talking about.

Let's talk about... *decorators*.

### Target #1: Decorators

Here's a page on how to use decorators in Python: https://www.geeksforgeeks.org/decorators-in-python/

Here's a decorator function it presents:

    def calculate_time(func):
        def inner1(*args, **kwargs):
            begin = time.time()
            func(*args, **kwargs)
            end = time.time()
            print("Total time taken in : ", func.__name__, end - begin)
        return inner1
OK, so, what I'm going to tell you is: **You don't need it.**

You just don't need it.

I have never found a situation where I needed a decorator.

If I want to time a function call, I can just:

    def time_fn_call(fn):
        begin = time.time()
        fn()
        end = time.time()
        return end - begin

You would call it like so:

    time_fn_call(lambda: foo(1, 2, 3))

I have never, in my life, seen a meaningful programming problem that was remarkably simplified by the use of decorators.  I think that they are pretty much completely superfluous.

Of course it looks pretty to see "@foo" next to a function, and know that it is providing some kind of annotation on the function, or something like that, -- but I haven't seen it actually be *useful*.  Let us reserve beauty for women, in the main, and we should not be trying to insert it into our mechanics, unless we want high-maintenance mechanics -- and we don't: We want low-maintenance mechanics.

I never use decorators in my code.

Next target: Meta-Classes.

### Target #2: Meta-Classes

Jesus Christ, for the love of God -- ...

As it is, I am only okay with classes -- just plain, ordinary classes, in two situations:
1. In a graphical programming environment like [Squeek](https://squeak.org/) or [SmallTalk](https://en.wikipedia.org/wiki/Smalltalk).  These are programming environments specifically crafted around classes and objects, and the notational pragmatics of classes and objects are very, very different, than they are in raw text-file based languages.  
2. When creating an object that is very primitive, and that will be used across broad swaths of code.

I am specifically opposed to the use of classes as the fundamental means of organizing programs in a text-file based programming environment.  I think that the strictures that they introduce are arbitrary, and that the inflexibilities that they introduce directly impede the path of programming.

Before I would use a class in a computer program, it must prove its merit.  If it hasn't paid for itself in any clear and obvious way, then I want it out.  And rigorously applying this ethic has led me to a place where I might create one class per year, if that.  I have found alternatives, as described in this document, that work far better for me.  Occasionally I do want and use a class, but in the main, I have no use of them.

And so: Meta-Classes, are the height of non-necessity.

I have not studied them in depth, and I plan to keep it that way.  I have not once in my life seen a situation that required or would benefit from meta-classes, rather than some other solution.

### Target #3: Iterators & Generators

Of all the things I've listed, I think that this one is actually the one that can be most genuinely useful.  But *I'm suspicious.*

What you can do with `yield`, -- stopping a function dead in its tracks, and then resuming later from that point -- you cannot do by any other method.

And I've seen people write entire operating-system-like environments in Python, using generators and yield.

"OK," if that is your specific need, (and I can imagine some situations where that would be the central need,) then I think these mechanisms are valuable.

But I have not yet encountered that need.  And when I have needed to perform tasks in chunks, I have found it easy enough to keep nullary functions in a list, and each "turn," take one item off of that list, and execute it.  When I needed to stop a task part-way to completion, I just put two functions, or three functions, into the list, representing the different parts of the task.

That was easy, and not a problem.

I didn't have to wrestle with scoping questions, because all data was in the global scope: Tasks just picked up where the prior one left off.

I didn't have to wrestle with argument passing systems, because there were no arguments.

If the task needed to stay in the queue, it could simply put itself back in: The function is essentially a memory address, and the queue is in the global scope, so it can just insert itself back onto the queue, in whatever place it needs to be put.

### Programming is Simple

Essentially, at the end of the day, programming is very simple.

Programming is about:
* Data -- organizing, storing, retrieving
* Math -- adding, subtracting, multiplying, dividing
* Steps -- one after another, occasionally looping or branching
* Promises -- making sure steps don't break promises

That's it.

That's all that you need, to solve the programming problems in the world.

Look at machine code:  MOV, ADD, SUB, MUL, DIV, CMP, JE, JNE, CALL, RET ...  Yes, there are crazy instructions for specific operations, (typically: math,) but underneath it, it's the same stuff.

Whatever we can organize on paper, we can program into a computer.

Variables, simple operations, flow control.  That's all you need, to solve pretty much every problem out there.

I don't mean to come off as anti-progress, or anti-experimentation.  I'm all for making 3-D programming mediums in Virtual Reality, I'm all for multi-process concurrent programming, I'm all for experimenting with new programming ideas, and so on, and so forth.  There are various things that I love to explore.

But we shouldn't kid ourselves, and forget that underneath it all, programming is fairly simple.  And if something takes us *away from* that simplicity, rather than bring us back to it, -- I seriously question the merit of that thing, whatever that thing is.

I have not found a genuine need for classes to help me organize my programs.  Modules have provided me with pretty much everything that I need, to keep a program organized.  Dictionaries and lists are fantastic containers for collections of data.  Symbols make it easy to index dictionaries, and represent meaningful values.