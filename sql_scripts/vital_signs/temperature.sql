-- --------------------------------------------------------
-- Title: Retrieves the temperature of adult patients
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
, temp as
(
  SELECT width_bucket(
      CASE
        WHEN itemid IN (223762, 676, 677) THEN valuenum -- celsius
        WHEN itemid IN (223761, 678, 679) THEN (valuenum - 32) * 5 / 9 --fahrenheit
      END
    , 30, 45, 160) AS bucket
  FROM chartevents ce
  INNER JOIN agetbl
  ON ce.hadm_id = agetbl.hadm_id
  WHERE itemid IN
  (
      676 -- Temperature C
    , 677 -- Temperature C (calc)
    , 678 -- Temperature F
    , 679 -- Temperature F (calc)
    , 223761 -- Temperature Fahrenheit
    , 223762 -- Temperature Celsius
  )
)
SELECT round((cast(bucket as numeric)/10) + 30,2) as temperature, count(*)
FROM temp
GROUP BY bucket
ORDER BY bucket;

-- --------------------------------------------------------
-- Title: Retrieves min & max Temperature values per admission
-- --------------------------------------------------------

WITH agetbl AS
(
  SELECT ad.subject_id, ad.hadm_id
  FROM admissions ad
  INNER JOIN patients p
  ON ad.subject_id = p.subject_id
  group by ad.subject_id, ad.hadm_id
)
, temp as
(
  SELECT
    agetbl.hadm_id,
    min(
      CASE
        WHEN itemid IN (223762, 676, 677) THEN valuenum -- celsius
        WHEN itemid IN (223761, 678, 679) THEN (valuenum - 32) * 5 / 9 --fahrenheit
      END
    ) AS min_temp,
    max(
      CASE
        WHEN itemid IN (223762, 676, 677) THEN valuenum -- celsius
        WHEN itemid IN (223761, 678, 679) THEN (valuenum - 32) * 5 / 9 --fahrenheit
      END
    ) AS max_temp
  FROM chartevents ce
  INNER JOIN agetbl
  ON ce.hadm_id = agetbl.hadm_id
  WHERE itemid IN
  (
      676 -- Temperature C
    , 677 -- Temperature C (calc)
    , 678 -- Temperature F
    , 679 -- Temperature F (calc)
    , 223761 -- Temperature Fahrenheit
    , 223762 -- Temperature Celsius
  )
  GROUP BY agetbl.hadm_id
)
SELECT hadm_id, min_temp, max_temp
FROM temp;