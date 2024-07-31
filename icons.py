# will use this for my own custom encoding.
# this will make icon editing a lot easier.
from bidict import bidict

# a bidict is a dictionary
# that can go both ways
# this is especially useful in this case
# where I want to readily switch between these
# as keys and items
ENC_AND_DEC = bidict({
    "Mario": "ᶆ",
    "Cappyless Mario": "ᵯ",
    "Peach": "ᵱ",
    "Pauline": "ᵽ",
    "Bowser": "Ƀ",
    "Topper": "Ⱦ",
    "Rango": "Ɍ",
    "Harriet": "Ƕ",
    "Spewert": "ʂ",
    "Broodals": "Ⅳ",
    "Luigi": "Ɫ",
    "Tiara": "Ṯ",
    "Cappy": "Ḉ",
    "Frog": "ʄ",
    "Globe": "Ꝍ",
    "Purple": "Ꝕ",
    "Checkpoint": "ↆ",
})

ENCODING_DICTIONARY = \
{
    "Mario": {
        # the special value listed explicitly
        # in the msbt files.
        # usually the character it relates to
        "val": ["Mario"],
        "ign": ["Mario_Icon"],
        "kuriimu": "<null>L<null>",
        # to get the actual byte value in the file,
        # append \x00 to the end of each of these
        # including the last one. God knows why, yeesh
        "bytes": b"L",
        "char": ENC_AND_DEC["Mario"],
    },
    "Cappyless Mario": {
        "val": ["Mario"],
        "ign": ["Mario_Icon_Capnon"],
        "kuriimu": "<null>N<null>",
        "bytes": b"N",
        "char": ENC_AND_DEC["Cappyless Mario"],
    },
    "Peach": {
        "val": ["Princess Peach", "Peach"],
        "ign": ["Peach_Icon"],
        "kuriimu": "<null>D<null>",
        "bytes": b"D",
        "char": ENC_AND_DEC["Peach"],
    },
    "Pauline": {
        "val": ["Mayor Pauline", "mayor", "Pauline"],
        "ign": ["Mayor_Icon", "Mayor_Icon2", "PaulineAtCeremony_Icon"],
        "kuriimu": "<null>O<null>",
        "bytes": b"O",
        "char": ENC_AND_DEC["Pauline"],
    },
    "Bowser": {
        "val": ["Bowser", "Boss"],
        "ign": ["Koopa_Icon", "Boss_Koopa_Icon"],
        "kuriimu": "<null>C<null>",
        "bytes": b"C",
        "char": ENC_AND_DEC["Bowser"],
    },
    "Topper": {
        "val": ["Broodal"],
        "ign": ["Stacker"],
        "kuriimu": "<null>H<null>",
        "bytes": b"H",
        "char": ENC_AND_DEC["Topper"],
    },
    "Rango": {
        "val": ["Broodal"],
        "ign": ["CapThrower"],
        "kuriimu": "<null>F<null>",
        "bytes": b"F",
        "char": ENC_AND_DEC["Rango"],
    },
    "Harriet": {
        "val": ["Broodal"],
        "ign": ["BombTail"],
        "kuriimu": "	<null>I<null>",
        "bytes": b"\x09I",
        "char": ENC_AND_DEC["Harriet"],
    },
    "Spewert": {
        "val": ["Broodal"],
        "ign": ["FireBlower"],
        "kuriimu": "<null>G<null>",
        "bytes": b"G",
        "char": ENC_AND_DEC["Spewert"],
    },
    "Broodals": {
        # skipping "GateKeepersUnknown" (val in code: "???")
        # as that's outside the scope of this, and also
        # Doesn't amount to much of anything
        "val": ["Broodals"],
        "ign": ["GateKeepers", "GateKeepers_Icon"],
        "kuriimu": "<null>G<null> <null>H<null> <null>F<null> 	<null>I<null>",
        "bytes": b"G H F \x09I",
        "char": ENC_AND_DEC["Broodals"],
    },
    "Luigi": {
        "val": ["Luigi"],
        "ign": ["TimeBalloonNPC_Icon"],
        "kuriimu": "3<null>9<null>",
        "bytes": b"39",
        "char": ENC_AND_DEC["Luigi"],
    },
    "Tiara": {
        "val": ["Tiara"],
        "ign": ["Tiara_Icon"],
        "kuriimu": "<null>E<null>",
        "bytes": b"E",
        "char": ENC_AND_DEC["Tiara"],
    },
    "Cappy": {
        "val": ["Cappy"],
        "ign": ["Cap_Icon"],
        "kuriimu": "\r<null>M<null>",
        "bytes": b"\x0dM",
        "char": ENC_AND_DEC["Cappy"],
    },
    "Frog": {
        "val": ["Frog"],
        "ign": ["Frog"],
        "kuriimu": "<null>K<null>",
        "bytes": b"K",
        "char": ENC_AND_DEC["Frog"],
    },
    # -------------------------------
    # enter the much simpler items
    "Globe": {
        "val": [],
        "ign": [],
        "kuriimu": "<null>A<null>",
        "bytes": b"A",
        "char": ENC_AND_DEC["Globe"],
    },
    "Globe": {
        "val": [],
        "ign": [],
        "kuriimu": "<null>A<null>",
        "bytes": b"A",
        "char": ENC_AND_DEC["Globe"],
    },
    "Purple": {
        "val": [],
        "ign": [],
        "kuriimu": "<null>",
        "bytes": b"",
        "char": ENC_AND_DEC["Purple"],
    },
    "Checkpoint": {
        "val": [],
        "ign": [],
        "kuriimu": "<null>B<null>",
        "bytes": b"B",
        "char": ENC_AND_DEC["Checkpoint"],
    },
    "Checkpoint": {
        "val": [],
        "ign": [],
        "kuriimu": "<null>B<null>",
        "bytes": b"B",
        "char": ENC_AND_DEC["Checkpoint"],
    },
}
