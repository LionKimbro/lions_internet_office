# Symbols

author: Lion Kimbro
date: 2022-09-01
context: Lion's Python Programming

Typically when I write Python programs, I use what I call "symbols."  Now, Python doesn't have a built-in concept of "symbols," so here's how I do it.

    FOO="FOO"
    BAR="BAR"

Here I have defined two "symbols" -- `FOO` and `BAR`.  Languages like LISP have a built-in concept of "symbols," but Python does not, so I simulate them.  I simulate them by creating an all-caps variable name, and bind it to a string that contains the same all-caps text of the variable name.

I use symbols for these reasons:
1. Clear Notation -- no need for quote marks
2. Clear Intent -- discrete values, not strings  & string operations
3. Easier Debugging -- catching `INCLUDE` vs. `INLCUDE`

We'll look at these in detail, but for the sake of explanation, I'll make use of this one example:

    g = {ALLOWKEYBOARD: YES,
         ALLOWMOUSE: NO}
    
    table = {A: ALLOWKEYBOARD,
             B: ALLOWKEYBOARD,
             X: ALLOWMOUSE,
             Y: ALLOWMOUSE,
             ON: YES,
             OFF: YES,
             HIT: NO}
    
    def permit(k):
        if table[k] == YES:
            return True
        elif table[k] == NO:
            return False
        else:
            return permissions[k]

Now for the first point...
## Clear Notation
Contrast the example code, with the following code:

    g = {"ALLOWKEYBOARD": "YES",
         "ALLOWMOUSE": "NO"}
    
    table = {"A": "ALLOWKEYBOARD",
             "B": "ALLOWKEYBOARD",
             "X": "ALLOWMOUSE",
             "Y": "ALLOWMOUSE",
             "ON": "YES",
             "OFF": "YES",
             "HIT": "NO"}
    
    def permit(k):
        if table[k] == "YES":
            return True
        elif table[k] == "NO":
            return False
        else:
            return permissions[k]

Perhaps this is purely subjective on my part, but I find that all those quotation marks all over the place -- I find it distracting.  The first code feels cleaner and clearer to me.

OK, now the second point:
## Clear Intent
When I look at a *string*, notated as a string, with quotation marks and all, in my code, my mind jumps as follows:

* What I Think of When I See Strings (ex: `"a string"`)
	 - **User Text, Input Text**
		 - textual user input
		 - input from a text file
		 - bytes from an incoming byte stream
	 - **String Manipulation**
		 - substring isolation,
		 - regular expressions,
		 - string concatenation,
		 - ...

But now look back again at the reference example.  That's not anything that's happening!  There is no user input, and there is no string manipulation.  I'm using *symbols*.

* What I Think of When I See Symbols (ex: `SYMBOL`)
	* Indexing Keys for Dictionaries
	* Representing Discrete Values

When I use a *symbol* in my code, it represents a discrete value.

It's clear it's a symbol if you could replace it with an integer, instead of a string, and it would function just fine.

For example, the symbol declarations could be:

	ALLOWKEYBOARD = 1
	ALLOWMOUSE = 2
	YES = 3
	NO = 4
	A = 5
	B = 6
	X = 7
	Y = 8
	ON = 9
	OFF = 10
	HIT = 11

...and the code would *function*, just fine.

It'd just be harder to debug.  If I had a value 5 in `k`, I'd have to examine a table, to figure out that it was the symbol `A` that was intended.  Having a string in there, makes it self-transparent though.  It shows up as `"A"` in the debugger.  And that's the _only_ reason, that it is a string.

So I use a string when I want to emphasize the stringiness of the string, (typically when I am parsing input text and such,) and I use a symbol when I want to emphasize discrete values.

Finally, my last point:
## Easier Debugging
It's so that I can catch programming mistakes as early as possible.

Look at these two indexes...

	D[INCLUDE]     # correct
	D[INLCUDE]     # incorrect -- see the mistake?

If I type `D[INLCUDE] = True`, when the runtime gets to it, it'll say: "STOP!!  I never heard of `INLCUDE`!!"  It'll tell me the filename, and the line number, of the source of this error.

But if I type `D["INLCUDE"] = True`, it'll go, "OK, I'll assign True to key `"INLCUDE"` in dictionary D, ... moving right along..."

It won't be until much later, that something will happen.  And then I'll need to figure out what happened, (and I might miss the transposed letters..!), and then once I've figured out that it was a misspelling, I'll potentially need to do a full text search to figure out the filename and line number where the mistake was made.  Not *the worst*?  But definitely a nuisance.

## Conclusion

So in reminder, the three reasons I use "symbols" in Python are:
1. Clear Notation -- no need for quote marks
2. Clear Intent -- it's about symbolic interactions, not strings
3. Easier Debugging -- catching `INLCUDE` vs. `INCLUDE`

These might matter more to me, than to other programmers.  I use *a lot* of dictionaries.  I eschew Python's built-in mechanism for implementing user-defined classes and objects, in general -- the subject of another paper.  (Perhaps... several papers.)  Instead, I primarily use dictionaries, in order to package up "objects."  That means that I'm explicitly indexing into dictionaries, far more frequently, than most Python programmers.  So I think that these reasons have a little more weight for me, than most programmers.  It may not matter as much to other programmers, as it does to me.  And if you think this is all nuts, that's fine.

But this is what I mean by "symbols," and why I use them.

## Additional Note -- Side-Benefit: String Interning
A side benefit of using symbols is that they compare quickly, generally speaking, because the strings are "interned."  You can read [Wikipedia:String interning](https://en.wikipedia.org/wiki/String_interning) to learn more about how that works, and why and when it generates run-time efficiencies.

I say "generally speaking" because input strings are not necessarily interned.

    >>> FOO = "FOO"
    >>> x = "FOO"   # Python interns, and finds it
    >>> FOO is x    # True: because both are intern'ed
    True
    >>> y = input() # I'm going to type "FOO" here...
    FOO             # OK, this is me typing it in...
    >>> y           # So you see, ...
    'FOO'           # it's got it, ..
    >>> FOO is y    # but, ...
    False           # <-- It's not interned.  It's at
    >>> x is y      #     a different memory address.
    False           # <-- see?
    >>> FOO is x    # <-- but FOO and x have
    True            #     the intern'ed "FOO".

But on the whole, it leads to faster string comparison and dictionary key lookup.

In the example at the start of the essay, each of the `table[k]` lookups gain a very slight lookup performance benefit because the key strings are interned, ... And in the comparison between the retrieved value and `== YES` or `== NO`, there is also a slight performance benefit in the equality check.

Like I said before -- I don't do it for the performance benefit.  If there were a slight performance hit, I'd still do it, for the sake of the main benefits I outlined: Clearer notation, clarity of intent, and easier debugging.
