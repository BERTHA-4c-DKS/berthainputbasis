import json
import basis_set_exchange as bse
import argparse


def convert_bertha_json(atomic_name,basis_data,comments='comment',lmax=0, nl=0):

    tojson = {}
    tojson["Atomname"]  = atomic_name 
    tojson["Basisname"] = basis_data['name']

    tojson["Comments"] = 'comments'

    tojson["Dim"] = lmax
    tojson["Header"] = []
    tojson["Values"] = []

    tojson["Header"] = nl
    tojson["Values"] = [list(map(str, sublist)) for sublist in tab_value]

    maindict = {}
    maindict[atomic_name + "/" +basis_data['name']+ "/basisset"] = tojson

    outfilename = basis_data['name']+"_"+"out.json"
    out_file = open(atomic_name+"_"+outfilename, "w")
    json.dump(maindict, out_file, indent = 4, sort_keys = False)
    out_file.close()

    return
########################################

parser = argparse.ArgumentParser()

parser.add_argument("-b","--basisset", \
        help="Specify BSE basisset: defoult-->dyall-v2z", \
        required=False, type=str, default="dyall-v2z")

parser.add_argument("-b_av","--bse_av", \
        help="Use this for see the avaiable basis set in BSE", \
        type=bool, default=False)


args = parser.parse_args()

basis_set_name=args.basisset
all_basis_sets = bse.get_all_basis_names()
print(all_basis_sets) 

#if basis_set_name not in all_basis_sets:
#    print(basis_set_name+ " is not in BSE")
#    print("use --bse_av")
#    exit(1)
#else:
#    print(basis_set_name+ " is used.")
#
if args.bse_av:
    print(f"Total basis sets available: {len(all_basis_sets)}")
    print(all_basis_sets) 

# 1. Fetch the raw python dictionary object
basis_dict = bse.get_basis(basis_set_name, elements=[], uncontract_general=True, uncontract_spdf=True, uncontract_segmented=True )
# 2. Convert or save using python's built-in json tool
# indent=4 makes it human-readable (pretty-printed)
pretty_json = json.dumps(basis_dict, indent=4)


with open("custom_basis.json", "w") as f:
    f.write(pretty_json)

# 1. Open and load the JSON file
with open("custom_basis.json", "r") as f:
    basis_data = json.load(f)


# 2. Navigate through the elements in the JSON
# The keys under 'elements' are atomic numbers as strings (e.g., '1' for H, '8' for O)
for atomic_number, element_info in basis_data['elements'].items():
    exp_value=[]
    ang_value=[]
    print(f"\nElement: (Z={atomic_number})")
    
    # 3. Loop through the electron shells (s, p, d, etc.)

    for i, shell in enumerate(element_info['electron_shells']):
        # angular_momentum is a list, e.g., [0] for s, [1] for p, [0, 1] for sp
        am = shell['angular_momentum']
        
        # Convert angular momentum integers to spectroscopic notation (s, p, d, f)
        am_labels = {0: 's', 1: 'p', 2: 'd', 3: 'f'}
        shell_type = "".join([am_labels.get(l, str(l)) for l in am])
        
        print(f"  Shell {i+1} ({shell_type}-type):")
        
        # 4. Extract and print the exponents
        exponents = shell['exponents']
        for exp in exponents:
            # Exponents are stored as strings in BSE JSON to prevent floating-point precision loss.
            # Convert them to floats for mathematical use.
            alpha = float(exp)
            exp_value.append(alpha)
            ang_value.append(am[0])
            print(f"Exponent : {alpha:<12.6f}")
    lmax = ang_value[-1]

    nl = []

    for i in range(lmax+1):
        nl.append(str(ang_value.count(i)))
        print(ang_value.count(i))

    print(exp_value)
    print(ang_value)
    print(lmax)
    print(nl)

    print(lmax)
    index=0
    tab_value=[]
    istart = 0
    iend   = istart + int(nl[0])

    start=0
    for i in range(lmax+1):
        print(nl[i])
        for expl in range(int(nl[i])):
            print(exp_value[index])
            index+=1


        tab_value.append(exp_value[start:index])
        start=index
    print('tab_value')
    print(tab_value)
    print(basis_data['name'])

    comments='CIAO' 

    atomic_name=bse.lut.element_sym_from_Z(atomic_number)

    a=convert_bertha_json(atomic_name,basis_data,comments,lmax, nl)
    print('a=',a)


import json
import glob

read_files = glob.glob("*out.json")

berthabset = {}
berthabset["BasisFittSetBertha"] = []

with open(basis_set_name+"_merged_file.json", "w") as outfile:
  for f in read_files:
    with open(f, "r") as infile:
      d = json.load(infile)
      berthabset["BasisFittSetBertha"].append(d)

  json.dump(berthabset, outfile, indent = 4, sort_keys = False)

import glob
import os

# 1. Find all files matching the pattern (e.g., all .json files)
files_to_remove = glob.glob("*out.json")

# 2. Loop through the list and delete each file
for file_path in files_to_remove:
    try:
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    except OSError as e:
        print(f"Error deleting {file_path}: {e}")
























