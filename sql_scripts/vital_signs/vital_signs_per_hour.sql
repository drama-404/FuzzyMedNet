WITH pvt AS (
  SELECT ie.subject_id, ie.hadm_id, ie.icustay_id,
    DATE_TRUNC('hour', ce.charttime) AS chart_hour,
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
      WHEN itemid in (762,226512) AND valuenum > 0 THEN 9 -- Weight at Admission
      ELSE NULL END AS vitalid,
      -- convert F to C
      CASE WHEN itemid IN (223761,678) THEN (valuenum-32)/1.8 ELSE valuenum END AS valuenum
  FROM icustays ie
  LEFT JOIN chartevents ce
    ON ie.icustay_id = ce.icustay_id
    AND ce.charttime BETWEEN ie.intime AND (ie.intime + INTERVAL '1 day')
    AND EXTRACT(EPOCH FROM (ce.charttime - ie.intime)) > 0
    AND EXTRACT(HOUR FROM (ce.charttime - ie.intime)) <= 24
    AND (ce.error IS NULL OR ce.error = 0)
  WHERE ce.itemid IN (
    211, 220045, -- HEART RATE
    51, 442, 455, 6701, 220179, 220050, -- SYS BP
    8368, 8440, 8441, 8555, 220180, 220051, -- DIAS BP
    456, 52, 6702, 443, 220052, 220181, 225312, -- MEAN ARTERIAL PRESSURE
    618, 615, 220210, 224690, -- RESPIRATORY RATE
    646, 220277, -- SpO2
    807, 811, 1529, 3745, 3744, 225664, 220621, 226537, -- GLUCOSE
    223762, 676, 223761, 678, -- TEMPERATURE
    762,226512       -- WEIGHT
  )
)
SELECT pvt.hadm_id, pvt.icustay_id, pvt.vitalid, pvt.chart_hour, pvt.valuenum
FROM pvt
ORDER BY pvt.hadm_id, pvt.icustay_id, pvt.vitalid, pvt.chart_hour;
