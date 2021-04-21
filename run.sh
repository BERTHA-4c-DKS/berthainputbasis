echo "Ag"
python3 txttojson.py -f ./Au/basis/dyall_vdz.txt --atomname "Ag" --basisname "dyall_vdz" --outfilename Ag1.json
python3 txttojson.py -f ./Ag/basis/dyall_vqz.txt --atomname "Ag" --basisname "dyall_vqz" --outfilename Ag2.json
python3 txttojson.py -f ./Ag/basis/dyall_vtz.txt --atomname "Ag" --basisname "dyall_vtz" --outfilename Ag3.json
python3 txttojson.py -f ./Ag/fitt/a1.txt -t  --atomname "Ag" --basisname "a1" --outfilename Ag4.json

echo "Au"
python3 txttojson.py -f ./Au/basis/dyall_vdz.txt --atomname "Au" --basisname "dyall_vdz" --outfilename Au1.json
python3 txttojson.py -f ./Au/basis/dyall_vqz.txt --atomname "Au" --basisname "dyall_vqz" --outfilename Au2.json
python3 txttojson.py -f ./Au/basis/dyall_vtz.txt --atomname "Au" --basisname "dyall_vtz" --outfilename Au3.json
python3 txttojson.py -f ./Au/fitt/b16.txt -t  --atomname "Au" --basisname "b16" --outfilename Au4.json
python3 txttojson.py -f ./Au/fitt/b20.txt -t  --atomname "Au" --basisname "b20" --outfilename Au5.json

echo "C"
python3 txttojson.py -f ./C/basis/aug-cc-pVDZ-DK.txt --atomname "C" --basisname "aug-cc-pVDZ-DK" --outfilename C1.json
python3 txttojson.py -f ./C/basis/aug-cc-pVQZ-DK.txt --atomname "C" --basisname "aug-cc-pVQZ-DK" --outfilename C2.json
python3 txttojson.py -f ./C/basis/aug-cc-pVTZ-DK.txt --atomname "C" --basisname "aug-cc-pVTZ-DK" --outfilename C3.json
python3 txttojson.py -f ./C/fitt/a1.txt -t  --atomname "C" --basisname "a1" --outfilename C4.json

echo "Cl"
python3 txttojson.py -f ./Cl/basis/aug-cc-pVTZ-DK.txt --atomname "Cl" --basisname "aug-cc-pVTZ-DK" --outfilename Cl1.json
python3 txttojson.py -f ./Cl/basis/basis.txt --atomname "Cl" --basisname "genericbasis" --outfilename Cl2.json
python3 txttojson.py -f ./Cl/fitt/a1.txt -t  --atomname "Cl" --basisname "a1" --outfilename Cl3.json
python3 txttojson.py -f ./Cl/fitt/a2.txt -t  --atomname "Cl" --basisname "a2" --outfilename Cl4.json





