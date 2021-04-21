import json

with open("merged_file.json") as f:
    d = json.load(f)
    print(d)
