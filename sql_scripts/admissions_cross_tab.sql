SELECT DISTINCT admission_location FROM admissions ORDER BY admission_location;

SELECT DISTINCT admission_type FROM admissions ORDER BY admission_type;

SELECT *
FROM crosstab(
       'SELECT admission_location,
               CASE
                   WHEN admission_type IN (''EMERGENCY'', ''URGENT'') THEN ''EMERGENCY''
                   ELSE admission_type
               END AS admission_type,
               count(*) as ct
        FROM   admissions
        GROUP BY admission_location, admission_type
        ORDER BY 1,2'
      -- below, we list all the unique values in admission_type
      -- these will become the columns
      -- hard-coding them ensures that the order matches what we specify later
      ,$$VALUES ('ELECTIVE'::text), ('EMERGENCY'::text), ('NEWBORN'::text)$$
    )
AS ct (
  -- first column has each unique value for the rows
  "Admission Location" text,
  -- now we list the columns
  "ELECTIVE" text, "EMERGENCY/URGENT" text, "NEWBORN" text
);