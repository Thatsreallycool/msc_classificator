from zb_msc_classificator.harmonize import Harmonizer

h = Harmonizer()

example_list = [
    "test",
    "eetfdf",
    "test",
    "17",
    "17"
]

t = h.find_duplicates(example_list)
for dup, coords in t.items():
    print(dup)
    print(coords)

if t.keys():
    my_list = [
        item
        for item in example_list
    ]

    for coords in t.values():
        for dup in coords[1:len(coords)]:
            my_list[dup] = coords[0]


print(example_list)
print(my_list)