-- --------------------------------------------------------
-- Title: Create a distribution of BUN values for adult hospital admissions
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
    -- group by hadm_id to ensure there is only 1 entry per admission
    group by ad.subject_id, ad.hadm_id
)
, bun as
(
  SELECT width_bucket(valuenum, 0, 280, 280) AS bucket
  FROM labevents le
  INNER JOIN agetbl
  ON le.hadm_id = agetbl.hadm_id
  WHERE itemid IN (51006)
)
SELECT bucket as blood_urea_nitrogen, count(*)
FROM bun
GROUP BY bucket
ORDER BY bucket;

-- --------------------------------------------------------
-- Title: Retrieve min & max BUN values per admission
-- --------------------------------------------------------

WITH agetbl AS
(
    SELECT ad.subject_id, ad.hadm_id
    FROM admissions ad
    INNER JOIN patients p
    ON ad.subject_id = p.subject_id
    -- group by hadm_id to ensure there is only 1 entry per admission
    GROUP BY ad.subject_id, ad.hadm_id
)
SELECT agetbl.hadm_id, MIN(le.valuenum) AS min_bun, MAX(le.valuenum) AS max_bun
FROM labevents le
INNER JOIN agetbl
ON le.subject_id = agetbl.subject_id
AND le.hadm_id = agetbl.hadm_id
WHERE le.itemid IN (51006)
AND le.valuenum IS NOT NULL -- Excludes rows with NULL BUN values
AND le.valuenum > 0 -- Excludes non-physiological values
AND le.valuenum < 280 -- Excludes non-physiological values
GROUP BY agetbl.hadm_id;
