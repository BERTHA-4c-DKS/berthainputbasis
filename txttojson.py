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

    comments = []
    alllines = []
    with open(args.inputfile) as fh:
        for l in fh:
            idx = l.find("#")
            line = []
            if idx >= 0:
                comments.append(l[idx+1:].replace("\n", ""))
                line = l[:idx]
            else:
                line = l

            line = line.replace("\n", "")
            line = ' '.join(line.split())

            if line != "":
                alllines.append(line)

    tojson["Comments"] = comments

    if len(alllines) > 0:
        if args.fittfile:
            tojson["Basistype"] = "fittset"
            firstline = alllines[0]
            dim = int(firstline)
            tojson["Dim"] = dim
            values = []

            tojson["Values"] = []

            for line in alllines[1:]:
                values.append(line)
            tojson["Values"].append(values)
        else:
            counter = 0
            tojson["Basistype"] = "basisset"

            firstline = alllines[counter]
            counter += 1
            dim = int(firstline)

            tojson["Dim"] = dim
            tojson["Header"] = []
            tojson["Values"] = []

            for i in range(0,dim+1):
                line = alllines[counter]
                counter += 1
                sline = line.split()

                if len(sline) != 1 and len(sline) != 3:
                    print("Error in file format")
                    exit(1)

                sdim = int(sline[0])
                #sval1 = int(sline[1])
                #sval2 = int(sline[2])
                
                line = line.replace("\n", "")
                tojson["Header"].append(str(sdim))

                values = []
                for j in range(sdim):
                    line = alllines[counter]
                    counter += 1
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
                
