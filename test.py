import tkinter as tk

root = tk.Tk()
text = tk.Text(root, wrap="none")  # wrap="none" so long lines stay on one line
text.pack(fill="both", expand=True)

# Attach scrollbars
ysb = tk.Scrollbar(root, orient="vertical", command=text.yview)
xsb = tk.Scrollbar(root, orient="horizontal", command=text.xview)
text.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
ysb.pack(side="right", fill="y")
xsb.pack(side="bottom", fill="x")

# Fill with sample text (lots of long lines)
for i in range(50):
    text.insert("end", "line %02d: %s\n" % (i, "x"*200))

def scroll_vertically(event):
    # record current x-view
    x0, x1 = text.xview()
    # perform vertical scroll
    if event.delta:  # mouse-wheel on Windows / Mac
        amount = -1 if event.delta > 0 else 1
        text.yview_scroll(amount, "units")
    else:            # on Linux you might get Button-4/5 events
        text.yview_scroll( -1 if event.num==4 else 1, "units")
    # restore x-view
    text.xview_moveto(x0)
    # prevent default handling
    return "break"

# Bind both wheel and scrollbar dragging
text.bind_all("<MouseWheel>", scroll_vertically)      # Windows & macOS
text.bind_all("<Button-4>", scroll_vertically)        # Linux scroll up
text.bind_all("<Button-5>", scroll_vertically)        # Linux scroll down

root.mainloop()