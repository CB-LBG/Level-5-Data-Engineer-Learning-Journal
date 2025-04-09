-- Create dimension tables

-- This table stores information about the students.
CREATE TABLE dim_student (
    -- student_id: A unique identifier for each student. It's the primary key for this table and automatically increments.
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- sex: The gender of the student (e.g., 'Male', 'Female'). It is a required field.
    sex VARCHAR(10) NOT NULL
);

-- This table stores information about the schools.
CREATE TABLE dim_school (
    -- school_id: A unique identifier for each school. It's the primary key and automatically increments.
    school_id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- school_code: A unique numerical code assigned to each school. It is a required field.
    school_code INTEGER NOT NULL
);

-- This table stores information about the parents' background.
CREATE TABLE dim_parent_background (
    -- parent_id: A unique identifier for each parent background record. It's the primary key and automatically increments.
    parent_id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- parent_revenue: A categorical representation of the parents' income level (0 to 4). It's a required field and has a check constraint to ensure values are within the valid range.
    parent_revenue INTEGER NOT NULL CHECK (parent_revenue BETWEEN 0 AND 4),
    -- father_education: A categorical representation of the father's highest level of education (0 to 6). It's a required field with a check constraint for valid values.
    father_education INTEGER NOT NULL CHECK (father_education BETWEEN 0 AND 6),
    -- mother_education: A categorical representation of the mother's highest level of education (0 to 6). It's a required field with a check constraint for valid values.
    mother_education INTEGER NOT NULL CHECK (mother_education BETWEEN 0 AND 6)
);

-- This table stores information about students' gaming habits.
CREATE TABLE dim_gaming_habits (
    -- gaming_id: A unique identifier for each gaming habit record. It's the primary key and automatically increments.
    gaming_id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- playing_years: The number of years the student has been playing games (0 to 4). It's a required field with a check constraint for valid values.
    playing_years INTEGER NOT NULL CHECK (playing_years BETWEEN 0 AND 4),
    -- playing_often: A categorical representation of how often the student plays games (0 to 5). It's a required field with a check constraint for valid values.
    playing_often INTEGER NOT NULL CHECK (playing_often BETWEEN 0 AND 5),
    -- playing_hours: A categorical representation of the number of hours the student spends playing games (0 to 5). It's a required field with a check constraint for valid values.
    playing_hours INTEGER NOT NULL CHECK (playing_hours BETWEEN 0 AND 5),
    -- plays_games: A boolean value indicating whether the student plays games (TRUE or FALSE). It is a required field.
    plays_games BOOLEAN NOT NULL
);
