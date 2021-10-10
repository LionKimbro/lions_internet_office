# tkinter Direct Injection
Lion Kimbro
2021-09-18

This is an article about my research into how to inject tcl/tk code directly from Python code, via tkinter.

The advantages of doing so are:
* simpler code
* every capacity of tcl/tk is available to you
* fewer surprises in the interaction between Python and tcl


Contents:
* [An Example of Direct Injection](#example)
* [The Three Techniques](#three)
  * [root.tk.eval](#eval)
  * [tk.StringVar](#stringvar)
  * [root.tk.createcommand](#createcommand)
* [Another Example](#example2)
* [Conclusion](#conclusion)


## <a name="example">An Example of Direct Injection</a>

Here's an example of a tkinter Python program.

This example comes directly from [the Grid tutorial on TkDocs.](https://tkdocs.com/tutorial/grid.html)

This is the Python code, as it is found there:

    from tkinter import *
    from tkinter import ttk
    
    root = Tk()
    
    content = ttk.Frame(root, padding=(3,3,12,12))
    frame = ttk.Frame(content, borderwidth=5, relief="ridge", width=200, height=100)
    namelbl = ttk.Label(content, text="Name")
    name = ttk.Entry(content)
    
    onevar = BooleanVar()
    twovar = BooleanVar()
    threevar = BooleanVar()
    
    onevar.set(True)
    twovar.set(False)
    threevar.set(True)
    
    one = ttk.Checkbutton(content, text="One", variable=onevar, onvalue=True)
    two = ttk.Checkbutton(content, text="Two", variable=twovar, onvalue=True)
    three = ttk.Checkbutton(content, text="Three", variable=threevar, onvalue=True)
    ok = ttk.Button(content, text="Okay")
    cancel = ttk.Button(content, text="Cancel")
    
    content.grid(column=0, row=0, sticky=(N, S, E, W))
    frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
    namelbl.grid(column=3, row=0, columnspan=2, sticky=(N, W), padx=5)
    name.grid(column=3, row=1, columnspan=2, sticky=(N,E,W), pady=5, padx=5)
    one.grid(column=0, row=3)
    two.grid(column=1, row=3)
    three.grid(column=2, row=3)
    ok.grid(column=3, row=3)
    cancel.grid(column=4, row=3)
    
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    content.columnconfigure(0, weight=3)
    content.columnconfigure(1, weight=3)
    content.columnconfigure(2, weight=3)
    content.columnconfigure(3, weight=1)
    content.columnconfigure(4, weight=1)
    content.rowconfigure(1, weight=1)
    
    root.mainloop()

And here's what the same code looks like, using a direct injection of tcl/tk code:

    import tkinter as tk
    
    root = tk.Tk()
    
    root.tk.eval("""
    ttk::frame .c -padding "3 3 12 12"
    ttk::frame .c.f -borderwidth 5 -relief ridge -width 200 -height 100 
    ttk::label .c.namelbl -text Name
    ttk::entry .c.name
    ttk::checkbutton .c.one -text One -variable one -onvalue 1; set one 1
    ttk::checkbutton .c.two -text Two -variable two -onvalue 1; set two 0
    ttk::checkbutton .c.three -text Three -variable three -onvalue 1; set three 1
    ttk::button .c.ok -text Okay
    ttk::button .c.cancel -text Cancel
    
    grid .c -column 0 -row 0 -sticky nsew
    grid .c.f -column 0 -row 0 -columnspan 3 -rowspan 2 -sticky nsew
    grid .c.namelbl -column 3 -row 0 -columnspan 2 -sticky nw -padx 5
    grid .c.name -column 3 -row 1 -columnspan 2 -sticky new -pady 5 -padx 5
    grid .c.one -column 0 -row 3
    grid .c.two -column 1 -row 3
    grid .c.three -column 2 -row 3
    grid .c.ok -column 3 -row 3
    grid .c.cancel -column 4 -row 3
    
    grid columnconfigure . 0 -weight 1
    grid rowconfigure . 0 -weight 1
    grid columnconfigure .c 0 -weight 3
    grid columnconfigure .c 1 -weight 3
    grid columnconfigure .c 2 -weight 3
    grid columnconfigure .c 3 -weight 1
    grid columnconfigure .c 4 -weight 1
    grid rowconfigure .c 1 -weight 1
    """)
    
    root.mainloop()

One of the two main reasons I like this technique, is that it's much less wordy, being much more direct.

Also note that every capacity of tcl/tk must be available to you.  It is impossible that there is a feature available in tcl/tk, that is not available to you to use.


## <a name="three">The Three Techniques</a>

There are three fundamental techniques that make this work:

* [root.tk.eval](#eval) -- executing raw Tcl/Tk
* [tk.StringVar](#stringvar) -- linking Tcl/Tk variables with Python variables
* [root.tk.createcommand](#createcommand) -- linking Tcl/Tk commands with Python functions


### <a name="eval">root.tk.eval</a>

The first technique is simply to call tcl.

I think there might be a way to do this without actually creating a `root = tk.Tk()` call, I think I have some memory of doing so in the past (today is 2021-09-18, and last I recall looking into this line, it was 2013,) but for the moment, I only know how to do this with a direct call to `root = tk.Tk()` first.

Essentially, you've seen it:

    import tkinter as tk
    
    root = tk.Tk()
    
    root.tk.eval("""
    ...
    """)


### <a name="stringvar">tk.StringVar</a>

When you create a `tk.StringVar(name="...")`, it creates the tk variable, and links it with the Python variable.

tkinter comes with 4 built-in classes of variable adaptors:
* `StringVar`
* `IntVar`
* `DoubleVar`
* `BooleanVar`

You call `my_var.set(...)` to set a value, and `my_var.get(...)` to retrieve the value.

I haven't looked into their implementation at the moment.

* [Python 3 Documentation: Coupling Widget Variables](https://docs.python.org/3/library/tkinter.html#coupling-widget-variables)

I think it is important to keep in mind that Tcl, ultimately, sees everything as a string.


### <a name="createcommand">root.tk.createcommand</a>

This functionality is a little dangerous to me -- the implementers of tkinter clearly had a layer of protection around the `Misc._register` function call that performs the binding between a Python function, and a tcl function.

Thta is, they have a piece called a `CallWrapper` that can optionally perform some substitutions on information received from tcl/tk.  That's gotta be there for a reason.  Furthermore, there is some cleaning up of things that there is an allocation for.  And they had a particular way of constructing unique names of functions, combining the id of the CallWrapper with the function's name, or the functions `__func__`, which I know little about.

That said, in my limited experimentation, root.tk.createcommand "just worked," and I encourage its study.

[The final example](#example2) will show how it can be used directly in code, but very briefly, the call signature is:

    root.tk.createcommand("calculate", calculate)

...where, in this example, "calculate" is the name _in tcl_ for the command, and `calculate` is the name of a Python function.

Abstractly:

    root.tk.createcommand("tclcommandstring", pythonfnname)

If you are interested in seeing how this works, be sure to reference the `Misc._register` call, which is typically called as part of `Misc._options` cleaning -- wherein `tkinter.Widget.__init__` looks through the initialization arguments, and if it sees a function call, turns it into a command in Tcl, and then uses tcl's string for it for its conversation with Tcl.

#### <a name="cleanupcommand">Cleaning Up Commands</a>

There's an aspect about cleaning up commands that is potentially important.

If you are creating and destroying widgets frequently in Python, this might be very important.

I don't understand how it works presently, so caveat emptor, but very briefly, it seems that this code (adapted from `Misc._register`) makes sure that the binding you've created is registered for deletion.

    if root._tclCommands is None:
        root._tclCommands = []
    root._tclCommands.append("calculate")

(Where "calculate" here is the name that tcl recognizes for the command.)


## <a name="example2">Another Example</a>

Here's an example that embeds all three of the functions.

This example, too, is based on [an example from TkDocs.](https://tkdocs.com/tutorial/firstexample.html)

First, I'm going to give the example as it shows up in pure Python:

    from tkinter import *
    from tkinter import ttk
    
    def calculate(*args):
        try:
            value = float(feet.get())
            meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
        except ValueError:
            pass
    
    root = Tk()
    root.title("Feet to Meters")
    
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    feet = StringVar()
    feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
    feet_entry.grid(column=2, row=1, sticky=(W, E))
    
    meters = StringVar()
    ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
    
    ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)
    
    ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
    ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
    ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)
    
    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
    
    feet_entry.focus()
    root.bind("<Return>", calculate)
    
    root.mainloop()

Now I'm going to do something particular --
I'm going to slice the code so that the layout is all created in tcl/tk, but the responsiveness -- specifically the calculation function, -- remains in Python code, by registering the `calculate` function.


    import tkinter as tk
    
    root = tk.Tk()
    
    feet = tk.StringVar(name="feet")
    meters = tk.StringVar(name="meters")
    
    def calculate(*args):
        try:
            value = float(feet.get())
            meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
        except ValueError:
            pass
    
    root.tk.eval("""
    package require Tk
    
    wm title . "Feet to Meters"
    grid [ttk::frame .c -padding "3 3 12 12"] -column 0 -row 0 -sticky nwes
    grid columnconfigure . 0 -weight 1; grid rowconfigure . 0 -weight 1
    
    grid [ttk::entry .c.feet -width 7 -textvariable feet] -column 2 -row 1 -sticky we
    grid [ttk::label .c.meters -textvariable meters] -column 2 -row 2 -sticky we
    grid [ttk::button .c.calc -text "Calculate" -command calculate] -column 3 -row 3 -sticky w
    
    grid [ttk::label .c.flbl -text "feet"] -column 3 -row 1 -sticky w
    grid [ttk::label .c.islbl -text "is equivalent to"] -column 1 -row 2 -sticky e
    grid [ttk::label .c.mlbl -text "meters"] -column 3 -row 2 -sticky w
    
    foreach w [winfo children .c] {grid configure $w -padx 5 -pady 5}
    focus .c.feet
    bind . <Return> {calculate}
    """)
    
    root.tk.createcommand("calculate", calculate)
    
    root.mainloop()


While the lines of code are almost identical between these two examples, I like this second example much more, because it feels simpler to me.  The tcl/tk code is purely tcl/tk code, and has its own self-consistent aesthetic.  Meanwhile, the Python code lives in its own way.


## <a name="conclusion">Conclusion</a>

For a conclusion, I just want to restate what I think are the three primary benefits of interacting with tcl/tk from Python in this way.

* simpler code
* every capacity of tcl/tk is available to you
* fewer surprises in the interaction between Python and tcl

If you should agree, I encourage you to explore this technique.

If this technique becomes popular enough, it might warrant creating an alternative tcl/tk wrapper that features only the minimum functionality required to support this mode of interaction.


## <a name="seealso">See Also</a>

* wiki.tcl-lang.org
  * [Python-Tcl Interactions](https://wiki.tcl-lang.org/page/Python-Tcl-Interactions)
  * [Accessing Tcl and Python from one another](https://wiki.tcl-lang.org/page/Accessing+Tcl+and+Python+from+one+another)

