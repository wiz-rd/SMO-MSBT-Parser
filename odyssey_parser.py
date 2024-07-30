#!/usr/bin/python3
# standard libraries
import re
import os
import sys
from tkinter import PhotoImage

# third party libraries
from PIL import Image, ImageTk  # type: ignore
import customtkinter as ctk  # type: ignore

# helper files
from icons import ENCODING_DICTIONARY, DECODING_DICTIONARY

# ================================
# = Setting const and global variables
# ================================

VERSION = "1.2"

SCHEME = "dark"
THEME = f"{SCHEME}-blue"

ctk.set_appearance_mode(SCHEME)
ctk.set_default_color_theme(THEME)


IMAGES_DIR = "images"


def insert_str(item, string: str, index: int):
    """
    A simple helper function to insert an item into a string at the given index.
    """
    return string[index:] + item + string[:index]



# -----------
# to fix a py-to-exe issue
# -----------

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# -----------
# end of code
# -----------
# massive thank you to
# https://stackoverflow.com/a/13790741


# ================================
# = Setting up classes
# ================================
cln_img_rel = resource_path(os.path.join(IMAGES_DIR, "Clean.png"))
cpy_img_rel = resource_path(os.path.join(IMAGES_DIR, "CappyAndPaste.png"))
pst_img_rel = resource_path(os.path.join(IMAGES_DIR, "ClipBoard.png"))
pil_cln = Image.open(cln_img_rel)
pil_cpy = Image.open(cpy_img_rel)
pil_pst = Image.open(pst_img_rel)
CLEAN_IMG = ctk.CTkImage(pil_cln, pil_cln, (50, 50))
PASTE_IMG = ctk.CTkImage(pil_pst, pil_pst, (50, 60))
COPY_IMG = ctk.CTkImage(pil_cpy, pil_cpy, (50, 60))

class SMOCleaner(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

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
        self.btn_clean = ctk.CTkButton(self.frame_buttons, text="", corner_radius=CORNER_RADIUS, image=CLEAN_IMG, command=self.encode)
        self.btn_copy = ctk.CTkButton(self.frame_buttons, text="", corner_radius=CORNER_RADIUS, image=COPY_IMG, command=self.copy)
        self.btn_paste = ctk.CTkButton(self.frame_buttons, text="", corner_radius=CORNER_RADIUS, image=PASTE_IMG, command=self.paste_input)
        self.btn_clean.place(relx=0.25, rely=0.5, relwidth=0.15, relheight=0.75, anchor="center")
        self.btn_copy.place(relx=0.50, rely=0.5, relwidth=0.15, relheight=0.75, anchor="center")
        self.btn_paste.place(relx=0.75, rely=0.5, relwidth=0.15, relheight=0.75, anchor="center")

        # output management
        self.lbl_out = ctk.CTkLabel(self.frame_output, text="Output", font=("TkDefaultFont", FONT_SIZE))
        self.txt_out_icons = ctk.CTkTextbox(self.frame_output, corner_radius=CORNER_RADIUS)
        self.txt_out_editable = ctk.CTkTextbox(self.frame_output, corner_radius=CORNER_RADIUS)
        self.lbl_out.pack()
        self.txt_out_icons.pack(fill=ctk.BOTH, padx=40, pady=10)

        # disabling the output text box so people can't edit it
        # and won't accidentally get their text deleted from here
        self.txt_out_icons.configure(state="disabled")

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
        current_output = self.txt_out_icons.get("1.0", "end-1c")
        new_output = current_output
        
        while "  " in new_output or "\n\n" in new_output:
            new_output = new_output.replace("  ", " ").replace("\n", " ")

        self.txt_out_icons.delete("1.0", "end-1c")
        self.txt_out_icons.insert("1.0", new_output)

    def cleanup(self):
        """
        Uses Regex to remove all non-alphanumeric
        characters from the input string. Doesn't remove punctuation.
        """
        self.txt_out_icons.configure(state="normal")
        # note: this only works for English (which is fine in this context)
        # but if you need other languages, use "".join([i for i in INPUT if i.isalpha()])

        # filter out everything that is either the phrase
        # <null> OR is NOT an (English) alphanumeric
        # character. Punctuation and whitespace are allowed
        regex_filter_out = re.compile("(?<![<])<null>(?![>])|[^':;,\s\.\!?a-zA-Z0-9]")

        # getting input
        original_text = self.txt_in.get("1.0", "end-1c")
        # clearing output
        self.txt_out_icons.delete("1.0", "end-1c")
        # actually cleaning output
        output_text = regex_filter_out.sub("", original_text)

        self.txt_out_icons.insert("1.0", output_text)
        self.txt_out_icons.configure(state="disabled")
        self.normalize()
    
    def copy(self):
        """
        Copies the output text to the user's clipboard.
        """
        self.clipboard_clear()
        self.clipboard_append(self.txt_out_icons.get("0.0", "end-1c"))
    
    def paste_input(self):
        """
        Pastest the user's clipboard to the input text box.
        """
        self.txt_in.insert("end", self.clipboard_get())

    def add_icon(self, line_num, index, image_path):
        """
        Adds an image, named "icon" in this context,
        to the given line (row) and index (column).
        """
        pil_img = Image.open(image_path)
        img = ctk.CTkImage(pil_img, pil_img)
        # img = ImageTk.PhotoImage(file=image_path)
        # self.txt_out_icons._textbox.image_create(f"{line_num}.{index}", image=img)
        self.txt_out_icons._textbox.window_create(f"{line_num}.{index}", window = ctk.CTkLabel(self.txt_out_icons, image = img, text=""))

    def encode(self):
        """
        A method to replace specific icon strings
        with special characters. This is intended
        to be able to support icon rendering later.
        """
        self.txt_out_icons.configure(state="normal")
        output_text_editable = self.txt_in.get("1.0", ctk.END)

        # encoding the string
        for value in ENCODING_DICTIONARY.values():
            output_text_editable = output_text_editable.replace(value["kuriimu"], value["char"])

        print(output_text_editable)

        output_text_icons = output_text_editable

        # removing all special characters from icon output only
        for ch in DECODING_DICTIONARY:
            output_text_icons = output_text_icons.replace(ch, "")

        # swapping encoded chars for icons
        for line_num, line in enumerate(output_text_editable.splitlines(), start=1):
            for letter_num, letter in enumerate(line):
                if letter in DECODING_DICTIONARY:
 
                    # clearing the output here so that
                    # adding the icons won't cause any problems
                    self.txt_out_icons.delete("1.0", ctk.END)
                    self.txt_out_icons.insert("1.0", output_text_icons)

                    self.add_icon(line_num, letter_num, resource_path(os.path.join(IMAGES_DIR, "amiibo.png"))) # f"{DECODING_DICTIONARY[letter]}.webp")))

        self.txt_out_icons.configure(state="disabled")


# ================================
# = Finalizing GUI
# ================================

app = SMOCleaner()
app.mainloop()
