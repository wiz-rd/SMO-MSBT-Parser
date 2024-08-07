#!/usr/bin/python3
# standard libraries
import re
import os
import sys
import random

# third party libraries
from PIL import Image  # type: ignore
import customtkinter as ctk  # type: ignore

# helper files
from dictionaries import *
from translate import translate

# ================================
# = Setting const and global variables
# ================================

VERSION = "2.0"

SCHEME = "dark"
THEME = f"{SCHEME}-blue"
SEPARATION_CHAR = "|"

END = "end-1c"

ctk.set_appearance_mode(SCHEME)
ctk.set_default_color_theme(THEME)

IMAGES_DIR = "images"

# some bytes that the cleanup grep string
# would allow if they weren't included.
# using a list and then converting it to a string
# for ease of viewing and modfication
MISSED_BYTES = "".join([
    "",
    "",
    "",
    "",
])


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
rvt_img_rel = resource_path(os.path.join(IMAGES_DIR, "Revert.png"))
trt_img_rel = resource_path(os.path.join(IMAGES_DIR, "ClipBoard.png"))
pil_cln = Image.open(cln_img_rel)
pil_cpy = Image.open(cpy_img_rel)
pil_rvt = Image.open(rvt_img_rel)
pil_trt = Image.open(trt_img_rel)
CLEAN_IMG = ctk.CTkImage(pil_cln, pil_cln, (50, 50))
COPY_IMG = ctk.CTkImage(pil_cpy, pil_cpy, (50, 60))
PASTE_IMG = ctk.CTkImage(pil_rvt, pil_rvt, (50, 50))
TRT_IMG = ctk.CTkImage(pil_trt, pil_trt, (50, 60))

class SMOCleaner(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        CORNER_RADIUS = 10
        FONT_SIZE = 25
        self.SP_CHAR = {}

        # frames in order of appearance
        self.frame_header = ctk.CTkFrame(self)
        self.frame_input = ctk.CTkFrame(self)
        self.frame_buttons = ctk.CTkFrame(self)
        self.frame_output = ctk.CTkFrame(self)
        self.frame_output_icons = ctk.CTkFrame(self.frame_output)
        self.frame_output_editable = ctk.CTkFrame(self.frame_output)

        # application title (not window title)
        self.lbl_title = ctk.CTkLabel(self.frame_header, text=f"SMO Text Cleaner v{VERSION}", font=("TkDefaultFont", FONT_SIZE + 10))
        self.lbl_title.pack()

        # input management
        self.lbl_in = ctk.CTkLabel(self.frame_input, text="Raw Text", font=("TkDefaultFont", FONT_SIZE))
        self.txt_in = ctk.CTkTextbox(self.frame_input, corner_radius=CORNER_RADIUS)
        self.lbl_in.pack()
        self.txt_in.pack(fill=ctk.BOTH, padx=40, pady=10)

        # button management
        self.btn_clean = ctk.CTkButton(self.frame_buttons, text="", corner_radius=CORNER_RADIUS, image=CLEAN_IMG, command=self.generate_output_from_input)
        self.btn_copy = ctk.CTkButton(self.frame_buttons, text="", corner_radius=CORNER_RADIUS, image=COPY_IMG, command=self.copy)
        self.btn_paste = ctk.CTkButton(self.frame_buttons, text="", corner_radius=CORNER_RADIUS, image=PASTE_IMG, command=self.revert_output)
        self.btn_translate = ctk.CTkButton(self.frame_buttons, text="", corner_radius=CORNER_RADIUS, image=TRT_IMG, command=self.translate)
        self.btn_clean.place(relx=0.20, rely=0.5, relwidth=0.15, relheight=0.75, anchor="center")
        self.btn_copy.place(relx=0.40, rely=0.5, relwidth=0.15, relheight=0.75, anchor="center")
        self.btn_paste.place(relx=0.60, rely=0.5, relwidth=0.15, relheight=0.75, anchor="center")
        self.btn_translate.place(relx=0.80, rely=0.5, relwidth=0.15, relheight=0.75, anchor="center")

        # -----------------
        # output management
        # ICONS
        # (the output box that cannot be edited
        # and that will render in-game text)
        self.lbl_out_icons = ctk.CTkLabel(self.frame_output_icons, text="In-game Output", font=("TkDefaultFont", FONT_SIZE))
        self.txt_out_icons = ctk.CTkTextbox(self.frame_output_icons, corner_radius=CORNER_RADIUS)
        self.lbl_out_icons.pack()
        self.txt_out_icons.pack(fill=ctk.BOTH, padx=40, pady=10)

        # EDITABLE
        # (the box that CAN be edited
        # and that will allow the user to shift
        # around the icons by moving special characters)
        self.lbl_out_editable = ctk.CTkLabel(self.frame_output_editable, text="Encoded Editor", font=("TkDefaultFont", FONT_SIZE))
        self.txt_out_editable = ctk.CTkTextbox(self.frame_output_editable, corner_radius=CORNER_RADIUS)
        self.lbl_out_editable.pack()
        self.txt_out_editable.pack(fill=ctk.BOTH, padx=40, pady=10)
        self.txt_out_editable.bind("<FocusOut>", command=self.update_icons)
        self.txt_out_editable.bind("<Control-Return>", command=self.update_icons)

        # disabling the output text box so people can't edit it
        # and won't accidentally get their text deleted from here
        self.txt_out_icons.configure(state="disabled")

        self.frame_output_icons.place(relx=0, rely=0, relwidth=0.5, relheight=1)
        self.frame_output_editable.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)
        # -----------------

        # grid-ing everything in order
        self.frame_header.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        self.frame_input.place(relx=0, rely=0.1, relwidth=1, relheight=0.5)
        self.frame_buttons.place(relx=0, rely=0.35, relwidth=1, relheight=0.2)
        self.frame_output.place(relx=0, rely=0.6, relwidth=1, relheight=0.5)

        self.title(f"SMO Cleaner v{VERSION} - {random.choice(MOTD)}")
        self.geometry("800x800")

    def translate(self):
        """
        Grabs the text from the output box and provides it to
        the translate function.
        """
        input_txt = self.txt_out_icons.get("1.0", END)
        output = translate(re.split(r"[\.\!\,\-\?\n]+", input_txt))

        # append the output to the "editable icons" box so icons can be moved around
        self.txt_out_editable.insert("1.0", output + "\n\n")

    def normalize(self, text: str):
        """
        Normalizes the provided text box by removing
        duplicate spaces, newlines, and the like.
        """
        # remove double spaces and newlines
        while "  " in text or "\n\n" in text:
            text = text.replace("  ", " ").replace("\n\n", "\n")

        return text

    def cleanup(self, text: str):
        """
        Uses Regex to remove all non-alphanumeric
        characters from the given string. Doesn't remove punctuation.
        """
        # note: this only works for English (which is fine in this context)
        # but if you need other languages, use "".join([i for i in INPUT if i.isalpha()])

        # filter out everything that is either the phrase
        # <null> OR is NOT an (English) alphanumeric
        # character. Punctuation and whitespace are allowed
        # BUT it does NOT filter out the special characters
        # used specifically for adding icons.
        spcl_chars = list(ENC_AND_DEC.values())
        spcl_str = "".join(spcl_chars)

        # used to replace all duplicate |||||| with one, and only one, |

        # actually cleaning output
        output_text = re.sub(f"(?<![<])<null>(?![>])|[^{spcl_str}\-':;,\s\.\!?a-zA-Z0-9]|[{MISSED_BYTES}]", SEPARATION_CHAR, text)
        output_text = self.normalize(output_text)
        print(output_text)
        output_text = re.sub(r"\|{2,}", "|", output_text)
        # regex_locate_bars = re.findall(r"(\w\|)|(\|+)", output_text)
        print(output_text)

        return output_text
    
    def copy(self):
        """
        Copies the output text to the user's clipboard.
        """
        self.clipboard_clear()
        self.clipboard_append(self.txt_out_icons.get("0.0", END))
    
    def revert_output(self):
        """
        Replaces the text in the "Raw Text" field with the given
        text, but decodes all encoded special characters to their
        byte sequences.
        """
        encoded_text = self.txt_out_editable.get("1.0", END)
        raw_text = encoded_text
        
        for key, val in ENC_AND_DEC.items():
            raw_text = raw_text.replace(val, ENCODING_DICTIONARY[key]["kuriimu"])

        # clearing and then setting the new text
        self.txt_in.delete("1.0", END)
        self.txt_in.insert("1.0", raw_text)

    def add_icon(self, line_num, index, image_path):
        """
        Adds an image, named "icon" in this context,
        to the given line (row) and index (column).
        """
        # setting the max size
        # this should allow images to be rescaled
        # BUT maintain their aspect ratio
        icon_max_size = 28, 28
        pil_img = Image.open(image_path)
        pil_img.thumbnail(icon_max_size)

        img = ctk.CTkImage(pil_img, pil_img, pil_img.size)
        # img = ImageTk.PhotoImage(file=image_path)
        # self.txt_out_icons._textbox.image_create(f"{line_num}.{index}", image=img)
        self.txt_out_icons._textbox.window_create(f"{line_num}.{index}", window = ctk.CTkLabel(self.txt_out_icons, image = img, text=""))

        # ensuring the image isn't garbage collected
        setattr(self.txt_out_icons, f"{line_num}_{index}", img)

    def encode(self, text_to_encode: str):
        """
        Convert the given string to the special characters
        in the custom encoding map. That way, when I clean up the text
        I can deliberately ignore and skip those characters.
        """
        # encoding the string for ease of parsing later
        # and so it can be edited by the user
        for value in ENCODING_DICTIONARY.values():
            text_to_encode = text_to_encode.replace(value["kuriimu"], value["char"]) # type: ignore
        
        return text_to_encode

    def render_output_editable(self, text: str):
        """
        Render the second output - the editable one - after cleaning it up
        and set it up to reflect the icons.
        """
        # clear output
        self.txt_out_editable.delete("1.0", END)
        # update output
        self.txt_out_editable.insert("1.0", text)

        # toggle it as "not edited" - this will allow
        # us to detect future updates and to update
        # the icon output dynamically
        # self.txt_out_editable.edit_modified(False)

    def generate_output_from_input(self, generate_from_editable: bool = False):
        """
        Replaces specific special characters
        with icons in one of the output strings.
        """
        # first, encode
        if not generate_from_editable:
            # if no changes made to editable - e.g.
            # if the user expects to just clean the text
            # do so
            input_text = self.txt_in.get("1.0", END)
        elif generate_from_editable:
            # if the user has made a change to editable
            # use the editable contents instead
            input_text = self.txt_out_editable.get("1.0", END)

        self.txt_out_icons.configure(state="normal")
        encoded_text = self.encode(input_text)

        # then, render the encoded text to be editable
        self.render_output_editable(encoded_text)

        # otherwise, ignore editable field
        # and remove all unwanted special chars from
        # normal output
        cleaned_text = self.cleanup(encoded_text)

        # equate the two so _icons can be modified
        output_text_icons = cleaned_text

        # replacing each special character with nothing in the output text
        for sp_ch in ENC_AND_DEC.values():
            output_text_icons = output_text_icons.replace(sp_ch, "")

        # clearing the output here so that
        # adding the icons won't cause any problems
        self.txt_out_icons.delete("1.0", END)
        self.txt_out_icons.insert("1.0", output_text_icons)

        # swapping encoded chars for icons
        # essentially, the exact same as grabbing each index

        # I have to use .split() instead of .splitlines() because
        # Nintendo - who knows why, again - chose to have some
        # newline-esque characters that cause .splitlines() to separate
        # them into different items in the list, breaking icon placement
        for line_num, line in enumerate(cleaned_text.split("\n"), start=1):
            for letter_num, letter in enumerate(line):
                if letter in ENC_AND_DEC.values():
                    try:
                        self.add_icon(line_num, letter_num, resource_path(os.path.join(IMAGES_DIR, f"{ENC_AND_DEC.inverse[letter]}.png")))
                    except FileNotFoundError:
                        alert = ctk.CTkInputDialog(title="Err", text=f"Icon not found: {os.path.join(IMAGES_DIR, ENC_AND_DEC.inverse[letter])}.png")
                        self.wait_window(alert)
                        print(f"ERR: icon {os.path.join(IMAGES_DIR, ENC_AND_DEC.inverse[letter])}.png not found")

        self.txt_out_icons.configure(state="disabled")
    
    def update_icons(self, name_of_event):
        """
        Updates the icon output after the user moved around the
        encoded text in "Encoded Editor".

        - name_of_event is a required argument and lists the event in question.
        
        I don't know why. This seems to just be "<FocusOut event>", which is exactly
        what I want, so I recommend you just treat it as though this variable does not exist.
        """
        # generate the output again, but this time
        # don't change the
        self.generate_output_from_input(generate_from_editable=True)

        # returning "break" prevents things like "ctrl + enter"
        # from putting a newline, which is exactly what we want
        return "break"


# ================================
# = Finalizing GUI
# ================================

app = SMOCleaner()
app.mainloop()
