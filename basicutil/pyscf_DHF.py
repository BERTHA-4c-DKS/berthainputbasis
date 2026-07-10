import basis_set_exchange as bse
from pyscf import gto, scf, lib
from pyscf.data import elements
import numpy as np
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f","--inputfile", help="Specify XYX input file", required=False, \
        type=str, default="")
parser.add_argument("--totalcharge", help="set total charge of the system (default=0)", \
        type=float, default="0")

parser.add_argument("--basisset", help="set basis set BSE", \
        type=str, default="")


args = parser.parse_args()


# 1. Define the molecule
lib.param.LIGHT_SPEED=137.0359898000
mol= gto.Mole()
#mol.atom ='2p_BH3CO.xyz'
mol.atom = args.inputfile
mol.spin=0
mol.unit='Bohr'
#mol.charge=0
mol.charge=int(args.totalcharge)
mol.build()
# 2. Programmatically build a custom basis dictionary using BSE's NWChem writer.
# PySCF's `gto.load` function takes an NWChem format string and parses it perfectly.
elements_in_molecule = [mol.atom_symbol(i) for i in range(mol.natm)]
mol.nucmod = 'G'
mol.build()
print('Nuclear Model:',mol.nucmod)
print('Atomic mass list:',mol.atom_mass_list())

# 2. Dynamically build the basis dictionary
custom_basis = {}
for element in elements_in_molecule:
    # Fetch from BSE in NWChem format
#    nwchem_str = bse.get_basis('dyall-v2z', elements=[element], fmt='nwchem', uncontract_general=True, uncontract_spdf=True, uncontract_segmented=True)
    nwchem_str = bse.get_basis(args.basisset, elements=[element], fmt='nwchem', uncontract_general=True, uncontract_spdf=True, uncontract_segmented=True)

    # Parse into PySCF format and add to dictionary
    custom_basis[element] = gto.load(nwchem_str, element)
# 3. Assign the explicit custom basis dictionary and build the molecule
mol.basis = custom_basis
mol.build()

# 4. Verify that the uncontracted orbitals loaded correctly
print(f"Number of Uncontracted Basis Functions: {mol.nao}")

mf = scf.DHF(mol)
mf.verbose = 4
total_iterations = mf.scf_summary.get('cycle', 0)
energy = mf.kernel()
dm = mf.make_rdm1()
j_matrix, k_matrix = mf.get_jk(mol, dm)

coulomb_energy = 0.5 * np.einsum('ij,ji', j_matrix, dm).real
exchange_energy = -0.5 * np.einsum('ij,ji', k_matrix, dm).real

print("")
print("")
print("-"*6 +" Final Report "+"-"*6)
print(f"Relativistic Coulomb Energy (J):  {coulomb_energy:.6f} Hartree")
print(f"Relativistic Exchange Energy (K): {exchange_energy:.6f} Hartree")
print(f"\nFinal DHF Energy: {energy:.12f} Ha")
dip_el = mf.dip_moment(mol, dm, unit='Debye')
print("")
print("")
print(dip_el)
pure_list = list(mol.atom_mass_list())
print(pure_list)
mass_dict = {str(i): str(float(mass)) for i, mass in enumerate(mol.atom_mass_list())}
print(mass_dict)
print("atomic_masses_used written in atomic_masses_from_pyscf.json:")
with open('atomic_masses_from_pyscf.json', 'w') as f:
    json.dump(mass_dict, f, indent=4)
print("Basise set used:",args.basisset)
