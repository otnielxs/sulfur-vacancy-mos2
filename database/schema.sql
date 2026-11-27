
DROP TABLE IF EXISTS neb_results CASCADE;
DROP TABLE IF EXISTS adsorption_results CASCADE;
DROP TABLE IF EXISTS electronic_structure CASCADE;
DROP TABLE IF EXISTS systems CASCADE;

-- Systems

CREATE TABLE systems (
    system_id SERIAL PRIMARY KEY,

    name VARCHAR(100) NOT NULL,
    description TEXT,

    has_vacancy BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Adsorption Results

CREATE TABLE adsorption_results (
    adsorption_id SERIAL PRIMARY KEY,

    system_id INTEGER NOT NULL,

    adsorbate VARCHAR(20) NOT NULL,

    adsorption_energy_ev DOUBLE PRECISION,

    bond_length_angstrom DOUBLE PRECISION,

    notes TEXT,

    CONSTRAINT fk_adsorption_system
        FOREIGN KEY(system_id)
        REFERENCES systems(system_id)
);

-- Electronic Structure

CREATE TABLE electronic_structure (
    electronic_id SERIAL PRIMARY KEY,

    system_id INTEGER NOT NULL,

    band_gap_ev DOUBLE PRECISION,

    calculation_type VARCHAR(30),

    notes TEXT,

    CONSTRAINT fk_electronic_system
        FOREIGN KEY(system_id)
        REFERENCES systems(system_id)
);

-- NEB Results

CREATE TABLE neb_results (
    neb_id SERIAL PRIMARY KEY,

    system_id INTEGER NOT NULL,

    reaction VARCHAR(200),

    activation_barrier_ev DOUBLE PRECISION,

    reaction_energy_ev DOUBLE PRECISION,

    converged BOOLEAN,

    notes TEXT,

    CONSTRAINT fk_neb_system
        FOREIGN KEY(system_id)
        REFERENCES systems(system_id)
);
