*Start of Readme.txt*
DATASET: Multiaxial creep stress relaxation in 316H stainless steel - Version 1.0
Copyright Harry Coules 2020

This file is best viewed with word wrap on.
This file last modified on: 06/05/2020.

%INTRODUCTION
This dataset contains information on the stress relaxation of 316H austenitic stainless steel at high temperature (550 deg. C). It includes the results of stress measurements performed on Double-Cantilever Beam (DCB) creep relaxation speciments, and the results of Finite Element Analysis (FEA) used to predict stress relaxation in the same specimens. It accompanies the paper:

H. E. Coules, S. O. Nneji, J. A. James, S. Kabra, J. N. Hu and Y. Wang, "Full-tensor measurement of multiaxial creep stress relaxation in 316H stainless steel".

%DATA INCLUDED IN THIS DATASET
This dataset contains:
 1. Time-of-flight neutron diffraction measurement results from the experiment described in the paper (ISIS experiment number: RB1610043). Measured lattice parameter values and analysed stress and strain tensors are given in this dataset. The raw neutron diffraction data are available from the ISIS data catalogue: https://data.isis.stfc.ac.uk/.
 2. Finite Element Analysis (FEA) model files, solver input files and data files for FEA modelleng performed to predict the creep relaxation in the same specimens as used in the experimental tests. FEA results interpolated onto the neutron diffraction measurement locations are also given.
 3. Drawings showing the experimental specimen design and the orientation in which the specimens were extracted from the parent component.
 
 %SOFTWARE
 - The neutron diffraction results are given in the MATLAB .mat v7.3+ format , which is hdf-5 based. They can be viewed using any modern version of MATLAB (The MathWorks, RI, USA).
 - FEA solver input (.inp) and data (.dat) files can be opened with any text editor. The model files (.cae) require Dassaut Systemes Abaqus/CAE v6.12 or above. Interpolated FEA reults at the neutron diffraction measurment locations are given in .mat format and can be opened using any modern version of MATLAB.

%CONTACT
data-bris@bristol.ac.uk

*End of Readme.txt*