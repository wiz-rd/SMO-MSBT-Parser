#!/usr/bin/python3
import tkinter as tk
import re

# ================================
# = Setting const and global variables
# ================================

SP_CHAR = dict()

# ================================
# = Setting variables and things
# ================================

# the text originally provided,
# with all that weird stuff,
# and the text after it's been changed


def insert_str(item, string: str, index: int):
    """
    A simple helper function to insert an item into a string at the given index.
    """
    return string[index:] + item + string[:index]


def cleanup():
    """
    Uses Regex to remove all non-alphanumeric
    characters from the input string. Doesn't remove punctuation.
    """
    # note: this only works for English (which is fine in this context)
    # but if you need other languages, use "".join([i for i in INPUT if i.isalpha()])
    SP_CHAR.clear()

    # filter out everything that is either the phrase
    # <null> OR is NOT an (English) alphanumeric
    # character. Punctuation and whitespace are allowed
    regex_filter_out = re.compile("(?<![\w<])<null>(?![\w>])|[^,\s\.\!?a-zA-Z0-9]")

    # getting input
    original_text = txt_in.get("1.0", "end-1c")
    # clearing output
    txt_out.delete("1.0", "end-1c")

    # storing location of each special character
    found = regex_filter_out.findall(original_text)

    # TODO: if item already exists in dictionary,
    # change the previous entry to a list of indexes
    # instead of just a singular index. This way
    # you can replace every occurrence of the
    # string in question
    
    # TODO: fix it so that when the output string has been parsed and is shorter,
    # inserting back the original characters doesn't break anything.
    # right now, it breaks stuff becauss it tries
    # to insert items "past" the limit of the current string
    index_in_original_string = 0
    for item in found:
        # get the index of each item
        # *starting from* the last item
        # that way duplicates aren't stored
        if index_in_original_string != 0:
            offset = 1
        else:
            offset = 0
        
        index_in_original_string = original_text.index(item, index_in_original_string + offset)

        # store the index of each special character
        # so we can add it back to the string later
        # after translation / modification

        # if there isn't a value yet, default to an empty list'
        if item not in SP_CHAR:
            SP_CHAR[item] = list()

        # if the item already exists, append it to the current list
        SP_CHAR[item].append(index_in_original_string)

    output_text = regex_filter_out.sub("", original_text)

    # SP_CHAR = special_chars
    txt_out.insert("1.0", output_text)
    print(found)


def revert():
    """
    Uses a dictionary stored in a variable to restore every character removed
    from the input to their proper locations.
    """
    # getting this string manually because Tkinter
    # text box's grid like interface is kind of ridiculous
    output_string = txt_out.get("1.0", "end-1c")
    for ch in SP_CHAR:
        for location in ch:
            output_string = insert_str(ch, output_string, location)

    txt_in.insert("1.0", output_string + "\n\n")


# ================================
# = Setting up tkinter
# ================================

window = tk.Tk()

frame_i = tk.Frame(window)
frame_o = tk.Frame(window)
frame_h = tk.Frame(window)
frame_buttons = tk.Frame(window)

lbl_title = tk.Label(frame_h, text="SMO Text Cleaner", font=("TkDefaultFont", 16))

btn_clean = tk.Button(
    master=frame_buttons,
    text="Cleanup text",
    width=12,
    height=2,
    command=cleanup,
)
btn_revert = tk.Button(
    master=frame_buttons,
    text="Revert text",
    width=12,
    height=2,
    command=revert,
)

txt_in = tk.Text(frame_i, width=50)
txt_out = tk.Text(frame_o, width=50)
lbl_in = tk.Label(frame_i, text="Input")
lbl_out = tk.Label(frame_o, text="Output")

lbl_title.pack()
lbl_in.pack()
txt_in.pack(fill=tk.BOTH)
btn_pad = 20
btn_clean.grid(row=0, column=0, padx=btn_pad)
btn_revert.grid(row=0, column=1, padx=btn_pad)
lbl_out.pack()
txt_out.pack(fill=tk.BOTH)

frame_h.grid()
frame_i.grid()
frame_buttons.grid(padx=10)
frame_o.grid()

window.wm_title("SMO Text Cleaner")
window.mainloop()
