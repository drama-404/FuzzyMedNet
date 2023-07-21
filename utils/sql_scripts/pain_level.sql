WITH pvt AS (
  SELECT ie.subject_id, ie.hadm_id, ie.icustay_id,
    DATE_TRUNC('hour', ce.charttime) AS chart_hour,
    CASE
      WHEN itemid IN (1044,223791) THEN value ELSE NULL
    END AS valuenum
  FROM icustays ie
  LEFT JOIN chartevents ce
    ON ie.icustay_id = ce.icustay_id
    AND ce.charttime BETWEEN ie.intime AND (ie.intime + INTERVAL '1 day')
    AND EXTRACT(EPOCH FROM (ce.charttime - ie.intime)) > 0
    AND EXTRACT(HOUR FROM (ce.charttime - ie.intime)) <= 24
    AND (ce.error IS NULL OR ce.error = 0)
  WHERE ce.itemid IN (
    1044,223791   -- PAIN SCORE
  )
)
SELECT pvt.hadm_id, pvt.icustay_id, pvt.chart_hour, pvt.valuenum
FROM pvt
ORDER BY pvt.hadm_id, pvt.icustay_id, pvt.chart_hour;