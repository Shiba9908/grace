# Diffusion, method comparisons, and phase field

The user has named MLIP, LAMMPS, DFT, and phase field as research directions.
Confirm whether an ambiguous "diff" request means diffusion, differences between
methods, or both. These workflows guide preparation and verification; they do not
imply an installed solver, completed simulation, or validated coupled model.

## Diffusion

For MD-derived diffusion, record diffusing species, concentration, ensemble,
temperature/pressure, timestep, thermostat/barostat, equilibration, production
duration, output stride, independent replicas, and model domain. Use unwrapped
coordinates and account for host/global drift appropriately. Verify a diffusive
regime and fit window, report dimensionality and units, and use independent
blocks/replicas for uncertainty. Do not report a reliable diffusivity from a
trapped short trajectory or fit ballistic motion as diffusion.

For NEB/hopping, verify endpoint minima and atom correspondence, path/images,
force definition and tolerances, climbing-image convergence, and the saddle's
character as appropriate. Distinguish electronic barriers, ZPE-corrected barriers,
and free-energy barriers. Relate hops to initial/final motifs and preserve network
connectivity. A barrier alone does not define a macroscopic diffusion coefficient;
state assumptions about prefactors, occupancies and kinetic models.

## Compare methods

Define the comparison before running: same structure and potential across ASE and
LAMMPS; different MLIPs on the same benchmark; or MLIP versus converged DFT.
Freeze the sample list and state whether energies, forces, stresses, relaxed
structures, barriers, diffusivities or runtime are compared. Match units,
references, precision and boundary conditions. Report missing/failed samples
alongside paired results. Keep compute speed and physical accuracy separate.

## Phase-field handoff

Identify the governing free energy and conserved/nonconserved fields before
choosing a solver. Record composition basis, phase definitions, temperature,
thermodynamic model, gradient energy, mobility, elasticity if included, boundary
conditions, grid and timestep. Retain source, units, validity range and uncertainty
for each parameter transferred from atomistic work or CALPHAD.

Check mesh/timestep sensitivity, conservation for conserved fields, bounds and
expected equilibrium/energy behaviour appropriate to the equations and boundary
conditions. Do not enforce monotonic energy decay when external driving/noise
makes that condition inapplicable. Atomistic insertion energies alone do not
constitute a phase-field free-energy model; document the statistical and
coarse-graining assumptions that connect the scales.

Consult the selected solver's current primary documentation, for example
[LAMMPS diffusion methods](https://docs.lammps.org/Howto_diffusion.html) and the
[MOOSE phase-field module](https://mooseframework.inl.gov/modules/phase_field/).
These links do not prescribe a solver choice or indicate either is installed.
