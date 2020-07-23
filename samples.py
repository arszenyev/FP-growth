from collections import OrderedDict

cond_patt_base = {
    'l1': {
        ('l2',): {'support': 4}
    },
    'l3': {
        ('l1',): {'support': 2},
        ('l2',): {'support': 2},
        ('l2', 'l1'): {'support': 2}
    },
    'l4': {
        ('l2',): {'support': 1},
        ('l2', 'l1'): {'support': 1}
    },
    'l5': {
        ('l2', 'l1'): {'support': 1},
        ('l2', 'l1', 'l3'): {'support': 1}
    }
}


D = {
    "T100": ["l1", "l2", "l5"],
    "T200": ["l2", "l4"],
    "T300": ["l2", "l3"],
    "T400": ["l1", "l2", "l4"],
    "T500": ["l1", "l3"],
    "T600": ["l2", "l3"],
    "T700": ["l1", "l3"],
    "T800": ["l1", "l2", "l3", "l5"],
    "T900": ["l1", "l2", "l3"],
}


han_et_al_2000 = {
    "T100": ["f", "a", "c", "d", "g", "i", "m", "p"],
    "T200": ["a", "b", "c", "f", "l", "m", "o"],
    "T300": ["b", "f", "h", "j", "o"],
    "T400": ["b", "c", "k", "s", "p"],
    "T500": ["a", "f", "c", "e", "l", "p", "m", "n"]
}


han_data_1 = OrderedDict({
    "T100": tuple(["l1", "l2", "l5"]),
    "T200": tuple(["l2", "l4"]),
    "T300": tuple(["l2", "l3"]),
    "T400": tuple(["l1", "l2", "l4"]),
    "T500": tuple(["l1", "l3"]),
    "T600": tuple(["l2", "l3"]),
    "T700": tuple(["l1", "l3"]),
    "T800": tuple(["l1", "l2", "l3", "l5"]),
    "T900": tuple(["l1", "l2", "l3"])
})


han_data_2 = {
    "T100": ["M", "O", "N", "K", "E", "Y"],
    "T200": ["D", "O", "N", "K", "E", "Y"],
    "T300": ["M", "A", "K", "E"],
    "T400": ["M", "U", "C", "K", "Y"],
    "T500": ["C", "O", "O", "K", "I", "E"]
}


some_data = OrderedDict({
    "t1": ("E", "K", "M", "N", "O", "Y"),
    "t2": ("D", "E", "K", "N", "O", "Y"),
    "t3": ("A", "E", "K", "M"),
    "t4": ("C", "K", "M", "U", "Y"),
    "t5": ("C", "E", "I", "K", "O", "O")
})

crazy_ronnys_college_stuff_emporium = OrderedDict({
    "T100": tuple(["A", "B", "C", "E", "F"]),
    "T200": tuple(["B", "C", "D"]),
    "T300": tuple(["A", "B", "D", "F"]),
    "T400": tuple(["A", "B", "C", "D", "E", "F"]),
    "T500": tuple(["A", "C", "D", "E"]),
    "T600": tuple(["B", "D", "E"]),
    "T700": tuple(["A", "C", "D"]),
    "T800": tuple(["A", "B", "C", "E"])
})

IdaSamson = OrderedDict({
    "T100": tuple(["I1", "I2", "I5"]),
    "T200": tuple(["I2", "I4"]),
    "T300": tuple(["I2", "I3"]),
    "T400": tuple(["I1", "I2", "I4"]),
    "T500": tuple(["I1", "I3"]),
    "T600": tuple(["I2", "I3"]),
    "T700": tuple(["I1", "I3"]),
    "T800": tuple(["I1", "I2", "I3", "I5"]),
    "T900": tuple(["I1", "I2", "I3"])
})


SoftwaretestingHelp = OrderedDict({
    "T100": tuple(["I1", "I2", "I3"]),
    "T200": tuple(["I2", "I3", "I4"]),
    "T300": tuple(["I4", "I5"]),
    "T400": tuple(["I1", "I2", "I4"]),
    "T500": tuple(["I1", "I2", "I3", "I5"]),
    "T600": tuple(["I1", "I2", "I3", "I4"])
})