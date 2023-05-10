rm fullsets.json 

export i=0

for atom in Ag Au C Cl Cn Cu F Fl H Hg N Nh Og Pb Pt Rn Tl O At Br I W Cr Mo Sg Ts
do
  echo $atom
  for b in $(ls ./"$atom"/basis)
  do
    name=$(echo "$b" | cut -f 1 -d '.')
    python3 txttojson.py -f ./"$atom"/basis/"$b" --atomname "$atom" --basisname "$name" --outfilename "$atom"_"$i".json
    i=$((i+1))
  done

  for b in $(ls ./"$atom"/fitt)
  do
    name=$(echo "$b" | cut -f 1 -d '.')
    python3 txttojson.py -f ./"$atom"/fitt/"$b" -t --atomname "$atom" --basisname "$name" --outfilename "$atom"_"$i".json
    i=$((i+1))
  done

done

python3 mergejsons.py

export i=0

for atom in Ag Au C Cl Cn Cu F Fl H Hg N Nh Og Pb Pt Rn Tl O At Br I W Cr Mo Sg Ts
do
  for b in $(ls ./"$atom"/basis)
  do
    rm -f "$atom"_"$i".json
    i=$((i+1))
  done

  for b in $(ls ./"$atom"/fitt)
  do
    rm -f "$atom"_"$i".json
    i=$((i+1))
  done

done

mv merged_file.json fullsets.json 
