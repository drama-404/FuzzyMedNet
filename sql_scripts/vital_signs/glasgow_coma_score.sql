-- --------------------------------------------------------
-- Title: Find the glasgow coma *MOTOR* score for each adult patient
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
, gcs as
(
    SELECT width_bucket(valuenum, 1, 30, 30) AS bucket
    FROM chartevents ce
    INNER JOIN agetbl
    ON ce.hadm_id = agetbl.hadm_id
    WHERE itemid IN
    (
        454 -- "Motor Response"
      , 223900 -- "GCS - Motor Response"
    )
)
SELECT bucket as GCS_Motor_Response, count(*)
FROM gcs
GROUP BY bucket
ORDER BY bucket;

-- --------------------------------------------------------
-- Title: Retrieve min & max GCS score per admission
-- --------------------------------------------------------

WITH agetbl AS
(
    SELECT ad.subject_id, ad.hadm_id
    FROM admissions ad
    INNER JOIN patients p
    ON ad.subject_id = p.subject_id
    GROUP BY ad.subject_id, ad.hadm_id
)
SELECT agetbl.hadm_id, MIN(ce.valuenum) AS min_gcs_motor, MAX(ce.valuenum) AS max_gcs_motor
FROM chartevents ce
INNER JOIN agetbl
ON ce.subject_id = agetbl.subject_id
AND ce.hadm_id = agetbl.hadm_id
WHERE ce.itemid IN
(
    454, -- "Motor Response"
    223900 -- "GCS - Motor Response"
)
AND ce.valuenum IS NOT NULL -- Excludes rows with NULL GCS Motor scores
AND ce.valuenum >= 1 -- The GCS Motor score ranges from 1 to 6
AND ce.valuenum <= 6
GROUP BY agetbl.hadm_id;
