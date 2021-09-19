
import pprint
import json
import tkinter as tk

import pyperclip


def read_clipboard():
    return pyperclip.paste().replace("\r\n", "\n")

def write_clipboard(s):
    pyperclip.copy(s.replace("\n", "\r\n"))


root = tk.Tk()

html = tk.StringVar(name="html")
raw = tk.StringVar(name="raw")
author = tk.StringVar(name="author")
hook = tk.StringVar(name="hook")
posted = tk.StringVar(name="posted")


def append_record():
    L = json.load(open("2021_articles_simple.json", "r", encoding="utf-8"))
    D = {
        "AUTHOR": author.get(),
        "HTML": html.get(),
        "RAW": raw.get(),
        "HOOK": hook.get(),
        "POSTED": posted.get()
    }
    L.append(D)
    json.dump(L, open("2021_articles_simple.json", "w", encoding="utf-8"), indent=2)
    pprint.pprint(D)
    print("(SAVED)")


root.tk.createcommand("appendrecord", append_record)


def read_two_paths_from_clipboard():
    L = [s for s in read_clipboard().split()
         if s.startswith("http://") or s.startswith("https://")]
    while len(L) < 2: L.append("")
    return L[:2]

def on_focus():
    a, b = read_two_paths_from_clipboard()
    html.set(a)
    raw.set(b)
    root.tk.eval("focus .c.hook")

root.tk.createcommand("focusin", on_focus)


root.tk.eval("""
package require Tk

ttk::frame .c -padding "3 3 3 3"
grid .c -column 0 -row 0 -sticky nwes
grid columnconfigure . 0 -weight 1
grid rowconfigure . 0 -weight 1

ttk::label .c.lblhtml -text "HTML:"
ttk::label .c.lblraw -text "Raw:"
ttk::label .c.lblauthor -text "Author:"
ttk::label .c.lblhook -text "Hook:"
ttk::label .c.lblposted -text "Posted:"

ttk::entry .c.html -textvariable html -width 125
ttk::entry .c.raw -textvariable raw -width 125

ttk::radiobutton .c.lion -text "lion" -variable author -value lion
ttk::radiobutton .c.ciprian -text "ciprian" -variable author -value "ciprian.cracium"
ttk::radiobutton .c.bouncepaw -text "bouncepaw" -variable author -value bouncepaw

ttk::entry .c.hook -textvariable hook
ttk::entry .c.posted -textvariable posted

ttk::button .c.append -text "Append" -command appendrecord

grid .c.lblhtml -column 0 -row 0 -sticky e
grid .c.lblraw -column 0 -row 1 -sticky e
grid .c.lblauthor -column 0 -row 2 -sticky e
grid .c.lblhook -column 0 -row 3 -sticky e
grid .c.lblposted -column 0 -row 4 -sticky e

grid .c.html -row 0 -column 1 -columnspan 3 -sticky ew
grid .c.raw -row 1 -column 1 -columnspan 3 -sticky ew

grid .c.lion -row 2 -column 1
grid .c.ciprian -row 2 -column 2
grid .c.bouncepaw -row 2 -column 3

grid .c.hook -row 3 -column 1 -columnspan 3 -sticky ew
grid .c.posted -row 4 -column 1 -columnspan 3 -sticky ew

grid .c.append -row 5 -column 0 -columnspan 4 -sticky e

grid columnconfigure .c 0 -weight 0
grid columnconfigure .c 1 -weight 1
grid columnconfigure .c 2 -weight 1
grid columnconfigure .c 3 -weight 1

wm title . "Data Entry"
wm resizable . 1 0

set author lion

bind .c <FocusIn> {focusin}
""")

root.mainloop()

