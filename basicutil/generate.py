
dim=9
dr=0.05
r1min=2.065652
r2min=2.505369

counter = 1
r1 = r1min
for i in range(9):
    r2 = r2min
    for j in range(9):
        print "./mergeatdist_dbl --set-values12=\"1:1:" + str(r1) + \
              "\" --set-values23=\"1:1:"+str(r2)+"\" Cl.xyz Au.xyz Cn.xyz > 1.xyz"
        print "./berthaingen -f \"Cl:../bertha_input/Cl/fitt/a2.txt;Cn:../bertha_input/Cn/fitt/cn.abs;Au:../bertha_input/Au/fitt/b20.txt\" -b \"Cl:../bertha_input/Cl/basis/aug-cc-pVTZ-DK.txt;Cn:../bertha_input/Cn/basis/dyall_vtz.txt;Au:../bertha_input/Au/basis/dyall_vqz.txt\" -c 1.xyz "
        print "mkdir "+str(counter)
        print "mv input.inp fitt2.inp ./"+str(counter)
        counter = counter + 1
        r2 = r2 + dr
    r1 = r1 + dr

#./mergeatdist_dbl --set-values12="1:1:2.265652" --set-values23="1:1:2.705369" Cl.xyz Au.xyz Cn.xyz
#./berthaingen -f "Cl:../bertha_input/Cl/fitt/a2.txt;Cn:../bertha_input/Cn/fitt/cn.abs;Au:../bertha_input/Au/fitt/b20.txt" -b "Cl:../bertha_input/Cl/basis/aug-cc-pVTZ-DK.txt;Cn:../bertha_input/Cn/basis/dyall_vtz.txt;Au:../bertha_input/Au/basis/dyall_vqz.txt" -c 1.xyz 

