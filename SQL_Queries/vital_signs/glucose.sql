-- --------------------------------------------------------
-- Title: Retrieve a glucose histogram of adult patients
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
, glc as
(
  SELECT width_bucket(valuenum, 0.5, 1000, 1000) AS bucket
  FROM labevents le
  INNER JOIN agetbl
  ON le.hadm_id = agetbl.hadm_id
  WHERE itemid IN (50809,50931)
  AND valuenum IS NOT NULL
)
SELECT bucket as glucose, count(*)
FROM glc
GROUP BY bucket
ORDER BY bucket;

-- --------------------------------------------------------
-- Title: Retrieve min & max Glucose values per admission
-- --------------------------------------------------------

WITH agetbl AS
(
  SELECT ad.subject_id, ad.hadm_id
  FROM admissions ad
  INNER JOIN patients p
  ON ad.subject_id = p.subject_id
  GROUP BY ad.subject_id, ad.hadm_id
)
SELECT agetbl.hadm_id, MIN(le.valuenum) AS min_glucose, MAX(le.valuenum) AS max_glucose
FROM labevents le
INNER JOIN agetbl
ON le.subject_id = agetbl.subject_id
AND le.hadm_id = agetbl.hadm_id
WHERE le.itemid IN (50809,50931)
AND le.valuenum IS NOT NULL -- Excludes rows with NULL glucose levels
AND le.valuenum >= 0 -- Assume glucose levels cannot be negative
GROUP BY agetbl.hadm_id;
