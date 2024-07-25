rm fullsets.json 

export i=0

for atom in Ac Ag Al Am Ar As At Au B Ba Be Bh Bi Bk Br C Ca Cd Ce Cf Cl Cm Cn Co Cr Cs Cu Db Ds Dy Er Es Eu F Fe Fl Fm Fr  Ga Gd Ge H He Hf Hg Ho Hs I In Ir K Kr La Li Lr Lu Lv Mc Md Mg Mn Mo Mt N Na Nb Nd Ne Nh Ni No Np O Og Os P Pa Pb Pd Pm Po Pr Pt Pu Ra Rb Re Rf Rg Rh Rn Ru S Sb Sc Se Sg Si Sm Sn Sr Ta Tb Tc Te Th Ti Tl Tm Ts U V W Xe Y Yb Zn Zr
do
  echo $atom
  for b in $(ls ./"$atom"/basis)
  do
#    name=$(echo "$b" | cut -f 1 -d '.')
    name=$(echo "$b" |  awk '{ print substr( $0, 1, length($0)-4)}')

    python3 txttojson.py -f ./"$atom"/basis/"$b" --atomname "$atom" --basisname "$name" --outfilename "$atom"_"$i".json
    i=$((i+1))
  done

  for b in $(ls ./"$atom"/fitt)
  do
#    name=$(echo "$b" | cut -f 1 -d '.')
    name=$(echo "$b" |  awk '{ print substr( $0, 1, length($0)-4)}')
    python3 txttojson.py -f ./"$atom"/fitt/"$b" -t --atomname "$atom" --basisname "$name" --outfilename "$atom"_"$i".json
    i=$((i+1))
  done

done

python3 mergejsons.py

export i=0

for atom in Ac Ag Al Am Ar As At Au B Ba Be Bh Bi Bk Br C Ca Cd Ce Cf Cl Cm Cn Co Cr Cs Cu Db Ds Dy Er Es Eu F Fe Fl Fm Fr  Ga Gd Ge H He Hf Hg Ho Hs I In Ir K Kr La Li Lr Lu Lv Mc Md Mg Mn Mo Mt N Na Nb Nd Ne Nh Ni No Np O Og Os P Pa Pb Pd Pm Po Pr Pt Pu Ra Rb Re Rf Rg Rh Rn Ru S Sb Sc Se Sg Si Sm Sn Sr Ta Tb Tc Te Th Ti Tl Tm Ts U V W Xe Y Yb Zn Zr
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
