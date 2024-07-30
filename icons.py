# will use this for my own custom encoding.
# this will make icon editing a lot easier.
# formatting it this way so it can easily
# be copied or moved into a JSON file in the future
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
        "char": "ᶆ",
    },
    "Cappyless Mario": {
        "val": ["Mario"],
        "ign": ["Mario_Icon_Capnon"],
        "kuriimu": "<null>N<null>",
        "bytes": b"N",
        "char": "ᵯ",
    },
    "Peach": {
        "val": ["Princess Peach", "Peach"],
        "ign": ["Peach_Icon"],
        "kuriimu": "<null>D<null>",
        "bytes": b"D",
        "char": "ᵱ",
    },
    "Pauline": {
        "val": ["Mayor Pauline", "mayor", "Pauline"],
        "ign": ["Mayor_Icon", "Mayor_Icon2", "PaulineAtCeremony_Icon"],
        "kuriimu": "<null>O<null>",
        "bytes": b"O",
        "char": "ᵽ",
    },
    "Bowser": {
        "val": ["Bowser", "Boss"],
        "ign": ["Koopa_Icon", "Boss_Koopa_Icon"],
        "kuriimu": "<null>C<null>",
        "bytes": b"C",
        "char": "Ƀ",
    },
    "Topper": {
        "val": ["Broodal"],
        "ign": ["Stacker"],
        "kuriimu": "<null>H<null>",
        "bytes": b"H",
        "char": "Ⱦ",
    },
    "Rango": {
        "val": ["Broodal"],
        "ign": ["CapThrower"],
        "kuriimu": "<null>F<null>",
        "bytes": b"F",
        "char": "Ɍ",
    },
    "Harriet": {
        "val": ["Broodal"],
        "ign": ["BombTail"],
        "kuriimu": "	<null>I<null>",
        "bytes": b"\x09I",
        "char": "Ƕ",
    },
    "Spewert": {
        "val": ["Broodal"],
        "ign": ["FireBlower"],
        "kuriimu": "<null>G<null>",
        "bytes": b"G",
        "char": "ʂ",
    },
    "Broodals": {
        # skipping "GateKeepersUnknown" (val in code: "???")
        # as that's outside the scope of this, and also
        # Doesn't amount to much of anything
        "val": ["Broodals"],
        "ign": ["GateKeepers", "GateKeepers_Icon"],
        "kuriimu": "<null>G<null> <null>H<null> <null>F<null> 	<null>I<null>",
        "bytes": b"G H F \x09I",
        "char": "Ⅳ",
    },
    "Luigi": {
        "val": ["Luigi"],
        "ign": ["TimeBalloonNPC_Icon"],
        "kuriimu": "3<null>9<null>",
        "bytes": b"39",
        "char": "Ɫ",
    },
    "Tiara": {
        "val": ["Tiara"],
        "ign": ["Tiara_Icon"],
        "kuriimu": "<null>E<null>",
        "bytes": b"E",
        "char": "Ṯ",
    },
    "Cappy": {
        "val": ["Cappy"],
        "ign": ["Cap_Icon"],
        "kuriimu": "\r<null>M<null>",
        "bytes": b"\x0dM",
        "char": "Ḉ",
    },
    "Frog": {
        "val": ["Frog"],
        "ign": ["Frog"],
        "kuriimu": "<null>K<null>",
        "bytes": b"K",
        "char": "ʄ",
    },
}

# for converting each long
# string of bytes
# to a single special character
DECODING_DICTIONARY = {
    "ᶆ": "Mario",
    "ᵯ": "Cappyless Mario",
    "ᵱ": "Peach",
    "ᵽ": "Pauline",
    "Ƀ": "Bowser",
    "Ⱦ": "Topper",
    "Ɍ": "Rango",
    "Ƕ": "Harriet",
    "ʂ": "Spewert",
    "Ⅳ": "Broodals",
    "Ɫ": "Luigi",
    "Ṯ": "Tiara",
    "Ḉ": "Cappy",
    "ʄ": "Frog",
}
