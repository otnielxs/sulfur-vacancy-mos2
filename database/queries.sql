-- Show all systems

SELECT *
FROM systems;

-- Show all band gap

SELECT
    s.name,
    e.band_gap_ev
FROM electronic_structure e
JOIN systems s
    ON e.system_id = s.system_id;

-- Show all adsorption energies

SELECT
    s.name,
    a.adsorbate,
    a.adsorption_energy_ev
FROM adsorption_results a
JOIN systems s
    ON a.system_id = s.system_id;

-- Summary

SELECT
    s.name,
    e.band_gap_ev,
    a.adsorbate,
    a.adsorption_energy_ev
FROM systems s
LEFT JOIN electronic_structure e
    ON s.system_id = e.system_id
LEFT JOIN adsorption_results a
    ON s.system_id = a.system_id;
