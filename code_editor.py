from idlelib.percolator import Percolator
import re
from jedi.api import Script

from utility import * # type: ignore 
from settings_handler import *
from gui import Root


class CodeEditor:
    def __init__(self, root: Root, master: DefaultSecondaryFrame):
        self.root: Root = root

        self.first_frame = DefaultPrimaryFrame(master)
        self.first_frame.pack(side=LEFT, fill=Y)

        self.spacer = Canvas(self.first_frame, height=30, width=60, bg=root.secondary_color, highlightbackground=root.secondary_color)
        self.spacer.pack(anchor=NW)

        self.label_frame = DefaultSecondaryFrame(master, height=34)
        self.label_frame.pack(side=TOP, fill=X)

        self.labels: list[FileLabel] = []
        

        self.line_number_frame = DefaultPrimaryFrame(self.first_frame, bg=root.secondary_color, padx=2, highlightbackground=root.primary_color)
        self.line_number_frame.pack(side=LEFT, fill=Y)

        
        self.frame = CodeEditorFrame(master, self, bg=root.primary_color, bd=0,)
        self.text = self.frame.text_widget


        
        self._job = None
        self.listbox = None


        self.line_number_text_widget = Text(
            self.line_number_frame,
            state="disabled",
            padx=10,
            width=4,
            bg=root.primary_color,
            fg=root.foreground_color,
            bd=0,
            wrap="none",
            insertbackground=root.foreground_color,
            selectbackground="#6F6F6F",
            tabs="40"
        )
        self.line_number_text_widget.tag_configure("right", justify='right')
        self.line_number_text_widget.pack(fill=Y, side=LEFT)

        # Prevent interaction with line number widget
        self.line_number_text_widget.bind("<MouseWheel>", lambda e: "break")
        self.line_number_text_widget.bind("<Key>", lambda e: "break")
        self.line_number_text_widget.bind("<Button-1>", lambda e: "break")
        self.line_number_text_widget.configure(takefocus=0)



        self.frame.pack(fill=BOTH, side=RIGHT, expand=True)



        
        self.percolator = Percolator(self.text)
        self.percolator.insertfilter(root.color_delegator) # type: ignore

    def load_into_editor(self, content: str):
        self.text.configure(undo=False) #clears the undo stack
        self.text.delete(1.0,END)
        self.text.insert(tk.END, content)
        self.update_line_numbers()
        self.text.configure(undo=True)

    def get_text_widget_content(self):
        return self.text.get("1.0",END)
    
    def update_line_numbers(self, event: Any=None) -> None:
        self.frame.after_idle(self._sync_line_numbers)

    def on_textscroll(self, *args: Any):
        try:
            first = float(args[0])
            if 0.0 <= first <= 1.0:
                self.line_number_text_widget.yview_moveto(args[0])
        except (ValueError, IndexError):
            pass
        self.frame.vertical_scrollbar.set(*args)


    def on_mousewheel(self, event: Any=None) -> str:
        # This scrolls the main text
        self.frame.text_widget.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        # Manually sync the line number widget
        self.line_number_text_widget.yview_moveto(self.frame.text_widget.yview()[0]) # type: ignore
        
        return "break"  # Prevent default scrolling from duplicating
    
    def on_shift_mousewheel(self, event: Any=None) -> str:
        self.frame.text_widget.xview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"
            
    def handle_mousewheel_and_update(self, event: Any=None) -> str:
        self.on_mousewheel(event)
        self.update_line_numbers()
        return "break"

        
    def _sync_line_numbers(self):
        self.line_number_text_widget.configure(state="normal")
        self.line_number_text_widget.delete("1.0", "end")

        num_lines = int(self.frame.text_widget.index("end-1c").split(".")[0])
        for i in range(1, num_lines + 1):
            self.line_number_text_widget.insert("end", f"{i}\n", "right")

        self.line_number_text_widget.yview_moveto(self.frame.text_widget.yview()[0]) # type: ignore
        self.line_number_text_widget.configure(state="disabled")

    # def update_label(self):
    #     current_file = settings_handler.get_variable("current_file_directory")
    #     current_file = current_file.split("/")[-1]
    #     self.file_label.configure(text=current_file)

    def add_label(self, directory: str):
        name = directory.split("/")[-1]
        for label in self.labels:
            if label.directory == directory:
                return
        file_label = FileLabel(master=self.label_frame, directory=directory, isFile=True, labels=self.labels, root=self.root, text=name, bg=self.root.primary_color)
        

        
        
        
    
    def open_label(self, opened_label: FileLabel) -> None:
        for label in self.labels:
            label.configure(bg=self.root.secondary_color)
            label.close_button.configure(bg=self.root.secondary_color)

        opened_label.close_button.configure(bg=self.root.primary_color)
        opened_label.configure(bg=self.root.primary_color)
        self.root.file_manager.open_file(opened_label.directory, label_opened=True)
    


    
class CodeEditorFrame(CustomWidgetMixin, Frame):
    def __init__(self, master: Any, code_editor: CodeEditor, **kwargs: Any):
        style = self.build_style()
        kwargs.update(style)
        super().__init__(master, **kwargs)


        # Frame containing Text + Scrollbars
        self.plus_scrollbar_frame = DefaultPrimaryFrame(self, bg=self.primary_color)
        self.plus_scrollbar_frame.pack(side="top", fill="both", expand=True)

        # Text widget
        self.text_widget = CodeEditorText(self.plus_scrollbar_frame, code_editor)
        
        self.text_widget.grid(row=0, column=0, sticky="nsew")



        # Grid weight for resizing
        self.plus_scrollbar_frame.grid_rowconfigure(0, weight=1)
        self.plus_scrollbar_frame.grid_columnconfigure(0, weight=1)

        # Vertical scrollbar
        self.vertical_scrollbar = AutoHiddenScrollbar(
            self.plus_scrollbar_frame,
            self.text_widget,
            style="My.Vertical.TScrollbar",
            orient=VERTICAL,
            cursor="arrow",
            command=self.on_scrollbar_scroll
        )
        self.vertical_scrollbar.grid(row=0, column=1, sticky="ns")

        # Horizontal scrollbar
        self.horizontal_scrollbar = AutoHiddenScrollbar(
            self.plus_scrollbar_frame,
            self.text_widget,
            style="My.Horizontal.TScrollbar",
            orient=HORIZONTAL,
            cursor="arrow",
            command=self.text_widget.xview # type: ignore
        )
        self.horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

        # Scrollbar <-> text widget communication
        self.text_widget.configure(xscrollcommand=self.horizontal_scrollbar.set)
        self.text_widget.configure(yscrollcommand=self.vertical_scrollbar.set)

    def build_style(self) -> dict[str, Any]:
        return {
            'bg': self.primary_color
        }



    def on_scrollbar_scroll(self, *args: Any) -> None:
        self.text_widget.yview(*args) # type: ignore


class CodeEditorText(CustomWidgetMixin, Text):
    def __init__(self, master: DefaultPrimaryFrame, code_editor: CodeEditor, **kwargs: Any):
        self.code_editor = code_editor
        self._job = None
        self.listbox: tk.Listbox = None # type: ignore

        style = self.build_style()
        kwargs.update(style)
        super().__init__(master, **kwargs)

        self.bind("<Control-BackSpace>", lambda event: self.on_control_backspace())
        self.bind("<Control-Delete>", lambda event: self.on_control_delete())

        self.bind("<Control-Shift-Z>", lambda event: self.edit_redo())

        self.bind("<Configure>", code_editor.update_line_numbers)
        self.bind("<Button-4>", code_editor.on_mousewheel)  # For Linux
        self.bind("<Button-5>", code_editor.on_mousewheel)
        self.bind("<KeyRelease-Up>", code_editor.update_line_numbers)
        self.bind("<KeyRelease-Down>", code_editor.update_line_numbers)
        self.bind("<BackSpace>", code_editor.update_line_numbers)
        self.bind("<MouseWheel>", code_editor.handle_mousewheel_and_update)
        self.bind("<ButtonRelease>", code_editor.update_line_numbers)
        self.bind("<Shift-MouseWheel>", code_editor.on_shift_mousewheel)
        self.bind("<Tab>",    self._on_tab)      # new
        self.bind("<KeyRelease>", self._on_keyrelease)
        self.bind("<Down>",   self._on_down)
        self.bind("<Up>",     self._on_up)
        self.bind("<Return>", self._on_return)
        self.bind("<Escape>", self._hide_listbox)

        self.configure(yscrollcommand=code_editor.on_textscroll)
        self.configure(undo=True, maxundo=-1, autoseparators=True)

    def build_style(self) -> dict[str, Any]:
            return {
            "padx": 10,
            "bg": self.primary_color,
            "fg": self.foreground_color,
            "bd": 0,
            "wrap": "none",
            "insertbackground": self.foreground_color,
            "selectbackground": "#6F6F6F",
            "tabs": "40",
            }    
    def on_control_backspace(self):
        cursor_index = self.index(tk.INSERT)

        # Stop if already at start
        if self.compare(cursor_index, "<=", "1.0"):
            return "break"

        break_chars = set(" \n\t()[]{}:;.,'\"#=+-*/%<>!&|^~\\")

        # Compute previous character safely
        prev_index = self.index(f"{cursor_index} -1c")
        char = self.get(prev_index)

        # If previous char is a break character, delete just one
        if char in break_chars:
            self.delete(prev_index, cursor_index)
            return "break"

        # Otherwise, delete until a break character or start of text
        index = cursor_index
        while True:
            prev_index = self.index(f"{index} -1c")
            if self.compare(prev_index, "<=", "1.0"):
                break  # stop before going past start
            char = self.get(prev_index)
            if char in break_chars:
                break
            index = prev_index

        self.delete(index, cursor_index)

        # If deletion reached the very first letter, simulate a single backspace
        if self.compare(index, "<=", "1.1"):
            self.event_generate("<BackSpace>")

        return "break"


    def on_control_delete(self):
        cursor_index = self.index(tk.INSERT)
        next_index = self.index(f"{cursor_index} +1c")

        if self.compare(next_index, ">", tk.END):
            return "break"  # Already at end of text

        char = self.get(cursor_index)

        break_chars = set(" \n\t()[]{}:;.,'\"#=+-*/%<>!&|^~\\")

        # If next character is a break character, delete just one
        if char in break_chars:
            self.delete(cursor_index, next_index)
            return "break"

        # Otherwise, delete until a break character is found
        index = cursor_index
        while True:
            char = self.get(index)
            if char in break_chars or self.compare(index, ">=", tk.END):
                break
            index = self.index(f"{index} +1c")

        self.delete(cursor_index, index)
        return "break"
    
    def _on_keyrelease(self, event: Any):
        self.code_editor.update_line_numbers()
        # Only debounce real typing keys
        if event.keysym in ("Up","Down","Left","Right","Return","Escape"):
            return
        if self._job:
            self.after_cancel(self._job)
        self._job = self.after(50, self._autocomplete)

    def _autocomplete(self) -> None:
        
        code = self.get("1.0", "end-1c")
        row, col = map(int, self.index("insert").split('.'))

        prefix = self.get(f"{row}.0", f"{row}.{col}")
        # if only whitespace—no token—hide and return
        if not prefix.strip():
            return self._hide_listbox() # type:ignore
        try:
            script = Script(code, path="__main__.py")
            comps = script.complete(line=row, column=col)
            words = [c.name for c in comps]
        except Exception:
            words = []

        words: list[str] = [n for n in words if n != prefix]
        if not words:
            return self._hide_listbox() # type:ignore
        
        if not words:
            return self._hide_listbox() # type:ignore

        if not self.listbox:
            self.listbox: tk.Listbox = tk.Listbox(self.master, height=6)
            self.listbox.bind("<<ListboxSelect>>", lambda e: self._on_listbox_select(e))

        self.listbox.delete(0, tk.END)
        for word in words:
            self.listbox.insert(tk.END, word)

        # place under cursor
        bbox = self.bbox("insert")
        if not bbox:
            return
        x, y, w, h = bbox
        abs_x = self.winfo_rootx() + x
        abs_y = self.winfo_rooty() + y + h
        self.listbox.place(x=abs_x, y=abs_y)
        self.listbox.lift()
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(0)
        self.listbox.see(0)

    def _on_down(self, event: Any):
        if self.listbox:
            idx = self.listbox.curselection()[0]
            if idx < self.listbox.size() - 1:
                new = idx + 1
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(new)
                self.listbox.see(new)
            return "break"

    def _on_up(self, event: Any):
        if self.listbox:
            idx = self.listbox.curselection()[0]
            if idx > 0:
                new: int = idx - 1
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(new)
                self.listbox.see(new)
            return "break"
        
    def _on_tab(self, event: Any) -> None | str:
        if self.listbox:
            self._insert_selection()
            return "break"    # prevent tab from inserting a tab character

    def _on_return(self, event: Any) -> None | str:
        self.code_editor.update_line_numbers
        if self.listbox:
            self._insert_selection()
            return "break"

    def _on_listbox_select(self, event: Any):
        self._insert_selection()

    def _insert_selection(self) -> None:
        if not self.listbox:
            return
        # 1. Which item?
        idxs= self.listbox.curselection()
        if not idxs:
            return
        completion = self.listbox.get(idxs[0])

        # 2. Find token prefix
        line, col = map(int, self.index("insert").split('.'))
        # get text of the current line up to cursor
        line_text = self.get(f"{line}.0", f"{line}.{col}")
        m = re.search(r"\w+$", line_text)
        if m:
            # calculate the start index for deletion
            start_col = m.start()
            start_index = f"{line}.{start_col}"
        else:
            # nothing to delete (e.g. first char isn't alnum)
            start_index = f"{line}.{col}"

        # 3. Delete only that prefix, then insert completion
        self.delete(start_index, f"{line}.{col}")
        self.insert(start_index, completion)
        self._hide_listbox()

    def _hide_listbox(self, event: Any = None):
        if self.listbox:
            self.listbox.destroy()
            self.listbox = None # type: ignore
