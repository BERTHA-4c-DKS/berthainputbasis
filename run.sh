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


echo "Cn"
python3 txttojson.py -f ./Cn/basis/dyall_vtz.txt --atomname "Cn" --basisname "dyall_vtz.txt" --outfilename Cn1.json
python3 txttojson.py -f ./Cn/fitt/cn_old.abs -t  --atomname "Cn" --basisname "cn_old.abs" --outfilename Cn3.json
python3 txttojson.py -f ./Cn/fitt/cn.abs -t  --atomname "Cn" --basisname "cn.abs" --outfilename Cn4.json


echo "Cu"
python3 txttojson.py -f ./Cu/basis/aug-cc-pVDZ-DK.txt --atomname "Cu" --basisname "aug-cc-pVDZ-DK" --outfilename Cu1.json
python3 txttojson.py -f ./Cu/basis/aug-cc-pVQZ-DK.txt --atomname "Cu" --basisname "aug-cc-pVQZ-DK" --outfilename Cu2.json
python3 txttojson.py -f ./Cu/basis/aug-cc-pVTZ-DK.txt --atomname "Cu" --basisname "aug-cc-pVTZ-DK" --outfilename Cu3.json
python3 txttojson.py -f ./Cu/fitt/a1.txt -t  --atomname "Cu" --basisname "a1" --outfilename Cu4.json


echo "F"
python3 txttojson.py -f ./F/fitt/a1.txt -t  --atomname "F" --basisname "a1" --outfilename F2.json




