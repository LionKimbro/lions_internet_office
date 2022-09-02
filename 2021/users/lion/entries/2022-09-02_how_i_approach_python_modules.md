# How I Approach Python Modules

Lion Kimbro
version: 1 (2022-09-02)
status: complete

These are some habits of how I write programs in Python.

* Isolation of Initialization
	* no import calculation
	* routines: `setup()` and `init()` and `teardown()`
	* modules: `go.py` and `init.py`
* Isolation of Installation
	* routines: `install()` and `uninstall()`

I am writing this mainly for myself.  If you are visitor, you may be more interested in [my overall approach to programming.](2021-09-06_programming-philosophy.md)

The two main themes here are isolation of initialization, and isolation of installation.

The "isolation of initialization" means that initialization procedures are highly controlled and isolated.  The reason this is important to me, is because I develop software systems out of collections of components, and those components are often highly interdependent.  I have discovered that if I am not able to think about and carefully control how those components are wired up to one another, that I lose control of the program.  What I mean by "lose control," is that at a certain point, I am perplexed about why things are behaving the way they are, or I have difficulty reasoning through how to add a new component into the system, without disturbing other components of the system.  When I cannot change or extend a program, and yet still have it be functional, I have "lost control" of the program.  I have discovered that by carefully controlling initialization and shutdown procedures, I am able to increase the amount of complexity that the program can have, before I lose control of it.

There are initialization and shutdown architectures that are superior to what I am describing here.  Logic programming methods and bus architectures with boot protocols, for example, can dramatically extend the scope of complexity available.  But those systems are usually more complex than what I need, and so the basic method I have worked out here is what I more typically use.

As for the isolation of installation -- I typically program for myself, and so I don't think much about it.  But the isolation of installation is crucial to extending a program to other computer systems, notably *other people's* computer systems, so it is something I think about more frequently these days.

## Theory of Initialization
There is a part in Card Captor Sakura in which ケルベロス explains that all magic consists in two things:  keeping promises, and following steps.  I have found that this is exactly true of designing programs:  Program designs work when they keep promises, and follow steps.

Keeping Promises:
* Making sure that variables are of the right type.  (For example, an integer, rather than a string.)
* Making sure that variables have the correct range of values.  (For example, an integer between 0 and 100.)
* Making sure that memory is not overrun.  (For example, a string that has 15 characters max, and terminates with a zero.)
* Making sure that certain things happen before certain other things, always.
* Making sure that two things cannot happen at the same time.

There are all kinds of promises that must be kept, in order for a system to function.

When the steps of a program try to do something where a promise hasn't been kept, the unexpected occurs.

Following Steps:
This is more intuitive to the programmer, because the programmer is literally writing the lines of code that the program has to follow.  If you can break the solution to the program down into correct discrete steps, input them into a computer, and have the computer follow those steps, then the proper outcome should arise.

"Following steps" is the visible part, "Keeping promises" is typically the invisible part.

What does this have to do with initialization?

It's because very likely, when the program is just starting, there is no state, there is no setup, there is no nothing.  And that means, typically that most all of your promises start out broken, to begin with.

For example, if one of the promises is that "the global value X will always have a value between 10 and 25", -- when the program begins, that is not the case.  The "global value X" might not even *exist* yet.

So some steps have to be followed, before the system gets to the minimal state of meeting its basic promises, and then from there, the component is free to follow steps that are designed with the understanding that a specific platform of promises will be upheld.

To make it perfectly clear:

**Initialization procedures are the steps that configure the environment to such a state that the program's promises are all kept.**

Now on to my specifics.

## No Import Calculation

When a module is imported, there should be no calculation.

Only declaration.

It is fine to declare [symbols](https://github.com/LionKimbro/lions_internet_office/blob/main/2021/users/lion/wiki/symbols.md):

    FOO="FOO"
    BAR="BAR"

It is fine to declare global values:

	g = {FOO: ...,
	     BAR: ...}
	
	db = []

It is fine to declare functions.

	def foo(...):
	    ...

But calculations, file operations, etc., are off limits:

	f = open("foobar.txt", "r")  # NOT ALLOWED
	s = f.read()  # ALSO NOT ALLOWED

An exception is made for calculations so trivial, that they can be performed in-place by the bytecode compiler:

	g = {FOO: 3+5,
	     BAR: "foo" + "bar"}

Because I follow this rule:
* I can safely import any module from any other module.
* I do not have to worry about circular dependencies.
* I do not have to worry about side effects.

But how do I initialize my modules?  That's the subject of `setup()` and `teardown()`.

## routines: `setup()`and `init()` and `teardown()`

Each of my modules, with the sole exception of `go.py`, define these two functions:

	def setup():
	    ...
	
	def teardown():
	    ...

`setup()` performs all initialization that the module can perform, entirely on its own.

`teardown()` ensures that all promises to the external environment are kept, once the module is gone.

They are not an exact mirror of one another:  `setup()` sets the module in all ways that it can complete with self-sufficiency, but perhaps not completely; `teardown()` assumes that the module was completely set up by the time it executes.

They are defined even if they do nothing.  (That is, if they consist only of the instruction: `pass`)

These are not necessarily the very first functions declared.  For example, they may both need use of a helper function, and I frequently put that helper function above the definitions of `setup()` and `teardown()`.

These functions are **always nullary functions.**  That is, they take no arguments.

When I want to supply parameters to initialization, or perform additional steps of initializing the module, I have initialization procedures:

	def init(...):
	    ...

Sometimes, I need multiple initialization procedures, because:
1. There are multiple ways to initialize the module.
2. The initialization steps must be interleaved with other system initialization steps.

The name of all initialization procedures begins with `init_`.

To expand on point #1: Initialization for testing purposes may differ from initialization for conventional use.

To expand on point #2: It sometimes happens that something in module A needs to be initialized before module B, and something in module B needs to be initialized before something in module A is initialized.

So in that case, the initialization code looks like:

	A.init_first_parts()
	B.init()
	A.init_parts_after_B_initialized()

Those specific function names are just for explaining; In reality it probably looks something more like:

    filesys.init_basic()  # initialize the filesystem access
    environvars.init()  # might read from a file, in some situation, for virtual environment variables...
    filesys.init_w_environment()  # continue file broker initialization, using environment variables

That is, there may be multiple initialization procedures.

Sometimes, I do not need any initialization procedure.  `setup()` may do all of the work that is required, by itself.  This is typically true of modules that are entirely self-contained.

Initialization procedures *may* have arguments, though [I avoid them.](https://github.com/LionKimbro/lions_internet_office/blob/main/2021/users/lion/entries/2021-09-06_programming-philosophy.md#global-variables)  When one would send a large collection of arguments, I typically prefer to send a dictionary.  I do this for many reasons, one of which is that it is possible to programmatically modify a dictionary.


## modules: `go.py` and `init.py`

Typically, when I have an "application," by which I mean "a program that is made of several modules working together," I have a `go.py` module, and sometimes an `init.py` module as well.

`go.py` is where the program beings execution.  It is comparable to `main()` in a C program.

It's responsibilities are ultimately:
* to make sure the system is initialized
* to discriminate the context of execution
* to kick off execution
* to make sure that the system shuts down correctly

If initialization is sufficiently complex, I also use a module `init.py`.

The responsibilities of `init.py` are:
* to collect all logic coordinating initialization
* to collect all logic coordinating shutdown

(Some times, `init.py` also collects logic required for major context switches, which may require shutting down and restarting modules, for the sake of ensuring promises are kept in the remainder of the system.)

When `init.py` is used, `go.py` defers system initialization and shutdown to the `init.py` module.

`init.py` can be very handy while debugging, because it could include routines to ease debugging.  You would open up a fresh `python` shell, `import init`, and run `init.debugging()`, and get a system fully initialized for the sake of running a debug session.

## routines: `install()` and `uninstall()`

I am exploring two additional routines, `install()` and `uninstall()`.

These are routines that should be run *only once* in the lifetime of a particular deployment of the system.  The first when you install the program, and then the second, when you uninstall the program.

My present thought is that each module *may* have an `install()` and `uninstall()` routine, and that `go.py` and `install.py` should coordinate the installation and uninstallation of the program, with or without the aid of `init.py`.

This is a point of active research for me.
