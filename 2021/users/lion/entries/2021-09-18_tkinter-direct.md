
# tkinter Direct Injection
Lion Kimbro
2021-09-18

This is an article about my research into how to inject tcl/tk code directly from Python code, via tkinter.

The advantages of doing so are:
* simpler code
* fewer surprises in the interaction between Python and tcl

## <a name="example">An Example of Direct Injection</a>

Here's an example of a typical tkinter Python program:

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

## <a name="research">Current Research</a>

* How to bind function calls.
* Known: How to use StringVar to communicate.
	* `feet = tk.StringVar(name="feet")`

