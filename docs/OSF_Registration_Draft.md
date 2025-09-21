# OSF Preregistration: Association Between APOE4 Carrier Status and Web-based Central Hearing Performance

This document outlines the research plan for a secondary analysis of data from the Great Minds dementia cohort.

## Metadata

* **Title:** Association Between APOE4 carrier status and Web-based Central Hearing Performance
* **Description:** This study will conduct a secondary analysis of data from the Great Minds cohort, a research-ready register managed by the Dementia Platform UK. The primary aim is to investigate the relationship between Apolipoprotein E4 (APOE4) allele status and performance on remote hearing tests. By analysing these pre-existing genetic and audiological data, the project seeks to explore the relationship between a key genetic risk factor for Alzheimer's disease and hearing function, providing potential insights into the early risk profiling of dementia.
* **Contributors:** Chris Happs and Meher Lad
* **Category:** Project
* **Affiliated Institutions:** No affiliated institutions
* **License:** [License Type, e.g., CC BY 4.0]
* **Subjects:** Medicine and Health Sciences
* **Tags:** Apolipoprotein E, Dementia, Hearing

---

## Study Information

### Research Questions

* Is APOE ε4 carrier status associated with poorer performance on auditory measures (digits in noise, speech in noise, auditory working memory frequency precision, auditory working memory amplitude modulation, Glasgow Hearing Aid Benefit Profile)?
* Are auditory performance measures associated with cognitive performance (Paired Associates Learning)?

### Hypotheses

* **H1:** APOE ε4 carrier status will be significantly associated with poorer performance on auditory measures. We predict that individuals with one or more ε4 alleles will show lower performance compared to non-carriers after controlling for age, sex, education, and cognitive performance.
* **H2:** Auditory measures will be significantly associated with cognitive performance (PAL), with speech in noise performance expected to be a strong predictor.

---

## Data Description

### Datasets Used

This study will use a pre-existing, cross-sectional dataset from the Great Minds cohort, a research register managed by Dementia Platform UK (DPUK). The specific data for this analysis includes APOE genotype status, derived from saliva samples, and performance metrics from remote, self-administered hearing tests. We will use the subset of participants for whom both complete APOE genotyping and remote hearing test data are available.

### Data Availability & Access

The dataset is available through protected access. Researchers must submit a formal application through the Dementia Platform UK (DPUK) Data Portal.

* **Data Identifier:** `https://portal.dementiasplatform.uk`

### Data Collection Procedures

The data collection procedures are documented by DPUK. APOE genotyping was performed on DNA extracted from saliva samples, and remote hearing performance was assessed using self-administered, web-based audiological tests.

### Variables

* **Primary Outcome Variables (Dependent Variables):** Five standardized auditory performance measures:
  - `dm`: Digits in noise score (continuous)
  - `slb`: Speech in noise score (continuous)
  - `awm_freq`: Auditory working memory frequency precision (continuous)
  - `awm_am`: Auditory working memory amplitude modulation (continuous)
  - `gmsi_tot`: Glasgow Hearing Aid Benefit Profile total score (continuous)
* **Predictor Variable (Independent Variable):** APOE ε4 carrier status (binary: 0 = non-carrier, 1 = carrier).
* **Additional Variables:**
  - `PALTEA28z`: Paired Associates Learning z-score (cognitive outcome, continuous)
  - `HighestEducation`: Education level (categorical)
  - `UnencryptedGender`: Gender (categorical)
  - `age`: Age in years (continuous)
* **Covariates:** Age, gender, education level, and cognitive performance (PALTEA28z) depending on analysis.

### Missing Data & Exclusions

* Participants with missing data for any analyzed variables will be excluded from specific analyses.
* Participants carrying the APOE ε2 allele will be excluded from primary APOE analyses due to its potentially protective effects.
* Final sample sizes will be reported for each analysis.

### Sample Size

The initial dataset contains 201 participants. After exclusions:
- Primary APOE analyses (excluding ε2 carriers): ~178 participants (128 non-carriers, 50 carriers)
- Secondary analyses (full sample): 201 participants

### Data Processing

All auditory measures will be z-transformed for standardized effect size interpretation in models. APOE ε4 dose (0, 1, 2 alleles) and carrier status (0/1) will be derived from APOE genotype data.

---

## Analyses

### Hypothesis 1: APOE ε4 Impact on Auditory Performance

**Adjusted Linear Models:** Multiple linear regression models testing APOE ε4 carrier status effects on each auditory measure, controlling for covariates:
* **Full Model:** `Auditory_Measure = β₀ + β₁(APOE_Status) + β₂(Age) + β₃(Education) + β₄(Gender) + β₅(PALTEA28z) + ε`
* **No Cognition Model:** `Auditory_Measure = β₀ + β₁(APOE_Status) + β₂(Age) + β₃(Education) + β₄(Gender) + ε`
* **Minimal Model:** `Auditory_Measure = β₀ + β₁(APOE_Status) + β₂(Age) + β₄(Gender) + ε`

**Unadjusted Group Comparisons:** Welch's t-tests comparing auditory measures between APOE ε4 carriers and non-carriers without covariates.

### Hypothesis 2: Auditory Performance and Cognitive Associations

**Auditory-Cognition Associations:** Pearson correlations between z-transformed auditory measures and PALTEA28z.

**Predictive Models:** Multiple linear regression models predicting PALTEA28z from individual auditory measures:
* **Baseline:** `PALTEA28z = β₀ + β₁(Auditory_z) + β₂(Age) + β₃(Gender) + β₄(Education) + ε`
* **With APOE:** `PALTEA28z = β₀ + β₁(Auditory_z) + β₂(Age) + β₃(Gender) + β₄(Education) + β₅(APOE_Status) + ε`

### Statistical Methods

* **Multiple Testing Correction:** False Discovery Rate (FDR) correction using Benjamini-Hochberg method across related tests.
* **Robust Standard Errors:** Heteroscedasticity-consistent (HC3) standard errors for regression models.
* **Effect Size Standardization:** Z-transformation of auditory variables for interpretable standardized coefficients.

### Inference Criteria

* Statistical significance threshold: p < 0.05 (two-tailed)
* FDR-corrected p-values reported for multiple comparison families
* Confidence intervals (95%) reported for all effect estimates

### Exploratory Analyses

* APOE gene-dose effects (0, 1, 2 ε4 alleles) using ANOVA
* Potential sex differences in APOE-auditory relationships
* Auditory measure inter-correlations
* Sensitivity analyses excluding APOE ε2 carriers

---

## Deviations from Original Preregistration

This analysis represents an expansion beyond the originally preregistered plan. Key deviations include:

* **Expanded Scope:** Originally planned for a single "hearing performance score"; actual analysis examined five distinct auditory measures
* **Enhanced Statistical Rigor:** Added FDR correction for multiple testing, robust standard errors, and z-transformation for standardized effects
* **Additional Analyses:** Included auditory inter-correlations, auditory-cognition relationships, and predictive modeling of cognition
* **Sample Processing:** Added exclusion of APOE ε2 carriers and more sophisticated handling of missing data
* **Covariate Strategy:** Expanded from simple age/sex adjustment to include education and cognitive performance as covariates

These expansions were necessary to fully characterize the complex relationships between APOE status, auditory performance, and cognition, while maintaining statistical rigor appropriate for the research questions.
