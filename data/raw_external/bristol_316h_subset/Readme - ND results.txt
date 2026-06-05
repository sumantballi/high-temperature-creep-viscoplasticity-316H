*Start of Readme - ND results.txt*
DATASET: Multiaxial creep stress relaxation in 316H stainless steel - Version 1.0
Copyright Harry Coules 2020

NEUTRON DIFFRACTION RESULTS:
 lattice data.mat - This contains lattice parameter data from the time-of-flight neutron diffraction measurements. The lattice parameters were determined from Pawley-type structure refinement of the raw neutron diffraction data. Includes:
 
 	measurementLocs - Measurement locations in sample coordinate system.
	scatteringVects - Scattering vectors i.e. measured strain directions.
 
	a -  Lattice parameters.
	a0 - Unstrained lattice parameters.
	ua - Standard uncertainties in lattice parameter from structure fitting.
	ua0 - Standard uncertainties in unstrained lattice parameter from structure fitting.
	
	eMeas - Strains in measured directions.
	ueMeas - Standard uncertainty in measured strains.

	e - Strain tensor (components given in Voigt order).
	ue - Standard uncertainty in the strain tensor (components given in Voigt order).
	
	s - Stress tensor (components given in Voigt order).
	us - Standard uncertainty in the stress tensor (components given in Voigt order).
	sVM - Von Mises equivalent stress.
 
NOTES:
 - In the experiment, the 800 hour specimen was scanned first and the 0 hour specimen was scanned last. So results are always given in the order: 800hr, 200hr, 50hr, 10hr, 1hr, 0hr.
 - The sample coordinate system used in measurements was different to that used in FEA (also used for prestnation of the results in the paper). The origin of the coordinate systems is the same, however the axis direction map as:
	FEA  - x  y  z
	Exp. - y  z  x

*End of Readme - ND results.txt*