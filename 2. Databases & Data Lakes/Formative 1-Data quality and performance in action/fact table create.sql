-- Create fact table

-- This table stores the actual grades and related information, linking to the dimension tables.
CREATE TABLE fact_grades (
    -- A unique identifier for each grade record. It's the primary key for this table and automatically increments.
    grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- A foreign key referencing the dim_student table, indicating which student achieved this grade. It is a required field.
    student_id INTEGER NOT NULL,
    -- A foreign key referencing the dim_school table, indicating which school the grade was achieved at. It is a required field.
    school_id INTEGER NOT NULL,
    -- A foreign key referencing the dim_parent_background table, linking the grade to the parent's background information. It is a required field.
    parent_id INTEGER NOT NULL,
    -- A foreign key referencing the dim_gaming_habits table, linking the grade to the student's gaming habits. It is a required field.
    gaming_id INTEGER NOT NULL,
    -- The actual grade achieved, stored as a decimal number with up to 5 total digits and 2 decimal places. It is a required field and has a check constraint 
    grade DECIMAL(5,2) NOT NULL CHECK (grade),
    -- The grade represented as a percentage, stored as a decimal number with up to 5 total digits and 2 decimal places. It is a required field and has a check constraint.
    percentage DECIMAL(5,2) NOT NULL CHECK (percentage),
    -- An optional text field that can be used to flag any issues or anomalies related to this grade record.
    error_flag VARCHAR(10),
    -- FOREIGN KEY (student_id) REFERENCES dim_student(student_id): This establishes a foreign key relationship with the student_id column in the dim_student table, ensuring data integrity.
    FOREIGN KEY (student_id) REFERENCES dim_student(student_id),
    -- FOREIGN KEY (school_id) REFERENCES dim_school(school_id): This establishes a foreign key relationship with the school_id column in the dim_school table, ensuring data integrity.
    FOREIGN KEY (school_id) REFERENCES dim_school(school_id),
    -- FOREIGN KEY (parent_id) REFERENCES dim_parent_background(parent_id): This establishes a foreign key relationship with the parent_id column in the dim_parent_background table, ensuring data integrity.
    FOREIGN KEY (parent_id) REFERENCES dim_parent_background(parent_id),
    -- FOREIGN KEY (gaming_id) REFERENCES dim_gaming_habits(gaming_id): This establishes a foreign key relationship with the gaming_id column in the dim_gaming_habits table, ensuring data integrity.
    FOREIGN KEY (gaming_id) REFERENCES dim_gaming_habits(gaming_id)
);