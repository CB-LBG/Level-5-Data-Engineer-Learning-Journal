-- Insert distinct schools
INSERT INTO dim_school (school_code)
-- This INSERT statement populates the dim_school table with unique school codes.
SELECT DISTINCT "School Code"
-- It selects only the distinct values from the "School Code" column of the raw_import table.
FROM raw_import;

-- Insert distinct student demographics
INSERT INTO dim_student (sex)
-- This INSERT statement populates the dim_student table with unique student genders.
SELECT DISTINCT "Sex"
-- It selects only the distinct values from the "Sex" column of the raw_import table.
FROM raw_import;

-- Insert parent background data
INSERT INTO dim_parent_background (parent_revenue, father_education, mother_education)
-- This INSERT statement populates the dim_parent_background table with unique combinations of parent revenue, father's education, and mother's education.
SELECT DISTINCT "Parent Revenue", "Father Education", "Mother Education"
-- It selects only the distinct combinations of values from the specified columns of the raw_import table.
FROM raw_import;

-- Insert gaming habits
INSERT INTO dim_gaming_habits (playing_years, playing_often, playing_hours, plays_games)
-- This INSERT statement populates the dim_gaming_habits table with unique combinations of playing years, playing frequency, playing hours, and a boolean indicating if the student plays games.
SELECT DISTINCT
    "Playing Years",
    "Playing Often",
    "Playing Hours",
    -- This CASE statement derives the plays_games boolean value. If "Playing Years" is greater than 0, it's considered TRUE (1), otherwise FALSE (0).
    CASE WHEN "Playing Years" > 0 THEN 1 ELSE 0 END
FROM raw_import;

-- Insert fact data with joins to dimension tables
INSERT INTO fact_grades (
    student_id, school_id, parent_id, gaming_id,
    grade, percentage, error_flag
)
-- This INSERT statement populates the fact_grades table with grade information, linking records to the dimension tables.
SELECT
    -- This selects the student_id from the dim_student table by joining on the "Sex" column.
    s.student_id,
    -- This selects the school_id from the dim_school table by joining on the "School Code" column.
    sc.school_id,
    -- This selects the parent_id from the dim_parent_background table by joining on the "Parent Revenue", "Father Education", and "Mother Education" columns.
    p.parent_id,
    -- This selects the gaming_id from the dim_gaming_habits table by joining on the "Playing Years", "Playing Often", and "Playing Hours" columns.
    g.gaming_id,
    -- This selects the "Grade" directly from the raw_import table.
    r."Grade",
    -- This selects and cleans the "Percentage" from the raw_import table. It replaces commas with periods and removes the percentage sign, then casts it to a DECIMAL data type.
    CAST(REPLACE(REPLACE(r."Percentage", ',', '.'), '%', '') AS DECIMAL(5,2)),
    -- This selects the "Error Check" directly from the raw_import table.
    r."Error Check"
FROM
    -- This specifies the raw_import table as the primary source of data (aliased as 'r').
    raw_import r
    -- This joins raw_import with the dim_student table (aliased as 's') on the matching "Sex".
    JOIN dim_student s ON r."Sex" = s.sex
    -- This joins raw_import with the dim_school table (aliased as 'sc') on the matching "School Code".
    JOIN dim_school sc ON r."School Code" = sc.school_code
    -- This joins raw_import with the dim_parent_background table (aliased as 'p') on the matching "Parent Revenue", "Father Education", and "Mother Education".
    JOIN dim_parent_background p ON r."Parent Revenue" = p.parent_revenue
                               AND r."Father Education" = p.father_education
                               AND r."Mother Education" = p.mother_education
    -- This joins raw_import with the dim_gaming_habits table (aliased as 'g') on the matching "Playing Years", "Playing Often", and "Playing Hours".
    JOIN dim_gaming_habits g ON r."Playing Years" = g.playing_years
                            AND r."Playing Often" = g.playing_often
                            AND r."Playing Hours" = g.playing_hours;