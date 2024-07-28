#!/usr/bin/python3
# standard libraries
import re

# third party libraries
from PIL import Image
import customtkinter as ctk

# ================================
# = Setting const and global variables
# ================================

VERSION = "1.0"

SCHEME = "dark"
THEME = f"{SCHEME}-blue"

ctk.set_appearance_mode(SCHEME)
ctk.set_default_color_theme(THEME)


def insert_str(item, string: str, index: int):
    """
    A simple helper function to insert an item into a string at the given index.
    """
    return string[index:] + item + string[:index]


# ================================
# = Setting up classes
# ================================
cln_img_rel = "./Clean.png"
cpy_img_rel = "./CappyAndPaste.png"
pil_cln = Image.open(cln_img_rel)
pil_cpy = Image.open(cpy_img_rel)
CLEAN_IMG = ctk.CTkImage(pil_cln, pil_cln, (50, 50))
COPY_IMG = ctk.CTkImage(pil_cpy, pil_cpy, (50, 60))

class SMOCleaner(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # CLEAN_IMG = PhotoImage(file=cln_img_rel)
        # COPY_IMG = PhotoImage(file=cpy_img_rel)
        CORNER_RADIUS = 10
        FONT_SIZE = 25

        # frames in order of appearance
        self.frame_header = ctk.CTkFrame(self)
        self.frame_input = ctk.CTkFrame(self)
        self.frame_buttons = ctk.CTkFrame(self)
        self.frame_output = ctk.CTkFrame(self)

        # application title (not window title)
        self.lbl_title = ctk.CTkLabel(self.frame_header, text=f"SMO Text Cleaner v{VERSION}", font=("TkDefaultFont", FONT_SIZE + 10))
        self.lbl_title.pack()

        # input management
        self.lbl_in = ctk.CTkLabel(self.frame_input, text="Input", font=("TkDefaultFont", FONT_SIZE))
        self.txt_in = ctk.CTkTextbox(self.frame_input, corner_radius=CORNER_RADIUS)
        self.lbl_in.pack()
        self.txt_in.pack(fill=ctk.BOTH, padx=40, pady=10)

        # button management
        self.btn_clean = ctk.CTkButton(self.frame_buttons, text="", corner_radius=CORNER_RADIUS, image=CLEAN_IMG, command=self.cleanup)
        self.btn_copy = ctk.CTkButton(self.frame_buttons, text="", corner_radius=CORNER_RADIUS, image=COPY_IMG, command=self.copy)
        self.btn_paste = ctk.CTkButton(self.frame_buttons, text="", corner_radius=CORNER_RADIUS, image=COPY_IMG, command=self.paste_input)
        self.btn_clean.place(relx=0.25, rely=0.5, relwidth=0.15, relheight=0.75, anchor="center")
        self.btn_copy.place(relx=0.50, rely=0.5, relwidth=0.15, relheight=0.75, anchor="center")
        self.btn_paste.place(relx=0.75, rely=0.5, relwidth=0.15, relheight=0.75, anchor="center")

        # output management
        self.lbl_out = ctk.CTkLabel(self.frame_output, text="Output", font=("TkDefaultFont", FONT_SIZE))
        self.txt_out = ctk.CTkTextbox(self.frame_output, corner_radius=CORNER_RADIUS)
        self.lbl_out.pack()
        self.txt_out.pack(fill=ctk.BOTH, padx=40, pady=10)

        # disabling the output text box so people can't edit it
        # and won't accidentally get their text deleted from here
        self.txt_out.configure(state="disabled")

        # grid-ing everything in order
        self.frame_header.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        self.frame_input.place(relx=0, rely=0.1, relwidth=1, relheight=0.5)
        self.frame_buttons.place(relx=0, rely=0.4, relwidth=1, relheight=0.2)
        self.frame_output.place(relx=0, rely=0.6, relwidth=1, relheight=0.5)

        self.geometry("600x800")

    def normalize(self):
        """
        Normalizes the output text box by removing
        duplicate spaces, newlines, and the like.
        """
        # remove double spaces and newlines
        current_output = self.txt_out.get("1.0", "end-1c")
        new_output = current_output
        
        while "  " in new_output or "\n\n" in new_output:
            new_output = new_output.replace("  ", " ").replace("\n", " ")

        self.txt_out.delete("1.0", "end-1c")
        self.txt_out.insert("1.0", new_output)

        # self.textbox = ctk.CTkTextbox(master=self, width=400, corner_radius=CORNER_RADIUS)
        # self.textbox.grid(row=0, column=0, sticky="nsew")
        # self.textbox.insert("0.0", "Some example text!\n" * 50)

    def cleanup(self):
        """
        Uses Regex to remove all non-alphanumeric
        characters from the input string. Doesn't remove punctuation.
        """
        self.txt_out.configure(state="normal")
        # note: this only works for English (which is fine in this context)
        # but if you need other languages, use "".join([i for i in INPUT if i.isalpha()])

        # filter out everything that is either the phrase
        # <null> OR is NOT an (English) alphanumeric
        # character. Punctuation and whitespace are allowed
        regex_filter_out = re.compile("(?<![<])<null>(?![>])|[^':;,\s\.\!?a-zA-Z0-9]")

        # getting input
        original_text = self.txt_in.get("1.0", "end-1c")
        # clearing output
        self.txt_out.delete("1.0", "end-1c")
        # actually cleaning output
        output_text = regex_filter_out.sub("", original_text)

        self.txt_out.insert("1.0", output_text)
        self.txt_out.configure(state="disabled")
        self.normalize()
    
    def copy(self):
        """
        Copies the output text to the user's clipboard.
        """
        self.clipboard_clear()
        self.clipboard_append(self.txt_out.get("0.0", "end-1c"))
    
    def paste_input(self):
        """
        Pastest the user's clipboard to the input text box.
        """
        self.txt_in.insert("end", self.clipboard_get())


# ================================
# = Finalizing GUI
# ================================

app = SMOCleaner()
app.mainloop()
