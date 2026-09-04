Programs:
abf_generator.py
This program aims to generate an auxiliary basis set in the format "fitt2.inp", that will be one of the input for BERTHA.
The program read the file "input.inp", that is also the input for BERTHA calculations.
The file "input.inp" has to be in the same directory where the script is executed.
The script provides two different way to generate the ABS the Xn and the Yn.
The Xn algorithm generates even-tempered ABS following the Koster approach.
The Yn algorithm is a new approach which based on Lehtola's work with a subsequent clustering, giving a not even-tempered ABS.

## Prerequisite 

In order to properly use  the scrypt ensure to have on your system:
- Python 3.0+
- NumPy 

## How to use

Even-tempered ABS generator:
python abf_generator.py X<float>

Clustered ABS generator:
python abf_generator.py Y<float>

## Example
First case
python abf_generator.py X2.0
Second case
python abf_generator.py Y1.7

## More help with
python abf_generator.py --help
