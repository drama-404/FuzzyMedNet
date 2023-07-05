-- This query pivots the vital signs for the first 24 hours of a patient's stay
-- Vital signs include heart rate, blood pressure, respiration rate, and temperature

WITH pvt AS (
  SELECT ie.subject_id, ie.hadm_id, ie.icustay_id,
    CASE
      WHEN itemid IN (211,220045) AND valuenum > 0 AND valuenum < 300 THEN 1 -- HeartRate
      WHEN itemid IN (51,442,455,6701,220179,220050) AND valuenum > 0 AND valuenum < 400 THEN 2 -- SysBP
      WHEN itemid IN (8368,8440,8441,8555,220180,220051) AND valuenum > 0 AND valuenum < 300 THEN 3 -- DiasBP
      WHEN itemid IN (456,52,6702,443,220052,220181,225312) AND valuenum > 0 AND valuenum < 300 THEN 4 -- MeanBP
      WHEN itemid IN (615,618,220210,224690) AND valuenum > 0 AND valuenum < 70 THEN 5 -- RespRate
      WHEN itemid IN (223761,678) AND valuenum > 70 AND valuenum < 120  THEN 6 -- TempF, converted to degC in valuenum call
      WHEN itemid IN (223762,676) AND valuenum > 10 AND valuenum < 50  THEN 6 -- TempC
      WHEN itemid IN (646,220277) AND valuenum > 0 AND valuenum <= 100 THEN 7 -- SpO2
      WHEN itemid IN (807,811,1529,3745,3744,225664,220621,226537) AND valuenum > 0 THEN 8 -- Glucose
      ELSE NULL END AS vitalid,
      -- convert F to C
      CASE WHEN itemid IN (223761,678) THEN (valuenum-32)/1.8 ELSE valuenum END AS valuenum
  FROM icustays ie
  LEFT JOIN chartevents ce
    ON ie.icustay_id = ce.icustay_id
    AND ce.charttime BETWEEN ie.intime AND (ie.intime + INTERVAL '1 day')
    AND EXTRACT(EPOCH FROM (ce.charttime - ie.intime)) > 0
    AND EXTRACT(HOUR FROM (ce.charttime - ie.intime)) <= 24
    -- exclude rows marked as error
    AND (ce.error IS NULL OR ce.error = 0)
  WHERE ce.itemid IN (
    211, 220045, -- HEART RATE
    51, 442, 455, 6701, 220179, 220050, -- SYS BP
    8368, 8440, 8441, 8555, 220180, 220051, -- DIAS BP
    456, 52, 6702, 443, 220052, 220181, 225312, -- MEAN ARTERIAL PRESSURE
    618, 615, 220210, 224690, -- RESPIRATORY RATE
    646, 220277, -- SpO2
    807, 811, 1529, 3745, 3744, 225664, 220621, 226537, -- GLUCOSE
    223762, 676, 223761, 678 -- TEMPERATURE
  ))
SELECT pvt.subject_id, pvt.hadm_id, pvt.icustay_id,
  -- Easier names
  MIN(CASE WHEN vitalid = 1 THEN valuenum ELSE NULL END) AS heartrate_min,
  MAX(CASE WHEN vitalid = 1 THEN valuenum ELSE NULL END) AS heartrate_max,
  AVG(CASE WHEN vitalid = 1 THEN valuenum ELSE NULL END) AS heartrate_mean,
  MIN(CASE WHEN vitalid = 2 THEN valuenum ELSE NULL END) AS sysbp_min,
  MAX(CASE WHEN vitalid = 2 THEN valuenum ELSE NULL END) AS sysbp_max,
  AVG(CASE WHEN vitalid = 2 THEN valuenum ELSE NULL END) AS sysbp_mean,
  MIN(CASE WHEN vitalid = 3 THEN valuenum ELSE NULL END) AS diasbp_min,
  MAX(CASE WHEN vitalid = 3 THEN valuenum ELSE NULL END) AS diasbp_max,
  AVG(CASE WHEN vitalid = 3 THEN valuenum ELSE NULL END) AS diasbp_mean,
  MIN(CASE WHEN vitalid = 4 THEN valuenum ELSE NULL END) AS meanbp_min,
  MAX(CASE WHEN vitalid = 4 THEN valuenum ELSE NULL END) AS meanbp_max,
  AVG(CASE WHEN vitalid = 4 THEN valuenum ELSE NULL END) AS meanbp_mean,
  MIN(CASE WHEN vitalid = 5 THEN valuenum ELSE NULL END) AS resprate_min,
  MAX(CASE WHEN vitalid = 5 THEN valuenum ELSE NULL END) AS resprate_max,
  AVG(CASE WHEN vitalid = 5 THEN valuenum ELSE NULL END) AS resprate_mean,
  MIN(CASE WHEN vitalid = 6 THEN valuenum ELSE NULL END) AS tempc_min,
  MAX(CASE WHEN vitalid = 6 THEN valuenum ELSE NULL END) AS tempc_max,
  AVG(CASE WHEN vitalid = 6 THEN valuenum ELSE NULL END) AS tempc_mean,
  MIN(CASE WHEN vitalid = 7 THEN valuenum ELSE NULL END) AS spo2_min,
  MAX(CASE WHEN vitalid = 7 THEN valuenum ELSE NULL END) AS spo2_max,
  AVG(CASE WHEN vitalid = 7 THEN valuenum ELSE NULL END) AS spo2_mean,
  MIN(CASE WHEN vitalid = 8 THEN valuenum ELSE NULL END) AS glucose_min,
  MAX(CASE WHEN vitalid = 8 THEN valuenum ELSE NULL END) AS glucose_max,
  AVG(CASE WHEN vitalid = 8 THEN valuenum ELSE NULL END) AS glucose_mean
FROM pvt
GROUP BY pvt.subject_id, pvt.hadm_id, pvt.icustay_id
ORDER BY pvt.subject_id, pvt.hadm_id, pvt.icustay_id;

