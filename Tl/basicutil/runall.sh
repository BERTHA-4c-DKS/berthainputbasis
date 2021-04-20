for n in {0..10}
do
   mkdir $n
   mv "$n"_input.inp ./"$n"/input.inp
   mv "$n"_fitt2.inp ./"$n"/fitt2.inp
   cd $n
   ln -s ../bertha.parallelshm .
   mpirun -n 4 ./bertha.parallelshm 1> out 2> err &
   cd ../
done
