#!/usr/bin/python3
import tkinter as tk
import re

# ================================
# = Setting const and global variables
# ================================

SP_CHAR: dict = {}

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


def normalize_output():
    """
    Normalizes the output text box by removing
    duplicate spaces, newlines, and the like.
    """
    cleanup_regex = re.compile("(\s\s)")
    current_output = txt_out.get("1.0", "end-1c")
    new_output = current_output
    
    while "  " in new_output or "\n\n" in new_output:
        new_output = new_output.replace("  ", " ").replace("\n", " ")

    txt_out.delete("1.0", "end-1c")
    txt_out.insert("1.0", new_output)


def flatten():
    """
    A function to "flatten" the special characters and their indices.
    Essentially, combines characters that should be combined together.
    """
    # start from the end of the list so that when you combine the lists,
    # they are combined from first to last instead of the other way around
    previous_index = None
    # TODO: DELETE DEBUGGING
    print(SP_CHAR)

    for string_index in sorted(SP_CHAR, reverse=True):
        # if an adjacent index is found, merge the two downwards
        # otherwise just continue.
        if previous_index is None: previous_index = string_index

        # if two indexes are one apart
        # e.g. if it's "@@<null>", then don't put their
        # indices as "1, 2, 3". Put them as just 1
        # with the list attached to the key of 1 as
        # ["@", "@", "<null>"]

        if (string_index - 1) in SP_CHAR:
            SP_CHAR[string_index - 1] += SP_CHAR.pop(string_index)

        # this is kind of hard to explain
        # essentially, this performs a similar role as the if statement above
        # but it calculates the length of "<null>" and whatnot - that way
        # two "<null><null>"s can be appended together, for example.
        # in the previous if statement, they would not be appended together,
        # because their indices would be 0 and 6 or so, and: 0 - 1 != 6
        # so even though they, visually, are against each other, to the code they are not.
        # this seeks to fix that.

        distance_between_indices = previous_index - string_index if previous_index is not None else -100
        length_of_previous_word = len("".join(SP_CHAR[string_index])) if string_index in SP_CHAR else -100
        short_enough = distance_between_indices == length_of_previous_word if previous_index in SP_CHAR else False

        # ensure they aren't the same index AND if the last index minus this index is less than or equal to the length of the characters stored,
        # then combine the two indices
        try:
            if (previous_index != string_index) and short_enough:
                SP_CHAR[string_index] += SP_CHAR.pop(previous_index)
        except KeyError:
            print("Skipping flattening adjacent nulls for now.")

        previous_index = string_index


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
    regex_filter_out = re.compile("(?<![<])<null>(?![>])|[^':;,\s\.\!?a-zA-Z0-9]")

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

        # if no character has been found at the given index yet,
        # create a new list for characters found there to be added to
        if index_in_original_string not in SP_CHAR:
            SP_CHAR[index_in_original_string] = [item]
        else:
            # append each item found to the end of the index's list
            SP_CHAR[index_in_original_string] = SP_CHAR[index_in_original_string].append(item)

        # append a list of the location and the
        # item itself into the overall list
        # SP_CHAR.append([index_in_original_string, item])

    output_text = regex_filter_out.sub("", original_text)

    # combining adjacent entries in the dictionary
    flatten()
    flatten()
    txt_out.insert("1.0", output_text)
    normalize_output()
    print(SP_CHAR)


def working_revert():
    """
    Uses a dictionary stored to restore every character removed from
    the input to their proper locations
    """
    # sort the index of each item
    # doing it backwards because it causes issues if you do it forwards
    indexes_found = sorted(SP_CHAR.keys(), reverse=True)

    input_string = txt_in.get("1.0", "end-1c")
    output_string = txt_out.get("1.0", "end-1c")

    # the ratio of output to input lengths- essentially, will
    # be used for placement of special characters instead of
    # *just* the index
    ratio = len(output_string) / len(input_string)

    # for each character removed
    for index in indexes_found:
        # get the item by joining all
        # characters found at that index
        item = "".join(SP_CHAR[index])
        normalized_location = round(index * ratio)
        # make sure it doesn't exceed the length of the output string
        normalized_location -= 1 if normalized_location >= len(output_string) else 0

        print(f"Inserting string {item} at location {normalized_location}")
        output_string = insert_str(item, output_string, normalized_location)

    txt_in.insert("1.0", output_string + "\n\n")


def revert():
    """
    Uses a dictionary stored in a variable to restore every character removed
    from the input to their proper locations.
    """
    # sort by the first item in each list (so the index
    # of the original string, not the item itself)
    # (ensures they'll be inserted in the correct order)
    SP_CHAR.sort(key=lambda x: x[0], reverse=True)

    # getting this string manually because Tkinter
    # text box's grid like interface is kind of ridiculous
    input_string = txt_in.get("1.0", "end-1c")
    output_string = txt_out.get("1.0", "end-1c")

    # the ratio of output to input lengths- essentially, will
    # be used for placement of special characters instead of
    # *just* the index
    ratio = len(output_string) / len(input_string)

    # for each character removed
    for group in SP_CHAR:
        print(group)
        # get the index
        location, item = group
        normalized_location = round(location * ratio)
        # make sure it doesn't exceed the length of the output string
        normalized_location -= 1 if normalized_location >= len(output_string) else 0

        print(f"Inserting string {item} at location {normalized_location}")
        output_string = insert_str(item, output_string, normalized_location)

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
    command=working_revert,
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
