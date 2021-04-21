import json
import glob

read_files = glob.glob("*.json")

berthabset = {}
berthabset["BasisFittSetBertha"] = []

with open("merged_file.json", "w") as outfile:
  for f in read_files:
    with open(f, "r") as infile:
      d = json.load(infile)
      berthabset["BasisFittSetBertha"].append(d)

  json.dump(berthabset, outfile, indent = 4, sort_keys = False)
