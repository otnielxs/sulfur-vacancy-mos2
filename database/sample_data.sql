-- Systems

INSERT INTO systems
(name, description, has_vacancy)
VALUES

(
'Pristine MoS2',
'Reference monolayer MoS2',
FALSE
),

(
'S-vacancy MoS2',
'Single sulfur vacancy',
TRUE
),

(
'S-vacancy + H2O',
'H2O adsorbed on sulfur vacancy',
TRUE
),

(
'S-vacancy + O2',
'O2 adsorbed on sulfur vacancy',
TRUE
);

-- Adsorption

INSERT INTO adsorption_results
(
system_id,
adsorbate,
adsorption_energy_ev,
bond_length_angstrom,
notes
)
VALUES

(
3,
'H2O',
-0.15,
NULL,
'Weak adsorption'
),

(
4,
'O2',
-3.21,
1.36,
'Strong adsorption and activation'
);

-- Band Gap

INSERT INTO electronic_structure
(
system_id,
band_gap_ev,
calculation_type,
notes
)
VALUES

(
1,
1.54,
'BAND',
'Pristine reference'
),

(
2,
0.26,
'BAND',
'Sulfur vacancy'
),

(
3,
0.14,
'BAND',
'H2O adsorption'
),

(
4,
0.98,
'BAND',
'O2 adsorption'
);

-- NEB

INSERT INTO neb_results
(
system_id,
reaction,
activation_barrier_ev,
reaction_energy_ev,
converged,
notes
)
VALUES

(
4,
'O2* -> 2O*',
1.0,
-1.0,
FALSE,
'Preliminary CI-NEB pathway'
);
