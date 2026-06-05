# High-Temperature Creep and Stress-Relaxation Modelling of 316H Stainless Steel

## Project Summary

This project develops a computational framework for high-temperature creep and stress-relaxation modelling of Type 316H austenitic stainless steel. Real neutron-diffraction measurements and finite-element simulation results are combined to study stress redistribution, time-dependent deformation, and constitutive behaviour at elevated temperature.

The workflow focuses on processing experimental and simulation datasets, validating finite-element predictions against measured stress states, and calibrating simplified stress-relaxation models for structural-integrity applications.

### Key Contributions

- Real-data analysis using neutron-diffraction measurements from 316H stainless steel
- Finite-element validation using interpolated stress tensors at measurement locations
- High-temperature stress-relaxation and creep behaviour assessment
- Constitutive modelling using Norton, Norton–Bailey and Garofalo-type creep laws
- Calibration of a reduced-order stress-relaxation model from experimental/FEA data
- Automated processing of MATLAB, CSV and finite-element output datasets
- Reproducible Python workflow for material modelling and validation

### Research Relevance

- High-temperature structural integrity
- Austenitic stainless steels
- Creep and viscoplastic deformation
- Constitutive material modelling
- Experimental–simulation correlation
- Finite-element validation
- Materials informatics and scientific computing

## Research motivation

Type 316H austenitic stainless steel is used in high-temperature structural components where time-dependent creep deformation and stress relaxation can control long-term integrity. For safety-critical components, it is not enough to know the initial stress state; the stress tensor evolves during high-temperature exposure. This repository demonstrates how real neutron-diffraction measurements and interpolated finite-element results can be processed into a reproducible modelling workflow for stress relaxation at **550 °C**.

## Real data included

This repository includes a compact numerical subset from the University of Bristol dataset:

> Harry Coules (2020), **Multiaxial creep stress relaxation in 316H stainless steel**, University of Bristol data repository, DOI: `10.5523/bris.rhg1bk2424a6262ecb9nouzp9`.

The uploaded source archive contains:

- neutron-diffraction stress/strain tensor measurements,
- finite-element model results interpolated at neutron measurement locations,
- Double-Cantilever Beam specimen information,
- Abaqus input/data files and Fortran creep-law files.

For GitHub practicality, this repository includes the compact `.mat` files needed for the numerical workflow, not the full large Abaqus `.dat` and `.cae` files.

## What this repository implements

1. **Real-data ingestion**
   - Reads Bristol 316H MATLAB `.mat` files.
   - Converts neutron-diffraction stress tensors and interpolated FEA tensors into tidy CSV files.
   - Joins measured and simulated stress states at the same measurement locations and exposure times.

2. **Real-data validation**
   - Compares neutron-diffraction von Mises stress with interpolated FEA predictions.
   - Produces location-wise residual maps and relaxation-evolution plots.
   - Stores reproducible validation metrics.

3. **Stress-relaxation modelling**
   - Fits a compact exponential stress-relaxation law to the real 316H FEA relaxation trend.
   - Provides a bridge toward more advanced Norton, Norton-Bailey, Garofalo, or Chaboche-type viscoplastic models.

4. **Constitutive creep modules**
   - Norton power-law creep.
   - Norton-Bailey time-hardening creep.
   - Garofalo hyperbolic-sine creep law.
   - Simple stress-relaxation integration under fixed total strain.

5. **PhD-level extension path**
   - Abaqus CREEP/UMAT implementation.
   - Creep-fatigue dwell modelling.
   - Microstructure descriptors such as grain size, carbide precipitation, and EBSD features.
   - Extension to nickel-base superalloys.

## Key processed outputs

After running the real-data scripts, the repository creates:

```text
data/processed/bristol_316h_neutron_stress_tensor.csv
data/processed/bristol_316h_fea_interpolated_stress_tensor.csv
data/processed/bristol_316h_joined_nd_fea.csv
data/processed/bristol_316h_relaxation_summary.csv

figures/bristol_316h_stress_relaxation_nd_vs_fea.png
figures/bristol_316h_fea_vs_neutron_svm.png
figures/bristol_316h_location_residuals_heatmap.png
figures/bristol_316h_fitted_relaxation_law.png

results/bristol_316h_realdata_metrics.json
results/bristol_316h_relaxation_law_fit.json
```

## Current real-data results

Using the Bristol 316H compact numerical dataset, the workflow processed **72 measurement points**: 6 exposure times and 12 neutron measurement locations.

For the interpolated FEA versus neutron-diffraction von Mises stress comparison, the current validation metrics are:

```json
{
  "n_measurements": 72,
  "temperature_C": 550.0,
  "mae_sVM_MPa": 24.09,
  "rmse_sVM_MPa": 33.12,
  "r2_sVM": -0.72
}
```

The negative R² is not hidden. It is discussed as a useful scientific result: the sparse neutron measurements and interpolated FEA fields do not match perfectly point-by-point, which is realistic for multiaxial stress-relaxation validation. The mean FEA relaxation trend is smoother and can be fitted well by a compact relaxation law:

```json
{
  "sigma_inf_MPa": 80.05,
  "sigma0_MPa": 93.91,
  "tau_h": 381.84,
  "r2": 0.94
}
```



## Repository structure

```text
src/
  ingest_bristol_mat.py             # real Bristol .mat ingestion
  analyze_bristol_realdata.py       # validation plots and metrics
  fit_relaxation_law_realdata.py    # simple real-data relaxation-law fit
  creep_models.py                   # Norton / Norton-Bailey / Garofalo laws
  calibration.py                    # fitting utilities
  stress_relaxation.py              # stress-relaxation ODE integration
  parse_abaqus_outputs.py           # Abaqus text parser utilities

data/
  raw_external/bristol_316h_subset/ # compact real-data .mat files
  processed/                        # generated tidy CSV datasets

figures/                            # generated validation and fit figures
results/                            # generated JSON metrics
reports/technical_note.md
```

## Scientific honesty

This repository does not claim new laboratory experiments. It uses real open experimental/FE data from the Bristol 316H dataset and builds an original, reproducible computational workflow around it. The constitutive-law fitting is intentionally compact and educational; the next research step would be implementation of a full temperature-dependent creep/viscoplastic law and validation against complete FE fields or additional creep rupture data.
