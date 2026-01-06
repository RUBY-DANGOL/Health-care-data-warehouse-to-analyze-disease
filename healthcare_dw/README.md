# 🏥 Healthcare Data Warehouse Project

A complete ETL pipeline and data warehouse solution for healthcare analytics using PostgreSQL and Docker.

## 📋 Project Overview

This project implements a **Star Schema Data Warehouse** for healthcare data analysis with:
- ✅ Automated ETL pipeline
- ✅ Dockerized PostgreSQL database
- ✅ Dimensional modeling (Star Schema)
- ✅ Healthcare analytics queries

## 🏗️ Architecture

```
ETL Process: Extract → Transform → Load

Source Data (CSV) → Python ETL → PostgreSQL Data Warehouse
```

### Star Schema Design

**Dimension Tables:**
- `dim_patient` - Patient demographics
- `dim_disease` - Medical conditions
- `dim_time` - Admission/discharge dates
- `dim_doctor` - Doctor information
- `dim_hospital` - Hospital details
- `dim_insurance` - Insurance providers

**Fact Table:**
- `fact_admissions` - Central fact table with all metrics

## 📁 Project Structure

```
healthcare_dw/
│
├── data/
│   └── healthcare_dataset.csv      # Source data
│
├── etl/
│   └── etl.py                      # ETL pipeline script
│
├── db/
│   └── init.sql                    # Database schema
│
├── docker-compose.yml              # Docker configuration
└── README.md                       # This file
```

## 🚀 Setup Instructions

### Prerequisites

- Docker Desktop installed
- Python 3.8+
- pip (Python package manager)

### Step 1: Install Python Dependencies

```powershell
pip install pandas sqlalchemy psycopg2-binary
```

### Step 2: Start PostgreSQL Database

```powershell
docker-compose up -d
```

This will:
- Pull PostgreSQL 15 image
- Create `healthcare_dw` database
- Initialize schema from `init.sql`
- Expose database on port 5432

### Step 3: Verify Database is Running

```powershell
docker ps
```

You should see `healthcare_db` container running.

### Step 4: Run ETL Pipeline

```powershell
cd etl
python etl.py
```

The ETL process will:
1. **Extract** data from CSV
2. **Transform** data (clean, create IDs)
3. **Load** into dimension tables
4. **Load** fact table with foreign keys

## 🔍 Database Access

### Using Docker CLI

```powershell
docker exec -it healthcare_db psql -U admin -d healthcare_dw
```

### Connection Details

- **Host:** localhost
- **Port:** 5432
- **Database:** healthcare_dw
- **Username:** admin
- **Password:** admin

## 📊 Sample Queries

### 1. Top 5 Most Common Medical Conditions

```sql
SELECT 
    dd.medical_condition,
    COUNT(*) as admission_count
FROM fact_admissions fa
JOIN dim_disease dd ON fa.disease_id = dd.disease_id
GROUP BY dd.medical_condition
ORDER BY admission_count DESC
LIMIT 5;
```

### 2. Average Billing by Insurance Provider

```sql
SELECT 
    di.insurance_provider,
    ROUND(AVG(fa.billing_amount), 2) as avg_billing,
    COUNT(*) as total_admissions
FROM fact_admissions fa
JOIN dim_insurance di ON fa.insurance_id = di.insurance_id
GROUP BY di.insurance_provider
ORDER BY avg_billing DESC;
```

### 3. Monthly Admission Trends

```sql
SELECT 
    dt.year,
    dt.month,
    COUNT(*) as admissions
FROM fact_admissions fa
JOIN dim_time dt ON fa.time_id = dt.time_id
GROUP BY dt.year, dt.month
ORDER BY dt.year, dt.month;
```

### 4. Gender Distribution by Medical Condition

```sql
SELECT 
    dd.medical_condition,
    dp.gender,
    COUNT(*) as patient_count
FROM fact_admissions fa
JOIN dim_patient dp ON fa.patient_id = dp.patient_id
JOIN dim_disease dd ON fa.disease_id = dd.disease_id
GROUP BY dd.medical_condition, dp.gender
ORDER BY dd.medical_condition, patient_count DESC;
```

### 5. Hospital Performance by Billing

```sql
SELECT 
    dh.hospital_name,
    COUNT(*) as total_admissions,
    ROUND(AVG(fa.billing_amount), 2) as avg_billing,
    ROUND(SUM(fa.billing_amount), 2) as total_revenue
FROM fact_admissions fa
JOIN dim_hospital dh ON fa.hospital_id = dh.hospital_id
GROUP BY dh.hospital_name
ORDER BY total_revenue DESC;
```

### 6. Age Group Analysis

```sql
SELECT 
    CASE 
        WHEN dp.age < 18 THEN 'Child'
        WHEN dp.age BETWEEN 18 AND 35 THEN 'Young Adult'
        WHEN dp.age BETWEEN 36 AND 55 THEN 'Adult'
        ELSE 'Senior'
    END as age_group,
    COUNT(*) as admission_count,
    ROUND(AVG(fa.billing_amount), 2) as avg_billing
FROM fact_admissions fa
JOIN dim_patient dp ON fa.patient_id = dp.patient_id
GROUP BY age_group
ORDER BY admission_count DESC;
```

## 🛠️ Useful Commands

### Check Database Tables

```sql
\dt
```

### View Table Structure

```sql
\d dim_patient
\d fact_admissions
```

### Count Records

```sql
SELECT COUNT(*) FROM fact_admissions;
SELECT COUNT(*) FROM dim_patient;
SELECT COUNT(*) FROM dim_disease;
```

### Reset Database (Clean Start)

```powershell
# Stop and remove containers
docker-compose down -v

# Start fresh
docker-compose up -d

# Re-run ETL
cd etl
python etl.py
```

## 🎯 Why This Architecture?

### Star Schema Benefits
- ✅ **Simple queries** - Easy joins
- ✅ **Fast performance** - Optimized for analytics
- ✅ **Easy to understand** - Business-friendly
- ✅ **Scalable** - Add dimensions easily

### Docker Benefits
- ✅ **Portable** - Works on any system
- ✅ **Reproducible** - Same setup every time
- ✅ **No manual setup** - One command to start
- ✅ **Easy submission** - Share entire project

## 📈 Analytics Use Cases

1. **Disease Trend Analysis** - Track seasonal patterns
2. **Revenue Analytics** - Billing insights by various dimensions
3. **Patient Demographics** - Age, gender distributions
4. **Hospital Performance** - Compare facilities
5. **Insurance Analytics** - Provider comparisons
6. **Doctor Performance** - Patient load, outcomes

## 🔧 Troubleshooting

### ETL Fails with Connection Error
```powershell
# Check if database is running
docker ps

# Restart if needed
docker-compose restart
```

### Port 5432 Already in Use
```yaml
# Edit docker-compose.yml, change ports:
ports:
  - "5433:5432"  # Use 5433 instead
```

### Re-run ETL with Fresh Data
```sql
-- Connect to database
docker exec -it healthcare_db psql -U admin -d healthcare_dw

-- Truncate tables (preserves structure)
TRUNCATE fact_admissions CASCADE;
TRUNCATE dim_patient CASCADE;
TRUNCATE dim_disease RESTART IDENTITY CASCADE;
TRUNCATE dim_time RESTART IDENTITY CASCADE;
TRUNCATE dim_doctor RESTART IDENTITY CASCADE;
TRUNCATE dim_hospital RESTART IDENTITY CASCADE;
TRUNCATE dim_insurance RESTART IDENTITY CASCADE;
```

## 📝 Next Steps

1. **Add More Analytics**
   - Create views for common queries
   - Build aggregation tables
   - Add time-series analysis

2. **Visualization**
   - Connect to Power BI / Tableau
   - Build dashboards
   - Create reports

3. **Automation**
   - Schedule ETL with cron
   - Add data validation
   - Implement logging

## 👨‍💻 Author

Healthcare Data Warehouse Project  
Created: January 2026

## 📄 License

Free to use for educational purposes.

---

**Happy Analytics! 📊**
