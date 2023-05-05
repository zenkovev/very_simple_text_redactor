import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.messagebox import askquestion

kTextRedactorWindowHeight = 500
kTextRedactorWindowWidth = 1000
kTextRedactorRowHeight = 1000
kTextRedactorRowWidth = 1000

class TextRedactor:
    def __init__(self):

        # Create root window
        self.root = tk.Tk()
        self.root.geometry(str(kTextRedactorWindowWidth) + "x" + str(kTextRedactorWindowHeight))
        self.root.title("With respect to Vim")
        self.root.minsize(height=kTextRedactorWindowHeight, width=kTextRedactorWindowWidth)

        # Prepare to bind hotkeys
        self.entry = tk.Entry(self.root)
        self.bindtags = self.entry.bindtags()
        self.entry.bindtags((self.bindtags[2], self.bindtags[0],
                             self.bindtags[1], self.bindtags[3]))

        # Add scrollbar
        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add text field
        self.text = tk.Text(self.root, width=kTextRedactorRowHeight, height=kTextRedactorRowWidth,
                       bg="darkviolet", fg="white", wrap=tk.WORD, yscrollcommand=self.scrollbar.set)
        self.text.pack(fill=tk.BOTH)

        # Configure scrollbar
        self.scrollbar.config(command=self.text.yview)

        # Create menubar
        self.menubar = tk.Menu(self.root)

        # Add filename
        self.current_filename = None

    def __open_file(self):
        choice = askquestion(
            "Rewrite text",
            "Do you want to rewrite text in window?",
            icon="warning"
        )
        if (choice == "no"):
            return

        filetypes = (("text files", "*.txt"), ("all files", "*.*"))
        filename = fd.askopenfilename(
            title="Open a file",
            initialdir="~",
            filetypes=filetypes
        )
        if (not filename):
            return

        self.current_filename = filename
        self.text.delete("1.0", tk.END)
        with open(self.current_filename) as input_file:
            self.text.insert(tk.END, input_file.read())

    def __write_to_current_file(self):
        choice = askquestion(
            "Rewrite file",
            "Do you want to rewrite file " + self.current_filename,
            icon="warning"
        )
        if (choice == "no"):
            return

        with open(self.current_filename, "w") as output_file:
            output_file.write(text.get("1.0", "end-1c"))

    def __write_to_selected_file(self):
        filetypes = (("text files", "*.txt"), ("all files", "*.*"))
        filename = fd.asksaveasfilename(
            title="Save to file",
            initialdir="~",
            filetypes=filetypes
        )
        if (not filename):
            return

        with open(filename, "w") as output_file:
            output_file.write(text.get("1.0", "end-1c"))

    def __save_to_file(self):
        if (self.current_filename):
            self.__write_to_current_file()
        else:
            self.__write_to_selected_file()

    def add_menu_file(self):
        self.menu_file = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.menu_file)

        self.menu_file.add_command(label="Open", command=self.__open_file)
        self.menu_file.add_command(label="Save", command=self.__save_to_file)
        self.menu_file.add_command(label="Save to", command=self.__write_to_selected_file)
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Exit", command=self.root.destroy)

    def __select_all(self, event=None):
        self.text.tag_add("sel", "1.0", "end")
        self.text.mark_set("insert", "1.0")
        return "break"

    def add_menu_edit(self):
        self.menu_edit = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=self.menu_edit)

        self.menu_edit.add_command(
            label="Cut",
            accelerator="Ctrl+X",
            command=lambda: self.root.focus_get().event_generate("<<Cut>>")
        )
        self.menu_edit.add_command(
            label="Copy",
            accelerator="Ctrl+C",
            command=lambda: self.root.focus_get().event_generate("<<Copy>>")
        )
        self.menu_edit.add_command(
            label="Paste",
            accelerator="Ctrl+V",
            command=lambda: self.root.focus_get().event_generate("<<Paste>>")
        )

        self.menu_edit.add_command(label="Select all", command=self.__select_all)
        self.text.bind("<Control-a>", self.__select_all)

    def __delete_word(self, event):
        start = self.text.search(r"\s", tk.INSERT, backwards=True, regexp=True)
        end = self.text.search(r"\s", tk.INSERT, regexp=True)
        if start and end:
            self.text.delete(start, end)
            self.text.mark_set(tk.INSERT, self.text.index("insert wordend"))
        return "break"

    def __delete_one_line(self, event):
        line_number = self.text.index(tk.INSERT).split(".")[0]
        self.text.delete(line_number + ".0", line_number + ".end + 1 char")
        return "break"

    def __delete_ten_lines(self, event):
        for i in range(10):
            if (self.text.index(tk.INSERT) != str(self.text.index("end-1c"))):
                line_number = self.text.index(tk.INSERT).split(".")[0]
                self.text.delete(line_number + ".0", line_number + ".end + 1 char")
        return "break"

    def set_delete_hotkeys(self):
        self.text.bind("<Control-p>", self.__delete_word)
        self.text.bind("<Control-d>", self.__delete_one_line)
        self.text.bind("<Control-r>", self.__delete_ten_lines)

    def __find_prev_space(self, event):
        self.text.mark_set(tk.INSERT, self.text.index("insert -1c wordstart"))
        return "break"

    def __find_next_space(self, event):
        self.text.mark_set(tk.INSERT, self.text.index("insert wordend"))
        return "break"

    def __find_prev_line(self, event):
        self.text.mark_set(tk.INSERT, self.text.index("insert -1c linestart"))
        return "break"

    def __find_next_line(self, event):
        self.text.mark_set(tk.INSERT, self.text.index("insert +1c lineend"))
        return "break"

    def set_shift_hotkeys(self):
        self.text.bind("<Control-Left>", self.__find_prev_space)
        self.text.bind("<Control-Right>", self.__find_next_space)
        self.text.bind("<Control-Up>", self.__find_prev_line)
        self.text.bind("<Control-Down>", self.__find_next_line)

    def run(self):
        self.add_menu_file()
        self.add_menu_edit()
        self.set_delete_hotkeys()
        self.set_shift_hotkeys()

        self.root.config(menu=self.menubar)
        self.root.mainloop()
