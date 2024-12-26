# Overview

This is a program that cannot standalone and is intended
to work with Kuriimu - a program that opens Super Mario
Odyssey MSBT files.

_There's a relatively high chance that I will convert this
into a program that can directly work with the files themselves,
but I recently heard of someone doing that exact thing, so I'll
leave it as it is for now._

# Setup

There are two ways to set this up: downloading the compiled
binary, or downloading and running the code.

### Binary

In order to use the binary, just head to the releases page
and download the most recent version. NOTE: virus scanners
**WILL** most likely flag it as a virus. I'm unfamailiar
with how to sign it officially, and to be frank, I'm not
sure if it was signed by AutoPyToExe already. Regardless,
just bear in mind that, as a very unknown executable,
the odds of it setting off some flags are very high.

Warnings aside, simply run the exe and it should open
the program.

### Code

As with most Python environments, simply download or clone
the repository, create and activate a virtual environment,
and run `pip install -r requirements.txt`

# Usage

So this program is a bit more complicated than I intended for it
to be, but due to the aforementioned MSBT program underway, I have
left it as-is for some time.

The usage is as follows:

- Open Kuriimu and this parser
- Find the text you'd like to clean up
- Copy the output from Kuriimu into the parser
- Click the leftmost button - the "clean up" button
- Review the in-game output on the bottom left
- Make edits to the icons on the bottom right
- "Re-encode" the text by clicking the rightmost button
  - This should **OVERWRITE** the text in the top box and replace it with text you can paste into Kuriimu
- Save the file in Kuriimu
- Exit

Note: the center button copies the text from the "In-game Output" box to your clipboard.
This had more usage previously but for now is largely an artifact of older versions.

Should I refactor this project, I plan to add a panel with icons so that adding
icons doesn't require either combing through the [dictionaries.py](https://github.com/wiz-rd/SMO-MSBT-Parser/blob/main/dictionaries.py) file
or locating a place where the icon occurs naturally in-game,
so look forward to that should this receive more updates.
