import json
import sys

with open(sys.argv[1]) as f:
    d = json.load(f)
    print(d)
