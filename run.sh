export i=0

for atom in Ag Au C Cl Cn Cu F Fl H Hg N Nh Og Pb Pt Rn Tl O
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
