-- Healthcare Data Warehouse - Star Schema
-- Created: January 2026

-- Dimension Tables

-- Patient Dimension
CREATE TABLE dim_patient (
    patient_id INT PRIMARY KEY,
    patient_name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    blood_type VARCHAR(10)
);

-- Disease Dimension
CREATE TABLE dim_disease (
    disease_id SERIAL PRIMARY KEY,
    medical_condition VARCHAR(100) UNIQUE
);

-- Time Dimension
CREATE TABLE dim_time (
    time_id SERIAL PRIMARY KEY,
    admission_date DATE UNIQUE,
    discharge_date DATE,
    month INT,
    year INT,
    quarter INT,
    day_of_week VARCHAR(10)
);

-- Doctor Dimension
CREATE TABLE dim_doctor (
    doctor_id SERIAL PRIMARY KEY,
    doctor_name VARCHAR(100) UNIQUE
);

-- Hospital Dimension
CREATE TABLE dim_hospital (
    hospital_id SERIAL PRIMARY KEY,
    hospital_name VARCHAR(100) UNIQUE
);

-- Insurance Dimension
CREATE TABLE dim_insurance (
    insurance_id SERIAL PRIMARY KEY,
    insurance_provider VARCHAR(100) UNIQUE
);

-- Fact Table

-- Admissions Fact Table
CREATE TABLE fact_admissions (
    admission_id SERIAL PRIMARY KEY,
    patient_id INT,
    disease_id INT,
    time_id INT,
    doctor_id INT,
    hospital_id INT,
    insurance_id INT,
    billing_amount DECIMAL(10, 2),
    room_number INT,
    admission_type VARCHAR(50),
    medication VARCHAR(200),
    test_results VARCHAR(50),
    FOREIGN KEY (patient_id) REFERENCES dim_patient(patient_id),
    FOREIGN KEY (disease_id) REFERENCES dim_disease(disease_id),
    FOREIGN KEY (time_id) REFERENCES dim_time(time_id),
    FOREIGN KEY (doctor_id) REFERENCES dim_doctor(doctor_id),
    FOREIGN KEY (hospital_id) REFERENCES dim_hospital(hospital_id),
    FOREIGN KEY (insurance_id) REFERENCES dim_insurance(insurance_id)
);

-- Create indexes for better query performance
CREATE INDEX idx_fact_patient ON fact_admissions(patient_id);
CREATE INDEX idx_fact_disease ON fact_admissions(disease_id);
CREATE INDEX idx_fact_time ON fact_admissions(time_id);
CREATE INDEX idx_fact_doctor ON fact_admissions(doctor_id);
CREATE INDEX idx_fact_hospital ON fact_admissions(hospital_id);
CREATE INDEX idx_fact_insurance ON fact_admissions(insurance_id);
