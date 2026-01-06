"""
Healthcare Data Warehouse ETL Pipeline
Extract, Transform, Load process for healthcare dataset
"""

import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
import hashlib

# Database connection
DATABASE_URL = "postgresql://admin:admin@localhost:5432/healthcare_dw"
engine = create_engine(DATABASE_URL)

def clear_database():
    """Clear all tables before loading new data"""
    print("\n🗑️  Clearing existing data...")
    
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE fact_admissions CASCADE"))
        conn.execute(text("TRUNCATE TABLE dim_patient CASCADE"))
        conn.execute(text("TRUNCATE TABLE dim_disease RESTART IDENTITY CASCADE"))
        conn.execute(text("TRUNCATE TABLE dim_time RESTART IDENTITY CASCADE"))
        conn.execute(text("TRUNCATE TABLE dim_doctor RESTART IDENTITY CASCADE"))
        conn.execute(text("TRUNCATE TABLE dim_hospital RESTART IDENTITY CASCADE"))
        conn.execute(text("TRUNCATE TABLE dim_insurance RESTART IDENTITY CASCADE"))
        conn.commit()
    
    print("✅ Database cleared")

def extract_data():
    """Extract data from CSV file"""
    print("📊 Extracting data from healthcare_dataset.csv...")
    df = pd.read_csv("../data/healthcare_dataset.csv")
    print(f"✅ Extracted {len(df)} records")
    return df

def transform_data(df):
    """Transform data for data warehouse"""
    print("\n🔄 Transforming data...")
    
    # Clean column names
    df.columns = df.columns.str.strip()
    
    # Convert dates to datetime
    df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
    df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])
    
    # Generate patient_id using hash of name
    df['patient_id'] = df['Name'].apply(
        lambda x: int(hashlib.md5(x.encode()).hexdigest()[:8], 16) % 1000000
    )
    
    print("✅ Data transformation completed")
    return df

def load_dim_patient(df):
    """Load patient dimension"""
    print("\n📥 Loading dim_patient...")
    
    df_patient = df[['patient_id', 'Name', 'Age', 'Gender', 'Blood Type']].copy()
    df_patient.columns = ['patient_id', 'patient_name', 'age', 'gender', 'blood_type']
    
    # Drop duplicates based on patient_id only (keep first occurrence)
    df_patient = df_patient.drop_duplicates(subset=['patient_id'], keep='first')
    
    # Load to database
    df_patient.to_sql('dim_patient', engine, if_exists='append', index=False)
    print(f"✅ Loaded {len(df_patient)} patients")

def load_dim_disease(df):
    """Load disease dimension"""
    print("\n📥 Loading dim_disease...")
    
    df_disease = df[['Medical Condition']].drop_duplicates()
    df_disease.columns = ['medical_condition']
    
    # Load to database
    df_disease.to_sql('dim_disease', engine, if_exists='append', index=False)
    print(f"✅ Loaded {len(df_disease)} medical conditions")

def load_dim_time(df):
    """Load time dimension"""
    print("\n📥 Loading dim_time...")
    
    # Create time dimension from admission dates
    df_time = df[['Date of Admission', 'Discharge Date']].copy()
    df_time.columns = ['admission_date', 'discharge_date']
    
    # Drop duplicates based on admission_date (unique constraint)
    df_time = df_time.drop_duplicates(subset=['admission_date'], keep='first')
    
    # Extract time attributes
    df_time['month'] = df_time['admission_date'].dt.month
    df_time['year'] = df_time['admission_date'].dt.year
    df_time['quarter'] = df_time['admission_date'].dt.quarter
    df_time['day_of_week'] = df_time['admission_date'].dt.day_name()
    
    # Load to database
    df_time.to_sql('dim_time', engine, if_exists='append', index=False)
    print(f"✅ Loaded {len(df_time)} time records")

def load_dim_doctor(df):
    """Load doctor dimension"""
    print("\n📥 Loading dim_doctor...")
    
    df_doctor = df[['Doctor']].drop_duplicates()
    df_doctor.columns = ['doctor_name']
    
    df_doctor.to_sql('dim_doctor', engine, if_exists='append', index=False)
    print(f"✅ Loaded {len(df_doctor)} doctors")

def load_dim_hospital(df):
    """Load hospital dimension"""
    print("\n📥 Loading dim_hospital...")
    
    df_hospital = df[['Hospital']].drop_duplicates()
    df_hospital.columns = ['hospital_name']
    
    df_hospital.to_sql('dim_hospital', engine, if_exists='append', index=False)
    print(f"✅ Loaded {len(df_hospital)} hospitals")

def load_dim_insurance(df):
    """Load insurance dimension"""
    print("\n📥 Loading dim_insurance...")
    
    df_insurance = df[['Insurance Provider']].drop_duplicates()
    df_insurance.columns = ['insurance_provider']
    
    df_insurance.to_sql('dim_insurance', engine, if_exists='append', index=False)
    print(f"✅ Loaded {len(df_insurance)} insurance providers")

def load_fact_admissions(df):
    """Load fact table with foreign keys"""
    print("\n📥 Loading fact_admissions...")
    
    # Get foreign keys from dimension tables
    with engine.connect() as conn:
        # Get disease IDs
        disease_map = pd.read_sql(
            "SELECT disease_id, medical_condition FROM dim_disease", conn
        )
        
        # Get time IDs
        time_map = pd.read_sql(
            "SELECT time_id, admission_date FROM dim_time", conn
        )
        # Convert admission_date to datetime for proper merging
        time_map['admission_date'] = pd.to_datetime(time_map['admission_date'])
        
        # Get doctor IDs
        doctor_map = pd.read_sql(
            "SELECT doctor_id, doctor_name FROM dim_doctor", conn
        )
        
        # Get hospital IDs
        hospital_map = pd.read_sql(
            "SELECT hospital_id, hospital_name FROM dim_hospital", conn
        )
        
        # Get insurance IDs
        insurance_map = pd.read_sql(
            "SELECT insurance_id, insurance_provider FROM dim_insurance", conn
        )
    
    # Prepare fact table data
    df_fact = df.copy()
    
    # Merge to get foreign keys
    df_fact = df_fact.merge(
        disease_map, 
        left_on='Medical Condition', 
        right_on='medical_condition', 
        how='left'
    )
    
    df_fact = df_fact.merge(
        time_map, 
        left_on='Date of Admission', 
        right_on='admission_date', 
        how='left'
    )
    
    df_fact = df_fact.merge(
        doctor_map, 
        left_on='Doctor', 
        right_on='doctor_name', 
        how='left'
    )
    
    df_fact = df_fact.merge(
        hospital_map, 
        left_on='Hospital', 
        right_on='hospital_name', 
        how='left'
    )
    
    df_fact = df_fact.merge(
        insurance_map, 
        left_on='Insurance Provider', 
        right_on='insurance_provider', 
        how='left'
    )
    
    # Select columns for fact table
    df_fact_final = df_fact[[
        'patient_id', 'disease_id', 'time_id', 'doctor_id', 
        'hospital_id', 'insurance_id', 'Billing Amount', 
        'Room Number', 'Admission Type', 'Medication', 'Test Results'
    ]]
    
    df_fact_final.columns = [
        'patient_id', 'disease_id', 'time_id', 'doctor_id',
        'hospital_id', 'insurance_id', 'billing_amount',
        'room_number', 'admission_type', 'medication', 'test_results'
    ]
    
    # Load to database
    df_fact_final.to_sql('fact_admissions', engine, if_exists='append', index=False)
    print(f"✅ Loaded {len(df_fact_final)} admission records")

def main():
    """Main ETL process"""
    print("=" * 60)
    print("🏥 HEALTHCARE DATA WAREHOUSE ETL PIPELINE")
    print("=" * 60)
    
    try:
        # Clear existing data
        clear_database()
        
        # Extract
        df = extract_data()
        
        # Transform
        df = transform_data(df)
        
        # Load Dimensions
        load_dim_patient(df)
        load_dim_disease(df)
        load_dim_time(df)
        load_dim_doctor(df)
        load_dim_hospital(df)
        load_dim_insurance(df)
        
        # Load Fact Table
        load_fact_admissions(df)
        
        print("\n" + "=" * 60)
        print("✅ ETL PROCESS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ETL Error: {e}")
        raise

if __name__ == "__main__":
    main()
