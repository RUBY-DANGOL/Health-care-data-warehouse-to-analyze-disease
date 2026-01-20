# 🏥 Healthcare Data Warehouse & Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)

A complete **OLAP (Online Analytical Processing)** data warehouse solution for healthcare analytics, featuring automated ETL pipelines, interactive SQL query interface, and dynamic data visualizations.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [System Architecture](#-system-architecture)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [ETL Pipeline](#-etl-pipeline)
- [Analytics](#-analytics)
- [Web Interface](#-web-interface)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Overview

This project implements a **production-grade healthcare data warehouse** with a star schema design, processing **55,500+ patient admission records** across 6 medical conditions, enabling real-time business intelligence and data-driven decision making.

### Key Capabilities

- ✅ **ETL Pipeline**: Automated Extract-Transform-Load from CSV to PostgreSQL
- ✅ **Star Schema**: Optimized OLAP design with 1 fact table + 6 dimension tables
- ✅ **Interactive Web UI**: SQL editor with auto-generated visualizations
- ✅ **14 Pre-built Analytics**: Disease trends, billing analysis, patient demographics
- ✅ **Docker Deployment**: Containerized for easy setup and portability
- ✅ **Real-time Visualizations**: Plotly charts (pie, bar, line) with hover interactions

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          DATA SOURCES                                │
│                   healthcare_dataset.csv (55,500 rows)              │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        ETL PIPELINE (etl.py)                         │
│  ┌──────────┐      ┌──────────────┐      ┌─────────────┐          │
│  │ EXTRACT  │ ───► │  TRANSFORM   │ ───► │    LOAD     │          │
│  │ Read CSV │      │ Hash IDs     │      │ Dimensions  │          │
│  │          │      │ Parse Dates  │      │ Facts       │          │
│  └──────────┘      │ Deduplicate  │      └─────────────┘          │
│                    └──────────────┘                                 │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│              POSTGRESQL DATA WAREHOUSE (Docker)                      │
│                                                                      │
│                         STAR SCHEMA                                  │
│                                                                      │
│        dim_patient          dim_disease         dim_doctor          │
│              │                    │                   │              │
│              │                    ▼                   │              │
│              └────────────► fact_admissions ◄─────────┘              │
│                                   ▲                                  │
│              ┌────────────────────┼───────────────────┐              │
│              │                    │                   │              │
│        dim_time           dim_hospital         dim_insurance        │
│                                                                      │
│  📊 55,500 admissions | 48,777 patients | 1,827 dates               │
└────────────────────────────┬────────────────────────────────────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
┌──────────────────┐  ┌──────────────┐  ┌──────────────────┐
│   WEB UI         │  │  ANALYTICS   │  │   ADMINER        │
│   Flask + Plotly │  │  Python CLI  │  │   DB Manager     │
│   Port: 5000     │  │  14 Queries  │  │   Port: 8080     │
│                  │  │              │  │                  │
│ • SQL Editor     │  │ • Trends     │  │ • Browse Tables  │
│ • 8 Templates    │  │ • Revenue    │  │ • Run Queries    │
│ • Auto Charts    │  │ • Demographics│ │ • Export Data    │
│ • Data Tables    │  │              │  │                  │
└──────────────────┘  └──────────────┘  └──────────────────┘
```

### Data Flow Diagram

```
CSV File (55,500 rows)
       │
       ▼
[EXTRACT] - pandas.read_csv()
       │
       ▼
[TRANSFORM]
├─ Hash patient IDs (Name → patient_id)
├─ Parse dates (string → datetime)
├─ Extract time components (year, month, day, quarter)
├─ Deduplicate patients (48,777 unique)
└─ Clean & validate data
       │
       ▼
[LOAD DIMENSIONS] - Load reference tables first
├─ 1. dim_patient (48,777 rows)
├─ 2. dim_disease (6 rows)
├─ 3. dim_time (1,827 rows)
├─ 4. dim_doctor (40,341 rows)
├─ 5. dim_hospital (39,876 rows)
└─ 6. dim_insurance (5 rows)
       │
       ▼
[LOAD FACTS] - Link to dimensions via foreign keys
└─ fact_admissions (55,500 rows)
       │
       ▼
[READY FOR ANALYSIS] - Query via Web UI, Analytics Script, or Adminer
```

---

## ✨ Features

### 🔄 ETL Pipeline
- **Automated Data Loading**: One-command CSV to database ingestion
- **Data Quality**: Automatic deduplication and validation
- **ID Generation**: Consistent patient ID hashing across loads
- **Error Handling**: Graceful failure with detailed logging
- **Incremental Updates**: Clear & reload capability

### 📊 Analytics & Reporting
- **Disease Distribution**: Pie charts showing case distribution across conditions
- **Monthly Trends**: Time-series analysis of admission patterns
- **Revenue Analysis**: Billing insights by insurance provider
- **Patient Demographics**: Age, gender, blood type distributions
- **Hospital Performance**: Rankings by patient volume and revenue
- **Doctor Workload**: Patient load distribution
- **Seasonal Patterns**: Admission trends across months/quarters

### 🌐 Web Interface
- **SQL Editor**: Write and execute custom queries
- **8 Query Templates**: Pre-built analyses ready to run
- **Auto Visualization**: Intelligent chart type selection
- **Interactive Charts**: Plotly-powered hover, zoom, pan
- **Data Tables**: Paginated results with all query data
- **Schema Browser**: Explore database structure
- **Responsive Design**: Works on desktop and tablets

### 🐳 Docker Deployment
- **One-Command Setup**: `docker-compose up -d`
- **PostgreSQL 15**: Latest stable database version
- **Adminer**: Web-based database management
- **Data Persistence**: Volumes for permanent storage
- **Health Checks**: Automatic container monitoring

---

## 🛠️ Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Database** | PostgreSQL | 15 | OLAP data warehouse |
| **Backend** | Python | 3.11+ | ETL & web server |
| **Web Framework** | Flask | 3.1.2 | REST API & UI |
| **Data Processing** | Pandas | Latest | ETL transformations |
| **Visualization** | Plotly | 6.5.0 | Interactive charts |
| **ORM** | SQLAlchemy | Latest | Database connectivity |
| **Containerization** | Docker Compose | Latest | Deployment orchestration |
| **DB Admin** | Adminer | Latest | Database management UI |

### Python Dependencies
```
flask==3.1.2
pandas
sqlalchemy
psycopg2-binary
plotly==6.5.0
```

---

## 📁 Project Structure

```
healthcare_dw/
│
├── 📂 data/                          # Raw data storage
│   └── healthcare_dataset.csv        # Source data (55,500 rows)
│
├── 📂 db/                            # Database definitions
│   └── init.sql                      # Star schema DDL
│
├── 📂 etl/                           # ETL pipeline
│   └── etl.py                        # Extract-Transform-Load script
│
├── 📂 analytics/                     # Analysis scripts
│   └── analysis.py                   # 14 pre-built analytics queries
│
├── 📂 webapp/                        # Web application
│   ├── app.py                        # Flask server + API
│   └── templates/
│       └── index.html                # Frontend UI
│
├── 📄 docker-compose.yml             # Container orchestration
├── 📄 README.md                      # Documentation
└── 📄 requirements.txt               # Python dependencies
```

---

## 🗄️ Database Schema

### Star Schema Design

```
┌──────────────────────────────────────────────────────────────────────┐
│                        FACT TABLE                                     │
│                    fact_admissions                                    │
│ ──────────────────────────────────────────────────────────────────── │
│ admission_id (PK)        │ INT                                        │
│ patient_id (FK)          │ INT ──────────┐                            │
│ disease_id (FK)          │ INT ──────┐   │                            │
│ admission_date_id (FK)   │ INT ───┐  │   │                            │
│ discharge_date_id (FK)   │ INT    │  │   │                            │
│ doctor_id (FK)           │ INT    │  │   │                            │
│ hospital_id (FK)         │ INT    │  │   │                            │
│ insurance_id (FK)        │ INT    │  │   │                            │
│ billing_amount           │ DECIMAL│  │   │                            │
│ room_number              │ INT    │  │   │                            │
│ admission_type           │ VARCHAR│  │   │                            │
│ test_results             │ VARCHAR│  │   │                            │
│ medication               │ VARCHAR│  │   │                            │
└──────────────────────────────────────┼──┼───┼────────────────────────┘
                                       │  │   │
        ┌──────────────────────────────┘  │   │
        │                                 │   │
        ▼                                 │   │
┌──────────────────┐                     │   │
│    dim_time      │                     │   │
├──────────────────┤                     │   │
│ time_id (PK)     │                     │   │
│ admission_date   │                     │   │
│ discharge_date   │                     │   │
│ year             │                     │   │
│ month            │                     │   │
│ day              │                     │   │
│ quarter          │                     │   │
└──────────────────┘                     │   │
                                         │   │
        ┌────────────────────────────────┘   │
        │                                    │
        ▼                                    │
┌──────────────────┐                         │
│   dim_disease    │                         │
├──────────────────┤                         │
│ disease_id (PK)  │                         │
│ medical_condition│                         │
└──────────────────┘                         │
                                             │
        ┌────────────────────────────────────┘
        │
        ▼
┌──────────────────┐
│   dim_patient    │
├──────────────────┤
│ patient_id (PK)  │
│ name             │
│ age              │
│ gender           │
│ blood_type       │
└──────────────────┘

┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   dim_doctor     │  │  dim_hospital    │  │  dim_insurance   │
├──────────────────┤  ├──────────────────┤  ├──────────────────┤
│ doctor_id (PK)   │  │ hospital_id (PK) │  │ insurance_id (PK)│
│ doctor_name      │  │ hospital_name    │  │ insurance_provider│
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

### Table Statistics

| Table | Rows | Description |
|-------|------|-------------|
| `dim_patient` | 48,777 | Patient demographics |
| `dim_disease` | 6 | Medical conditions |
| `dim_time` | 1,827 | Date dimensions |
| `dim_doctor` | 40,341 | Doctor names |
| `dim_hospital` | 39,876 | Hospital names |
| `dim_insurance` | 5 | Insurance providers |
| `fact_admissions` | 55,500 | Central fact table |

---

## 🚀 Installation

### Prerequisites

- **Docker Desktop** (Windows/Mac) or Docker Engine (Linux)
- **Python 3.11+**

### Step 1: Start Database Containers

```bash
cd healthcare_dw
docker-compose up -d
```

Verify containers are running:
```bash
docker-compose ps
```

### Step 2: Set Up Python Environment

```powershell
# Windows
cd ..
python -m venv env
.\env\Scripts\Activate.ps1
pip install flask plotly pandas sqlalchemy psycopg2-binary
```

```bash
# Linux/Mac
cd ..
python3 -m venv env
source env/bin/activate
pip install flask plotly pandas sqlalchemy psycopg2-binary
```

### Step 3: Load Data

```bash
cd healthcare_dw\etl
python etl.py
```

---

## 📖 Usage Guide

### Option 1: Web Interface (Recommended) ⭐

```bash
cd ..\webapp
python app.py
```

Open: **http://localhost:5000**

### Option 2: Analytics Script

```bash
cd ..\analytics
python analysis.py
```

### Option 3: Adminer

Open: **http://localhost:8080**

**Credentials:**
- Server: `postgres`
- Username: `admin`
- Password: `admin`
- Database: `healthcare_dw`

---

## 🔄 ETL Pipeline

### Workflow

```
1. EXTRACT   → Read CSV (55,500 rows)
2. TRANSFORM → Hash IDs, parse dates, deduplicate
3. LOAD      → Insert dimensions, then facts
```

### Run ETL

```bash
cd etl
python etl.py
# Expected time: 30-60 seconds
```

---

## 📊 Analytics

### Sample Query: Disease Distribution

```sql
SELECT 
    d.medical_condition,
    COUNT(*) as count
FROM fact_admissions f
JOIN dim_disease d ON f.disease_id = d.disease_id
GROUP BY d.medical_condition;
```

### Pre-built Templates

| Template | Chart | Description |
|----------|-------|-------------|
| Disease Distribution | Pie | Cases by condition |
| Monthly Trends | Line | Admissions over time |
| Hospital Performance | Bar | Revenue by hospital |
| Insurance Claims | Pie | Claims by provider |

---

## 🌐 Web Interface

### API: Execute Query

**POST** `/execute_query`

Request:
```json
{
  "query": "SELECT ...",
  "chart_type": "pie"
}
```

Response:
```json
{
  "success": true,
  "columns": [...],
  "data": [...],
  "chart": "{...plotly JSON...}"
}
```

---

## 🐛 Troubleshooting

### Containers Won't Start

```bash
docker-compose down -v
docker-compose up -d
```

### ETL Fails

```bash
# Just rerun - it clears data first
python etl.py
```

### Charts Not Rendering

- Hard refresh browser (Ctrl+Shift+R)
- Check console (F12) for errors

---

## 📈 Performance

| Operation | Time |
|-----------|------|
| Full ETL | ~45 sec |
| Simple Query | <100ms |
| Complex Join | <500ms |

---

## 🎓 OLAP Concepts

- ✅ **Star Schema**: 1 fact + 6 dimensions
- ✅ **ETL**: Extract-Transform-Load
- ✅ **OLAP Ops**: Slice, Dice, Drill, Roll-up
- ✅ **BI**: Pre-aggregated queries & viz

---

## 📊 Project Stats

```
Lines of Code:     ~2,500
Python Files:      4
SQL Files:         1
Docker Containers: 2
Database Tables:   7
Pre-built Queries: 22
Data Records:      55,500
```

---

<div align="center">

**🏥 Production-Grade OLAP Data Warehouse**

**Built for Healthcare Analytics | January 2026**

</div>
