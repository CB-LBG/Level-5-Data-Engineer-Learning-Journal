-- Average grade by gaming frequency
SELECT
    -- Selects the 'playing_often' category from the dim_gaming_habits table. This will be used to group the results.
    gh.playing_often,
    -- Calculates the average of the 'grade' column from the fact_grades table for each gaming frequency group. The result is aliased as 'avg_grade'.
    AVG(fg.grade) as avg_grade,
    -- Counts the number of students (grade records) within each gaming frequency group. The result is aliased as 'student_count'.
    COUNT(*) as student_count
FROM
    -- Specifies the fact_grades table (aliased as 'fg') as the primary table for this query.
    fact_grades fg
JOIN
    -- Joins the fact_grades table with the dim_gaming_habits table (aliased as 'gh') using the common 'gaming_id' column. This links each grade record to the corresponding gaming habits of the student.
    dim_gaming_habits gh ON fg.gaming_id = gh.gaming_id
GROUP BY
    -- Groups the result set based on the 'playing_often' column from the dim_gaming_habits table. This allows the AVG and COUNT functions to operate on each distinct gaming frequency.
    gh.playing_often
ORDER BY
    -- Orders the final result set by the 'playing_often' column in ascending order. This makes it easier to see the trend of average grades across different gaming frequencies.
    gh.playing_often;