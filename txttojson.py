import json
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--inputfile", help="Specify input file", required=True, 
        type=str, default="")
    parser.add_argument("-t","--fittfile", help="The input file is a fitting basisset file", required=False, 
        action="store_true", default=False)
    parser.add_argument("--atomname", help="Specify the atom name", 
        required=True, type=str, default="")
    parser.add_argument("--basisname", help="Specify the basis name", 
        required=True, type=str, default="")
    parser.add_argument("--outfilename", help="Specify the output json filename", 
        required=False, type=str, default="out.json")

    args = parser.parse_args()

    if args.basisname.find("/") >= 0 or \
        args.atomname.find("/") >= 0 :
        print("Cannot use name with / inside ")
        exit(1)

    tojson = {}
    tojson["Atomname"] = args.atomname
    tojson["Basisname"] = args.basisname

    with open(args.inputfile) as fh:
        if args.fittfile:
            tojson["Basistype"] = "fittset"
            firstline = fh.readline()
            dim = int(firstline)
            tojson["Dim"] = dim
            values = []

            tojson["Values"] = []

            for line in fh:
                line = line.replace("\n", "")
                line = ' '.join(line.split())
                values.append(line)
            tojson["Values"].append(values)
        else:
            tojson["Basistype"] = "basisset"

            firstline = fh.readline()
            dim = int(firstline)

            tojson["Dim"] = dim
            tojson["Header"] = []
            tojson["Values"] = []

            for i in range(0,dim+1):
                line = fh.readline()
                sline = line.split()

                if len(sline) != 3:
                    print("Error in file format")
                    exit(1)

                sdim = int(sline[0])
                sval1 = int(sline[1])
                sval2 = int(sline[2])
                
                line = line.replace("\n", "")
                tojson["Header"].append(line)

                values = []
                for j in range(sdim):
                    line = fh.readline()
                    line = line.replace("\n", "")
                    line = line.replace(" ", "")
                    values.append(line)
                tojson["Values"].append(values)

    maindict = {}
    if args.fittfile:
         maindict[args.atomname + "/" +args.basisname + "/fittset"] = tojson
    else:
        maindict[args.atomname + "/" +args.basisname + "/basisset"] = tojson

    out_file = open(args.outfilename, "w")
    json.dump(maindict, out_file, indent = 4, sort_keys = False)
    out_file.close()
                
