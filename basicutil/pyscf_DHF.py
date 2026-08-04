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

with open(args.inputfile, 'r') as file:
    # Collects the first word of every non-empty line
    first_words = [line.split()[0] for line in file if line.split()]


elements_in_molecule=first_words[2::]


# 1. Define the molecule
lib.param.LIGHT_SPEED=137.0359898000
mol= gto.Mole()
#mol.atom ='2p_BH3CO.xyz'
mol.atom = args.inputfile
mol.spin=0
mol.unit='Bohr'
mol.charge=int(args.totalcharge)
# 2. Programmatically build a custom basis dictionary using BSE's NWChem writer.
# PySCF's `gto.load` function takes an NWChem format string and parses it perfectly.
mol.nucmod ='1'
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
#mol.set_common_orig([0.0, 0.0, -7.05144896])
mol.build()

# 4. Verify that the uncontracted orbitals loaded correctly
print(f"Number of Uncontracted Basis Functions: {mol.nao}")

#
pure_list = list(mol.atom_mass_list())
print(pure_list)
mass_dict = {str(i): str(float(mass)) for i, mass in enumerate(mol.atom_mass_list())}
print(mass_dict)
print("atomic_masses_used written in atomic_masses_from_pyscf.json:")
with open('atomic_masses_from_pyscf.json', 'w') as f:
    json.dump(mass_dict, f, indent=4)
print("Basise set used:",args.basisset)

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

#pure_list = list(mol.atom_mass_list())
#print(pure_list)
#mass_dict = {str(i): str(float(mass)) for i, mass in enumerate(mol.atom_mass_list())}
#print(mass_dict)
#print("atomic_masses_used written in atomic_masses_from_pyscf.json:")
#with open('atomic_masses_from_pyscf.json', 'w') as f:
#    json.dump(mass_dict, f, indent=4)
#print("Basise set used:",args.basisset)


# na2c is the number of 2-component spin-orbitals (2 * nao)
n2c = mol.nao_2c()
# 2. Large-Large (LL) Spinor Dipole Integrals: <µ_L| r |ν_L>
# Keyword: 'int1e_r_spinor'
# Output shape: (3, n2c, n2c) with complex values
ll_dip = mol.intor_symmetric('int1e_r_spinor', comp=3)
# 3. Small-Small (SS) Spinor Dipole Integrals: <µ_S| (σ·p) r (σ·p) |ν_S>
# Keyword: 'int1e_sprsp_spinor'
# Output shape: (3, n2c, n2c) with complex values
ss_dip = mol.intor_symmetric('int1e_sprsp_spinor', comp=3)
#print("Large-component dipole matrix shape:", ll_dip.shape)
#print("Small-component dipole matrix shape:", ss_dip.shape)

# Extract 4-C density matrix blocks
dm_LL = dm[:n2c, :n2c]
dm_SS = dm[n2c:, n2c:]

c=lib.param.LIGHT_SPEED
print(c)

# Compute LL and SS electronic dipole contributions
elec_dip_LL = -np.einsum('xij,ji->x', ll_dip, dm_LL).real
elec_dip_SS = -np.einsum('xij,ji->x', ss_dip, dm_SS).real * (0.5 / c)**2
AU_TO_DEBYE = 2.54174623

# Total Electronic Dipole
elec_dip_total_au = elec_dip_LL + elec_dip_SS

#print("LL Contribution (au):", elec_dip_LL )
#print("SS Contribution (au):", elec_dip_SS )
#print("Total Electronic Dipole (a.u.):", elec_dip_total_au)

# 4. Nuclear Dipole Vector
charges = mol.atom_charges()
coords = mol.atom_coords()
nuc_dip = np.dot(charges, coords)
print(" ")
print("Nuclear  Dipole (au):     ", nuc_dip)
print("Electric Dipole (au):     ", elec_dip_total_au)
tot_dip=elec_dip_total_au+nuc_dip
print("Total    Dipole (a.u.):   ", tot_dip)
dip=np.sqrt(tot_dip@tot_dip)
print(f"Total dipole moment (a.u)  : {dip:.5f}")
print(f"Total dipole moment (Debye): {dip*AU_TO_DEBYE:.5f}")

print("")
print("For test:Non-relativistic RHF")
# 1. Hartree-Fock (RHF)
mf_hf = scf.RHF(mol).run()
dip_hf = np.linalg.norm(mf_hf.dip_moment(unit='Debye', verbose=False))
print(f"Non-reativistic:RHF:   {dip_hf:.4f} Debye")

