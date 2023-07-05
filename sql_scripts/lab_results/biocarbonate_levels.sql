-- --------------------------------------------------------
-- Title: Create a histogram bicarbonate levels for all patients (adults and neonates)
-- --------------------------------------------------------

WITH agetbl AS
(
  SELECT ad.subject_id, ad.hadm_id
  FROM admissions ad
  INNER JOIN patients p
  ON ad.subject_id = p.subject_id
  WHERE
  -- filter to only adults
  EXTRACT(YEAR FROM age(ad.admittime, p.dob)) > 15
  -- group by subject_id to ensure there is only 1 subject_id per row
  group by ad.subject_id, ad.hadm_id
)
, hco as
(
  SELECT width_bucket(valuenum, 0, 231, 231) AS bucket
  FROM labevents le
  INNER JOIN agetbl
  ON le.hadm_id = agetbl.hadm_id
  WHERE itemid IN (50803, 50804, 50882)
  AND valuenum IS NOT NULL
)
SELECT bucket as bicarbonate, count(*)
FROM hco
GROUP BY bucket
ORDER BY bucket;

-- --------------------------------------------------------
-- Title: Retrieve min & mac Biocarbonate values per admission
-- --------------------------------------------------------

WITH agetbl AS
(
  SELECT ad.subject_id, ad.hadm_id
  FROM admissions ad
  INNER JOIN patients p
  ON ad.subject_id = p.subject_id
  GROUP BY ad.subject_id, ad.hadm_id
)
SELECT agetbl.hadm_id, MIN(le.valuenum) AS min_bicarbonate, MAX(le.valuenum) AS max_bicarbonate
FROM labevents le
INNER JOIN agetbl
ON le.subject_id = agetbl.subject_id
AND le.hadm_id = agetbl.hadm_id
WHERE le.itemid IN (50803, 50804, 50882)
AND le.valuenum IS NOT NULL -- Exclude rows with NULL bicarbonate levels
AND le.valuenum >= 0 -- Assume bicarbonate levels cannot be negative
GROUP BY agetbl.hadm_id;
