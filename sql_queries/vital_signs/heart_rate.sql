-- --------------------------------------------------------
-- Title: Create a histogram of heart rates for adult patients
-- --------------------------------------------------------
WITH agetbl AS
(
  SELECT ad.subject_id, ad.hadm_id
  FROM admissions ad
  INNER JOIN patients p
  ON ad.subject_id = p.subject_id
  WHERE
  EXTRACT(YEAR FROM age(ad.admittime, p.dob)) > 15
  group by ad.subject_id, ad.hadm_id
)
, hr as
(
  SELECT width_bucket(valuenum, 0, 300, 301) AS bucket
  FROM chartevents ce
  INNER JOIN agetbl
  ON ce.hadm_id = agetbl.hadm_id
  WHERE itemid in (211,220045)
)
SELECT bucket as heart_rate, count(*)
FROM hr
GROUP BY bucket
ORDER BY bucket;

-- --------------------------------------------------------
-- Title: Retrieve min & max heart rate per admission
-- --------------------------------------------------------
WITH agetbl AS
(
  SELECT ad.subject_id, ad.hadm_id
  FROM admissions ad
  INNER JOIN patients p
  ON ad.subject_id = p.subject_id
  -- group by subject_id, hadm_id to ensure there is only 1 row per admission
  GROUP BY ad.subject_id, ad.hadm_id
)
SELECT agetbl.hadm_id, MIN(ce.valuenum) AS min_heart_rate, MAX(ce.valuenum) AS max_heart_rate
FROM chartevents ce
INNER JOIN agetbl
ON ce.subject_id = agetbl.subject_id
AND ce.hadm_id = agetbl.hadm_id
WHERE ce.itemid IN (211,220045)
AND ce.valuenum IS NOT NULL -- Excludes rows with NULL heart rates
AND ce.valuenum > 0 -- Excludes non-physiological values
AND ce.valuenum < 300 -- Excludes non-physiological values
GROUP BY agetbl.hadm_id;

