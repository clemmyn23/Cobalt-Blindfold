all_bopae = {}

import sys
import os
import json
import hashlib

listo = os.listdir()
listo.remove("bopae.json")      # TODO remove bopae.json
listo.remove("lister.py")       # debug

with open("bopae.json") as f:
    bp1 = json.load(f)

bp2 = {}
for i in listo:
    with open(i) as f:
        print("opening file {} as f".format(i))
        tmp = json.load(f)
        bp2.update(tmp)



print(bp1 == bp2)
for i in bp1:
    print("bp1: " + i)

for i in bp2:
    print("bp2: " + i)
