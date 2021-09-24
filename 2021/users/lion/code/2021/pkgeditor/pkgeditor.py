
import tkinter as tk

root = tk.Tk()

entry = tk.StringVar(name="entry")

root.tk.eval("""
ttk::treeview .tree
grid .tree -row 0 -column 0 -sticky nsew -rowspan 3 -pady 5 -padx "5 0"

ttk::scrollbar .treescroll -orient vertical -command ".tree yview"
.tree configure -yscrollcommand ".treescroll set"
grid .treescroll -row 0 -column 1 -rowspan 3 -sticky nsew -pady 5


ttk::frame .detail -borderwidth 5 -relief ridge
grid .detail -row 0 -column 2 -columnspan 2 -sticky nsew -padx 5 -pady 5


tk::text .text -width 72 -height 8 -yscrollcommand ".textscroll set" -state disabled
grid .text -row 1 -column 2 -sticky nsew -padx "5 0"

ttk::scrollbar .textscroll -orient vertical -command ".text yview"
grid .textscroll -row 1 -column 3 -sticky nsew -padx "0 5"

.text tag configure entryinput -underline true


ttk::entry .entry -textvariable entry
grid .entry -row 2 -column 2 -columnspan 2 -sticky ew -padx 5 -pady "0 5"

grid rowconfigure . 0 -weight 8
grid rowconfigure . 1 -weight 6
grid columnconfigure . 0 -weight 9
grid columnconfigure . 2 -weight 15

bind . <Return> {calculate}

proc calculate {} {
  .text configure -state normal
  .text insert end $::entry entryinput
  .text insert end "\n"
  .text yview moveto 1.0
  python_calc
  .text configure -state disabled
  set ::entry {}
}
""")

def calc():
    if entry.get() in {"q", "quit", "exit", "x"}:
        root.destroy()
    else:
        root.tk.eval('.text insert end "additional text\n"')

root.tk.createcommand("python_calc", calc)

root.mainloop()

